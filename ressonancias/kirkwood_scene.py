"""
MISTAGOGOS · V2 · A Lua e o relógio da vida · lacunas de Kirkwood
Cena A "Gota": interferência de duas fontes (analogia, INTERPRETÁVEL).
Cena B "Lacunas": histograma real do JPL, ressonâncias de Kepler, vista orbital e
simulação própria (MEDÍVEL). Dados em ressonancias/dados/ (kirkwood_sim.py, kirkwood_verify.py).

Paleta Gruvbox · EB Garamond · sons de output/sons (se faltar, roda muda)
"""

import json
from pathlib import Path

import numpy as np

from manim import (
    DOWN,
    ITALIC,
    LEFT,
    RIGHT,
    UP,
    Circumscribe,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    ImageMobject,
    Line,
    MathTex,
    Polygon,
    RoundedRectangle,
    Scene,
    Text,
    VGroup,
    ValueTracker,
    always_redraw,
    color_gradient,
    rate_functions,
)

# ———— Paleta Gruvbox ————
GRUV_BG = "#282828"
GRUV_FG = "#ebdbb2"
GRUV_YELLOW = "#fabd2f"
GRUV_ORANGE = "#fe8019"
GRUV_RED = "#fb4934"
GRUV_AQUA = "#8ec07c"
GRUV_BLUE = "#83a598"
GRUV_GRAY = "#a89984"
GRUV_DARK = "#3c3836"
GRUV_NEUT = "#7c6f64"

FONT = "EB Garamond"
AQUI = Path(__file__).resolve().parent
DADOS = AQUI / "dados"
SONS = AQUI.parent / "output" / "sons"

A_J = 5.2044
RESSON = [("3:1", 1 / 3), ("5:2", 2 / 5), ("7:3", 3 / 7), ("2:1", 1 / 2), ("3:2", 2 / 3)]


def a_res(r):
    return A_J * r ** (2 / 3)


def texto(s, size=26, cor=GRUV_FG, **kw):
    return Text(s, font=FONT, color=cor, font_size=size, **kw)


def selo(s, cor, size=22):
    t = texto(s, size, cor)
    caixa = RoundedRectangle(corner_radius=0.08, width=t.width + 0.4, height=t.height + 0.24,
                             color=cor, stroke_width=2.0, fill_color=GRUV_BG, fill_opacity=0.9)
    t.move_to(caixa)
    return VGroup(caixa, t)


def texto_vivo(get_str, size=26, cor=GRUV_FG):
    """Text que só é refeito quando a string muda."""
    estado = {"s": get_str()}
    t = texto(estado["s"], size, cor)

    def upd(m):
        s = get_str()
        if s != estado["s"]:
            estado["s"] = s
            m.become(texto(s, size, cor).move_to(m.get_center()))

    t.add_updater(upd)
    return t


# ———————————————————————————————————————————————————————————
# CENA A · GOTA
# ———————————————————————————————————————————————————————————
LARG, ALT = 14.222, 8.0
GW, GH = 400, 225
K_ONDA = 2 * np.pi / 1.1
OM_ONDA = 2 * np.pi * 1.2
C_ONDA = OM_ONDA / K_ONDA
FONTES = [(-1.5, 0.0, 0.0), (1.5, 0.0, 3.0)]

PARADAS = np.array([-1.0, -0.35, 0.0, 0.5, 1.0])
CORES = np.array([
    [0x1D, 0x20, 0x21],
    [0x28, 0x28, 0x28],
    [0x3C, 0x38, 0x36],
    [0xB5, 0x76, 0x14],
    [0xFA, 0xBD, 0x2F],
], dtype=float)


def campo(t):
    X = np.linspace(-LARG / 2, LARG / 2, GW)[None, :]
    Y = np.linspace(ALT / 2, -ALT / 2, GH)[:, None]
    u = np.zeros((GH, GW))
    for sx, sy, t0 in FONTES:
        tau = t - t0
        if tau <= 0:
            continue
        r = np.hypot(X - sx, Y - sy)
        frente = 1.0 / (1.0 + np.exp(-(C_ONDA * tau - r) / 0.2))
        u += frente * np.cos(K_ONDA * r - OM_ONDA * tau) / np.sqrt(1.0 + 0.9 * r)
    u = np.tanh(1.1 * u)
    img = np.stack([np.interp(u, PARADAS, CORES[:, c]) for c in range(3)], axis=-1)
    return img.astype(np.uint8)


def ponto_nodal(y, n=1):
    """x>0 em que |r1 - r2| = n*λ/2 na altura y (linha nodal de cancelamento)."""
    lam = 2 * np.pi / K_ONDA
    xs = np.linspace(0.0, 6.5, 4000)
    r1 = np.hypot(xs + 1.5, y)
    r2 = np.hypot(xs - 1.5, y)
    d = np.abs(r1 - r2) - n * lam / 2
    i = np.argmin(np.abs(d))
    return xs[i]


class Gota(Scene):
    def tocar(self, wav, **kw):
        if (SONS / wav).exists():
            self.add_sound(str(SONS / wav), **kw)

    def construct(self):
        self.camera.background_color = GRUV_BG
        self.tocar("whoosh_agua.wav", gain=-16)
        self.tocar("drone_esferas.wav", gain=-18)

        t = ValueTracker(0.0)
        t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(t)

        def imagem():
            im = ImageMobject(campo(t.get_value()))
            im.set_width(LARG)
            return im

        img = always_redraw(imagem)
        self.add(img)
        self.wait(5.0)

        # fontes e rótulos
        pt1 = Dot([FONTES[0][0], 0, 0], radius=0.09, color=GRUV_FG)
        pt2 = Dot([FONTES[1][0], 0, 0], radius=0.09, color=GRUV_FG)
        self.play(FadeIn(pt1), FadeIn(pt2), run_time=0.6)
        self.wait(1.4)

        y_lab = 2.4
        x_n = ponto_nodal(y_lab, 3)
        marca_r = Dot([0.0, y_lab, 0], radius=0.09, color=GRUV_FG)
        marca_c = Dot([x_n, y_lab, 0], radius=0.09, color=GRUV_FG)
        lab_r = texto("reforço", 30, GRUV_YELLOW).add_background_rectangle(
            color=GRUV_BG, opacity=0.8, buff=0.12).next_to(marca_r, LEFT, buff=0.18)
        lab_c = texto("cancelamento", 30, GRUV_BLUE).add_background_rectangle(
            color=GRUV_BG, opacity=0.8, buff=0.12).next_to(marca_c, RIGHT, buff=0.18)
        self.play(FadeIn(marca_r), FadeIn(lab_r), run_time=0.8)
        self.wait(1.4)
        self.play(FadeIn(marca_c), FadeIn(lab_c), run_time=0.8)
        self.wait(1.0)

        explic = texto("onde duas cristas se encontram, as ondas se somam; "
                       "onde crista encontra vale, se anulam", 26).add_background_rectangle(
            color=GRUV_BG, opacity=0.8, buff=0.15).to_edge(DOWN, buff=1.0)
        self.play(FadeIn(explic), run_time=0.8)
        s = selo("INTERPRETÁVEL (analogia)", GRUV_ORANGE).to_corner(UP + RIGHT, buff=0.35)
        self.play(FadeIn(s), run_time=0.6)
        self.wait(3.0)

        aviso = texto("é só uma imagem: a ressonância dos asteroides é gravitacional, não é onda de água",
                      24, GRUV_GRAY).add_background_rectangle(
            color=GRUV_BG, opacity=0.8, buff=0.15).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(aviso), run_time=0.8)
        self.wait(4.0)
        self.play(FadeOut(VGroup(marca_r, marca_c, lab_r, lab_c, explic, aviso, s, pt1, pt2)),
                  run_time=0.8)
        self.wait(0.4)
        t.clear_updaters()


# ———————————————————————————————————————————————————————————
# CENA B · LACUNAS
# ———————————————————————————————————————————————————————————
FAIXA_A = (2.0, 4.2)
BIN = 0.01
AX_L, AX_R = -6.0, 5.8
AX_BASE, AX_ALT = -2.0, 2.4


def x_de(a):
    return AX_L + (a - FAIXA_A[0]) / (FAIXA_A[1] - FAIXA_A[0]) * (AX_R - AX_L)


def carrega_real():
    a = []
    for nome in ("sbdb_mba.json", "sbdb_externo.json"):
        d = json.load(open(DADOS / nome))
        a += [float(l[0]) for l in d["data"] if l[0] is not None]
    return np.array(a)


def contagens(a):
    bordas = np.arange(FAIXA_A[0], FAIXA_A[1] + BIN / 2, BIN)
    c, _ = np.histogram(a, bins=bordas)
    return c.astype(float)


def poligono_hist(c, ymax, cor, opac=0.55):
    n = len(c)
    pts = [[x_de(FAIXA_A[0]), AX_BASE, 0]]
    for i in range(n):
        h = AX_BASE + AX_ALT * min(c[i] / ymax, 1.0)
        xa = x_de(FAIXA_A[0] + i * BIN)
        xb = x_de(FAIXA_A[0] + (i + 1) * BIN)
        pts += [[xa, h, 0], [xb, h, 0]]
    pts.append([x_de(FAIXA_A[1]), AX_BASE, 0])
    return Polygon(*pts, color=cor, stroke_width=1.2, fill_color=cor, fill_opacity=opac)


def eixos():
    base = Line([AX_L, AX_BASE, 0], [AX_R, AX_BASE, 0], color=GRUV_GRAY, stroke_width=2.0)
    g = VGroup(base)
    for a in (2.0, 2.5, 3.0, 3.5, 4.0):
        x = x_de(a)
        g.add(Line([x, AX_BASE, 0], [x, AX_BASE - 0.1, 0], color=GRUV_GRAY, stroke_width=2.0))
        g.add(texto(f"{a:.1f}".replace(".", ","), 22, GRUV_GRAY).move_to([x, AX_BASE - 0.32, 0]))
    g.add(texto("semieixo maior a (UA)", 22, GRUV_GRAY).move_to([x_de(3.1), AX_BASE - 0.72, 0]))
    return g


def linhas_ressonancia(nomes=None):
    g = VGroup()
    desloc = {"3:1": 0.0, "5:2": 0.0, "7:3": 0.0, "2:1": 0.0, "3:2": 0.0}
    for nome, r in RESSON:
        if nomes is not None and nome not in nomes:
            continue
        x = x_de(a_res(r))
        ln = DashedLine([x, AX_BASE, 0], [x, AX_BASE + AX_ALT + 0.15, 0], color=GRUV_YELLOW,
                        stroke_width=2.0, dash_length=0.1)
        rotulo = nome + (" Hilda" if nome == "3:2" else "")
        lab = texto(rotulo, 24, GRUV_YELLOW).move_to([x + desloc[nome], AX_BASE + AX_ALT + 0.42, 0])
        g.add(VGroup(ln, lab))
    return g


class Lacunas(Scene):
    def tocar(self, wav, **kw):
        if (SONS / wav).exists():
            self.add_sound(str(SONS / wav), **kw)

    def construct(self):
        self.camera.background_color = GRUV_BG
        self.tocar("drone_esferas.wav", gain=-16)

        ver = json.load(open(DADOS / "verificacao.json"))
        snaps = np.load(DADOS / "kirkwood_snapshots.npz")
        orb = np.load(DADOS / "kirkwood_orbital.npz")

        legenda = texto("A ressonância limpa em vez de construir", 28, GRUV_AQUA, slant=ITALIC)
        legenda.to_edge(DOWN, buff=0.28)
        self.add(legenda)

        # ———— 1. histograma real ————
        real = carrega_real()
        cr = contagens(real)
        ymax_r = cr.max() * 1.08
        poly_real = poligono_hist(cr, ymax_r, GRUV_AQUA)
        ax = eixos()
        titulo = texto("o cinturão de asteroides hoje", 36).to_edge(UP, buff=0.35)
        n_real = f"{len(real):,}".replace(",", ".")
        sub = texto(f"{n_real} asteroides do JPL (H < 16), a entre 2,0 e 4,2 UA", 22, GRUV_GRAY).next_to(titulo, DOWN, buff=0.12)
        s_med = selo("MEDÍVEL", GRUV_AQUA).to_corner(UP + RIGHT, buff=0.35)
        self.play(FadeIn(titulo), FadeIn(sub), FadeIn(ax), run_time=1.0)
        self.play(FadeIn(poly_real), FadeIn(s_med), run_time=1.6)
        self.wait(3.0)

        # ———— 2. ressonâncias de Kepler ————
        calc = MathTex(r"a = a_J \left(\tfrac{1}{3}\right)^{2/3} = 5{,}2044 \times 0{,}4807 = 2{,}50\ \mathrm{UA}",
                       color=GRUV_FG, font_size=40)
        calc.move_to([0.0, 1.45, 0])
        calc_fundo = RoundedRectangle(corner_radius=0.08, width=calc.width + 0.5, height=calc.height + 0.4,
                                      color=GRUV_NEUT, stroke_width=1.5, fill_color=GRUV_BG,
                                      fill_opacity=0.92).move_to(calc)
        terceira = texto("terceira lei de Kepler: o período de 1/3 do de Júpiter pede a = 2,50 UA", 22,
                         GRUV_GRAY).next_to(calc_fundo, UP, buff=0.12)
        lin = linhas_ressonancia()
        self.play(FadeIn(lin[0]), run_time=0.9)
        self.play(FadeIn(calc_fundo), FadeIn(calc), FadeIn(terceira), run_time=1.0)
        self.wait(3.5)
        self.play(FadeOut(calc_fundo), FadeOut(calc), FadeOut(terceira), run_time=0.6)
        for i in (1, 2, 3, 4):
            self.play(FadeIn(lin[i]), run_time=0.7)
        pos_teor = ver["posicoes_teoricas_UA"]
        nota = texto("posições pela terceira lei: 3:1 " + pos_teor["3:1"].__str__().replace(".", ",")
                     + " · 5:2 " + str(pos_teor["5:2"]).replace(".", ",")
                     + " · 7:3 " + str(pos_teor["7:3"]).replace(".", ",")
                     + " · 2:1 " + str(pos_teor["2:1"]).replace(".", ",")
                     + " · 3:2 " + str(pos_teor["3:2"]).replace(".", ","), 22, GRUV_GRAY)
        nota.move_to([0.0, 1.6, 0])
        self.play(FadeIn(nota), run_time=0.6)
        self.wait(3.5)
        self.play(FadeOut(nota), run_time=0.5)

        # ———— 3. vista de cima ————
        self.play(FadeOut(VGroup(poly_real, ax, lin, titulo, sub, s_med)), run_time=0.9)

        ESC = 0.62
        CEN = np.array([0.0, 0.15, 0.0])
        sol = Dot(CEN, radius=0.14, color=GRUV_YELLOW)
        jup_o = Dot(CEN, radius=0.1, color=GRUV_ORANGE)
        a0 = orb["a0"]
        cmap = color_gradient([GRUV_AQUA, GRUV_YELLOW, GRUV_ORANGE], 60)
        ca3 = a_res(1 / 3)
        dest = np.abs(a0 - ca3) <= 0.03
        pts = VGroup()
        for i, a in enumerate(a0):
            k = int(np.clip((a - 2.0) / 2.2 * 59, 0, 59))
            if dest[i]:
                pts.add(Dot(CEN, radius=0.075, color=GRUV_RED))
            else:
                pts.add(Dot(CEN, radius=0.03, color=cmap[k]))
        # destacadas por cima das demais
        ordem = np.argsort(dest.astype(int), kind="stable")
        pts = VGroup(*[pts[i] for i in ordem])
        ordem_inv = np.argsort(ordem)

        tit3 = texto("vista de cima: Júpiter e 500 partículas de teste", 34).to_edge(UP, buff=0.35)
        sel3 = texto("MEDÍVEL (simulação própria: Sol, Júpiter e partículas de teste)", 20,
                     GRUV_AQUA).next_to(tit3, DOWN, buff=0.12)
        fr = ValueTracker(0.0)
        pos = orb["pos"]
        jup = orb["jup"]
        tq = orb["t"]

        def atualiza(_m):
            f = fr.get_value()
            i0 = int(np.floor(f))
            i1 = min(i0 + 1, len(tq) - 1)
            w = f - i0
            p = pos[i0] * (1 - w) + pos[i1] * w
            for j, d in enumerate(pts):
                src = ordem[j]
                d.move_to(CEN + ESC * np.array([p[src, 0], p[src, 1], 0.0]))
            jp = jup[i0] * (1 - w) + jup[i1] * w
            jup_o.move_to(CEN + ESC * np.array([jp[0], jp[1], 0.0]))

        pts.add_updater(atualiza)
        atualiza(None)
        relogio = texto_vivo(lambda: f"t = {tq[min(int(fr.get_value()), len(tq) - 1)]:4.1f} anos".replace(".", ","),
                             26, GRUV_FG)
        relogio.move_to([5.2, -1.4, 0])
        info = texto("em vermelho, as partículas em 3:1: três voltas para cada volta de Júpiter", 22,
                     GRUV_RED).move_to([0.0, -3.0, 0])
        self.play(FadeIn(sol), FadeIn(jup_o), FadeIn(pts), FadeIn(tit3), FadeIn(sel3), run_time=1.0)
        self.add(relogio)
        self.play(FadeIn(info), run_time=0.6)
        self.play(fr.animate.set_value(len(tq) - 1), run_time=24.0, rate_func=rate_functions.linear)
        self.wait(0.5)
        pts.clear_updaters()
        relogio.clear_updaters()
        self.play(FadeOut(VGroup(sol, jup_o, pts, tit3, sel3, relogio, info)), run_time=0.9)

        # ———— 4. a simulação abre as lacunas ————
        ts = snaps["t"]
        hist = []
        for k in range(len(ts)):
            a = snaps["a"][k][snaps["vivo"][k]]
            hist.append(contagens(a))
        ymax_s = max(h.max() for h in hist) * 1.15
        poly = poligono_hist(hist[0], ymax_s, GRUV_AQUA)
        ax2 = eixos()
        lin2 = linhas_ressonancia()
        tit4 = texto("a simulação: 3.000 partículas, 200 mil anos", 36).to_edge(UP, buff=0.35)
        sel4 = texto("MEDÍVEL (simulação própria: Sol, Júpiter e partículas de teste)", 20,
                     GRUV_AQUA).next_to(tit4, DOWN, buff=0.12)
        ini = texto("começam distribuídas por igual em a", 22, GRUV_GRAY).move_to([0.0, 1.9, 0])
        self.play(FadeIn(tit4), FadeIn(sel4), FadeIn(ax2), FadeIn(lin2), FadeIn(poly), run_time=1.0)

        def rot_t(t):
            if t == 0:
                return "t = 0"
            if t < 1e4:
                return f"t = {t / 1e3:.0f} mil anos"
            return f"t = {t / 1e3:.0f} mil anos"

        rel = texto(rot_t(ts[0]), 30, GRUV_FG).move_to([5.2, 2.55, 0])
        vivas = texto(f"vivas: {int(snaps['vivo'][0].sum())}", 22, GRUV_GRAY).next_to(rel, DOWN, buff=0.1)
        self.add(rel, vivas)
        self.play(FadeIn(ini), run_time=0.6)
        self.wait(2.0)
        self.play(FadeOut(ini), run_time=0.4)
        for k in range(1, len(ts)):
            novo = poligono_hist(hist[k], ymax_s, GRUV_AQUA)
            rel_n = texto(rot_t(ts[k]), 30, GRUV_FG).move_to(rel.get_center())
            viv_n = texto(f"vivas: {int(snaps['vivo'][k].sum())}", 22, GRUV_GRAY).next_to(rel_n, DOWN, buff=0.1)
            self.play(poly.animate.become(novo), rel.animate.become(rel_n),
                      vivas.animate.become(viv_n), run_time=2.6)
            self.wait(1.2)

        # ———— resultado honesto ————
        def pct(v):
            return f"{v['variacao_pct']:+.0f}%".replace("-", "−")

        final = ver["simulacao"][f"{ts[-1]:.0f}"]["ressonancias"]
        sigmas = [abs(final[n]["sigma_poisson"]) for n in ("3:1", "5:2", "7:3", "2:1")]
        a_tent = ver["tentativas"]["A"]["ressonancias_por_t"]["1000000"]["ressonancias"]["3:1"]
        jpl = ver["jpl_sbdb"]["ressonancias"]
        l1 = "aos 200 mil anos, em ±0,02 UA contra a vizinhança:"
        l2 = ("simulação  " + " · ".join(f"{n} {pct(final[n])}" for n in ("3:1", "5:2", "7:3", "2:1"))
              + f"  (até {max(sigmas):.1f}σ de ruído)".replace(".", ","))
        l3 = f"até 1 milhão de anos, 800 partículas perto de 3:1: {pct(a_tent)}"
        l4 = "dado real do JPL  " + " · ".join(f"{n} {pct(jpl[n])}" for n in ("3:1", "5:2", "7:3", "2:1"))
        l5 = "esta simulação simples não abre as lacunas; o céu real as tem"
        caixa = VGroup(texto(l1, 20, GRUV_GRAY), texto(l2, 20, GRUV_FG), texto(l3, 20, GRUV_FG),
                       texto(l4, 20, GRUV_AQUA), texto(l5, 20, GRUV_YELLOW)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([0.0, 2.15, 0])
        fundo = RoundedRectangle(corner_radius=0.08, width=caixa.width + 0.4, height=caixa.height + 0.3,
                                 color=GRUV_NEUT, stroke_width=1.5, fill_color=GRUV_BG,
                                 fill_opacity=0.92).move_to(caixa)
        self.play(FadeOut(VGroup(rel, vivas, sel4)), run_time=0.5)
        self.play(FadeIn(fundo), FadeIn(caixa), run_time=0.9)
        self.play(Circumscribe(lin2[0], color=GRUV_RED), run_time=1.2)
        self.wait(7.0)
        self.play(FadeOut(VGroup(fundo, caixa, poly, ax2, lin2, tit4)), run_time=0.9)
        self.wait(1.2)
