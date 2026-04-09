# Scripts

Scripts utilitários do hub.

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
