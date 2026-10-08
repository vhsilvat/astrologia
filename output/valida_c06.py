#!/usr/bin/env python3
"""MISTAGOGOS · validação pixel a pixel — c06 As Consonâncias (timeline quantizada).

Uso: python valida_c06.py [caminho/do/video.mp4]
Reconstrói a timeline quantizada do script (ceil(d·fps)/fps por segmento)
e deriva todas as janelas — vale para -ql (15 fps) e -qh (60 fps).
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
    "media/videos/v01_c06_consonancias/480p15/Consonancias.mp4")
FRAMES = "/tmp/frames_c06"

FG = (235, 219, 178)
YELLOW = (250, 189, 47)
RED = (204, 36, 29)
AQUA = (142, 192, 124)
ORANGE = (254, 128, 25)
GREEN = (184, 187, 38)
BLUE = (131, 165, 152)
GRAY = (168, 153, 132)
NEUT = (124, 111, 100)

W_U = 14.222222
H_U = 8.0
Y_STR = 0.40
BEAD_Y = 0.50
PARK_UX = 5.8
Y_REG = -1.75

SEGS = []
IDX = {}


def add(nome, durs):
    if nome:
        IDX[nome] = (len(SEGS), len(durs))
    SEGS.extend(durs)


add("cab", [0.8, 1.0])
add("pinos", [0.5])
add("lbl", [0.6])
add("d220", [0.12, 1.3, 0.5])
add("pos220", [3.6])
add("mord8", [0.9])
add("d330", [0.12, 1.2, 0.5])
add("no8", [0.3])
add("t330", [0.7])
add("pos330", [5.4])
add("mord9", [0.85])
add("d293", [0.12, 1.2, 0.5])
add("no9", [0.3])
add("t293", [0.7])
add("pos293", [4.9])
add("fracin", [1.0])
add("circ", [1.2])
add("epo", [0.6])
add("posep", [7.2])
add("out1", [0.6])
add("reset", [0.8])
add("regin", [0.8])
add("arco1", [0.9])
add("posr1", [2.4])
add("arco2", [0.9])
add("posr2", [3.4])
add("wave", [1.6])
add("fin", [1.0])
add("fim", [2.6])


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
    return (g.gx(-3.3), g.fy(-1.90), g.gx(3.3), g.fy(-2.60))


def pino_box(g, lado):
    x = -5.0 if lado == "L" else 5.0
    return (g.gx(x - 0.15), g.fy(0.52), g.gx(x + 0.15), g.fy(0.28))


RESULTS = []


def check(nome, ok, detail=""):
    RESULTS.append(ok)
    print("%-4s %-40s %s" % ("PASS" if ok else "FAIL", nome, detail))


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
    print("fps: %d · video: %.3f s · modelo: %.3f s" % (fps, dur, total))
    check("duracao = timeline modelo", abs(dur - total) <= 0.35,
          "video %.2f · modelo %.2f" % (dur, total))
    check("audio aac presente", probe_audio())

    g = Grid(mid("lbl", 0))
    check("corda reta + pinos nas pontas",
          g.has(str_box(g, 0.05, 0.45), FG, 45, 20)
          and g.has(pino_box(g, "L"), FG, 45, 3)
          and g.has(pino_box(g, "R"), FG, 45, 3))

    g = Grid(mid("pos220", 0))
    check("cabecalho aqua",
          g.has((g.gx(-4.5), g.fy(3.7), g.gx(4.5), g.fy(3.0)), AQUA, 45, 5))
    check("rotulo La·220 verde + raz 12/12",
          g.has(nota_box(g), GREEN, 45, 5) and g.has(raz_box(g), FG, 45, 5))
    r = ringwin("d220")
    check("corda inteira vibrando",
          vibrando([r[0] + 0.4, r[0] + 0.8, r[0] + 1.2], 0.2, 0.8))

    g = Grid(mid("pos330", 0))
    check("aresta mordendo 2/3 (Diapente)",
          g.has(bite_box(g, 2.0 / 3.0), YELLOW, 45, 3))
    check("conta vermelha em 2/3",
          g.has(bead_box(g, 2.0 / 3.0), RED, 45, 2))
    check("rotulo Mi4 laranja + 8/12",
          g.has(nota_box(g), ORANGE, 45, 5) and g.has(raz_box(g), FG, 45, 5))
    r = ringwin("d330")
    check("quinta vibrando (0 a 2/3)",
          vibrando([r[0] + 0.3, r[0] + 0.7, r[0] + 1.1], 0.05, 0.60))
    g2 = Grid(r[0] + 0.6)
    check("lado direito dampado (apos 2/3)",
          g2.absent((g2.fx(0.73), g2.fy(Y_STR + 0.10),
                     g2.fx(0.95), g2.fy(Y_STR - 0.10)), FG))

    g = Grid(mid("pos293", 0))
    check("aresta mordendo 3/4 (Diatessaron)",
          g.has(bite_box(g, 0.75), YELLOW, 45, 3))
    check("conta vermelha em 3/4",
          g.has(bead_box(g, 0.75), RED, 45, 2))
    check("rotulo Re4 aqua + 9/12",
          g.has(nota_box(g), AQUA, 45, 5) and g.has(raz_box(g), FG, 45, 5))
    r = ringwin("d293")
    check("quarta vibrando (0 a 3/4)",
          vibrando([r[0] + 0.3, r[0] + 0.7, r[0] + 1.1], 0.05, 0.70))
    g2 = Grid(r[0] + 0.6)
    check("lado direito dampado (apos 3/4)",
          g2.absent((g2.fx(0.80), g2.fy(Y_STR + 0.10),
                     g2.fx(0.95), g2.fy(Y_STR - 0.10)), FG))

    g = Grid(mid("posep", 0))
    check("fracao 3/2 laranja",
          g.has((g.gx(-2.6), g.fy(2.75), g.gx(-0.8), g.fy(1.45)),
                ORANGE, 45, 4))
    check("fracao 4/3 aqua",
          g.has((g.gx(-1.0), g.fy(2.75), g.gx(0.5), g.fy(1.45)),
                AQUA, 45, 4))
    check("fracao 9/8 amarela",
          g.has((g.gx(0.5), g.fy(2.75), g.gx(2.2), g.fy(1.45)),
                YELLOW, 45, 4))
    check("Epogdoon — o tom inteiro",
          g.has((g.gx(-3.0), g.fy(1.6), g.gx(3.0), g.fy(1.0)), FG, 45, 4))

    g = Grid(mid("posr2", 0))
    check("regua na altura Y_REG",
          g.has((g.gx(-5.0), g.fy(-1.68), g.gx(5.0), g.fy(-1.82)),
                FG, 45, 20))
    check("Marte vermelho",
          g.has((g.gx(0.8), g.fy(-1.60), g.gx(1.2), g.fy(-1.90)),
                RED, 45, 3))
    check("Plutao neutro",
          g.has((g.gx(3.8), g.fy(-1.60), g.gx(4.2), g.fy(-1.90)),
                NEUT, 35, 3))
    check("Urano azul",
          g.has((g.gx(-1.2), g.fy(-1.60), g.gx(-0.8), g.fy(-1.90)),
                BLUE, 40, 3))
    check("Mercurio cinza",
          g.has((g.gx(-4.2), g.fy(-1.60), g.gx(-3.8), g.fy(-1.90)),
                GRAY, 40, 3))
    check("arco 1 acima da regua",
          g.has((g.gx(-3.9), g.fy(-1.25), g.gx(-1.1), g.fy(-1.62)),
                YELLOW, 45, 3))
    check("arco 2 acima da regua",
          g.has((g.gx(1.1), g.fy(-1.25), g.gx(3.9), g.fy(-1.62)),
                YELLOW, 45, 3))
    check("rotulos 2:1 amarelos",
          g.has((g.gx(-2.9), g.fy(-0.75), g.gx(-2.1), g.fy(-1.00)),
                YELLOW, 45, 3)
          and g.has((g.gx(2.1), g.fy(-0.75), g.gx(2.9), g.fy(-1.00)),
                    YELLOW, 45, 3))
    check("caption as oitavas superiores",
          g.has((g.gx(-2.5), g.fy(-2.85), g.gx(2.5), g.fy(-3.25)),
                YELLOW, 45, 4))
    check("aresta estacionada no park",
          g.has(park_box(g), YELLOW, 45, 3))
    check("corda reta durante a regua",
          g.has(str_box(g, 0.1, 0.9), FG, 45, 20))
    check("cabecalho persiste",
          g.has((g.gx(-4.5), g.fy(3.7), g.gx(4.5), g.fy(3.0)),
                AQUA, 45, 5))

    g = Grid(mid("fim", 0))
    check("tela limpa — sem FG",
          g.absent((0, 0, g.w, g.h), FG))
    check("tela limpa — sem amarelo",
          g.absent((0, 0, g.w, g.h), YELLOW))
    check("tela limpa — sem vermelho",
          g.absent((0, 0, g.w, g.h), RED))

    print()
    n_ok = sum(RESULTS)
    print("RESULTADO: %d/%d checks" % (n_ok, len(RESULTS)))
    sys.exit(0 if n_ok == len(RESULTS) else 1)


if __name__ == "__main__":
    main()
