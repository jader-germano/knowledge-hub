# JPG Labs — Documentação de Infraestrutura
**Domínio:** jpglabs.com.br | **VPS IP:** 187.77.227.151 (Hostinger)
**OS:** Ubuntu 24.04 LTS | **Atualizado:** 07/03/2026

---

## Checklist de Status

| Etapa | Status |
|-------|--------|
| Registro do domínio `jpglabs.com.br` | ✅ Concluído |
| Cloudflare — domínio adicionado e DNS configurado | ✅ Concluído |
| Registro.br — nameservers atualizados para Cloudflare | ✅ Concluído |
| Cloudflare API token created and stored securely | ✅ Concluído |
| VPS — n8n + Traefik rodando com SSL | ✅ Concluído |
| VPS — docker-mailserver configurado e imagem baixada | ✅ Concluído |
| Portas de email abertas (25, 143, 465, 587, 993) | ✅ Concluído |
| Propagação NS para Cloudflare | ⏳ Em andamento (1–24h) |
| SSL para mail.jpglabs.com.br via certbot | ⏳ Aguardando NS |
| docker-mailserver iniciado | ⏳ Aguardando NS |
| Contas de email criadas | ⏳ Após start do DMS |
| DKIM TXT no Cloudflare DNS | ⏳ Após start do DMS |
| Claude API no VPS | ⏳ Próximo passo |
| Upgrade Claude Team/Enterprise | ⏳ Após email funcionar |

---

## 1. Registro do Domínio

| Campo | Valor |
|---|---|
| Domínio | `jpglabs.com.br` |
| Titular | Jader Philipe Germano |
| E-mail | `jader.germano@icloud.com` |
| Status | ✅ Registrado e pago |

---

## 2. Cloudflare DNS

**Conta:** `jader.germano@icloud.com` | **Plano:** Free | **Login:** GitHub SSO
**Zone ID:** stored in Cloudflare dashboard / secret manager

### Nameservers configurados no Registro.br
```
dane.ns.cloudflare.com
ingrid.ns.cloudflare.com
```

### Registros DNS

| Tipo | Nome | Valor | Proxy | Status |
|------|------|-------|-------|--------|
| A | `@` | `187.77.227.151` | ✅ | ✅ |
| A | `www` | `187.77.227.151` | ✅ | ✅ |
| A | `n8n` | `187.77.227.151` | ✅ | ✅ |
| A | `mail` | `187.77.227.151` | DNS only | ✅ |
| MX | `@` | `mail.jpglabs.com.br` (pri 10) | DNS only | ✅ |
| TXT | `@` | `v=spf1 mx ~all` | DNS only | ✅ |
| TXT | `_dmarc` | `v=DMARC1; p=quarantine; rua=mailto:jader@jpglabs.com.br` | DNS only | ✅ |
| TXT | `mail._domainkey` | *(gerado pelo DMS — DKIM)* | DNS only | ⏳ |

### Cloudflare API Token
- **Token:** stored securely outside versioned docs
- **Escopo:** Zone DNS Edit — jpglabs.com.br
- **Arquivo no VPS:** `/root/.secrets/cloudflare.ini` (chmod 600)
- **Uso:** certbot DNS-01 challenge para SSL
- **Política:** nunca registrar token real em markdown, screenshots ou logs
- **Ação:** rotate immediately if a real token was ever committed or shared

---

## 3. VPS — n8n + Traefik

**Diretório:** `/docker/n8n/`
**URL:** https://n8n.jpglabs.com.br (após NS propagar) / https://n8n.srv1443703.hstgr.cloud (já funciona)
**Stack:** n8n + Traefik com SSL automático Let's Encrypt

### .env configurado
```env
DOMAIN_NAME=jpglabs.com.br
SSL_EMAIL=jader.germano@icloud.com
GENERIC_TIMEZONE=America/Sao_Paulo
```

### Comandos
```bash
cd /docker/n8n
docker compose ps          # status
docker compose logs -f     # logs em tempo real
docker compose restart     # reiniciar
```

---

## 4. VPS — docker-mailserver

**Diretório:** `/docker/mailserver/`
**Imagem:** `ghcr.io/docker-mailserver/docker-mailserver:latest` (já baixada)
**SSL:** Let's Encrypt via certbot + Cloudflare DNS-01 challenge

### Arquivos configurados
| Arquivo | Descrição |
|---------|-----------|
| `docker-compose.yml` | Stack config com portas e volumes |
| `mailserver.env` | Config DMS: DKIM, DMARC, SpamAssassin, Fail2ban |
| `setup.sh` | Helper oficial do docker-mailserver |
| `finish-setup.sh` | Script de finalização automática |

### Portas
| Porta | Protocolo | Uso |
|-------|-----------|-----|
| 25 | SMTP | Recebimento de email externo |
| 143 | IMAP | Leitura de email (sem SSL) |
| 465 | ESMTP SSL | Envio com SSL implícito |
| 587 | Submission | Envio com STARTTLS |
| 993 | IMAPS | Leitura de email com SSL |

### Para completar o setup (após NS propagar)
```bash
# Verificar propagação primeiro:
dig NS jpglabs.com.br @8.8.8.8 +short
# Deve retornar: dane.ns.cloudflare.com / ingrid.ns.cloudflare.com

# Executar script de finalização:
bash /docker/mailserver/finish-setup.sh
```

O script faz automaticamente:
1. Verifica propagação NS
2. Obtém SSL para `mail.jpglabs.com.br` via certbot
3. Sobe o docker-mailserver
4. Cria contas `jader@jpglabs.com.br` e `contato@jpglabs.com.br`
5. Gera chaves DKIM e exibe registro TXT para Cloudflare
6. Reinicia para aplicar DKIM

### Certbot manual (se necessário)
```bash
certbot certonly --dns-cloudflare \
  --dns-cloudflare-credentials /root/.secrets/cloudflare.ini \
  --dns-cloudflare-propagation-seconds 60 \
  -d mail.jpglabs.com.br \
  --email jader.germano@icloud.com \
  --agree-tos --non-interactive
```

### Após o script — Adicionar DKIM no Cloudflare
O script exibirá o valor. Adicionar no Cloudflare DNS:
- **Tipo:** TXT
- **Nome:** `mail._domainkey`
- **Valor:** `v=DKIM1; h=sha256; k=rsa; p=MII...` (exibido pelo script)

### Comandos de gerenciamento
```bash
cd /docker/mailserver
docker compose ps
docker compose logs -f
docker exec mailserver setup email list
docker exec mailserver setup email add user@jpglabs.com.br
docker exec mailserver setup email del user@jpglabs.com.br
```

---

## 5. Contas de Email (após setup)

| Email | Uso |
|-------|-----|
| `jader@jpglabs.com.br` | Principal — Jader |
| `contato@jpglabs.com.br` | Contato geral JPG Labs |

### Configuração cliente de email
| Campo | Valor |
|-------|-------|
| IMAP Host | `mail.jpglabs.com.br` |
| IMAP Port | `993` (SSL/TLS) |
| SMTP Host | `mail.jpglabs.com.br` |
| SMTP Port | `587` (STARTTLS) ou `465` (SSL) |
| Usuário | email completo (ex: `jader@jpglabs.com.br`) |
| Senha | definida no `finish-setup.sh` |

---

## 6. Estrutura de Arquivos no VPS

```
/docker/
├── n8n/
│   ├── docker-compose.yml
│   └── .env
└── mailserver/
    ├── docker-compose.yml
    ├── mailserver.env
    ├── setup.sh
    ├── finish-setup.sh
    └── docker-data/dms/         (criado ao subir o container)
        ├── mail-data/
        ├── mail-state/
        ├── mail-logs/
        └── config/opendkim/keys/jpglabs.com.br/mail.txt

/root/.secrets/
└── cloudflare.ini               (API token certbot)

/etc/letsencrypt/live/
├── n8n.jpglabs.com.br/          (após NS propagar)
└── mail.jpglabs.com.br/         (após finish-setup.sh)
```

---

## 7. Comandos de Verificação DNS

```bash
# Nameservers (deve mostrar Cloudflare após propagação)
dig NS jpglabs.com.br @8.8.8.8 +short

# IP do servidor de mail
dig A mail.jpglabs.com.br @1.1.1.1 +short

# Registro MX
dig MX jpglabs.com.br @1.1.1.1 +short

# SPF e DMARC
dig TXT jpglabs.com.br @1.1.1.1 +short

# DKIM (após gerado)
dig TXT mail._domainkey.jpglabs.com.br @1.1.1.1 +short

# Checar propagação global
# https://dnschecker.org/#NS/jpglabs.com.br
```

---

## 8. Links e Acessos

| Serviço | URL |
|---------|-----|
| n8n (domínio próprio) | https://n8n.jpglabs.com.br |
| n8n (Hostinger direto) | https://n8n.srv1443703.hstgr.cloud |
| Cloudflare Dashboard | https://dash.cloudflare.com |
| Hostinger VPS Panel | https://hpanel.hostinger.com/vps/1443703/overview |
| Registro.br | https://registro.br |
| DNS Checker | https://dnschecker.org/#NS/jpglabs.com.br |

---

## 9. Próximos Passos

1. ⏳ Aguardar propagação NS (verificar com `dig NS jpglabs.com.br @8.8.8.8 +short`)
2. ▶️ Rodar `bash /docker/mailserver/finish-setup.sh`
3. ▶️ Adicionar registro DKIM no Cloudflare (exibido pelo script)
4. ▶️ Testar envio/recebimento de email em `jader@jpglabs.com.br`
5. ▶️ Configurar Claude API no VPS
6. ▶️ Fazer upgrade para Claude Team/Enterprise com `jader@jpglabs.com.br`

---

*JPG Labs Infrastructure — Documentação gerada automaticamente em 07/03/2026*
