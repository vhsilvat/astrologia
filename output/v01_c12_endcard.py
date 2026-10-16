"""
MISTAGOGOS · v01 · c12 — End Card
MISTAGOGOS + «a iniciação continua» · teaser do próximo vídeo · o cubo
isométrico (âncora de c11) orbita o logotipo, girando devagar.

Paleta Gruvbox · EB Garamond · sons em sons/ (se faltar um arquivo, roda muda)
"""

from pathlib import Path

import numpy as np

from manim import (
    DEGREES,
    DOWN,
    ITALIC,
    Circle,
    FadeIn,
    Polygon,
    Scene,
    Text,
    VGroup,
    ValueTracker,
    always_redraw,
)

# ———— Paleta Gruvbox ————
GRUV_BG = "#282828"
GRUV_FG = "#ebdbb2"
GRUV_AQUA = "#8ec07c"
GRUV_GRAY = "#a89984"
GRUV_DARK = "#3c3833"

FONT = "EB Garamond"
SONS = Path(__file__).resolve().parent / "sons"


class EndCard(Scene):
    def tocar(self, wav, **kwargs):
        caminho = SONS / wav
        if caminho.exists():
            self.add_sound(str(caminho), **kwargs)

    def construct(self):
        self.camera.background_color = GRUV_BG
        self.tocar("acorde_harmonico.wav", gain=-6)
        self.tocar("tic_relogio.wav", gain=-10)

        titulo = VGroup(
            Text("MISTAGOGOS", font=FONT, color=GRUV_FG, font_size=80),
            Text("a iniciação continua", font=FONT, color=GRUV_AQUA,
                 font_size=30, slant=ITALIC),
        ).arrange(DOWN, buff=0.26).move_to([0.0, 0.5, 0.0])
        self.play(FadeIn(titulo, shift=0.15 * DOWN), run_time=1.0)

        # ———— o cubo isométrico orbitando o logotipo ————
        orbita_ang = ValueTracker(0.0)
        orbita_ang.add_updater(lambda m, dt: m.increment_value(0.6 * dt))
        giro = ValueTracker(0.0)
        giro.add_updater(lambda m, dt: m.increment_value(0.8 * dt))
        self.add(orbita_ang, giro)

        def cubo():
            s = 0.22
            g = giro.get_value()
            angs = [90, 150, 210, 270, 330, 30]
            p = [s * np.array([np.cos((a + g / DEGREES) * DEGREES),
                               np.sin((a + g / DEGREES) * DEGREES), 0.0])
                 for a in angs]
            o = np.array([0.0, 0.0, 0.0])
            topo = Polygon(o, p[0], p[1], p[2], color=GRUV_GRAY, stroke_width=1.3,
                          fill_color=GRUV_FG, fill_opacity=0.9)
            direita = Polygon(o, p[2], p[3], p[4], color=GRUV_GRAY, stroke_width=1.3,
                             fill_color=GRUV_GRAY, fill_opacity=0.9)
            esquerda = Polygon(o, p[4], p[5], p[0], color=GRUV_GRAY, stroke_width=1.3,
                              fill_color=GRUV_DARK, fill_opacity=0.9)
            r_orb = 2.6
            a_orb = orbita_ang.get_value()
            centro = np.array([r_orb * np.cos(a_orb), 0.5 + 0.5 * np.sin(a_orb), 0.0])
            return VGroup(direita, esquerda, topo).move_to(centro)

        cubo_vis = always_redraw(cubo)
        self.add(cubo_vis)
        self.wait(0.6)

        teaser = Text("próximo — os sólidos platônicos · os quatro elementos · Jung",
                      font=FONT, color=GRUV_GRAY, font_size=24).move_to([0.0, -2.3, 0.0])
        self.play(FadeIn(teaser), run_time=0.9)
        self.wait(10.5)

        orbita_ang.clear_updaters()
        giro.clear_updaters()
        self.wait(1.0)
