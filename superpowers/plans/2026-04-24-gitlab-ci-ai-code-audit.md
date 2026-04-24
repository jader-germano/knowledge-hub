# GitLab CI AI Code Audit — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar o GitLab CI Component `ai-code-audit` no pacote `red-cartesian-motion`, com Job A (análise estática JS/TS) e Job B (Ollama na VPS via Tailscale), e ativá-lo em 6 repos do workspace JPGLabs.

**Architecture:** Componente GitLab CI publicado em `red-cartesian-motion/packages/ci/components/ai-code-audit/`. Job A roda em runner padrão com `node:22-slim`; Job B conecta na VPS via Tailscale ephemeral e chama Ollama. Resultado: artifact `audit-report.md` + comentário automático no MR. Um smoke test ranqueia os modelos Ollama disponíveis antes do primeiro uso em produção.

**Tech Stack:** Shell (bash), YAML (GitLab CI), Node.js 22, `madge` (npm), `bats-core` (shell testing), Tailscale CLI, Ollama REST API (`/api/generate`, `/api/tags`), GitLab API (`/notes`).

**Spec:** `jpglabs/docs/superpowers/specs/2026-04-24-gitlab-ci-ai-code-audit-design.md`

---

## Mapa de Arquivos

### Criados (repo: `red-cartesian-motion` — novo)

```
red-cartesian-motion/
├── package.json                                    ← workspace root (npm workspaces)
├── .gitlab-ci.yml                                  ← CI do próprio red-cartesian-motion
├── packages/
│   └── ci/
│       ├── package.json                            ← package do CI Component
│       └── components/
│           └── ai-code-audit/
│               ├── template.yml                    ← CI Component entry point
│               └── scripts/
│                   ├── static-audit.sh             ← Job A: checks estáticos
│                   ├── ai-audit.sh                 ← Job B: Ollama + comentário MR
│                   └── smoke-test.sh               ← ranking de modelos Ollama
└── tests/
    └── ci/
        ├── fixtures/
        │   ├── bad-diff.patch                      ← diff sintético com CCN=25, 420 linhas, circular
        │   └── good-diff.patch                     ← diff limpo (baseline)
        └── static-audit.bats                       ← testes bats para static-audit.sh
```

### Modificados (6 repos alvo)

```
jpglabs-dashboard/.gitlab-ci.yml      ← adicionar include + stage audit
openclaude-hub/.gitlab-ci.yml         ← adicionar include + stage audit
portfolio-backend/.gitlab-ci.yml      ← criar (não existe) + include
portfolio-mobile/.gitlab-ci.yml       ← criar (não existe) + include
imap-server/.gitlab-ci.yml            ← criar (não existe) + include
docs/.gitlab-ci.yml                   ← adicionar include + stage audit
```

---

## Task 1: Bootstrap do repo `red-cartesian-motion`

**Files:**
- Create: `/Users/philipegermano/code/red-cartesian-motion/package.json`
- Create: `/Users/philipegermano/code/red-cartesian-motion/packages/ci/package.json`
- Create: `/Users/philipegermano/code/red-cartesian-motion/.gitignore`
- Create: `/Users/philipegermano/code/red-cartesian-motion/.gitlab-ci.yml`

- [ ] **Step 1: Criar diretório e inicializar git**

```bash
mkdir -p /Users/philipegermano/code/red-cartesian-motion/packages/ci/components/ai-code-audit/scripts
mkdir -p /Users/philipegermano/code/red-cartesian-motion/tests/ci/fixtures
cd /Users/philipegermano/code/red-cartesian-motion
git init
git checkout -b main
```

- [ ] **Step 2: Criar package.json raiz (npm workspaces)**

```json
{
  "name": "red-cartesian-motion",
  "version": "0.1.0",
  "private": true,
  "workspaces": ["packages/*"],
  "description": "JPGLabs shared CI and Design components",
  "license": "MIT"
}
```

Salvar em: `red-cartesian-motion/package.json`

- [ ] **Step 3: Criar package.json do pacote ci**

```json
{
  "name": "@jpglabs/ci",
  "version": "0.1.0",
  "description": "GitLab CI Components for JPGLabs workspace",
  "license": "MIT"
}
```

Salvar em: `red-cartesian-motion/packages/ci/package.json`

- [ ] **Step 4: Criar .gitignore**

```
node_modules/
.DS_Store
*.log
```

Salvar em: `red-cartesian-motion/.gitignore`

- [ ] **Step 5: Criar .gitlab-ci.yml do próprio repo (valida o componente)**

```yaml
stages:
  - test

default:
  image: node:22-slim

test-component:
  stage: test
  before_script:
    - apt-get update -qq && apt-get install -y -qq git
    - npm install -g bats
  script:
    - bats tests/ci/static-audit.bats
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == "main"'
```

Salvar em: `red-cartesian-motion/.gitlab-ci.yml`

- [ ] **Step 6: Commit inicial**

```bash
cd /Users/philipegermano/code/red-cartesian-motion
git add .
git commit -m "chore: bootstrap red-cartesian-motion workspace"
```

---

## Task 2: Fixtures de teste (diff sintético)

**Files:**
- Create: `tests/ci/fixtures/bad-diff.patch`
- Create: `tests/ci/fixtures/good-diff.patch`

- [ ] **Step 1: Criar bad-diff.patch — CCN=25, arquivo 420 linhas, import circular**

```diff
diff --git a/src/processor.ts b/src/processor.ts
new file mode 100644
index 0000000..aaaaaaa
--- /dev/null
+++ b/src/processor.ts
@@ -0,0 +1,421 @@
+import { helper } from './helper'; // circular: helper imports processor
+
+export function processRequest(input: any) {
+  if (!input) return null;
+  if (input.type === 'a') {
+    if (input.value > 0) {
+      if (input.value > 100) {
+        if (input.flags?.enabled) {
+          if (input.flags.level === 1) {
+            return 'high-a';
+          } else if (input.flags.level === 2) {
+            return 'medium-a';
+          } else if (input.flags.level === 3) {
+            return 'low-a';
+          } else {
+            return 'unknown-a';
+          }
+        } else {
+          return 'disabled-a';
+        }
+      } else if (input.value > 50) {
+        if (input.flags?.enabled) {
+          return 'mid-a';
+        }
+        return 'mid-disabled-a';
+      }
+    }
+  } else if (input.type === 'b') {
+    return helper(input);
+  }
+  return null;
+}
```

Nota: completar o arquivo até 421 linhas adicionando funções dummy no final:

```diff
+// padding to exceed 300-line threshold
+function pad001() { return 1; }
+function pad002() { return 2; }
// ... repetir até linha 421
```

Gerar o patch completo com o script abaixo:

```bash
cd /Users/philipegermano/code/red-cartesian-motion
python3 - <<'PYEOF'
lines = [
    "diff --git a/src/processor.ts b/src/processor.ts",
    "new file mode 100644",
    "index 0000000..aaaaaaa",
    "--- /dev/null",
    "+++ b/src/processor.ts",
    "@@ -0,0 +1,421 @@",
    "+import { helper } from './helper';",
    "+",
    "+export function processRequest(input: any) {",
    "+  if (!input) return null;",
    "+  if (input.type === 'a') {",
    "+    if (input.value > 0) {",
    "+      if (input.value > 100) {",
    "+        if (input.flags?.enabled) {",
    "+          if (input.flags.level === 1) { return 'high-a'; }",
    "+          else if (input.flags.level === 2) { return 'medium-a'; }",
    "+          else if (input.flags.level === 3) { return 'low-a'; }",
    "+          else { return 'unknown-a'; }",
    "+        } else { return 'disabled-a'; }",
    "+      } else if (input.value > 50) {",
    "+        if (input.flags?.enabled) { return 'mid-a'; }",
    "+        return 'mid-disabled-a';",
    "+      }",
    "+    }",
    "+  } else if (input.type === 'b') { return helper(input); }",
    "+  return null;",
    "+}",
]
for i in range(len(lines), 422):
    lines.append(f"+function pad{i:03d}() {{ return {i}; }}")
print('\n'.join(lines))
PYEOF
```

Redirecionar saída para `tests/ci/fixtures/bad-diff.patch`.

- [ ] **Step 2: Criar good-diff.patch — arquivo pequeno, sem circulares, CCN baixo**

```diff
diff --git a/src/utils.ts b/src/utils.ts
new file mode 100644
index 0000000..bbbbbbb
--- /dev/null
+++ b/src/utils.ts
@@ -0,0 +1,10 @@
+export function add(a: number, b: number): number {
+  return a + b;
+}
+
+export function isPositive(n: number): boolean {
+  return n > 0;
+}
```

Salvar em: `tests/ci/fixtures/good-diff.patch`

- [ ] **Step 3: Commit**

```bash
cd /Users/philipegermano/code/red-cartesian-motion
git add tests/
git commit -m "test(ci): add synthetic fixtures for static-audit tests"
```

---

## Task 3: `static-audit.sh` — Job A

**Files:**
- Create: `packages/ci/components/ai-code-audit/scripts/static-audit.sh`
- Test: `tests/ci/static-audit.bats`

- [ ] **Step 1: Escrever testes bats (TDD — escrever antes do script)**

```bash
# tests/ci/static-audit.bats
#!/usr/bin/env bats

SCRIPT="packages/ci/components/ai-code-audit/scripts/static-audit.sh"
FIXTURES="tests/ci/fixtures"

setup() {
  export AUDIT_CCN_MAX="20"
  export AUDIT_MAX_LINES="300"
  export AUDIT_BLOCK_ON_CIRCULAR="true"
}

@test "bad-diff: detecta arquivo > 300 linhas" {
  run bash "$SCRIPT" --mode lines --input "$FIXTURES/bad-diff.patch"
  [ "$status" -eq 1 ]
  [[ "$output" == *"FAIL: módulo excede"* ]]
}

@test "good-diff: arquivo pequeno passa na verificação de linhas" {
  run bash "$SCRIPT" --mode lines --input "$FIXTURES/good-diff.patch"
  [ "$status" -eq 0 ]
  [[ "$output" == *"OK: tamanho"* ]]
}

@test "respeita variável AUDIT_MAX_LINES=500" {
  export AUDIT_MAX_LINES="500"
  run bash "$SCRIPT" --mode lines --input "$FIXTURES/bad-diff.patch"
  [ "$status" -eq 0 ]
}

@test "bad-diff: detecta import circular via madge" {
  skip "requer madge instalado e repo real — rodar em CI"
}
```

Salvar em: `tests/ci/static-audit.bats`

- [ ] **Step 2: Rodar testes para confirmar que falham**

```bash
cd /Users/philipegermano/code/red-cartesian-motion
npm install -g bats 2>/dev/null || true
bats tests/ci/static-audit.bats
```

Esperado: `FAIL — bash: packages/ci/.../static-audit.sh: No such file`

- [ ] **Step 3: Implementar static-audit.sh**

```bash
#!/usr/bin/env bash
# static-audit.sh — Job A: análise estática JS/TS
# Uso: static-audit.sh [--mode lines|ccn|circular|all] [--input <patch-file>]
# Variáveis: AUDIT_CCN_MAX (default 20), AUDIT_MAX_LINES (default 300),
#            AUDIT_BLOCK_ON_CIRCULAR (default true)

set -euo pipefail

MODE="${2:-all}"
INPUT_PATCH="${4:-}"
CCN_MAX="${AUDIT_CCN_MAX:-20}"
MAX_LINES="${AUDIT_MAX_LINES:-300}"
BLOCK_CIRCULAR="${AUDIT_BLOCK_ON_CIRCULAR:-true}"
RESULTS_FILE="${AUDIT_RESULTS_FILE:-static-audit-results.txt}"
EXIT_CODE=0

log()  { echo "[audit-static] $*"; }
fail() { echo "[audit-static] FAIL: $*" | tee -a "$RESULTS_FILE"; EXIT_CODE=1; }
ok()   { echo "[audit-static] OK: $*"   | tee -a "$RESULTS_FILE"; }
warn() { echo "[audit-static] WARN: $*" | tee -a "$RESULTS_FILE"; }

# Parseamento básico de args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode)   MODE="$2";  shift 2 ;;
    --input)  INPUT_PATCH="$2"; shift 2 ;;
    *)        shift ;;
  esac
done

: > "$RESULTS_FILE"

# ── CHECK 1: Tamanho de módulo ────────────────────────────────────────────────
check_lines() {
  log "Verificando tamanho de módulos (threshold: ${MAX_LINES} linhas)..."

  if [[ -n "$INPUT_PATCH" ]]; then
    # Modo patch: conta linhas adicionadas por arquivo no diff
    local current_file=""
    local line_count=0
    while IFS= read -r line; do
      if [[ "$line" =~ ^\+\+\+\ b/(.+)$ ]]; then
        current_file="${BASH_REMATCH[1]}"
        line_count=0
      elif [[ "$line" =~ ^\+ && ! "$line" =~ ^\+\+\+ ]]; then
        ((line_count++)) || true
        if [[ $line_count -gt $MAX_LINES ]]; then
          fail "módulo excede ${MAX_LINES} linhas: ${current_file} (${line_count}+ linhas)"
          return
        fi
      fi
    done < "$INPUT_PATCH"
    ok "tamanho de módulos dentro do limite"
  else
    # Modo repo: varre arquivos TS/JS no working dir
    local violations=()
    while IFS= read -r file; do
      local count
      count=$(wc -l < "$file")
      if [[ $count -gt $MAX_LINES ]]; then
        violations+=("$file ($count linhas)")
      fi
    done < <(find src -name "*.ts" -o -name "*.tsx" -o -name "*.js" 2>/dev/null)
    if [[ ${#violations[@]} -gt 0 ]]; then
      for v in "${violations[@]}"; do fail "módulo excede ${MAX_LINES} linhas: $v"; done
    else
      ok "tamanho de módulos dentro do limite"
    fi
  fi
}

# ── CHECK 2: Complexidade ciclomática (ESLint) ────────────────────────────────
check_ccn() {
  log "Verificando complexidade ciclomática (threshold: CCN > ${CCN_MAX})..."
  if ! command -v npx &>/dev/null; then
    warn "npx não encontrado — pulando check CCN"
    return
  fi
  local output
  output=$(npx --yes eslint \
    --rule "{\"complexity\": [\"error\", ${CCN_MAX}]}" \
    --format compact \
    "src/**/*.ts" "src/**/*.tsx" "src/**/*.js" 2>&1) || true

  if echo "$output" | grep -q "complexity"; then
    echo "$output" | grep "complexity" | while IFS= read -r line; do
      fail "CCN alto: $line"
    done
  else
    ok "complexidade ciclomática dentro do limite"
  fi
}

# ── CHECK 3: Imports circulares (madge) ──────────────────────────────────────
check_circular() {
  log "Verificando imports circulares..."
  if ! command -v npx &>/dev/null; then
    warn "npx não encontrado — pulando check circular"
    return
  fi
  local output
  output=$(npx --yes madge --circular --extensions ts,tsx,js src/ 2>&1) || true

  if echo "$output" | grep -qE "Found [1-9]|circular"; then
    if [[ "$BLOCK_CIRCULAR" == "true" ]]; then
      fail "imports circulares detectados:\n$output"
    else
      warn "imports circulares detectados (não bloqueando):\n$output"
    fi
  else
    ok "nenhum import circular"
  fi
}

# ── CHECK 4: Estrutura de camadas (warning apenas) ───────────────────────────
check_layers() {
  log "Verificando estrutura de camadas (warning)..."
  if ! command -v npx &>/dev/null; then
    warn "npx não encontrado — pulando check de camadas"
    return
  fi
  # Detecta controller importando repository diretamente
  local violations
  violations=$(grep -rn "from.*repository\|require.*repository" src/controllers/ 2>/dev/null || true)
  if [[ -n "$violations" ]]; then
    warn "possível violação de camada (controller → repository direto):\n$violations"
  else
    ok "estrutura de camadas aparentemente ok"
  fi
}

# ── Dispatch ─────────────────────────────────────────────────────────────────
case "$MODE" in
  lines)    check_lines ;;
  ccn)      check_ccn ;;
  circular) check_circular ;;
  layers)   check_layers ;;
  all)
    check_lines
    check_ccn
    check_circular
    check_layers
    ;;
  *) echo "Modo desconhecido: $MODE"; exit 2 ;;
esac

log "Análise estática concluída. Resultado salvo em: $RESULTS_FILE"
exit $EXIT_CODE
```

Salvar em: `packages/ci/components/ai-code-audit/scripts/static-audit.sh`

```bash
chmod +x packages/ci/components/ai-code-audit/scripts/static-audit.sh
```

- [ ] **Step 4: Rodar testes para confirmar que passam**

```bash
cd /Users/philipegermano/code/red-cartesian-motion
bats tests/ci/static-audit.bats
```

Esperado:
```
 ✓ bad-diff: detecta arquivo > 300 linhas
 ✓ good-diff: arquivo pequeno passa na verificação de linhas
 ✓ respeita variável AUDIT_MAX_LINES=500
 - bad-diff: detecta import circular via madge (skipped)

3 tests, 0 failures, 1 skipped
```

- [ ] **Step 5: Commit**

```bash
cd /Users/philipegermano/code/red-cartesian-motion
git add packages/ tests/
git commit -m "feat(ci): implementar static-audit.sh com checks de linhas, CCN, circulares e camadas"
```

---

## Task 4: `smoke-test.sh` — ranking de modelos Ollama

**Files:**
- Create: `packages/ci/components/ai-code-audit/scripts/smoke-test.sh`

- [ ] **Step 1: Implementar smoke-test.sh**

```bash
#!/usr/bin/env bash
# smoke-test.sh — ranqueia modelos Ollama para o audit
# Variáveis: OLLAMA_HOST (ex: http://100.68.217.36:11434)
# Output: smoke-report.md com ranking

set -euo pipefail

OLLAMA_HOST="${OLLAMA_HOST:-http://localhost:11434}"
REPORT="smoke-report.md"
FIXTURES_DIR="${SMOKE_FIXTURES_DIR:-tests/ci/fixtures}"
BAD_DIFF="$FIXTURES_DIR/bad-diff.patch"
TIMEOUT=60

log() { echo "[smoke-test] $*"; }

# Lê o diff sintético
DIFF_CONTENT=$(cat "$BAD_DIFF")

# Prompt padrão para avaliação
PROMPT="Você é um auditor de código sênior. Analise o diff abaixo e identifique EXATAMENTE estes 3 problemas: (1) função com alta complexidade ciclomática/muitos ifs aninhados, (2) arquivo com mais de 300 linhas, (3) import circular entre módulos. Liste cada problema encontrado como: PROBLEMA_1: ..., PROBLEMA_2: ..., PROBLEMA_3: ...

[DIFF]
${DIFF_CONTENT:0:3000}"

# Busca modelos disponíveis
log "Conectando ao Ollama em $OLLAMA_HOST..."
MODELS_JSON=$(curl -sf "$OLLAMA_HOST/api/tags" 2>/dev/null) || {
  log "ERRO: não foi possível conectar ao Ollama em $OLLAMA_HOST"
  exit 1
}

MODELS=$(echo "$MODELS_JSON" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for m in data.get('models', []):
    print(m['name'])
")

if [[ -z "$MODELS" ]]; then
  log "Nenhum modelo encontrado no Ollama"
  exit 1
fi

log "Modelos encontrados:"
echo "$MODELS" | while read -r m; do log "  - $m"; done

# Inicializa relatório
{
  echo "# Smoke Test — Ranking de Modelos Ollama para AI Code Audit"
  echo ""
  echo "**Data:** $(date -u '+%Y-%m-%d %H:%M UTC')"
  echo "**Host:** $OLLAMA_HOST"
  echo ""
  echo "## Resultados por Modelo"
  echo ""
} > "$REPORT"

RANKING=()

# Testa cada modelo
while IFS= read -r MODEL; do
  log "Testando modelo: $MODEL"
  SCORE=0
  START=$(date +%s)

  RESPONSE=$(curl -sf --max-time "$TIMEOUT" \
    "$OLLAMA_HOST/api/generate" \
    -d "{\"model\": \"$MODEL\", \"prompt\": $(echo "$PROMPT" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))'), \"stream\": false}" \
    2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response',''))" 2>/dev/null) || RESPONSE=""

  END=$(date +%s)
  ELAPSED=$((END - START))

  # Critério 1: identificou os 3 problemas (50 pts)
  PROBLEMS_FOUND=0
  echo "$RESPONSE" | grep -qi "complexidade\|ifs aninhados\|cyclomatic\|complexity" && ((PROBLEMS_FOUND++)) || true
  echo "$RESPONSE" | grep -qi "300 linhas\|linhas\|lines\|arquivo grande\|large file" && ((PROBLEMS_FOUND++)) || true
  echo "$RESPONSE" | grep -qi "circular\|import circular\|circular import" && ((PROBLEMS_FOUND++)) || true
  SCORE=$((SCORE + PROBLEMS_FOUND * 17))  # max 51 (≈50%)

  # Critério 2: tempo ≤ 30s (30 pts)
  if [[ $ELAPSED -le 30 ]]; then
    SCORE=$((SCORE + 30))
  elif [[ $ELAPSED -le 45 ]]; then
    SCORE=$((SCORE + 15))
  fi

  # Critério 3: output estruturado (20 pts)
  echo "$RESPONSE" | grep -qE "PROBLEMA_[123]:|##|^\d\." && SCORE=$((SCORE + 20)) || true

  RANKING+=("$SCORE $ELAPSED $MODEL")
  log "  Score: $SCORE/100 | Tempo: ${ELAPSED}s | Problemas: $PROBLEMS_FOUND/3"

  {
    echo "### $MODEL"
    echo "- **Score:** $SCORE/100"
    echo "- **Tempo:** ${ELAPSED}s"
    echo "- **Problemas identificados:** $PROBLEMS_FOUND/3"
    echo "- **Output (primeiros 500 chars):**"
    echo '```'
    echo "${RESPONSE:0:500}"
    echo '```'
    echo ""
  } >> "$REPORT"

done <<< "$MODELS"

# Ordena ranking e escreve sumário
SORTED=$(printf '%s\n' "${RANKING[@]}" | sort -rn)
WINNER=$(echo "$SORTED" | head -1 | awk '{print $3}')

{
  echo "## Ranking Final"
  echo ""
  echo "| Posição | Modelo | Score | Tempo |"
  echo "|---|---|---|---|"
  POS=1
  while IFS=" " read -r score elapsed model; do
    echo "| $POS | \`$model\` | $score/100 | ${elapsed}s |"
    ((POS++))
  done <<< "$SORTED"
  echo ""
  echo "## Modelo Recomendado"
  echo ""
  echo "\`\`\`"
  echo "AUDIT_AI_MODEL=$WINNER"
  echo "\`\`\`"
  echo ""
  echo "Definir essa variável em **Settings > CI/CD > Variables** de cada repo alvo."
} >> "$REPORT"

log "Relatório salvo em: $REPORT"
log "Modelo recomendado: $WINNER"
cat "$REPORT"
```

Salvar em: `packages/ci/components/ai-code-audit/scripts/smoke-test.sh`

```bash
chmod +x packages/ci/components/ai-code-audit/scripts/smoke-test.sh
```

- [ ] **Step 2: Commit**

```bash
cd /Users/philipegermano/code/red-cartesian-motion
git add packages/ci/components/ai-code-audit/scripts/smoke-test.sh
git commit -m "feat(ci): implementar smoke-test.sh para ranking de modelos Ollama"
```

---

## Task 5: `ai-audit.sh` — Job B (Ollama + comentário MR)

**Files:**
- Create: `packages/ci/components/ai-code-audit/scripts/ai-audit.sh`

- [ ] **Step 1: Implementar ai-audit.sh**

```bash
#!/usr/bin/env bash
# ai-audit.sh — Job B: análise semântica via Ollama + comentário no MR
# Variáveis obrigatórias:
#   OLLAMA_HOST         — ex: http://100.68.217.36:11434
#   AUDIT_AI_MODEL      — ex: llama3.1:8b
#   GITLAB_TOKEN        — token com scope api
#   CI_PROJECT_ID       — injetado pelo GitLab CI
#   CI_MERGE_REQUEST_IID — injetado pelo GitLab CI
# Variáveis opcionais:
#   CI_SERVER_URL       — default https://gitlab.com
#   AUDIT_RESULTS_FILE  — saída do Job A (default static-audit-results.txt)

set -euo pipefail

OLLAMA_HOST="${OLLAMA_HOST:-http://localhost:11434}"
MODEL="${AUDIT_AI_MODEL:-llama3.1:8b}"
GITLAB_URL="${CI_SERVER_URL:-https://gitlab.com}"
PROJECT_ID="${CI_PROJECT_ID:-}"
MR_IID="${CI_MERGE_REQUEST_IID:-}"
TOKEN="${GITLAB_TOKEN:-}"
STATIC_RESULTS="${AUDIT_RESULTS_FILE:-static-audit-results.txt}"
REPORT_FILE="audit-report.md"
TARGET_BRANCH="${CI_MERGE_REQUEST_TARGET_BRANCH_NAME:-main}"
BOT_MARKER="<!-- ai-code-audit-bot -->"
MAX_DIFF_CHARS=16000

log()  { echo "[audit-ai] $*"; }
die()  { echo "[audit-ai] ERRO: $*" >&2; exit 1; }

[[ -n "$PROJECT_ID" ]] || die "CI_PROJECT_ID não definido"
[[ -n "$MR_IID"     ]] || die "CI_MERGE_REQUEST_IID não definido (job não está num MR?)"
[[ -n "$TOKEN"      ]] || die "GITLAB_TOKEN não definido"

# ── 1. Extrair diff do MR ────────────────────────────────────────────────────
log "Extraindo diff do MR (branch alvo: $TARGET_BRANCH)..."
git fetch origin "$TARGET_BRANCH" 2>/dev/null || true
DIFF=$(git diff "origin/$TARGET_BRANCH" --unified=3 -- '*.ts' '*.tsx' '*.js' '*.mjs' 2>/dev/null \
  | head -c "$MAX_DIFF_CHARS")
DIFF_LINES=$(echo "$DIFF" | wc -l)
log "Diff: $DIFF_LINES linhas (limitado a $MAX_DIFF_CHARS chars)"

# ── 2. Ler resultados estáticos ──────────────────────────────────────────────
STATIC_SUMMARY=""
if [[ -f "$STATIC_RESULTS" ]]; then
  STATIC_SUMMARY=$(cat "$STATIC_RESULTS")
  log "Resultados estáticos carregados de $STATIC_RESULTS"
else
  STATIC_SUMMARY="(análise estática não disponível)"
  log "Aviso: $STATIC_RESULTS não encontrado"
fi

# ── 3. Montar prompt ─────────────────────────────────────────────────────────
PROMPT="Você é um auditor de código sênior. Analise o diff abaixo e os resultados da análise estática. Identifique: riscos de manutenibilidade, violações de arquitetura, e sugira refatorações objetivas e concisas. Seja direto — sem introduções longas.

Formato obrigatório de resposta em Markdown:
## Riscos Críticos
(lista de itens bloqueadores, ou \"Nenhum\" se não houver)

## Avisos
(problemas que não bloqueiam mas merecem atenção)

## Sugestões
(melhorias opcionais)

[MÉTRICAS ESTÁTICAS]
${STATIC_SUMMARY}

[DIFF DO MR — ${DIFF_LINES} linhas]
${DIFF}"

# ── 4. Chamar Ollama ─────────────────────────────────────────────────────────
log "Chamando Ollama ($MODEL) em $OLLAMA_HOST..."
PROMPT_JSON=$(python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))" <<< "$PROMPT")

AI_RESPONSE=$(curl -sf --max-time 120 \
  "$OLLAMA_HOST/api/generate" \
  -H "Content-Type: application/json" \
  -d "{\"model\": \"$MODEL\", \"prompt\": $PROMPT_JSON, \"stream\": false}" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response','(sem resposta)'))" \
  2>/dev/null) || AI_RESPONSE="(erro ao chamar Ollama — verifique OLLAMA_HOST e AUDIT_AI_MODEL)"

log "Resposta recebida (${#AI_RESPONSE} chars)"

# ── 5. Gerar audit-report.md ─────────────────────────────────────────────────
COMMIT_SHA="${CI_COMMIT_SHA:-$(git rev-parse HEAD 2>/dev/null || echo 'unknown')}"
{
  echo "$BOT_MARKER"
  echo "# AI Code Audit — MR !${MR_IID}"
  echo ""
  echo "**Modelo:** \`$MODEL\`  "
  echo "**Data:** $(date -u '+%Y-%m-%d %H:%M UTC')  "
  echo "**Commit:** \`${COMMIT_SHA:0:8}\`"
  echo ""
  echo "---"
  echo ""
  echo "## Análise Estática"
  echo ""
  echo '```'
  echo "$STATIC_SUMMARY"
  echo '```'
  echo ""
  echo "---"
  echo ""
  echo "## Análise Semântica (IA)"
  echo ""
  echo "$AI_RESPONSE"
} > "$REPORT_FILE"

log "Relatório salvo em $REPORT_FILE"

# ── 6. Postar ou editar comentário no MR ────────────────────────────────────
REPORT_CONTENT=$(cat "$REPORT_FILE")
COMMENT_BODY=$(python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))" <<< "$REPORT_CONTENT")

GL_API="$GITLAB_URL/api/v4/projects/$PROJECT_ID/merge_requests/$MR_IID"

# Busca comentário existente com o marcador
EXISTING_NOTE_ID=$(curl -sf \
  -H "PRIVATE-TOKEN: $TOKEN" \
  "$GL_API/notes?per_page=100" \
  | python3 -c "
import sys,json
notes = json.load(sys.stdin)
for n in notes:
    if '$BOT_MARKER' in n.get('body',''):
        print(n['id'])
        break
" 2>/dev/null || echo "")

if [[ -n "$EXISTING_NOTE_ID" ]]; then
  log "Editando comentário existente (note_id=$EXISTING_NOTE_ID)..."
  curl -sf -X PUT \
    -H "PRIVATE-TOKEN: $TOKEN" \
    -H "Content-Type: application/json" \
    "$GL_API/notes/$EXISTING_NOTE_ID" \
    -d "{\"body\": $COMMENT_BODY}" > /dev/null
  log "Comentário atualizado com sucesso"
else
  log "Postando novo comentário no MR..."
  curl -sf -X POST \
    -H "PRIVATE-TOKEN: $TOKEN" \
    -H "Content-Type: application/json" \
    "$GL_API/notes" \
    -d "{\"body\": $COMMENT_BODY}" > /dev/null
  log "Comentário postado com sucesso"
fi

log "Job B concluído."
```

Salvar em: `packages/ci/components/ai-code-audit/scripts/ai-audit.sh`

```bash
chmod +x packages/ci/components/ai-code-audit/scripts/ai-audit.sh
```

- [ ] **Step 2: Commit**

```bash
cd /Users/philipegermano/code/red-cartesian-motion
git add packages/ci/components/ai-code-audit/scripts/ai-audit.sh
git commit -m "feat(ci): implementar ai-audit.sh com Ollama + comentário automático no MR"
```

---

## Task 6: `template.yml` — GitLab CI Component

**Files:**
- Create: `packages/ci/components/ai-code-audit/template.yml`

- [ ] **Step 1: Criar template.yml**

```yaml
# GitLab CI Component: ai-code-audit
# Uso:
#   include:
#     - component: gitlab.com/jpglabs/red-cartesian-motion/ci/ai-code-audit@~latest
#   stages: [audit, validate, deploy]
#
# Variáveis configuráveis (definir em Settings > CI/CD > Variables):
#   AUDIT_CCN_MAX          (default: 20)
#   AUDIT_MAX_LINES        (default: 300)
#   AUDIT_BLOCK_ON_CIRCULAR (default: "true")
#   AUDIT_LAYER_VIOLATIONS  (default: "warn")
#   AUDIT_AI_MODEL          (obrigatório para Job B — definir após smoke test)
#   OLLAMA_HOST             (obrigatório para Job B)
#   GITLAB_TOKEN            (obrigatório para Job B — scope: api)
#   TS_AUTHKEY              (obrigatório para Job B — Tailscale ephemeral key)

spec:
  inputs:
    stage:
      default: audit
      description: "Stage where audit jobs run"
    node_image:
      default: "node:22-slim"
      description: "Docker image for static analysis job"

---

variables:
  AUDIT_CCN_MAX: "20"
  AUDIT_MAX_LINES: "300"
  AUDIT_BLOCK_ON_CIRCULAR: "true"
  AUDIT_LAYER_VIOLATIONS: "warn"

.audit-base:
  stage: $[[ inputs.stage ]]
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  allow_failure: false

audit-static:
  extends: .audit-base
  image: $[[ inputs.node_image ]]
  before_script:
    - apt-get update -qq && apt-get install -y -qq git curl
    - npm install -g madge 2>/dev/null || true
  script:
    - |
      curl -fsSL \
        "https://gitlab.com/jpglabs/red-cartesian-motion/-/raw/main/packages/ci/components/ai-code-audit/scripts/static-audit.sh" \
        -o /tmp/static-audit.sh
      chmod +x /tmp/static-audit.sh
      bash /tmp/static-audit.sh --mode all
  artifacts:
    when: always
    expire_in: 7 days
    paths:
      - static-audit-results.txt

audit-ai:
  extends: .audit-base
  image: node:22-slim
  needs:
    - audit-static
  tags:
    - vps
  before_script:
    - apt-get update -qq && apt-get install -y -qq git curl python3
    # Tailscale userspace (mesmo padrão do openclaude-hub)
    - curl -fsSL https://tailscale.com/install.sh | sh
    - tailscaled --tun=userspace-networking --socks5-server=localhost:1055
        --state=/tmp/tailscaled.state > /tmp/tailscaled.log 2>&1 &
    - sleep 3
    - tailscale up --authkey="$TS_AUTHKEY" --hostname="audit-ci-$CI_JOB_ID"
        --ephemeral --accept-dns=false
    - tailscale status | head -3
  script:
    - |
      curl -fsSL \
        "https://gitlab.com/jpglabs/red-cartesian-motion/-/raw/main/packages/ci/components/ai-code-audit/scripts/ai-audit.sh" \
        -o /tmp/ai-audit.sh
      chmod +x /tmp/ai-audit.sh
      bash /tmp/ai-audit.sh
  artifacts:
    when: always
    expire_in: 30 days
    paths:
      - audit-report.md
  after_script:
    - tailscale logout 2>/dev/null || true

audit-model-smoke:
  stage: $[[ inputs.stage ]]
  image: node:22-slim
  tags:
    - vps
  when: manual
  allow_failure: true
  before_script:
    - apt-get update -qq && apt-get install -y -qq curl python3
    - curl -fsSL https://tailscale.com/install.sh | sh
    - tailscaled --tun=userspace-networking --socks5-server=localhost:1055
        --state=/tmp/tailscaled.state > /tmp/tailscaled.log 2>&1 &
    - sleep 3
    - tailscale up --authkey="$TS_AUTHKEY" --hostname="smoke-ci-$CI_JOB_ID"
        --ephemeral --accept-dns=false
  script:
    - |
      curl -fsSL \
        "https://gitlab.com/jpglabs/red-cartesian-motion/-/raw/main/packages/ci/components/ai-code-audit/scripts/smoke-test.sh" \
        -o /tmp/smoke-test.sh
      chmod +x /tmp/smoke-test.sh
      # Baixa fixtures
      mkdir -p tests/ci/fixtures
      curl -fsSL \
        "https://gitlab.com/jpglabs/red-cartesian-motion/-/raw/main/tests/ci/fixtures/bad-diff.patch" \
        -o tests/ci/fixtures/bad-diff.patch
      SMOKE_FIXTURES_DIR=tests/ci/fixtures bash /tmp/smoke-test.sh
  artifacts:
    when: always
    expire_in: 90 days
    paths:
      - smoke-report.md
  after_script:
    - tailscale logout 2>/dev/null || true
```

Salvar em: `packages/ci/components/ai-code-audit/template.yml`

- [ ] **Step 2: Commit + tag v0.1.0**

```bash
cd /Users/philipegermano/code/red-cartesian-motion
git add packages/ci/components/ai-code-audit/template.yml
git commit -m "feat(ci): adicionar template.yml do GitLab CI Component ai-code-audit"
git tag -a v0.1.0 -m "chore: release v0.1.0 — ai-code-audit component inicial"
```

---

## Task 7: Push para GitLab e configurar variáveis de CI

- [ ] **Step 1: Criar repo no GitLab**

```
Acesse: https://gitlab.com/jpglabs
Criar novo projeto: red-cartesian-motion
Visibilidade: Internal (ou Public se planejado)
```

- [ ] **Step 2: Push do repo local**

```bash
cd /Users/philipegermano/code/red-cartesian-motion
git remote add origin git@gitlab.com:jpglabs/red-cartesian-motion.git
git push -u origin main
git push origin v0.1.0
```

- [ ] **Step 3: Configurar variáveis de grupo no GitLab**

```
GitLab > jpglabs (grupo) > Settings > CI/CD > Variables

Adicionar:
  AUDIT_AI_MODEL      = <definir após smoke test — Task 9>
  OLLAMA_HOST         = http://<ip-ollama-tailnet>:11434
  TS_AUTHKEY          = <ephemeral authkey do Tailscale>
  GITLAB_TOKEN        = <Personal/Group token com scope api>
```

Variáveis de grupo são herdadas por todos os repos — não precisa repetir em cada projeto.

---

## Task 8: Adicionar `include` nos 6 repos alvo

Para cada repo abaixo, repetir os mesmos passos (adaptar o `stages` existente).

**Repos:** `jpglabs-dashboard`, `openclaude-hub`, `portfolio-backend`, `portfolio-mobile`, `imap-server`, `docs`

- [ ] **Step 1: jpglabs-dashboard** — adicionar ao `.gitlab-ci.yml` existente

Abrir: `/Users/philipegermano/code/jpglabs/jpglabs-dashboard/.gitlab-ci.yml`

Adicionar no topo (antes de `stages:`):

```yaml
include:
  - component: gitlab.com/jpglabs/red-cartesian-motion/ci/ai-code-audit@~latest
    inputs:
      stage: audit
```

Alterar a linha `stages:`:

```yaml
# de:
stages:
  - validate
  - deploy

# para:
stages:
  - audit
  - validate
  - deploy
```

Commit:
```bash
cd /Users/philipegermano/code/jpglabs/jpglabs-dashboard
git add .gitlab-ci.yml
git commit -m "ci: adicionar ai-code-audit component ao pipeline"
```

- [ ] **Step 2: openclaude-hub**

Abrir: `/Users/philipegermano/code/jpglabs/openclaude-hub/.gitlab-ci.yml`

Mesma operação: adicionar `include:` no topo, adicionar `audit` ao `stages:`.

```bash
cd /Users/philipegermano/code/jpglabs/openclaude-hub
git add .gitlab-ci.yml
git commit -m "ci: adicionar ai-code-audit component ao pipeline"
```

- [ ] **Step 3: portfolio-backend** — criar `.gitlab-ci.yml` (não existe)

```yaml
include:
  - component: gitlab.com/jpglabs/red-cartesian-motion/ci/ai-code-audit@~latest
    inputs:
      stage: audit

stages:
  - audit

default:
  image: node:22-slim
```

Salvar em `/Users/philipegermano/code/jpglabs/portfolio-backend/.gitlab-ci.yml`

```bash
cd /Users/philipegermano/code/jpglabs/portfolio-backend
git add .gitlab-ci.yml
git commit -m "ci: adicionar ai-code-audit pipeline"
```

- [ ] **Step 4: portfolio-mobile** — criar `.gitlab-ci.yml`

```yaml
include:
  - component: gitlab.com/jpglabs/red-cartesian-motion/ci/ai-code-audit@~latest
    inputs:
      stage: audit

stages:
  - audit

variables:
  AUDIT_MAX_LINES: "400"   # mobile tem componentes maiores por convenção
```

Salvar em `/Users/philipegermano/code/jpglabs/portfolio-mobile/.gitlab-ci.yml`

```bash
cd /Users/philipegermano/code/jpglabs/portfolio-mobile
git add .gitlab-ci.yml
git commit -m "ci: adicionar ai-code-audit pipeline"
```

- [ ] **Step 5: imap-server** — criar `.gitlab-ci.yml`

```yaml
include:
  - component: gitlab.com/jpglabs/red-cartesian-motion/ci/ai-code-audit@~latest
    inputs:
      stage: audit

stages:
  - audit

default:
  image: node:22-slim
```

Salvar em `/Users/philipegermano/code/jpglabs/imap-server/.gitlab-ci.yml`

```bash
cd /Users/philipegermano/code/jpglabs/imap-server
git add .gitlab-ci.yml
git commit -m "ci: adicionar ai-code-audit pipeline"
```

- [ ] **Step 6: docs** — adicionar ao `.gitlab-ci.yml` existente

Abrir: `/Users/philipegermano/code/jpglabs/docs/.gitlab-ci.yml`

```yaml
# Adicionar no topo:
include:
  - component: gitlab.com/jpglabs/red-cartesian-motion/ci/ai-code-audit@~latest
    inputs:
      stage: audit

# Alterar stages:
stages:
  - audit
  - sync
```

```bash
cd /Users/philipegermano/code/jpglabs/docs
git add .gitlab-ci.yml
git commit -m "ci: adicionar ai-code-audit component ao pipeline"
```

---

## Task 9: Smoke test na VPS — definir AUDIT_AI_MODEL

- [ ] **Step 1: Verificar acesso Tailscale à VPS**

```bash
tailscale status --json | python3 -c "
import sys,json
d=json.load(sys.stdin)
peers = d.get('Peer',{})
for k,v in peers.items():
    if 'jpglabs-vps' in v.get('HostName',''):
        print(v['HostName'], v['TailscaleIPs'])
"
```

Esperado: IP da VPS na tailnet (ex: `100.68.217.36`)

- [ ] **Step 2: Verificar modelos disponíveis no Ollama**

```bash
OLLAMA_IP="<ip-da-vps-tailnet>"
curl -s "http://$OLLAMA_IP:11434/api/tags" | python3 -c "
import sys,json
d=json.load(sys.stdin)
for m in d.get('models',[]):
    print(m['name'], '—', round(m['size']/1e9,1), 'GB')
"
```

- [ ] **Step 3: Rodar smoke test localmente**

```bash
cd /Users/philipegermano/code/red-cartesian-motion
OLLAMA_HOST="http://<ip-da-vps-tailnet>:11434" \
SMOKE_FIXTURES_DIR=tests/ci/fixtures \
bash packages/ci/components/ai-code-audit/scripts/smoke-test.sh
```

- [ ] **Step 4: Ler smoke-report.md e definir variável**

```bash
cat smoke-report.md | grep "AUDIT_AI_MODEL="
```

Copiar o valor e definir em:
```
GitLab > jpglabs (grupo) > Settings > CI/CD > Variables
AUDIT_AI_MODEL = <modelo-vencedor>
```

---

## Task 10: Validação end-to-end no `jpglabs-dashboard`

- [ ] **Step 1: Abrir um MR de teste no jpglabs-dashboard**

```bash
cd /Users/philipegermano/code/jpglabs/jpglabs-dashboard
git checkout -b test/ai-code-audit-validation
# Criar arquivo de teste com violações deliberadas
cat > src/test-audit-target.ts << 'EOF'
// Arquivo de teste — remover após validação
import { something } from './test-circular'; // circular intencional
export function complexFunction(x: any) {
  if (x) { if (x.a) { if (x.b) { if (x.c) { if (x.d) {
    return 1;
  } } } } }
  return 0;
}
EOF
git add src/test-audit-target.ts
git commit -m "test: arquivo com violações para validar audit pipeline"
git push origin test/ai-code-audit-validation
```

Abrir MR no GitLab apontando para `main`.

- [ ] **Step 2: Verificar pipeline**

```
GitLab > jpglabs-dashboard > CI/CD > Pipelines
Confirmar que stage "audit" aparece antes de "validate"
```

- [ ] **Step 3: Verificar Job A (audit-static)**

```
Pipeline > audit-static
Esperado: FAILED com mensagem de import circular ou CCN alto
```

- [ ] **Step 4: Disparar smoke test manual (primeira vez)**

```
Pipeline > audit-model-smoke > ▶ (trigger manual)
Aguardar execução
Download artifact: smoke-report.md
Verificar ranking e definir AUDIT_AI_MODEL
```

- [ ] **Step 5: Verificar Job B (audit-ai)**

```
Pipeline > audit-ai
Esperado: 
  ✓ artifact audit-report.md disponível para download
  ✓ comentário automático postado no MR com seções:
    ## Riscos Críticos
    ## Avisos  
    ## Sugestões
```

- [ ] **Step 6: Limpar branch de teste**

```bash
cd /Users/philipegermano/code/jpglabs/jpglabs-dashboard
# Fechar o MR no GitLab (sem merge)
git push origin --delete test/ai-code-audit-validation
git checkout main
git branch -d test/ai-code-audit-validation
# Remover arquivo de teste do repo local
```

---

## Self-Review

**Cobertura da spec:**
- ✅ Job A (4 checks: CCN, linhas, circular, camadas)
- ✅ Job B (Ollama via Tailscale, comentário + artifact)
- ✅ Smoke test de modelos com ranking
- ✅ Comentário: criar ou editar (marcador `<!-- ai-code-audit-bot -->`)
- ✅ Variáveis configuráveis por repo
- ✅ 6 repos alvo cobertos
- ✅ GitLab CI Component em `red-cartesian-motion`
- ✅ Validação end-to-end

**Sem placeholders:** verificado — todos os steps contêm código completo.

**Consistência de tipos:** `static-audit-results.txt` produzido pelo Job A e consumido pelo Job B via `AUDIT_RESULTS_FILE` — consistente nas Tasks 3, 5 e 6.
