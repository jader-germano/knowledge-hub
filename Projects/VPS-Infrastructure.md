# 🖥️ VPS Infrastructure

> Host: `187.77.227.151` (Hostinger)  
> Domain: `jpglabs.com.br` (Cloudflare)  
> OS: Ubuntu 24.04 LTS (fresh after reinstall)

---

## Services

| Service | URL | Status |
|---------|-----|--------|
| Portfolio | https://jpglabs.com.br | 🔄 deploying |
| AI API | https://api.jpglabs.com.br | 🔄 deploying |
| n8n | https://n8n.jpglabs.com.br | 🔄 deploying |
| Open-WebUI | https://chat.jpglabs.com.br | 🔄 deploying |

## Deploy

```bash
# After VPS reinstall:
# 1. Install k3s
curl -sfL https://get.k3s.io | sh -

# 2. Copy manifests to VPS
scp -r ~/code/pessoal/jpglabs/infrastructure/k8s/ root@187.77.227.151:/k8s/

# 3. Fill secrets
ssh root@187.77.227.151 "cp /k8s/02-secrets-template.yaml /k8s/02-secrets.yaml"
# Edit 02-secrets.yaml on VPS with real values

# 4. Deploy
ssh root@187.77.227.151 "bash /k8s/apply-all.sh"
```

## Links
- [[Projects/AwesomePie]] — uses api.jpglabs.com.br as VPS tier
- [[Projects/Pi-Agent]] — memory synced via sync-memory.sh
- [[Backlog/00-Backlog]] — deploy items
