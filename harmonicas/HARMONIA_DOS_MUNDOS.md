# A harmonia dos mundos: como o wav é montado

Animação Manim de 90 s (`harmonia_dos_mundos.py`, cena `HarmoniaDosMundos`): o tempo passa no
sistema solar visto de cima e cada planeta "canta" a própria velocidade angular heliocêntrica.
O `.wav` não vai para o git (`harmonicas/sons/` está no `.gitignore`). Ele é regenerável e
determinístico (semente 1619).

## Como regenerar

```
pip install manim numpy scipy ephem
python3 harmonicas/harmonia_dos_mundos.py                              # só o áudio -> harmonicas/sons/harmonia_dos_mundos.wav
manim render -qh --fps 30 harmonicas/harmonia_dos_mundos.py HarmoniaDosMundos   # vídeo 1080p30 (gera o wav sozinho se faltar)
```

Fonte EB Garamond precisa estar instalada. Variável `HARM_QUADRO=<s>` com `-s` renderiza um
único quadro (teste de layout).

## Definição de altura (MEDÍVEL / INTERPRETÁVEL)

- **MEDÍVEL:** posição heliocêntrica de cada planeta nas efemérides VSOP87 (PyEphem, não o JPL,
  porque o ambiente em que foi feito não alcança o JPL). A longitude é desenrolada e ajustada
  por spline cúbica; a derivada da spline é a velocidade angular ω (rad/dia). A Terra vem de
  `ephem.Sun` (`hlon`, `earth_distance`).
- **INTERPRETÁVEL:** frequência = `F_G * (ω / ω_Saturno,mín) * 2^(-k)`. `F_G` = 97,9989 Hz
  (G2), o afélio de Saturno, o movimento mais lento de todos. Os demais planetas guardam a
  razão exata com Saturno e descem `k` oitavas inteiras para caber na orquestra (Marte 2,
  Terra 2, Vênus 3, Mercúrio 3). É a definição de Kepler, *Harmonices Mundi* V (1619): a altura
  segue o movimento aparente visto do Sol, do afélio (grave) ao periélio (agudo), de modo
  contínuo, sem saltos.
- Vozes na ordem de Kepler (V.8): Saturno e Júpiter baixo, Marte tenor, Terra e Vênus
  contralto, Mercúrio soprano.

## Tempo

`dias(t)` converte segundos de vídeo em dias de calendário a partir de 22/out/2026: 8 d/s até
20 s, rampa linear até 36 d/s aos 50 s, constante depois. O mesmo `dias(t)` alimenta imagem e
som, então os dois não saem de sincronia.

## Síntese (função `gera_audio`, 44,1 kHz estéreo)

Não é sample nem SoundFont: é síntese aditiva, calculada a cada amostra.

1. `f(t)` = frequência da voz do planeta ao longo dos 90 s, a partir de `dias(t)` e da spline de ω.
2. Cada voz (`_voz`) soma 2 a 3 cópias levemente desafinadas (efeito de naipe de cordas), cada
   uma com vibrato próprio, deriva lenta de afinação e fase aleatória.
3. Cada cópia soma até 9 a 22 harmônicos (conforme o planeta), gerados pela recorrência de
   Chebyshev `sin((n+1)φ) = 2cosφ·sin(nφ) − sin((n−1)φ)`, com amplitude `n^-1.15`, corte
   passa-baixa de 650 a 2400 Hz e realces suaves de "corpo de madeira" perto de 280, 550 e
   1100 Hz. A fase φ é a integral da frequência instantânea, por isso o glissando é contínuo.
4. Saturno ganha um sub-harmônico (oitava abaixo, baixinho) para pesar como contrabaixo.
   Mercúrio tem ganho reduzido (0,30), porque a varredura rápida dele soa como sirene.
5. Um sopro de arco (ruído em banda 1,5 a 5,5 kHz, bem baixo) dá o ataque de corda.
6. Pan por voz (Saturno à direita, Mercúrio à esquerda).
7. Reverb por convolução com uma resposta sintética (ruído com decaimento, RT60 2,6 s, passa-baixa
   4,5 kHz, mix 28%).
8. Normalização para pico 0,89 e limitador `tanh` suave, fade-in de 0,4 s.

Entradas das vozes (s): Saturno 1,5; Júpiter 5; Marte 8,5; Terra 12; Vênus 15,5; Mercúrio 19.

## Limites conhecidos

- O som nunca foi ouvido por quem escreveu o código (só espectrograma: as linhas de altura
  seguem os planetas; RMS cerca de −14 dBFS). Timbre e andamento dependem do ouvido de quem
  testa.
- Efemérides VSOP87 batem com a tabela de movimentos extremos de Kepler (1619) em cerca de
  1 a 3% (Marte: 26,2 e 38,1 min/dia contra 26′14″ e 38′1″; Mercúrio: 164,6 e 379 contra 164′ e 384′).
- Alternativa mais "orquestral": renderizar com SoundFont e pitch-bend contínuo (licença do
  SoundFont a conferir). Já existe uma: `sinfonia_orquestra2.py` (General MIDI via FluidSynth, uma nota por pulso).
