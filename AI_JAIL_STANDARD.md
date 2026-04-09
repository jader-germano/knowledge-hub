# AI Jail (AIJL) — Padrão de Segurança para Agentes de IA

**Status:** Padrão Ativo  
**Vigência:** a partir de 2026-04-08  
**Fonte:** [Akita — AI Agents: Garantindo a Proteção do seu Sistema](https://akitaonrails.com/2026/01/10/ai-agents-garantindo-a-protecao-do-seu-sistema/) + [ai-jail: Sandbox para Agentes de IA](https://akitaonrails.com/2026/03/01/ai-jail-sandbox-para-agentes-de-ia-de-shell-script-a-ferramenta-real/)

---

## Por Que AIJL É o Padrão

Agentes de IA (Claude Code, Codex, OpenCode, Crush) precisam de acesso ao filesystem e capacidade de rodar compiladores, linters e comandos do sistema. Esse acesso cria superfície para:

- `rm -rf` fora do diretório do projeto
- Leitura de `~/.aws/credentials`, chaves SSH, tokens
- Exfiltração de dados via `npm install` com post-install malicioso (supply-chain attack)

AIJL resolve isso com sandboxing no nível do processo, sem root, sem overhead de VM.

---

## Ferramenta: ai-jail

**Repositório:** `https://github.com/akitaonrails/ai-jail`  
**Runtime:** Rust, ~880KB, 4 dependências, 124 testes  
**Backend Linux:** bubblewrap (bwrap) + Landlock LSM  
**Backend macOS:** `sandbox-exec` (SBPL profile gerado em runtime)

### Instalação

```bash
# macOS (preferencial)
brew tap akitaonrails/tap && brew install ai-jail

# Linux (apt)
sudo apt install bubblewrap
cargo install ai-jail

# Mise (cross-platform)
mise use -g ubi:akitaonrails/ai-jail
```

### Uso Padrão

```bash
cd ~/Projects/meu-projeto
ai-jail claude          # Claude Code em sandbox
ai-jail codex           # Codex em sandbox
ai-jail opencode        # OpenCode em sandbox
ai-jail bash            # shell para debug
```

Na primeira execução, cria `.ai-jail` no projeto (TOML commitável):

```toml
command = ["claude"]
rw_maps = []
ro_maps = []
```

---

## O Que o Sandbox Garante

### Linux (via bubblewrap + Landlock)

| Recurso | Comportamento no Sandbox |
|---------|--------------------------|
| Diretório do projeto | Leitura + **escrita** |
| `~/.aws`, `~/.gnupg`, `~/.ssh`, `~/.sparrow` | **Invisível** — nunca montado |
| `~/.claude`, `~/.config`, `~/.cargo`, `~/.docker` | Read-write (agentes precisam escrever) |
| Resto do `$HOME` | Read-only |
| `/usr`, `/etc`, `/opt` | Read-only (ferramentas do sistema) |
| GPU, Docker socket, X11/Wayland | Auto-detectados e montados se existirem |
| PID, UTS, IPC namespaces | Isolados (`--die-with-parent`) |

### macOS (via sandbox-exec SBPL)

- Deny por padrão em tudo
- Permite leitura global, nega `~/.gnupg`, `~/.aws`, `~/.ssh`, `~/Library/Keychains`, `~/Library/Mail`
- Escrita somente no diretório do projeto, dotfiles de ferramentas, `/tmp`
- Limitação: GPU (Metal) e display (Cocoa) não são restritos (system-level)

---

## Modo Lockdown

Para auditar código de terceiros ou rodar agentes em projetos desconhecidos:

```bash
ai-jail --lockdown bash
```

- Projeto montado **read-only**
- GPU, Docker, Display e mise **desabilitados**
- `$HOME` como tmpfs puro (sem dotfiles do host)
- Rede cortada no Linux (`--unshare-net`)

---

## Bootstrap de Permissões

Configura automaticamente os arquivos de permissão para cada agente:

```bash
ai-jail --bootstrap
```

Gera `~/.claude/settings.json` com allow/deny/ask:
- **Permite:** `git status/diff/log`, `ls`, `grep`, `cargo`, `npm`, `python`, `docker compose`
- **Bloqueia:** `rm -rf`, `sudo`, `chmod 777`, `git push --force`
- **Pergunta antes:** `git push`, `rm`, `docker run`

---

## Por Que Não Apenas o Sandbox Nativo do Claude Code

| | Claude Code `/sandbox` | ai-jail |
|---|---|---|
| Ferramenta | Só Claude | Qualquer agente |
| Escape hatch | Sim — pode usar `dangerouslyDisableSandbox` | Não existe |
| Configuração | Global | Por projeto (TOML commitável) |
| Transparência | Opaco | `--dry-run --verbose` mostra tudo |

O Claude Code tem um sandbox próprio (bubblewrap/sandbox-exec por baixo), mas permite que o agente decida sair dele. O `ai-jail` não tem essa válvula de escape — o processo roda dentro do bwrap, ponto.

---

## Configuração por Projeto (Kit on Rails)

A configuração segue convenção sobre configuração:

1. **`.ai-jail` na raiz** — commitável no repositório, compartilhado com o time
2. **`ai-jail --bootstrap`** — configura permissões dos agentes automaticamente
3. **`ai-jail claude`** como comando padrão de desenvolvimento — não `claude` diretamente

Analogia Rails: assim como `bin/rails server` é o ponto de entrada padrão de um app Rails, `ai-jail claude` é o ponto de entrada padrão de uma sessão com agente IA em qualquer projeto JPGLabs.

---

## Aplicação nos Projetos JPGLabs

### Padrão — Obrigatório por Default

- Todo novo projeto inclui `.ai-jail` na raiz
- Sessões de desenvolvimento iniciam com `ai-jail claude` (ou agente equivalente)
- `ai-jail --bootstrap` roda na criação do ambiente do projeto

### Projetos Existentes

- `jpglabs-saas` → adicionar `.ai-jail` no scaffold
- `openclaude` → adicionar `.ai-jail` na raiz
- `pi-local-app` → adicionar `.ai-jail` na raiz
- Todos os repos do workspace → `.ai-jail` como arquivo padrão de bootstrap

### Exceções

Situações que podem justificar abrir exceção (requer confirmação explícita):
- Ambiente CI/CD onde bubblewrap não está disponível (usar `--lockdown` como fallback)
- Desenvolvimento dentro de container Docker já isolado (doc o racional no ADR)
- macOS com ferramentas de sistema que o sandbox-exec quebra (doc e desative só o que precisar)

---

## Regra de Comportamento para Claude

Quando o usuário solicitar algo que contradiz este padrão (ex: rodar agente sem sandbox, `--dangerously-skip-permissions` sem sandbox envolvente, deploy direto sem revisão), Claude deve:

1. Identificar o conflito com o padrão AIJL
2. Perguntar: *"Isso vai contra o padrão AIJL documentado. Confirma que quer prosseguir sem sandbox?"*
3. Aguardar confirmação explícita antes de executar

---

## Referências

- [Bubblewrap](https://github.com/containers/bubblewrap)
- [ai-jail GitHub](https://github.com/akitaonrails/ai-jail)
- [Landlock LSM](https://landlock.io/)
- [Akita — Artigo 1](https://akitaonrails.com/2026/01/10/ai-agents-garantindo-a-protecao-do-seu-sistema/)
- [Akita — Artigo 2 (ai-jail)](https://akitaonrails.com/2026/03/01/ai-jail-sandbox-para-agentes-de-ia-de-shell-script-a-ferramenta-real/)
