"""
MISTAGOGOS · v01 · c02 — O Retorno de Saturno
A roda zodiacal com 12 setores; Saturno orbita com um contador de anos
(1994→2023,5), fecha a órbita no ponto natal — o Retorno de Saturno aos
29,5 anos. Netuno entra pela órbita externa e cruza o mesmo grau: a
conjunção no marco zero de Áries, o ponto de reinicialização cíclica.
Posições simbólicas, não efemérides.

Paleta Gruvbox · EB Garamond (zodíaco sem glifos — abreviações, per §4
do planejamento) · sons em sons/ (se faltar um arquivo, roda muda)
"""

from pathlib import Path

import numpy as np

from manim import (
    DEGREES,
    ITALIC,
    Annulus,
    Circle,
    Circumscribe,
    DashedVMobject,
    Dot,
    FadeIn,
    FadeOut,
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
GRUV_YELLOW = "#fabd2f"
GRUV_AQUA = "#8ec07c"
GRUV_GRAY = "#a89984"
GRUV_DARK = "#3c3833"

FONT = "EB Garamond"
SONS = Path(__file__).resolve().parent / "sons"

R_ZODIACO = 2.7
R_SAT = 2.1
R_NET = 2.55
CENTRO = np.array([0.0, 0.5, 0.0])

SIGNOS = ["Ár", "To", "Ge", "Cn", "Le", "Vi", "Li", "Es", "Sa", "Cp", "Aq", "Pe"]


def ponto(theta_deg, raio, centro=CENTRO):
    rad = (theta_deg + 90) * DEGREES
    return centro + raio * np.array([np.cos(rad), np.sin(rad), 0.0])


class RetornoSaturno(MovingCameraScene):
    def tocar(self, wav):
        caminho = SONS / wav
        if caminho.exists():
            self.add_sound(str(caminho))

    def construct(self):
        self.camera.background_color = GRUV_BG

        # ———— A roda zodiacal ————
        anel = Annulus(inner_radius=R_ZODIACO - 0.10, outer_radius=R_ZODIACO + 0.10,
                       color=GRUV_DARK, fill_opacity=1.0, stroke_width=0).move_to(CENTRO)
        ticks = VGroup()
        rotulos = VGroup()
        for i, nome in enumerate(SIGNOS):
            th = i * 30
            p_in = ponto(th, R_ZODIACO - 0.22)
            p_out = ponto(th, R_ZODIACO + 0.22)
            cor = GRUV_YELLOW if i == 0 else GRUV_GRAY
            ticks.add(Line(p_in, p_out, color=cor, stroke_width=3.0 if i == 0 else 2.0))
            rotulos.add(Text(nome, font=FONT, color=cor,
                             font_size=22).move_to(ponto(th, R_ZODIACO + 0.48)))

        self.play(FadeIn(anel), run_time=1.0)
        self.play(FadeIn(ticks), FadeIn(rotulos), run_time=1.2)
        self.wait(0.5)

        # ———— Órbitas tracejadas ————
        orbita_sat = DashedVMobject(
            Circle(radius=R_SAT, color=GRUV_GRAY, stroke_width=1.5).move_to(CENTRO),
            num_dashes=48).set_opacity(0.5)
        orbita_net = DashedVMobject(
            Circle(radius=R_NET, color=GRUV_AQUA, stroke_width=1.5).move_to(CENTRO),
            num_dashes=60).set_opacity(0.35)
        self.play(FadeIn(orbita_sat), run_time=0.7)
        self.wait(0.3)

        # ———— Contador de anos ————
        ano = ValueTracker(1994)
        contador = always_redraw(lambda: Text(f"{int(ano.get_value())}", font=FONT,
                                              color=GRUV_FG, font_size=34)
                                 .move_to([0.0, -3.55, 0.0]))
        self.add(contador)

        # ———— Saturno orbita ————
        theta_sat = ValueTracker(0.0)
        saturno = always_redraw(lambda: VGroup(
            Dot(ponto(theta_sat.get_value(), R_SAT), radius=0.09, color=GRUV_GRAY),
            Circle(radius=0.16, color=GRUV_GRAY, stroke_width=1.5)
                .move_to(ponto(theta_sat.get_value(), R_SAT)),
        ))
        self.add(saturno)
        self.wait(0.3)

        self.play(
            theta_sat.animate.set_value(360.0),
            ano.animate.set_value(2023.5),
            run_time=7.0, rate_func=rate_functions.ease_in_out_sine,
        )

        # ———— A órbita fecha no ponto natal ————
        marco = ticks[0]
        self.play(Circumscribe(marco, color=GRUV_YELLOW, buff=0.2), run_time=1.0)
        legenda = Text("29,5 anos — o Retorno de Saturno", font=FONT, color=GRUV_YELLOW,
                       font_size=30, slant=ITALIC).move_to([0.0, -3.05, 0.0])
        self.play(FadeIn(legenda), run_time=0.8)
        self.wait(1.6)
        self.play(FadeOut(legenda), run_time=0.6)

        # ———— Netuno entra pela órbita externa ————
        self.play(FadeIn(orbita_net), run_time=0.7)
        theta_net = ValueTracker(230.0)
        netuno = always_redraw(lambda: Dot(ponto(theta_net.get_value(), R_NET),
                                           radius=0.1, color=GRUV_AQUA))
        self.add(netuno)
        self.wait(0.3)
        self.play(theta_net.animate.set_value(360.0), ano.animate.set_value(2026),
                  run_time=5.0, rate_func=rate_functions.ease_in_out_sine)

        # ———— Conjunção: os dois convergem ao zero ————
        centro_zero = ponto(0, (R_SAT + R_NET) / 2)
        onda = Circle(radius=0.25, color=GRUV_FG, stroke_width=5.0).move_to(centro_zero)
        self.add(onda)
        self.tocar("bigorna_Do262.wav")
        self.play(onda.animate.scale(3.2).set_opacity(0), run_time=0.9)
        self.remove(onda)

        legenda2 = Text("reinicialização cíclica de fase", font=FONT, color=GRUV_FG,
                        font_size=30, slant=ITALIC).move_to([0.0, -3.05, 0.0])
        self.play(FadeIn(legenda2), run_time=0.9)
        self.wait(2.0)

        # ———— Zoom no ponto zero ————
        alvo = ponto(0, R_ZODIACO)
        self.play(FadeOut(legenda2), FadeOut(contador), run_time=0.6)
        self.play(self.camera.frame.animate.scale(0.28).move_to(alvo), run_time=2.0)
        self.wait(1.0)
