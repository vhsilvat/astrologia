"""
MISTAGOGOS · a forja da hemíola (3 contra 2)
Sol martela 3 · Dó martela 2 — a cadência acelera até se tornar nota:
262 golpes/s = Dó central (262 Hz) · a bigorna acende em glow.
Depois: tela 1:1 — a forja vibra à esquerda; à direita, as oscilações de
Sol (eixo x · 393 Hz) e Dó (eixo y · 262 Hz) desenham a figura 3:2 — Diapente.
Paleta Gruvbox · EB Garamond · tiques de trem + zumbido de bigorna
"""

import math
from pathlib import Path

import numpy as np

from manim import (
    Circle,
    DashedLine,
    Dot,
    DOWN,
    FadeIn,
    FadeOut,
    ITALIC,
    Line,
    ParametricFunction,
    Polygon,
    Rectangle,
    Scene,
    TAU,
    Text,
    Transform,
    Triangle,
    UP,
    VMobject,
    VGroup,
    ValueTracker,
    always_redraw,
)

# ———— Paleta Gruvbox ————
GRUV_BG = "#282828"
GRUV_FG = "#ebdbb2"
GRUV_YELLOW = "#fabd2f"
GRUV_GREEN = "#b8bb26"
GRUV_AQUA = "#8ec07c"
GRUV_GRAY = "#a89984"
GRUV_NEUT = "#7c6f64"
GRUV_DARK = "#3c3833"

FONT = "EB Garamond"
SONS = Path(__file__).resolve().parent / "sons"  # pasta sons/ ao lado do script

# ———— Forja (geometria já validada) ————
BIGORNA_Y = -1.40
Y_FACE = BIGORNA_Y + 0.75   # topo da face (move_to centraliza o bbox do Polygon)
Y_CHAO = -2.15
XH_D = -0.65                # martelo Dó (12 lb · grave · lento)
XH_S = 0.55                 # martelo Sol (6 lb · agudo · rápido)
SUBIDA = 1.20

# ———— Hemíola (idêntico ao gerador de tic_trem_hemiola.wav: lead 0.65 s) ————
D0 = 2.2                    # duração do 1º ciclo (s)
T_ACC = 10.7                # janela de aceleração — no fim: Dó = 262/s
D_END = 1.0 / 131.0         # 131 ciclos/s → Dó 262/s · Sol 393/s
LAM = math.log(D0 / D_END) / T_ACC
T0 = 3.2                    # instante em que a aceleração começa
MAX_U = T_ACC + 26.0        # o cronograma continua após a fusão
TSPLIT = 16.9               # divisão da tela 1:1

# ———— Gráfico (lado direito) ————
GX, GY = 3.60, 0.75
AX_L, AY_L = 2.10, 1.60     # meia-extensão dos eixos
AX_A, AY_A = 1.35, 1.05     # amplitudes da figura


def d_de(u):
    if u <= 0:
        return D0
    if u >= T_ACC:
        return D_END
    return D0 * math.exp(-LAM * u)


def strikes_de(tag):
    """Instantes dos golpes — mantenha IDÊNTICO ao gerador do WAV."""
    ts = []
    t = 0.65                # alinhado ao lead-in do tic_trem_hemiola.wav
    while t < MAX_U:
        d = d_de(t)
        if tag == "D":
            ts += [t, t + d / 2.0]
        else:
            ts += [t, t + d / 3.0, t + 2.0 * d / 3.0]
        t += d
    return np.array(sorted(ts))


def height_at(u, s):
    """Distância abaixo do repouso: 0 = repouso · SUBIDA = face (impacto)."""
    if u < s[0]:
        f = (u - (s[0] - 0.45)) / 0.45
        return SUBIDA * min(max(f, 0.0), 1.0)
    if u >= s[-1]:
        return SUBIDA * max(0.0, 1.0 - (u - s[-1]) / 0.5)
    i = int(np.searchsorted(s, u, side="right") - 1)
    nxt = s[i + 1] if i + 1 < len(s) else s[-1] + d_de(u)
    gap = max(nxt - s[i], 1e-6)
    p = (u - s[i]) / gap
    if p <= 0.25:
        return SUBIDA * (1.0 - p / 0.25)
    if p <= 0.60:
        return 0.0
    return SUBIDA * (p - 0.60) / 0.40


class FerrariaHemiola(Scene):
    def construct(self):
        self.camera.background_color = GRUV_BG

        # ———— Relógio global ————
        tt = ValueTracker(0.0)
        tt.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(tt)

        # ———— Cabeçalho ————
        cab = Text("Nicômaco de Gerasa · Enchiridion Harmonices",
                   font=FONT, color=GRUV_AQUA, font_size=38,
                   slant=ITALIC).move_to([0.0, 3.35, 0.0])
        self.play(FadeIn(cab), run_time=1.0)                     # → 1.0

        # ———— Chão · bigorna ————
        chao = Line([-6.4, Y_CHAO, 0.0], [6.4, Y_CHAO, 0.0],
                    color=GRUV_NEUT, stroke_width=2.5)
        pontos = [
            (-0.90, 0.55, 0.0), (0.90, 0.55, 0.0), (1.75, 0.28, 0.0), (0.90, 0.02, 0.0),
            (0.62, -0.50, 0.0), (0.95, -0.95, 0.0), (-0.95, -0.95, 0.0), (-0.62, -0.50, 0.0),
            (-1.75, 0.28, 0.0), (-0.90, 0.02, 0.0),
        ]
        bigorna = Polygon(*pontos, color=GRUV_GRAY, stroke_width=3.0,
                          fill_color=GRUV_DARK, fill_opacity=1.0,
                          ).move_to([0.0, BIGORNA_Y, 0.0])
        self.play(FadeIn(chao), FadeIn(bigorna), run_time=0.9)   # → 1.9

        # ———— Martelos: o mito reina (pesado = grave = lento) ————
        def martelo(cor, comp, alt, rotulo, x):
            y_rest = Y_FACE + alt / 2 + SUBIDA
            cabeca = Rectangle(width=comp, height=alt, color=cor,
                               stroke_width=3.0, fill_color=cor,
                               fill_opacity=0.92).move_to([x, y_rest, 0.0])
            cabo = Rectangle(width=0.13, height=1.05, color=GRUV_GRAY,
                             stroke_width=2.5, fill_color=GRUV_GRAY,
                             fill_opacity=0.85).next_to(cabeca, UP, buff=0.03)
            peso = Text(rotulo, font=FONT, color=cor,
                        font_size=30).next_to(cabo, UP, buff=0.14)
            return VGroup(cabeca, cabo, peso)

        m_d = martelo(GRUV_FG, 0.95, 0.40, "Dó · 12 lb", XH_D)
        m_s = martelo(GRUV_YELLOW, 0.62, 0.30, "Sol · 6 lb", XH_S)
        self.play(FadeIn(m_d), FadeIn(m_s), run_time=0.8)        # → 2.7

        # ———— Cartaz (morfa até o final) ————
        card = VGroup(
            Text("3 : 2", font=FONT, color=GRUV_FG, font_size=46),
            Text("a cadência vira nota", font=FONT, color=GRUV_AQUA,
                 font_size=26, slant=ITALIC),
        ).arrange(DOWN, buff=0.18).move_to([0.0, -2.95, 0.0])
        self.play(FadeIn(card), run_time=0.5)                    # → 3.2 = T0

        # ———— Contador de cadência (golpes/s do Dó) ————
        def cnt_build():
            u = tt.get_value() - T0
            if u < 0.70:
                b = "···"
            else:
                c = 2.0 / d_de(min(u, T_ACC))
                if c >= 262:
                    b = "262"
                else:
                    v = 2.0
                    while v * 2.0 <= c and v < 256.0:
                        v *= 2.0
                    b = str(int(v))
            if getattr(cnt_build, "b_", None) == b:
                return cnt_build.m_
            cnt_build.b_ = b
            cnt_build.m_ = Text(f"golpes/s · Dó:  {b}", font=FONT,
                                color=GRUV_FG, font_size=28
                                ).move_to([2.60, 2.80, 0.0])
            return cnt_build.m_

        cnt = always_redraw(cnt_build)
        self.add(cnt)

        # ———— Martelos guiados pelo CRONOGRAMA do áudio ————
        SK_D = strikes_de("D")
        SK_S = strikes_de("S")
        flash_d = ValueTracker(-99.0)
        flash_s = ValueTracker(-99.0)

        def hammer_updater(s_arr, flash_tr, rest_y0):
            state = [-1]

            def up(m):
                u = tt.get_value() - T0
                if u < 0:
                    m.set_y(rest_y0)
                    return
                i = int(np.searchsorted(s_arr, u, side="right") - 1)
                if i >= 0 and i != state[0]:
                    state[0] = i
                    flash_tr.set_value(u)
                m.set_y(rest_y0 - height_at(u, s_arr))

            return up

        m_d.add_updater(hammer_updater(SK_D, flash_d, m_d.get_y()))
        m_s.add_updater(hammer_updater(SK_S, flash_s, m_s.get_y()))

        # ———— Ondas de impacto (apenas enquanto o olho resolve os golpes) ————
        def ring(xh, cor, flash_tr):
            def build():
                u = tt.get_value() - T0
                age = u - flash_tr.get_value()
                c = 2.0 / d_de(min(max(u, 1e-9), T_ACC))
                vis = max(0.0, (8.0 - c) / 8.0) ** 2
                if u < 0 or age < 0.001 or age > 0.55 or vis <= 0.02:
                    return Line([xh, Y_FACE, 0.0], [xh, Y_FACE, 0.0],
                                stroke_width=0).set_opacity(0.0)
                r = 0.25 + 4.0 * age
                return Circle(radius=r, color=cor,
                              stroke_width=4.0).move_to([xh, Y_FACE, 0.0])
            return build

        r_d = always_redraw(ring(XH_D, GRUV_GREEN, flash_d))
        r_s = always_redraw(ring(XH_S, GRUV_YELLOW, flash_s))
        self.add(r_d, r_s)

        # ———— FASE A · a hemíola acelera (WAV nasce do mesmo cronograma) ————
        self.add_sound(str(SONS / "tic_trem_hemiola.wav"))
        self.wait(T_ACC)                                         # → 13.9

        # ———— FASE B · a cadência vira nota: o glow ————
        glow = ValueTracker(0.0)
        tcentral = Text("Dó central · 262 Hz", font=FONT, color=GRUV_GREEN,
                        font_size=28).move_to([2.60, 2.80, 0.0])

        def halo(rk, op0):
            def build():
                g = glow.get_value()
                if g <= 0.02:
                    return Line([0, BIGORNA_Y, 0], [0, BIGORNA_Y, 0],
                                stroke_width=0).set_opacity(0.0)
                k = 0.5 + 0.5 * math.sin(2 * math.pi * 1.35 * (tt.get_value() - T0 - T_ACC))
                return (Circle(radius=rk * (0.92 + 0.11 * k) * g,
                               color=GRUV_YELLOW, stroke_width=3.5)
                        .move_to([0.0, BIGORNA_Y + 0.15, 0.0])
                        .set_opacity(g * op0 * (0.65 + 0.35 * k)))
            return build

        halo1 = always_redraw(halo(1.55, 0.30))
        halo2 = always_redraw(halo(2.15, 0.16))

        def barra(w, xh, cor):
            def build():
                g = glow.get_value()
                if g <= 0.02:
                    return Line([xh, Y_FACE, 0], [xh, Y_FACE, 0],
                                stroke_width=0).set_opacity(0.0)
                dy = 0.05 * math.sin(2 * math.pi * 34.0 * tt.get_value())
                op = 0.32 + 0.10 * math.sin(2 * math.pi * 21.0 * tt.get_value())
                return (Rectangle(width=w, height=0.30, color=cor,
                                  stroke_width=2.0, fill_color=cor,
                                  fill_opacity=0.9)
                        .move_to([xh, Y_FACE + 0.28 + dy, 0.0])
                        .set_opacity(op * g))
            return build

        bar_d = always_redraw(barra(0.95, XH_D, GRUV_GREEN))
        bar_s = always_redraw(barra(0.62, XH_S, GRUV_YELLOW))

        self.add(halo1, halo2, bar_d, bar_s)
        self.add_sound(str(SONS / "bigorna_Do262.wav"))
        self.add_sound(str(SONS / "bigorna_Sol393.wav"))
        cnt.clear_updaters()
        self.play(FadeIn(tcentral), FadeOut(cnt),
                  glow.animate.set_value(1.0),
                  FadeOut(m_d), FadeOut(m_s),
                  run_time=0.9)                                  # → 14.8
        m_d.clear_updaters()
        m_s.clear_updaters()
        self.remove(m_d, m_s)
        self.wait(2.0)                                           # → 16.8

        # ———— FASE C · tela 1:1 — a forja vibra · a figura nasce ————
        bar_d.clear_updaters()
        bar_s.clear_updaters()
        halo1.clear_updaters()
        halo2.clear_updaters()
        divisor = (DashedLine([0.0, -3.85, 0.0], [0.0, 3.75, 0.0],
                              color=GRUV_GRAY, stroke_width=3.0)
                   .set_opacity(0.55))
        rotulo_11 = Text("1 : 1", font=FONT, color=GRUV_GRAY,
                         font_size=24).move_to([0.0, 3.05, 0.0])
        self.play(FadeOut(bar_d), FadeOut(bar_s),
                  FadeOut(halo1), FadeOut(halo2),
                  FadeOut(chao),
                  bigorna.animate.scale(0.72).move_to([-3.00, -0.95, 0.0]),
                  FadeIn(divisor), FadeIn(rotulo_11),
                  run_time=1.5)                                  # → 18.3

        # tremor + halos locais da bigorna recolocada
        bx, by = bigorna.get_center()[:2]
        bigorna.add_updater(
            lambda m: m.move_to([bx, by + 0.020 * math.sin(
                2 * math.pi * 6.2 * (tt.get_value() - TSPLIT)), 0.0]))

        def halo_local(rk, op0):
            def build():
                k = 0.5 + 0.5 * math.sin(2 * math.pi * 1.35 * (tt.get_value() - T0 - T_ACC))
                return (Circle(radius=rk * (0.92 + 0.10 * k),
                               color=GRUV_YELLOW, stroke_width=3.0)
                        .move_to([bx, by, 0.0])
                        .set_opacity(0.30 * (0.65 + 0.35 * k) * op0))
            return build

        hl1 = always_redraw(halo_local(1.05, 1.0))
        hl2 = always_redraw(halo_local(1.55, 0.5))
        self.add(hl1, hl2)

        # ———— Gráfico: eixos com a oscilação de cada nota ————
        eixo_x = Line([GX - AX_L - 0.15, GY, 0.0], [GX + AX_L + 0.15, GY, 0.0],
                      color=GRUV_GRAY, stroke_width=2.5)
        eixo_y = Line([GX, GY - AY_L - 0.15, 0.0], [GX, GY + AY_L + 0.15, 0.0],
                      color=GRUV_GRAY, stroke_width=2.5)
        lbl_x = Text("Sol · 393 Hz", font=FONT, color=GRUV_YELLOW,
                     font_size=26).move_to([GX + 1.05, GY - 0.62, 0.0])
        lbl_y = Text("Dó · 262 Hz", font=FONT, color=GRUV_GREEN,
                     font_size=26).move_to([GX - 1.05, GY + AY_L + 0.30, 0.0])

        def onda_x():
            ph = 2.2 * (tt.get_value() - TSPLIT)

            def f(p):
                return np.array([GX + AX_L * (p - 0.5),
                                 GY + 0.30 * math.sin(3 * math.pi * p + ph), 0.0])

            return (ParametricFunction(f, t_range=(0.0, 1.0, 0.01),
                                       color=GRUV_YELLOW,
                                       stroke_width=3.0).set_opacity(0.85))

        def onda_y():
            ph = 2.2 * (tt.get_value() - TSPLIT)

            def f(p):
                return np.array([GX + 0.30 * math.sin(2 * math.pi * p + ph),
                                 GY + AY_L * (p - 0.5), 0.0])

            return (ParametricFunction(f, t_range=(0.0, 1.0, 0.01),
                                       color=GRUV_GREEN,
                                       stroke_width=3.0).set_opacity(0.85))

        wx = always_redraw(onda_x)
        wy = always_redraw(onda_y)
        self.play(FadeIn(eixo_x), FadeIn(eixo_y),
                  FadeIn(lbl_x), FadeIn(lbl_y),
                  FadeIn(wx), FadeIn(wy), run_time=0.6)          # → 18.9

        # ———— A figura: Lissajous 3:2 pelas duas oscilações ————
        NT = 1600
        TH = np.linspace(0.0, TAU, NT)
        PTS = np.stack([GX + AX_A * np.sin(3 * TH),
                        GY + AY_A * np.sin(2 * TH),
                        np.zeros_like(TH)], axis=1)
        prog = ValueTracker(0.0)

        def trace_build():
            k = int(max(2, round(prog.get_value() * (NT - 1))))
            v = VMobject(color=GRUV_FG, stroke_width=3.5)
            v.set_points_as_corners(list(PTS[:k + 1]))
            return v

        traco = always_redraw(trace_build)

        def ponto_build():
            k = max(1, int(prog.get_value() * (NT - 1)))
            return Dot(PTS[k], radius=0.06, color=GRUV_YELLOW)

        ponto = always_redraw(ponto_build)
        self.add(traco, ponto)
        self.play(prog.animate.set_value(1.0), run_time=4.6,
                  rate_func=lambda p: p * p * (3 - 2 * p))       # → 23.5
        traco.clear_updaters()
        ponto.clear_updaters()

        # cruzamentos: 3 no eixo y · 2 no eixo x
        cruz_y = VGroup(Dot([GX, GY + AY_A * 0.866, 0.0], radius=0.055, color=GRUV_AQUA),
                        Dot([GX, GY, 0.0], radius=0.055, color=GRUV_AQUA),
                        Dot([GX, GY - AY_A * 0.866, 0.0], radius=0.055, color=GRUV_AQUA))
        cruz_x = VGroup(Dot([GX + AX_A, GY, 0.0], radius=0.055, color=GRUV_YELLOW),
                        Dot([GX - AX_A, GY, 0.0], radius=0.055, color=GRUV_YELLOW))
        wx.clear_updaters()
        wy.clear_updaters()
        self.wait(0.4)                                           # → 23.9
        self.play(FadeIn(cruz_y), FadeIn(cruz_x), run_time=0.4)  # → 24.3

        # ———— Cartaz final ————
        card2 = VGroup(
            Text("3 : 2 — Diapente", font=FONT, color=GRUV_FG, font_size=46),
            Text("Dó 262 Hz · Sol 393 Hz — a quinta nasce do ritmo",
                 font=FONT, color=GRUV_AQUA, font_size=26, slant=ITALIC),
        ).arrange(DOWN, buff=0.18).move_to([0.0, -3.15, 0.0])
        self.play(Transform(card, card2), run_time=0.9)          # → 25.2
        self.wait(2.6)                                           # → 27.8

        # ———— Encerramento ————
        for mob in (tt, bigorna, r_d, r_s, wx, wy, traco, ponto, hl1, hl2):
            mob.clear_updaters()
        self.play(FadeOut(card), FadeOut(tcentral), FadeOut(cab),
                  FadeOut(bigorna), FadeOut(eixo_x), FadeOut(eixo_y),
                  FadeOut(lbl_x), FadeOut(lbl_y),
                  FadeOut(cruz_y), FadeOut(cruz_x),
                  FadeOut(divisor), FadeOut(rotulo_11),
                  FadeOut(r_d), FadeOut(r_s),
                  FadeOut(wx), FadeOut(wy),
                  FadeOut(traco), FadeOut(ponto),
                  FadeOut(hl1), FadeOut(hl2),
                  run_time=0.9)                                  # → 28.7
        self.wait(0.3)
