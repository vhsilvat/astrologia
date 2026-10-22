# Animações pendentes (ideias para não esquecer)

> Registro de 21/out/2026. Nada aqui foi construído. Cada item diz de onde vem, o que mostrar e o que ainda falta decidir.

## 1. Kepler: da gravura à animação (V1, tijolo T4 "O céu e o estudo que o testa") **[PROPOSTO, aceito pelo Victor]**

Ordem na tela:
1. **Gravura de 1619, 3 a 4 s**, para passar autoridade (é a imagem do livro, não uma recriação). Usar a gravura original (domínio público) a partir da digitalização de 1619; ver "Fonte" abaixo.
2. **Redesenhar em Manim só o que carrega a ideia:** as faixas de velocidade angular de cada planeta (do afélio ao periélio) sobre um **teclado**, com som. É o que Kepler chama de "melodia" de cada planeta (livro V, caps. 4 a 6). Rótulo: MEDÍVEL para as velocidades, INTERPRETÁVEL para a leitura como música.
3. **Os cinco sólidos entre as esferas ficam como imagem, sem animar.** Motivo: o próprio Kepler diz que o encaixe não é exato ("Nevertheless it is not wholly equal, as I once dared to promise", livro V, cap. 3 [277], trad. Wallis 1939). Animar seria dar à ideia mais precisão do que ela tem.

**[RASCUNHO FEITO em 22/out]** `harmonicas/harmonia_dos_mundos.py` (cena `HarmoniaDosMundos`, 90 s): o tempo passa no sistema solar (vista de cima, ângulos reais) e os seis planetas tocam a velocidade angular heliocêntrica como altura (afélio de Saturno = G, 98 Hz; razões exatas; transposição por oitavas; vozes na ordem de Kepler, V.8), com faixas sobre um teclado e som de cordas sintetizado. Dados: efemérides VSOP87 (PyEphem). Falta o Victor ouvir e ajustar timbre, andamento e quanto cabe no T4. A faixa do planeta só mostra o intervalo medido hoje; as razões de Kepler (4:5, 5:6, 2:3, 15:16, 24:25, 5:12) estão no rótulo.

Pontos a decidir: se o som usa a afinação justa (razões como 5:4, 4:3, 3:2) ou a temperada; se as faixas mostram os seis planetas ou só alguns; quanto tempo cabe no orçamento do T4 (≈3:15).

Dados na fonte: tabelas de movimentos extremos e de excentricidades (livro V, caps. 4 e 9) e as pautas dos caps. 6 e 7 (notas de Elliott Carter na edição de 1939; conferir direitos antes de reproduzir a página).

**Fonte para as gravuras e o texto original:** *Ioannis Keppleri Harmonices mundi libri V* (Linz, 1619), digitalização da Smithsonian Libraries no Internet Archive: `archive.org/details/ioanniskepplerih00kepl` (360 páginas, latim, inclui o Apêndice sobre Ptolomeu e Fludd; PDF 27,5 MB, texto 982 KB). O PDF em inglês que temos (Wallis, 1939) é só o livro V.

## 2. Teste da tira de tempo com zoom in e zoom out **[PENDENTE, "deixar para depois"]**

**Ideia do Victor:** a linha do tempo do mapa (Cadeia de Ouro) fica na tela. O tijolo dá *zoom in* no ponto que cita; as animações e os temas do tijolo acontecem dentro desse zoom; *zoom out* para a tira inteira, que acende o ponto ligado; *zoom in* de novo no seguinte. É animação sobre a narração, não fala.

**Amostra mínima proposta (antes de gastar tempo com o resto):** três pontos da linhagem `v1-corda-ao-ceu`: Pitágoras, Kepler e Bank & Scafetta (2022). Dados saem de `genealogia/data/*.json` (nome, data, faixa, cor da faixa).

**Como julgar a amostra (o ponto é o tom, não o efeito):**
- Movimento lento e sem sobressalto; zoom de ≈3 a 4 s, sobre a fala que já corre (não soma tempo).
- A tira inteira sempre legível quando está de fora; cores das faixas do mapa (Gruvbox), para o espectador reconhecer a faixa.
- Ao parar num ponto, mostrar nome, data e a fonte (livro ou artigo) na tela.
- Se parecer palestra de marketing ou efeito de transição de aplicativo, cortar e deixar a tira estática com um destaque.

**Sequência de saltos que a tira precisa cobrir no V1:** séc. VI a.C. (Pitágoras) → séc. II (Nicômaco, Ptolomeu) → 1619 (Kepler) → séc. IX (Tábua de Esmeralda) → 1908 (*Caibalion*) → 1924 em diante (de Broglie) → 2022 (Bank & Scafetta). Nem todos estão no mapa: de Broglie e a física quântica ficam fora dele e entrariam como marcas à parte.

Quando for a hora: gerar o prompt para o Claude Code (cena Manim `TiraDeTempo`, lendo os JSON do mapa) e renderizar os quadros-chave em `ressonancias/frames/` ou numa pasta própria para o Claude do chat conferir.
