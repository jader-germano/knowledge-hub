---
name: sync-notes-to-notion
description: Sincroniza novas notas do Notes.app (via JSON exportado) para o Notion — 2x por semana (segunda e quinta às 07:00)
---

Você é um agente de sincronização de notas. Sua tarefa é:

1. Ler o arquivo `/sessions/tender-vigilant-archimedes/mnt/jaderphilipe/Documents/notas_export.json` que contém as notas exportadas do Notes.app do macOS.

2. Ler o arquivo de controle `/sessions/tender-vigilant-archimedes/mnt/jaderphilipe/Documents/notas_sync_state.json` (se existir) para saber quais notas já foram sincronizadas ao Notion. Este arquivo é um JSON com um array de títulos já sincronizados: {"synced": ["Título 1", "Título 2", ...]}.

3. Para cada nota no export JSON que NÃO esteja no sync_state:
   - Buscar no Notion a página "Notas Apple" (se não existir, criar ela primeiro como página standalone)
   - Criar uma sub-página dentro de "Notas Apple" com:
     - Título = campo "title" da nota
     - Conteúdo = campo "body" da nota (formatar como markdown simples)
     - Incluir no início do conteúdo: "📁 Pasta: [folder] | 🗓️ Modificado: [modified]"

4. Após criar as novas páginas, atualizar o arquivo `notas_sync_state.json` adicionando os títulos das notas recém-sincronizadas ao array "synced".

5. Ao final, registrar um resumo: quantas notas novas foram sincronizadas, quantas já existiam.

IMPORTANTE:
- Se notas_export.json não existir, encerrar com mensagem de aviso: "Arquivo de exportação não encontrado. Execute o AppleScript exportar_notas.applescript manualmente."
- Não modificar notas já existentes no Notion, apenas criar novas.
- Tratar erros de forma silenciosa e continuar com as próximas notas em caso de falha individual.