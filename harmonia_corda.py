"""
MISTAGOGOS · teste de ambiente
Harmônicos de uma corda vibrante — proporções pitagóricas 1:2 (metades) e 1:3 (terços)
Paleta Gruvbox · Tipografia EB Garamond · Tons reais (220 / 440 / 660 Hz) via Scene.add_sound
"""

import numpy as np

from manim import (
    Create,
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
    VGroup,
    ValueTracker,
    Write,
    always_redraw,
)

# ———— Paleta Gruvbox ————
GRUV_BG = "#282828"      # fundo
GRUV_FG = "#ebdbb2"      # texto e linhas principais
GRUV_YELLOW = "#fabd2f"  # destaques
GRUV_GREEN = "#b8bb26"   # frequências · 3º harmônico
GRUV_RED = "#cc241d"     # nós de divisão
GRUV_AQUA = "#8ec07c"   # subtítulo
GRUV_BLUE = "#83a598"   # rótulos laterais (f · 2f · 3f)
GRUV_GRAY = "#a89984"   # apoios · guias tracejadas

FONT = "EB Garamond"
SONS = "/a0/usr/projects/musicofthespheres/sons"

X0, X1 = -3.0, 3.0
SPAN = X1 - X0
Y_MAIN = 0.0
AMP = 0.62
PHASE_SPEED = 4.0


class HarmoniaCorda(Scene):
    def construct(self):
        self.camera.background_color = GRUV_BG

        # Fase global: mantém todos os modos oscilando continuamente.
        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: m.increment_value(PHASE_SPEED * dt))
        self.add(phase)

        amp1 = ValueTracker(0.0)
        amp2 = ValueTracker(0.0)
        amp3 = ValueTracker(0.0)

        def fio(n, tracker, y, color):
            """Corda vibrante no modo n; amplitude lida de um ValueTracker."""

            def build():
                ph = phase.get_value()
                a = tracker.get_value()

                def curva(t):
                    return np.array(
                        [
                            X0 + SPAN * t,
                            y + a * np.sin(n * np.pi * t) * np.cos(n * ph),
                            0.0,
                        ]
                    )

                return ParametricFunction(
                    curva,
                    t_range=(0.0, 1.0, 0.005),
                    color=color,
                    stroke_width=5.0,
                )

            return always_redraw(build)

        f1 = fio(1, amp1, Y_MAIN, GRUV_FG)
        f2 = fio(2, amp2, Y_MAIN, GRUV_YELLOW)
        f3 = fio(3, amp3, Y_MAIN, GRUV_GREEN)

        def rotulo(l1, l2, l3):
            return VGroup(
                Text(l1, font=FONT, color=GRUV_FG, font_size=34),
                Text(l2, font=FONT, color=GRUV_YELLOW, font_size=29),
                Text(l3, font=FONT, color=GRUV_GREEN, font_size=29),
            ).arrange(DOWN, buff=0.12).move_to([0.0, -1.75, 0.0])

        # ———— Cabeçalho ————
        cabecalho = VGroup(
            Text("Harmônicos da Corda Vibrante",
                 font=FONT, color=GRUV_FG, font_size=52),
            Text("as proporções pitagóricas do som",
                 font=FONT, color=GRUV_AQUA, font_size=30, slant=ITALIC),
        ).arrange(DOWN, buff=0.22).move_to([0.0, 3.1, 0.0])

        corda_repouso = Line([X0, Y_MAIN, 0.0], [X1, Y_MAIN, 0.0],
                             color=GRUV_FG, stroke_width=5.0)
        apoios = VGroup(
            Dot([X0, Y_MAIN, 0.0], radius=0.07, color=GRUV_GRAY),
            Dot([X1, Y_MAIN, 0.0], radius=0.07, color=GRUV_GRAY),
        )

        # ———— 1 · Fundamental (corda inteira) ————
        self.play(Write(cabecalho), run_time=1.2)
        self.play(Create(corda_repouso), run_time=0.9)
        self.play(FadeIn(apoios), run_time=0.4)
        self.remove(corda_repouso)
        self.add(f1)
        rot_a = rotulo("Fundamental", "corda inteira · 1:1", "f = 220 Hz")
        self.play(FadeIn(rot_a), amp1.animate.set_value(AMP), run_time=1.0)
        self.add_sound(f"{SONS}/tom_fundamental_220.wav")
        self.wait(2.9)

        # ———— 2 · Metades (1:2 → oitava) ————
        divisao_b = VGroup(
            DashedLine([0.0, Y_MAIN - 0.85, 0.0], [0.0, Y_MAIN + 0.85, 0.0],
                       color=GRUV_GRAY, stroke_width=2.0).set_opacity(0.45),
            Dot([0.0, Y_MAIN, 0.0], radius=0.06, color=GRUV_RED),
        )
        self.play(amp1.animate.set_value(0.0), FadeOut(rot_a), run_time=0.55)
        self.remove(f1)
        self.add(f2)
        rot_b = rotulo("2º harmônico", "metades · 1:2 · oitava", "2f = 440 Hz")
        self.play(FadeIn(divisao_b), FadeIn(rot_b),
                  amp2.animate.set_value(AMP), run_time=1.0)
        self.add_sound(f"{SONS}/tom_oitava_440.wav")
        self.wait(2.9)

        # ———— 3 · Terços (1:3 → quinta) ————
        x_t = X0 + SPAN / 3
        x_q = X0 + 2 * SPAN / 3
        divisao_c = VGroup(
            DashedLine([x_t, Y_MAIN - 0.85, 0.0], [x_t, Y_MAIN + 0.85, 0.0],
                       color=GRUV_GRAY, stroke_width=2.0).set_opacity(0.45),
            Dot([x_t, Y_MAIN, 0.0], radius=0.06, color=GRUV_RED),
            DashedLine([x_q, Y_MAIN - 0.85, 0.0], [x_q, Y_MAIN + 0.85, 0.0],
                       color=GRUV_GRAY, stroke_width=2.0).set_opacity(0.45),
            Dot([x_q, Y_MAIN, 0.0], radius=0.06, color=GRUV_RED),
        )
        self.play(amp2.animate.set_value(0.0),
                  FadeOut(rot_b), FadeOut(divisao_b), run_time=0.55)
        self.remove(f2, divisao_b)
        self.add(f3)
        rot_c = rotulo("3º harmônico", "terços · 1:3 · quinta", "3f = 660 Hz")
        self.play(FadeIn(divisao_c), FadeIn(rot_c),
                  amp3.animate.set_value(AMP), run_time=1.0)
        self.add_sound(f"{SONS}/tom_quinta_660.wav")
        self.wait(2.9)

        # ———— 4 · Os três modos juntos: Harmonia Mundi ————
        self.play(amp3.animate.set_value(0.0),
                  FadeOut(rot_c), FadeOut(divisao_c), run_time=0.55)
        self.remove(f3, divisao_c, apoios)

        ys = [1.05, 0.0, -1.05]
        cores = [GRUV_FG, GRUV_YELLOW, GRUV_GREEN]
        divisoes = ["1:1", "1:2", "1:3"]
        freqs = ["f", "2f", "3f"]
        TRIO_AMP = 0.32

        trio = [
            fio(1, amp1, ys[0], GRUV_FG),
            fio(2, amp2, ys[1], GRUV_YELLOW),
            fio(3, amp3, ys[2], GRUV_GREEN),
        ]
        lateral = VGroup()
        for i in range(3):
            lateral.add(
                Text(divisoes[i], font=FONT, color=cores[i],
                     font_size=28).move_to([X0 - 0.55, ys[i], 0.0]),
                Text(freqs[i], font=FONT, color=GRUV_BLUE,
                     font_size=28).move_to([X1 + 0.55, ys[i], 0.0]),
            )
        for fio_ativo in trio:
            self.add(fio_ativo)

        final_txt = VGroup(
            Text("Harmonia Mundi", font=FONT, color=GRUV_YELLOW,
                 font_size=50, slant=ITALIC),
            Text("a corda inteira contém todos os seus harmônicos",
                 font=FONT, color=GRUV_FG, font_size=30),
        ).arrange(DOWN, buff=0.22).move_to([0.0, -2.45, 0.0])

        self.play(FadeIn(lateral),
                  amp1.animate.set_value(TRIO_AMP),
                  amp2.animate.set_value(TRIO_AMP),
                  amp3.animate.set_value(TRIO_AMP),
                  run_time=1.0)
        self.add_sound(f"{SONS}/acorde_harmonico.wav")
        self.play(FadeIn(final_txt), run_time=0.6)
        self.wait(4.0)

        # ———— Encerramento ————
        self.play(amp1.animate.set_value(0.0),
                  amp2.animate.set_value(0.0),
                  amp3.animate.set_value(0.0),
                  FadeOut(lateral),
                  FadeOut(final_txt),
                  FadeOut(cabecalho),
                  run_time=1.0)
        self.remove(*trio, lateral, final_txt, cabecalho)
        self.wait(0.4)
