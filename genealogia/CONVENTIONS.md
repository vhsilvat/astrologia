# Genealogia da Astrologia: contrato de extensão

Leia este arquivo inteiro antes de mexer em qualquer outro. Ele existe para que qualquer instância futura do Claude, de qualquer versão, continue o trabalho sem depender da conversa em que ele nasceu. Tudo o que importa está nestes arquivos.

## 1. Para quem e para quê

- **Usuário:** Victor (@333victorhugo). Aprende melhor de forma visual, conectando os pontos. Quer ser desafiado no raciocínio, não afirmado.
- **Uso:** apoio de estudo e de roteiro para um canal de YouTube sobre astrologia como *correspondência ontológica* (Plotino, Jung), não como causação. O rigor histórico é a marca do canal.
- **O que o mapa mostra:** quem ensinou, influenciou, criticou ou reivindicou quem, no tempo. Cada linha precisa poder ser defendida com fonte.

## 2. Arquivos

```
index (a página HTML)       renderizador; não guarda dados
data/domains.json           eixo do tempo, tipos de relação, lista de domínios (temas)
data/<dominio>.json         um arquivo por domínio ativo
CONVENTIONS.md              este contrato
```

A página lê os JSON por `fetch` relativo, valida tudo ao carregar e mostra o resultado no rodapé ("Integridade"). **Nunca** coloque dados dentro do HTML.

## 3. Como estender (procedimento)

1. Liste os artifacts do usuário e abra o da "Genealogia da Astrologia". Leia a página com `action: "read"`, depois leia `CONVENTIONS.md` e `data/*.json` com `path`/`paths`.
2. Edite os JSON (não o HTML, salvo para corrigir o renderizador).
3. Republique **no mesmo URL** (nunca crie um artifact novo), enviando em `files` os arquivos alterados.
4. Abra a página e confira o rodapé "Integridade": deve dizer OK. Corrija avisos antes de dizer que terminou.
5. Acrescente uma linha ao Registro de mudanças (seção 9).

## 4. Idempotência (regras)

- **`id` é estável e imutável:** slug ASCII minúsculo, sem acento (`jamblico`, `court-de-gebelin`). Nunca renomeie um id existente.
- **Upsert, nunca duplicar:** se o `id` já existe, atualize o nó. Antes de criar, procure por nome e por apelido.
- **Relação é única por (`from`, `to`, `type`).** Se existe, atualize `desc`; não crie outra.
- **Cada pessoa aparece uma vez**, no domínio onde mais importa. Outros domínios ligam a ela por relações (podem cruzar arquivos).
- Reaplicar o mesmo conjunto de mudanças duas vezes deve produzir o mesmo resultado.

## 5. Esquema

`data/domains.json`
- `axis.knots`: pares `[ano, x]` que definem a escala do tempo (por partes, não linear). Para ampliar o eixo, acrescente um nó no fim e aumente o espaço das épocas densas. Ano negativo = a.C.
- `axis.ticks`, `axis.eras`: marcas e rótulos de épocas.
- `edgeTypes`: `mestre`, `influencia`, `critica`, `debatido`, `reivindicada` (cada um com `label` e `dash`).
- `domains[]`: `id`, `name`, `status` (`ativo` ou `planejado`), `file`, `desc`.

`data/<dominio>.json`
- `lanes[]`: `{id, name, color}`. `id` com prefixo do domínio (`astro.tecnica`). `color` é 1–8 (tokens `--c1`…`--c8`).
- `nodes[]`: `{id, name, date, yr, lane, dy, work, why}`
  - `yr`: ano aproximado usado na posição (negativo = a.C.). `date` é o texto exibido.
  - `dy`: posição do rótulo, `-1` acima, `-2` acima mais alto, `1` abaixo, `2` abaixo mais baixo. Use para evitar sobreposição (o validador avisa).
  - `work`: obra(s) principal(is). `why`: uma ou duas frases verificáveis; sem adjetivo vazio.
- `edges[]`: `{from, to, type, desc}`. A seta vai de quem age ao alvo (mestre → discípulo; influência → influenciado; crítico → criticado).
- `trails[]`: `{id, name, intro, steps:[{node, read, hours}]}`. A numeração nos nós vem da primeira trilha do domínio.
- `lineages[]`: `{id, name, nodes:[ids]}`, conjuntos para destacar.

## 6. Regras de rigor (não negociáveis)

- **Não afirme linhagem sem fonte.** Escolha o tipo com honestidade:
  - `influencia`/`mestre`: documentado em fonte antiga ou em bibliografia acadêmica.
  - `debatido`: estudiosos discordam (ex.: orfismo ↔ pitagorismo).
  - `reivindicada`: a própria tradição diz, mas não há documentação (ex.: "o tarot veio do Egito"; as origens alegadas da Golden Dawn). **É isso que impede que história e mito se misturem.**
- **Autoria e datas incertas:** diga na `date` ("c.", "séc.") e, se preciso, em `why`. Pseudepigrafia é dita como tal.
- **Verifique antes de acrescentar.** Use busca na web para datas e títulos. Na dúvida, não inclua ou marque `debatido`.
- **Não derive correspondências em causa.** O tom do mapa é histórico, não de validação do sistema simbólico.
- Texto em português do Brasil, sem travessão como pausa, sem adjetivação de efeito.

## 7. Domínios planejados e mapa de encaixe (candidatos a verificar)

Nada abaixo está no mapa ainda. São sugestões, cada uma exige verificação de fonte.

- **Tarot e cartomancia:** jogo de trionfi (Itália, séc. XV); Court de Gébelin (1781, origem egípcia reivindicada); Etteilla (1783); Éliphas Lévi; Golden Dawn (1888); Waite–Smith (1909); Crowley–Harris (Thoth). Apoio crítico: Michael Dummett; Decker e Dummett, *A History of the Occult Tarot*.
- **Hermetismo e magia cerimonial:** Agrippa, Dee, Lévi, Blavatsky, Golden Dawn, Crowley (A∴A∴, Thelema, *The Equinox*), *Kybalion* (1908). Ligar ao nó `hermetica` e a `casaubon` já existentes.
- **Alquimia (planejado):** Zósimo, Paracelso e outros alquimistas lidos por Jung em *Estudos Alquímicos* (CW13). Gerhard Dorn não foi verificado. Ligar a `jung` e a `hermetica`.
- **Candidatos ainda por verificar para `psicologia`:** Richard Tarnas (*The Passion of the Western Mind*, *Cosmos and Psyche*), Stephen Arroyo, Howard Sasportas, Marc Edmund Jones, Alice Bailey, Charles Carter, Margaret Hone, Bruno e Louise Huber, Roberto Assagioli, Shawn Carlson (teste duplo-cego, *Nature*, 1985, como nó crítico). A relação `alan-leo → rudhyar` não tem fonte conferida e não foi incluída (Hand, no prefácio de *Saturn*, só diz que Leo já apontava nessa direção).

Ao ativar um domínio: criar `data/<dominio>.json`, mudar `status` para `ativo` em `domains.json`, definir faixas, nós, relações, trilha e linhagens. Não altere a trilha da astrologia nem os ids existentes.

## 8. Pegadinhas conhecidas

- O renderizador desenha as relações só entre nós visíveis. Se um domínio está desligado, as relações cruzadas somem.
- Rótulos podem colidir quando dois nós da mesma faixa estão a menos de ~80 px. Ajuste `dy`.
- Numeração da trilha: o primeiro domínio ativo usa 1, 2, 3; os demais usam letras a, b, c, para não repetir números nos círculos.
- Ao abrir, só o primeiro domínio ativo fica ligado. Os outros se ligam pelos botões de tema.
- Relações podem cruzar arquivos (ex.: `platao → jung` mora em `psicologia.json`). Cada relação vive no arquivo do domínio que a introduz.
- O título da página é "Genealogia da Astrologia". Se o segundo domínio entrar, considere perguntar ao usuário antes de renomear.

## 9. Registro de mudanças (acrescente no fim, nunca apague)

- 2026-10-19 · v1 · Domínio `astrologia`: 37 nós, 46 relações, trilha mínima de 11 etapas (~73 h), 3 linhagens. Estrutura em JSON, validador, domínios planejados (tarot, magia, psicologia).
- 2026-10-19 · v2 · Domínio `psicologia` ativado: 6 nós (Alan Leo, Evangeline Adams, Rudhyar, Greene, Jung, Pauli), 6 relações (3 cruzam para a astrologia), 1 trilha, 2 linhagens. Domínio `alquimia` planejado. Fontes: Wikipedia (Psychological astrology, Alan Leo, Evangeline Adams, Liz Greene, Dane Rudhyar, Synchronicity, Alchemical Studies); Psicologia e Alquimia (1944), Mysterium (1955–56) e ensaio de Pauli sobre Kepler (1952) vêm de conhecimento geral, conferir se for citar no canal.
- 2026-10-19 · v3 · Relação `rudhyar → greene` (influencia) acrescentada, fonte: Robert Hand, prefácio de *Saturn: A New Look at an Old Devil* (Weiser, 2011), p. 5–6. Total: 43 nós, 53 relações.
