"""
MISTAGOGOS · v01 · c10 — Scafetta
A simetria espelhada do Sistema Solar em torno do Cinturão de Asteroides:
pares internos (Mercúrio·Vênus / Vênus·Terra / Terra·Marte) à esquerda,
pares externos (Júpiter·Saturno / Saturno·Urano / Urano·Netuno) à direita.
As razões de ressonância convergem para o Epogdoon — 9/8. Os arcos
endurecem em dentes de engrenagem — a ponte para o Relógio de Deus (c11).

Fonte: artigos/SCALING, MIRROR SYMMETRIES & CONSONANCES.pdf (Scafetta, 2023)
Paleta Gruvbox · EB Garamond · sons em sons/ (se faltar um arquivo, roda muda)
"""

from pathlib import Path

import numpy as np

from manim import (
    DOWN,
    ITALIC,
    UP,
    Circumscribe,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    MathTex,
    ParametricFunction,
    Polygon,
    Scene,
    Text,
    VGroup,
)

# ———— Paleta Gruvbox ————
GRUV_BG = "#282828"
GRUV_FG = "#ebdbb2"
GRUV_YELLOW = "#fabd2f"
GRUV_ORANGE = "#fe8019"
GRUV_AQUA = "#8ec07c"
GRUV_GRAY = "#a89984"

FONT = "EB Garamond"
SONS = Path(__file__).resolve().parent / "sons"

EIXO_Y = 0.2

INTERNOS = [("Mercúrio", -4.2), ("Vênus", -3.0), ("Terra", -1.8), ("Marte", -0.6)]
EXTERNOS = [("Júpiter", 0.6), ("Saturno", 1.8), ("Urano", 3.0), ("Netuno", 4.2)]


class Scafetta(Scene):
    def tocar(self, wav):
        caminho = SONS / wav
        if caminho.exists():
            self.add_sound(str(caminho))

    def construct(self):
        self.camera.background_color = GRUV_BG

        caption = Text("Scafetta (2023) — erro < 1% · p(aleatório) < 0,1%",
                       font=FONT, color=GRUV_AQUA, font_size=28,
                       slant=ITALIC).move_to([0.0, -3.4, 0.0])

        eixo = DashedLine([-5.0, EIXO_Y, 0.0], [5.0, EIXO_Y, 0.0],
                          color=GRUV_GRAY, stroke_width=2.0)
        belt = Text("cinturão de asteroides", font=FONT, color=GRUV_GRAY,
                    font_size=22, slant=ITALIC).move_to([0.0, EIXO_Y - 0.45, 0.0])
        self.play(FadeIn(eixo), FadeIn(belt), run_time=0.9)
        self.wait(0.3)

        def planetas(lista, cor):
            g = VGroup()
            for nome, x in lista:
                d = Dot([x, EIXO_Y, 0.0], radius=0.09, color=cor)
                t = Text(nome, font=FONT, color=cor,
                         font_size=22).next_to(d, UP, buff=0.9)
                g.add(VGroup(d, t))
            return g

        internos = planetas(INTERNOS, GRUV_YELLOW)
        externos = planetas(EXTERNOS, GRUV_ORANGE)
        self.play(FadeIn(internos), run_time=1.0)
        self.wait(0.2)
        self.play(FadeIn(externos), run_time=1.0)
        self.wait(0.4)

        def arco(xa, xb, cor):
            return ParametricFunction(
                lambda t: np.array([xa + (xb - xa) * t,
                                    EIXO_Y + 0.55 * np.sin(np.pi * t), 0.0]),
                t_range=(0.0, 1.0, 0.01), color=cor, stroke_width=2.5,
            )

        arcos = VGroup()
        for i in range(3):
            arcos.add(arco(INTERNOS[i][1], INTERNOS[i + 1][1], GRUV_YELLOW))
        for i in range(3):
            arcos.add(arco(EXTERNOS[i][1], EXTERNOS[i + 1][1], GRUV_ORANGE))

        self.tocar("acorde_harmonico.wav")
        self.play(FadeIn(arcos), run_time=1.0)
        self.wait(1.4)

        # ———— As razões convergindo para o Epogdoon ————
        centro = MathTex(r"\approx \frac{9}{8}", color=GRUV_FG,
                         font_size=56).move_to([0.0, EIXO_Y - 1.5, 0.0])
        self.play(FadeIn(centro), run_time=0.9)
        self.play(Circumscribe(centro, color=GRUV_YELLOW, buff=0.15), run_time=1.0)
        self.play(FadeIn(caption), run_time=0.8)
        self.wait(3.2)

        # ———— Saída: os arcos endurecem em dentes de engrenagem ————
        self.play(FadeOut(caption), FadeOut(centro), run_time=0.6)

        dentes = VGroup()
        for i in range(3):
            xa, xb = INTERNOS[i][1], INTERNOS[i + 1][1]
            xm = (xa + xb) / 2
            dentes.add(Polygon([xa, EIXO_Y, 0.0], [xm, EIXO_Y + 0.55, 0.0],
                               [xb, EIXO_Y, 0.0], color=GRUV_YELLOW,
                               fill_color=GRUV_YELLOW, fill_opacity=0.85, stroke_width=1.5))
        for i in range(3):
            xa, xb = EXTERNOS[i][1], EXTERNOS[i + 1][1]
            xm = (xa + xb) / 2
            dentes.add(Polygon([xa, EIXO_Y, 0.0], [xm, EIXO_Y + 0.55, 0.0],
                               [xb, EIXO_Y, 0.0], color=GRUV_ORANGE,
                               fill_color=GRUV_ORANGE, fill_opacity=0.85, stroke_width=1.5))

        self.play(*[arcos[i].animate.become(dentes[i]) for i in range(6)], run_time=1.1)
        self.wait(2.2)
