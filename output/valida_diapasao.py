#!/usr/bin/env python3
"""MISTAGOGOS · validação pixel a pixel — O Diapasão corrigido (v2).

O render do Manim quantiza cada play/wait para um número inteiro de
frames (ceil(d·fps)/fps por segmento): em -ql (15 fps) os eventos correm
até ~1,3 s depois dos tempos nominais do script — os 3 FAILs do v1 eram
falsos alarmes por amostragem em tempos nominais. Esta versão reconstrói
a timeline QUANTIZADA a partir da lista de segmentos do script e deriva
dela TODAS as janelas de amostragem — vale igualmente para -ql (15 fps)
e -qh (60 fps, desvio ~+0,05 s).

Uso: python valida_diapasao.py [caminho/do/video.mp4]
"""
import math
import os
import re
import shutil
import subprocess
import sys
from fractions import Fraction

import numpy as np
from PIL import Image

VID = sys.argv[1] if len(sys.argv) > 1 else (
    "media/videos/da_forja_ao_diapasao/480p15/Diapasao.mp4")
FRAMES = "/tmp/frames_dia"

# ———— Gruvbox (RGB) ————
FG = (235, 219, 178)
YELLOW = (250, 189, 47)
RED = (204, 36, 29)
AQUA = (142, 192, 124)
ORANGE = (254, 128, 25)
GREEN = (184, 187, 38)
DARK = (60, 56, 51)

W_U = 14.222222
H_U = 8.0
Y_STR = 0.40
BEAD_Y = 0.50
PARK_UX = 5.8

# ———— Timeline quantizada (espelha o script segmento a segmento) ————
GOLPE = [0.20, 0.15, 0.12, 0.55]

SEGS = []
IDX = {}


def add(nome, durs):
    if nome:
        IDX[nome] = (len(SEGS), len(durs))
    SEGS.extend(durs)


add("cab", [1.0, 1.4])                    # FadeIn cabeçalho · wait
add("forja", [0.9, 1.6])                  # chão+bigorna · wait
add("martelos", [0.8, 2.2])               # m1+m2 · wait
add("g1", GOLPE)                          # golpe 12 lb (rot_f)
add("posg1", [2.6])
add("g2", GOLPE)                          # golpe 6 lb (rot_2f)
add("posg2", [2.6])
add("gd", GOLPE)                          # golpe duplo
add("posgd", [2.0])
add("cartaz", [0.9, 3.6])                 # cartaz 12:6 · wait
add("gd2", GOLPE)                         # golpe duplo
add("posgd2", [4.4])
add("trans", [0.8, 1.6])                  # rótulos out · cartaz→aresta · wait
add("repl", [1.0, 0.4])                   # martelos→pinos · bigorna→aresta · wait
add("corda", [1.1])                       # pinos às pontas · corda · aresta→PARK
add("precord", [0.9])                     # wait
add("lbl", [0.6, 0.4])                    # nota/raz · wait
add("d220", [0.12, 1.5, 0.5])             # rampa · ring · decay
add("pos220", [2.8])
add("mord", [1.0])                        # aresta morde 6/12
add("no12", [0.3, 0.3])                   # conta · wait
add("d440", [0.12, 1.3, 0.5])             # rampa · ring · decay
add("pos440", [1.8])
add("t440", [0.7, 2.4])                   # troca · wait
add("m13", [0.85, 0.2])                   # aresta→1/3 · wait
add("d660", [0.12, 1.2, 0.5])             # rampa · ring · decay
add("n13", [0.3, 1.6])                    # contas 1/3·2/3 · wait
add("t660", [0.7, 2.2])                   # troca · wait
add("m14", [0.8])                         # aresta→1/4
add("d880", [0.12, 1.1, 0.5])             # rampa · ring · decay
add("n14", [0.3, 1.4])                    # contas 1/4·3/4 · wait
add("t880", [0.7, 2.0])                   # troca · wait
add("fimmod", [1.2, 0.5])                 # aresta recolhe · wait
add("modos", [0.1, 0.55, 0.8, 0.6, 0.8, 0.7, 1.0])
add("saltos", [0.8, 2.0])                 # frase · wait
add("serie", [2.2, 2.4])                  # conjunto · wait
add("mundi", [1.0, 4.0])                  # Harmonia Mundi · wait
add("fim", [0.6, 0.9, 3.0])               # amp→0 · fades · wait final


# ———— Probes ————
def probe_video():
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries",
         "stream=duration,avg_frame_rate,codec_name,width,height",
         "-of", "default=noprint_wrappers=1", VID],
        capture_output=True, text=True, check=True).stdout
    dur = float(re.search(r"^duration=([0-9.]+)", out, re.M).group(1))
    rate = re.search(r"^avg_frame_rate=(\S+)", out, re.M).group(1)
    fps = round(float(Fraction(rate)))
    return dur, fps


def probe_audio():
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0",
         "-show_entries", "stream=codec_name", "-of",
         "default=noprint_wrappers=1", VID],
        capture_output=True, text=True, check=True).stdout
    return "aac" in out


# ———— Frames ————
shutil.rmtree(FRAMES, ignore_errors=True)
os.makedirs(FRAMES, exist_ok=True)


def grab(t):
    path = os.path.join(FRAMES, "f_%06d.png" % int(round(t * 1000)))
    if not os.path.exists(path):
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-ss", "%.3f" % t, "-i", VID,
             "-frames:v", "1", path],
            check=True, capture_output=True)
    return path


class Grid:
    def __init__(self, t):
        self.t = t
        self.im = Image.open(grab(t)).convert("RGB")
        self.w, self.h = self.im.size
        self.px = self.w / W_U
        self.py = self.h / H_U

    def gx(self, ux):
        return (ux + W_U / 2.0) * self.px

    def fy(self, uy):
        return (H_U / 2.0 - uy) * self.py

    def fx(self, frac):
        return self.gx(-5.0 + 10.0 * frac)

    def has(self, box, color, tol=45, min_px=2):
        x0, x1 = sorted((int(round(box[0])), int(round(box[2]))))
        y0, y1 = sorted((int(round(box[1])), int(round(box[3]))))
        x0, y0 = max(x0, 0), max(y0, 0)
        x1, y1 = min(x1, self.w), min(y1, self.h)
        if x1 <= x0 or y1 <= y0:
            return False
        arr = np.asarray(self.im.crop((x0, y0, x1, y1)), dtype=np.int16)
        cr, cg, cb = color
        mask = ((np.abs(arr[..., 0] - cr) <= tol)
                & (np.abs(arr[..., 1] - cg) <= tol)
                & (np.abs(arr[..., 2] - cb) <= tol))
        return int(mask.sum()) >= min_px

    def absent(self, box, color, tol=35):
        return not self.has(box, color, tol=tol, min_px=1)

    def displaced(self, u0, u1):
        """FG a >=0.13 un. da linha de repouso, na faixa fx(u0)..fx(u1)."""
        up = (self.fx(u0), self.fy(Y_STR + 0.62),
              self.fx(u1), self.fy(Y_STR + 0.13))
        dn = (self.fx(u0), self.fy(Y_STR - 0.13),
              self.fx(u1), self.fy(Y_STR - 0.62))
        return self.has(up, FG, 45, 2) or self.has(dn, FG, 45, 2)


def vibrando(ts, u0, u1):
    return any(Grid(t).displaced(u0, u1) for t in ts)


def park_box(g):
    return (g.gx(PARK_UX - 0.35), g.fy(0.45),
            g.gx(PARK_UX + 0.35), g.fy(-0.15))


def bite_box(g, frac):
    cx = g.fx(frac)
    return (cx - 0.35 * g.px, g.fy(0.48),
            cx + 0.35 * g.px, g.fy(0.02))


def bead_box(g, frac):
    cx = g.fx(frac)
    return (cx - 0.12 * g.px, g.fy(BEAD_Y + 0.08),
            cx + 0.12 * g.px, g.fy(BEAD_Y - 0.08))


def str_box(g, u0, u1):
    return (g.fx(u0), g.fy(Y_STR + 0.07), g.fx(u1), g.fy(Y_STR - 0.07))


def nota_box(g):
    return (g.gx(-2.4), g.fy(-1.15), g.gx(2.4), g.fy(-1.95))


def raz_box(g):
    return (g.gx(-2.6), g.fy(-1.90), g.gx(2.6), g.fy(-2.60))


def pino_box(g, lado):
    x = -5.0 if lado == "L" else 5.0
    return (g.gx(x - 0.15), g.fy(0.52), g.gx(x + 0.15), g.fy(0.28))


RESULTS = []


def check(nome, ok, detail=""):
    RESULTS.append(ok)
    print("%-4s %-38s %s" % ("PASS" if ok else "FAIL", nome, detail))


def main():
    dur, fps = probe_video()
    cum = []
    t = 0.0
    for d in SEGS:
        t += math.ceil(d * fps - 1e-9) / fps
        cum.append(t)
    total = cum[-1]

    def mid(nome, k):
        i0, n = IDX[nome]
        a = cum[i0 + k - 1] if i0 + k > 0 else 0.0
        return a + 0.5 * (cum[i0 + k] - a)

    def ringwin(nome):
        i0, n = IDX[nome]
        return (cum[i0], cum[i0 + 1])

    print("video:", VID)
    print("fps detectado: %d · duração do vídeo: %.3f s · timeline modelo: %.3f s"
          % (fps, dur, total))
    check("duração = timeline modelo", abs(dur - total) <= 0.35,
          "vídeo %.2f s · modelo %.2f s" % (dur, total))
    check("áudio aac presente", probe_audio())

    # ———— forja ————
    g = Grid(mid("martelos", 1))
    check("bigorna (corpo escuro)",
          g.has((g.gx(-1.0), g.fy(-1.05), g.gx(1.0), g.fy(-1.85)),
                DARK, 12, 40))
    check("martelos 12/6 erguidos",
          g.has((g.gx(-1.05), g.fy(0.98), g.gx(-0.05), g.fy(0.50)), FG, 45, 20)
          and g.has((g.gx(0.02), g.fy(0.90), g.gx(0.68), g.fy(0.52)),
                    YELLOW, 45, 10))
    g = Grid(mid("posg2", 0))
    check("rótulos da forja (verde+amarelo)",
          g.has((g.gx(-5.45), g.fy(-2.48), g.gx(-4.15), g.fy(-3.12)),
                GREEN, 45, 5)
          and g.has((g.gx(4.15), g.fy(-2.48), g.gx(5.45), g.fy(-3.12)),
                    YELLOW, 45, 5))
    g = Grid(mid("cartaz", 1))
    check("cartaz 12:6",
          g.has((g.gx(-1.7), g.fy(-2.68), g.gx(1.7), g.fy(-3.62)), FG, 45, 10))

    # ———— 12/12 · aresta estacionada (P1) ————
    g = Grid(mid("lbl", 1))
    check("corda reta + pinos nas pontas",
          g.has(str_box(g, 0.05, 0.45), FG, 45, 20)
          and g.has(pino_box(g, "L"), FG, 45, 3)
          and g.has(pino_box(g, "R"), FG, 45, 3))
    check("aresta estacionada à direita (P1)",
          g.has(park_box(g), YELLOW, 45, 3))
    check("centro livre em 12/12 (P1)",
          g.absent(bite_box(g, 0.5), YELLOW))
    check("rótulo verde Lá 220", g.has(nota_box(g), GREEN, 45, 5))
    check("rótulo 12/12 corda inteira", g.has(raz_box(g), FG, 45, 5))
    r = ringwin("d220")
    check("corda inteira vibrando",
          vibrando([r[0] + 0.4, r[0] + 0.8, r[0] + 1.2], 0.2, 0.8))

    # ———— mordida 6/12 ————
    g = Grid(mid("no12", 1))
    check("aresta mordendo no centro (6/12)",
          g.has(bite_box(g, 0.5), YELLOW, 45, 3))
    check("conta vermelha sobre a corda (P5)",
          g.has(bead_box(g, 0.5), RED, 45, 2))
    check("metade direita dampada",
          g.absent((g.fx(0.58), g.fy(Y_STR + 0.10),
                    g.fx(0.95), g.fy(Y_STR - 0.10)), FG))
    r = ringwin("d440")
    check("metade esquerda vibrando",
          vibrando([r[0] + 0.45, r[0] + 0.85, r[0] + 1.25], 0.05, 0.45))
    g = Grid(mid("t440", 1))
    check("rótulos Lá⁴ 440 e 6/12",
          g.has(nota_box(g), YELLOW, 45, 5)
          and g.has(raz_box(g), FG, 45, 5))

    # ———— 4/12 ————
    g = Grid(mid("m13", 1))
    check("aresta no terço (4/12)", g.has(bite_box(g, 1 / 3), YELLOW, 45, 3))
    r = ringwin("d660")
    check("terço vibrando",
          vibrando([r[0] + 0.4, r[0] + 0.8], 0.05, 0.28))
    g = Grid(mid("n13", 1))
    check("contas em 1/3 e 2/3",
          g.has(bead_box(g, 1 / 3), RED, 45, 2)
          and g.has(bead_box(g, 2 / 3), RED, 45, 2))
    g = Grid(mid("t660", 1))
    check("rótulo Mi⁵ 660 (laranja)", g.has(nota_box(g), ORANGE, 45, 5))

    # ———— 3/12 ————
    r = ringwin("d880")
    g = Grid(r[0] + 0.3)
    check("aresta no quarto (3/12)", g.has(bite_box(g, 0.25), YELLOW, 45, 3))
    check("quarto vibrando",
          vibrando([r[0] + 0.2, r[0] + 0.6, r[0] + 1.0], 0.02, 0.22))
    g = Grid(mid("n14", 1))
    check("contas em 1/4 e 3/4",
          g.has(bead_box(g, 0.25), RED, 45, 2)
          and g.has(bead_box(g, 0.75), RED, 45, 2))
    g = Grid(mid("t880", 1))
    check("rótulo Lá⁵ 880 (aqua)", g.has(nota_box(g), AQUA, 45, 5))

    # ———— modos ————
    t3 = mid("modos", 4)
    check("modo 3 vibrando",
          vibrando([t3 - 0.2, t3, t3 + 0.2], 0.36, 0.64))
    g = Grid(t3)
    check("aresta recolhida nos modos",
          g.has(park_box(g), YELLOW, 45, 3)
          and g.absent(bite_box(g, 0.5), YELLOW))
    t4 = mid("modos", 6)
    check("modo 4 vibrando (lobos internos)",
          vibrando([t4 - 0.2, t4], 0.30, 0.45)
          and vibrando([t4 - 0.2, t4], 0.55, 0.70))

    # ———— saltos · série · mundi ————
    g = Grid(mid("saltos", 1))
    check("frase dos saltos sucessivos",
          g.has((g.gx(-3.3), g.fy(-2.75), g.gx(3.3), g.fy(-3.35)), FG, 45, 5))
    g = Grid(mid("serie", 1))
    check("série harmônica (nota+rótulo)",
          g.has(nota_box(g), YELLOW, 45, 5)
          and g.has(raz_box(g), FG, 45, 5))
    g = Grid(mid("mundi", 1))
    check("Harmonia Mundi",
          g.has((g.gx(-3.3), g.fy(-2.25), g.gx(3.3), g.fy(-3.15)),
                YELLOW, 45, 8))

    # ———— âncora final (M1) ————
    g = Grid(mid("fim", 2))
    check("corda e pinos permanecem (M1)",
          g.has(str_box(g, 0.1, 0.9), FG, 45, 20)
          and g.has(pino_box(g, "L"), FG, 45, 3)
          and g.has(pino_box(g, "R"), FG, 45, 3))
    check("aresta estacionada no fim",
          g.has(park_box(g), YELLOW, 45, 3)
          and g.absent(bite_box(g, 0.5), YELLOW))
    check("contas desapareceram",
          g.absent((g.gx(-3.0), g.fy(0.72), g.gx(3.0), g.fy(0.30)), RED))
    check("textos desapareceram",
          g.absent((g.gx(-3.3), g.fy(-0.60), g.gx(3.3), g.fy(-3.40)), FG)
          and g.absent((g.gx(-3.3), g.fy(-0.60), g.gx(3.3), g.fy(-3.40)),
                       YELLOW))

    print()
    n_ok = sum(RESULTS)
    print("RESULTADO: %d/%d checks" % (n_ok, len(RESULTS)))
    sys.exit(0 if n_ok == len(RESULTS) else 1)


if __name__ == "__main__":
    main()
