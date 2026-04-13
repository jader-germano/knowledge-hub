# CLAUDE — jpglabs-saas

## Bootstrap Rápido

Ao trabalhar neste projeto, carregar a skill obrigatória de sessão:
```
~/.claude/scheduled-tasks/jpglabs-session-bootstrap/SKILL.md
```

## Contexto do Projeto

- **Produto**: Monitor de Licitações SaaS (B2B, engenharia)
- **Empresa**: JPGLABS TECNOLOGIA LTDA — CNPJ 56.090.159/0001-07
- **Fase atual**: Fase 0 (fundação fiscal) → Fase 1 (MVP)
- **Contabilidade**: keycont.com.br — contabilidade@keycont.com.br

## Stack Principal

- Java 21 + Spring Boot 3.x (back-end API + Spring Batch)
-Nest.js 15 + TypeScript (front-end)
- Supabase PostgreSQL (banco multi-tenant)
- Claude API Sonnet 4.6 (análise de editais)

## Regras Deste Contexto

1. Documentação em **português**, código em **inglês**
2. Erros e bloqueios → abrir **Bug no Jira** (label: `bloqueio`)
3. Novas features → **Story no Jira** vinculada ao Epic MVP
4. Docs importantes → espelhar no **Confluence** (space JPGLABS)
5. Não iniciar dev de monetização antes de CNAE TI incluído no CNPJ

## Jira — Atalhos

```bash
# Listar issues abertas (projeto: SCRUM, cloudId: d9f316a4-b4d8-40c9-a90a-0539675e39a1)
ATLASSIAN_PAT=$(security find-generic-password -s jpglabs-atlassian-mcp -a jader.germano -w 2>/dev/null)
curl -s "https://jpglabs.atlassian.net/rest/api/3/search?jql=project=SCRUM+AND+status!=Done" \
  -H "Authorization: Bearer $ATLASSIAN_PAT" | jq '.issues[] | {key:.key, summary:.fields.summary, status:.fields.status.name}'
# Jira: https://jpglabs.atlassian.net/jira
# Confluence: https://jadergermano.atlassian.net/wiki
```

## Arquivos-chave Locais

| Arquivo | Propósito |
|---|---|
| `/Users/philipegermano/contratos/jpglabs/STATUS.md` | Estado atual do projeto |
| `/Users/philipegermano/contratos/jpglabs/06_keycont-draft/email-keycont.md` | Draft para enviar ao contador |
| `/Users/philipegermano/contratos/jpglabs/03_fiscal-juridico/checklist-fiscal.md` | Checklist fiscal pendente |
