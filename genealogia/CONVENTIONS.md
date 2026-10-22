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
- `edgeTypes`: `mestre`, `influencia`, `critica`, `debatido`, `reivindicada`, `identificacao`, `registro`, `escola`. Cada um tem `label` (legenda), `out` (rótulo no painel quando a figura é a origem), `in` (rótulo quando é o alvo), `dash`, `css` (nome da variável de cor) e, opcionalmente, `directed: false`. Crie ou altere por `mapa.py set-edgetype`. Um tipo novo exige também a variável CSS em `index.html` (claro e escuro). O painel agrupa as relações por tipo e direção, um bloco por rótulo, e só mostra os não vazios.
- `domains[]`: `id`, `name`, `status` (`ativo` ou `planejado`), `file`, `desc`.

`data/<tema>.json`
- `lanes[]`: `{id, name, color}`. `id` com prefixo do tema (`astro.tecnica`, `myth.grega`). `color` é 1–8.
- `nodes[]`: `{id, name, date, yr, lane, dy, dx?, work, why}`. `dx` (opcional, inteiro em px) desloca só o desenho, nunca o ano: use para figuras de mesma data na mesma faixa (`add-node --id X --dx -18`; `--dx 0` remove). Figura cujo `yr` coincide com uma marca de `axis.marks` (hoje Jesus, ano 0) ganha halo e nome em destaque, sem configuração. `yr` é o ano usado na posição; `date` é o texto exibido (curto: ele é centrado no ponto). `dy`: `-1` rótulo acima, `-2` mais alto, `1` abaixo, `2` mais baixo (o validador avisa colisões). `why`: uma ou duas frases verificáveis.
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
  - `mestre`: só ensino direto documentado, de pessoa a pessoa (Sócrates→Platão, Plotino→Porfírio, Jesus→João). Rótulos: "Mestre de" / "Discípulo de".
  - `escola`: seguidores de uma tradição, sem ensino direto documentado (Platão→Plotino, Pitágoras→Nicômaco). Rótulos: "Escola seguida por" / "Segue a escola de". Não use `mestre` para isso.
  - `registro`: a figura ou o ensino é preservado ou relatado num texto (Jesus→evangelhos, Nag Hammadi). Rótulos: "Preservado ou relatado em" / "Preserva ou relata". Autoria do texto é outra coisa (`reivindicada`).
  - `identificacao`: duas figuras tomadas como a mesma por uma cultura (Hermes e Thoth). Diga quem identificou e quando.
- **Autoria e datas incertas:** diga na `date` ("c.", "séc.") e, se preciso, em `why`. Pseudepigrafia é dita como tal.
- **Wikipedia não é fonte.** Nunca cite Wikipedia (nem enciclopédia online parecida) em `why`, `desc` ou no registro. Fontes aceitas: livros, artigos científicos, edições acadêmicas e fontes primárias. O Victor tem muitos livros e pode enviar o que for preciso. Dado que veio de fonte não aceita leva o aviso `[FONTE A SUBSTITUIR]` até ser conferido.
- **Verifique antes de acrescentar.** Use busca na web para datas e títulos. Na dúvida, não inclua ou marque `debatido`.
- **Não derive correspondências em causa.** O tom do mapa é histórico, não de validação do sistema simbólico.
- Texto em português do Brasil, sem travessão como pausa, sem adjetivação de efeito.

## 7. Temas planejados e candidatos (a verificar)

Nada abaixo está no mapa. Cada item exige fonte antes de entrar.

- **Tarot e cartomancia:** trionfi (Itália, séc. XV); Court de Gébelin (1781, origem egípcia reivindicada); Etteilla (1783); Éliphas Lévi; Waite–Smith (1909); Crowley–Harris. Apoio crítico: Dummett; Decker e Dummett, *A History of the Occult Tarot*.
- **Hermetismo e magia cerimonial:** tema `magia` ativo desde a v13 (Tábua de Esmeralda, Caibalion, Agrippa, Golden Dawn). Faltam Dee, Lévi, Blavatsky, Crowley (A∴A∴, Thelema) e o *Sefer Yetzirah* (datação discutida, do séc. II a.C. ao IX; sem elo documentado com figuras do mapa, por isso ficou de fora). Ligar a `hermetica`, `thoth` e `casaubon`. O Egito entra por `thoth`; ampliar a faixa `myth.egipcia` (Osíris, Ísis, Hórus) quando Crowley entrar.
- **Alquimia:** hoje só Zósimo, Paracelso e gnose. Gerhard Dorn não foi verificado. Os arcontes ofitas (Orígenes, *Contra Celso* VI.31) estão resumidos em `gnose`; a correspondência Saturno ↔ Yaldabaoth não foi confirmada em fonte e não está no mapa.
- **Para `psicologia`:** Arroyo, Sasportas, Marc Edmund Jones, Alice Bailey, Carter, Hone, Huber, Assagioli (Tarnas e Carlson entraram na v13). A relação `alan-leo → rudhyar` não tem fonte conferida e não foi incluída.

Ao ativar um tema: criar `data/<tema>.json`, mudar `status` para `ativo` em `domains.json`, definir faixas e figuras; relações e trilhas vão para os arquivos globais.

## 8. Pegadinhas conhecidas

- O renderizador só desenha relações entre figuras visíveis. Se um tema está desligado, as relações cruzadas somem do desenho, mas continuam listadas no painel (clicar abre o tema).
- Escolher uma trilha ou linhagem em "Destacar" liga automaticamente os temas que ela cruza.
- Rótulos colidem quando duas figuras da mesma faixa estão a menos de ~84 px. Ajuste `dy`.
- Ao abrir, só o primeiro tema fica ligado e a trilha `default` vem selecionada.
- Navegação: arrastar move o mapa; Ctrl/⌘ + roda, ou os botões, dão zoom. O mínimo de zoom é o que mostra o mapa inteiro (cai sozinho conforme o mapa cresce) e o máximo é 250%.
- Seleção: ao abrir, nada vem selecionado. Passar o mouse (ou focar com Tab) traz o nome da figura para a frente, com fundo opaco, e destaca suas relações. Clicar seleciona: o nome fica em destaque e o hover nas vizinhas é ignorado até limpar a seleção, clicando numa área vazia do mapa ou com Esc.
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
- 2026-10-20 · v9 · Hover traz o nome para a frente (camada superior com fundo); seleção persistente sem hover nas vizinhas; limpar com clique em área vazia ou Esc; ao abrir nada vem selecionado.
- 2026-10-20 · v10 · Painel agrupado por tipo e direção, com rótulos por tipo em `domains.json` (substitui "Vem de" e "Leva a ou atinge", que sugeriam filiação). Novos tipos `registro` (jesus→4 evangelhos, apocrifo-joao, hermetica e valentim→nag-hammadi) e `escola` (platao→plotino, pitagoras→nicomaco). Comando `set-edgetype` na CLI. Notas do Obsidian seguem o mesmo agrupamento. Sem nó "Escola pitagórica" por ora: `pitagoras→filolau` fica `debatido`.
- 2026-10-20 · v11 · Campo `dx` (deslocamento visual) para separar os quatro evangelhos (c. 70–100) sem mexer no ano; Jesus destacado por coincidir com o marco zero (halo e nome em negrito); Jesus `dy -2`, João `dy 1`.
- 2026-10-21 · v12 · Cadeia de transmissão da imagem dos "ombros de gigantes" (Escola de Chartres). Nós: `bernardo-chartres`, `guilherme-conches`, `joao-salisbury` (faixa `astro.filos`) e `newton` (faixa `astro.critica`). Relações: bernardo→guilherme e guilherme→joão (`mestre`), bernardo→joão (`registro`, Metalogicon 1159), platão→guilherme (Glosae super Platonem), boécio→guilherme (Glosae super Boetium), kepler→newton (`influencia`). Linhagem `ombros-gigantes` só com os três de Chartres: não há transmissão documentada até Newton. Fontes: Wikipedia (Standing on the shoulders of giants, William of Conches, John of Salisbury, Bernard of Chartres, Isaac Newton's occult studies), Newton Project (venda da Sotheby's, 1936) e Physics World (acervo de ≈8 milhões de palavras). A conferir antes de citar no canal: livro e capítulo do Metalogicon; Kepler→Newton nos Principia, da memória. Total: 75 nós, 106 relações, 13 linhagens.
- 2026-10-21 · v13 · Linhagens do V1 e tema `magia`. Nós novos: `brahe`, `galileu`, `carlson`, `bank-scafetta`, `fludd` (astrologia); `tarnas` (psicologia); `tabua-esmeralda`, `caibalion`, `agrippa`, `golden-dawn` (tema `magia`, ativado nesta versão; faixas `mag.textos` e `mag.magos`). Relações novas com fonte (Wikipedia: Emerald Tablet, The Kybalion, Shawn Carlson, Robert Fludd, Tycho Brahe, Galileo Galilei, Agrippa, Hermetic Order of the Golden Dawn, Hermetic Qabalah, Hermetica, Cosmos and Psyche, Harmonice Mundi, Nicomachus; arXiv 2202.03939): `brahe→kepler`, `galileu→kepler` (marés, crítica), `kepler→fludd` (crítica), `hermetica→fludd`, `platao→hermetica` (platonismo médio e estoicismo), `ficino→agrippa`, `pico→agrippa`, `pico→golden-dawn` (elo de tradição, cabala cristã), `hermetica→tabua-esmeralda` e `hermetica→caibalion` (ambas `reivindicada`), `pitagoras→bank-scafetta`, `jung→tarnas`, `carlson→alan-leo` (de tema, não de citação, dito na descrição). **Correção:** `pitagoras→kepler` dizia que Kepler assume a herança pitagórica; agora diz que retoma a ideia e abandona a afinação pitagórica e a numerologia. `boecio` não diz mais que organiza a música das esferas "até Kepler". `nicomaco` registra a lenda dos martelos (registro mais antigo que sobrevive). Linhagens: `orfica` termina em Boécio (Boécio→Macróbio e Macróbio→Kepler não têm aresta documentada; Macróbio sai); `junguiana` agora é Platão, Hermética, Fludd, Kepler, Pauli, Jung, Rudhyar, Greene, Tarnas (sem os dois elos sem fonte); novas `v1-corda-ao-ceu` e `v1-axioma`. CLI: `add-domain` passa a ativar um tema planejado (cria o arquivo de dados). Da memória, a conferir: Kepler comenta a *Harmônica* de Ptolomeu, capítulo da lenda em Nicômaco, reanálises do teste de Carlson. Total: 85 nós, 119 relações, 15 linhagens.
- 2026-10-21 · v14 · Correção de método: o Victor proibiu a Wikipedia como fonte. As 24 citações que a usavam (nós brahe, galileu, carlson, fludd, nicomaco, agrippa, golden-dawn, tabua-esmeralda, caibalion, tarnas; relações dos mesmos e de Chartres) trocam a referência por `[FONTE A SUBSTITUIR]`. Linhagem `orfica` restaurada com Macróbio e Kepler (as alterações do mapa só incluem, não excluem). `pitagoras→kepler` volta ao texto anterior com `[A CONFERIR no Harmonices Mundi]`; `boecio` idem. As fontes dos registros v2 e v7 acima também citam Wikipedia e entram na mesma revisão.
- 2026-10-21 · v15 · Fontes primárias e acadêmicas entram no lugar das provisórias. Conferidos nos livros e artigos enviados pelo Victor: Kepler, *Harmonices Mundi* livro V (trad. Wallis, 1939); Burkert, *Lore and Science in Ancient Pythagoreanism* (1972); Copenhaver, *Hermetica* (1992); Carlson, *Nature* 318 (1985); texto do *Caibalion* (Gutenberg, ed. 1912). Nós reescritos: `carlson`, `nicomaco`, `tabua-esmeralda`, `caibalion`, `brahe`, `kepler`, `boecio`. Relações novas: `cicero→kepler` (Sonho de Cipião citado duas vezes), `brahe→kepler`, `hermetica→abumashar`, e quatro `registro` da lenda dos martelos (`pitagoras→nicomaco`, `→jamblico`, `→macrobio`, `→boecio`; Burkert, nota 28), que ligam Macróbio à linhagem pitagórica por documento. Relações corrigidas: `ptolomeu→kepler` (Kepler leu a *Harmônica* em manuscrito de Herwart; Proêmio), `proclo→kepler` (o hino ao Sol, não o comentário a Euclides, que fica a conferir), `pitagoras→kepler` (o grau de adesão à afinação e numerologia pitagóricas depende do livro III, ausente do PDF). `platao→hermetica` passa de `influencia` a `debatido` (Copenhaver relata a disputa entre Reitzenstein, Zielinski, J. Kroll e Bousset). Ainda `[FONTE A SUBSTITUIR]`: galileu, fludd, agrippa, golden-dawn, tarnas, chartres, horóscopos de Brahe e a autoria do *Caibalion*. Total: 85 nós, 125 relações, 15 linhagens.
- 2026-10-21 · v16 · Kepler no latim (escaneamento de 1619 do Internet Archive, lido no texto e na imagem das páginas; traduções provisórias minhas) e Franco (1991, lido por OCR). Resolvidos os `[A CONFERIR]`: `pitagoras→kepler` (livro III: rejeita os 'números abstratos' pitagóricos como causa das consonâncias; dedicatória: obra 'que cheira a Pitágoras e a Platão'), `ptolomeu→kepler` (comparação dos aspectos com as consonâncias 'transmitida por Ptolomeu, explicada por Cardano'; crítica no livro III e no Apêndice), `proclo→kepler` (comentário a Euclides: prefácio do livro I e epígrafe do livro IV), `kepler→fludd` (Apêndice, p. 251 a 254). Nó novo: `cardano` (identificação a conferir). Relações novas: `macrobio→kepler` (Kepler completa com Macróbio o texto que falta no cap. XVI da *Harmônica* III), `hermetica→kepler` (livro III, p. 7: 'ou Pitágoras hermetizou, ou Hermes pitagorizou', opinião de Kepler, não documento), `pico→kepler`, `kepler→pico`, `ptolomeu→cardano`, `cardano→kepler`; `cicero→kepler` ganha a menção do livro IV. `hermetica→fludd` reescrita com o 'axioma de Hermes' citado por Kepler. `fludd` passa a `yr` 1617 (tomo visto por Kepler); `tabua-esmeralda` ganha a nota do 'axioma de Hermes' em 1619. Linhagem `v1-axioma` inclui `fludd` e `kepler` (o contraponto de 1619). **Correção:** a frase 'Copenhaver: Kepler o acusou de teósofo, e acertou' (nó `fludd`) não foi achada no Copenhaver nem no Apêndice e foi removida. Ainda `[FONTE A SUBSTITUIR]`: galileu, agrippa, golden-dawn, tarnas, chartres, horóscopos de Brahe, autoria do *Caibalion*, e em `fludd` datas de vida e obras de 1621 e 1622. Não lidos: *Tertius Interveniens* e a digressão sobre Bodin no fim do livro III. Total: 86 nós, 131 relações, 15 linhagens.
- 2026-10-22 · v17 · Aiton, Duncan e Field (1997) conferem as passagens de Kepler (páginas dessa edição nos textos); Negus (1997, teses 64 a 69 do Tertius Interveniens, tradução abreviada) e digressão de Kepler sobre Bodin (Aiton pp. 255 a 278). Fludd sem pendências (datas, obras, polêmica de 1621 e 1622 por Aiton); Cardano identificado (Girolamo, 1501-1576; comentário à Tetrabiblos, Basileia, 1554); Pico com divergência de data (1495 em Aiton, 1496 no nó) marcada; `hermetica→kepler` com as notas 28 e 29 de Aiton; `kepler` com o epílogo sublunar e a polêmica Roslin-Feselius. Total: 86 nós, 131 relações, 15 linhagens (sem nós novos).
