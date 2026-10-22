"""
MISTAGOGOS · "A harmonia do mundo", versão orquestra (instrumentos de verdade)

Mesma regra do Wolfram: cada planeta toca uma nota por pulso, em semitons (a discretização de
Kepler), com os instrumentos General MIDI do quinteto barroco: cravo (Mercúrio), dois violinos
(Vênus, Terra), viola (Marte) e dois violoncelos (Júpiter, Saturno). A diferença é que a nota de
cada pulso vem da velocidade angular ω(t) da órbita kepleriana real (f = 98,12 Hz · ω/ω_mín(Saturno)).
O áudio é renderizado pelo FluidSynth com o soundfont GeneralUser GS (~/apps/soundfonts).

Uso: cd output && manim render -qh ../harmonicas/sinfonia_orquestra.py SinfoniaOrquestra
"""

import struct
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sinfonia import DUR, Sinfonia  # noqa: E402
from sinfonia_instrumentos import VOZES, freq_voz  # noqa: E402

AQUI = Path(__file__).resolve().parent
SF2 = Path.home() / "apps" / "soundfonts" / "gu" / "GeneralUser-GS-main" / "GeneralUser-GS.sf2"
MID = AQUI / "wav" / "sinfonia_orquestra.mid"
WAV_ORQ = AQUI / "wav" / "sinfonia_orquestra.wav"
TPQ = 480  # ticks por semínima; a 120 bpm, 1 s = 960 ticks
TICKS_S = 2 * TPQ

# planeta: (canal, programa GM, pulso em s, nota longa?, velocity, pan 0-127)
GM = {
    "Saturno": (0, 42, 1.0, 1.02, 88, 30),
    "Júpiter": (1, 42, 1.0, 1.02, 84, 45),
    "Marte": (2, 41, 1.0, 1.02, 80, 62),
    "Terra": (3, 40, 1.0, 1.02, 78, 80),
    "Vênus": (4, 40, 1.0, 1.02, 74, 95),
    "Mercúrio": (5, 6, 0.5, 0.45, 92, 110),
}


def vlq(n):
    b = [n & 0x7F]
    n >>= 7
    while n:
        b.append((n & 0x7F) | 0x80)
        n >>= 7
    return bytes(reversed(b))


def nota_midi(f):
    return int(round(69 + 12 * np.log2(f / 440.0)))


def monta_midi():
    ev = []  # (tick, ordem, bytes)
    for nome, (ch, prog, pulso, dur, vel, pan) in GM.items():
        ev.append((0, 0, bytes([0xC0 | ch, prog])))
        ev.append((0, 0, bytes([0xB0 | ch, 10, pan])))
        ev.append((0, 0, bytes([0xB0 | ch, 91, 70])))  # reverb
        ev.append((0, 0, bytes([0xB0 | ch, 7, 110])))
        entrada = VOZES[nome][2]
        for tau in np.arange(entrada, DUR - 0.5, pulso):
            f = float(freq_voz(nome, np.array([tau]))[0])
            n = nota_midi(f)
            on = int(tau * TICKS_S)
            off = int((tau + pulso * dur) * TICKS_S)
            ev.append((on, 1, bytes([0x90 | ch, n, vel])))
            ev.append((off, 0, bytes([0x80 | ch, n, 0])))
    ev.sort(key=lambda e: (e[0], e[1]))
    trk = bytearray()
    trk += vlq(0) + b"\xFF\x51\x03" + (500000).to_bytes(3, "big")  # 120 bpm
    ult = 0
    for tick, _, dados in ev:
        trk += vlq(tick - ult) + dados
        ult = tick
    trk += vlq(0) + b"\xFF\x2F\x00"
    MID.parent.mkdir(exist_ok=True)
    with open(MID, "wb") as f:
        f.write(b"MThd" + struct.pack(">IHHH", 6, 0, 1, TPQ))
        f.write(b"MTrk" + struct.pack(">I", len(trk)) + bytes(trk))


def gera_audio_orquestra():
    monta_midi()
    bruto = WAV_ORQ.with_suffix(".raw.wav")
    subprocess.run(["fluidsynth", "-ni", "-g", "1.0", "-r", "44100", "-T", "wav", "-F", str(bruto),
                    str(SF2), str(MID)], check=True, capture_output=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(bruto), "-t", str(DUR),
                    "-af", f"apad=whole_dur={DUR},afade=t=out:st={DUR - 3}:d=3,loudnorm=I=-18:TP=-2",
                    "-ar", "44100", "-ac", "2", str(WAV_ORQ)], check=True)
    bruto.unlink()


class SinfoniaOrquestra(Sinfonia):
    X_PAINEL = (0.45, 3.6, 5.3, 5.65)
    ENTRADAS = {n: v[2] for n, v in VOZES.items()}

    def prepara_audio(self):
        gera_audio_orquestra()
        return WAV_ORQ

    def rotulo_det(self, nome, o):
        return f"{VOZES[nome][0]} · mín:máx {o.om_min / o.om_max:.2f} · Kepler {o.kepler}"

    def freq_painel(self, nome, o, tt):
        return freq_voz(nome, tt)


if __name__ == "__main__":
    gera_audio_orquestra()
    print("ok", WAV_ORQ)
