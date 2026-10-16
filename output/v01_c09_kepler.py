"""
MISTAGOGOS · v01 · c09 — Kepler
A elipse do c08 ganha o Sol num foco; o planeta acelera no periélio e
desacelera no afélio — aproximação visual honesta da Segunda Lei de
Kepler (não uma integração física exata). Uma régua lateral acompanha
a razão aparente da velocidade angular, variando de 1:1 (afélio) a 2:1
(periélio) — cruzando no caminho as mesmas razões já ouvidas: 4:3 e 3:2.
Saída: zoom-out — esta elipse é uma entre outras.

Paleta Gruvbox · EB Garamond
"""

from pathlib import Path

import numpy as np

from manim import (
    DEGREES,
    DOWN,
    ITALIC,
    RIGHT,
    UP,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    MovingCameraScene,
    ParametricFunction,
    Text,
    TracedPath,
    always_redraw,
    ValueTracker,
)

# ———— Paleta Gruvbox ————
GRUV_BG = "#282828"
GRUV_FG = "#ebdbb2"
GRUV_YELLOW = "#fabd2f"
GRUV_GRAY = "#a89984"
GRUV_AQUA = "#8ec07c"

FONT = "EB Garamond"
SONS = Path(__file__).resolve().parent / "sons"

A, B = 3.0, 1.9
C = (A ** 2 - B ** 2) ** 0.5  # foco (Sol)
BASE_SPEED = 1.1
AMP = 1.0 / 3.0  # faz a razão periélio/afélio bater exatamente em 2:1


def pos(phi):
    return np.array([A * np.cos(phi), B * np.sin(phi), 0.0])


def vel(phi):
    return BASE_SPEED * (1 + AMP * np.cos(phi))


class Kepler(MovingCameraScene):
    def tocar(self, wav):
        caminho = SONS / wav
        if caminho.exists():
            self.add_sound(str(caminho))

    def construct(self):
        self.camera.background_color = GRUV_BG

        caption = Text("Kepler · Harmonices Mundi (1619)", font=FONT, color=GRUV_AQUA,
                       font_size=32, slant=ITALIC).move_to([0.0, 3.3, 0.0])
        self.play(FadeIn(caption), run_time=0.9)

        elipse = ParametricFunction(pos, t_range=(0.0, 2 * np.pi, 0.01),
                                    color=GRUV_FG, stroke_width=3.5)
        sol = Dot([C, 0.0, 0.0], radius=0.16, color=GRUV_YELLOW)
        self.play(FadeIn(elipse), run_time=1.0)
        self.play(FadeIn(sol), run_time=0.6)
        self.wait(0.3)

        # ———— O planeta, acelerando no periélio ————
        phi = ValueTracker(np.pi)  # começa no afélio
        phi.add_updater(lambda m, dt: m.increment_value(vel(m.get_value()) * dt))
        self.add(phi)

        planeta = always_redraw(lambda: Dot(pos(phi.get_value()), radius=0.11, color=GRUV_FG))
        trilha = TracedPath(lambda: pos(phi.get_value()), stroke_color=GRUV_YELLOW,
                            stroke_width=3.0, dissipating_time=1.2)
        self.add(trilha, planeta)
        self.wait(0.3)

        # ———— A régua lateral da razão instantânea ————
        rx = 5.0
        ry0, ry1 = -1.6, 1.6
        regua = Line([rx, ry0, 0.0], [rx, ry1, 0.0], color=GRUV_GRAY, stroke_width=2.0)
        lab_lento = Text("lento · afélio", font=FONT, color=GRUV_GRAY,
                         font_size=22).next_to([rx, ry0, 0.0], DOWN, buff=0.25)
        lab_rapido = Text("rápido · periélio", font=FONT, color=GRUV_YELLOW,
                          font_size=22).next_to([rx, ry1, 0.0], UP, buff=0.25)

        def frac_vel():
            v = vel(phi.get_value())
            return (v - vel(np.pi)) / (vel(0.0) - vel(np.pi))

        marcador = always_redraw(lambda: Dot([rx, ry0 + (ry1 - ry0) * frac_vel(), 0.0],
                                             radius=0.08, color=GRUV_YELLOW))
        razao_txt = always_redraw(lambda: Text(
            f"{vel(phi.get_value()) / vel(np.pi):.2f} : 1", font=FONT,
            color=GRUV_FG, font_size=24,
        ).next_to([rx, 0.0, 0.0], RIGHT, buff=0.3))

        self.play(FadeIn(regua), FadeIn(lab_lento), FadeIn(lab_rapido), run_time=0.8)
        self.add(marcador, razao_txt)
        self.wait(0.3)

        # ———— O planeta corre algumas voltas ————
        self.wait(10.0)

        # ———— Saída: zoom-out — esta elipse é uma entre outras ————
        self.play(FadeOut(caption), FadeOut(regua), FadeOut(lab_lento), FadeOut(lab_rapido),
                  FadeOut(razao_txt), FadeOut(marcador), run_time=0.7)
        self.play(self.camera.frame.animate.scale(2.5), run_time=2.2)
        self.wait(0.6)
