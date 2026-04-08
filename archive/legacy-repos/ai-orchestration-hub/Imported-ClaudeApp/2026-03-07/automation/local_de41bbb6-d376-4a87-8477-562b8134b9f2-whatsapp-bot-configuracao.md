# 🤖 WhatsApp Chatbot — Guia de Configuração

> Workflow criado com sucesso no n8n em **05/03/2026**
> **ID do workflow:** `1w34rK2QP45XmmvE`
> **URL:** https://n8n.srv1443703.hstgr.cloud/workflow/1w34rK2QP45XmmvE

---

## O que foi criado

Um chatbot inteligente de 16 nodes no seu n8n que, ao receber uma mensagem no WhatsApp Business, **classifica automaticamente** a mensagem com GPT-4o-mini e age de acordo:

| Categoria | Ação |
|---|---|
| 📋 Recrutamento | Responde com IA + envia e-mail de resumo ao fim do diálogo |
| 🛍️ Produto / Serviço | Responde com IA + envia e-mail de resumo ao fim do diálogo |
| 🚨 Pessoal Urgente | Envia notificação push via Pushover (alerta sonoro) |
| 💬 Pessoal Normal | Sem ação (log silencioso) |

---

## ✅ Checklist de Configuração

### Passo 1 — Editar o node "Configuracoes" no n8n

1. Acesse: https://n8n.srv1443703.hstgr.cloud/workflow/1w34rK2QP45XmmvE
2. Clique no node **"Configuracoes"** (segundo node do fluxo)
3. Substitua cada valor placeholder:

```javascript
CONFIG: {
  OPENAI_KEY:        "sk-COLOQUE_SUA_CHAVE_OPENAI_AQUI",
  WA_ACCESS_TOKEN:   "COLOQUE_SEU_TOKEN_META_PERMANENTE_AQUI",
  PUSHOVER_TOKEN:    "COLOQUE_SEU_APP_TOKEN_PUSHOVER_AQUI",
  PUSHOVER_USER_KEY: "COLOQUE_SEU_USER_KEY_PUSHOVER_AQUI",
  OWNER_EMAIL:       "jader.germano@icloud.com"   // já configurado ✓
}
```

4. Clique em **"Save"**

**Onde obter cada chave:**

- **OpenAI Key** → https://platform.openai.com/api-keys → Create new secret key
- **Meta Access Token** → Meta Developer Portal → WhatsApp → API Setup → gerar token permanente (System User)
- **Pushover Token** → https://pushover.net → Your Applications → Create an Application
- **Pushover User Key** → https://pushover.net → tela inicial (Your User Key)

---

### Passo 2 — Configurar credencial SMTP

O node **"Email Resumo"** precisa de uma credencial SMTP para enviar o e-mail de resumo do diálogo.

1. No n8n, acesse **Settings → Credentials → + Add Credential**
2. Selecione o tipo **"SMTP"**
3. Preencha com os dados do seu servidor de e-mail:
   - Host: `seu.servidor.smtp.com`
   - Porta: `587` (TLS) ou `465` (SSL)
   - Usuário: seu e-mail
   - Senha: sua senha de app
4. Clique em **Save**
5. Volte ao workflow → clique no node **"Email Resumo"** → selecione a credencial criada

---

### Passo 3 — Registrar o Webhook na Meta

Para que as mensagens cheguem ao n8n, você precisa registrar a URL do webhook no Meta Developer Portal.

1. No workflow do n8n, clique no node **"WhatsApp Trigger"**
2. Copie a **Webhook URL** exibida (algo como `https://n8n.srv1443703.hstgr.cloud/webhook/...`)
3. Acesse: https://developers.facebook.com → seu App → **WhatsApp → Configuration**
4. Em **Webhook**, cole a URL copiada
5. Defina o **Verify Token** (qualquer string secreta, ex: `philipe-bot-2026`)
6. Configure o mesmo Verify Token no node **"WhatsApp Trigger"** do n8n
7. Em **Webhook fields**, assine: `messages`
8. Clique em **Verify and Save**

---

### Passo 4 — Ativar o workflow

Após configurar tudo:

1. No workflow, clique no botão **"Inactive"** no topo direito
2. Ele ficará **"Active"** (verde)
3. O bot começará a responder automaticamente

---

## 🔧 Como ajustar o comportamento do bot

### Mudar as instruções de resposta da IA

Abra o node **"Prep Resposta IA"** e edite o `system_prompt`. Exemplo atual:
- Para recrutamento: apresenta Philipe como desenvolvedor sênior e pede mais detalhes
- Para produto/serviço: responde com interesse e agenda conversa

### Mudar a classificação das mensagens

Abra o node **"Prep Classificar"** e edite o prompt de classificação para adicionar ou renomear categorias.

### Mudar a detecção de fim de diálogo

Abra o node **"Verificar Fim Dialogo"** e edite o array `endSignals` com as palavras-chave que indicam encerramento da conversa.

---

## 📊 Ver execuções e logs

1. Acesse: https://n8n.srv1443703.hstgr.cloud/workflow/1w34rK2QP45XmmvE
2. Clique na aba **"Executions"**
3. Cada mensagem recebida aparecerá como uma execução
4. Clique em qualquer execução para ver o resultado de cada node

---

## 🚨 Troubleshooting

| Sintoma | Causa provável | Solução |
|---|---|---|
| Bot não responde nada | Workflow inativo | Ativar o workflow no n8n |
| Erro na classificação IA | OPENAI_KEY inválida | Verificar chave no node Configuracoes |
| Mensagem não enviada no WA | WA_ACCESS_TOKEN expirado | Gerar novo token permanente na Meta |
| Push não chegou | Token Pushover errado | Verificar PUSHOVER_TOKEN e PUSHOVER_USER_KEY |
| E-mail não chegou | Credencial SMTP não configurada | Seguir Passo 2 acima |
| Webhook não recebe | URL não registrada na Meta | Seguir Passo 3 acima |

---

## 📋 Resumo do workflow (16 nodes)

```
[1]  WhatsApp Trigger       ← recebe mensagens via webhook Meta
[2]  Configuracoes          ← ⚙️ EDITAR AQUI: todas as chaves de API
[3]  Extrair Mensagem       ← extrai texto, remetente, phone number ID
[4]  Prep Classificar       ← monta prompt para classificar a mensagem
[5]  IA Classificar         ← chama GPT-4o-mini para classificar
[6]  Processar Classificacao← parse do JSON retornado pela IA
[7]  Roteador               ← switch com 4 saídas por categoria
[8]  Prep Resposta IA       ← monta prompt de resposta (business msgs)
[9]  IA Gerar Resposta      ← chama GPT-4o-mini para gerar resposta
[10] Prep Envio WA          ← monta payload para a Meta Graph API
[11] Enviar WhatsApp        ← POST na Meta API v18.0 para enviar msg
[12] Verificar Fim Dialogo  ← detecta sinais de encerramento
[13] Dialogo Encerrado      ← IF: diálogo encerrou?
[14] Email Resumo           ← envia HTML com resumo do diálogo
[15] Pushover Urgente       ← push notification para msgs urgentes
[16] Pessoal Normal Log     ← sem ação (noOp)
```

---

*Gerado automaticamente por Claude em 05/03/2026*
