"""
MISTAGOGOS · "A harmonia do mundo", orquestra v3: 30 anos lineares, Mercúrio como voz contínua

Teste da opção A: o relógio é linear de 27/03/1996 a 27/03/2026 (0,67 ano por segundo), então
Mercúrio dá ~124 voltas e oscila ~2,8 vezes por segundo. Em vez de notas separadas, Mercúrio é
uma voz de coro (GM 52, Choir Aahs) numa nota única sustentada, com pitch bend contínuo que segue
f ∝ ω (faixa de 14,4 semitons, do Dó#4 ao Mi5). As outras cinco vozes são as de sinfonia_orquestra.py
(uma nota por segundo, no semitom de f ∝ ω).

Uso: cd output && manim render -qh ../harmonicas/sinfonia_orquestra3.py SinfoniaOrquestra3
"""

import struct
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sinfonia  # noqa: E402
import sinfonia_instrumentos as instr  # noqa: E402
import sinfonia_orquestra as base  # noqa: E402

ANOS_TOTAL = 30.0
sinfonia.RATE0 = sinfonia.RATE1 = ANOS_TOTAL / sinfonia.DUR  # tempo linear
instr.VOZES["Mercúrio"] = ("coro", 5, 16.0, 0.55, 0.55)  # uma oitava abaixo do cravo da v1

DUR, SR = sinfonia.DUR, sinfonia.SR
AQUI = Path(__file__).resolve().parent
MID3 = AQUI / "wav" / "sinfonia_orquestra3.mid"
WAV3 = AQUI / "wav" / "sinfonia_orquestra3.wav"
CANAL_MERC, PROG_CORO, PAN_MERC = 5, 52, 100
FAIXA_BEND = 24  # semitons para cada lado
PASSO_BEND = 0.005  # s entre eventos de pitch bend


def midi_exato(f):
    return 69 + 12 * np.log2(f / 440.0)


def eventos_mercurio():
    ev = []
    ch = CANAL_MERC
    entrada = instr.VOZES["Mercúrio"][2]
    ts = np.arange(entrada, DUR - 0.3, PASSO_BEND)
    f = instr.freq_voz("Mercúrio", ts)
    n0 = int(round(midi_exato(float(np.sqrt(f.min() * f.max())))))
    dev = midi_exato(f) - n0  # semitons
    assert np.abs(dev).max() < FAIXA_BEND
    ev.append((0, 0, bytes([0xC0 | ch, PROG_CORO])))
    ev.append((0, 0, bytes([0xB0 | ch, 10, PAN_MERC])))
    ev.append((0, 0, bytes([0xB0 | ch, 91, 70])))
    ev.append((0, 0, bytes([0xB0 | ch, 7, 110])))
    for cc, v in ((101, 0), (100, 0), (6, FAIXA_BEND), (38, 0), (101, 127), (100, 127)):  # RPN 0: faixa do bend
        ev.append((0, 0, bytes([0xB0 | ch, cc, v])))
    t0 = int(entrada * base.TICKS_S)
    ev.append((t0, 0, bytes([0xB0 | ch, 11, 0])))
    b0 = 8192 + int(round(dev[0] / FAIXA_BEND * 8192))
    ev.append((t0, 0, bytes([0xE0 | ch, b0 & 0x7F, b0 >> 7])))
    ev.append((t0, 1, bytes([0x90 | ch, n0, 100])))
    for tau, d in zip(ts, dev):
        tick = int(tau * base.TICKS_S)
        b = int(np.clip(8192 + round(d / FAIXA_BEND * 8192), 0, 16383))
        ev.append((tick, 0, bytes([0xE0 | ch, b & 0x7F, b >> 7])))
        ev.append((tick, 0, bytes([0xB0 | ch, 11, int(np.clip((tau - entrada) / 2.0, 0, 1) * 110)])))
    ev.append((int((DUR - 0.3) * base.TICKS_S), 0, bytes([0x80 | ch, n0, 0])))
    return ev


def monta_midi(so_mercurio=False):
    ev = eventos_mercurio()
    for nome, (ch, prog, pulso, dur, vel, pan) in base.GM.items():
        if nome == "Mercúrio" or so_mercurio:
            continue
        ev.append((0, 0, bytes([0xC0 | ch, prog])))
        ev.append((0, 0, bytes([0xB0 | ch, 10, pan])))
        ev.append((0, 0, bytes([0xB0 | ch, 91, 70])))
        ev.append((0, 0, bytes([0xB0 | ch, 7, 110])))
        for tau in np.arange(instr.VOZES[nome][2], DUR - 0.5, pulso):
            n = base.nota_midi(float(instr.freq_voz(nome, np.array([tau]))[0]))
            ev.append((int(tau * base.TICKS_S), 1, bytes([0x90 | ch, n, vel])))
            ev.append((int((tau + pulso * dur) * base.TICKS_S), 0, bytes([0x80 | ch, n, 0])))
    ev.sort(key=lambda e: (e[0], e[1]))
    trk = bytearray(base.vlq(0) + b"\xFF\x51\x03" + (500000).to_bytes(3, "big"))
    ult = 0
    for tick, _, dados in ev:
        trk += base.vlq(tick - ult) + dados
        ult = tick
    trk += base.vlq(0) + b"\xFF\x2F\x00"
    return b"MThd" + struct.pack(">IHHH", 6, 0, 1, base.TPQ) + b"MTrk" + struct.pack(">I", len(trk)) + bytes(trk)


def renderiza(mid_path, wav_path, dados):
    mid_path.write_bytes(dados)
    bruto = wav_path.with_suffix(".raw.wav")
    subprocess.run(["fluidsynth", "-ni", "-g", "1.0", "-r", "44100", "-T", "wav", "-F", str(bruto),
                    str(base.SF2), str(mid_path)], check=True, capture_output=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(bruto), "-t", str(DUR),
                    "-af", f"apad=whole_dur={DUR},afade=t=out:st={DUR - 3}:d=3,loudnorm=I=-18:TP=-2",
                    "-ar", str(SR), "-ac", "2", str(wav_path)], check=True)
    bruto.unlink()


def gera_audio():
    renderiza(MID3, WAV3, monta_midi())


class SinfoniaOrquestra3(base.SinfoniaOrquestra):
    def prepara_audio(self):
        gera_audio()
        return WAV3


if __name__ == "__main__":
    gera_audio()
    # teste: só Mercúrio, para conferir o glissando
    renderiza(AQUI / "wav" / "teste_mercurio.mid", AQUI / "wav" / "teste_mercurio.wav", monta_midi(so_mercurio=True))
    print("ok")
