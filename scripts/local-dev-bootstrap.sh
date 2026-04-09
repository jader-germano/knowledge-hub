#!/usr/bin/env bash
set -euo pipefail

ROOT="${ROOT:-$HOME/code}"
PORTFOLIO_BE="$ROOT/jpglabs/portfolio-backend"
HUB_APP="$ROOT/jpglabs/knowledge-hub-app"

portfolio_env="$PORTFOLIO_BE/.env.local"
hub_env="$HUB_APP/.env.local"

get_env_value() {
  local file="$1"
  local key="$2"
  [[ -f "$file" ]] || return 0
  python3 - "$file" "$key" <<'PY'
from pathlib import Path
import sys
path = Path(sys.argv[1])
key = sys.argv[2]
for line in path.read_text(encoding='utf-8', errors='ignore').splitlines():
    if line.startswith(key + '='):
        print(line.split('=', 1)[1])
        break
PY
}

generate_secret() {
  if command -v openssl >/dev/null 2>&1; then
    openssl rand -base64 32 | tr -d '\n'
  else
    python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(32))
PY
  fi
}

ensure_portfolio_backend_env() {
  if [[ -f "$portfolio_env" ]]; then
    echo "portfolio-backend env: present"
    return 0
  fi

  local supabase_url=""
  local supabase_anon=""
  local supabase_service=""
  local nextauth_secret=""

  if [[ -f "$hub_env" ]]; then
    supabase_url="$(get_env_value "$hub_env" "NEXT_PUBLIC_SUPABASE_URL")"
    supabase_anon="$(get_env_value "$hub_env" "NEXT_PUBLIC_SUPABASE_ANON_KEY")"
    supabase_service="$(get_env_value "$hub_env" "SUPABASE_SERVICE_ROLE_KEY")"
  fi

  nextauth_secret="$(generate_secret)"

  cat > "$portfolio_env" <<EOF
NEXT_PUBLIC_SUPABASE_URL=${supabase_url}
NEXT_PUBLIC_SUPABASE_ANON_KEY=${supabase_anon}
SUPABASE_SERVICE_ROLE_KEY=${supabase_service}
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=${nextauth_secret}
PI_RUNTIME_DSV_URL=http://localhost:3131
PI_RUNTIME_STG_URL=https://stg.jpglabs.com.br/pi
PI_RUNTIME_PROD_URL=https://jpglabs.com.br/pi
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
OLLAMA_URL=http://localhost:11434
EOF

  chmod 600 "$portfolio_env"
  echo "portfolio-backend env: created"
}

ensure_portfolio_backend_env
