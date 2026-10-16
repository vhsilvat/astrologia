"""
MISTAGOGOS · v01 · c01 — Abertura (cold open)
Anel zodiacal fino, girando devagar; o tick do topo (0° Áries) realçado.
Saturno e Netuno convergem ao tick — ao se tocarem, um ting distante de
bigorna e uma onda expansiva discreta. MISTAGOGOS surge.
Saída: zoom no anel → c02.

Paleta Gruvbox · EB Garamond · sons em sons/ (se faltar um arquivo, roda muda)
"""

from pathlib import Path

import numpy as np

from manim import (
    DEGREES,
    DOWN,
    ITALIC,
    UP,
    Annulus,
    Circle,
    Dot,
    FadeIn,
    Line,
    MovingCameraScene,
    Text,
    VGroup,
    ValueTracker,
    always_redraw,
    rate_functions,
)

# ———— Paleta Gruvbox ————
GRUV_BG = "#282828"
GRUV_FG = "#ebdbb2"
GRUV_AQUA = "#8ec07c"
GRUV_YELLOW = "#fabd2f"
GRUV_GRAY = "#a89984"
GRUV_DARK = "#3c3833"

FONT = "EB Garamond"
SONS = Path(__file__).resolve().parent / "sons"

R_ANEL = 3.0


def ponto(theta_deg, raio):
    rad = (theta_deg + 90) * DEGREES
    return np.array([raio * np.cos(rad), raio * np.sin(rad), 0.0])


class Abertura(MovingCameraScene):
    def tocar(self, wav, **kwargs):
        caminho = SONS / wav
        if caminho.exists():
            self.add_sound(str(caminho), **kwargs)

    def construct(self):
        self.camera.background_color = GRUV_BG
        self.tocar("drone_esferas.wav", gain=-12)

        # ———— O anel zodiacal ————
        anel = Annulus(inner_radius=R_ANEL - 0.06, outer_radius=R_ANEL + 0.06,
                       color=GRUV_DARK, fill_opacity=1.0, stroke_width=0)
        ticks = VGroup()
        for i in range(12):
            th = i * 30
            cor = GRUV_YELLOW if i == 0 else GRUV_GRAY
            largura = 3.5 if i == 0 else 1.6
            ticks.add(Line(ponto(th, R_ANEL - 0.22), ponto(th, R_ANEL + 0.22),
                           color=cor, stroke_width=largura))

        grupo_anel = VGroup(anel, ticks)
        self.play(FadeIn(grupo_anel), run_time=1.2)
        self.wait(14.5)

        # ———— Saturno e Netuno convergem ao tick do topo ————
        theta_sat = ValueTracker(-150.0)
        theta_net = ValueTracker(150.0)
        saturno = always_redraw(lambda: VGroup(
            Dot(ponto(theta_sat.get_value(), R_ANEL), radius=0.08, color=GRUV_GRAY),
            Circle(radius=0.14, color=GRUV_GRAY, stroke_width=1.3)
                .move_to(ponto(theta_sat.get_value(), R_ANEL)),
        ))
        netuno = always_redraw(lambda: Dot(ponto(theta_net.get_value(), R_ANEL),
                                           radius=0.09, color=GRUV_AQUA))
        self.add(saturno, netuno)
        self.play(theta_sat.animate.set_value(0.0), theta_net.animate.set_value(0.0),
                  run_time=5.0, rate_func=rate_functions.ease_in_out_sine)

        # ———— O encontro: ting + onda expansiva ————
        self.tocar("martelo_agudo_440.wav", gain=-16)
        onda = Circle(radius=0.2, color=GRUV_FG, stroke_width=4.0).move_to(ponto(0, R_ANEL))
        self.add(onda)
        self.play(onda.animate.scale(4.0).set_opacity(0), run_time=1.1)
        self.remove(onda)
        self.wait(2.0)

        # ———— MISTAGOGOS ————
        titulo = VGroup(
            Text("MISTAGOGOS", font=FONT, color=GRUV_FG, font_size=80),
            Text("a arquitetura oculta da realidade", font=FONT, color=GRUV_AQUA,
                 font_size=30, slant=ITALIC),
        ).arrange(DOWN, buff=0.28).move_to([0.0, -0.1, 0.0])
        self.play(FadeIn(titulo, shift=0.2 * UP), run_time=1.4)
        self.wait(4.2)

        # ———— Saída: zoom no anel ————
        self.play(self.camera.frame.animate.scale(0.3).move_to(ponto(0, R_ANEL)),
                  run_time=1.8)
        self.wait(1.0)
