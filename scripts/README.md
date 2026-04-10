# Scripts

Scripts utilitários do hub.

## `sync-session-close.py`

Sincroniza o fechamento canônico de uma sessão a partir do `report.md`.

### Objetivos

- manter `report.md` como artefato humano principal
- sincronizar a entrada correspondente em `/Users/philipegermano/code/daily/`
- sincronizar um resumo operacional em `agents/AGENT_BRIDGE.md`
- emitir ou atualizar o sidecar JSON em `memory/events/`
- tentar projetar o sidecar no grafo derivado sem transformar o grafo em
  blocker de fechamento

### Uso

```bash
python3 /Users/philipegermano/code/jpglabs/docs/scripts/sync-session-close.py \
  --report /Users/philipegermano/code/jpglabs/docs/projects/<repo>/sessions/<feature-id>/<yyyy-mm-dd-session>/report.md \
  --write
```

### Limites

- o script assume que `report.md` já está fechado e com estrutura suficiente
- a projeção no Docker MCP pode falhar sem invalidar o fechamento
- sessões legadas continuam dependendo de backfill e curadoria

## `backfill-session-sidecars.py`

Importa relatórios legados em sidecars JSON e pode reescrever sidecars
importados quando houver metadata mais precisa em `report.md` ou no diário.

## `fed-safe.sh`

Wrapper local para abrir o `FrankMD` sem alterar o projeto original.

### Objetivos

- limpar explicitamente o container `frankmd` anterior
- evitar reaproveitar uma sessão Docker antiga por engano
- não repassar por padrão secrets de providers e `FRANKMD_ENV`
- restringir o alvo ao subtree de `/Users/philipegermano/code`

### Uso

```bash
zsh /Users/philipegermano/code/jpglabs/docs/scripts/fed-safe.sh
zsh /Users/philipegermano/code/jpglabs/docs/scripts/fed-safe.sh /Users/philipegermano/code/jpglabs/docs
```

### Limites

- o wrapper melhora higiene operacional, não isolamento forte
- depois que o Docker sobe o container, o sandbox do shell não é o principal
  controle de segurança
- a proteção real depende do escopo do diretório montado e do modo de acesso

### Recomendação

- leitura: preferir visão curada ou read-only
- edição: montar apenas o recorte realmente necessário
- evitar mount bruto do workspace inteiro quando um subconjunto resolve
