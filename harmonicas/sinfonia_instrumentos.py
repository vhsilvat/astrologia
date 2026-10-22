"""
MISTAGOGOS · "A harmonia do mundo", versão com instrumentos (quinteto barroco do Wolfram)

Mesmas órbitas e mesma regra f ∝ ω de sinfonia.py, agora com um instrumento por planeta,
na distribuição das vozes de Kepler: Mercúrio, soprano (cravo); Vênus e Terra, contralto
(dois violinos); Marte, tenor (viola); Júpiter e Saturno, baixo (dois violoncelos).
Síntese aditiva própria (sem sampler): cordas friccionadas com vibrato, cravo dedilhado,
reverberação e panorama estéreo. As vozes entram uma a uma.

Uso: cd output && manim render -qh ../harmonicas/sinfonia_instrumentos.py SinfoniaInstrumentos
"""

import sys
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sinfonia import (  # noqa: E402
    DUR, F_SATURNO, OM_REF, ORBITAS, SR, Sinfonia, anos,
)

WAV_INSTR = Path(__file__).resolve().parent / "wav" / "sinfonia_instrumentos.wav"

# planeta: (instrumento, oitavas abaixo do f bruto, entrada em s, pan -1..1, ganho)
VOZES = {
    "Mercúrio": ("cravo", 4, 16.0, 0.55, 0.55),
    "Vênus": ("violino", 3, 13.0, 0.35, 0.40),
    "Terra": ("violino", 3, 10.0, 0.15, 0.45),
    "Marte": ("viola", 3, 7.0, -0.10, 0.55),
    "Júpiter": ("violoncelo", 1, 4.0, -0.30, 0.75),
    "Saturno": ("violoncelo", 0, 1.5, -0.50, 0.90),
}
# corte (Hz) do rolamento de harmônicos de cada corda e vibrato (Hz, profundidade relativa)
CORDAS = {"violino": (3200.0, 5.6, 0.0045), "viola": (2200.0, 5.2, 0.0040),
          "violoncelo": (1300.0, 4.8, 0.0035)}
PASSO_CRAVO = 0.2  # s entre dedilhados


def freq_voz(nome, tt):
    o = ORBITAS[nome]
    _, _, om, _ = o.estado(anos(tt))
    return F_SATURNO * om / OM_REF / 2 ** VOZES[nome][1]


def corda(nome, t, rng, idx):
    inst, _, entrada, _, _ = VOZES[nome]
    fc, vib_hz, vib_prof = CORDAS[inst]
    f = freq_voz(nome, t)
    vib = vib_prof * np.sin(2 * np.pi * vib_hz * t + 1.7 * idx) * np.clip((t - entrada - 0.8) / 1.5, 0, 1)
    fase = 2 * np.pi * np.cumsum(f * (1 + vib)) / SR
    # arco: leve flutuação lenta de amplitude (ruído filtrado)
    lento = np.convolve(rng.standard_normal(t.size), np.ones(2205) / 2205, mode="same")
    amp_arco = 1 + 3.0 * lento / (lento.std() * 6)
    x = np.zeros_like(t)
    for k in range(1, 22):
        ak = (1.0 / k) / (1 + (k * f / fc) ** 2) * (1 if k % 2 else 0.85)
        ak = np.where(k * f < 0.45 * SR, ak, 0.0)
        x += ak * np.sin(k * fase)
    ataque = np.clip((t - entrada) / 0.6, 0, 1) ** 1.5
    return x * ataque * amp_arco


def cravo(nome, t, rng):
    _, _, entrada, _, _ = VOZES[nome]
    saida = np.zeros_like(t)
    dur = int(1.4 * SR)
    tl = np.arange(dur) / SR
    for t0 in np.arange(entrada, DUR - 0.05, PASSO_CRAVO):
        f0 = float(freq_voz(nome, np.array([t0]))[0])
        i0 = int(t0 * SR)
        seg = np.zeros(min(dur, t.size - i0))
        for k in range(1, 16):
            if k * f0 > 0.45 * SR:
                break
            tau = 0.55 / (1 + 0.35 * (k - 1))
            seg += (1.0 / k ** 0.8) * np.exp(-tl[:seg.size] / tau) * np.sin(2 * np.pi * k * f0 * tl[:seg.size] + k)
        seg *= np.minimum(1, tl[:seg.size] / 0.004)
        saida[i0:i0 + seg.size] += seg
    return saida


def reverb(x, rng, seg=1.8, mix=0.22):
    n = int(seg * SR)
    ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR / 0.55 * 3.0)
    ir /= np.abs(ir).sum() ** 0.5
    N = 1 << int(np.ceil(np.log2(x.size + n)))
    y = np.fft.irfft(np.fft.rfft(x, N) * np.fft.rfft(ir, N), N)[: x.size]
    y *= x.std() / (y.std() + 1e-12)
    return (1 - mix) * x + mix * y


def gera_audio_instrumentos():
    rng = np.random.default_rng(1996)
    t = np.arange(int(SR * DUR)) / SR
    L = np.zeros_like(t)
    R = np.zeros_like(t)
    for idx, (nome, (inst, _, entrada, pan, ganho)) in enumerate(VOZES.items()):
        x = cravo(nome, t, rng) if inst == "cravo" else corda(nome, t, rng, idx)
        x = x / (np.abs(x).max() + 1e-12) * ganho
        ang = (pan + 1) * np.pi / 4
        L += x * np.cos(ang)
        R += x * np.sin(ang)
    env = np.minimum(1.0, (DUR - t) / 3.0)
    L, R = reverb(L * env, rng), reverb(R * env, rng)
    pico = max(np.abs(L).max(), np.abs(R).max())
    est = np.stack([L, R], axis=1) / pico * 0.8
    WAV_INSTR.parent.mkdir(exist_ok=True)
    with wave.open(str(WAV_INSTR), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((est * 32767).astype("<i2").tobytes())


class SinfoniaInstrumentos(Sinfonia):
    X_PAINEL = (0.45, 3.6, 5.3, 5.65)
    ENTRADAS = {n: v[2] for n, v in VOZES.items()}

    def prepara_audio(self):
        gera_audio_instrumentos()
        return WAV_INSTR

    def rotulo_det(self, nome, o):
        return f"{VOZES[nome][0]} · mín:máx {o.om_min / o.om_max:.2f} · Kepler {o.kepler}"

    def freq_painel(self, nome, o, tt):
        return freq_voz(nome, tt)
