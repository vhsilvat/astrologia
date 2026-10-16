# MISTAGOGOS · Vídeo 01 — Planejamento Mestre de Produção

**«A Arquitetura Oculta da Realidade — Astrologia, Harmonia Pitagórica e a Música das Esferas»**

Plano v1 · fonte de conteúdo: o roteiro de 5 seções (a fonte da verdade) · estruturação por blocos conforme `canal/video01.md` · identidade Gruvbox estrita + EB Garamond exclusiva · 1080p60.

---

## 1 · Decisões-âncora

| Item | Decisão |
|---|---|
| Formato | 16:9 · 1920×1080 · 60 fps · h264 + AAC |
| Duração alvo | **10:30 (±15 s)** — dentro da faixa 8–12 min do nicho educativo/filosófico |
| Narração | ~1.540 palavras · ritmo erudito ~145–150 ppm · gravada por ato (6 takes) e sobreposta na montagem |
| Música/SFX | Diegéticos via `Scene.add_sound` (WAVs sintetizados próprios) · sem trilha externa |
| Montagem | Peças renderizadas em `-qh` → concat/xfade no ffmpeg → narração → mix com loudnorm −14 LUFS |
| Método | Uma peça por vez, lapidação no percorrer (`-ql` + checagem pixel PIL) · transições como transformações contínuas — nunca corte seco dentro de um ato |
| Folga | Cada peça entra com ~10% de headroom sobre a narração; trim fino na edição, não no render |
| Identidade | Referências (Fludd, Rafael, Hermes) recriadas em vetorial — nunca coladas |

---

## 2 · Mapa de peças (11 renders · 630 s = 10:30)

| Peça | Arquivo | Ato | Janela | Duração | Status |
|---|---|---|---|---|---|
| c01 | `v01_c01_abertura.py` | 0 · Cold open | 0:00–0:35 | 35 s | ✅ novo · validado — anel zodiacal estático (12 ticks, 0° realçado), Saturno/Netuno convergem exatamente no tick, ting + onda, MISTAGOGOS, zoom final |
| c02 | `v01_c02_retorno_saturno.py` | 1 · O mapa do jogo | 0:35–2:30 | 115 s | ✅ novo · validado — roda zodiacal com abreviações, Saturno orbita + contador 1994→2023,5, Circumscribe no retorno, Netuno converge, zoom final |
| c03 | `v01_c03_logos_hermes.py` | 2 · Axiomas & Hermética | 2:30–4:45 | 135 s | ✅ novo · validado (111,6 s) — etimologia ASTRO/LOGIA, AXIOMA, Hermes atravessa vigília/inconsciente, caduceu (duas senoides entrelaçadas, crossings visíveis), Caronte/Morfeu, Correspondência (espiral↔átomo), Polaridade (círculo luz/sombra), saída: caduceu vira martelo |
| c04 | `martelos_monocordio.py` (substitui `da_forja_ao_diapasao.py`) | 3 · Pitágoras i | 4:45–6:15 | 90 s | ✅ novo · validado — forja → transformação fluida martelos→corda → monocórdio Fludd (modos 1-4, oitava·quinta·quarta como razões entre modos sucessivos) |
| c06 | `v01_c06_consonancias.py` | 3 · Pitágoras ii | 6:15–7:10 | 55 s | ✅ novo · validado — três cordas simultâneas: fundamental (aresta, 220Hz) · quinta (8/12, 330Hz) · quarta (9/12, 293Hz, nasce nova — a da quinta permanece intacta); cada uma com nota+frequência ao lado da própria ponta; legenda de fração/intervalo abaixo de tudo; Epogdoon em MathTex; régua de oitavas Mercúrio→Urano · Marte→Plutão |
| c07 | `v01_c07_peixe_agua.py` | 3 · Pitágoras iii | 7:10–7:30 | 20 s | ✅ novo · validado — onda ambiente nunca zero, peixe nadando, texto troca (Transform), pontos condensam em linha (âncora c08) |
| c08 | `v01_c08_tetraktys.py` | 4 · Validação i | 7:30–8:15 | 45 s | ✅ novo · validado — triângulo de 10 pontos (LaggedStart + harmônicos), 1+2+3+4=10, razões 2:1·3:2·4:3·9:8, 9:8 vira elipse |
| c09 | `v01_c09_kepler.py` | 4 · Validação ii | 8:15–8:45 | 30 s | ✅ novo · validado — planeta acelera no periélio (razão 1:1→2:1 na régua lateral), zoom-out final |
| c10 | `v01_c10_scafetta.py` | 4 · Validação iii | 8:45–9:15 | 30 s | ✅ novo · validado — diagrama espelhado em torno do cinturão de asteroides, arcos convergindo a ≈9/8, arcos endurecem em dentes de engrenagem (âncora para c11) |
| c11 | `v01_c11_relogio.py` | 5 · O relógio de Deus | 9:15–10:15 | 60 s | ✅ novo · validado — sete esferas (legenda lateral), fantasmas além de Saturno, anéis viram engrenagens de dentes trapezoidais engrenadas, compasso 0° Áries, cubo isométrico teaser |
| c12 | `v01_c12_endcard.py` | 5 · End card | 10:15–10:30 | 15 s | ✅ novo · validado — MISTAGOGOS + cubo isométrico orbitando o logotipo, teaser do próximo vídeo |

Novos scripts em `output/` com prefixo `v01_` · sons novos em `output/sons/`.

---

## 3 · Roteiro de narração final (com cues de animação)

Como ler: `[cXX · beat]` = o que está na tela no momento da fala · takes gravados por ato · pausas deliberadas onde a animação fala por si.

### ATO 0 · Cold open — c01 (0:00–0:35 · ~85 palavras)

Se você consome conteúdo na internet, certamente já viu pipocar vídeos sobre a conjunção de Saturno e Netuno no grau zero de Áries. A narrativa comum diz: «Saturno é o carma, o construtor; Netuno, os sonhos e a dissolução.» Mas como isso se aplica à vida prática? O que é, de fato, a astrologia?

[c01 · anel zodiacal; os dois pontos convergem ao zero]

A resposta curta: é o mapa de um jogo. E todo jogo tem regras. Este jogo também tem. Essas regras têm um nome — axiomas — e têm uma origem.

[c01 · MISTAGOGOS surge]

Bem-vindo aos Mistagogos.

### ATO 1 · O mapa do jogo — c02 (0:35–2:30 · ~280)

Em termos operacionais, a astrologia é o mapa de um jogo. Vivemos inseridos em uma simulação interativa com regras precisas. Para quem cresceu nos anos 1990 e 2000 jogando os primeiros MMORPGs da Level Up Games, explorando o universo de Skyrim, ou encarando a brutalidade técnica dos jogos da FromSoftware, a mecânica é familiar: cada desafio anterior funcionou quase como um tutorial para o verdadeiro jogo — a realidade.

[c02 · a roda do jogo; Saturno orbita com o contador de anos]

É sintomático que o software clássico usado por astrólogos tradicionais — o Astrolog, criado entre 1991 e 1996 por Walter D. Pullen, um programador abertamente fascinado por labirintos — espelhe essa lógica: um sistema de regras legível, em que cada corpo celeste é uma peça de comportamento determinístico.

[c02 · a órbita fecha no ponto natal]

E há uma coincidência cirúrgica. Para a geração nascida em meados da década de 1990, o primeiro Retorno de Saturno — aos 29,5 anos — coincide com o ingresso e a conjunção de Saturno e Netuno no marco zero zodiacal, Áries.

[c02 · Netuno cruza; os dois pontos se tocam no zero]

Onde o zodíaco recomeça, a vida também recomeça: um ponto de reinicialização cíclica de fase. Mas, para decodificar esse jogo, precisamos recorrer às suas regras basilares: os axiomas.

### ATO 2 · Axiomas, logos e a tradição hermética — c03 (2:30–4:45 · ~330)

Um axioma — do grego áxios, «digno», «válido» — é um princípio fundamental aceito como ponto de partida, dispensado de comprovação direta: a fundação sobre a qual teoremas e cosmologias são erguidos.

[c03 · ASTROLOGIA se decompõe]

A própria palavra astrologia carrega uma pista etimológica frequentemente ignorada. Astro, de ástron: corpo celeste. Logia, de lógos — e aqui lógos não se limita a «estudo» ou «fala»: na filosofia clássica grega, lógos significa primordialmente razão, proporção matemática, medida inteligível. Astrologia, em sua raiz, é a proporção matemática dos astros.

[c03 · Thoth → Hermes Trismegisto]

Esses princípios universais convergem historicamente na figura arquetípica de Thoth, no Antigo Egito: a mente ordenadora, patrono da escrita, da geometria e da mediação entre mundos. Com a expansão de Alexandre, o Grande, o período helenístico sincretizou Thoth com o Hermes grego e o Mercúrio romano, dando origem a Hermes Trismegisto — «o três vezes grande».

[c03 · o psicopompo atravessa a fronteira]

Hermes é o psicopompo arquetípico — de psyche, «sopro vital, alma», e pompós, «guia, condutor»: aquele que transita livremente entre a vigília e o inconsciente, o plano material e o submundo. Outros arquétipos exercem essa função de fronteira: Saturno e Caronte, o barqueiro da travessia, guardião do tempo linear, do limite físico e da matéria; e Morfeu, a ponte entre o plano sutil e o cérebro biológico por meio dos sonhos — reverberado na cultura pop no Morpheus de Matrix, que desperta o buscador para a realidade fora do véu ilusório.

[c03 · Correspondência: galáxia ↔ átomo]

Toda a mecânica celeste e a física clássica derivam de dois princípios herméticos estruturais. Primeiro, o Princípio da Correspondência: «o que está em cima é como o que está embaixo; o que está dentro é como o que está fora». Não há cisão entre psique interior e cosmos exterior; o cérebro atua apenas como um filtro sensorial — o conceito hindu de Maya, a ilusão de separação.

[c03 · Polaridade: o círculo gira claro↔escuro]

Segundo, o Princípio da Polaridade: «tudo é duplo; tudo tem polos; o igual e o desigual são a mesma coisa». Polos opostos diferem apenas em grau ou vibração — calor e frio, luz e escuridão, carga positiva e negativa.

[c03 · o caduceu desliza ao centro]

E se o logos é proporção, quem primeiro o ouviu vibrar na matéria?

### ATO 3 · Pitágoras e a física da harmonia — c04 + c06 + c07 (4:45–7:30 · ~400)

Grande parte da matemática e da filosofia grega bebeu diretamente do Egito. Pitágoras — c. 570 a c. 495 antes de Cristo — passou décadas em centros de mistério egípcios e babilônicos, fato atestado por autores como Porfírio e Clemente de Alexandria, absorvendo tanto a geometria sagrada quanto a doutrina da metempsicose: metá, «além, mudança»; em-psyche, a transmigração da alma.

[c04 · a forja: martelos 12 lb e 6 lb]

O relato clássico, registrado pelo neopitagórico Nicômaco de Gerasa no Enchiridion Harmonices, descreve a epifania de Pitágoras ao passar por uma forja: martelos com massas proporcionais — doze e seis unidades — batiam na bigorna emitindo sons consonantes, o intervalo exato da oitava justa: a proporção dois para um.

[c04 · martelos viram pinos; a bigorna vira a aresta]

Ao transpor o experimento para o monocórdio, Pitágoras determinou as razões matemáticas inteiras dos intervalos musicais fundamentais: dois para um, o Diapasão, a oitava justa; três para dois, o Diapente, a quinta perfeita; quatro para três, o Diatessaron, a quarta perfeita; e nove para oito, o Epogdoon, o tom inteiro pitagórico — a diferença exata entre a quinta e a quarta: três sobre dois, dividido por quatro sobre três, é nove sobre oito.

[c06 · a aresta desliza a 8/12 e a 9/12]

Repare no que esses intervalos têm a ver com a série que você acabou de ouvir: os saltos entre os harmônicos sucessivos da corda — o segundo sobre o primeiro, o terceiro sobre o segundo, o quarto sobre o terceiro — são precisamente a oitava, a quinta e a quarta. A série harmônica já contém, em si, as consonâncias de Pitágoras.

[c06 · oitavas planetárias: Mercúrio→Urano, Marte→Plutão]

Essa relação se estende à própria leitura astrológica: quando a tradição moderna diz que Plutão é a oitava superior de Marte, ou Urano a oitava superior de Mercúrio, estamos aplicando diretamente a transposição do intervalo harmônico de Pitágoras à psicologia das energias arquetípicas.

[c07 · o peixe na água]

Pitágoras concluiu que o Cosmos — do grego kósmos, «ordem, arranjo belo e governado» — não é silencioso nem caótico. Se corpos materiais em rotação e tensão vibram e geram som proporcional à sua massa e velocidade, as esferas planetárias em movimento contínuo emitem uma ressonância contínua: a Música das Esferas. Harmonia Mundi. Mas por que não a escutamos? Nascemos imersos nessa vibração desde o primeiro instante de vida. Assim como o peixe não percebe a água em que nada, por não ter um referencial externo de ar, o silêncio humano é, na verdade, a própria escuta contínua da harmonia fundamental do cosmos.

### ATO 4 · Da Escola de Atenas à física contemporânea — c08 + c09 + c10 (7:30–9:15 · ~255)

Na célebre Escola de Atenas, de Rafael Sanzio, enquanto Platão aponta para o alto — as Ideias — e Aristóteles projeta a mão para a terra — o empirismo —, Pitágoras surge no canto inferior esquerdo, transcrevendo numa lousa o diagrama do tetraktys e as relações harmônicas, incluindo o Epogdoon.

[c08 · a lousa: pontos 1·2·3·4]

Essa intuição antiga deixou de ser especulação mística com a física orbital. Em seu tratado Harmonices Mundi, de 1619, Johannes Kepler superou o modelo geocêntrico e as órbitas circulares ao demonstrar órbitas elípticas — provando que a velocidade angular aparente de cada planeta varia do afélio ao periélio em proporções que espelham, com precisão matemática, intervalos de escalas musicais.

[c09 · o planeta acelera no periélio]

E em 2023, o astrofísico Nicola Scafetta demonstrou que as órbitas planetárias estão arranjadas numa simetria espelhada em torno do Cinturão de Asteroides, entre Marte e Júpiter — e que as razões de ressonância entre pares de planetas vizinhos convergem para consonâncias harmônicas e para a fração pitagórica fundamental de nove sobre oito, o Epogdoon, com margem de erro inferior a um por cento e probabilidade estatística de aleatoriedade menor que 0,1 por cento.

[c10 · os pares convergem a 9/8]

### ATO 5 · O relógio de Deus — c11 + c12 (9:15–10:30 · ~185)

Saturno representava, tradicionalmente, a última esfera visível a olho nu: a fronteira intransponível do ego consciente e da matéria, antes do abismo do inconsciente transpessoal — que a astrologia moderna atribuiu a Urano, Netuno e Plutão.

[c11 · as esferas até Saturno; além, o abismo]

O cosmos opera como um relógio de precisão harmônica, cujas engrenagens matemáticas afetam as correntes sutis e os arquétipos da psique individual e coletiva. A conjunção no grau zero de Áries é a marcação de um novo compasso rítmico.

[c11 · anéis viram engrenagens; o compasso marca o zero]

No próximo passo, aprofundaremos como Platão e os sólidos platônicos se conectam aos quatro elementos de Empédocles — fogo, terra, ar e água —, demonstrando como a geometria sagrada funda os tipos psicológicos de Carl Jung e a decodificação analítica dos signos zodiacais.

[c11 · o cubo: 12 arestas · 6 faces · 8 vértices]

Doze arestas, seis faces, oito vértices: doze para seis — a mesma razão dois para um da forja, escondida na geometria.

[c12 · MISTAGOGOS]

A iniciação continua.

---

## 4 · Especificação cena a cena

### c01 · abertura (35 s)
- Fundo #282828 · anel zodiacal fino (Annulus #3c3833, 12 ticks #a89984) girando devagar; tick do topo realçado = 0° Áries.
- Saturno (dot #a89984 + anel fino) e Netuno (dot #8ec07c) convergem ao tick; ao se tocarem: um ting distante de bigorna (assinatura sonora da série) + onda expansiva discreta.
- FadeIn: MISTAGOGOS (96 pt #ebdbb2) + «a arquitetura oculta da realidade» (itálico #8ec07c, 34 pt).
- Som: drone_esferas (ganho 0,25) + martelo_agudo_440 (ganho 0,2).
- Saída: zoom no anel → c02.

### c02 · retorno de Saturno (115 s)
- Roda completa: 12 setores rotulados. ⚠ EB Garamond provavelmente não tem glifos zodiacais (♈ U+2648) — validar com Pango; fallback: abreviações Ár·To·Ge·Cn·Le·Vi·Li·Es·Sa·Cp·Aq·Pe.
- Saturno orbita (DashedCircle #a89984) com contador de anos 1994→2026 (ValueTracker + always_redraw); tic suave a cada volta.
- O retorno: órbita fecha no ponto natal → Circumscribe + «29,5 anos — o Retorno de Saturno».
- Netuno entra pela órbita externa (lenta) e cruza ao mesmo grau; os dois convergem ao zero → flash/onda (reuso do efeito dos golpes) → «reinicialização cíclica de fase».
- Posições simbólicas, não efemérides — o vídeo é arquetípico, não leitura de mapa.
- Saída: zoom no ponto zero.

### c03 · logos & Hermética (135 s)
- Etimologia: ASTROLOGIA divide-se (Transform) em «astro (ástron) · corpo celeste» / «logia (lógos) · razão · proporção · medida» (Brace duplo).
- «AXIOMA» (de áxios: digno, válido) + definição de uma linha.
- Hermes psicopompo: recriação vetorial de `roteiro/hermes-psicopompo.jpg` (perfil em linhas #ebdbb2 sobre silhueta #3c3833) atravessando uma faixa-fronteira tracejada («vigília» / «inconsciente»); caduceu = 2 ParametricFunction senoidais entrelaçadas + eixo + asas triangulares.
- Faixa inferior: Caronte (barca: arco + casco) e Morfeu (onda → perfil adormecido; caption rápida «Morpheus · Matrix»).
- Correspondência: eixo central espelhado — espiral galáctica (paramétrica) ↔ átomo (3 elipses orbitais) com ReplacementTransform um→outro; «como acima, embaixo» + «Maya».
- Polaridade: círculo metade luz (#ebdbb2) / metade sombra (#3c3833) girando 180° — polos trocam por rotação: «diferem apenas em grau».
- Saída: o caduceu desliza ao centro e Transform no martelo (âncora c03→c04).

### c04 · forja→diapasão (90 s)
- Base: `da_forja_ao_diapasao.py` com P1–P5 + M1 + M2 aplicados (ver §7).
- Estrutura interna inalterada: forja (12 lb / 6 lb · 12:6 = 2:1) → transição contínua (martelos→pinos · bigorna→aresta) → monocórdio 12/12 · 6/12 · 4/12 · 3/12 → modos 1→2→3→4 → «Harmonia Mundi».
- Frase-na-tela nova durante os modos (eco da narração): «os saltos sucessivos: 2:1 · 3:2 · 4:3» (FadeIn discreto sob a corda).
- Fim: corda e pinos permanecem em cena (M1) — âncora para c06.

### c06 · consonâncias (55 s)
- A MESMA corda de 12 unidades (pinos, coordenadas, paleta) — continuidade literal.
- Aresta desliza a 8/12 → dedilhada Mi₄ · 330 Hz → «8/12 · Diapente — a quinta 3:2».
- Aresta a 9/12 → Ré₄ · 293,3 Hz → «9/12 · Diatessaron — a quarta 4:3».
- MathTex central: `\frac{3}{2} \div \frac{4}{3} = \frac{9}{8}` + «Epogdoon — o tom inteiro» (Circumscribe no 9/8).
- Régua de oitavas: linha 110–220–440–880 com pares Mercúrio→Urano e Marte→Plutão (dots + setas #fabd2f) — «oitavas superiores».
- Sons: harpa_mi4_330 · harpa_re4_293 (+ harpa_si3_247 opcional).
- Saída: a última onda da régua ondula para fora da tela → vira a água de c07.

### c07 · peixe na água (20 s)
- Onda ambiente lenta atravessando a tela (always_redraw), amplitude decaindo até ~0,02 — imperceptível mas nunca zero: o próprio frame continua «escutando».
- Peixe vetorial mínimo (elipse + cauda #b8bb26) nadando contra a onda.
- Textos: «o peixe não percebe a água» → troca → «o silêncio é a escuta contínua».
- Som: drone_esferas + whoosh_agua (fundos, ganho baixo).
- Saída: os pontos da onda condensam → tetraktys.

### c08 · tetraktys (45 s)
- Painel-lousa (Rectangle #3c3833, stroke #a89984) + caption «Rafael · A Escola de Atenas — recriação do detalhe».
- Pontos 1·2·3·4 nascendo em LaggedStart, linha a linha, cores #b8bb26 · #fabd2f · #fe8019 · #8ec07c; cada linha com seu harmônico (220/440/660/880 — reuso dos WAVs).
- MathTex: `1+2+3+4 = 10` · abaixo, as razões fluindo `2:1 \cdot 3:2 \cdot 4:3 \cdot 9:8`.
- Saída: o 9:8 cresce e Transform na elipse.

### c09 · Kepler (30 s)
- Elipse (ParametricFunction #ebdbb2), Sol num foco (dot #fabd2f), planeta acelerando no periélio (parametrização não-uniforme — aproximação visual honesta; rótulos deixam claro).
- Rastro (segmentos de arco com fade) marcando a variação; régua lateral com a razão instantânea aproximando 2:1 · 3:2 · 4:3 («lento» no afélio, «rápido» no periélio).
- Caption: «Kepler · Harmonices Mundi (1619)».
- Saída: zoom-out — a elipse é uma entre outras.

### c10 · Scafetta (30 s)
- Diagrama espelhado: eixo central = Cinturão de Asteroides (dashes #a89984); pares internos (Mercúrio·Vênus / Vênus·Terra / Terra·Marte) à esquerda; externos (Júpiter·Saturno / Saturno·Urano / Urano·Netuno) à direita.
- Arcos de ressonância entre pares; razões (Text) estabilizando juntas → Circumscribe no «9/8» central (#fe8019).
- Caption: «Scafetta (2023) — erro < 1% · p(aleatório) < 0,1%». Fonte: `artigos/SCALING, MIRROR SYMMETRIES & CONSONANCES.pdf` — gráfico recriado em Gruvbox.
- Som: acorde_harmonico (ganho 0,4) na convergência.
- Saída: os arcos endurecem em dentes de engrenagem.

### c11 · o relógio de Deus (60 s)
- Esferas concêntricas (Annulus ×7, ordem caldaica: Lua · Mercúrio · Vênus · Sol · Marte · Júpiter · Saturno; #3c3833/#a89984, nomes #ebdbb2 22 pt); Saturno = borda sólida.
- Além: escuridão com Urano · Netuno · Plutão como traços fantasmas (dashed #7c6f64) — «o abismo transpessoal».
- Transform: anéis → engrenagens (polígonos dentados gerados por pontos; girando engrenadas com razões 2:1 entre vizinhos — a harmonia vira mecanismo).
- Compasso/ponteiro marca 0° Áries → «um novo compasso rítmico».
- Teaser: cubo isométrico vetorial girando devagar + «12 arestas · 6 faces · 8 vértices» + «12 : 6 = 2 : 1» (Circumscribe — eco do cartaz da forja).
- Som: tic_relogio + drone_esferas.
- Saída: cubo encolhe ao centro.

### c12 · end card (15 s)
- MISTAGOGOS (96 pt #ebdbb2) + «a iniciação continua» (itálico #8ec07c).
- Linha: «próximo — os sólidos platônicos · os quatro elementos · Jung».
- Cubo mini (âncora de c11) orbitando o logotipo; micro-vibração de fundo persistente.
- Som: acorde final + último tic.

---

## 5 · Âncoras de continuidade (transições)

| Fronteira | Âncora |
|---|---|
| c01→c02 | o anel zodiacal é o mesmo objeto; a câmera aproxima do ponto zero |
| c02→c03 | o ponto 0° Áries pulsa e vira o «ponto de partida» dos axiomas |
| c03→c04 | o caduceu de Hermes se transforma no martelo (o presente do psicopompo) |
| dentro de c04 | martelos→pinos · bigorna→aresta (já existe) |
| c04→c06 | a mesma corda de 12 unidades permanece (M1) |
| c06→c07 | a última onda da régua de frequências vira a água |
| c07→c08 | os pontos da onda condensam nos pontos do tetraktys |
| c08→c09 | o 9:8 cresce e vira a elipse (a razão vira geometria orbital) |
| c09→c10 | zoom-out: a elipse é uma entre as órbitas dos pares |
| c10→c11 | os arcos de ressonância endurecem em dentes de engrenagem |
| c11→c12 | o cubo persiste, miniaturizado, sobre o logotipo |

Fronteiras entre atos sem âncora: crossfade 0,4 s (`xfade` no ffmpeg).

---

## 6 · Biblioteca sonora

Existentes (10): martelo_grave_220 · martelo_agudo_440 · harpa_la_220 · harpa_la4_440 · harpa_mi5_660 · harpa_la5_880 · tom_fundamental_220 · tom_oitava_440 · tom_quinta_660 · acorde_harmonico.

Novos (6) — ✅ gerados via output/sintetiza_sons.py:
- `harpa_mi4_330.wav` — Karplus-Strong, 330 Hz (a quinta 3:2 sobre 220) — c06
- `harpa_re4_293.wav` — Karplus-Strong, 293,33 Hz (a quarta 4:3 sobre 220) — c06
- `harpa_si3_247.wav` — Karplus-Strong, 247,5 Hz (9:8 sobre 220, o tom inteiro — opcional) — c06
- `tic_relogio.wav` — click metálico grave (parciais ~150/300 Hz + ruído, decay ~80 ms) — c02/c11
- `drone_esferas.wav` — osciladores graves detunados (~55/55,5 Hz) + ruído filtrado, ~10 s, loopável, ganho baixo — c01/c07/c11
- `whoosh_agua.wav` — ruído filtrado com sweep de abertura (~3 s) — c06→c07/c07

Gerar com o mesmo script de síntese das harpas (método KS já validado).

---

## 7 · Auditoria — `da_forja_ao_diapasao.py` (revisão solicitada)

**Veredito: a aritmética das divisões está correta** — 12/12→220, 6/12→440, 4/12→660, 3/12→880 (comprimento vibrante 1/n → frequência n×220) e os rótulos batem. A «vacila» que você sentiu é real, mas mora noutros níveis:

- **P1 · Física (a principal):** a aresta já nasce mordendo a corda no «12/12 · corda inteira». `cav_static` fica em [0, Y_STR−0,20] e o ápice do triângulo (escala 0,24) ultrapassa a linha da corda em ~0,04 — durante a primeira dedilhada a corda inteira vibra através da aresta, que fisicamente forçaria um nó. Correção: nascer abaixo da corda (Y_STR−0,28) e subir à mordida via tracker de altura (mesmo padrão de tb/cavx), ou só entrar em cena na divisão.
- **P2 · Conceitual:** a peça mostra a série harmônica (1:1, 1:2, 1:3, 1:4), não as consonâncias pitagóricas do roteiro (2:1, 3:2, 4:3, 9:8). A quinta 3:2 exige comprimento 8/12 → 330 Hz (Mi₄); a quarta 4:3 exige 9/12 → 293,3 Hz (Ré₄) — nenhum dos dois aparece. Não é erro de conta: é lacuna narrativa. Resolvida pela nova c06 + pela frase nova na narração do Ato 3 (os saltos entre harmônicos sucessivos já são oitava · quinta · quarta).
- **P3 · Acústica:** o rótulo final «em conjunto → Lá · 880 Hz» é discutível — 220+440+660+880 é a pilha de parciais de Lá₃ (fundamental 220), ou seja, timbre de Lá₃, não Lá₅. Alternativa: «a oitava completa — o Diapasão», ou manter como licença estética. Decisão do autor.
- **P4 · Pop visual:** `FadeOut(cav_static)` + `self.add(cav)` sem transição — pisca no frame; fundir num único objeto (sempre o always_redraw, com tracker de opacidade) ou usar Transform.
- **P5 · Sobreposição:** `no_12` nasce exatamente sobre a aresta (ambos em xde(0,5)) — o dot vermelho cobre o triângulo; deslocar o dot (ex.: à esquerda da aresta, marcando o nó que ela cria) ou adiá-lo.
- **M1 · Âncora c04→c06:** o encerramento atual apaga a corda e os pinos — preservá-los até o fim (fade apenas nos textos) para que c06 continue literalmente a mesma corda.
- **M2 · Fôlego:** esticar os waits para ~90 s (a peça-base tem 39,4 s) sem alterar os tempos relativos dos golpes e dedilhadas.

`monocordio_harpa.py`: a aritmética também está correta; a sobreposição análoga a P5 (nó sobre o cavalete) existe e é benigna.

---

## 8 · Pipeline de produção & verificação

1. Ambiente: checar fontes (`fc-list | grep -i EB Garamond`) e venv antes de cada sessão; sons sempre via `Path(__file__).resolve().parent / "sons"`.
2. Por peça: escrever → `manim render -ql` → checagem pixel PIL por fases (método atual) → lapidar até verde → `-qh` (1080p60) → `ffprobe` (h264 · 1920×1080 · 60 fps · AAC · duração) → marcar OK no mapa (§2).
3. Cache: updaters/always_redraw invalidam partial movies — iterar sempre no `-ql`; `--disable_caching` só para depurar.
4. Regras GL herdadas (se 3D): FadeIn em tudo (Write/Create segfaultam no GL de software); `self.add` explícito para always_redraw; câmera via euler_angles.
5. Montagem: concat com codecs idênticos ou re-encode único; `xfade` 0,4 s só nas fronteiras sem âncora (§5); narração em 6 takes → mix (`amix`) → `loudnorm` −14 LUFS.
6. Verificação final: ffprobe completo + PIL spot-check nos frames das costuras + duração 10:30 ± 15 s + audição completa.

---

## 9 · Ordem de produção (proposta)

1. Correções P1–P5 + M1 + M2 em `da_forja_ao_diapasao.py` (base c04) — revalidar com -ql + PIL.
2. Sintetizar os 6 WAVs novos (§6).
3. `c06_consonancias` — fecha o arco pitagórico (conceitualmente a peça mais urgente).
4. `c02_retorno_saturno` — abre o argumento astrológico.
5. `c08_tetraktys` → `c09_kepler` → `c10_scafetta` (arco de validação; compartilham MathTex e razões).
6. `c11_relogio` + `c12_endcard` (fechamento e assinatura).
7. `c03_logos_hermes` (o mais trabalhoso: vetoriais de Hermes).
8. `c01_abertura` e `c07_peixe` (peças leves; fecha o mapa).
9. Montagem + narração + mix (§8.5–8.6).

---

## 10 · Pendências administrativas

- **Todas as 11 peças do mapa (§2) estão renderizadas em 1080p60 e validadas** — faltam apenas: gravação da narração (6 takes, roteiro §3), montagem (concat + xfade + mix), e os ajustes de P1–P5/M1/M2 do antigo `da_forja_ao_diapasao.py` ficaram obsoletos (c04 foi totalmente recriado em `martelos_monocordio.py`).
- Commit + push da fase local (scripts novos, sons, reestruturação `output/`) — **aguardando seu sinal**.
- `artigos/` versionar depois, como combinado.
- Dependência de ambiente: `MathTex` exige o pacote `texlive-latexextra` (classe `standalone.cls`) — instalado nesta sessão. Se o `latex.fmt` reclamar de versão divergente (`made by different executable version`), rodar `sudo fmtutil-sys --all`.
