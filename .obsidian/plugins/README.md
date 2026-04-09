# Plugins recomendados — JPGLabs Docs Vault

Plugins listados em `community-plugins.json`. Para instalar: Obsidian → Settings →
Community plugins → Browse → pesquisar pelo nome.

## Essenciais

| Plugin | ID | Uso |
|--------|-----|-----|
| **Dataview** | `dataview` | Queries sobre frontmatter (listas dinâmicas de projetos, daily notes) |
| **Templater** | `templater-obsidian` | Templates com variáveis dinâmicas (`{{date}}`, `{{title}}` etc.) |
| **Calendar** | `calendar` | Navegação visual por daily notes |

## Opcionais / QoL

| Plugin | ID | Uso |
|--------|-----|-----|
| **Style Settings** | `obsidian-style-settings` | Customização visual do tema |

## Sem plugins (plain Obsidian)

O vault funciona sem nenhum plugin. Os templates em `_templates/` usam a sintaxe
nativa `{{date}}` e `{{title}}` do plugin core Templates (já ativo). Dataview queries
têm fallbacks em comentários HTML nos arquivos que as usam.

## Não instalar (conflitos conhecidos)

- `obsidian-git` — o repo usa GitLab com SSH configurado; conflito com hooks customizados
- qualquer plugin de sync — o vault usa Obsidian Sync nativo (já ativo no core)
