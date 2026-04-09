# design-system-pipeline

Use esta skill quando a tarefa envolver extração de tokens de design de arquivos HTML,
construção ou comparação de design systems, ou geração do relatório visual Token Atlas.

## Quando Ativar

- "extrair tokens de design"
- "rodar o pipeline de design"
- "comparar os temas / design systems"
- "gerar o Token Atlas"
- "build de design system a partir dos HTMLs"
- "atualizar os tokens de cor / tipografia / espaçamento"
- qualquer referência aos 4 temas: Google Light, Stripe Editorial Dark,
  Monkeytype Terminal Dark, JPGLabs Product Dark

## Ferramenta

```
/Users/philipegermano/code/design-pipeline/pipeline.py
```

Dependência: `anthropic>=0.43.0` — instalar com:

```bash
pip install -r /Users/philipegermano/code/design-pipeline/requirements.txt
```

Variável de ambiente obrigatória: `ANTHROPIC_API_KEY`

## Protocolo de Execução

### Run completo (sem outputs anteriores)

```bash
cd /Users/philipegermano/code/design-pipeline
python pipeline.py \
  --html /path/to/google.html \
         /path/to/stripe.html \
         /path/to/jpglabs.html \
         /path/to/monkeytype.html
```

### Retomar a partir de um step específico

```bash
python pipeline.py --from-step 2 --run-id <run_id>
python pipeline.py --from-step 5 --run-id <run_id>   # só gerar o Token Atlas
```

O `run_id` é o nome do subdiretório em `outputs/` (formato `YYYYMMDD-HHMM` por padrão).

### Localizar os HTMLs de referência

Os 4 arquivos de referência foram salvos via browser. Se não estiverem em `~/code`,
verificar em:
- `~/Downloads/`
- repositórios atuais dentro de `/Users/philipegermano/code/`

Não usar o path antigo do iCloud como referência operacional viva.

## Etapas e HITL

| Step | Nome | Output | HITL |
|------|------|--------|------|
| 1 | Extração por arquivo HTML | `01_extracted_<slug>.json` x4 | Obrigatório |
| 2 | Normalização cross-file | `02_normalized.json` | Obrigatório |
| 3 | Manifesto Figma | `03_figma_manifest.json` | Obrigatório |
| 4 | Export CSS + JSON | `04_tokens.css`, `04_tokens.json` | Obrigatório |
| 5 | Token Atlas HTML | `05_token_atlas.html` | Obrigatório |

Em cada fronteira o usuário pode:
- **[A]** Aprovar e continuar
- **[E]** Editar o arquivo de output e continuar
- **[R]** Refazer o step com instrução adicional
- **[Q]** Encerrar o pipeline

Não pular etapas sem aprovação explícita. Cada step depende dos outputs do anterior.

## Output Final

O arquivo `05_token_atlas.html` é um relatório visual interativo com:
- 4 cards de tema (renderizados nas cores de cada tema)
- Grid de tokens de cor com Compare Mode entre temas
- Specimens de tipografia + tabela de escala
- Barras de spacing proporcionais
- Quadrados demonstrativos de radius
- Previews animados de motion easings
- Chips de componentes estilizados por tema

Abrir com:

```bash
open outputs/<run_id>/05_token_atlas.html
```

## Gaps Conhecidos

- Os HTMLs de referência do JPGLabs não incluem o CSS bundle compilado; extração
  parcial até o bundle estar disponível.
- Cores art-direction do Stripe (covers) devem permanecer separadas dos tokens UI.

## Ownership

Esta skill é compartilhada pelo hub. Qualquer bootstrap de provedor deve apontar
para esta versão canônica.

Índice: `manifests/skills.index.yaml`
