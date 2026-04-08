# jpglabs-saas — Arquitetura e Fases de Desenvolvimento

**Produto:** Monitor de Licitações SaaS  
**Empresa:** JPGLABS TECNOLOGIA LTDA (CNPJ 56.090.159/0001-07)  
**Última atualização:** 2026-04-08

---

## Contexto de Negócio

B2B vertical para engenharia: empresas de engenharia e construção que precisam monitorar licitações públicas (PNCP — Portal Nacional de Contratações Públicas) sem gastar horas manualmente filtrando editais irrelevantes.

**Proposta de valor:** "Você recebe só as licitações que fazem sentido para o seu negócio, com análise de fit já feita."

---

## Stack Técnica

### Camada de Produto

| Componente | Tecnologia | Deploy |
|------------|-----------|--------|
| API REST + Batch | Spring Boot 3.x / Java 21 | Railway |
| Frontend | Next.js 15 + TypeScript + shadcn/ui + Tailwind | Vercel |
| Banco de dados | Supabase PostgreSQL (multi-tenant, RLS) | Supabase Cloud |
| Pagamentos | Pagar.me (PIX + cartão) | Pagar.me API |
| Ingestão de editais | Spring Batch (jobs agendados) | Railway |

### Camada de IA (entrega)

| Componente | Tecnologia | Notas |
|------------|-----------|-------|
| Análise de editais | QwinCoder (Qwen2.5-Coder) via Ollama VPS | Self-hosted, sem custo por token |
| Endpoint IA | `http://vpglabs-vps-tailnet:11434` | Acesso interno via Tailscale |
| Fallback | Fila assíncrona no Railway se VPS indisponível | |

> Claude **não** faz parte da stack de entrega. É ferramenta de trabalho interno do Philipe.

### Segurança de Agentes

- Sessões de desenvolvimento: `ai-jail claude` (padrão AIJL)
- `.ai-jail` na raiz do repositório
- Dados do cliente não saem da infra JPGLabs

---

## Modelo de Dados — Entidades Principais

```
Tenant (empresa cliente)
  ├── User (membros da empresa)
  ├── Profile (critérios de busca: segmentos, regiões, valores)
  └── Subscription (plano, status, datas)

Licitação (cache do PNCP)
  ├── raw_json (dados originais)
  ├── edital_text (texto extraído)
  └── Analysis (resultado da IA por Tenant/Profile)
       ├── fit_score (0-100)
       ├── requisitos[]
       ├── prazo
       ├── valor_estimado
       └── recomendacao (participar/não participar/verificar)

Alerta
  ├── tenant_id
  ├── licitacao_id
  ├── canal (email / webhook / dashboard)
  └── enviado_em
```

**Multi-tenancy:** Row Level Security no Supabase. Cada tenant vê apenas seus dados. A tabela `Licitação` é compartilhada (cache global do PNCP); a tabela `Analysis` é por tenant.

---

## Arquitetura de Sistema

```
[PNCP API] ──► [Spring Batch Job (Railway)]
                    │
                    ▼
            [Supabase PostgreSQL]
            (licitacoes, raw_json)
                    │
                    ▼ (nova licitação que match profile)
            [Spring Boot API]
                    │
                    ├──► [Ollama VPS / QwinCoder]
                    │       └──► Analysis JSON → Supabase
                    │
                    ├──► [Alerta: email/webhook]
                    │
                    └──► [Next.js Frontend / Vercel]
                              └──► Dashboard do cliente
```

---

## Fluxo Principal — Análise de Edital

```
1. Batch Job detecta nova licitação no PNCP que match profile de algum tenant
2. Extrai texto do edital (PDF → texto)
3. POST → Ollama VPS:
   {
     "model": "qwen2.5-coder:7b",
     "system": "Você é um especialista em licitações públicas...",
     "prompt": "<texto do edital>"
   }
4. Recebe JSON estruturado com fit_score, requisitos, prazo, valor
5. Salva em Analysis no Supabase (vinculado ao tenant)
6. Dispara alerta se fit_score > threshold do tenant
7. Atualiza dashboard do cliente
```

---

## Fases de Desenvolvimento

### Fase 0 — Fundação Fiscal (ATUAL)
**Bloqueio:** processo JUCESP em andamento (alteração razão social + CNAEs TI)  
**Meta:** CNPJ com CNAEs de TI antes do primeiro faturamento

- [x] CNPJ registrado (56.090.159/0001-07)
- [x] Repositório GitLab criado
- [x] Jira + Confluence configurados
- [ ] **BLOQUEANTE:** CNAE TI incluído via JUCESP ← email enviado para Keycont
- [ ] Conta PJ aberta (Nubank PJ ou Inter PJ)

---

### Fase 1 — Scaffold + Landing Page (MVP Mínimo)
**Objetivo:** ter algo publicável, capturar lista de espera, validar demanda  
**Desbloqueio:** após CNAE TI aprovado

#### 1.1 Scaffold Técnico
- [ ] Inicializar Spring Boot 3.x no GitLab
- [ ] Inicializar Next.js 15 + shadcn/ui no GitLab
- [ ] Configurar Supabase projeto com schema inicial
- [ ] Deploy base: Railway (API) + Vercel (Frontend)
- [ ] `.ai-jail` na raiz + `ai-jail --bootstrap`

#### 1.2 Landing Page
- [ ] Página de apresentação do produto (Next.js)
- [ ] Formulário de lista de espera (Supabase table `waitlist`)
- [ ] Deploy em `jpglabs.com.br` (Vercel + Cloudflare)

#### 1.3 Integração PNCP (Leitura)
- [ ] Spring Batch job: pull licitações do PNCP por categoria/região
- [ ] Salvar em `licitacoes` no Supabase
- [ ] Endpoint de busca básico no Spring Boot

**Critério de aceite Fase 1:** Landing no ar, lista de espera funcionando, job PNCP rodando no Railway com dados chegando no Supabase.

---

### Fase 2 — MVP Funcional
**Objetivo:** primeiro cliente pagante  
**Desbloqueio:** após Fase 1 validar lista de espera com ≥ 10 interessados

#### 2.1 Autenticação e Multi-tenancy
- [ ] Supabase Auth (email/password + Google OAuth)
- [ ] RLS configurado por tenant
- [ ] Onboarding: criação de Profile (segmentos, regiões, faixa de valor)

#### 2.2 Análise por IA
- [ ] QwinCoder na VPS estabilizado (ver `AI_STACK_STRATEGY.md`)
- [ ] Spring Boot → Ollama VPS integration
- [ ] Análise de edital → JSON → Supabase `analysis`
- [ ] Prompt de sistema calibrado para licitações de engenharia

#### 2.3 Dashboard
- [ ] Lista de licitações com fit_score
- [ ] Detalhe do edital + análise da IA
- [ ] Filtros: data, valor, região, segmento

#### 2.4 Alertas
- [ ] Email de alerta quando nova licitação com fit_score > threshold
- [ ] Configuração de threshold por Profile

#### 2.5 Pagamentos
- [ ] Pagar.me: planos mensais (PIX + cartão)
- [ ] Webhook de confirmação de pagamento → ativa Subscription
- [ ] Trial gratuito de 14 dias

**Critério de aceite Fase 2:** cliente consegue criar conta, configurar perfil, receber alertas e pagar. Primeiro pagamento recebido.

---

### Fase 3 — Escala e Retenção
**Objetivo:** reduzir churn, aumentar valor percebido  
**Desbloqueio:** após 10 clientes ativos na Fase 2

- [ ] Relatórios exportáveis (PDF/Excel)
- [ ] Integração webhook para ERPs e sistemas de licitação dos clientes
- [ ] App mobile (React Native ou PWA)
- [ ] API pública para integrações (documentada no Postman)
- [ ] Painel de admin JPGLabs (gestão de tenants, billing, suporte)
- [ ] SLA de disponibilidade: 99.5%+

---

## Decisões Arquiteturais (ADRs)

### ADR-001: Self-hosted AI vs Claude API
**Decisão:** Usar QwinCoder/Ollama na VPS para análise de editais, não Claude API.  
**Motivo:** controle de custo, privacidade de dados do cliente, independência de fornecedor.  
**Trade-off:** qualidade de análise pode ser inferior para editais complexos; mitigar com prompt engineering e calibração.  
**Revisão:** após 3 meses de produção, comparar acurácia com benchmark manual.

### ADR-002: Spring Boot para API e Batch
**Decisão:** Manter Spring Boot 3.x / Java 21 para backend.  
**Motivo:** Spring Batch é maduro para jobs de ingestão de PNCP; Java 21 virtual threads para performance de I/O.  
**Trade-off:** mais verboso que Node/Python; mitigado com Lombok e geração de código.

### ADR-003: Supabase para multi-tenancy
**Decisão:** Row Level Security no Supabase para isolamento de tenants.  
**Motivo:** zero overhead de infra para multi-tenancy; RLS em SQL é auditável.  
**Trade-off:** lock-in no Supabase; mitigado exportando schemas como migrations versionadas.

---

## Próxima Ação Imediata

**Bloqueante:** aguardar resposta da Keycont sobre CNAE TI.  
**Paralelo enquanto espera:**
1. Pull `qwen2.5-coder:7b` na VPS e validar endpoint
2. Inicializar scaffold Spring Boot + Next.js no GitLab
3. Configurar Supabase projeto com schema inicial de `licitacoes` e `tenants`
