"""
MISTAGOGOS · v01 · c03 — Axiomas, Logos e a Tradição Hermética
Etimologia (astro · logia) → AXIOMA → Hermes psicopompo atravessando a
fronteira vigília/inconsciente, com o caduceu (recriação vetorial, nunca
colada) → Caronte e Morfeu → o Princípio da Correspondência (espiral
galáctica ↔ átomo) → o Princípio da Polaridade (círculo luz/sombra) →
saída: o caduceu desliza ao centro e vira o martelo (âncora para c04).

Paleta Gruvbox · EB Garamond · sons em sons/ (se faltar um arquivo, roda muda)
"""

from pathlib import Path

import numpy as np

from manim import (
    DOWN,
    ITALIC,
    LEFT,
    RIGHT,
    UP,
    Arc,
    Brace,
    Circle,
    DashedLine,
    Dot,
    Ellipse,
    FadeIn,
    FadeOut,
    Line,
    ParametricFunction,
    Polygon,
    Rectangle,
    ReplacementTransform,
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
GRUV_AQUA = "#8ec07c"
GRUV_GRAY = "#a89984"
GRUV_DARK = "#3c3833"

FONT = "EB Garamond"
SONS = Path(__file__).resolve().parent / "sons"


class LogosHermes(Scene):
    def tocar(self, wav, **kwargs):
        caminho = SONS / wav
        if caminho.exists():
            self.add_sound(str(caminho), **kwargs)

    def construct(self):
        self.camera.background_color = GRUV_BG
        self._etimologia()
        self._axioma()
        self._hermes_psicopompo()
        self._caronte_morfeu()
        self._correspondencia()
        self._polaridade()
        self._saida()

    # ———————————————— Etimologia ————————————————
    def _etimologia(self):
        palavra = Text("ASTROLOGIA", font=FONT, color=GRUV_FG, font_size=64)
        self.play(FadeIn(palavra), run_time=1.0)
        self.wait(3.0)

        astro = Text("ASTRO", font=FONT, color=GRUV_YELLOW,
                     font_size=56).move_to([-2.6, 1.3, 0.0])
        logia = Text("LOGIA", font=FONT, color=GRUV_AQUA,
                     font_size=56).move_to([2.6, 1.3, 0.0])
        self.play(ReplacementTransform(palavra, VGroup(astro, logia)), run_time=1.1)
        self.wait(0.4)

        def_astro = VGroup(
            Text("ástron", font=FONT, color=GRUV_YELLOW, font_size=30, slant=ITALIC),
            Text("corpo celeste", font=FONT, color=GRUV_FG, font_size=26),
        ).arrange(DOWN, buff=0.12)
        def_logia = VGroup(
            Text("lógos", font=FONT, color=GRUV_AQUA, font_size=30, slant=ITALIC),
            Text("razão · proporção · medida", font=FONT, color=GRUV_FG, font_size=26),
        ).arrange(DOWN, buff=0.12)

        brace_a = Brace(astro, direction=DOWN, buff=0.2, color=GRUV_YELLOW)
        brace_l = Brace(logia, direction=DOWN, buff=0.2, color=GRUV_AQUA)
        def_astro.next_to(brace_a, DOWN, buff=0.2)
        def_logia.next_to(brace_l, DOWN, buff=0.2)

        self.play(FadeIn(brace_a), FadeIn(brace_l), run_time=0.7)
        self.play(FadeIn(def_astro), FadeIn(def_logia), run_time=0.9)
        self.wait(9.0)

        sintese = Text("a proporção matemática dos astros", font=FONT, color=GRUV_FG,
                       font_size=32, slant=ITALIC).move_to([0.0, -2.4, 0.0])
        self.play(FadeIn(sintese), run_time=0.9)
        self.wait(8.0)

        self.play(FadeOut(astro), FadeOut(logia), FadeOut(brace_a), FadeOut(brace_l),
                  FadeOut(def_astro), FadeOut(def_logia), FadeOut(sintese), run_time=0.9)

    # ———————————————— Axioma ————————————————
    def _axioma(self):
        axioma = Text("AXIOMA", font=FONT, color=GRUV_YELLOW, font_size=68)
        self.play(FadeIn(axioma, shift=0.2 * UP), run_time=0.9)
        self.wait(0.5)

        etim = Text("de áxios — digno, válido", font=FONT, color=GRUV_GRAY,
                    font_size=28, slant=ITALIC).next_to(axioma, DOWN, buff=0.35)
        defin = Text("o ponto de partida dispensado de comprovação direta",
                    font=FONT, color=GRUV_FG, font_size=28).next_to(etim, DOWN, buff=0.3)
        self.play(FadeIn(etim), run_time=0.6)
        self.play(FadeIn(defin), run_time=0.8)
        self.wait(9.0)

        self.play(FadeOut(axioma), FadeOut(etim), FadeOut(defin), run_time=0.8)

    # ———————————————— Hermes psicopompo ————————————————
    def _hermes_psicopompo(self):
        fronteira = DashedLine([0.0, 2.3, 0.0], [0.0, -1.0, 0.0],
                               color=GRUV_GRAY, stroke_width=2.0)
        lbl_vig = Text("vigília", font=FONT, color=GRUV_GRAY, font_size=24,
                      slant=ITALIC).move_to([-1.6, 2.6, 0.0])
        lbl_inc = Text("inconsciente", font=FONT, color=GRUV_GRAY, font_size=24,
                       slant=ITALIC).move_to([1.6, 2.6, 0.0])
        self.play(FadeIn(fronteira), FadeIn(lbl_vig), FadeIn(lbl_inc), run_time=0.8)

        # ———— figura vetorial mínima: Hermes em perfil ————
        def figura(x):
            cabeca = Circle(radius=0.18, color=GRUV_FG, stroke_width=2.5).move_to([x, 1.0, 0.0])
            torso = Line([x, 0.82, 0.0], [x, 0.1, 0.0], color=GRUV_FG, stroke_width=2.5)
            perna1 = Line([x, 0.1, 0.0], [x - 0.22, -0.4, 0.0], color=GRUV_FG, stroke_width=2.5)
            perna2 = Line([x, 0.1, 0.0], [x + 0.18, -0.42, 0.0], color=GRUV_FG, stroke_width=2.5)
            braco = Line([x, 0.6, 0.0], [x + 0.32, 0.75, 0.0], color=GRUV_FG, stroke_width=2.5)
            return VGroup(cabeca, torso, perna1, perna2, braco)

        hermes_x = ValueTracker(-3.0)
        hermes = always_redraw(lambda: figura(hermes_x.get_value()))
        self.add(hermes)
        self.wait(0.3)
        self.play(hermes_x.animate.set_value(1.6), run_time=2.6)
        self.wait(0.4)

        txt_psico = VGroup(
            Text("psicopompo", font=FONT, color=GRUV_YELLOW, font_size=32, slant=ITALIC),
            Text("psyché — sopro vital · pompós — guia, condutor", font=FONT,
                color=GRUV_FG, font_size=24),
        ).arrange(DOWN, buff=0.14).move_to([0.0, -2.5, 0.0])
        self.play(FadeIn(txt_psico), run_time=0.9)
        self.wait(8.0)
        self.play(FadeOut(txt_psico), FadeOut(lbl_vig), FadeOut(lbl_inc), run_time=0.6)

        # ———— o caduceu: duas senoides entrelaçadas + eixo + asas ————
        eixo = Line([0.0, -0.3, 0.0], [0.0, 1.6, 0.0], color=GRUV_GRAY, stroke_width=3.0)

        def serpente(sinal, cor):
            return ParametricFunction(
                lambda t: np.array([sinal * 0.3 * np.sin(2.5 * np.pi * t), -0.3 + t * 1.9, 0.0]),
                t_range=(0.0, 1.0, 0.004), color=cor, stroke_width=3.0,
            )

        s1 = serpente(1, GRUV_YELLOW)
        s2 = serpente(-1, GRUV_AQUA)
        asa1 = Triangle(color=GRUV_FG, stroke_width=2.0, fill_color=GRUV_FG,
                        fill_opacity=0.7).scale(0.22).move_to([-0.3, 1.75, 0.0]).rotate(-0.5)
        asa2 = Triangle(color=GRUV_FG, stroke_width=2.0, fill_color=GRUV_FG,
                        fill_opacity=0.7).scale(0.22).move_to([0.3, 1.75, 0.0]).rotate(0.5)
        caduceu = VGroup(eixo, s1, s2, asa1, asa2).move_to([0.0, 0.0, 0.0])

        self.play(FadeOut(hermes), FadeOut(fronteira), run_time=0.6)
        self.play(FadeIn(caduceu), run_time=1.1)
        self.wait(7.0)

        self.caduceu = caduceu

    # ———————————————— Caronte & Morfeu ————————————————
    def _caronte_morfeu(self):
        caduceu = self.caduceu
        self.play(caduceu.animate.scale(0.5).move_to([0.0, 2.6, 0.0]), run_time=0.8)

        # Caronte — a barca
        casco = Arc(radius=0.55, start_angle=np.pi, angle=np.pi, color=GRUV_GRAY,
                   stroke_width=2.5).move_to([-2.8, -0.3, 0.0])
        mastro = Line([-2.8, -0.3, 0.0], [-2.8, 0.5, 0.0], color=GRUV_GRAY, stroke_width=2.0)
        caronte_txt = Text("Caronte", font=FONT, color=GRUV_GRAY,
                          font_size=26).move_to([-2.8, -1.1, 0.0])
        caronte = VGroup(casco, mastro, caronte_txt)

        # Morfeu — a onda que vira perfil adormecido
        onda = ParametricFunction(
            lambda t: np.array([2.1 + t, -0.3 + 0.25 * np.sin(3 * t), 0.0]),
            t_range=(0.0, 1.4, 0.01), color=GRUV_AQUA, stroke_width=2.5,
        )
        morfeu_txt = Text("Morfeu", font=FONT, color=GRUV_AQUA,
                         font_size=26).move_to([2.8, -1.1, 0.0])
        morfeu = VGroup(onda, morfeu_txt)

        self.play(FadeIn(caronte), FadeIn(morfeu), run_time=1.0)
        self.wait(6.0)

        caption = Text("Morpheus · Matrix", font=FONT, color=GRUV_GRAY,
                       font_size=22, slant=ITALIC).move_to([2.8, -1.7, 0.0])
        self.play(FadeIn(caption), run_time=0.5)
        self.wait(5.5)
        self.play(FadeOut(caption), FadeOut(caronte), FadeOut(morfeu), run_time=0.7)

    # ———————————————— Correspondência ————————————————
    def _correspondencia(self):
        caduceu = self.caduceu
        self.play(caduceu.animate.move_to([0.0, 3.1, 0.0]).scale(0.7), run_time=0.6)

        titulo = Text("o Princípio da Correspondência", font=FONT, color=GRUV_AQUA,
                      font_size=32, slant=ITALIC).move_to([0.0, 2.2, 0.0])
        self.play(FadeIn(titulo), run_time=0.8)

        # espiral galáctica (paramétrica)
        espiral = ParametricFunction(
            lambda t: np.array([
                -2.4 + 0.18 * t * np.cos(t), 0.0 + 0.18 * t * np.sin(t), 0.0]),
            t_range=(0.0, 4 * np.pi, 0.02), color=GRUV_YELLOW, stroke_width=2.5,
        ).move_to([-2.4, 0.0, 0.0])

        # átomo (núcleo + 3 elipses orbitais)
        nucleo = Dot([2.4, 0.0, 0.0], radius=0.09, color=GRUV_AQUA)
        orbitais = VGroup(*[
            Ellipse(width=2.0, height=0.8, color=GRUV_AQUA, stroke_width=1.8)
                .move_to([2.4, 0.0, 0.0]).rotate(ang)
            for ang in (0, np.pi / 3, 2 * np.pi / 3)
        ])
        atomo = VGroup(orbitais, nucleo)

        self.play(FadeIn(espiral), run_time=1.0)
        self.wait(0.5)
        self.play(FadeIn(atomo), run_time=1.0)
        self.wait(2.5)

        texto = VGroup(
            Text("como em cima, assim embaixo", font=FONT, color=GRUV_FG,
                font_size=30, slant=ITALIC),
            Text("Maya — a ilusão de separação", font=FONT, color=GRUV_GRAY, font_size=24),
        ).arrange(DOWN, buff=0.16).move_to([0.0, -2.4, 0.0])
        self.play(FadeIn(texto), run_time=0.9)
        self.wait(9.0)

        self.play(FadeOut(espiral), FadeOut(atomo), FadeOut(texto), FadeOut(titulo),
                  run_time=0.8)

    # ———————————————— Polaridade ————————————————
    def _polaridade(self):
        caduceu = self.caduceu

        titulo = Text("o Princípio da Polaridade", font=FONT, color=GRUV_AQUA,
                      font_size=32, slant=ITALIC).move_to([0.0, 2.2, 0.0])
        self.play(FadeIn(titulo), run_time=0.8)

        luz = Arc(radius=1.3, start_angle=np.pi / 2, angle=np.pi, color=GRUV_FG,
                 stroke_width=0, fill_color=GRUV_FG, fill_opacity=1.0)
        sombra = Arc(radius=1.3, start_angle=-np.pi / 2, angle=np.pi, color=GRUV_DARK,
                    stroke_width=0, fill_color=GRUV_DARK, fill_opacity=1.0)
        # usar Polygon de meio-disco em vez de Arc puro (Arc não fecha a fatia)
        def meio_disco(start, cor):
            pts = [[1.3 * np.cos(start + i * np.pi / 24), 1.3 * np.sin(start + i * np.pi / 24), 0.0]
                   for i in range(25)]
            pts.append([0.0, 0.0, 0.0])
            return Polygon(*pts, color=cor, stroke_width=0, fill_color=cor, fill_opacity=1.0)

        luz = meio_disco(np.pi / 2, GRUV_FG)
        sombra = meio_disco(-np.pi / 2, GRUV_DARK)
        borda = Circle(radius=1.3, color=GRUV_GRAY, stroke_width=2.0)
        circulo = VGroup(luz, sombra, borda).move_to([0.0, -0.2, 0.0])
        self.play(FadeIn(circulo), run_time=0.9)
        self.wait(2.0)

        self.play(circulo.animate.rotate(np.pi), run_time=2.0)
        texto = Text("diferem apenas em grau", font=FONT, color=GRUV_FG, font_size=30,
                    slant=ITALIC).move_to([0.0, -2.3, 0.0])
        self.play(FadeIn(texto), run_time=0.8)
        self.wait(8.0)

        self.play(FadeOut(circulo), FadeOut(texto), FadeOut(titulo), run_time=0.8)
        self.caduceu = caduceu

    # ———————————————— Saída: caduceu → martelo ————————————————
    def _saida(self):
        caduceu = self.caduceu
        self.play(caduceu.animate.move_to([0.0, 0.0, 0.0]).scale(1.3), run_time=1.0)

        cabeca = Rectangle(width=0.95, height=0.4, color=GRUV_FG, stroke_width=3.0,
                          fill_color=GRUV_FG, fill_opacity=0.92).move_to([0.0, 0.3, 0.0])
        cabo = Rectangle(width=0.13, height=1.05, color=GRUV_GRAY, stroke_width=2.5,
                        fill_color=GRUV_GRAY, fill_opacity=0.85).next_to(cabeca, UP, buff=0.03)
        martelo = VGroup(cabeca, cabo)

        self.play(ReplacementTransform(caduceu, martelo), run_time=1.2)
        self.wait(0.8)
        self.play(FadeOut(martelo), run_time=0.6)
        self.wait(0.3)
