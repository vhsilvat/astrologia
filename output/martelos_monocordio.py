"""
MISTAGOGOS · Da Forja ao Monocórdio
Nicômaco de Gerasa · Enchiridion Harmonices

Os martelos (12 lb / 6 lb — 2:1) golpeiam a bigorna e revelam o Diapasão.
Então a cabeça de cada martelo se funde num pino, e a própria bigorna —
o objeto que fez o som nascer — se estica e vira a corda: o mesmo princípio,
agora visto de frente. O Monocórdio canta seus quatro primeiros modos,
à maneira de Fludd: uma corda sempre inteira, nunca fisicamente dividida.

Paleta Gruvbox · EB Garamond · sons em sons/ (se faltar um arquivo, roda muda)
"""

from pathlib import Path

import numpy as np

from manim import (
    DOWN,
    ITALIC,
    LEFT,
    RIGHT,
    UP,
    Circle,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    ParametricFunction,
    Polygon,
    Rectangle,
    ReplacementTransform,
    Scene,
    Text,
    Triangle,
    VGroup,
    ValueTracker,
    always_redraw,
    rate_functions,
)

# ———— Paleta Gruvbox ————
GRUV_BG = "#282828"
GRUV_FG = "#ebdbb2"
GRUV_YELLOW = "#fabd2f"
GRUV_GREEN = "#b8bb26"
GRUV_ORANGE = "#fe8019"
GRUV_AQUA = "#8ec07c"
GRUV_BLUE = "#83a598"
GRUV_RED = "#cc241d"
GRUV_GRAY = "#a89984"
GRUV_NEUT = "#7c6f64"
GRUV_DARK = "#3c3833"

FONT = "EB Garamond"
SONS = Path(__file__).resolve().parent / "sons"

# Geometria da forja
BIGORNA_Y = -1.40
Y_FACE = BIGORNA_Y + 0.75
Y_CHAO = -2.15
XH1, XH2 = -0.55, 0.35
SUBIDA = 1.20

# Geometria do monocórdio (12 unidades, estilo Fludd)
X0, X1 = -5.0, 5.0
SPAN = X1 - X0
Y_STR = 0.55
AMP = 0.62
SPEED = 3.0

# n → (cor, nota, razão da divisão, nome grego do intervalo, wav)
MODOS = {
    1: (GRUV_FG, "Lá · 220 Hz", "corda inteira · 1:1", "fundamental", "harpa_la_220.wav"),
    2: (GRUV_YELLOW, "Lá⁴ · 440 Hz", "metades · 1:2", "diapasão · a oitava", "harpa_la4_440.wav"),
    3: (GRUV_ORANGE, "Mi⁵ · 660 Hz", "terços · 1:3", "diapente · a quinta (sobre a oitava)", "harpa_mi5_660.wav"),
    4: (GRUV_AQUA, "Lá⁵ · 880 Hz", "quartos · 1:4", "disdiapasão · a dupla oitava", "harpa_la5_880.wav"),
}
ENTRE = {2: "2:1 · oitava", 3: "3:2 · quinta", 4: "4:3 · quarta"}


def xde(frac):
    return X0 + SPAN * frac


class MartelosMonocordio(Scene):
    def tocar(self, wav):
        caminho = SONS / wav
        if caminho.exists():
            self.add_sound(str(caminho))

    def construct(self):
        self.camera.background_color = GRUV_BG
        self._forja()
        self._transicao()
        self._monocordio()

    # ———————————————— PARTE 1 · A forja ————————————————
    def _forja(self):
        titulo = Text(
            "Nicômaco de Gerasa · Enchiridion Harmonices",
            font=FONT, color=GRUV_AQUA, font_size=38, slant=ITALIC,
        ).move_to([0.0, 3.35, 0.0])
        self.play(FadeIn(titulo), run_time=1.0)
        self.wait(0.5)

        chao = Line([-6.4, Y_CHAO, 0.0], [6.4, Y_CHAO, 0.0],
                    color=GRUV_NEUT, stroke_width=2.5)
        pontos = [
            (-0.90, 0.55, 0.0), (0.90, 0.55, 0.0), (1.75, 0.28, 0.0), (0.90, 0.02, 0.0),
            (0.62, -0.50, 0.0), (0.95, -0.95, 0.0), (-0.95, -0.95, 0.0), (-0.62, -0.50, 0.0),
            (-1.75, 0.28, 0.0), (-0.90, 0.02, 0.0),
        ]
        bigorna = Polygon(
            *pontos, color=GRUV_GRAY, stroke_width=3.0,
            fill_color=GRUV_DARK, fill_opacity=1.0,
        ).move_to([0.0, BIGORNA_Y, 0.0])
        self.play(FadeIn(chao), FadeIn(bigorna), run_time=0.9)
        self.wait(0.4)

        def martelo(cor, comp, alt, peso_txt, x):
            y_rest = Y_FACE + alt / 2 + SUBIDA
            cabeca = Rectangle(
                width=comp, height=alt, color=cor, stroke_width=3.0,
                fill_color=cor, fill_opacity=0.92,
            ).move_to([x, y_rest, 0.0])
            cabo = Rectangle(
                width=0.13, height=1.05, color=GRUV_GRAY, stroke_width=2.5,
                fill_color=GRUV_GRAY, fill_opacity=0.85,
            ).next_to(cabeca, UP, buff=0.03)
            peso = Text(peso_txt, font=FONT, color=cor,
                        font_size=30).next_to(cabo, UP, buff=0.14)
            return VGroup(cabeca, cabo, peso)

        m1 = martelo(GRUV_FG, 0.95, 0.40, "12 lb", XH1)
        m2 = martelo(GRUV_YELLOW, 0.62, 0.30, "6 lb", XH2)
        self.play(FadeIn(m1), FadeIn(m2), run_time=0.8)
        self.wait(0.5)

        rot_f = Text("Lá · 220 Hz", font=FONT, color=GRUV_GREEN,
                     font_size=34).move_to([-4.80, -2.80, 0.0])
        rot_2f = Text("Lá⁴ · 440 Hz", font=FONT, color=GRUV_YELLOW,
                      font_size=34).move_to([4.80, -2.80, 0.0])

        def golpe(g, x, cor, wav, rotulo=None):
            self.play(g.animate.shift(SUBIDA * DOWN), run_time=0.20,
                      rate_func=rate_functions.rush_into)
            self.tocar(wav)
            onda = Circle(radius=0.32, color=cor,
                          stroke_width=5.0).move_to([x, Y_FACE, 0.0])
            self.add(onda)
            anims = [onda.animate.scale(2.8).set_opacity(0),
                     bigorna.animate.shift(0.05 * RIGHT)]
            if rotulo is not None:
                anims.append(FadeIn(rotulo))
            self.play(*anims, run_time=0.15)
            self.play(bigorna.animate.shift(0.05 * LEFT), run_time=0.12)
            self.remove(onda)
            self.play(g.animate.shift(SUBIDA * UP), run_time=0.55)

        def golpe_duplo():
            self.play(m1.animate.shift(SUBIDA * DOWN), m2.animate.shift(SUBIDA * DOWN),
                      run_time=0.20, rate_func=rate_functions.rush_into)
            self.tocar("martelo_grave_220.wav")
            self.tocar("martelo_agudo_440.wav")
            o1 = Circle(radius=0.32, color=GRUV_FG,
                       stroke_width=5.0).move_to([XH1, Y_FACE, 0.0])
            o2 = Circle(radius=0.32, color=GRUV_YELLOW,
                       stroke_width=5.0).move_to([XH2, Y_FACE, 0.0])
            self.add(o1, o2)
            self.play(o1.animate.scale(2.8).set_opacity(0),
                      o2.animate.scale(2.8).set_opacity(0),
                      bigorna.animate.shift(0.05 * RIGHT), run_time=0.15)
            self.play(bigorna.animate.shift(0.05 * LEFT), run_time=0.12)
            self.remove(o1, o2)
            self.play(m1.animate.shift(SUBIDA * UP), m2.animate.shift(SUBIDA * UP), run_time=0.55)

        golpe(m1, XH1, GRUV_FG, "martelo_grave_220.wav", rot_f)
        self.wait(0.4)
        golpe(m2, XH2, GRUV_YELLOW, "martelo_agudo_440.wav", rot_2f)
        self.wait(0.4)
        golpe_duplo()
        self.wait(0.3)

        razao = VGroup(
            Text("12 : 6  =  2 : 1", font=FONT, color=GRUV_FG, font_size=54),
            Text("Diapasão — a oitava justa", font=FONT, color=GRUV_YELLOW,
                 font_size=34, slant=ITALIC),
        ).arrange(DOWN, buff=0.22).move_to([0.0, -3.15, 0.0])
        self.play(FadeIn(razao), run_time=0.9)
        self.wait(0.7)
        golpe_duplo()
        self.wait(0.7)

        # guardados para a transição
        self.m1, self.m2 = m1, m2
        self.bigorna, self.chao = bigorna, chao
        self.titulo_forja = titulo
        self.rot_f, self.rot_2f, self.razao = rot_f, rot_2f, razao

    # ———————————————— PARTE 2 · A transição ————————————————
    def _transicao(self):
        self.play(
            FadeOut(self.rot_f), FadeOut(self.rot_2f), FadeOut(self.razao),
            FadeOut(self.chao), FadeOut(self.titulo_forja), run_time=0.7,
        )

        pino_l = Dot([X0, Y_STR, 0.0], radius=0.09, color=GRUV_GRAY)
        pino_r = Dot([X1, Y_STR, 0.0], radius=0.09, color=GRUV_GRAY)
        corda_reta = Line([X0, Y_STR, 0.0], [X1, Y_STR, 0.0],
                          color=GRUV_FG, stroke_width=5.5)

        # a cabeça de cada martelo vira um pino; a bigorna — o próprio corpo
        # que fez o som nascer — estica-se e torna-se a corda.
        self.play(
            ReplacementTransform(self.m1[0], pino_l),
            ReplacementTransform(self.m2[0], pino_r),
            ReplacementTransform(self.bigorna, corda_reta),
            FadeOut(self.m1[1], self.m1[2], self.m2[1], self.m2[2]),
            run_time=1.6,
        )
        self.pinos = VGroup(pino_l, pino_r)

        # motor do monocórdio — criado já aqui para a entrega ser sem costura
        self.fase = ValueTracker(0.0)
        self.fase.add_updater(lambda m, dt: m.increment_value(SPEED * dt))
        self.add(self.fase)
        self.amp = ValueTracker(0.0)
        self.modo = ValueTracker(1.0)

        vib = always_redraw(self._corda_fn)
        env = always_redraw(self._envelope_fn)
        self.remove(corda_reta)
        self.add(env, vib)
        self.vib, self.env = vib, env
        self.wait(0.3)

    def _corda_fn(self):
        n = int(round(self.modo.get_value()))
        a = self.amp.get_value()
        ph = self.fase.get_value()
        cor = GRUV_FG if n == 0 else MODOS[n][0]

        def f(t):
            if n == 0:
                y = sum((1.0 / k) * np.sin(k * np.pi * t) * np.cos(k * ph + 0.6 * k)
                        for k in (1, 2, 3, 4)) / 1.2
            else:
                y = np.sin(n * np.pi * t) * np.cos(n * ph)
            return np.array([xde(t), Y_STR + a * y, 0.0])

        return ParametricFunction(f, t_range=(0.0, 1.0, 0.004),
                                  color=cor, stroke_width=5.5)

    def _envelope_fn(self):
        n = int(round(self.modo.get_value()))
        a = self.amp.get_value()
        if n == 0 or a < 0.02:
            return VGroup()

        def mk(sinal):
            return ParametricFunction(
                lambda t: np.array([xde(t), Y_STR + sinal * a * np.sin(n * np.pi * t), 0.0]),
                t_range=(0.0, 1.0, 0.01), color=GRUV_GRAY, stroke_width=1.6,
                fill_color=GRUV_GRAY, fill_opacity=0.14, stroke_opacity=0.45,
            )

        return VGroup(mk(1), mk(-1))

    # ———————————————— PARTE 3 · O monocórdio ————————————————
    def _monocordio(self):
        amp, modo = self.amp, self.modo

        cab = VGroup(
            Text("O Monocórdio", font=FONT, color=GRUV_FG, font_size=50),
            Text("a mesma corda, agora em seus modos", font=FONT, color=GRUV_AQUA,
                 font_size=28, slant=ITALIC),
        ).arrange(DOWN, buff=0.18).move_to([0.0, 3.1, 0.0])
        self.play(FadeIn(cab), run_time=1.0)

        Y_SEG = -0.85

        def segmentos(n):
            cor = MODOS[n][0]
            g = VGroup()
            for i in range(n):
                a, b = xde(i / n) + 0.07, xde((i + 1) / n) - 0.07
                g.add(Line([a, Y_SEG, 0], [b, Y_SEG, 0], color=cor, stroke_width=4))
                g.add(Line([a, Y_SEG - 0.09, 0], [a, Y_SEG + 0.09, 0], color=cor, stroke_width=2.5))
                g.add(Line([b, Y_SEG - 0.09, 0], [b, Y_SEG + 0.09, 0], color=cor, stroke_width=2.5))
                g.add(Text(f"1/{n}" if n > 1 else "1", font=FONT, color=cor, font_size=24)
                      .move_to([(a + b) / 2, Y_SEG - 0.38, 0]))
            return g

        def nos(n):
            g = VGroup()
            for i in range(1, n):
                g.add(Dot([xde(i / n), Y_STR, 0], radius=0.075, color=GRUV_RED))
                g.add(DashedLine([xde(i / n), Y_STR - 0.95, 0], [xde(i / n), Y_STR + 0.95, 0],
                                 color=GRUV_GRAY, stroke_width=2).set_opacity(0.4))
            if n > 1:
                g.add(Triangle(color=GRUV_YELLOW, stroke_width=2.5,
                               fill_color=GRUV_DARK, fill_opacity=0.95)
                      .scale(0.2).move_to([xde(1 / n), Y_STR - 0.22, 0]))
            return g

        def rotulos(n):
            cor, nota, raz, grego, _ = MODOS[n]
            linhas = VGroup(
                Text(nota, font=FONT, color=cor, font_size=40),
                Text(raz, font=FONT, color=GRUV_FG, font_size=30),
                Text(grego, font=FONT, color=GRUV_BLUE, font_size=26, slant=ITALIC),
            ).arrange(DOWN, buff=0.14)
            linhas.move_to([0.0, -2.55, 0.0])
            if n in ENTRE:
                linhas.add(Text("em relação ao modo anterior  →  " + ENTRE[n], font=FONT,
                                color=GRUV_YELLOW, font_size=24)
                           .next_to(linhas, DOWN, buff=0.16))
                linhas.move_to([0.0, -2.7, 0.0])
            return linhas

        seg = segmentos(1)
        no = nos(1)
        rot = rotulos(1)
        self.play(FadeIn(seg), FadeIn(rot), amp.animate.set_value(AMP), run_time=0.9)
        self.tocar(MODOS[1][4])
        self.wait(3.2)

        for n in (2, 3, 4):
            self.play(amp.animate.set_value(0.0), FadeOut(seg), FadeOut(rot), FadeOut(no),
                      run_time=0.55)
            modo.set_value(n)
            seg, no, rot = segmentos(n), nos(n), rotulos(n)
            self.play(FadeIn(seg), FadeIn(no), FadeIn(rot),
                      amp.animate.set_value(AMP), run_time=0.9)
            self.tocar(MODOS[n][4])
            self.wait(3.4)

        self.play(amp.animate.set_value(0.0), FadeOut(seg), FadeOut(rot), FadeOut(no),
                  run_time=0.55)
        modo.set_value(0)
        fim = VGroup(
            Text("Harmonia Mundi", font=FONT, color=GRUV_YELLOW, font_size=50, slant=ITALIC),
            Text("uma corda real vibra em todos os modos ao mesmo tempo",
                 font=FONT, color=GRUV_FG, font_size=28),
            Text("1 : 2 : 3 : 4  —  o número tornado som", font=FONT, color=GRUV_AQUA,
                 font_size=26, slant=ITALIC),
        ).arrange(DOWN, buff=0.2).move_to([0.0, -2.35, 0.0])
        self.play(FadeIn(fim), amp.animate.set_value(AMP), run_time=1.0)
        for w in ("harpa_la_220.wav", "harpa_la4_440.wav", "harpa_mi5_660.wav", "harpa_la5_880.wav"):
            self.tocar(w)
        self.wait(5.0)

        self.play(amp.animate.set_value(0.0), FadeOut(fim), FadeOut(cab), run_time=1.0)
        self.play(FadeOut(self.pinos), run_time=0.5)
        self.remove(self.vib, self.env, self.fase)
        self.wait(0.3)
