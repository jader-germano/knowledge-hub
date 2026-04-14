# Plano de Proteção para AI Agents

Referência principal: artigo do Akita sobre proteção de sistemas ao operar com agentes de IA.

## Objetivo

Aplicar um modelo operacional seguro para agentes em workspaces locais, bridges de Markdown, MCPs e repositórios compartilhados sem perder velocidade de desenvolvimento.
jpglabs/docs/reports/sessions/_template/report.md
## Princípios

- isolamento por workspace e por projeto
- acesso mínimo a arquivos e segredos
- política explícita para comandos destrutivos ou de publicação
- rastreabilidade entre documentação, implementação e testes
- dependência opcional de MCP para recursos avançados, nunca para o núcleo local-first

## Fase 1. Isolamento e permissões

- executar agentes dentro de sandbox por projeto
- restringir escrita ao repositório ativo e aos diretórios de saída previstos
- tratar `git push`, `docker run`, `rm`, `rebase` e deploy como ações com confirmação
- negar acesso padrão a diretórios de credenciais amplas e dados pessoais fora do escopo do projeto

## Fase 2. Segredos e bridges

- manter segredos fora do alcance padrão dos agentes
- usar arquivos de configuração compartilhados só quando necessários e documentados
- separar bridge local-first de bridges remotos opcionais
- evitar que leitura e edição do vault dependam de serviços externos

## Fase 3. Qualidade e revisão

- TDD como regra de entrada para novas fatias
- documentação por categoria e escopo ligada a código, testes e API docs
- validação mínima de integração antes de conectar novos MCPs ou fontes externas
- revisão de risco antes de automações que toquem deploy, versionamento ou dados sensíveis

## Fase 4. Observabilidade operacional

- registrar comandos sensíveis executados na sessão
- registrar arquivos alterados e repositório afetado
- manter handoff entre agentes com resumo factual e sem segredos
- manter inventário de MCPs, bridges e superfícies de escrita

## Aplicação por repositório

### `apple-study-checklist`

- reforçar o modelo local-first do vault
- cobrir em testes os fluxos de criar vault editável, importar pasta externa e salvar arquivo
- completar internacionalização e edição de arquivos dentro do app sem depender de MCP

### `FrankMD`

- aproveitar o filesystem-first como superfície primária de conhecimento
- versionar notas técnicas, handoffs e estudos como Markdown
- usar o app como base de visualização e edição local do conhecimento

### `knowledge-hub`

- manter classificação de documentos, handoff entre agentes e regras compartilhadas
- centralizar inventário de práticas e referências de segurança operacional

### `infrastructure`
Tailscale MagicDNS (recomendado)  │ https://srv1443703.tail4c4f3a.ts.net:8384 │ user: jpglabs / pass: jpgl4bs-sync! │                   
├───────────────────────────────────┼───────────────────────────────────────────┼─────────────────────────────────────┤
│ Tailscale IP direto               │ https://100.68.217.36:8384                │ mesma auth                          │                     
├───────────────────────────────────┼───────────────────────────────────────────┼─────────────────────────────────────┤                     
│ DNS público (após criar A record) │ http://syncthing.jpglabs.com.br           │ Syncthing built-in auth (mesma)

- aplicar a mesma política de risco a workflows, infraestrutura e automação
- isolar credenciais e reforçar revisão para qualquer mudança que toque VPS, k3s ou integração externa

## Componentes reaproveitáveis da comunidade open source

- sandbox de processo e filesystem em estilo jail para agentes
- documentação filesystem-first em Markdown
- portais de docs com hierarquia estável e rastreabilidade
- convenções claras de TDD, suites por camada e DocC ou equivalente para superfícies de API

## Próximos passos

1. transformar permissões atuais em política mais explícita por categoria de comando
2. fechar testes de integração dos fluxos críticos de vault
3. documentar bridge local-first e bridge remoto opcional como superfícies distintas
4. consolidar o inventário mensal de repositórios, práticas e referências reaproveitáveis
