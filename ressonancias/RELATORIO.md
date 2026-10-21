# Relatório: lacunas de Kirkwood e ondas da gota

Branch `claude/kirkwood-simulacao` (a partir da `master`). Executado em 21/out/2026.

## Resumo honesto

- **Dado real (MEDÍVEL):** o histograma de 182.252 asteroides do JPL mostra as lacunas em 3:1, 5:2, 7:3 e 2:1 e a concentração em 3:2 (grupo Hilda).
- **Simulação própria (MEDÍVEL, só como explicação):** com os parâmetros do prompt (e inicial ≤ 0,1, 2×10⁵ anos, 3.000 partículas) **nenhuma lacuna se abriu**. Os desvios em ±0,02 UA ficaram dentro de ≈1,3σ de ruído de contagem.
- Três tentativas suplementares (abaixo), até 10⁶ anos, **também não abriram lacuna**. Não ajustei parâmetros até o efeito aparecer; a cena B mostra o resultado como ele é.
- Efeito: a cena B mostra o dado real com lacunas e, depois, a simulação sem lacuna, com a frase "esta simulação simples não abre as lacunas; o céu real as tem". Não afirmo que a simulação explica as lacunas.

## Versões e execução

- Python 3.14.7, Manim CE 0.21.0, rebound 5.2.2, numpy 2.5.3.
- Semente: 20261021 (`numpy.random.default_rng`). Tentativas A, B, C: sementes 1, 2, 3.
- Tempo de execução (CPU única por processo): simulação principal 1873 s; A 3182 s; B 3175 s; C 5191 s.
- Integrador: WHFast, passo 0,1 ano, problema restrito planar (Sol 1 M☉, Júpiter 9,5479×10⁻⁴ M☉, a = 5,2044 UA, e = 0,0489, partículas de teste sem massa).

## Parte 1: simulação (`kirkwood_sim.py`)

- N = 3000, a uniforme em [2,0; 4,2] UA, e uniforme em [0; 0,1], ω e M aleatórios, inclinação zero.
- Snapshots (a, e, vivo/ejetado) em t = 0, 1e3, 1e4, 5e4, 1e5, 2e5 anos em `dados/kirkwood_snapshots.npz`.
- Ejeção: r < 1,0 UA, r > 10 UA ou e > 0,7, **checada a cada 10 anos** (não a cada passo); a partícula ejetada sai da integração e fica marcada como morta. Sobreviventes em 2×10⁵ anos: 2787 de 3000.
- Os elementos (a, e) gravados são **osculantes heliocêntricos**; as oscilações de curto período causadas por Júpiter alargam o histograma em ~0,01 UA.
- Teste de sanidade da ejeção: em 1000 anos foram perdidas 55 partículas, todas com a inicial ≥ 4,0 UA, perto da zona caótica de Júpiter, como esperado. O integrador remove partículas.
- Animação orbital: subconjunto das 500 primeiras partículas, 600 quadros em 50 anos, `dados/kirkwood_orbital.npz`. Para ter quadros uniformes usei um passo de 0,0417 ano (dois passos por quadro) numa execução curta separada, e não o passo de 0,1 ano da execução longa. Como as partículas de teste não interagem, a dinâmica de cada uma é a mesma.

## Parte 2: verificação (`kirkwood_verify.py`, números em `dados/verificacao.json`)

Posições teóricas, a = a_J · (período relativo)^(2/3), com a_J = 5,2044 UA:

| ressonância | razão de períodos (asteroide/Júpiter) | a (UA) |
|---|---|---|
| 3:1 | 1/3 | 2,502 |
| 5:2 | 2/5 | 2,825 |
| 7:3 | 3/7 | 2,958 |
| 2:1 | 1/2 | 3,279 |
| 3:2 (Hilda) | 2/3 | 3,972 |

Método: contagem em ±0,02 UA comparada com a densidade média das janelas vizinhas (0,05 < |a − a_res| ≤ 0,15 UA, dos dois lados), reescalada para a mesma largura. Variação % = contagem / esperado − 1. σ = (obs − esperado) / √esperado (Poisson).

### Simulação principal (3.000 partículas, a de 2,0 a 4,2)

| t (anos) | vivas | 3:1 | 5:2 | 7:3 | 2:1 |
|---|---|---|---|---|---|
| 0 | 3000 | −8% (−0,6σ) | +20% (+1,4σ) | −20% (−1,5σ) | +20% (+1,4σ) |
| 1×10³ | 2945 | −6% | +22% | −17% | −12% |
| 1×10⁴ | 2871 | −3% | +18% | −19% | +4% |
| 5×10⁴ | 2818 | −4% | +24% | −21% | −10% |
| 1×10⁵ | 2802 | −5% | +26% | −20% | +6% |
| 2×10⁵ | 2787 | −3% (−0,2σ) | +16% (+1,1σ) | −18% (−1,3σ) | −15% (−1,1σ) |

Leitura: nada aparece além do ruído. As diferenças já existiam em t = 0 (a semente produz esses acasos) e não crescem com o tempo. As lacunas 5:2 e 7:3 já são mais fracas na natureza; aqui não aparecem de jeito nenhum.
3:2 (Hilda): +14% em t = 0, +45% em 10⁴ anos (+2,8σ), +30% em 2×10⁵ anos (+1,8σ). O excesso vem em boa parte de um artefato do método: acima de ≈4,0 UA as partículas são ejetadas (zona caótica de Júpiter), o que esvazia a vizinhança externa usada como referência e infla a razão. Não é prova de captura em 3:2.

### Tentativas suplementares (descritas uma a uma, rodadas depois do resultado acima)

Motivo: o prompt manda reportar a ausência e só então testar mais tempo ou mais partículas. Não ajustei nada para forçar o efeito; cada tentativa muda um fator e o resultado está abaixo, qualquer que seja.

| tentativa | a inicial | e inicial | N | tempo | 3:1 em t final |
|---|---|---|---|---|---|
| A | 2,3 a 2,7 | ≤ 0,1 | 800 | 10⁶ anos | −10% (−0,9σ); 800 vivas |
| B | 2,3 a 2,7 | ≤ 0,2 | 800 | 10⁶ anos | −15% (−1,3σ); 796 vivas |
| C | 2,0 a 3,4 | ≤ 0,1 | 1500 | 10⁶ anos | 3:1 −32% (−2,1σ); 5:2 −4%; 7:3 −17%; 1493 vivas |

Em C o 3:1 já estava −26% em t = 0 (−1,7σ) e fica entre −24% e −32% em todos os snapshots, ou seja, não há tendência temporal: é o acaso da semente. Em A e B, o 3:1 em t = 0 já era −10% e −11%.

Não testei: partículas com e inicial ≥ 0,3 numa faixa larga, mais de 10⁶ anos, Saturno e Marte no modelo, nem mais de uma semente por configuração. Hipótese não testada: o esvaziamento real do 3:1 depende de ressonâncias seculares com Saturno (ν6) e de excentricidades iniciais maiores, ausentes aqui. Isso é hipótese, não resultado.

### Dado real (JPL SBDB)

- Consulta `https://ssd-api.jpl.nasa.gov/sbdb_query.api` em 21/out/2026 (rede disponível). Campos a, e, H. Filtro H < 16 (amostra aproximadamente completa, menos viés de observação).
- Duas consultas, porque a classe MBA do JPL termina em a = 3,2 UA: (1) classe MBA, H < 16 → 169.085 objetos (`dados/sbdb_mba.json`); (2) asteroides com 3,2 ≤ a ≤ 4,4 e H < 16 → 13.167 objetos (`dados/sbdb_externo.json`). Uso a entre 2,0 e 4,4 UA, total 182.252 objetos.

| ressonância | em ±0,02 UA | esperado pela vizinhança | variação |
|---|---|---|---|
| 3:1 (2,50) | 951 | 6975 | −86% |
| 5:2 (2,82) | 1883 | 5477 | −66% |
| 7:3 (2,96) | 4275 | 6822 | −37% |
| 2:1 (3,28) | 197 | 6426 | −97% |
| 3:2 (3,97) | 1750 | 30 | +5657% |

Ressalvas: 5:2 e 7:3 são mais fracas que 3:1 e 2:1 também no dado real (−66% e −37%). No 3:2, a vizinhança é quase vazia (os Hildas ficam isolados), então o percentual enorme só diz "muito mais que o fundo", não é uma razão comparável às outras.

## Parte 3: cenas (`kirkwood_scene.py`)

- **Gota** (~21 s): campo de ondas de duas fontes, matriz numpy 400×225 por quadro → `ImageMobject`, paleta Gruvbox. Rótulos "reforço" e "cancelamento" (o ponto do cancelamento fica na terceira linha nodal, |r₁−r₂| = 3λ/2), selo INTERPRETÁVEL (analogia), aviso de que a ressonância dos asteroides é gravitacional.
- **Lacunas** (~81 s): histograma real com as linhas e a conta a = a_J (1/3)^(2/3) = 2,50 UA; vista de cima (500 partículas, 3:1 em vermelho, três voltas por volta de Júpiter); histograma da simulação em t = 0 a 2×10⁵ anos; quadro final com a comparação simulação × tentativa A × JPL. Legenda fixa "A ressonância limpa em vez de construir". Rótulos: dado real = MEDÍVEL; simulação = "MEDÍVEL (simulação própria: Sol, Júpiter e partículas de teste)".
- Diferença em relação ao pedido: a cena B, item 4, não mostra "a lacuna se abrindo", porque a simulação não a abriu. Mostra o histograma sem lacuna e diz isso na tela.

## Parte 4: verificação visual

Comandos (a partir de `output/`):

```
cd output && source ../venv/bin/activate
manim render -ql ../ressonancias/kirkwood_scene.py Gota
manim render -ql ../ressonancias/kirkwood_scene.py Lacunas
ffmpeg -ss <t> -i media/videos/kirkwood_scene/480p15/<Cena>.mp4 -frames:v 1 ../ressonancias/frames/<arquivo>.png
manim render -qh ../ressonancias/kirkwood_scene.py Gota
manim render -qh ../ressonancias/kirkwood_scene.py Lacunas
```

Quadros em `ressonancias/frames/`:

- `gota_ql_1s.png` (uma gota), `gota_ql_10s.png` (rótulos), `gota_ql_19s.png` (aviso final).
- `lacunas_ql_3s.png` (histograma real), `lacunas_ql_8s.png` (conta de Kepler), `lacunas_ql_25s.png` (vista de cima), `lacunas_ql_45s.png` e `lacunas_ql_56s.png` (início e meio da simulação, histograma antes), `lacunas_ql_62s.png` e `lacunas_ql_70s.png` (histograma depois), `lacunas_ql_78s.png` (quadro final de comparação).

Os renders finais `-qh` (1920x1080, 60 fps) ficam em `output/media/videos/kirkwood_scene/1080p60/` (a pasta `media/` é ignorada pelo git, como no resto do projeto).

## Arquivos

`kirkwood_sim.py`, `kirkwood_verify.py`, `kirkwood_scene.py`, `dados/` (`kirkwood_snapshots.npz`, `kirkwood_orbital.npz`, `kirkwood_tent_{A,B,C}.npz`, `sbdb_mba.json`, `sbdb_externo.json`, `verificacao.json`), `frames/`.
