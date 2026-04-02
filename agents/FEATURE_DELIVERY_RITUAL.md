# Feature Delivery Ritual

Use este rito para toda sessão que abra, avance ou feche uma `feature`.

Ele complementa o `agents/SESSION_CLOSE_TEMPLATE.md` e define o pacote mínimo
de evidência para considerar uma fatia realmente entregue.

## Quando aplicar

- branch `feature/*`
- fatia de produto com comportamento novo, ajustado ou validado
- sessão que altera fluxo, UI, navegação, vault, sync, revisão ou contrato de
  uso

Sessões só de pesquisa, grooming ou documentação podem usar o template de
fechamento sem declarar a feature como entregue.

## Gate de abertura

Antes de implementar:

1. definir `feature/session id`
2. registrar objetivo aprovado da sessão
3. listar entregáveis explícitos
4. declarar escopo fora da sessão
5. apontar o arquivo ou frame do Figma quando houver impacto visual ou de fluxo

Se a fatia tocar UI, navegação, sessão, revisão ou sync, não abrir execução sem
link de Figma ou sem registrar claramente por que o protótipo ainda não é
necessário.

## Definition of Done

Uma sessão de feature só fecha como válida quando existir:

1. implementação ou validação objetiva do escopo combinado
2. testes e builds executados para a fatia
3. atualização documental proporcional ao impacto
4. evidência operacional do fluxo em macOS
5. evidência operacional do fluxo em iOS
6. relatório de sessão com links e artefatos localizáveis

## Pacote obrigatório de evidências

Cada sessão de feature deve gerar uma pasta em:

`/Users/philipegermano/code/jpglabs/docs/projects/<repo>/sessions/<feature-id>/<yyyy-mm-dd-session>/`

Conteúdo mínimo:

- `report.md`
- `prototype.md` ou link explícito para o frame/arquivo Figma
- `macos.gif`
- `ios.gif`

Conteúdo opcional quando ajudar a auditoria:

- `screenshot-*.png`
- `logs.txt`
- `diff.txt`

## Campos obrigatórios do relatório

- `feature/session id`
- repositório e branch
- objetivo aprovado
- entregáveis explícitos
- link do arquivo ou frame Figma
- evidência `macOS`: GIF e breve descrição do fluxo validado
- evidência `iOS`: GIF e breve descrição do fluxo validado
- testes, builds e comandos executados
- arquivos criados e modificados
- riscos, gaps e próximos passos
- commits ou diffs relacionados

## Regra de fechamento

Sem `report.md`, `macos.gif` e `ios.gif`, a sessão não deve ser marcada como
feature concluída.

Se a sessão terminar apenas em planejamento ou design, isso deve estar explícito
no relatório e o fechamento não conta como entrega funcional.
