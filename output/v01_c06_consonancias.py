"""
MISTAGOGOS · c06 — As Consonâncias Pitagóricas
Diapente 3:2 (8/12) · Diatessaron 4:3 (9/12) · Epogdoon 9:8 — a razão entre elas
Continuação literal de O Diapasão (c04): a mesma corda de 12 unidades,
os mesmos pinos, a mesma aresta estacionada. A régua das oitavas superiores:
Mercúrio → Urano · Marte → Plutão (2:1). Saída: a régua ondula — a água de c07.
Paleta Gruvbox · EB Garamond · harpas Karplus-Strong travadas na tônica.
"""

from pathlib import Path

import numpy as np

from manim import (
    ApplyWave,
    Circumscribe,
    CurvedArrow,
    DashedLine,
    DOWN,
    Dot,
    FadeIn,
    FadeOut,
    ITALIC,
    LEFT,
    Line,
    ParametricFunction,
    RIGHT,
    Scene,
    TAU,
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
GRUV_BLUE = "#83a598"
GRUV_RED = "#cc241d"
GRUV_GRAY = "#a89984"
GRUV_NEUT = "#7c6f64"
GRUV_DARK = "#3c3833"

FONT = "EB Garamond"
SONS = Path(__file__).resolve().parent / "sons"

# Monocórdio (12 unidades) — idêntico à c04
X0, X1 = -5.0, 5.0
SPAN = X1 - X0
Y_STR = 0.40
A_AMP = 0.60
SPEED = 4.0
CAV_Y_BITE = Y_STR - 0.20   # aresta mordendo: o ápice cruza a corda
CAV_Y_LOW = Y_STR - 0.32    # aresta recolhida: o ápice fica sob a corda
PARK_X = 1.08               # fração onde a aresta espera, além do pino direito
BEAD_Y = Y_STR + 0.10       # contas de divisão pousadas sobre a corda
Y_REG = -1.75               # altura da régua das oitavas


def xde(frac):
    return X0 + SPAN * frac


class Consonancias(Scene):
    def construct(self):
        self.camera.background_color = GRUV_BG

        # ———— Cabeçalho ————
        cab = Text("As Consonâncias Pitagóricas", font=FONT, color=GRUV_AQUA,
                   font_size=38, slant=ITALIC).move_to([0.0, 3.35, 0.0])
        self.play(FadeIn(cab), run_time=0.8)
        self.wait(1.0)

        # ———— MOTOR: a mesma corda de 12 unidades ————
        tb = ValueTracker(1.0)
        cavx = ValueTracker(PARK_X)
        cavy = ValueTracker(CAV_Y_LOW)
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

        def ponte():
            return (Triangle(color=GRUV_YELLOW, stroke_width=2.5,
                             fill_color=GRUV_DARK, fill_opacity=0.95)
                    .scale(0.24).move_to(
                        [xde(cavx.get_value()), cavy.get_value(), 0.0]))

        cav = always_redraw(ponte)
        self.add(vib, res, cav)

        pinos = VGroup(
            Dot([X0, Y_STR, 0.0], radius=0.09, color=GRUV_FG),
            Dot([X1, Y_STR, 0.0], radius=0.09, color=GRUV_FG),
        )
        self.play(FadeIn(pinos), run_time=0.5)

        nota = Text("Lá · 220 Hz", font=FONT, color=GRUV_GREEN,
                    font_size=38).move_to([0.0, -1.55, 0.0])
        raz = Text("12/12 · a tônica", font=FONT, color=GRUV_FG,
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

        # ———— A tônica: 12/12 · Lá 220 ————
        self.play(FadeIn(nota), FadeIn(raz), run_time=0.6)
        dedilha("harpa_la_220.wav", 1.3)
        self.wait(3.6)

        # ———— 8/12 · Diapente — a quinta 3:2 ————
        self.play(tb.animate.set_value(2.0 / 3.0),
                  cavy.animate.set_value(CAV_Y_BITE),
                  cavx.animate.set_value(2.0 / 3.0), run_time=0.9)
        dedilha("harpa_mi4_330.wav", 1.2)
        no_8 = Dot([xde(2.0 / 3.0), BEAD_Y, 0.0], radius=0.055, color=GRUV_RED)
        self.play(FadeIn(no_8), run_time=0.3)
        troca("Mi⁴ · 330 Hz", GRUV_ORANGE, "8/12 · Diapente — a quinta 3:2")
        self.wait(5.4)

        # ———— 9/12 · Diatessaron — a quarta 4:3 ————
        self.play(tb.animate.set_value(0.75),
                  cavx.animate.set_value(0.75), run_time=0.85)
        dedilha("harpa_re4_293.wav", 1.2)
        no_9 = Dot([xde(0.75), BEAD_Y, 0.0], radius=0.055, color=GRUV_RED)
        self.play(FadeIn(no_9), run_time=0.3)
        troca("Ré⁴ · 293,3 Hz", GRUV_AQUA, "9/12 · Diatessaron — a quarta 4:3")
        self.wait(4.9)

        # ———— O Epogdoon: a razão entre elas ————
        def fracao(num, den, cor):
            n = Text(num, font=FONT, color=cor, font_size=36)
            d = Text(den, font=FONT, color=cor, font_size=36)
            tr = Line(LEFT, RIGHT, color=cor, stroke_width=3.0)
            tr.set_width(max(n.width, d.width) * 1.14)
            return VGroup(n, tr, d).arrange(DOWN, buff=0.09)

        frac_32 = fracao("3", "2", GRUV_ORANGE)
        frac_43 = fracao("4", "3", GRUV_AQUA)
        frac_98 = fracao("9", "8", GRUV_YELLOW)
        sinal_div = Text("÷", font=FONT, color=GRUV_FG, font_size=40)
        sinal_eq = Text("=", font=FONT, color=GRUV_FG, font_size=40)
        frac = (VGroup(frac_32, sinal_div, frac_43, sinal_eq, frac_98)
                .arrange(RIGHT, buff=0.40).move_to([0.0, 2.10, 0.0]))
        self.play(FadeIn(frac), run_time=1.0)
        self.add_sound(str(SONS / "harpa_si3_247.wav"), gain=0.45)
        self.play(Circumscribe(frac_98, color=GRUV_YELLOW, buff=0.14,
                               run_time=1.2))
        epo = Text("Epogdoon — o tom inteiro", font=FONT, color=GRUV_FG,
                   font_size=30, slant=ITALIC).next_to(frac, DOWN, buff=0.30)
        self.play(FadeIn(epo), run_time=0.6)
        self.wait(7.2)

        # ———— A régua das oitavas superiores ————
        self.play(FadeOut(nota), FadeOut(raz), FadeOut(no_8), FadeOut(no_9),
                  FadeOut(frac), FadeOut(epo), run_time=0.6)
        self.play(tb.animate.set_value(1.0),
                  cavy.animate.set_value(CAV_Y_LOW),
                  cavx.animate.set_value(PARK_X), run_time=0.8)

        regua = Line([-5.6, Y_REG, 0.0], [5.6, Y_REG, 0.0],
                     color=GRUV_FG, stroke_width=3.5)

        def planeta(x, nome, cor):
            dot = Dot([x, Y_REG, 0.0], radius=0.10, color=cor)
            rot = Text(nome, font=FONT, color=cor, font_size=26
                       ).next_to(dot, DOWN, buff=0.22)
            return VGroup(dot, rot)

        p_mercurio = planeta(-4.0, "Mercúrio", GRUV_GRAY)
        p_urano = planeta(-1.0, "Urano", GRUV_BLUE)
        p_marte = planeta(1.0, "Marte", GRUV_RED)
        p_plutao = planeta(4.0, "Plutão", GRUV_NEUT)

        arco1 = CurvedArrow([-4.0, Y_REG + 0.18, 0.0], [-1.0, Y_REG + 0.18, 0.0],
                            angle=-TAU / 8, color=GRUV_YELLOW, stroke_width=3.5)
        arco2 = CurvedArrow([1.0, Y_REG + 0.18, 0.0], [4.0, Y_REG + 0.18, 0.0],
                            angle=-TAU / 8, color=GRUV_YELLOW, stroke_width=3.5)
        r21_1 = Text("2:1", font=FONT, color=GRUV_YELLOW,
                     font_size=28).move_to([-2.5, -0.88, 0.0])
        r21_2 = Text("2:1", font=FONT, color=GRUV_YELLOW,
                     font_size=28).move_to([2.5, -0.88, 0.0])
        cap = Text("as oitavas superiores", font=FONT, color=GRUV_YELLOW,
                   font_size=30, slant=ITALIC).move_to([0.0, -3.05, 0.0])

        self.play(FadeIn(regua), FadeIn(p_mercurio), FadeIn(p_urano),
                  FadeIn(cap), run_time=0.8)
        self.add_sound(str(SONS / "harpa_la_220.wav"), gain=0.45)
        self.add_sound(str(SONS / "harpa_la4_440.wav"), gain=0.45)
        self.play(FadeIn(arco1), FadeIn(r21_1), run_time=0.9)
        self.wait(2.4)
        self.add_sound(str(SONS / "harpa_la4_440.wav"), gain=0.45)
        self.add_sound(str(SONS / "harpa_la5_880.wav"), gain=0.45)
        self.play(FadeIn(p_marte), FadeIn(p_plutao),
                  FadeIn(arco2), FadeIn(r21_2), run_time=0.9)
        self.wait(3.4)

        # ———— Saída: a última onda ondula (âncora para a água de c07) ————
        self.play(ApplyWave(regua, amplitude=0.22, run_time=1.6))

        self.remove(vib, res, cav)
        corda_fim = Line([X0, Y_STR, 0.0], [X1, Y_STR, 0.0],
                         color=GRUV_FG, stroke_width=5.0)
        self.add(corda_fim)
        self.play(FadeOut(corda_fim), FadeOut(pinos), FadeOut(regua),
                  FadeOut(p_mercurio), FadeOut(p_urano), FadeOut(p_marte),
                  FadeOut(p_plutao), FadeOut(arco1), FadeOut(arco2),
                  FadeOut(r21_1), FadeOut(r21_2), FadeOut(cap),
                  FadeOut(cab), run_time=1.0)
        fase.clear_updaters()
        self.remove(fase, tb, amp, speed, cavx, cavy)
        self.wait(2.6)
