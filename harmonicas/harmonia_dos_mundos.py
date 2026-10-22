"""
MISTAGOGOS · A harmonia dos mundos
T4 · "O céu e o estudo que o testa" · Kepler, Harmonices Mundi, livro V (1619)

O tempo passa no sistema solar (vista de cima, ângulos reais) e cada planeta
"canta" a sua velocidade angular heliocêntrica: quanto mais rápido gira visto
do Sol, mais agudo o som. É a definição de Kepler (livro V, cap. 4 a 9): a
altura segue o movimento aparente visto do Sol, entre o afélio (nota mais
grave do planeta) e o periélio (a mais aguda), de modo contínuo, sem saltos.

  MEDÍVEL        velocidades angulares (efemérides VSOP87, via PyEphem)
  INTERPRETÁVEL  a leitura dessas velocidades como altura de som (Kepler, 1619)

Escolhas (todas explícitas, para o Victor mudar se quiser):
  - Referência de altura: o afélio de Saturno (o movimento mais lento de todos)
    é o Sol grave, 98 Hz (G2); os outros planetas guardam a razão exata com
    ele e são transpostos por oitavas inteiras para caber numa orquestra.
    Isto é o que o próprio Kepler faz (Saturno G, Júpiter B...) e o que o
    programa de Christopher Arthur faz (98,12 Hz para o movimento de Saturno).
  - Vozes na ordem de Kepler (V.8): Saturno e Júpiter baixo, Marte tenor,
    Terra e Vênus contralto, Mercúrio soprano.
  - Os seis "instrumentos" são síntese aditiva de cordas (conjunto de
    violinos, violas, violoncelos e contrabaixos com vibrato), não amostras.
  - Distâncias do desenho comprimidas em escala logarítmica; ângulos reais.
  - O tempo acelera de 8 dias/s no começo a 36 dias/s depois dos 50 s.

Dependências: manim, numpy, scipy, ephem (PyEphem; VSOP87).
Render: manim render -ql harmonicas/harmonia_dos_mundos.py HarmoniaDosMundos
        manim render -qh harmonicas/harmonia_dos_mundos.py HarmoniaDosMundos
Para gerar só o áudio: python3 harmonicas/harmonia_dos_mundos.py

Paleta Gruvbox · EB Garamond
"""

from __future__ import annotations

import datetime as dt
import math
import os
from pathlib import Path

import numpy as np

# ———— Paleta Gruvbox ————
GRUV_BG = "#282828"
GRUV_FG = "#ebdbb2"
GRUV_YELLOW = "#fabd2f"
GRUV_GREEN = "#b8bb26"
GRUV_ORANGE = "#fe8019"
GRUV_AQUA = "#8ec07c"
GRUV_RED = "#fb4934"
GRUV_BLUE = "#83a598"
GRUV_PURPLE = "#d3869b"
GRUV_GRAY = "#a89984"
GRUV_NEUT = "#7c6f64"
GRUV_DARK = "#3c3833"
GRUV_BLACK = "#1d2021"

FONT = "EB Garamond"
AQUI = Path(__file__).resolve().parent
SONS = AQUI / "sons"
WAV = SONS / "harmonia_dos_mundos.wav"

# ———— Tempo ————
DUR = 90.0                 # segundos de vídeo
DATA_INICIO = dt.date(2026, 10, 22)
EPH_INICIO = "2026/10/22"  # mesma data, no formato do PyEphem
T_LENTO, T_RAMPA = 20.0, 50.0   # até 20 s: lento; rampa até 50 s; depois constante
R_LENTO, R_RAPIDO = 8.0, 36.0   # dias de calendário por segundo de vídeo
CAUDA_ANTES = 2700.0       # dias de história que as caudas precisam antes do início

# ———— Altura ————
F_G = 97.9989              # Hz, o G grave de Saturno no afélio (A4 = 440)

# ———— Planetas, na ordem de Kepler: do baixo ao soprano ————
# k = quantas oitavas descer a nota que sai da razão direta com Saturno;
# entra = instante (s) em que o planeta aparece e a voz entra;
# razao = intervalo afélio:periélio que Kepler assinala (livro V, cap. 6 e 9).
PLANETAS = [
    dict(id="Saturn", nome="Saturno", cor=GRUV_PURPLE, voz="baixo", razao="4:5",
         per=10759.2, passo=2.0, k=0, entra=1.5, fc=650, harm=22, gan=1.00,
         pan=+0.35, copias=(-4, 4), vib=(4.6, 3.0), sub=0.30),
    dict(id="Jupiter", nome="Júpiter", cor=GRUV_ORANGE, voz="baixo", razao="5:6",
         per=4332.6, passo=1.0, k=0, entra=5.0, fc=1100, harm=18, gan=0.85,
         pan=+0.20, copias=(-5, 0, 5), vib=(4.9, 4.0)),
    dict(id="Mars", nome="Marte", cor=GRUV_RED, voz="tenor", razao="2:3",
         per=687.0, passo=0.5, k=2, entra=8.5, fc=1700, harm=14, gan=0.70,
         pan=+0.05, copias=(-6, 0, 6), vib=(5.3, 5.0)),
    dict(id="Earth", nome="Terra", cor=GRUV_BLUE, voz="contralto", razao="15:16",
         per=365.26, passo=0.5, k=2, entra=12.0, fc=2400, harm=12, gan=0.55,
         pan=-0.20, copias=(-7, 0, 7), vib=(5.5, 6.0)),
    dict(id="Venus", nome="Vênus", cor=GRUV_YELLOW, voz="contralto", razao="24:25",
         per=224.7, passo=0.5, k=3, entra=15.5, fc=2400, harm=12, gan=0.55,
         pan=-0.35, copias=(-7, 0, 7), vib=(5.7, 6.0)),
    dict(id="Mercury", nome="Mercúrio", cor=GRUV_AQUA, voz="soprano", razao="5:12",
         per=88.0, passo=0.25, k=3, entra=19.0, fc=2400, harm=9, gan=0.30,
         pan=-0.50, copias=(-8, 0, 8), vib=(6.0, 7.0)),
]

MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


# ═════════════════════════════ tempo ═════════════════════════════
def dias(t):
    """Dias de calendário decorridos após DATA_INICIO no instante t (s) do vídeo."""
    t = np.asarray(t, dtype=float)
    r0, r1 = R_LENTO, R_RAPIDO
    a = r0 * np.minimum(t, T_LENTO)
    u = np.clip(t - T_LENTO, 0.0, T_RAMPA - T_LENTO)
    b = r0 * u + 0.5 * (r1 - r0) * u * u / (T_RAMPA - T_LENTO)
    c = r1 * np.maximum(t - T_RAMPA, 0.0)
    return a + b + c


def taxa(t):
    t = float(t)
    if t <= T_LENTO:
        return R_LENTO
    if t >= T_RAMPA:
        return R_RAPIDO
    return R_LENTO + (R_RAPIDO - R_LENTO) * (t - T_LENTO) / (T_RAMPA - T_LENTO)


def smooth(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


# ═════════════════════════════ efemérides ═════════════════════════════
def _helio(nome, d):
    import ephem
    if nome == "Earth":
        s = ephem.Sun(d)
        return math.degrees(s.hlon), s.earth_distance
    b = getattr(ephem, nome)(d)
    return math.degrees(b.hlon), b.sun_distance


def _serie(nome, d_ini, d_fim, passo):
    """(dias relativos a EPH_INICIO, longitude heliocêntrica desenrolada em rad, r em UA)."""
    import ephem
    d0 = ephem.Date(EPH_INICIO)
    t = np.arange(d_ini, d_fim + passo, passo)
    lon = np.empty(len(t))
    r = np.empty(len(t))
    for i, x in enumerate(t):
        lon[i], r[i] = _helio(nome, ephem.Date(d0 + x))
    return t, np.unwrap(np.radians(lon)), r


class Efemerides:
    """Tabelas VSOP87 (PyEphem) com splines cúbicas: posição e velocidade angular."""

    def __init__(self):
        from scipy.interpolate import CubicSpline

        self.d_fim = float(dias(DUR)) + 60.0
        self.lon, self.r, self.w = [], [], []
        self.faixa = []          # (w_afélio, w_periélio) numa órbita inteira, rad/dia
        self.anel = []           # (lon, r) de uma órbita, para desenhar o caminho
        for p in PLANETAS:
            t, lon, r = _serie(p["id"], -CAUDA_ANTES, self.d_fim, p["passo"])
            sl = CubicSpline(t, lon)
            self.lon.append(sl)
            self.r.append(CubicSpline(t, r))
            self.w.append(sl.derivative())
            # uma órbita inteira, a partir de 2016/01/01, para as extremas de ω
            import ephem
            d_a = float(ephem.Date("2016/01/01") - ephem.Date(EPH_INICIO))
            ts, ls, rs = _serie(p["id"], d_a, d_a + 1.03 * p["per"], p["passo"])
            ss = CubicSpline(ts, ls)
            fino = np.linspace(ts[2], ts[-3], 6000)
            ww = ss.derivative()(fino)
            self.faixa.append((float(ww.min()), float(ww.max())))
            # anel de uma volta (para desenhar a órbita)
            tt = np.linspace(ts[0], ts[0] + p["per"], 361)
            self.anel.append((np.mod(ss(tt), 2 * np.pi), CubicSpline(ts, rs)(tt)))
        self.w_sat_min = self.faixa[0][0]   # o movimento mais lento: Saturno no afélio

    # frequência da voz (Hz) a partir de ω
    def f_de_w(self, i, w):
        k = PLANETAS[i]["k"]
        return F_G * (w / self.w_sat_min) * 2.0 ** (-k)

    def f_voz(self, i, d):
        return self.f_de_w(i, self.w[i](d))

    def faixa_hz(self, i):
        a, b = self.faixa[i]
        return self.f_de_w(i, a), self.f_de_w(i, b)


_EF = None


def efem():
    global _EF
    if _EF is None:
        _EF = Efemerides()
    return _EF


# ═════════════════════════════ áudio ═════════════════════════════
SR = 44100


def _lento(N, taxa_hz, rng):
    """Ruído suave (interpolação cúbica) com 'taxa_hz' pontos por segundo."""
    from scipy.interpolate import CubicSpline
    n = int(N / SR * taxa_hz) + 4
    pts = rng.standard_normal(n)
    return CubicSpline(np.arange(n), pts)(np.linspace(0, n - 3, N))


def _corpo(f):
    """Ressonâncias de corpo de madeira: realces suaves perto de 280, 550 e 1100 Hz."""
    g = 1.0
    for fc, larg, alt in ((280.0, 0.35, 0.6), (550.0, 0.40, 0.5), (1100.0, 0.45, 0.5)):
        g = g + alt * np.exp(-(np.log2(np.maximum(f, 20.0) / fc) ** 2) / (2 * larg ** 2))
    return g


def _voz(f_base, p, rng):
    """Uma voz de cordas: 'copias' desafinadas, vibrato, deriva lenta, harmônicos até p['harm']."""
    N = len(f_base)
    t = np.arange(N) / SR
    sair = smooth((DUR - t) / 6.0)
    ent = smooth((t - p["entra"]) / 2.6)
    env = ent * sair * (1.0 + 0.07 * _lento(N, 0.5, rng))
    vib_hz, vib_c = p["vib"]
    vib_rampa = smooth((t - p["entra"] - 1.0) / 2.5)
    L = np.zeros(N)
    R = np.zeros(N)
    cop = p["copias"]
    for j, cents in enumerate(cop):
        vf = vib_hz * (1 + 0.06 * (j - 1))
        vib = vib_c * vib_rampa * np.sin(2 * np.pi * vf * t + rng.uniform(0, 2 * np.pi))
        deriva = 2.5 * _lento(N, 0.6, rng)
        fc = f_base * 2.0 ** ((cents + vib + deriva) / 1200.0)
        phi = 2 * np.pi * np.cumsum(fc) / SR + rng.uniform(0, 2 * np.pi)
        c1, s1 = np.cos(phi), np.sin(phi)
        s_prev, s_n = np.zeros(N), s1
        soma = np.zeros(N)
        for n in range(1, p["harm"] + 1):
            nf = n * fc
            a = n ** -1.15 / (1.0 + (nf / p["fc"]) ** 2.0) * _corpo(nf)
            a = np.where(nf < 0.45 * SR, a, 0.0)
            soma += a * s_n
            s_prev, s_n = s_n, 2.0 * c1 * s_n - s_prev
        if p.get("sub"):
            soma += p["sub"] * np.sin(0.5 * phi)   # peso de contrabaixo: a oitava abaixo, baixinha
        pan = p["pan"] + 0.12 * (j - (len(cop) - 1) / 2.0)
        th = (np.clip(pan, -1, 1) + 1.0) * math.pi / 4.0
        L += soma * math.cos(th)
        R += soma * math.sin(th)
    esc = p["gan"] * env / math.sqrt(len(cop))
    # sopro de arco: ruído filtrado, bem baixo
    from scipy.signal import butter, sosfilt
    ar = sosfilt(butter(2, [1500, 5500], btype="band", fs=SR, output="sos"), rng.standard_normal(N))
    ar *= 0.012 * p["gan"] * env
    return L * esc + ar * 0.7, R * esc + ar * 0.7


def _reverb(L, R, rng, rt60=2.6, mix=0.28):
    from scipy.signal import butter, fftconvolve, sosfilt
    n = int(3.0 * SR)
    t = np.arange(n) / SR
    env = np.exp(-6.91 * t / rt60) * smooth(t / 0.03)
    sos = butter(2, 4500, btype="low", fs=SR, output="sos")
    ir_l = sosfilt(sos, rng.standard_normal(n)) * env
    ir_r = sosfilt(sos, rng.standard_normal(n)) * env
    ir_l /= np.sqrt((ir_l ** 2).sum())
    ir_r /= np.sqrt((ir_r ** 2).sum())
    wl = fftconvolve(L, ir_l)[: len(L)]
    wr = fftconvolve(R, ir_r)[: len(R)]
    return (1 - mix) * L + mix * wl, (1 - mix) * R + mix * wr


def gera_audio(destino: Path = WAV, semente: int = 1619):
    from scipy.io import wavfile
    ef = efem()
    rng = np.random.default_rng(semente)
    N = int(DUR * SR)
    t = np.arange(N) / SR
    d = dias(t)
    L = np.zeros(N)
    R = np.zeros(N)
    for i, p in enumerate(PLANETAS):
        f = ef.f_voz(i, d)
        vl, vr = _voz(f, p, rng)
        L += vl
        R += vr
    L, R = _reverb(L, R, rng)
    pico = max(np.abs(L).max(), np.abs(R).max())
    L, R = L / pico * 0.89, R / pico * 0.89
    # limitador suave e fade-in curto
    ini = smooth(t / 0.4)
    L, R = np.tanh(1.15 * L) / np.tanh(1.15) * ini, np.tanh(1.15 * R) / np.tanh(1.15) * ini
    destino.parent.mkdir(parents=True, exist_ok=True)
    wavfile.write(str(destino), SR, (np.stack([L, R], axis=1) * 32767).astype(np.int16))
    return destino


def garante_audio(forcar=False):
    if forcar or not WAV.exists():
        gera_audio()
    return WAV


# ═════════════════════════════ teclado ═════════════════════════════
M0, M1 = 43, 101           # G2 .. F7 (MIDI)
BRANCAS = {0, 2, 4, 5, 7, 9, 11}


def _centros_teclas(largura):
    n_b = sum(1 for m in range(M0, M1 + 1) if m % 12 in BRANCAS)
    ww = largura / n_b
    xc, w = {}, 0
    for m in range(M0, M1 + 1):
        if m % 12 in BRANCAS:
            xc[m] = (w + 0.5) * ww
            w += 1
        else:
            xc[m] = w * ww
    return xc, ww


# ═════════════════════════════ cena ═════════════════════════════
from manim import (  # noqa: E402
    DOWN, ITALIC, LEFT, ORIGIN, RIGHT, UP, Dot, FadeIn, Line, Mobject, Rectangle,
    RoundedRectangle, Scene, Text, Triangle, VGroup, VMobject, ValueTracker, linear,
)

# orrery
CX, CY = -3.45, -0.30
def r_tela(r_ua):
    return 1.231 + 0.655 * math.log(max(r_ua, 0.2))

# painel das vozes
PX0, PX1 = 0.55, 6.85
KEY_TOP, KEY_H = -2.40, 0.62
LANE_Y0, LANE_DY = -1.62, 0.70
N_CAUDA = 16


class HarmoniaDosMundos(Scene):
    def construct(self):
        self.camera.background_color = GRUV_BG
        dummy = Mobject()      # primeiro da cena: tudo que vem depois é redesenhado a cada quadro
        self.add(dummy)
        ef = efem()
        garante_audio()
        xc, ww = _centros_teclas(PX1 - PX0)

        def x_de_f(f):
            m = 69.0 + 12.0 * np.log2(np.maximum(f, 1.0) / 440.0)
            m = float(np.clip(m, M0, M1 - 1e-6))
            m0 = int(math.floor(m))
            fr = m - m0
            return PX0 + xc[m0] + (xc[m0 + 1] - xc[m0]) * fr

        # ——— título e legendas fixas ———
        titulo = Text("A harmonia dos mundos", font=FONT, font_size=40, color=GRUV_YELLOW)
        titulo.to_corner(UP + LEFT, buff=0.35)
        sub = Text("Kepler · Harmonices Mundi, livro V (1619)", font=FONT, font_size=20,
                   color=GRUV_GRAY, slant=ITALIC)
        sub.next_to(titulo, DOWN, buff=0.08, aligned_edge=LEFT)
        topo_dir = Text("cada voz é a velocidade angular de um planeta", font=FONT, font_size=23,
                        color=GRUV_FG, slant=ITALIC)
        topo_dir.move_to([(PX0 + PX1) / 2, 3.50, 0])
        topo_dir2 = Text("vista do Sol: quanto mais rápido, mais agudo", font=FONT, font_size=20,
                         color=GRUV_GRAY)
        topo_dir2.next_to(topo_dir, DOWN, buff=0.08)
        topo_dir3 = Text("do afélio (nota grave) ao periélio (nota aguda)", font=FONT, font_size=17,
                         color=GRUV_NEUT, slant=ITALIC)
        topo_dir3.next_to(topo_dir2, DOWN, buff=0.06)
        legenda = Text("vista do polo norte da eclíptica · ângulos reais · distâncias em escala logarítmica",
                       font=FONT, font_size=15, color=GRUV_NEUT, slant=ITALIC)
        legenda.move_to([CX, -3.36, 0])
        g1 = Text("MEDÍVEL", font=FONT, font_size=15, color=GRUV_AQUA, weight="BOLD")
        g1b = Text("velocidades angulares (efemérides VSOP87)", font=FONT, font_size=15, color=GRUV_GRAY)
        g2 = Text("INTERPRETÁVEL", font=FONT, font_size=15, color=GRUV_YELLOW, weight="BOLD")
        g2b = Text("leitura como altura de som (Kepler, 1619)", font=FONT, font_size=15, color=GRUV_GRAY)
        g1b.next_to(g1, RIGHT, buff=0.12)
        g2b.next_to(g2, RIGHT, buff=0.12)
        grau = VGroup(VGroup(g1, g1b), VGroup(g2, g2b)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        grau.move_to([(PX0 + PX1) / 2, -3.50, 0], aligned_edge=ORIGIN)

        # ——— Sol ———
        sol_halo = [Dot([CX, CY, 0], radius=r, color=GRUV_YELLOW).set_opacity(o)
                    for r, o in ((0.34, 0.07), (0.24, 0.12), (0.16, 0.25))]
        sol = Dot([CX, CY, 0], radius=0.11, color=GRUV_YELLOW)

        # ——— teclado ———
        teclas = VGroup()
        pretas = VGroup()
        rotulos_c = VGroup()
        for m in range(M0, M1 + 1):
            if m % 12 in BRANCAS:
                k = Rectangle(width=ww, height=KEY_H, stroke_width=0.8, stroke_color=GRUV_BLACK,
                              fill_color=GRUV_FG, fill_opacity=0.88)
                k.move_to([PX0 + xc[m], KEY_TOP - KEY_H / 2, 0])
                teclas.add(k)
                if m % 12 == 0:
                    o = m // 12 - 1
                    rotulos_c.add(Text(f"C{o}", font=FONT, font_size=13, color=GRUV_GRAY)
                                  .move_to([PX0 + xc[m], KEY_TOP - KEY_H - 0.14, 0]))
            else:
                k = Rectangle(width=ww * 0.62, height=KEY_H * 0.60, stroke_width=0.6,
                              stroke_color=GRUV_BLACK, fill_color=GRUV_BLACK, fill_opacity=1.0)
                k.move_to([PX0 + xc[m], KEY_TOP - KEY_H * 0.30, 0])
                pretas.add(k)
        teclado = VGroup(teclas, pretas, rotulos_c)

        # ——— objetos por planeta ———
        objs = []
        for i, p in enumerate(PLANETAS):
            cor = p["cor"]
            lon, rr = ef.anel[i]
            pts = [np.array([CX + r_tela(r) * math.cos(a), CY + r_tela(r) * math.sin(a), 0.0])
                   for a, r in zip(lon, rr)]
            anel = VMobject().set_points_smoothly(pts + [pts[0]]).set_stroke(cor, 1.3, 0.0)
            raio = Line([CX, CY, 0], [CX + 1, CY, 0], stroke_width=1.0, color=cor)
            cauda = VGroup(*[Line(LEFT, RIGHT, color=cor, stroke_width=3.0) for _ in range(N_CAUDA)])
            halo = Dot(radius=0.16, color=cor).set_opacity(0)
            ponto = Dot(radius=0.08, color=cor)
            # pista
            ly = LANE_Y0 + LANE_DY * i
            f_a, f_p = ef.faixa_hz(i)
            xa, xp = x_de_f(f_a), x_de_f(f_p)
            barra = RoundedRectangle(corner_radius=0.07, width=max(xp - xa, 0.14), height=0.14,
                                     stroke_color=cor, stroke_width=1.2, fill_color=cor, fill_opacity=0.0)
            barra.move_to([(xa + xp) / 2, ly, 0])
            fio = Line([PX0, ly, 0], [PX1, ly, 0], stroke_width=0.6, color=GRUV_NEUT)
            rot = Text(f"{p['nome']} · {p['voz']} · {p['razao']}", font=FONT, font_size=17,
                       color=cor, t2c={})
            rot.next_to(barra, UP, buff=0.04, aligned_edge=LEFT)
            if rot.get_right()[0] > PX1 + 0.1:
                rot.shift(LEFT * (rot.get_right()[0] - PX1 - 0.1))
            vlinha = Line([0, ly, 0], [0, KEY_TOP, 0], stroke_width=1.2, color=cor)
            marca = Dot(radius=0.085, color=cor)
            seta = Triangle(color=cor, fill_color=cor, fill_opacity=1.0, stroke_width=0).scale(0.075)
            seta.rotate(math.pi)
            objs.append(dict(anel=anel, raio=raio, cauda=cauda, halo=halo, ponto=ponto,
                             barra=barra, fio=fio, rot=rot, vlinha=vlinha, marca=marca, seta=seta,
                             ly=ly))

        # camadas: fundo → frente
        for o in objs:
            self.add(o["anel"], o["fio"], o["barra"])
        self.add(teclado)
        for o in objs:
            self.add(o["vlinha"], o["raio"], o["cauda"], o["halo"], o["ponto"], o["marca"], o["seta"], o["rot"])
        self.add(*sol_halo, sol)

        tt = ValueTracker(0.0)
        cache = {"data": None, "taxa": None}
        X_DATA, X_TAXA, Y_BASE = CX - 1.45, CX + 0.25, -3.80   # esquerda fixa e mesma linha de base

        def texto_base(s, size, cor, x_esq, **kw):
            # "Hg" invisível no fim dá a todas as strings a mesma altura (H e g), e o fundo do H é a
            # linha de base: assim a data e a taxa não sobem nem descem conforme as letras do mês
            t = Text(s + "Hg", font=FONT, font_size=size, color=cor, **kw)
            t[-2].set_opacity(0)
            t[-1].set_opacity(0)
            return t.shift(RIGHT * (x_esq - t.get_left()[0]) + UP * (Y_BASE - t[-2].get_bottom()[1]))

        tx_data = Text("", font=FONT, font_size=30, color=GRUV_AQUA)
        tx_taxa = Text("", font=FONT, font_size=18, color=GRUV_GRAY, slant=ITALIC)
        self.add(tx_data, tx_taxa)

        def atualiza(_):
            t = tt.get_value()
            d = float(dias(t))
            data = DATA_INICIO + dt.timedelta(days=d)
            s_data = f"{MESES[data.month - 1]} {data.year}"
            if s_data != cache["data"]:
                cache["data"] = s_data
                tx_data.become(texto_base(s_data, 28, GRUV_AQUA, X_DATA))
            s_taxa = f"1 s ≈ {taxa(t):.0f} dias"
            if s_taxa != cache["taxa"]:
                cache["taxa"] = s_taxa
                tx_taxa.become(texto_base(s_taxa, 18, GRUV_GRAY, X_TAXA, slant=ITALIC))
            for i, (p, o) in enumerate(zip(PLANETAS, objs)):
                a = float(smooth((t - p["entra"]) / 1.6))
                lon = float(ef.lon[i](d))
                r = float(ef.r[i](d))
                rd = r_tela(r)
                pos = np.array([CX + rd * math.cos(lon), CY + rd * math.sin(lon), 0.0])
                o["anel"].set_stroke(opacity=0.38 * a)
                o["raio"].put_start_and_end_on(np.array([CX, CY, 0.0]), pos).set_stroke(opacity=0.22 * a)
                o["ponto"].move_to(pos).set_opacity(a)
                o["halo"].move_to(pos).set_opacity(0.22 * a)
                # cauda: 20% da órbita, em dias, do mais novo ao mais velho
                span = 0.20 * p["per"]
                prev = pos
                for q in range(N_CAUDA):
                    dq = d - span * (q + 1) / N_CAUDA
                    lq = float(ef.lon[i](dq))
                    rq = r_tela(float(ef.r[i](dq)))
                    pq = np.array([CX + rq * math.cos(lq), CY + rq * math.sin(lq), 0.0])
                    seg = o["cauda"][q]
                    seg.put_start_and_end_on(prev, pq)
                    seg.set_stroke(opacity=a * 0.75 * (1 - q / N_CAUDA) ** 1.4,
                                   width=3.2 * (1 - 0.7 * q / N_CAUDA))
                    prev = pq
                # pista: a nota de agora
                f = float(ef.f_voz(i, d))
                x = x_de_f(f)
                o["marca"].move_to([x, o["ly"], 0]).set_opacity(a)
                o["vlinha"].put_start_and_end_on(np.array([x, o["ly"], 0.0]),
                                                 np.array([x, KEY_TOP + 0.02, 0.0]))
                o["vlinha"].set_stroke(opacity=0.42 * a)
                o["seta"].move_to([x, KEY_TOP + 0.075, 0]).set_opacity(a)
                o["barra"].set_stroke(opacity=0.85 * a).set_fill(opacity=0.22 * a)
                o["fio"].set_stroke(opacity=0.25 * a)
                o["rot"].set_opacity(a)

        dummy.add_updater(atualiza)

        quadro = os.environ.get("HARM_QUADRO")
        if quadro:                       # teste: um quadro só, no instante pedido (use com -s)
            for m in (titulo, sub, topo_dir, topo_dir2, topo_dir3, legenda, grau):
                self.add(m)
            tt.set_value(float(quadro))
            atualiza(None)               # em -s o Manim não roda os updaters sozinho
            self.wait(0.07)
            return

        self.add_sound(str(WAV))
        # o texto fixo entra nos primeiros segundos; o resto roda na trilha única de tempo (tt)
        self.play(*[FadeIn(m) for m in (titulo, sub)], tt.animate.set_value(1.5),
                  run_time=1.5, rate_func=linear)
        self.play(*[FadeIn(m) for m in (topo_dir, topo_dir2, topo_dir3, legenda, grau)],
                  tt.animate.set_value(3.0), run_time=1.5, rate_func=linear)
        self.play(tt.animate.set_value(DUR), run_time=DUR - 3.0, rate_func=linear)
        dummy.remove_updater(atualiza)


if __name__ == "__main__":
    print(garante_audio(forcar=True))
