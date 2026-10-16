"""
MISTAGOGOS · v01 · c07 — O Peixe na Água
Uma onda ambiente lenta atravessa a tela, amplitude decaindo até quase
zero — mas nunca zero: o próprio frame continua "escutando". Um peixe
vetorial mínimo nada contra a onda. «O peixe não percebe a água» → «o
silêncio é a escuta contínua». Saída: os pontos da onda condensam —
âncora para o tetraktys (c08).

Paleta Gruvbox · EB Garamond · sons em sons/ (se faltar um arquivo, roda muda)
"""

from pathlib import Path

import numpy as np

from manim import (
    ITALIC,
    Dot,
    Ellipse,
    FadeIn,
    FadeOut,
    ParametricFunction,
    Polygon,
    Scene,
    Text,
    Transform,
    VGroup,
    ValueTracker,
    always_redraw,
)

# ———— Paleta Gruvbox ————
GRUV_BG = "#282828"
GRUV_FG = "#ebdbb2"
GRUV_GREEN = "#b8bb26"
GRUV_GRAY = "#a89984"

FONT = "EB Garamond"
SONS = Path(__file__).resolve().parent / "sons"

X0, X1 = -6.0, 6.0


class PeixeAgua(Scene):
    def tocar(self, wav, **kwargs):
        caminho = SONS / wav
        if caminho.exists():
            self.add_sound(str(caminho), **kwargs)

    def construct(self):
        self.camera.background_color = GRUV_BG
        self.tocar("drone_esferas.wav", gain=-14)
        self.tocar("whoosh_agua.wav", gain=-18)

        # ———— A onda ambiente: amplitude decai, nunca chega a zero ————
        fase = ValueTracker(0.0)
        fase.add_updater(lambda m, dt: m.increment_value(1.2 * dt))
        amp = ValueTracker(0.5)
        self.add(fase)

        def onda():
            a = amp.get_value()
            ph = fase.get_value()
            return ParametricFunction(
                lambda t: np.array([t, 0.3 * a * np.sin(0.9 * t + ph), 0.0]),
                t_range=(X0, X1, 0.05), color=GRUV_GRAY, stroke_width=2.0,
            )

        onda_vis = always_redraw(onda)
        self.add(onda_vis)
        self.wait(0.3)

        # ———— O peixe: elipse + cauda, nadando contra a onda ————
        x_peixe = ValueTracker(X0 + 1.0)

        def peixe():
            x = x_peixe.get_value()
            a = amp.get_value()
            ph = fase.get_value()
            y = 0.3 * a * np.sin(0.9 * x + ph) + 0.35
            corpo = Ellipse(width=0.55, height=0.26, color=GRUV_GREEN, stroke_width=2.0,
                           fill_color=GRUV_GREEN, fill_opacity=0.85).move_to([x, y, 0.0])
            cauda = Polygon([x - 0.26, y, 0.0], [x - 0.42, y + 0.14, 0.0],
                           [x - 0.42, y - 0.14, 0.0], color=GRUV_GREEN,
                           fill_color=GRUV_GREEN, fill_opacity=0.85)
            return VGroup(corpo, cauda)

        peixe_vis = always_redraw(peixe)
        self.add(peixe_vis)

        self.play(amp.animate.set_value(0.5), x_peixe.animate.set_value(X0 + 2.5),
                  run_time=0.1)
        self.play(x_peixe.animate.set_value(X1 - 1.0), amp.animate.set_value(0.08),
                  run_time=9.0)

        texto1 = Text("o peixe não percebe a água", font=FONT, color=GRUV_FG,
                      font_size=34, slant=ITALIC).move_to([0.0, -2.6, 0.0])
        self.play(FadeIn(texto1), run_time=0.8)
        self.wait(2.2)

        texto2 = Text("o silêncio é a escuta contínua", font=FONT, color=GRUV_FG,
                      font_size=34, slant=ITALIC).move_to([0.0, -2.6, 0.0])
        self.play(Transform(texto1, texto2), run_time=0.8)
        self.wait(2.2)

        # ———— Saída: os pontos da onda condensam ————
        self.play(FadeOut(texto1), FadeOut(peixe_vis), run_time=0.6)
        self.remove(onda_vis)

        pontos = VGroup(*[Dot([x, 0.0, 0.0], radius=0.04, color=GRUV_GRAY)
                          for x in np.linspace(X0, X1, 40)])
        self.add(pontos)
        self.play(pontos.animate.arrange_in_grid(rows=1, buff=0.3).move_to([0.0, 0.0, 0.0]),
                  run_time=1.3)
        self.wait(0.3)
        self.remove(pontos, fase)
