---
name: daily-job-applications
description: Candidaturas diárias: 10 no LinkedIn + 5 nos repos GitHub de vagas + resumo diário + git push
---

## Objetivo
Aplicar a até **10 vagas no LinkedIn** e **5 vagas nos repositórios GitHub de vagas brasileiras**, registrar tudo em arquivos de resumo diário e fazer push para o GitHub do usuário.

---

## Perfil do Usuário — Jader Germano

- **Nome:** Jader Germano
- **Email:** jader.germano@icloud.com
- **Telefone:** +55 61981945408
- **Localização:** Brasília, Brasil
- **LinkedIn:** https://www.linkedin.com/in/jader-germano/
- **Empresa atual:** DIGISYSTEM - IT Solutions
- **Salário atual:** R$ 14.900
- **Pretensão salarial:** R$ 18.000 (BRL) / USD 3.500 (para vagas contractor em dólar)
- **Inglês:** Avançado | **Espanhol:** Básico

### Stack técnica
- Java: 5 anos | Angular: 6 anos | Node.js / NestJS / TypeScript: sim
- Spring Boot, Microservices, REST APIs, Kafka, Docker, AWS
- React: **NÃO profissional — não aplicar para vagas focadas em React**

### CV a usar
Selecionar sempre o PDF mais recente disponível no LinkedIn Easy Apply (geralmente "CV - Jader Germano - Pt.pdf").

---

## Regras de Filtragem de Vagas

| Critério | Ação |
|----------|------|
| Stack moderna: Java 17+, Spring Boot 3.x, Angular 14+, Node.js, NestJS, TypeScript, Docker, Kafka | ✅ APLICAR |
| Stack legada: EJB, Struts, JSP, etc. | ❌ PULAR (a menos que salário/range > R$ 20.000) |
| Foco em React como principal | ❌ PULAR |
| Presencial ou híbrido fora de Brasília | ❌ PULAR |
| Issue com label "Stale" no GitHub | ❌ PULAR |
| Limite diário LinkedIn | Máximo 10 candidaturas |
| Limite diário GitHub repos | Máximo 5 candidaturas |

---

## PARTE 1 — LinkedIn Easy Apply (até 10 vagas)

### Passo 1 — Abrir LinkedIn Jobs

Navegue para:
```
https://www.linkedin.com/jobs/search/?f_AL=true&f_WT=2&keywords=Java%20Full%20Stack%20Developer&location=Brazil
```
Filtros: `f_AL=true` (Easy Apply only) | `f_WT=2` (Remote only)

### Passo 2 — Revisar e Aplicar

Para cada vaga (até 10):

**a)** Leia o título e descrição completa
**b)** Verifique compatibilidade com as regras acima
**c)** Se compatível, clique em "Easy Apply" e preencha:
- **Contato:** jader.germano@icloud.com | Brasil (+55) | 61981945408
- **CV:** selecionar PDF mais recente
- **Campos de salário:** atual = 14900, pretensão = 18000 (USD 3500 se contractor)
  - ⚠️ Alguns campos aceitam apenas números sem formatação (ex: `18000` não `R$ 18.000`)
- **Anos de experiência:** Java=5, Angular=6, Node.js/NestJS=Sim, Backend=5
- **URL LinkedIn:** https://www.linkedin.com/in/jader-germano/
- **Empresa atual:** DIGISYSTEM - IT Solutions
- **Inglês:** Avançado

**d)** Submeter e confirmar "Your application was sent"
**e)** Registrar: empresa, vaga, stack, resultado

---

## PARTE 2 — GitHub Repositórios de Vagas (até 5 vagas)

### Passo 1 — Buscar issues abertas compatíveis

Verifique os seguintes repositórios, nesta ordem de prioridade:

**1. backend-br/vagas — Java:**
```
https://github.com/backend-br/vagas/issues?q=is%3Aopen+label%3ARemoto+label%3AJava+-label%3AStale&sort=created&direction=desc
```

**2. backend-br/vagas — Node.js:**
```
https://github.com/backend-br/vagas/issues?q=is%3Aopen+label%3ARemoto+label%3ANode.js+-label%3AStale&sort=created&direction=desc
```

**3. nodejsdevbr/vagas — abertas recentes:**
```
https://github.com/nodejsdevbr/vagas/issues?q=is%3Aopen+-label%3AStale&sort=created&direction=desc
```

**4. frontendbr/vagas — Angular (opcional, se não atingiu 5):**
```
https://github.com/frontendbr/vagas/issues?q=is%3Aopen+label%3AAngular+-label%3AStale&sort=created&direction=desc
```

### Passo 2 — Analisar cada issue

Para cada issue aberta:

**a)** Leia o título: verificar se é Java, Node.js, NestJS, TypeScript, Angular, Spring Boot
**b)** Leia o corpo: verificar salário (pular se legada e < R$20k), stack, requisitos
**c)** Verificar se NÃO tem label "Stale" (seria fechada em breve)
**d)** Localizar o **link de candidatura** — geralmente aparece como:
   - `Como se candidatar: [link]`
   - `Link: https://...`
   - `👉 Link para cadastro: https://...`
   - `🔗 https://...`

### Passo 3 — Candidatar via link da issue

**a)** Abrir o link de candidatura da issue
**b)** Preencher o formulário com os dados de Jader (nome, email, telefone, LinkedIn, CV)
**c)** Cada empresa tem seu próprio sistema (Greenhouse, Lever, Gupy, inhire.app, etc.)
   - Campos comuns: nome, email, telefone, LinkedIn URL, upload de CV, anos de experiência
   - Salário: R$18.000 ou USD 3.500 conforme a vaga
**d)** Confirmar envio e registrar resultado
**e)** Marcar a notificação no GitHub como "Done" se aplicável

---

## PARTE 3 — Criar Arquivo de Resumo do Dia

Crie ou atualize o arquivo detalhado em:
```
/sessions/hopeful-exciting-cannon/mnt/outputs/diario/YYYY-MM-DD.md
```

### Estrutura do arquivo diário:

```markdown
# 📋 Diário — DD de mês de AAAA

## 💼 Candidaturas LinkedIn (X/10)

| Empresa | Vaga | Stack | Status |
|---------|------|-------|--------|
| ... | ... | ... | ✅/❌/⏭️ |

## 🐙 Candidaturas GitHub Repos (X/5)

| Repo | Issue | Empresa | Stack | Link | Status |
|------|-------|---------|-------|------|--------|
| backend-br/vagas | #XXXX | ... | ... | ... | ✅/❌ |

## 📬 Mensagens / Notificações relevantes
(Informações compartilhadas pelo usuário ou detectadas no browser)

## ⏭️ Vagas Puladas
| Vaga | Motivo |
|------|--------|
| ... | Legacy tech / React focus / Stale / etc. |

## 📊 Resumo do dia
- LinkedIn: X/10 candidaturas enviadas
- GitHub: X/5 candidaturas enviadas
- Total: X candidaturas no dia
```

---

## PARTE 4 — Atualizar Índice Principal

Atualize o arquivo `/sessions/hopeful-exciting-cannon/mnt/outputs/resumo_diario.md` adicionando uma linha na tabela de índice:

```markdown
| [YYYY-MM-DD](diario/YYYY-MM-DD.md) | ✅ X LinkedIn + X GitHub | [outras tarefas se houver] | [conclusão em 1 frase] |
```

---

## PARTE 5 — Commit e Push para o GitHub

```bash
cd /sessions/hopeful-exciting-cannon/mnt/outputs

# Remover lock file se existir (pode sobrar de sessões anteriores)
rm -f .git/index.lock

git add -A

TODAY=$(date +%Y-%m-%d)
git commit -m "daily: candidaturas e resumo $TODAY"

git push origin main
```

Se o push falhar por falta de credenciais, registrar no arquivo do dia:
```
⚠️ Push para GitHub pendente — configurar autenticação conforme SETUP_GIT.md
```

---

## Critério de Sucesso

- [ ] Até 10 candidaturas LinkedIn Easy Apply submetidas
- [ ] Até 5 candidaturas via GitHub repos submetidas
- [ ] Arquivo `diario/YYYY-MM-DD.md` criado com todos os detalhes
- [ ] `resumo_diario.md` atualizado com nova linha no índice
- [ ] Commit e push realizados (ou erro documentado)

---

## Notas Importantes

- Se LinkedIn exibir CAPTCHA ou verificação de bot: parar e registrar no diário
- Vagas que exigem cover letter manual além do Easy Apply: pular
- Se vaga já aparece como "Applied" no LinkedIn: pular
- Issues GitHub com label "Stale": pular (serão fechadas em breve)
- Campos de salário: tentar formato numérico simples se formatado der erro
- Aguardar sempre confirmação de envio antes de marcar como ✅
- Se um site de candidatura (Gupy, Greenhouse, etc.) exigir criar conta do zero: pular e registrar
