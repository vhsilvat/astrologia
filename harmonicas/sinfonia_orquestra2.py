"""
MISTAGOGOS · "A harmonia do mundo", orquestra v2: o mesmo arranjo de sinfonia_orquestra.py
(cravo, dois violinos, viola e dois violoncelos, uma nota por pulso) com o relógio LINEAR.

Em sinfonia_orquestra.py o tempo acelera e, no fim, Mercúrio gira bem mais rápido que o cravo.
Aqui a taxa é constante e escolhida para que Mercúrio dê uma volta em VOLTA_MERCURIO segundos:
com o pulso do cravo de 0,5 s são 8 notas por volta, e a frase de Mercúrio se repete idêntica.

Uso: cd output && manim render -qh ../harmonicas/sinfonia_orquestra2.py SinfoniaOrquestra2
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sinfonia  # noqa: E402
import sinfonia_orquestra as base  # noqa: E402

AQUI = Path(__file__).resolve().parent
VOLTA_MERCURIO = 4.0  # s de vídeo por volta de Mercúrio (8 pulsos de 0,5 s)

periodo_anos = 2 * 3.141592653589793 / sinfonia.ORBITAS["Mercúrio"].n / 365.25
sinfonia.RATE0 = sinfonia.RATE1 = periodo_anos / VOLTA_MERCURIO  # anos simulados por segundo (linear)
base.MID = AQUI / "wav" / "sinfonia_orquestra2.mid"
base.WAV_ORQ = AQUI / "wav" / "sinfonia_orquestra2.wav"


class SinfoniaOrquestra2(base.SinfoniaOrquestra):
    pass


if __name__ == "__main__":
    print("taxa", sinfonia.RATE0, "anos/s; total", sinfonia.anos(sinfonia.DUR), "anos")
    base.gera_audio_orquestra()
