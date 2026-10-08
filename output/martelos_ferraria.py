"""
MISTAGOGOS · teste da forja
Nicômaco de Gerasa · Enchiridion Harmonices
Martelos de 12 e 6 libras sobre a bigorna: 12 : 6 = 2 : 1 → Diapasão (oitava).
Paleta Gruvbox · Tipografia EB Garamond · tings percussivos 220 / 440 Hz
"""

from pathlib import Path

from manim import (
    DOWN,
    ITALIC,
    LEFT,
    RIGHT,
    UP,
    Circle,
    FadeIn,
    FadeOut,
    Line,
    Polygon,
    Rectangle,
    Scene,
    Text,
    VGroup,
    rate_functions,
)

# ———— Paleta Gruvbox ————
GRUV_BG = "#282828"      # fundo
GRUV_FG = "#ebdbb2"     # texto · cabeça do 1º martelo
GRUV_YELLOW = "#fabd2f" # 2º martelo · destaque
GRUV_GREEN = "#b8bb26"  # tom grave Lá
GRUV_AQUA = "#8ec07c"   # cabeçalho
GRUV_GRAY = "#a89984"   # bigorna · cabos
GRUV_NEUT = "#7c6f64"   # chão
GRUV_DARK = "#3c3833"   # corpo da bigorna

FONT = "EB Garamond"
SONS = Path(__file__).resolve().parent / "sons"  # pasta sons/ ao lado do script

BIGORNA_Y = -1.40
Y_FACE = BIGORNA_Y + 0.75   # topo da face (o move_to centraliza o bbox do Polygon)
Y_CHAO = -2.15
X1, X2 = -0.55, 0.35        # pontos de impacto na face
SUBIDA = 1.20               # recuo dos martelos após o golpe


class Ferraria(Scene):
    def construct(self):
        self.camera.background_color = GRUV_BG

        # ———— Cabeçalho ————
        titulo = Text(
            "Nicômaco de Gerasa · Enchiridion Harmonices",
            font=FONT, color=GRUV_AQUA, font_size=38, slant=ITALIC,
        ).move_to([0.0, 3.35, 0.0])
        self.play(FadeIn(titulo), run_time=1.0)

        # ———— Chão · bigorna ————
        chao = Line([-6.4, Y_CHAO, 0.0], [6.4, Y_CHAO, 0.0],
                    color=GRUV_NEUT, stroke_width=2.5)
        pontos = [
            (-0.90, 0.55, 0.0), (0.90, 0.55, 0.0), (1.75, 0.28, 0.0), (0.90, 0.02, 0.0),
            (0.62, -0.50, 0.0), (0.95, -0.95, 0.0), (-0.95, -0.95, 0.0), (-0.62, -0.50, 0.0),
            (-1.75, 0.28, 0.0), (-0.90, 0.02, 0.0),
        ]
        bigorna = Polygon(
            *pontos,
            color=GRUV_GRAY, stroke_width=3.0,
            fill_color=GRUV_DARK, fill_opacity=1.0,
        ).move_to([0.0, BIGORNA_Y, 0.0])
        self.play(FadeIn(chao), FadeIn(bigorna), run_time=0.9)

        # ———— Martelos (cabeça na base · cabo acima · peso no alto) ————
        def martelo(cor, comp, alt, peso_txt, x):
            y_rest = Y_FACE + alt / 2 + SUBIDA
            cabeca = Rectangle(
                width=comp, height=alt, color=cor, stroke_width=3.0,
                fill_color=cor, fill_opacity=0.92,
            ).move_to([x, y_rest, 0.0])
            cabo = Rectangle(
                width=0.13, height=1.05, color=GRUV_GRAY, stroke_width=2.5,
                fill_color=GRUV_GRAY, fill_opacity=0.85,
            ).next_to(cabeca, UP, buff=0.03)
            peso = Text(peso_txt, font=FONT, color=cor,
                        font_size=30).next_to(cabo, UP, buff=0.14)
            return VGroup(cabeca, cabo, peso)

        m1 = martelo(GRUV_FG, 0.95, 0.40, "12 lb", X1)
        m2 = martelo(GRUV_YELLOW, 0.62, 0.30, "6 lb", X2)
        self.play(FadeIn(m1), FadeIn(m2), run_time=0.8)

        # ———— Rótulos das notas ————
        rot_f = Text("Lá · 220 Hz", font=FONT, color=GRUV_GREEN,
                     font_size=34).move_to([-4.80, -2.80, 0.0])
        rot_2f = Text("Lá⁴ · 440 Hz", font=FONT, color=GRUV_YELLOW,
                      font_size=34).move_to([4.80, -2.80, 0.0])

        def golpe(g, x, cor, wav, rotulo=None):
            """Desce, golpeia (som + onda + tremor) e retorna ao repouso."""
            self.play(g.animate.shift(SUBIDA * DOWN), run_time=0.20,
                      rate_func=rate_functions.rush_into)
            self.add_sound(str(SONS / wav))
            onda = Circle(radius=0.32, color=cor,
                          stroke_width=5.0).move_to([x, Y_FACE, 0.0])
            self.add(onda)
            anims = [onda.animate.scale(2.8).set_opacity(0),
                     bigorna.animate.shift(0.05 * RIGHT)]
            if rotulo is not None:
                anims.append(FadeIn(rotulo))
            self.play(*anims, run_time=0.15)
            self.play(bigorna.animate.shift(0.05 * LEFT), run_time=0.12)
            self.remove(onda)
            self.play(g.animate.shift(SUBIDA * UP), run_time=0.55)

        def golpe_duplo():
            """Os dois martelos soam juntos (consonância)."""
            self.play(m1.animate.shift(SUBIDA * DOWN),
                      m2.animate.shift(SUBIDA * DOWN),
                      run_time=0.20, rate_func=rate_functions.rush_into)
            self.add_sound(str(SONS / "martelo_grave_220.wav"))
            self.add_sound(str(SONS / "martelo_agudo_440.wav"))
            onda1 = Circle(radius=0.32, color=GRUV_FG,
                           stroke_width=5.0).move_to([X1, Y_FACE, 0.0])
            onda2 = Circle(radius=0.32, color=GRUV_YELLOW,
                           stroke_width=5.0).move_to([X2, Y_FACE, 0.0])
            self.add(onda1, onda2)
            self.play(onda1.animate.scale(2.8).set_opacity(0),
                      onda2.animate.scale(2.8).set_opacity(0),
                      bigorna.animate.shift(0.05 * RIGHT), run_time=0.15)
            self.play(bigorna.animate.shift(0.05 * LEFT), run_time=0.12)
            self.remove(onda1, onda2)
            self.play(m1.animate.shift(SUBIDA * UP),
                      m2.animate.shift(SUBIDA * UP), run_time=0.55)

        # ———— 1 e 2 · Um golpe de cada martelo ————
        golpe(m1, X1, GRUV_FG, "martelo_grave_220.wav", rot_f)
        self.wait(0.45)
        golpe(m2, X2, GRUV_YELLOW, "martelo_agudo_440.wav", rot_2f)
        self.wait(0.45)

        # ———— 3 · Golpe conjunto — ANTES do subtítulo ————
        golpe_duplo()
        self.wait(0.35)

        # ———— Subtítulo: a razão harmônica ————
        razao = VGroup(
            Text("12 : 6  =  2 : 1", font=FONT, color=GRUV_FG, font_size=54),
            Text("Diapasão — a oitava justa", font=FONT, color=GRUV_YELLOW,
                 font_size=34, slant=ITALIC),
        ).arrange(DOWN, buff=0.22).move_to([0.0, -3.15, 0.0])
        self.play(FadeIn(razao), run_time=0.9)
        self.wait(0.6)

        # ———— 4 · Golpe conjunto — APÓS o subtítulo ————
        golpe_duplo()
        self.wait(0.9)

        # ———— Encerramento ————
        self.play(FadeOut(titulo), FadeOut(chao), FadeOut(bigorna),
                  FadeOut(m1), FadeOut(m2), FadeOut(rot_f), FadeOut(rot_2f),
                  FadeOut(razao), run_time=0.8)
        self.wait(0.3)
