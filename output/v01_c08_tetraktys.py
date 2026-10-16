"""
MISTAGOGOS · v01 · c08 — O Tetraktys
Recriação vetorial do detalhe de Pitágoras n'A Escola de Atenas (Rafael):
a lousa com o triângulo de dez pontos — 1+2+3+4=10 — e as razões que já
ouvimos: 2:1 · 3:2 · 4:3 · 9:8. O 9:8 cresce e vira a elipse — a ponte
para Kepler (c09).

Paleta Gruvbox · EB Garamond · sons em sons/ (se faltar um arquivo, roda muda)
"""

from pathlib import Path

from manim import (
    DOWN,
    ITALIC,
    UP,
    Dot,
    Ellipse,
    FadeIn,
    FadeOut,
    LaggedStart,
    MathTex,
    Rectangle,
    ReplacementTransform,
    Scene,
    Text,
    VGroup,
)

# ———— Paleta Gruvbox ————
GRUV_BG = "#282828"
GRUV_FG = "#ebdbb2"
GRUV_YELLOW = "#fabd2f"
GRUV_GREEN = "#b8bb26"
GRUV_ORANGE = "#fe8019"
GRUV_AQUA = "#8ec07c"
GRUV_GRAY = "#a89984"
GRUV_DARK = "#3c3833"

FONT = "EB Garamond"
SONS = Path(__file__).resolve().parent / "sons"

TRI_TOP = 1.55
DY = -0.82
DX = 0.52
CORES = [GRUV_GREEN, GRUV_YELLOW, GRUV_ORANGE, GRUV_AQUA]
WAVS = ["tom_fundamental_220.wav", "tom_oitava_440.wav", "tom_quinta_660.wav", "harpa_la5_880.wav"]


class Tetraktys(Scene):
    def tocar(self, wav):
        caminho = SONS / wav
        if caminho.exists():
            self.add_sound(str(caminho))

    def construct(self):
        self.camera.background_color = GRUV_BG

        lousa = Rectangle(width=6.6, height=6.8, color=GRUV_GRAY, stroke_width=2.5,
                          fill_color=GRUV_DARK, fill_opacity=1.0).move_to([0.0, 0.0, 0.0])
        caption = Text("Rafael · A Escola de Atenas — recriação do detalhe",
                       font=FONT, color=GRUV_AQUA, font_size=30,
                       slant=ITALIC).move_to([0.0, 3.5, 0.0])
        self.play(FadeIn(lousa), run_time=0.8)
        self.play(FadeIn(caption), run_time=0.8)
        self.wait(1.0)

        # ———— O triângulo: 1 · 2 · 3 · 4 pontos ————
        linhas = []
        for r in range(1, 5):
            y = TRI_TOP + (r - 1) * DY
            cor = CORES[r - 1]
            linha = VGroup(*[
                Dot([-(r - 1) * DX / 2 + i * DX, y, 0.0], radius=0.11, color=cor)
                for i in range(r)
            ])
            linhas.append(linha)

        for r, linha in enumerate(linhas, start=1):
            self.tocar(WAVS[r - 1])
            self.play(LaggedStart(*[FadeIn(d, scale=1.3) for d in linha], lag_ratio=0.3),
                      run_time=0.5 + 0.15 * r)
            self.wait(1.1)

        self.wait(1.8)

        # ———— 1 + 2 + 3 + 4 = 10 ————
        soma = MathTex(r"1 + 2 + 3 + 4 = 10", color=GRUV_FG,
                       font_size=50).move_to([0.0, -1.9, 0.0])
        self.play(FadeIn(soma), run_time=0.9)
        self.wait(3.0)

        # ———— As razões fluindo ————
        razoes = MathTex(r"2:1 \quad\cdot\quad 3:2 \quad\cdot\quad 4:3 \quad\cdot\quad ",
                         r"9:8", color=GRUV_FG, font_size=40).move_to([0.0, -2.75, 0.0])
        razoes[1].set_color(GRUV_YELLOW)
        self.play(FadeIn(razoes), run_time=1.0)
        self.wait(4.0)

        # ———— Saída: o 9:8 cresce e vira a elipse ————
        self.play(FadeOut(lousa), FadeOut(caption), FadeOut(soma),
                  FadeOut(razoes[0]), FadeOut(VGroup(*linhas)), run_time=0.9)

        elipse = Ellipse(width=5.2, height=3.1, color=GRUV_FG,
                         stroke_width=4.0).move_to([0.0, 0.0, 0.0])
        self.play(ReplacementTransform(razoes[1], elipse), run_time=1.2)
        self.wait(1.5)
        self.remove(elipse)
