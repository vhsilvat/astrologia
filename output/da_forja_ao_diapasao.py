"""
MISTAGOGOS · O Diapasão — da forja ao monocórdio
Nicômaco de Gerasa · Enchiridion Harmonices
12 : 6 → os martelos viram as pontas da corda, a bigorna vira a aresta
(a aresta · o diapasão) · frações sem simplificar: 12/12 · 6/12 · 4/12 · 3/12
A aresta espera recolhida ao lado, sobe e morde a cada divisão; retirada,
a corda inteira vibra nos modos. Contas de divisão pousadas sobre a corda.
Saltos sucessivos 2:1 · 3:2 · 4:3 · a série harmônica de Lá · 880 Hz.
A corda e os pinos permanecem no fim — âncora para c06 · Harmonia Mundi.
Paleta Gruvbox · EB Garamond · tings de bigorna + harpa (Karplus-Strong)
"""

from pathlib import Path

import numpy as np

from manim import (
    DOWN,
    ITALIC,
    LEFT,
    RIGHT,
    UP,
    Circle,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    ParametricFunction,
    Polygon,
    Rectangle,
    ReplacementTransform,
    Scene,
    Text,
    Transform,
    Triangle,
    VGroup,
    ValueTracker,
    always_redraw,
    rate_functions,
)

# ———— Paleta Gruvbox ————
GRUV_BG = "#282828"
GRUV_FG = "#ebdbb2"
GRUV_YELLOW = "#fabd2f"
GRUV_GREEN = "#b8bb26"
GRUV_ORANGE = "#fe8019"
GRUV_AQUA = "#8ec07c"
GRUV_RED = "#cc241d"
GRUV_GRAY = "#a89984"
GRUV_NEUT = "#7c6f64"
GRUV_DARK = "#3c3833"

FONT = "EB Garamond"
SONS = Path(__file__).resolve().parent / "sons"

# Forja
BIGORNA_Y = -1.40
Y_FACE = BIGORNA_Y + 0.75
Y_CHAO = -2.15
XH1, XH2 = -0.55, 0.35
SUBIDA = 1.20

# Monocórdio (12 unidades)
X0, X1 = -5.0, 5.0
SPAN = X1 - X0
Y_STR = 0.40
A_AMP = 0.60
SPEED = 4.0
CAV_Y_BITE = Y_STR - 0.20   # aresta mordendo: o ápice cruza a corda
CAV_Y_LOW = Y_STR - 0.32    # aresta recolhida: o ápice fica sob a corda
PARK_X = 1.08               # fração onde a aresta espera, além do pino direito
BEAD_Y = Y_STR + 0.10       # contas de divisão pousadas sobre a corda


def xde(frac):
    return X0 + SPAN * frac


class Diapasao(Scene):
    def construct(self):
        self.camera.background_color = GRUV_BG

        # ———— Cabeçalho único ————
        cab = Text("Nicômaco de Gerasa · Enchiridion Harmonices",
                   font=FONT, color=GRUV_AQUA, font_size=38,
                   slant=ITALIC).move_to([0.0, 3.35, 0.0])
        self.play(FadeIn(cab), run_time=1.0)
        self.wait(1.4)

        # ———— A FORJA ————
        chao = Line([-6.4, Y_CHAO, 0.0], [6.4, Y_CHAO, 0.0],
                    color=GRUV_NEUT, stroke_width=2.5)
        pontos = [
            (-0.90, 0.55, 0.0), (0.90, 0.55, 0.0), (1.75, 0.28, 0.0), (0.90, 0.02, 0.0),
            (0.62, -0.50, 0.0), (0.95, -0.95, 0.0), (-0.95, -0.95, 0.0), (-0.62, -0.50, 0.0),
            (-1.75, 0.28, 0.0), (-0.90, 0.02, 0.0),
        ]
        bigorna = Polygon(*pontos, color=GRUV_GRAY, stroke_width=3.0,
                          fill_color=GRUV_DARK, fill_opacity=1.0,
                          ).move_to([0.0, BIGORNA_Y, 0.0])
        self.play(FadeIn(chao), FadeIn(bigorna), run_time=0.9)
        self.wait(1.6)

        def martelo(cor, comp, alt, peso_txt, x):
            y_rest = Y_FACE + alt / 2 + SUBIDA
            cabeca = Rectangle(width=comp, height=alt, color=cor, stroke_width=3.0,
                               fill_color=cor, fill_opacity=0.92,
                               ).move_to([x, y_rest, 0.0])
            cabo = Rectangle(width=0.13, height=1.05, color=GRUV_GRAY,
                             stroke_width=2.5, fill_color=GRUV_GRAY,
                             fill_opacity=0.85).next_to(cabeca, UP, buff=0.03)
            peso = Text(peso_txt, font=FONT, color=cor,
                        font_size=30).next_to(cabo, UP, buff=0.14)
            return VGroup(cabeca, cabo, peso)

        m1 = martelo(GRUV_FG, 0.95, 0.40, "12 lb", XH1)
        m2 = martelo(GRUV_YELLOW, 0.62, 0.30, "6 lb", XH2)
        self.play(FadeIn(m1), FadeIn(m2), run_time=0.8)
        self.wait(2.2)

        rot_f = Text("Lá · 220 Hz", font=FONT, color=GRUV_GREEN,
                     font_size=34).move_to([-4.80, -2.80, 0.0])
        rot_2f = Text("Lá⁴ · 440 Hz", font=FONT, color=GRUV_YELLOW,
                      font_size=34).move_to([4.80, -2.80, 0.0])

        def golpe(g, x, cor, wav, rotulo=None):
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
            self.play(m1.animate.shift(SUBIDA * DOWN),
                      m2.animate.shift(SUBIDA * DOWN),
                      run_time=0.20, rate_func=rate_functions.rush_into)
            self.add_sound(str(SONS / "martelo_grave_220.wav"))
            self.add_sound(str(SONS / "martelo_agudo_440.wav"))
            o1 = Circle(radius=0.32, color=GRUV_FG,
                        stroke_width=5.0).move_to([XH1, Y_FACE, 0.0])
            o2 = Circle(radius=0.32, color=GRUV_YELLOW,
                        stroke_width=5.0).move_to([XH2, Y_FACE, 0.0])
            self.add(o1, o2)
            self.play(o1.animate.scale(2.8).set_opacity(0),
                      o2.animate.scale(2.8).set_opacity(0),
                      bigorna.animate.shift(0.05 * RIGHT), run_time=0.15)
            self.play(bigorna.animate.shift(0.05 * LEFT), run_time=0.12)
            self.remove(o1, o2)
            self.play(m1.animate.shift(SUBIDA * UP),
                      m2.animate.shift(SUBIDA * UP), run_time=0.55)

        # 4 tempos aprovados
        golpe(m1, XH1, GRUV_FG, "martelo_grave_220.wav", rot_f)
        self.wait(2.6)
        golpe(m2, XH2, GRUV_YELLOW, "martelo_agudo_440.wav", rot_2f)
        self.wait(2.6)
        golpe_duplo()
        self.wait(2.0)

        # Cartaz — fração SEM simplificar
        cartaz = VGroup(
            Text("12 : 6", font=FONT, color=GRUV_FG, font_size=54),
            Text("Diapasão — a oitava justa", font=FONT, color=GRUV_YELLOW,
                 font_size=34, slant=ITALIC),
        ).arrange(DOWN, buff=0.22).move_to([0.0, -3.15, 0.0])
        self.play(FadeIn(cartaz), run_time=0.9)
        self.wait(3.6)
        golpe_duplo()
        self.wait(4.4)

        # ———— TRANSIÇÃO: martelos → pontas · bigorna → aresta ————
        aresta_txt = Text("a aresta · o diapasão", font=FONT, color=GRUV_YELLOW,
                          font_size=34, slant=ITALIC).move_to([0.0, -2.60, 0.0])
        self.play(FadeOut(rot_f), FadeOut(rot_2f),
                  Transform(cartaz, aresta_txt), run_time=0.8)
        self.wait(1.6)

        pinoL = Dot([XH1 - 0.8, Y_STR, 0.0], radius=0.09, color=GRUV_FG)
        pinoR = Dot([XH2 + 0.8, Y_STR, 0.0], radius=0.09, color=GRUV_FG)

        cavx = ValueTracker(0.5)        # posição da aresta
        cavy = ValueTracker(CAV_Y_LOW)  # altura: recolhida → à mordida

        def ponte():
            return (Triangle(color=GRUV_YELLOW, stroke_width=2.5,
                             fill_color=GRUV_DARK, fill_opacity=0.95)
                    .scale(0.24).move_to(
                        [xde(cavx.get_value()), cavy.get_value(), 0.0]))

        cav = always_redraw(ponte)
        cav_snap = (Triangle(color=GRUV_YELLOW, stroke_width=2.5,
                             fill_color=GRUV_DARK, fill_opacity=0.95)
                    .scale(0.24).move_to([xde(0.5), CAV_Y_LOW, 0.0]))
        self.play(
            ReplacementTransform(m1[0], pinoL),
            ReplacementTransform(m2[0], pinoR),
            FadeOut(m1[1], m1[2], m2[1], m2[2]),
            ReplacementTransform(bigorna, cav_snap),
            FadeOut(chao),
            run_time=1.0,
        )
        self.remove(cav_snap)
        self.add(cav)
        self.wait(0.4)

        corda_sta = Line([X0, Y_STR, 0.0], [X1, Y_STR, 0.0],
                         color=GRUV_FG, stroke_width=5.0)
        self.play(pinoL.animate.move_to([X0, Y_STR, 0.0]),
                  pinoR.animate.move_to([X1, Y_STR, 0.0]),
                  Create(corda_sta),
                  cavx.animate.set_value(PARK_X), run_time=1.1)
        self.remove(corda_sta)

        # ———— MOTOR DO MONOCÓRDIO (12 unidades) ————
        tb = ValueTracker(1.0)     # ponto onde a corda vibra até
        amp = ValueTracker(0.0)
        speed = ValueTracker(SPEED)
        fase = ValueTracker(0.0)
        fase.add_updater(lambda m, dt: m.increment_value(speed.get_value() * dt))
        self.add(fase)

        def vibrante():
            t = tb.get_value()
            a = amp.get_value()
            ph = fase.get_value()

            def f(u):
                return np.array([xde(u),
                                 Y_STR + a * np.sin(np.pi * u / t) * np.cos(ph),
                                 0.0])

            return ParametricFunction(f, t_range=(0.0, t, 0.004),
                                      color=GRUV_FG, stroke_width=5.0)

        vib = always_redraw(vibrante)

        def resto():
            t = tb.get_value()
            if t > 0.995:
                return DashedLine([X1, Y_STR, 0.0], [X1, Y_STR, 0.0],
                                  color=GRUV_GRAY,
                                  stroke_width=2.5).set_opacity(0.0)
            return DashedLine([xde(t), Y_STR, 0.0], [X1, Y_STR, 0.0],
                              color=GRUV_GRAY,
                              stroke_width=2.5).set_opacity(0.5)

        res = always_redraw(resto)
        self.add(vib, res)
        self.wait(0.9)

        nota = Text("Lá · 220 Hz", font=FONT, color=GRUV_GREEN,
                    font_size=38).move_to([0.0, -1.55, 0.0])
        raz = Text("12/12 · corda inteira", font=FONT, color=GRUV_FG,
                   font_size=30).move_to([0.0, -2.25, 0.0])

        def troca(txt_nota, cor_nota, txt_raz):
            nova = Text(txt_nota, font=FONT, color=cor_nota,
                        font_size=38).move_to(nota)
            nvz = Text(txt_raz, font=FONT, color=GRUV_FG,
                       font_size=30).move_to(raz)
            self.play(Transform(nota, nova), Transform(raz, nvz), run_time=0.7)

        def dedilha(wav, ring):
            self.add_sound(str(SONS / wav))
            self.play(amp.animate.set_value(A_AMP), run_time=0.12,
                      rate_func=rate_functions.rush_into)
            self.wait(ring)
            self.play(amp.animate.set_value(0.0), run_time=0.5)

        no_12 = Dot([xde(0.5), BEAD_Y, 0.0], radius=0.055, color=GRUV_RED)
        nos_13 = VGroup(Dot([xde(1 / 3), BEAD_Y, 0.0], radius=0.055, color=GRUV_RED),
                        Dot([xde(2 / 3), BEAD_Y, 0.0], radius=0.055, color=GRUV_RED))
        nos_14 = VGroup(Dot([xde(0.25), BEAD_Y, 0.0], radius=0.055, color=GRUV_RED),
                        Dot([xde(0.75), BEAD_Y, 0.0], radius=0.055, color=GRUV_RED))

        # ———— 12/12 · Lá 220 (o tom do martelo de 12 lb) ————
        self.play(FadeIn(nota), FadeIn(raz), run_time=0.6)
        self.wait(0.4)
        dedilha("harpa_la_220.wav", 1.5)
        self.wait(2.8)

        # ———— a aresta morde: 6/12 · Lá⁴ 440 (o tom do martelo de 6 lb) ————
        self.play(tb.animate.set_value(0.5),
                  cavy.animate.set_value(CAV_Y_BITE),
                  cavx.animate.set_value(0.5),
                  FadeOut(cartaz), run_time=1.0)
        self.play(FadeIn(no_12), run_time=0.3)
        self.wait(0.3)
        dedilha("harpa_la4_440.wav", 1.3)
        self.wait(1.8)
        troca("Lá⁴ · 440 Hz", GRUV_YELLOW, "6/12 · metade da corda")
        self.wait(2.4)

        # ———— 4/12 · Mi⁵ 660 ————
        self.play(tb.animate.set_value(1 / 3), cavx.animate.set_value(1 / 3),
                  run_time=0.85)
        self.wait(0.2)
        dedilha("harpa_mi5_660.wav", 1.2)
        self.play(FadeIn(nos_13), run_time=0.3)
        self.wait(1.6)
        troca("Mi⁵ · 660 Hz", GRUV_ORANGE, "4/12 · o terço")
        self.wait(2.2)

        # ———— 3/12 · Lá⁵ 880 ————
        self.play(tb.animate.set_value(0.25), cavx.animate.set_value(0.25),
                  run_time=0.8)
        dedilha("harpa_la5_880.wav", 1.1)
        self.play(FadeIn(nos_14), run_time=0.3)
        self.wait(1.4)
        troca("Lá⁵ · 880 Hz", GRUV_AQUA, "3/12 · o quarto")
        self.wait(2.0)

        # ———— FINAL: a aresta se retira ao bordo · a corda vibra nos modos ————
        self.play(tb.animate.set_value(1.0),
                  cavy.animate.set_value(CAV_Y_LOW),
                  cavx.animate.set_value(PARK_X),
                  speed.animate.set_value(5.5),
                  FadeOut(raz), run_time=1.2)
        self.remove(vib, res)

        modo = ValueTracker(1.0)

        def modo_vib():
            mo = modo.get_value()
            a = amp.get_value()
            ph = fase.get_value()

            def f(t):
                return np.array(
                    [xde(t),
                     Y_STR + a * np.sin(mo * np.pi * t) * np.sin(np.pi * t) * np.cos(ph),
                     0.0])

            return ParametricFunction(f, t_range=(0.0, 1.0, 0.004),
                                      color=GRUV_FG, stroke_width=5.0)

        mvib = always_redraw(modo_vib)
        self.add(mvib)
        self.wait(0.5)

        self.play(amp.animate.set_value(0.55), run_time=0.1)
        self.add_sound(str(SONS / "harpa_la_220.wav"))
        tn2 = Text("Lá⁴ · 440 Hz", font=FONT, color=GRUV_YELLOW,
                   font_size=38).move_to(nota)
        self.play(modo.animate.set_value(2.0), speed.animate.set_value(6.5),
                  Transform(nota, tn2), run_time=0.55)
        self.add_sound(str(SONS / "harpa_la4_440.wav"))
        self.wait(0.8)
        tn3 = Text("Mi⁵ · 660 Hz", font=FONT, color=GRUV_ORANGE,
                   font_size=38).move_to(nota)
        self.play(modo.animate.set_value(3.0), speed.animate.set_value(7.5),
                  Transform(nota, tn3), run_time=0.6)
        self.add_sound(str(SONS / "harpa_mi5_660.wav"))
        self.wait(0.8)
        tn4 = Text("Lá⁵ · 880 Hz", font=FONT, color=GRUV_AQUA,
                   font_size=38).move_to(nota)
        self.play(modo.animate.set_value(4.0), speed.animate.set_value(8.5),
                  Transform(nota, tn4), run_time=0.7)
        self.add_sound(str(SONS / "harpa_la5_880.wav"))
        self.wait(1.0)

        # ———— eco dos saltos sucessivos (semeadura de c06) ————
        saltos = Text("os saltos sucessivos — 2:1 · 3:2 · 4:3",
                      font=FONT, color=GRUV_FG, font_size=26,
                      slant=ITALIC).move_to([0.0, -3.05, 0.0])
        self.play(FadeIn(saltos), run_time=0.8)
        self.wait(2.0)

        # ———— Em conjunto: a série harmônica de Lá ————
        self.add_sound(str(SONS / "harpa_la_220.wav"), gain=0.45)
        self.add_sound(str(SONS / "harpa_la4_440.wav"), gain=0.45)
        self.add_sound(str(SONS / "harpa_mi5_660.wav"), gain=0.45)
        self.add_sound(str(SONS / "harpa_la5_880.wav"), gain=0.45)
        tconj = Text("Lá · 880 Hz", font=FONT, color=GRUV_YELLOW,
                     font_size=46).move_to(nota)
        rconj = Text("a série harmônica de Lá", font=FONT, color=GRUV_FG,
                     font_size=28, slant=ITALIC).move_to(raz)
        self.play(modo.animate.set_value(4.0), speed.animate.set_value(9.5),
                  Transform(nota, tconj), FadeIn(rconj), run_time=2.2)
        self.wait(2.4)

        # ———— Harmonia Mundi ————
        mundi = Text("Harmonia Mundi", font=FONT, color=GRUV_YELLOW,
                     font_size=52, slant=ITALIC).move_to([0.0, -2.70, 0.0])
        self.play(Transform(nota, mundi), FadeOut(rconj), FadeOut(saltos),
                  run_time=1.0)
        self.wait(4.0)

        # ———— Encerramento: a corda permanece ————
        self.play(amp.animate.set_value(0.0), run_time=0.6)
        self.remove(mvib, fase, tb, amp, modo, speed, cavx, cavy)
        corda_fim = Line([X0, Y_STR, 0.0], [X1, Y_STR, 0.0],
                         color=GRUV_FG, stroke_width=5.0)
        self.add(corda_fim)
        self.play(FadeOut(cab), FadeOut(nota), FadeOut(no_12),
                  FadeOut(nos_13), FadeOut(nos_14), run_time=0.9)
        self.wait(3.0)
