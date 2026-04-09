#!/usr/bin/env bash
set -euo pipefail

ROOT="${ROOT:-$HOME/code}"
HUB_ROOT="${HUB_ROOT:-$ROOT/jpglabs/docs}"
INFRA_ROOT="$HUB_ROOT"
STATE_ROOT="$HUB_ROOT/infrastructure/local-dev"
LOG_DIR="$STATE_ROOT/logs"
RUN_DIR="$STATE_ROOT/run"
BOOTSTRAP="$HUB_ROOT/scripts/infrastructure/local-dev-bootstrap.sh"
LOCALHOST="${LOCALHOST:-localhost}"

mkdir -p "$LOG_DIR" "$RUN_DIR"

service_port() {
  case "$1" in
    portfolio-fe) echo 8082 ;;
    portfolio-be) echo 3000 ;;
    hub) echo 3001 ;;
    gobarber-be) echo 3333 ;;
    gobarber-fe) echo 8084 ;;
    gobarber-db) echo 5432 ;;
    *) return 1 ;;
  esac
}

service_dir() {
  case "$1" in
    portfolio-fe) echo "$ROOT/jpglabs/portfolio-frontend" ;;
    portfolio-be) echo "$ROOT/jpglabs/portfolio-backend" ;;
    hub) echo "$ROOT/jpglabs/knowledge-hub-app" ;;
    gobarber-db|gobarber-be) echo "$ROOT/backend-goBarber" ;;
    gobarber-fe) echo "$ROOT/frontend-gobarber" ;;
    *) return 1 ;;
  esac
}

pid_file() { echo "$RUN_DIR/$1.pid"; }
log_file() { echo "$LOG_DIR/$1.log"; }

is_pid_running() {
  local pid="$1"
  [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null
}

saved_pid() {
  local file
  file="$(pid_file "$1")"
  if [[ -f "$file" ]]; then
    cat "$file"
  else
    true
  fi
}

port_owner() {
  lsof -nP -iTCP:"$1" -sTCP:LISTEN -t 2>/dev/null | head -n 1 || true
}

process_cwd() {
  lsof -a -p "$1" -d cwd -Fn 2>/dev/null | sed -n 's/^n//p' | head -n 1 || true
}

require_port_available() {
  local service="$1"
  local expected_dir="$2"
  local port owner pid owner_cwd
  port="$(service_port "$service")"
  owner="$(port_owner "$port")"
  pid="$(saved_pid "$service")"
  if [[ -n "$owner" && "$owner" != "$pid" ]]; then
    owner_cwd="$(process_cwd "$owner")"
    if [[ -n "$owner_cwd" && "$owner_cwd" == "$expected_dir" ]]; then
      echo "$owner" > "$(pid_file "$service")"
      echo "$service already running (adopted PID $owner)"
      return 2
    fi
    echo "ERROR: port $port is already in use by PID $owner; cannot start $service" >&2
    return 1
  fi
}

start_bg() {
  local service="$1"
  local dir="$2"
  local command="$3"
  local pid log rc
  pid="$(saved_pid "$service")"
  log="$(log_file "$service")"

  if [[ -n "$pid" ]] && is_pid_running "$pid"; then
    echo "$service already running (PID $pid)"
    return 0
  fi

  set +e
  require_port_available "$service" "$dir"
  rc=$?
  set -e
  if [[ "$rc" -eq 2 ]]; then
    return 0
  elif [[ "$rc" -ne 0 ]]; then
    return "$rc"
  fi

  nohup bash -lc "cd '$dir' && $command" >> "$log" 2>&1 &
  echo $! > "$(pid_file "$service")"
  echo "started $service (PID $(cat "$(pid_file "$service")"))"
}

stop_bg() {
  local service="$1"
  local pid
  pid="$(saved_pid "$service")"
  if [[ -z "$pid" ]]; then
    echo "$service not running"
    return 0
  fi
  if is_pid_running "$pid"; then
    kill "$pid" 2>/dev/null || true
    sleep 2
    if is_pid_running "$pid"; then
      kill -9 "$pid" 2>/dev/null || true
    fi
  fi
  rm -f "$(pid_file "$service")"
  echo "stopped $service"
}

http_code() {
  curl -s -o /dev/null -w '%{http_code}' --max-time 2 "$1" 2>/dev/null || echo 000
}

wait_for_http() {
  local url="$1"
  local attempts="${2:-60}"
  local i code
  for (( i=1; i<=attempts; i++ )); do
    code="$(http_code "$url")"
    if [[ "$code" =~ ^[1234][0-9][0-9]$ ]]; then
      return 0
    fi
    sleep 1
  done
  return 1
}

wait_for_port() {
  local port="$1"
  local attempts="${2:-60}"
  local i
  for (( i=1; i<=attempts; i++ )); do
    if [[ -n "$(port_owner "$port")" ]]; then
      return 0
    fi
    sleep 1
  done
  return 1
}

start_service() {
  case "$1" in
    portfolio-fe)
      start_bg portfolio-fe "$(service_dir portfolio-fe)" "npm run dev -- --host $LOCALHOST --port 8082"
      wait_for_http "http://$LOCALHOST:8082" || { tail -n 40 "$(log_file portfolio-fe)"; return 1; }
      ;;
    portfolio-be)
      bash "$BOOTSTRAP"
      start_bg portfolio-be "$(service_dir portfolio-be)" "npm run dev -- --hostname $LOCALHOST --port 3000"
      wait_for_http "http://$LOCALHOST:3000" || { tail -n 40 "$(log_file portfolio-be)"; return 1; }
      ;;
    hub)
      start_bg hub "$(service_dir hub)" "npm run dev -- --hostname $LOCALHOST --port 3001"
      wait_for_http "http://$LOCALHOST:3001/api/health" || { tail -n 60 "$(log_file hub)"; return 1; }
      ;;
    gobarber-db)
      (cd "$(service_dir gobarber-db)" && docker compose up -d db)
      wait_for_port 5432 || return 1
      echo "started gobarber-db"
      ;;
    gobarber-be)
      start_service gobarber-db
      start_bg gobarber-be "$(service_dir gobarber-be)" "npm run dev:server"
      wait_for_port 3333 || { tail -n 60 "$(log_file gobarber-be)"; return 1; }
      ;;
    gobarber-fe)
      start_bg gobarber-fe "$(service_dir gobarber-fe)" "npm run dev -- --host $LOCALHOST --port 8084"
      wait_for_http "http://$LOCALHOST:8084" || { tail -n 40 "$(log_file gobarber-fe)"; return 1; }
      ;;
    all)
      start_service portfolio-be
      start_service hub
      start_service gobarber-be
      start_service portfolio-fe
      start_service gobarber-fe
      ;;
    *) echo "Unknown service: $1" >&2; return 1 ;;
  esac
}

stop_service() {
  case "$1" in
    gobarber-db)
      (cd "$(service_dir gobarber-db)" && docker compose stop db >/dev/null)
      echo "stopped gobarber-db"
      ;;
    all)
      stop_bg portfolio-fe
      stop_bg portfolio-be
      stop_bg hub
      stop_bg gobarber-fe
      stop_bg gobarber-be
      stop_service gobarber-db
      ;;
    portfolio-fe|portfolio-be|hub|gobarber-be|gobarber-fe)
      stop_bg "$1"
      ;;
    *) echo "Unknown service: $1" >&2; return 1 ;;
  esac
}

status_service() {
  local service="$1"
  local port pid code
  case "$service" in
    gobarber-db)
      if (cd "$(service_dir gobarber-db)" && docker compose ps db --format json 2>/dev/null | grep -q 'running'); then
        echo "gobarber-db  UP   port=5432  docker"
      else
        echo "gobarber-db  DOWN port=5432  docker"
      fi
      return 0
      ;;
  esac

  port="$(service_port "$service")"
  pid="$(saved_pid "$service")"
  if [[ -n "$pid" ]] && is_pid_running "$pid"; then
    case "$service" in
      portfolio-fe) code="$(http_code http://$LOCALHOST:8082)" ;;
      portfolio-be) code="$(http_code http://$LOCALHOST:3000)" ;;
      hub) code="$(http_code http://$LOCALHOST:3001/api/health)" ;;
      gobarber-fe) code="$(http_code http://$LOCALHOST:8084)" ;;
      gobarber-be) code="$(http_code http://$LOCALHOST:3333)" ;;
      *) code="000" ;;
    esac
    echo "$service  UP   pid=$pid  port=$port  http=$code"
  else
    echo "$service  DOWN pid=-   port=$port"
  fi
}

logs_service() {
  case "$1" in
    gobarber-db)
      cd "$(service_dir gobarber-db)"
      docker compose logs -f db
      ;;
    portfolio-fe|portfolio-be|hub|gobarber-be|gobarber-fe)
      touch "$(log_file "$1")"
      tail -n 120 -f "$(log_file "$1")"
      ;;
    *) echo "Unknown service: $1" >&2; return 1 ;;
  esac
}

k8s_available() {
  kubectl config current-context >/dev/null 2>&1 && kubectl get nodes >/dev/null 2>&1
}

k8s_status() {
  if ! k8s_available; then
    echo "Kubernetes is not available in the current Docker Desktop context."
    return 0
  fi
  kubectl get nodes
  echo "---"
  kubectl get pods -A
}

k8s_logs() {
  local namespace="$1"
  local target="$2"
  if ! k8s_available; then
    echo "Kubernetes is not available in the current Docker Desktop context."
    return 0
  fi
  kubectl -n "$namespace" logs -f deploy/"$target" --all-containers=true
}

k8s_restart() {
  local namespace="$1"
  local deployment="$2"
  if ! k8s_available; then
    echo "Kubernetes is not available in the current Docker Desktop context."
    return 0
  fi
  kubectl -n "$namespace" rollout restart deploy/"$deployment"
  kubectl -n "$namespace" rollout status deploy/"$deployment"
}

k8s_prune() {
  if ! k8s_available; then
    echo "Kubernetes is not available in the current Docker Desktop context."
    return 0
  fi
  kubectl delete pod -A --field-selector=status.phase==Succeeded --ignore-not-found >/dev/null 2>&1 || true
  kubectl delete pod -A --field-selector=status.phase==Failed --ignore-not-found >/dev/null 2>&1 || true
  echo "Kubernetes prune completed (Succeeded/Failed pods removed where present)."
}

show_usage() {
  cat <<EOF
Usage:
  $(basename "$0") start [all|service]
  $(basename "$0") stop [all|service]
  $(basename "$0") restart [all|service]
  $(basename "$0") status
  $(basename "$0") logs <service>
  $(basename "$0") prune
  $(basename "$0") k8s-status
  $(basename "$0") k8s-logs <namespace> <deployment>
  $(basename "$0") k8s-restart <namespace> <deployment>
  $(basename "$0") k8s-prune

Services:
  portfolio-fe | portfolio-be | hub | gobarber-db | gobarber-be | gobarber-fe
EOF
}

command="${1:-status}"
service="${2:-all}"

case "$command" in
  start)
    start_service "$service"
    ;;
  stop)
    stop_service "$service"
    ;;
  restart)
    stop_service "$service"
    start_service "$service"
    ;;
  status)
    status_service portfolio-fe
    status_service portfolio-be
    status_service hub
    status_service gobarber-db
    status_service gobarber-be
    status_service gobarber-fe
    ;;
  logs)
    [[ $# -ge 2 ]] || { show_usage; exit 1; }
    logs_service "$2"
    ;;
  prune)
    docker builder prune -af >/dev/null
    docker image prune -a -f >/dev/null
    docker system df
    ;;
  k8s-status)
    k8s_status
    ;;
  k8s-logs)
    [[ $# -ge 3 ]] || { show_usage; exit 1; }
    k8s_logs "$2" "$3"
    ;;
  k8s-restart)
    [[ $# -ge 3 ]] || { show_usage; exit 1; }
    k8s_restart "$2" "$3"
    ;;
  k8s-prune)
    k8s_prune
    ;;
  *)
    show_usage
    exit 1
    ;;
esac
