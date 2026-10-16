"""
MISTAGOGOS · v01 · c11 — O Relógio de Deus
As sete esferas em ordem caldaica (Lua · Mercúrio · Vênus · Sol · Marte ·
Júpiter · Saturno), com Urano · Netuno · Plutão como traços fantasmas
além de Saturno — o abismo transpessoal. Os anéis viram engrenagens,
engrenadas em razões 2:1 entre vizinhas — a harmonia vira mecanismo.
Um compasso marca 0° Áries. Teaser: o cubo — 12 arestas · 6 faces ·
8 vértices · 12:6 = 2:1, eco do cartaz da forja (c04).

Paleta Gruvbox · EB Garamond · sons em sons/ (se faltar um arquivo, roda muda)
"""

from pathlib import Path

import numpy as np

from manim import (
    DEGREES,
    DOWN,
    ITALIC,
    ORIGIN,
    UP,
    Circle,
    Circumscribe,
    DashedVMobject,
    FadeIn,
    FadeOut,
    Line,
    MathTex,
    Polygon,
    ReplacementTransform,
    Scene,
    Text,
    VGroup,
)

# ———— Paleta Gruvbox ————
GRUV_BG = "#282828"
GRUV_FG = "#ebdbb2"
GRUV_YELLOW = "#fabd2f"
GRUV_GRAY = "#a89984"
GRUV_NEUT = "#7c6f64"
GRUV_DARK = "#3c3833"

FONT = "EB Garamond"
SONS = Path(__file__).resolve().parent / "sons"

ORDEM = ["Lua", "Mercúrio", "Vênus", "Sol", "Marte", "Júpiter", "Saturno"]
RAIOS = [0.55, 0.95, 1.35, 1.75, 2.15, 2.6, 3.05]
ALEM = ["Urano", "Netuno", "Plutão"]
RAIOS_ALEM = [3.55, 3.95, 4.35]


class Relogio(Scene):
    def tocar(self, wav):
        caminho = SONS / wav
        if caminho.exists():
            self.add_sound(str(caminho))

    def construct(self):
        self.camera.background_color = GRUV_BG
        self.tocar("drone_esferas.wav")

        # ———— As sete esferas, ordem caldaica ————
        aneis = VGroup()
        for nome, r in zip(ORDEM, RAIOS):
            solido = nome == "Saturno"
            c = Circle(radius=r, color=GRUV_GRAY,
                      stroke_width=3.0 if solido else 1.6)
            aneis.add(c)

        # legenda lateral — ordem caldaica, de dentro para fora
        legenda = VGroup(*[
            Text(nome, font=FONT, color=GRUV_FG, font_size=24)
            for nome in ORDEM
        ]).arrange(DOWN, buff=0.22)
        legenda.move_to([5.7, 0.0, 0.0])

        self.play(FadeIn(aneis), run_time=1.4)
        self.play(FadeIn(legenda), run_time=1.2)
        self.wait(0.6)

        # ———— Além de Saturno: o abismo transpessoal ————
        fantasmas = VGroup()
        for r in RAIOS_ALEM:
            fantasmas.add(DashedVMobject(
                Circle(radius=r, color=GRUV_NEUT, stroke_width=1.3), num_dashes=36))
        abismo_txt = Text("o abismo transpessoal", font=FONT, color=GRUV_NEUT,
                          font_size=26, slant=ITALIC).move_to([0.0, -3.6, 0.0])
        self.play(FadeIn(fantasmas), FadeIn(abismo_txt), run_time=1.2)
        self.wait(1.8)
        self.play(FadeOut(fantasmas), FadeOut(abismo_txt), FadeOut(legenda), run_time=0.9)

        # ———— Transform: anéis → engrenagens (dentes trapezoidais) ————
        def engrenagem(raio, n_dentes, cor, largura):
            raio_raiz = raio * 0.76
            passo = 2 * np.pi / n_dentes
            pts = []
            for i in range(n_dentes):
                a0 = i * passo
                a1 = a0 + passo * 0.45
                a2 = a0 + passo * 0.65
                a3 = a0 + passo
                for ang, r in ((a0, raio_raiz), (a1, raio), (a2, raio), (a3, raio_raiz)):
                    pts.append([r * np.cos(ang), r * np.sin(ang), 0.0])
            return Polygon(*pts, color=cor, stroke_width=largura)

        engrenagens = VGroup(*[
            engrenagem(r, int(6 + r * 1.6), GRUV_GRAY, 3.0 if ORDEM[i] == "Saturno" else 1.6)
            for i, r in enumerate(RAIOS)
        ])
        self.tocar("tic_relogio.wav")
        self.play(*[ReplacementTransform(aneis[i], engrenagens[i]) for i in range(7)],
                  run_time=1.6)
        self.wait(0.3)

        # ———— Engrenadas: razões 2:1 entre vizinhas ————
        for i, g in enumerate(engrenagens):
            direcao = 1 if i % 2 == 0 else -1
            vel = 1.0 / (2 ** i) * 6.0
            g.add_updater(lambda m, dt, d=direcao, v=vel: m.rotate(d * v * dt))
        self.wait(3.0)

        # ———— O compasso marca 0° Áries ————
        ponteiro = Line(ORIGIN, [0.0, RAIOS[-1] + 0.3, 0.0], color=GRUV_YELLOW, stroke_width=3.0)
        self.tocar("tic_relogio.wav")
        self.play(FadeIn(ponteiro), run_time=0.7)
        compasso_txt = Text("um novo compasso rítmico", font=FONT, color=GRUV_YELLOW,
                            font_size=30, slant=ITALIC).move_to([0.0, -3.6, 0.0])
        self.play(FadeIn(compasso_txt), run_time=0.8)
        self.wait(2.2)

        for g in engrenagens:
            g.clear_updaters()
        self.play(FadeOut(compasso_txt), FadeOut(ponteiro), FadeOut(engrenagens), run_time=1.0)

        # ———— Teaser: o cubo isométrico ————
        s = 1.25
        angs = [90, 150, 210, 270, 330, 30]
        p = [np.array([s * np.cos(a * DEGREES), s * np.sin(a * DEGREES), 0.0]) for a in angs]
        o = np.array([0.0, 0.0, 0.0])
        topo = Polygon(o, p[0], p[1], p[2], color=GRUV_GRAY, stroke_width=2.0,
                       fill_color=GRUV_FG, fill_opacity=0.9)
        direita = Polygon(o, p[2], p[3], p[4], color=GRUV_GRAY, stroke_width=2.0,
                          fill_color=GRUV_GRAY, fill_opacity=0.9)
        esquerda = Polygon(o, p[4], p[5], p[0], color=GRUV_GRAY, stroke_width=2.0,
                           fill_color=GRUV_DARK, fill_opacity=0.9)
        cubo = VGroup(direita, esquerda, topo).move_to([0.0, 0.3, 0.0])
        cubo.add_updater(lambda m, dt: m.rotate(dt * 0.5))

        self.play(FadeIn(cubo), run_time=1.0)
        self.wait(0.4)

        info = Text("12 arestas · 6 faces · 8 vértices", font=FONT, color=GRUV_FG,
                    font_size=30).move_to([0.0, -2.3, 0.0])
        self.play(FadeIn(info), run_time=0.8)
        self.wait(1.2)

        razao = MathTex(r"12 : 6 = 2 : 1", color=GRUV_YELLOW,
                        font_size=44).move_to([0.0, -3.1, 0.0])
        self.play(FadeIn(razao), run_time=0.8)
        self.play(Circumscribe(razao, color=GRUV_YELLOW, buff=0.15), run_time=1.0)
        self.wait(2.0)

        # ———— Saída: o cubo encolhe ao centro ————
        cubo.clear_updaters()
        self.play(FadeOut(info), FadeOut(razao), run_time=0.6)
        self.play(cubo.animate.scale(0.05).move_to(ORIGIN), run_time=1.3)
        self.remove(cubo)
        self.wait(0.4)
