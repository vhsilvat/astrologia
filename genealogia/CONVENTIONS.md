# A Cadeia de Ouro: contrato de extensão

Leia este arquivo inteiro antes de mexer em qualquer outro. Ele existe para que qualquer instância futura do Claude, de qualquer versão, continue o trabalho sem depender da conversa em que ele nasceu.

## 1. Para quem e para quê

- **Usuário:** Victor (@333victorhugo). Aprende melhor de forma visual, conectando os pontos. Quer ser desafiado no raciocínio, não afirmado.
- **Uso:** apoio de estudo e de roteiro para um canal de YouTube sobre astrologia como *correspondência ontológica* (Plotino, Jung), não como causação. O rigor histórico é a marca do canal.
- **Tema e título:** "A Cadeia de Ouro" é a *aurea catena* homérica (Ilíada VIII), que Macróbio e os neoplatônicos leem como a corrente que liga o alto ao baixo. O mapa segue a **tese de correspondência** ("em cima como embaixo") e suas críticas. A imagem tem dois sentidos que usamos: cadeia de seres e causas, e cadeia de transmissão entre mestres.
- **Critério de entrada:** uma figura, texto ou tradição entra se *transmite, transforma, critica ou serve de ponto de referência* para a tese de correspondência **e** tem ao menos uma relação documentada com algo que já está no mapa. Sem as duas coisas, fica na lista de candidatos (seção 7). O cristianismo antigo entra como ponto de referência (arcontes, elementos, Logos, reação gnóstica), não como tema doutrinal.
- **O que o mapa mostra:** não é mais só astrologia. É um mapa geral de relações entre figuras, textos e tradições (astrologia, mito, alquimia e gnose, psicologia profunda, e depois tarot e magia): quem ensinou, influenciou, criticou, identificou com quem ou reivindicou quem, no tempo. Cada linha precisa poder ser defendida com fonte.

## 2. Arquivos

```
index.html                  renderizador; não guarda dados
data/domains.json           título, eixo do tempo, tipos de relação, lista de temas
data/<tema>.json            figuras (nodes) e faixas (lanes) de UM tema
data/relacoes.json          TODAS as relações, inclusive entre temas
data/trilhas.json           trilhas de leitura e linhagens, inclusive entre temas
tools/mapa.py               CLI: única forma recomendada de alterar os dados
tools/gerar_obsidian.py     gera obsidian/ (via `mapa.py build`)
```

Relações e trilhas moram fora dos arquivos de tema porque cruzam temas (Zósimo, da alquimia, leva a Jung, da psicologia). Assim nenhuma relação "pertence" a um tema e remover um tema não deixa pontas soltas escondidas. **Nunca** coloque dados dentro do HTML.

## 3. Como alterar (procedimento)

1. Rode `python3 tools/mapa.py validate`. Deve dizer OK antes de começar.
2. Use os comandos da CLI (seção 4). Edição manual de JSON é permitida, mas passe pelo `validate` e, de preferência, deixe o próprio `mapa.py` regravar em formato canônico: `python3 tools/mapa.py --dry validate` não grava; qualquer comando de escrita regrava tudo em ordem estável.
3. `python3 tools/mapa.py build` regenera `obsidian/`.
4. Para a página publicada como artifact: leia o artifact (`action: "read"`), republique **no mesmo URL** enviando em `files` `data/*.json` (e `index.html` se mudou). Abra e confira o rodapé "Integridade": deve dizer OK.
5. Acrescente uma linha ao Registro de mudanças (seção 9) e faça commit.

## 4. CLI e idempotência

Opção global `--dry` (antes do comando): valida e diz o que mudaria sem gravar.

```
mapa.py validate
mapa.py list nodes|edges|trails|lineages|lanes
mapa.py show <id>
mapa.py add-node --id X --domain T --lane L --name N --date D --yr 1500 --dy -1 --work W --why Y
mapa.py add-node --id X --why "novo texto"          # figura existente: só atualiza os campos dados
mapa.py rm-node <id>                                  # apaga também relações, passos e linhagens que o citam
mapa.py add-edge <de> <para> <tipo> "descrição"       # upsert por (de, para, tipo)
mapa.py rm-edge <de> <para> [tipo]
mapa.py edit-trail <id> [--name N] [--intro I]          # renomeia sem mexer nos passos
mapa.py trail <id> "Nome" "Introdução" "no|leitura|horas" ... [--default]
mapa.py rm-trail <id>
mapa.py lineage <id> "Nome" no1 no2 ...
mapa.py rm-lineage <id>
mapa.py add-domain <id> "Nome" "Descrição" [--before <id>]
mapa.py add-lane <tema> <id> "Nome" [--color 1-8]
mapa.py set-title "Título" "Subtítulo"
mapa.py build
```

Garantias:
- Rodar o mesmo comando duas vezes dá o mesmo resultado (a segunda diz "nada a mudar").
- Toda escrita valida o conjunto inteiro antes de gravar; se houver problema, nada é gravado.
- A gravação é canônica (figuras ordenadas por faixa, ano e id; relações por origem, destino e tipo; JSON com indentação fixa). Dois Claudes editando em paralelo geram diffs mínimos e fáceis de mesclar.
- `rm-node` é em cascata; `trail` e `lineage` substituem a definição inteira pelo id dado.
- Relações sem direção (`identificacao`) são normalizadas: `hermes thoth` e `thoth hermes` são a mesma relação.

Regras de identidade:
- **`id` é estável e imutável:** slug ASCII minúsculo, sem acento (`jamblico`, `court-de-gebelin`). Nunca renomeie.
- **Upsert, nunca duplicar:** antes de criar, procure por nome e por apelido (`mapa.py list nodes`).
- **Relação é única por (`from`, `to`, `type`).**
- **Cada figura aparece uma vez**, no tema onde mais importa. Outros temas ligam a ela por relações.

## 5. Esquema

`data/domains.json`
- `title`, `subtitle`: título e subtítulo exibidos.
- `axis.knots`: pares `[ano, x]` da escala de tempo (por partes, não linear; a.C. é negativo). Começa em -2500 (Egito). Para ampliar, acrescente um nó no fim.
- `axis.ticks`, `axis.eras`: marcas e rótulos de épocas. `axis.marks`: `[{yr, label}]`, linha forte com rótulo (hoje o marco zero, ano 0).
- `edgeTypes`: `mestre`, `influencia`, `critica`, `debatido`, `reivindicada`, `identificacao`. Cada um tem `label`, `dash`, `css` (nome da variável de cor) e, opcionalmente, `directed: false`. Um tipo novo exige também a variável CSS em `index.html`.
- `domains[]`: `id`, `name`, `status` (`ativo` ou `planejado`), `file`, `desc`.

`data/<tema>.json`
- `lanes[]`: `{id, name, color}`. `id` com prefixo do tema (`astro.tecnica`, `myth.grega`). `color` é 1–8.
- `nodes[]`: `{id, name, date, yr, lane, dy, work, why}`. `yr` é o ano usado na posição; `date` é o texto exibido (curto: ele é centrado no ponto). `dy`: `-1` rótulo acima, `-2` mais alto, `1` abaixo, `2` mais baixo (o validador avisa colisões). `why`: uma ou duas frases verificáveis.
- `notes[]` (opcional): `{title, text}`, exibidos quando o tema está ligado.

`data/relacoes.json`: `edges[]` com `{from, to, type, desc}`. A seta vai de quem age ao alvo. `identificacao` não tem direção nem seta.

`data/trilhas.json`
- `trails[]`: `{id, name, intro, steps:[{node, read, hours}], default?}`. Trilha de leitura ordenada. Só **uma** é mostrada por vez, e só ela numera os círculos (1, 2, 3…). Isso resolve a numeração entre temas: números pertencem à trilha escolhida, não ao tema.
- `lineages[]`: `{id, name, nodes:[ids]}`. Conjunto destacado, sem numeração. Ids de trilha e de linhagem são independentes (uma trilha e uma linhagem podem ter o mesmo id).

## 6. Regras de rigor (não negociáveis)

- **Não afirme linhagem sem fonte.** Escolha o tipo com honestidade:
  - `influencia`/`mestre`: documentado em fonte antiga ou em bibliografia acadêmica.
  - `debatido`: estudiosos discordam (ex.: orfismo ↔ pitagorismo; Pitágoras ↔ Empédocles).
  - `reivindicada`: a própria tradição diz, mas não há documentação (ex.: "o tarot veio do Egito"; origens alegadas da Golden Dawn). **É isso que impede que história e mito se misturem.**
  - `identificacao`: duas figuras tomadas como a mesma por uma cultura (Hermes e Thoth). Diga quem identificou e quando.
- **Autoria e datas incertas:** diga na `date` ("c.", "séc.") e, se preciso, em `why`. Pseudepigrafia é dita como tal.
- **Verifique antes de acrescentar.** Use busca na web para datas e títulos. Na dúvida, não inclua ou marque `debatido`.
- **Não derive correspondências em causa.** O tom do mapa é histórico, não de validação do sistema simbólico.
- Texto em português do Brasil, sem travessão como pausa, sem adjetivação de efeito.

## 7. Temas planejados e candidatos (a verificar)

Nada abaixo está no mapa. Cada item exige fonte antes de entrar.

- **Tarot e cartomancia:** trionfi (Itália, séc. XV); Court de Gébelin (1781, origem egípcia reivindicada); Etteilla (1783); Éliphas Lévi; Golden Dawn (1888); Waite–Smith (1909); Crowley–Harris. Apoio crítico: Dummett; Decker e Dummett, *A History of the Occult Tarot*.
- **Hermetismo e magia cerimonial:** Agrippa, Dee, Lévi, Blavatsky, Golden Dawn, Crowley (A∴A∴, Thelema), *Kybalion* (1908). Ligar a `hermetica`, `thoth` e `casaubon`. O Egito entra por `thoth`; ampliar a faixa `myth.egipcia` (Osíris, Ísis, Hórus) quando Crowley entrar.
- **Alquimia:** hoje só Zósimo, Paracelso e gnose. Gerhard Dorn não foi verificado. Os arcontes ofitas (Orígenes, *Contra Celso* VI.31) estão resumidos em `gnose`; a correspondência Saturno ↔ Yaldabaoth não foi confirmada em fonte e não está no mapa.
- **Para `psicologia`:** Tarnas, Arroyo, Sasportas, Marc Edmund Jones, Alice Bailey, Carter, Hone, Huber, Assagioli, Shawn Carlson (teste duplo-cego, *Nature*, 1985, como nó crítico). A relação `alan-leo → rudhyar` não tem fonte conferida e não foi incluída.

Ao ativar um tema: criar `data/<tema>.json`, mudar `status` para `ativo` em `domains.json`, definir faixas e figuras; relações e trilhas vão para os arquivos globais.

## 8. Pegadinhas conhecidas

- O renderizador só desenha relações entre figuras visíveis. Se um tema está desligado, as relações cruzadas somem do desenho, mas continuam listadas no painel (clicar abre o tema).
- Escolher uma trilha ou linhagem em "Destacar" liga automaticamente os temas que ela cruza.
- Rótulos colidem quando duas figuras da mesma faixa estão a menos de ~84 px. Ajuste `dy`.
- Ao abrir, só o primeiro tema fica ligado e a trilha `default` vem selecionada.
- Navegação: arrastar move o mapa; Ctrl/⌘ + roda, ou os botões, dão zoom. O mínimo de zoom é o que mostra o mapa inteiro (cai sozinho conforme o mapa cresce) e o máximo é 250%.
- Tema visual: Gruvbox (escuro por padrão, claro pelo botão "Tema"; a escolha fica no navegador). Cores de faixa e de relação são variáveis CSS `--c1`…`--c8` e `--e-*` em `index.html`.
- Os dados são carregados por `fetch` relativo: abrir `index.html` por `file://` falha; use `python3 -m http.server`.
- Duas instâncias editando ao mesmo tempo: mescle o branch primeiro e rode `mapa.py validate` depois do merge.

## 9. Registro de mudanças (acrescente no fim, nunca apague)

- 2026-10-19 · v1 · Domínio `astrologia`: 37 nós, 46 relações, trilha mínima de 11 etapas (~73 h), 3 linhagens. Estrutura em JSON, validador, domínios planejados (tarot, magia, psicologia).
- 2026-10-19 · v2 · Domínio `psicologia` ativado: 6 nós (Alan Leo, Evangeline Adams, Rudhyar, Greene, Jung, Pauli), 6 relações (3 cruzam para a astrologia), 1 trilha, 2 linhagens. Domínio `alquimia` planejado. Fontes: Wikipedia (Psychological astrology, Alan Leo, Evangeline Adams, Liz Greene, Dane Rudhyar, Synchronicity, Alchemical Studies); Psicologia e Alquimia (1944), Mysterium (1955–56) e ensaio de Pauli sobre Kepler (1952) vêm de conhecimento geral, conferir se for citar no canal.
- 2026-10-19 · v3 · Relação `rudhyar → greene` (influencia) acrescentada, fonte: Robert Hand, prefácio de *Saturn: A New Look at an Old Devil* (Weiser, 2011), p. 5–6. Total: 43 nós, 53 relações.
- 2026-10-19 · v4 · Refatoração para mapa geral. Relações e trilhas saem dos arquivos de tema (`relacoes.json`, `trilhas.json`); CLI `tools/mapa.py`; tipo `identificacao`; eixo começa em 2500 a.C.; numeração só da trilha selecionada; busca e seletor de destaque na página. Temas novos: `mitologia` (Homero, Hermes, Thoth) e `alquimia` (gnose antiga, Zósimo, Paracelso). Acrescentados Empédocles e Stanton Marlan (*The Black Sun*, 2008). Total: 51 nós, 69 relações, 3 trilhas, 8 linhagens. Fontes a conferir antes de citar no canal: ensaio de Jung sobre Zósimo (Eranos 1937), ensaios sobre Paracelso (1929, 1941), *Septem Sermones* (1916), Heródoto sobre Hermes/Thoth, Platão e a palavra "elemento" no *Timeu*.
- 2026-10-20 · v5 · Trilhas renomeadas por tema; marco zero no eixo (`axis.marks`); `egito-templos` (Egito → Pitágoras e Babilônia → Pitágoras como `reivindicada`; fontes: Porfírio VP 6, Jâmblico, Heródoto II.123, Burkert); `dionisio` e `persefone` (Apolodoro, Biblioteca 3.5.3; Diodoro IV.4 e V.75.4; Hinos Órficos; Hino Homérico a Deméter) e linhagem "Descida ao Hades e retorno". CLAUDE.md na raiz do repositório. Total: 54 nós, 74 relações. Jesus, evangelhos e Nag Hammadi aguardam decisão de escopo e de título.
- 2026-10-20 · v6 · Título "A Cadeia de Ouro" e critério de entrada (seção 1). Tema `cristianismo` com Paulo de Tarso (stoicheia e arcontes; ligado a `gnose` e a `agostinho`; Pagels 1975). Faixa `myth.relatos` com Heródoto (II.81, relação `debatido` com Pitágoras; problema textual nos manuscritos). **Correção:** a relação Hermes–Thoth dizia que Heródoto foi o primeiro a identificá-los e que Platão os via como distintos; nenhuma das duas afirmações foi confirmada. Agora cita a identificação ptolemaica (interpretatio graeca) e Cícero, De Natura Deorum III.56. CLI: `add-domain`, `add-lane`, `set-title`. Total: 56 nós, 77 relações. Da memória, a confirmar antes de citar: Romanos 13:13 na conversão de Agostinho (Confissões VIII.12); 1 Coríntios 2:6–8; Heródoto II.123.
- 2026-10-20 · v7 · Onda cristã e gnóstica. Nó genérico `gnose` removido e substituído por `basilides`, `valentim`, `sethianos`, `heracleao`, `ofitas`, `mani`, `apocrifo-joao` e `nag-hammadi` (tema alquimia/gnose); tema cristianismo: `jesus`, `joao-apostolo`, `marcos`, `mateus`, `lucas`, `evangelho-joao`, `ireneu`, `origenes` (além de `paulo`). Autoria dos evangelhos tratada como atribuição da tradição: os textos são anônimos, e o Evangelho de João não nomeia o filho de Zebedeu (só o Apócrifo de João o faz; relações `reivindicada`). **Removido por não confirmado:** a afirmação de que Ireneu liga os arcontes ofitas aos sete planetas, e qualquer identificação Yaldabaoth–Saturno em Orígenes (nada disso aparece nas fontes consultadas). Fontes: Wikipedia (Gospel, Gospel of John, John the Apostle, Irenaeus, Heracleon, Valentinus, Basilides, Papias, Ophites, Sethianism, Apocryphon of John, Nag Hammadi library, Manichaeism); Porfírio, Vida de Plotino 16, via hypotyposeis.org; Pagels, The Gnostic Paul (Fortress, 1975). Da memória, a conferir: João 21:2 (única menção a "filhos de Zebedeu" no evangelho), datas de Jesus, Gálatas 1:11–12. Candidatos ainda fora: Egípcia Eneáda e Ogdóada de Hermópolis (ligação com o Oitavo e Nono hermético não achada em fonte), Minotauro e labirinto (Plutarco, Teseu; Kerényi, Labyrinth-Studien, 1941; Jung e Kerényi, 1941), Evangelho de Tomé, Plutarco (De Iside), Arato.
- 2026-10-20 · v8 · Tema Gruvbox (escuro e claro), arrastar e zoom com limites que acompanham o tamanho do mapa, subtítulo com a palavra "genealogia", notas de leitura da astrologia removidas.
