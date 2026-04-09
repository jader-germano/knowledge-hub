# Memória do Projeto: Relatório Mensal de Atividades - Digisystem

**Atualizado em:** 05/03/2026

---

## Visão Geral

Jader Phelipe Germano é colaborador da Digisystem alocado no projeto **Banco de Docentes da EJE** (Escola Judiciária Eleitoral) no **TSE** (Tribunal Superior Eleitoral). Mensalmente, no dia 1º de cada mês, ele precisa preencher um relatório de atividades do mês anterior e enviá-lo ao empregador (Digisystem).

---

## Planilha de Relatório

- **Ferramenta:** Google Sheets (migrado do OneDrive Excel em março/2026)
- **URL:** https://docs.google.com/spreadsheets/d/1GOA37wPrqLp6MpYPO3wdZCBCD85F7v4x88AhmJEmpj8/edit
- **Estrutura:** Uma aba por mês (ex: "Fevereiro 2026", "Marco 2026"...)
- **Colunas:** Data | Descrição da Atividade | Task / Issue Jira
- **Formatação:** Cabeçalho azul (#1155CC), fins de semana em cinza, feriados em amarelo
- **Método de preenchimento:** Apps Script (Extensions > Apps Script) — muito mais confiável que automação direta de UI

### Por que Google Sheets (e não OneDrive Excel)?

O OneDrive Excel Online apresentou muitos problemas para automação via browser:
- Células de data usavam date picker, impossibilitando digitação direta
- Name Box abria dropdown ao invés de navegar para a célula
- Ctrl+V não funcionava para colar dados via clipboard do VM
- Seleções com Shift+Down não funcionavam corretamente

O Google Sheets com Apps Script resolve tudo isso de forma programática, sem depender de UI.

---

## Fonte de Dados: Jira TSE

- **Projeto:** Banco de Docentes da EJE - Acompanhamento do projeto
- **Instância:** https://jira.tse.jus.br
- **Usuário Jira:** jader.germano
- **API REST para buscar issues do mês:**

```
https://jira.tse.jus.br/rest/api/2/search?jql=updated%20%3E%3D%20{ANO}-{MES}-01%20AND%20updated%20%3C%3D%20{ANO}-{MES}-{ULTIMO_DIA}%20AND%20assignee%20in%20(jader.germano)&maxResults=50&fields=summary,status,updated,key
```

Exemplo para fevereiro/2026:
```
https://jira.tse.jus.br/rest/api/2/search?jql=updated%20%3E%3D%202026-02-01%20AND%20updated%20%3C%3D%202026-02-28%20AND%20assignee%20in%20(jader.germano)&maxResults=50&fields=summary,status,updated,key
```

---

## Histórico de Relatórios Preenchidos

### Fevereiro 2026 (preenchido em 05/03/2026)

**Issues encontradas no Jira (11 total):**

| Key | Título | Status | Data Atualização |
|-----|--------|--------|------------------|
| TS1506US-1698 | [MELHORIA] Inclusão de botão "Limpar" para resetar todos os filtros | Backlog | 18/02/2026 |
| TS1506US-1694 | [BUG] Filtro de status exibe opções incorretas | Fechado | 27/02/2026 |
| TS1506US-1693 | [DEV] Implementação de log da LGPD | Em Andamento | 13/02/2026 |
| TS1506US-1692 | [BUG] Comportamento do campo "Especialidades/Matérias" | Em Revisão | 27/02/2026 |
| TS1506US-1661 | [Melhoria] Implementar ordenação de tabela à pesquisa | Fechado | 20/02/2026 |
| TS1506US-1657 | [Melhoria] Incluir paginação e itens por página | Fechado | 20/02/2026 |
| TS1506US-1612 | [DEV - FRONTEND] Tela de Filtros | Fechado | 20/02/2026 |
| TS1506US-1607 | [DEV-BACKEND] Estruturação de serviço de e-mail - FakeSMTP | Fechado | 03/02/2026 |
| TS1506US-1596 | Estruturação de e-mail no Backend - FakeSMTP | Fechado | 09/02/2026 |
| TS1506US-1553 | [DEV] Back end - Ações educacionais | Fechado | 10/02/2026 |
| TS1506STS-843 | Validar GSTI 487687 | Cancelado | 24/02/2026 |

**Dias úteis de fevereiro/2026:** 02, 03, 04, 05, 06, 09, 10, 11, 12, 13, 18, 19, 20, 23, 24, 25, 26, 27 (total: 18 dias)
**Feriados:** 16/02 e 17/02 (Carnaval)
**Fins de semana:** 01, 07, 08, 14, 15, 21, 22, 28

---

## Skill Automatizada

- **Nome:** `relatorio-atividades-digisystem-mensal`
- **Arquivo .skill:** `relatorio-atividades-digisystem-mensal.skill` (pasta do usuário)
- **Agendamento:** Todo dia 1º do mês às 11h00 (cron: `0 11 1 * *`)
- **Fluxo:** Passo 1 (buscar Jira) → Passo 2 (mapear por dia) → Passo 3 (preencher via Apps Script)

---

## Observações Técnicas

- O Apps Script armazenado na planilha precisa de autorização OAuth na primeira execução (aparece popup)
- Após autorizar uma vez, execuções seguintes são automáticas
- O script usa `monaco.editor.getModels()[0].setValue(code)` para injetar código no editor do Apps Script via browser
- Feriados nacionais precisam ser verificados manualmente a cada ano (datas variáveis como Carnaval, Páscoa, Corpus Christi)
