# Session Report - 2026-04-02

## Session Metadata

- objetivo: registrar um case possível de implementação para recuperar o uso
  dos transmissores Kaidi sem depender de novos dongles descartáveis
- workspace afetado: `/Users/philipegermano/code`
- repo documental: `/Users/philipegermano/code/jpglabs/docs`
- status: hipótese documentada, não aprovada para execução
- foco: decisão de investimento, arquitetura-alvo e critérios de go/no-go

## Problem Statement

- O usuário já absorveu perda financeira recorrente com receptores/dongles dos
  kits Kaidi.
- Há necessidade real de mobilidade, inclusive em cenário doméstico com
  deslocamento constante durante reuniões.
- O valor dos transmissores ainda é relevante e justifica explorar uma trilha
  de recuperação de uso antes de descartar o conjunto.
- O usuário não possui, hoje, hardware SDR nem bancada RF para implementação.

## Premissas Explícitas

- Os kits Kaidi `KMF4-A` e `KMF4-C` são comercializados como sistemas
  `2 microfones + 1 receptor`, plug-and-play, o que sugere um enlace
  `2.4 GHz` acoplado ao receptor e não um microfone Bluetooth genérico do
  sistema operacional.
- O protocolo de rádio entre transmissor e receptor pode ser proprietário,
  possivelmente com `pairing`, `FEC`, `codec`, `clocking` e algum nível de
  tráfego bidirecional.
- Sem receptor funcional ou documentação de chipset, um projeto SDR não é
  integração simples; é engenharia reversa de RF e baseband.
- O alvo operacional inicial, se um protótipo vier a existir, deve ser
  `macOS` ou `Linux`. `iOS` não é plataforma adequada para a primeira versão.

## Decisão Recomendada

- Não iniciar compras nem implementação agora.
- Salvar esta trilha apenas como `case possível de implementação`.
- Priorizar, quando houver janela de execução real:
  - `Gate 0`: recuperação elétrica do receptor atual
  - `Gate 1`: investigação RX-only por SDR
  - `Gate 2`: protótipo funcional apenas se Gate 1 provar baixa complexidade

Resumo executivo:

- Se o objetivo for `resultado prático com baixo risco`, o case deve ficar
  arquivado até haver tempo, orçamento e motivação técnica para pesquisa.
- Se o objetivo for `recuperar valor e aprender`, a trilha faz sentido, mas
  precisa de disciplina para matar o projeto cedo se os sinais forem ruins.

## Arquitetura-Alvo

### Gate 0 - Rework Do Receptor Existente

- Abrir o dongle defeituoso.
- Inspecionar:
  - conector USB-C
  - trilhas quebradas
  - solda fria
  - eventual mau contato mecânico entre PCB e conector
- Tentar re-hospedar o PCB em:
  - breakout USB-C de bancada
  - cabo curto pigtail
  - caixa impressa/suporte simples para reduzir esforço mecânico
- Critério de sucesso:
  - o receptor volta a enumerar e operar de forma estável no host
- Critério de falha:
  - PCB danificado, chipset morto ou instabilidade persistente

### Gate 1 - Descoberta Do Enlace RF

- Objetivo:
  - identificar `frequência`, `largura de canal`, `hopping`, `modulação`,
    padrão temporal e dependência de downlink
- Stack sugerida:
  - SDR de entrada para recepção e análise
  - `Universal Radio Hacker` para captura e reversão de protocolo
  - `GNU Radio` para experimentos de demodulação e framing
- Critério de sucesso:
  - portadoras/canais identificados
  - prova de captura consistente de frames do transmissor
  - evidência clara se o link é `uplink-only` ou `bidirecional`
- Critério de falha:
  - hopping agressivo sem fingerprint útil
  - dependência de resposta do receptor em tempo muito curto
  - codec/camada física sem progresso prático após janela controlada de estudo

### Gate 2 - Receiver Em Software

- Só seguir se Gate 1 indicar viabilidade real.
- Meta mínima:
  - suportar `1 transmissor`, `mono`, no `Mac`, com estabilidade suficiente
    para reunião ou gravação curta
- Pipeline alvo:
  - SDR -> demodulação -> framing -> decodificação -> PCM -> dispositivo de
    áudio virtual no host
- Saída de áudio:
  - `BlackHole` ou equivalente como mic virtual no macOS

### Gate 3 - Transceptor/Substituto Completo

- Só seguir se houver prova de que o enlace depende de ACK ou controle ativo.
- Essa fase exige SDR mais capaz e aumenta muito custo e complexidade.
- Alvo:
  - emular o comportamento mínimo do receptor original
- Observação:
  - este gate é o mais arriscado e o primeiro candidato a cancelamento

## Hardware E Ferramentas Por Fase

### Fase Mínima

- ferro/solda fina e fluxo
- lupa ou microscópio simples
- breakout USB-C
- multímetro

### Fase De Descoberta

- SDR de entrada para RX
- antena 2.4 GHz adequada
- atenuador e cabos curtos
- notebook/host para análise

### Fase De Protótipo Funcional

- SDR mais robusto
- áudio virtual no host
- eventual host dedicado para serviço contínuo

## Custo Relativo

- `Gate 0`: baixo
  - melhor relação risco/retorno
- `Gate 1`: médio
  - custo moderado, ainda aceitável como trilha de descoberta
- `Gate 2`: médio para alto
  - depende do resultado de engenharia reversa
- `Gate 3`: alto
  - pode ultrapassar facilmente o custo de substituir todo o sistema por outra
    solução comercial melhor

## Go/No-Go

### Go

- há interesse explícito em projeto experimental
- há janela de estudo prática
- o usuário aceita que o resultado pode ser apenas diagnóstico, sem produto
  final utilizável
- Gate 0 falhou, mas Gate 1 mostra fingerprint reproduzível e arquitetura
  relativamente simples

### No-Go

- o objetivo é solução rápida para trabalho do dia a dia
- não há orçamento para bancada mínima
- o enlace exigir bidirecionalidade estrita e baixa latência sem progresso
  rápido
- o custo total projetado começar a competir com um sistema comercial mais
  confiável

## Riscos

- risco alto de protocolo proprietário complexo
- risco de custo total acima do benefício marginal
- risco de emissão inadequada em `2.4 GHz` se a trilha evoluir para TX
- risco de consumir tempo relevante sem chegar a uma solução de produção
- risco de o resultado final servir para laboratório, mas não para operação
  confiável em reuniões reais

## Recomendação Final

- Este case deve permanecer salvo como opção futura, não como execução
  imediata.
- Quando houver vontade real de atacar o problema, a ordem correta é:
  1. tentar rework do receptor atual
  2. validar o enlace só em recepção
  3. abortar cedo se a camada física ou o protocolo forem hostis
- Recomendação direta:
  - `não comprar hardware de TX/full-duplex no início`
  - `não prometer reaproveitamento integral dos 4 mics`
  - `mirar primeiro em recuperar 1 transmissor de forma estável`

## Deliverable Esperado Se O Case For Aprovado No Futuro

- documento de BOM mínima
- checklist de bancada
- plano de 2 semanas com critérios de abandono
- PoC RX-only
- decisão formal `seguir` ou `encerrar`

## References

- Kaidi KMF4-C:
  https://www.lojacentric.com.br/microfone-de-lapela-compacto-sem-fio-usb-tipo-c-par-kmf4-c-28181
- Kaidi KMF4-A:
  https://www.precisashop.com.br/produtos/microfone-lapela-kaidi-ios-kmf4-a/
- HackRF One docs:
  https://hackrf.readthedocs.io/en/stable/hackrf_one.html
- HackRF FAQ:
  https://hackrf.readthedocs.io/en/stable/faq.html
- bladeRF xA4:
  https://www.nuand.com/product/bladerf-xa4/
- Universal Radio Hacker:
  https://github.com/jopohl/urh
- GNU Radio:
  https://www.gnuradio.org/
- Anatel radiofrequência:
  https://www.gov.br/anatel/pt-br/regulado/radiofrequencia

## Handoff Notes

- O case foi salvo como `possível implementação`, não como backlog aprovado.
- O melhor ROI técnico continua sendo o rework do receptor atual.
- Se a trilha voltar a ficar ativa, o próximo artefato correto é um
  `implementation brief` com BOM, tempo estimado e budget teto.
