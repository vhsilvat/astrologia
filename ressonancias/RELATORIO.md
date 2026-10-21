# Relatório: lacunas de Kirkwood e ondas da gota

Branch `claude/kirkwood-simulacao` (a partir da `master`). Executado em 21/out/2026.

## Resumo honesto

- **Dado real (MEDÍVEL):** o histograma de 182.252 asteroides do JPL mostra as lacunas em 3:1, 5:2, 7:3 e 2:1 e a concentração em 3:2 (grupo Hilda).
- **Modelo v1** (Sol + Júpiter, e inicial ≤ 0,1, 2×10⁵ anos) e as tentativas A, B, C (até 10⁶ anos): **nenhuma lacuna**. Mantidos abaixo como resultados negativos.
- **Modelo v2** (Sol + Júpiter + Saturno, e inicial do dado real, remoção por periélio q < 1,67 UA como proxy de Marte, 5×10⁵ anos): **o 3:1 se esvazia** (−8% em t = 0 → −60% aos 5×10⁵ anos, −4,4σ), mas **5:2, 7:3 e 2:1 não mostram lacuna** (−16%, −20%, +8%, todos dentro de ≈1,4σ). Com o critério antigo de remoção (r < 1 UA, e > 0,7) o 3:1 chega só a −20% (−1,5σ). Ou seja, o efeito no 3:1 depende do proxy de Marte, que é uma suposição declarada.
- A borda interna (2,0 a 2,2 UA) perde 88% das partículas na v2 (287 → 34), observação extra do adendo.
- A cena B mostra o dado real, a conta de Kepler, a vista orbital e a evolução da v2 com o resultado parcial dito na tela. Não afirmo que a simulação reproduz o cinturão: reproduz o esvaziamento do 3:1 e não os outros.

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

## Parte 5: modelo v2 (`kirkwood_sim_v2.py`, adendos 1 e 2 do prompt)

As simulações v1 (principal, A, B, C) terminaram antes do adendo 2; os arquivos e logs foram preservados. A v2 grava em arquivos próprios (`kirkwood_v2_*`).

Mudanças, definidas pelo adendo e não pelo resultado:

1. **Excentricidade inicial do dado real.** Para cada partícula (a uniforme em [2,0; 4,2] UA), e sorteada entre os asteroides reais do JPL com |a_real − a| ≤ 0,05 UA (`sbdb_mba.json` e `sbdb_externo.json`). 109 partículas (a > ≈3,6 UA, onde há poucos objetos) não tiveram ao menos 5 vizinhos reais e receberam e uniforme em [0; 0,2]. e inicial médio 0,146, máximo 0,660.
2. **Remoção.** Duas marcações na mesma integração: (a) critério de Marte: periélio q = a(1 − e) < 1,67 UA, ou r > 10 UA; (b) critério antigo: r < 1 UA, r > 10 UA ou e > 0,7. A partícula só sai da integração pelo critério antigo, então a contagem por Marte é a mesma partícula seguida até esse ponto.
3. **Saturno.** Sol, Júpiter (9,5479×10⁻⁴ M☉, a = 5,2044 UA, e = 0,0489) e Saturno (2,858×10⁻⁴ M☉, a = 9,58 UA, e = 0,057). Sem usar o Horizons: elementos planares fixos (ϖ e longitude média aproximados de J2000: Júpiter ϖ = 14,73°, L = 34,40°; Saturno ϖ = 92,60°, L = 49,94°), declarados aqui. Massa de Mercúrio a Marte (≈5,97×10⁻⁶ M☉) somada à do Sol.
4. **Limites do modelo:** planar; sem Marte como corpo; sem Vênus e Terra individuais; sem inclinação; sem interação entre partículas.
5. **Desempenho.** 3 processos (`multiprocessing`), `nice` 10, `OMP_NUM_THREADS=1`; cada processo integra 1.000 partículas com o mesmo Sol, Júpiter e Saturno. Tempo total 1576 s (26 min), abaixo dos 45 a 60 min estimados. Passo 0,1 ano; checagem de remoção a cada 5 anos (não a cada passo).
6. **Aviso do integrador.** Apareceu `Possible convergence issue. Timestep in Kepler solver is larger than one orbital period` durante a execução. Vem de partículas que mergulham perto do Sol (período < 0,1 ano) antes da checagem seguinte as remover. Não investiguei a fundo; essas partículas são removidas pelos dois critérios.
7. Semente 20261021 (o conjunto de a iniciais é o mesmo da simulação principal v1; ω, M e e diferem). Snapshots em t = 0, 1e3, 1e4, 5e4, 1e5, 2e5 e 5e5 anos.

### Resultado v2 (3.000 partículas, a de 2,0 a 4,2)

Remoção tipo Marte (q < 1,67 UA):

| t (anos) | vivas | 3:1 | 5:2 | 7:3 | 2:1 |
|---|---|---|---|---|---|
| 0 | 3000 | −8% (−0,6σ) | +20% | −20% | +20% |
| 1×10³ | 2686 | −11% | +21% | −22% | −14% |
| 1×10⁴ | 2534 | −35% (−2,6σ) | +12% | −17% | +2% |
| 5×10⁴ | 2410 | −53% (−3,8σ) | +4% | −18% | +10% |
| 1×10⁵ | 2319 | −53% (−3,8σ) | +3% | −17% | −2% |
| 2×10⁵ | 2180 | −56% (−4,1σ) | +3% | −18% | −20% |
| 5×10⁵ | 2067 | −60% (−4,4σ) | −16% (−1,1σ) | −20% (−1,4σ) | +8% (+0,6σ) |

Critério antigo (sem proxy de Marte), 5×10⁵ anos, 2316 vivas: 3:1 −20% (−1,5σ), 5:2 −3%, 7:3 −21%, 2:1 +10%.

Leitura:
- O 3:1 mostra uma queda monotônica e acima de 4σ só com a remoção por Marte. Com o critério antigo, não passa de 1,5σ. Isso sugere que o esvaziamento em a ≈ 2,50 UA é feito por partículas que ganham excentricidade e cruzam a órbita de Marte; mas "sugere" é o limite: não testei, por exemplo, uma variante sem Saturno com a mesma remoção, então não separo o papel de Saturno e o da remoção.
- 5:2, 7:3 e 2:1 não abrem lacuna em 5×10⁵ anos. O −20% no 7:3 já estava em t = 0 (acaso da semente), e o 2:1 oscila entre −20% e +10% sem tendência.
- 3:2 (Hilda): +14% em t = 0 e +132% aos 5×10⁵ anos (+5,0σ). Parte disso é artefato do método (a vizinhança externa é esvaziada porque partículas com a ≳ 3,6 a 4,2 UA são removidas, o que reduz a referência). Não afirmo captura em 3:2.

### Borda interna (observação extra)

Partículas com a inicial em 2,0 a 2,2 UA vivas (critério de Marte): 287 (t = 0) → 264 (10³) → 248 (10⁴) → 212 (5×10⁴) → 170 (10⁵) → 81 (2×10⁵) → 34 (5×10⁵ anos). As outras faixas perdem pouco (2,2 a 2,5: 409 → 321; 2,5 a 3,0: 690 → 634; 3,0 a 3,5: 655 → 637; 3,5 a 4,2: 959 → 441, a perda forte vem da borda caótica de Júpiter). O dado real tem a borda interna do cinturão em ≈2,1 UA. O adendo associa isso à ressonância secular ν6 com Saturno; eu só observo a depleção, não identifiquei o mecanismo.

## Parte 3: cenas (`kirkwood_scene.py`)

- **Gota** (~21 s): campo de ondas de duas fontes, matriz numpy 400×225 por quadro → `ImageMobject`, paleta Gruvbox. Rótulos "reforço" e "cancelamento" (o ponto do cancelamento fica na terceira linha nodal, |r₁−r₂| = 3λ/2), selo INTERPRETÁVEL (analogia), aviso de que a ressonância dos asteroides é gravitacional.
- **Lacunas** (~87 s): histograma real com as linhas e a conta a = a_J (1/3)^(2/3) = 2,50 UA; vista de cima (500 partículas, 3:1 em vermelho, três voltas por volta de Júpiter; dados da v1, 50 anos); histograma da simulação v2 em t = 0 a 5×10⁵ anos; quadro final comparando v2 × critério antigo × JPL e a borda interna. Legenda fixa "A ressonância limpa em vez de construir". Rótulos: dado real = MEDÍVEL; simulação = "MEDÍVEL (simulação própria: Sol, Júpiter, Saturno e partículas de teste)".
- Diferença em relação ao pedido: a cena B, item 4, não mostra a lacuna se abrindo em todas as ressonâncias: na v2 o 3:1 se esvazia e as outras não, e o quadro final diz isso na tela. O histograma de 0,01 UA com 3.000 partículas é ruidoso (≈14 por bin), então a queda do 3:1 aparece nos números do quadro final mais que a olho no gráfico.

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
- `lacunas_ql_3s.png` (histograma real), `lacunas_ql_8s.png` (conta de Kepler), `lacunas_ql_25s.png` (vista de cima), `lacunas_v2_ql_50s.png` e `lacunas_v2_ql_56s.png` (início da v2, histograma antes), `lacunas_v2_ql_62s.png` e `lacunas_v2_ql_68s.png` (histograma depois), `lacunas_v2_ql_final.png` (quadro final de comparação).

Os renders finais `-qh` (1920x1080, 60 fps) ficam em `output/media/videos/kirkwood_scene/1080p60/` (a pasta `media/` é ignorada pelo git, como no resto do projeto).

## Arquivos

`kirkwood_sim.py` (v1), `kirkwood_sim_v2.py`, `kirkwood_verify.py`, `kirkwood_scene.py`, `dados/` (`kirkwood_snapshots.npz`, `kirkwood_orbital.npz`, `kirkwood_tent_{A,B,C}.npz`, `kirkwood_v2_snapshots.npz` (e `_w{0,1,2}` parciais), `sbdb_mba.json`, `sbdb_externo.json`, `verificacao.json`), `frames/`.
