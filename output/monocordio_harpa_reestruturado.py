"""
MISTAGOGOS · O Monocórdio — a corda inteira em vários modos
Estilo Robert Fludd: UMA corda, sempre inteira, vibrando em modos 1 → 2 → 3 → 4.
Os nós ficam parados; os ventres oscilam em sentidos alternados.
Paleta Gruvbox · EB Garamond · sons em sons/ (se faltar um arquivo, a cena roda muda)
"""

from pathlib import Path

import numpy as np

from manim import (
    DashedLine,
    DOWN,
    Dot,
    FadeIn,
    FadeOut,
    ITALIC,
    Line,
    ParametricFunction,
    Scene,
    Text,
    Triangle,
    VGroup,
    ValueTracker,
    always_redraw,
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
GRUV_DARK = "#3c3833"

FONT = "EB Garamond"
SONS = Path(__file__).resolve().parent / "sons"

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
# intervalo entre o modo n e o modo anterior (as razões superparticulares)
ENTRE = {2: "2:1 · oitava", 3: "3:2 · quinta", 4: "4:3 · quarta"}


def xde(frac):
    return X0 + SPAN * frac


class Monocordio(Scene):
    def tocar(self, wav):
        caminho = SONS / wav
        if caminho.exists():
            self.add_sound(str(caminho))

    def construct(self):
        self.camera.background_color = GRUV_BG

        fase = ValueTracker(0.0)
        fase.add_updater(lambda m, dt: m.increment_value(SPEED * dt))
        self.add(fase)

        amp = ValueTracker(0.0)
        modo = ValueTracker(1.0)  # 1..4 = modo puro · 0 = todos somados

        # ———— A corda: sempre inteira ————
        def corda():
            n = int(round(modo.get_value()))
            a = amp.get_value()
            ph = fase.get_value()
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

        vib = always_redraw(corda)

        # ———— Envelope fantasma: a "forma" do modo (±) ————
        def envelope():
            n = int(round(modo.get_value()))
            a = amp.get_value()
            if n == 0 or a < 0.02:
                return VGroup()

            def mk(sinal):
                return ParametricFunction(
                    lambda t: np.array([xde(t), Y_STR + sinal * a * np.sin(n * np.pi * t), 0.0]),
                    t_range=(0.0, 1.0, 0.01), color=GRUV_GRAY, stroke_width=1.6,
                    fill_color=GRUV_GRAY, fill_opacity=0.14, stroke_opacity=0.45,
                )

            return VGroup(mk(1), mk(-1))

        env = always_redraw(envelope)

        pinos = VGroup(
            Dot([X0, Y_STR, 0.0], radius=0.09, color=GRUV_GRAY),
            Dot([X1, Y_STR, 0.0], radius=0.09, color=GRUV_GRAY),
        )

        # ———— Cabeçalho ————
        cab = VGroup(
            Text("O Monocórdio", font=FONT, color=GRUV_FG, font_size=50),
            Text("uma só corda, muitos modos", font=FONT, color=GRUV_AQUA,
                 font_size=28, slant=ITALIC),
        ).arrange(DOWN, buff=0.18).move_to([0.0, 3.1, 0.0])

        # ———— Elementos que dependem de n ————
        Y_SEG = -0.85

        def segmentos(n):
            """n pedaços iguais abaixo da corda, com a fração de cada um."""
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
            """Nós (parados) + um toque leve no primeiro, como no harmônico de harpa."""
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

        # ———— Abertura ————
        self.play(FadeIn(cab), run_time=1.0)
        repouso = Line([X0, Y_STR, 0], [X1, Y_STR, 0], color=GRUV_FG, stroke_width=5.5)
        self.play(FadeIn(pinos), FadeIn(repouso), run_time=0.7)
        self.remove(repouso)
        self.add(env, vib)

        seg = segmentos(1)
        no = nos(1)
        rot = rotulos(1)
        self.play(FadeIn(seg), FadeIn(rot), amp.animate.set_value(AMP), run_time=0.9)
        self.tocar(MODOS[1][4])
        self.wait(3.2)

        # ———— Modos 2, 3, 4: a mesma corda, mais ventres ————
        for n in (2, 3, 4):
            self.play(amp.animate.set_value(0.0), FadeOut(seg), FadeOut(rot), FadeOut(no),
                      run_time=0.55)
            modo.set_value(n)
            seg, no, rot = segmentos(n), nos(n), rotulos(n)
            self.play(FadeIn(seg), FadeIn(no), FadeIn(rot),
                      amp.animate.set_value(AMP), run_time=0.9)
            self.tocar(MODOS[n][4])
            self.wait(3.4)

        # ———— Tudo ao mesmo tempo: a corda real ————
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

        # ———— Encerramento ————
        self.play(amp.animate.set_value(0.0), FadeOut(fim), FadeOut(cab), run_time=1.0)
        self.play(FadeOut(pinos), run_time=0.5)
        self.remove(vib, env, fase)
        self.wait(0.3)
