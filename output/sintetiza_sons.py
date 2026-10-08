#!/usr/bin/env python3
"""
MISTAGOGOS · Síntese dos sons novos do vídeo 01 (planejamento §6)
================================================================

Gerados em output/sons/ — 44100 Hz · mono · int16, idêntico aos WAVs existentes:

- harpa_mi4_330.wav   · Karplus-Strong, tônica × 3:2 (Diapente — quinta justa)
- harpa_re4_293.wav   · Karplus-Strong, tônica × 4:3 (Diatessaron — quarta justa)
- harpa_si3_247.wav   · Karplus-Strong, tônica × 9:8 (Epogdoon — tom inteiro)
- tic_relogio.wav     · click metálico ~150/300 Hz + ruído, decay ~80 ms
- drone_esferas.wav   · 55 + 55,5 Hz detunados + ruído filtrado · 10 s loopável
- whoosh_agua.wav     · ruído com sweep de abertura 120→900 Hz · ~3 s

As três harpas travam na fundamental MEDIDA de harpa_la_220.wav — as razões
ouvidas (3:2, 4:3, 9:8) são exatas contra a tônica do vídeo, sejam quais
forem os arredondamentos da síntese original. RHO = 0.9965 por período,
calibrado pelos envelopes das harpas existentes (mesma família de timbre).
"""

import wave
from pathlib import Path

import numpy as np

SR = 44100
SONS = Path(__file__).resolve().parent / "sons"
RHO = 0.9965


# ———— E/S ————
def read_wav(path):
    with wave.open(str(path), "rb") as w:
        p = w.getparams()
        x = np.frombuffer(w.readframes(p.nframes), dtype=np.int16)
    return x.astype(np.float64) / 32768.0, p


def write_wav(path, x, peak):
    x = np.asarray(x, dtype=np.float64)
    m = float(np.abs(x).max())
    if m < 1e-9:
        raise ValueError("sinal nulo: %s" % path)
    xi = np.round(x / m * peak * 32767.0).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(xi.tobytes())


def edge_fade(x, fin_ms=2.0, fout_ms=8.0):
    ni = max(1, int(fin_ms * SR / 1000.0))
    no = max(1, int(fout_ms * SR / 1000.0))
    r = np.ones(len(x))
    r[:ni] = 0.5 - 0.5 * np.cos(np.linspace(0.0, np.pi, ni))
    if no < len(x):
        r[-no:] = 0.5 + 0.5 * np.cos(np.linspace(0.0, np.pi, no))
    return x * r


# ———— Medição espectral ————
def f0_fft(x, fmin, fmax):
    n = len(x)
    spec = np.abs(np.fft.rfft(x * np.hanning(n)))
    freqs = np.arange(len(spec)) * SR / n
    sel = (freqs >= fmin) & (freqs <= fmax)
    k = int(np.argmax(np.where(sel, spec, 0.0)))
    d = 0.0
    if 0 < k < len(spec) - 1:
        a, b, c = spec[k - 1], spec[k], spec[k + 1]
        den = a - 2.0 * b + c
        if den != 0.0:
            d = 0.5 * (a - c) / den
    return (k + d) * SR / n


def relatorio(path):
    y, p = read_wav(path)
    env = float(np.sqrt((y * y).mean()))
    print("  %-24s sr=%d ch=%d dur=%.2fs peak=%.3f rms=%.4f"
          % (path.name, p.framerate, p.nchannels,
             p.nframes / p.framerate, float(np.abs(y).max()), env))


# ———— Harpa Karplus-Strong com atraso fracionário (afinação exata) ————
def ks_harp(freq, dur, seed):
    d = SR / freq
    n = int(d)
    alpha = d - n
    n_total = int(round(dur * SR))
    y = np.zeros(n_total)
    y[: n + 2] = np.random.default_rng(seed).uniform(-1.0, 1.0, n + 2)
    for i in range(n + 2, n_total):
        y[i] = RHO * ((1.0 - alpha) * y[i - n] + alpha * y[i - n - 1])
    return y


# ———— Tic do relógio: parciais metálicas + burst de ruído ————
def tic_relogio(seed):
    k = int(0.5 * SR)
    t = np.arange(k) / SR
    rng = np.random.default_rng(seed)
    x = np.zeros(k)
    for f, a, tau in ((150.0, 1.0, 0.080), (300.7, 0.55, 0.055),
                      (452.0, 0.30, 0.040), (690.0, 0.16, 0.028)):
        x += a * np.sin(2.0 * np.pi * f * t
                       + rng.uniform(0.0, 2.0 * np.pi)) * np.exp(-t / tau)
    ruido = rng.uniform(-1.0, 1.0, k) * np.exp(-t / 0.008)
    x += 0.8 * np.convolve(ruido, np.ones(9) / 9.0, mode="same")
    return edge_fade(x)


# ———— Drone das esferas: 55 + 55,5 Hz (ciclos inteiros) + ruído em laço ————
def drone_esferas(seed):
    n = int(round(10.0 * SR))            # 441000: 550 e 555 ciclos exatos
    t = np.arange(n) / SR
    x = (0.50 * np.sin(2.0 * np.pi * 55.0 * t)
         + 0.45 * np.sin(2.0 * np.pi * 55.5 * t)
         + 0.15 * np.sin(2.0 * np.pi * 110.0 * t)
         + 0.13 * np.sin(2.0 * np.pi * 111.0 * t))
    m = n + 22050                        # 0,5 s extra para o crossfade do laço
    ru = np.random.default_rng(seed).uniform(-1.0, 1.0, m)
    a1 = 1.0 - np.exp(-2.0 * np.pi * 250.0 / SR)
    a2 = 1.0 - np.exp(-2.0 * np.pi * 35.0 / SR)
    l1 = np.empty(m)
    l2 = np.empty(m)
    v1 = 0.0
    v2 = 0.0
    for i in range(m):
        v1 += a1 * (ru[i] - v1)
        v2 += a2 * (ru[i] - v2)
        l1[i] = v1
        l2[i] = v2
    banda = (l1 - l2) / float(np.abs(l1 - l2).max())
    f = 22050
    s = np.arange(f) / float(f)
    loop_banda = np.empty(n)
    loop_banda[: n - f] = banda[f:n]
    loop_banda[n - f:] = banda[n:] * (1.0 - s) + banda[:f] * s
    salto = float(abs(loop_banda[0] - loop_banda[-1]))
    tipico = float(np.median(np.abs(np.diff(loop_banda[:4000]))))
    print("  laço do ruído: salto na emenda %.5f · passo típico %.5f"
          % (salto, tipico))
    return x + 0.22 * loop_banda


# ———— Whoosh da água: banda de ruído varrendo 120→900 Hz ————
def whoosh_agua(seed):
    dur = 3.0
    n = int(round(dur * SR))
    t = np.arange(n) / SR
    x = np.random.default_rng(seed).uniform(-1.0, 1.0, n)
    fc = 120.0 * (900.0 / 120.0) ** (t / dur)
    a1 = 1.0 - np.exp(-2.0 * np.pi * fc / SR)
    a2 = 1.0 - np.exp(-2.0 * np.pi * (fc / 4.0) / SR)
    y = np.empty(n)
    v1 = 0.0
    v2 = 0.0
    for i in range(n):
        v1 += a1[i] * (x[i] - v1)
        v2 += a2[i] * (x[i] - v2)
        y[i] = v1 - v2
    return y * np.sin(np.pi * t / dur) ** 2


def main():
    la, _ = read_wav(SONS / "harpa_la_220.wav")
    f0 = f0_fft(la, 200.0, 240.0)
    print("tônica medida em harpa_la_220.wav: %.3f Hz" % f0)

    print("— harpas travadas na tônica —")
    harpas = (
        ("harpa_si3_247.wav", 9.0 / 8.0, "Epogdoon 9:8", 3.3, 0.42, 1101),
        ("harpa_re4_293.wav", 4.0 / 3.0, "Diatessaron 4:3", 3.2, 0.41, 1102),
        ("harpa_mi4_330.wav", 3.0 / 2.0, "Diapente 3:2", 3.0, 0.40, 1103),
    )
    for nome, razao, rotulo, dur, peak, seed in harpas:
        f = f0 * razao
        y = ks_harp(f, dur, seed)
        write_wav(SONS / nome, y, peak)
        fm = f0_fft(y, 0.92 * f, 1.08 * f)
        desvio = abs(fm / f0 / razao - 1.0)
        print("  %-24s alvo %.3f Hz · medido %.3f Hz · razão %.5f · %s · desvio %.3f%%"
              % (nome, f, fm, fm / f0, rotulo, 100.0 * desvio))
        assert desvio < 0.002, nome
        relatorio(SONS / nome)

    print("— tic_relogio —")
    write_wav(SONS / "tic_relogio.wav", tic_relogio(7), 0.55)
    relatorio(SONS / "tic_relogio.wav")

    print("— drone_esferas —")
    write_wav(SONS / "drone_esferas.wav", drone_esferas(8), 0.30)
    relatorio(SONS / "drone_esferas.wav")

    print("— whoosh_agua —")
    write_wav(SONS / "whoosh_agua.wav", whoosh_agua(9), 0.50)
    relatorio(SONS / "whoosh_agua.wav")

    print("OK — 6 WAVs em %s" % SONS)


if __name__ == "__main__":
    main()
