"""
MISTAGOGOS · teste do monocórdio parte 2
A corda dividida: 1:1 → 1:2 → 1:3 → 1:4
Lá 220 → Lá⁴ 440 → Mi⁵ 660 → Lá⁵ 880 · dedilhado de harpa (Karplus-Strong)
Paleta Gruvbox · Tipografia EB Garamond · cavalete móvel + Transform
"""

from pathlib import Path

import numpy as np

from manim import (
    DashedLine,
    Dot,
    DOWN,
    FadeIn,
    FadeOut,
    ITALIC,
    Line,
    ParametricFunction,
    Scene,
    Text,
    Transform,
    Triangle,
    VGroup,
    ValueTracker,
    always_redraw,
    rate_functions,
)

# ———— Paleta Gruvbox ————
GRUV_BG = "#282828"      # fundo
GRUV_FG = "#ebdbb2"     # corda · texto principal
GRUV_YELLOW = "#fabd2f" # Lá⁴ · cavalete
GRUV_GREEN = "#b8bb26"  # Lá
GRUV_ORANGE = "#fe8019" # Mi⁵
GRUV_AQUA = "#8ec07c"   # Lá⁵ · cabeçalho
GRUV_RED = "#cc241d"    # nós de divisão
GRUV_GRAY = "#a89984"   # pinos · corda dampada
GRUV_DARK = "#3c3833"   # corpo do cavalete

FONT = "EB Garamond"
SONS = Path(__file__).resolve().parent / "sons"  # pasta sons/ ao lado do script

X0, X1 = -5.0, 5.0
SPAN = X1 - X0
Y_STR = 0.40
A_AMP = 0.60
SPEED = 4.0


def xde(frac):
    return X0 + SPAN * frac


class Monocordio(Scene):
    def construct(self):
        self.camera.background_color = GRUV_BG

        # ———— Rastreadores globais ————
        tb = ValueTracker(1.0)    # posição do cavalete (fração da corda)
        amp = ValueTracker(0.0)   # amplitude vibrante
        fase = ValueTracker(0.0)
        fase.add_updater(lambda m, dt: m.increment_value(SPEED * dt))
        self.add(fase)

        # ———— Cabeçalho ————
        cab = Text("O Monocórdio · a corda dividida", font=FONT, color=GRUV_AQUA,
                   font_size=40, slant=ITALIC).move_to([0.0, 3.5, 0.0])

        # ———— Corda: segmento vibrante + resto dampado ————
        def vibrante():
            t = tb.get_value()
            a = amp.get_value()
            ph = fase.get_value()

            def f(u):
                return np.array(
                    [xde(u),
                     Y_STR + a * np.sin(np.pi * u / t) * np.cos(ph),
                     0.0]
                )

            return ParametricFunction(f, t_range=(0.0, t, 0.004),
                                      color=GRUV_FG, stroke_width=5.0)

        vib = always_redraw(vibrante)

        def resto():
            t = tb.get_value()
            if t > 0.995:
                return Line([X1, Y_STR, 0.0], [X1, Y_STR, 0.0],
                            color=GRUV_GRAY, stroke_width=2.5).set_opacity(0.0)
            return DashedLine([xde(t), Y_STR, 0.0], [X1, Y_STR, 0.0],
                              color=GRUV_GRAY,
                              stroke_width=2.5).set_opacity(0.5)

        res = always_redraw(resto)

        def ponte():
            t = tb.get_value()
            return Triangle(color=GRUV_YELLOW, stroke_width=2.5,
                            fill_color=GRUV_DARK, fill_opacity=0.95,
                            ).scale(0.24).move_to([xde(t), Y_STR - 0.20, 0.0])

        cav = always_redraw(ponte)

        pinos = VGroup(
            Dot([X0, Y_STR, 0.0], radius=0.08, color=GRUV_GRAY),
            Dot([X1, Y_STR, 0.0], radius=0.08, color=GRUV_GRAY),
        )

        # ———— Rótulos (trocados por Transform, sem cortes) ————
        nota = Text("Lá · 220 Hz", font=FONT, color=GRUV_GREEN,
                    font_size=38).move_to([0.0, -1.55, 0.0])
        raz = Text("corda inteira · 1:1", font=FONT, color=GRUV_FG,
                   font_size=30).move_to([0.0, -2.25, 0.0])

        def troca(txt_nota, cor_nota, txt_raz):
            nova = Text(txt_nota, font=FONT, color=cor_nota,
                        font_size=38).move_to(nota)
            nvz = Text(txt_raz, font=FONT, color=GRUV_FG,
                       font_size=30).move_to(raz)
            self.play(Transform(nota, nova), Transform(raz, nvz), run_time=0.7)

        # ———— Nós das divisões ————
        def no(frac):
            return Dot([xde(frac), Y_STR, 0.0], radius=0.07, color=GRUV_RED)

        no_12 = no(0.5)
        nos_13 = VGroup(no(1 / 3), no(2 / 3))
        nos_14 = VGroup(no(0.25), no(0.75))

        def dedilha(wav, ring):
            """Punzeia: som + amplitude instantânea + decaimento suave."""
            self.add_sound(str(SONS / wav))
            self.play(amp.animate.set_value(A_AMP), run_time=0.12,
                      rate_func=rate_functions.rush_into)
            self.wait(ring)
            self.play(amp.animate.set_value(0.0), run_time=0.5)

        # ———— Abertura ————
        self.play(FadeIn(cab), run_time=1.0)
        self.play(FadeIn(pinos), run_time=0.4)
        corda_repouso = Line([X0, Y_STR, 0.0], [X1, Y_STR, 0.0],
                             color=GRUV_FG, stroke_width=5.0)
        self.play(FadeIn(corda_repouso), FadeIn(nota), FadeIn(raz), run_time=0.6)
        self.remove(corda_repouso)
        self.add(vib, res)  # corda viva: segmento vibrante + resto dampado

        # ———— 1 · Corda inteira · Lá 220 Hz ————
        dedilha("harpa_la_220.wav", 1.6)

        # ———— 2 · Metade · Lá⁴ 440 Hz (cavalete desliza até 1/2) ————
        self.play(FadeIn(cav), tb.animate.set_value(0.5), run_time=1.0)
        dedilha("harpa_la4_440.wav", 1.3)
        self.play(FadeIn(no_12), run_time=0.3)
        troca("Lá⁴ · 440 Hz", GRUV_YELLOW, "metade · 1:2")

        # ———— 3 · Um terço · Mi⁵ 660 Hz ————
        self.play(tb.animate.set_value(1 / 3), run_time=0.9)
        dedilha("harpa_mi5_660.wav", 1.2)
        self.play(FadeIn(nos_13), run_time=0.3)
        troca("Mi⁵ · 660 Hz", GRUV_ORANGE, "um terço · 1:3")

        # ———— 4 · Um quarto · Lá⁵ 880 Hz ————
        self.play(tb.animate.set_value(0.25), run_time=0.8)
        dedilha("harpa_la5_880.wav", 1.1)
        self.play(FadeIn(nos_14), run_time=0.3)
        troca("Lá⁵ · 880 Hz", GRUV_AQUA, "um quarto · 1:4")

        # ———— Final: cavalete liberado · morfismo 1 → 2 → 3 → 4 ————
        self.play(tb.animate.set_value(1.0), run_time=0.9)
        self.remove(vib, res, cav)

        modo = ValueTracker(1.0)

        def modo_vib():
            m = modo.get_value()
            a = amp.get_value()
            ph = fase.get_value()

            def f(t):
                y = (Y_STR
                     + a * np.sin(m * np.pi * t) * np.sin(np.pi * t)
                     * np.cos(ph))
                return np.array([xde(t), y, 0.0])

            return ParametricFunction(f, t_range=(0.0, 1.0, 0.004),
                                      color=GRUV_FG, stroke_width=5.0)

        mvib = always_redraw(modo_vib)
        self.add(mvib)

        # Arpejo de harpa acompanhando o desenhar dos modos
        self.play(amp.animate.set_value(0.55), run_time=0.1)
        self.add_sound(str(SONS / "harpa_la_220.wav"))
        self.wait(0.45)
        self.play(modo.animate.set_value(2.0), run_time=0.55)
        self.add_sound(str(SONS / "harpa_la4_440.wav"))
        self.wait(0.4)
        self.play(modo.animate.set_value(3.0), run_time=0.6)
        self.add_sound(str(SONS / "harpa_mi5_660.wav"))
        self.wait(0.4)
        self.play(modo.animate.set_value(4.0), run_time=0.7)
        self.add_sound(str(SONS / "harpa_la5_880.wav"))
        self.wait(0.9)

        fim = VGroup(
            Text("Harmonia Mundi", font=FONT, color=GRUV_YELLOW,
                 font_size=48, slant=ITALIC),
            Text("quatro modos · uma corda", font=FONT, color=GRUV_FG,
                 font_size=26),
        ).arrange(DOWN, buff=0.2).move_to([0.0, -3.15, 0.0])
        self.play(FadeIn(fim), run_time=0.8)
        self.wait(1.8)

        # ———— Encerramento ————
        self.play(amp.animate.set_value(0.0), run_time=0.6)
        self.remove(mvib, fase, tb, amp, modo)
        self.play(FadeOut(cab), FadeOut(pinos), FadeOut(nota), FadeOut(raz),
                  FadeOut(no_12), FadeOut(nos_13), FadeOut(nos_14),
                  FadeOut(fim), run_time=0.8)
        self.wait(0.3)
