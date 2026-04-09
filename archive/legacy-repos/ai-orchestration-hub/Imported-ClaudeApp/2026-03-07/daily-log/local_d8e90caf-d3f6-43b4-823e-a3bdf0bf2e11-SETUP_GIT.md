# 🔧 Setup Git — Autenticação (fazer apenas 1 vez)

Para que a automação diária consiga fazer push para o GitHub automaticamente,
você precisa criar um Personal Access Token (PAT) e configurá-lo uma vez.

## Passo 1 — Criar o token no GitHub

1. Acesse: https://github.com/settings/tokens/new
2. Preencha:
   - **Note:** `daily-log-automation`
   - **Expiration:** `No expiration` (ou 1 ano)
   - **Scopes:** marque ✅ `repo` (acesso completo a repositórios privados)
3. Clique em **Generate token**
4. **Copie o token gerado** (começa com `ghp_...`) — você só verá uma vez!

## Passo 2 — Configurar no terminal do seu Mac

Abra o Terminal e cole os comandos abaixo, substituindo `SEU_TOKEN` pelo token copiado:

```bash
cd ~/Library/CloudStorage  # ou o caminho onde está sua pasta outputs
# Navegue até a pasta outputs onde o git foi inicializado
cd /caminho/para/outputs

git config credential.helper store
echo "https://jader-germano:SEU_TOKEN@github.com" > ~/.git-credentials
git pull origin main --allow-unrelated-histories
git push -u origin main
```

## Passo 3 — Verificar

```bash
git log --oneline
```

Se aparecer o histórico, está tudo funcionando! ✅

---

> Após configurado, a automação diária fará push automaticamente todo dia às 9h.
