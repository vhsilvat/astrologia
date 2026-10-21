# Prompt para o Claude Code: lacunas de Kirkwood e ondas da gota

Uso no V2, tijolo "A Lua e o relógio da vida" (ver `canal/roadmap.md`). Quem executa: Claude Code local do Victor.

## Antes de começar

Leia `CLAUDE.md`, `canal/decisoes.md`, o tijolo T3 do V2 em `canal/roadmap.md`, `canal/manim_referencia.md` e um molde aprovado (procure `monocordio_harpa.py` e `harmonia_corda.py` no repositório). Trabalhe numa branch nova, `claude/kirkwood-simulacao`, a partir da `master`. Não faça merge na `master`. Valide, renderize, commite e dê push você mesmo. Se precisar decidir algo, escolha o padrão mais simples e anote no relatório; não pare para perguntar.

## Objetivo

Duas cenas em Manim CE, 1920x1080 a 60 fps no padrão visual do canal (Gruvbox estrito, EB Garamond, textos em português do Brasil, sem travessão como pausa), apoiadas num dado que dê para verificar. O estatuto de cada cena vai rotulado na tela com os termos do canal: MEDÍVEL, INTERPRETÁVEL.

## Parte 1: simulação numérica (`ressonancias/kirkwood_sim.py`)

- Problema restrito e planar: Sol (1 massa solar), Júpiter (9,5479e-4 massa solar, a = 5,2044 UA, e = 0,0489) e N = 3000 partículas de teste sem massa, com a uniforme em [2,0; 4,2] UA, e uniforme em [0; 0,1], ângulos aleatórios e semente fixa.
- Use `rebound` (`pip install rebound`), integrador WHFast, passo de ≈0,1 ano. Se não instalar, escreva um integrador simplético próprio com numpy e diga isso no relatório.
- Tempo total: 2×10⁵ anos (≈17.000 períodos de Júpiter). Salve snapshots (a, e, vivo/ejetado) em t = 0, 1e3, 1e4, 5e4, 1e5 e 2e5 anos.
- Para a animação orbital, salve à parte as posições (x, y) de um subconjunto de 500 partículas, em ≈600 quadros cobrindo os primeiros ≈50 anos.
- Marque como "ejetada" a partícula com r < 1,0 UA, r > 10 UA ou e > 0,7.
- Guarde tudo em `.npz` dentro de `ressonancias/dados/`. Se a execução ficar lenta, reduza N antes de reduzir o tempo e documente.

## Parte 2: verificação honesta (`ressonancias/kirkwood_verify.py`, gera `ressonancias/RELATORIO.md`)

- Posições teóricas pela terceira lei de Kepler: a = a_Júpiter · (período relativo)^(2/3). Esperado: 3:1 em 2,50 UA (período do asteroide = 1/3 do de Júpiter), 5:2 em 2,82, 7:3 em 2,95, 2:1 em 3,27. Concentração esperada em 3:2 (grupo Hilda) em 3,97 UA.
- Histograma de a (bins de 0,01 UA) em t = 0 e no final. Para cada ressonância, compare a contagem em ±0,02 UA com a média de janelas vizinhas (de ±0,05 a ±0,15 UA) e reporte a queda ou o aumento em porcentagem.
- Regra principal: não ajuste parâmetros até a lacuna aparecer. Se algo não aparecer em 2×10⁵ anos, reporte isso. Só então teste mais tempo ou mais partículas, descrevendo cada tentativa. Não invente dado. O relatório diz o que apareceu e o que não apareceu (as lacunas 5:2 e 7:3 costumam ser mais fracas).
- Se houver rede, baixe do JPL SBDB (`https://ssd-api.jpl.nasa.gov/sbdb_query.api`) os asteroides do cinturão principal (a, e, H) e faça o histograma real. Ele é o dado MEDÍVEL; a simulação é a explicação. Sem rede, diga isso no relatório.

## Parte 3: cenas (`ressonancias/kirkwood_scene.py`)

**Cena A, "Gota" (≈20 s).** Campo de ondas 2D de duas fontes pontuais (gotas) com interferência, desenhado como imagem atualizada por quadro (numpy → `ImageMobject`) com paleta Gruvbox. Rótulos "reforço" e "cancelamento" nas regiões correspondentes e o selo INTERPRETÁVEL (analogia).

**Cena B, "Lacunas" (≈60 a 75 s).**
1. Histograma real (se houver) com as lacunas.
2. Linhas verticais nas ressonâncias, rotuladas 3:1, 5:2, 7:3 e 2:1, com a conta a = a_J · (1/3)^(2/3).
3. Vista de cima: Sol, Júpiter e partículas coloridas por a, em movimento orbital, com as partículas em 3:1 destacadas.
4. Histograma da simulação evoluindo de t = 0 a 2×10⁵ anos, com a lacuna se abrindo.

Rótulos: dado real = MEDÍVEL; simulação = "MEDÍVEL (simulação própria: Sol, Júpiter e partículas de teste)". Legenda fixa: "A ressonância limpa em vez de construir". Não afirmar que as ondas da gota são a causa: a ressonância é gravitacional.

## Parte 4: verificação visual (para o Claude do chat conferir)

- Renderize em `-ql` e salve quadros PNG de momentos-chave em `ressonancias/frames/` (início, meio e fim de cada cena; histograma antes e depois), com `manim render -s` ou `ffmpeg -ss`. Registre os comandos no `RELATORIO.md`.
- Faça o render final em `-qh` e salve em `output/`.
- No `RELATORIO.md`, liste versões (Python, Manim, rebound), tempo de execução e semente. Commite e dê push na branch.
