# Estratégia de Stack de IA — JPGLabs

**Última atualização:** 2026-04-08  
**Decisão de:** Jader Philipe Germano

---

## Separação Fundamental

| Camada | Modelo | Uso | Visibilidade |
|--------|--------|-----|--------------|
| **Ferramenta de trabalho** | Claude (Anthropic) | Produção interna do Philipe — arquitetura, código, docs, planejamento | Interno |
| **Stack de entrega** | QwinCoder na VPS | Produto entregue a clientes — análise de editais, automações, prospecting | Externo / produto |

**Princípio:** Claude é como um IDE premium — o dev usa, o cliente não sabe e não precisa saber. O produto entregável usa modelos próprios, self-hosted, sem dependência de terceiros na cadeia de valor do cliente.

---

## Por Que Essa Separação

1. **Controle de custo de entrega** — Ollama self-hosted na VPS tem custo fixo, sem consumo por token do cliente
2. **Independência de fornecedor** — produto não depende de APIs externas de IA para funcionar
3. **Oferta diferenciada** — JPGLabs pode garantir privacidade de dados (os dados dos clientes não saem da infra JPGLabs)
4. **Posicionamento** — o produto é "IA proprietária JPGLabs", não "powered by Anthropic"
5. **Claude como vantagem competitiva pessoal** — Philipe usa Claude para produzir mais rápido, mas isso é vantagem operacional, não dependência técnica do produto

---

## QwinCoder na VPS

**Modelo:** `qwen2.5-coder` (ou equivalente) via Ollama  
**Endpoint interno:** `http://localhost:11434` (dentro da VPS) / `http://100.68.217.36:11434` (via Tailscale — sem túnel SSH)  
**Status atual:** ✅ operacional

### Casos de uso de entrega

| Caso de uso | Input | Output esperado |
|-------------|-------|-----------------|
| Análise de editais (jpglabs-saas) | PDF/texto do edital PNCP | JSON estruturado com requisitos, prazo, valor, fit |
| Geração de oferta LinkedIn | Perfil do lead + contexto JPGLabs | Mensagem de prospecção personalizada |
| Cards de Confluence | Briefing de projeto | Página/card formatado em Confluence |
| Automações n8n | Trigger de evento | Ação gerada por LLM |

### Integração com n8n

```
n8n workflow → POST http://localhost:11434/api/generate → resposta LLM → ação downstream
```

Todos os workflows de automação que usam IA devem apontar para o endpoint Ollama da VPS, nunca para APIs externas de IA.

---

## Claude — Uso Interno

Claude (via Claude Code) é usado por Philipe para:

- Arquitetura de sistemas (ADRs, diagramas, planejamento de fases)
- Implementação guiada (pair programming, code review, TDD)
- Documentação técnica (Confluence, markdown, specs)
- Automação do próprio workflow (skills, sessões, health checks)
- Análise de contexto e tomada de decisão técnica

Claude **não deve aparecer** em:
- Código de produto entregado a clientes
- Workflows n8n de atendimento/entrega
- Stack de análise do jpglabs-saas
- Materiais de prospecção como "tecnologia usada"

---

## Roteamento de IA — Hierarquia de Fallback

```
Tarefa de entrega (n8n / automação / análise)
       │
       ▼
[1. PRIMARY] Ollama VPS — qwen2.5-coder:7b
  22 tok/s | self-hosted | zero custo por token
       │ indisponível ou qualidade insuficiente
       ▼
[2. FALLBACK] NVIDIA NIM — nvidia/llama-3.3-nemotron-super-49b-v1.5
  qualidade real de nemotron | pay-per-use | sem infra local
  Free tier: 1.000 chamadas/mês | https://build.nvidia.com
  Chave keychain: security find-generic-password -s nvidia-nim-api -a jpglabs -w
```

**Endpoint NIM (OpenAI-compatible):**
```
OPENAI_BASE_URL=https://integrate.api.nvidia.com/v1
OPENAI_MODEL=nvidia/llama-3.3-nemotron-super-49b-v1.5
```

---

## Roadmap de Estabilização da Stack de Entrega

### Fase A — Ollama VPS operacional ✅ CONCLUÍDO (2026-04-08)

- [x] Pull `qwen2.5-coder:7b` no Ollama da VPS (4.7 GB)
- [x] Benchmark: **22.7 tok/s**, 5.4s resposta, português validado
- [x] Tailscale instalado na VPS — endpoint acessível em `http://100.68.217.36:11434`
- [x] Validado: `curl http://100.68.217.36:11434/api/tags` funciona do Mac sem túnel SSH
- [ ] Benchmark de análise de edital de teste (PDF → JSON estruturado)

### Fase A2 — NVIDIA NIM Fallback

- [ ] Criar conta em https://build.nvidia.com → obter API key (free tier)
- [ ] Salvar chave: `security add-generic-password -s nvidia-nim-api -a jpglabs -w <KEY>`
- [ ] Testar endpoint NIM com `nvidia/llama-3.3-nemotron-super-49b-v1.5`
- [ ] Config openclaude `.env` MODO B pronto para ativar quando necessário

### Fase B — Automações de prospecção LinkedIn + Confluence

> **Pré-requisito:** n8n deployado no k8s da VPS (não está rodando atualmente)

- [ ] Deploy n8n no k3s da VPS (`/opt/k8s-deployments/`)
- [ ] Workflow: perfil LinkedIn + contexto JPGLabs → Ollama VPS → mensagem personalizada
- [ ] Fallback no workflow: se Ollama falhar → NVIDIA NIM
- [ ] Card Confluence gerado automaticamente com resultado e histórico

### Fase C — Análise de editais (jpglabs-saas)

- [ ] Spring Boot → Ollama VPS (endpoint interno Tailscale)
- [ ] Prompt calibrado para extração de campos-chave de editais
- [ ] Fallback: Ollama falha → NVIDIA NIM → análise processada
- [ ] Cache de análise no Supabase (não reprocessar mesmo edital)

---

## Modelos Disponíveis na VPS (Ollama)

| Modelo | Tamanho | tok/s | Finalidade | Status |
|--------|---------|-------|-----------|--------|
| `qwen2.5-coder:7b` | 4.7 GB | **22.7** | Delivery primário | ✅ Ativo |
| `codellama:7b` | 3.8 GB | ~20 | Geração de código | ✅ Disponível |
| `llava:latest` | 4.7 GB | ~18 | Multimodal | ✅ Disponível |
| `qwen2.5:32b-instruct-q4_K_M` | 19 GB | 5.2 | Raciocínio pesado (lento) | ✅ Disponível |
| `deepseek-r1:7b` | 4.7 GB | ~20 | Raciocínio | ✅ Disponível |
| `nemotron-3-super:latest` | 86 GB | <2 | Excede RAM (32 GB) — uso local inviável | ⚠️ |

## Modelos NVIDIA NIM (cloud fallback)

| Modelo ID | Qualidade | Custo |
|-----------|-----------|-------|
| `nvidia/llama-3.3-nemotron-super-49b-v1.5` | ⭐⭐⭐⭐⭐ | ~$0.40/1M tok |
| `nvidia/llama-3.1-nemotron-ultra-253b-v1` | ⭐⭐⭐⭐⭐+ | maior/mais caro |
| `nvidia/llama-3.1-nemotron-70b-instruct` | ⭐⭐⭐⭐ | mais rápido |

---

## Regra para Claude

Ao projetar funcionalidades do `jpglabs-saas` ou de qualquer produto JPGLabs entregável:
- Propor arquitetura com Ollama/QwinCoder como camada de IA
- Nunca incluir Claude API na stack de entrega sem confirmação explícita
- Se houver justificativa técnica para usar Claude API temporariamente (ex: capacidade que QwinCoder não cobre), documentar como dívida técnica a substituir
