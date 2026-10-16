"""
MISTAGOGOS · v01 · c06 — As Consonâncias Pitagóricas
Continua a mesma corda de 12 unidades do c04 (martelos_monocordio.py).
Uma aresta desliza e morde a corda em 8/12 (Diapente · a quinta 3:2) e
9/12 (Diatessaron · a quarta 4:3) — o método histórico do monocórdio de
Pitágoras. Para cada parte encurtada, uma NOVA corda nasce abaixo, com o
mesmo comprimento isolado pela aresta, vibrando inteira no seu próprio
fundamental (n=1, fisicamente correta) — a corda da quinta permanece
quando a da quarta nasce; as três ficam visíveis lado a lado, cada
uma com sua nota e frequência ao lado. Depois, o Epogdoon:
3/2 ÷ 4/3 = 9/8, e a régua de oitavas planetárias
(Mercúrio→Urano · Marte→Plutão).

Paleta Gruvbox · EB Garamond · sons em sons/ (se faltar um arquivo, roda muda)
"""

from pathlib import Path

import numpy as np

from manim import (
    DOWN,
    ITALIC,
    RIGHT,
    UP,
    Circumscribe,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    MathTex,
    ParametricFunction,
    Scene,
    Text,
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
GRUV_ORANGE = "#fe8019"
GRUV_AQUA = "#8ec07c"
GRUV_GRAY = "#a89984"
GRUV_DARK = "#3c3833"

FONT = "EB Garamond"
SONS = Path(__file__).resolve().parent / "sons"

# Geometria da corda (idêntica ao c04 — continuidade literal)
X0, X1 = -5.0, 4.2
SPAN = X1 - X0

# Três fileiras — corda 1 (fundamental, com a aresta), corda 2 (quinta,
# 8/12) e corda 3 (quarta, 9/12) — todas visíveis ao mesmo tempo, cada
# uma com nota+frequência ao lado da sua própria ponta direita.
Y_STR = 2.2
AMP = 0.5
SPEED = 4.0
CAV_Y_BITE = Y_STR - 0.20
CAV_Y_LOW = Y_STR - 0.32

Y_STR2 = 0.3
AMP2 = 0.45
SPEED2 = 3.5

Y_STR3 = -1.6
AMP3 = 0.45
SPEED3 = 3.0

CAPTION_Y = -3.2


def xde(frac):
    return X0 + SPAN * frac


class Consonancias(Scene):
    def tocar(self, wav):
        caminho = SONS / wav
        if caminho.exists():
            self.add_sound(str(caminho))

    def construct(self):
        self.camera.background_color = GRUV_BG

        # ———— Reconstituir a corda (continuidade com c04) ————
        pino_l = Dot([X0, Y_STR, 0.0], radius=0.09, color=GRUV_GRAY)
        pino_r = Dot([X1, Y_STR, 0.0], radius=0.09, color=GRUV_GRAY)
        pinos = VGroup(pino_l, pino_r)
        repouso = Line([X0, Y_STR, 0.0], [X1, Y_STR, 0.0],
                       color=GRUV_FG, stroke_width=5.5)
        self.play(FadeIn(pinos), FadeIn(repouso), run_time=0.6)
        self.wait(0.3)
        self.remove(repouso)

        titulo = Text("As Consonâncias Pitagóricas", font=FONT, color=GRUV_AQUA,
                      font_size=36, slant=ITALIC).move_to([0.0, 3.55, 0.0])
        self.play(FadeIn(titulo), run_time=0.8)

        # ———— Motor: aresta deslizante morde a corda em qualquer fração ————
        tb = ValueTracker(1.0)       # fração vibrante (0, tb]
        cavx = ValueTracker(1.0)     # posição da aresta
        cavy = ValueTracker(CAV_Y_LOW)
        amp = ValueTracker(0.0)
        speed = ValueTracker(SPEED)
        fase = ValueTracker(0.0)
        fase.add_updater(lambda m, dt: m.increment_value(speed.get_value() * dt))
        self.add(fase)

        def ponte():
            return (Triangle(color=GRUV_YELLOW, stroke_width=2.5,
                             fill_color=GRUV_DARK, fill_opacity=0.95)
                    .scale(0.22).move_to([xde(cavx.get_value()), cavy.get_value(), 0.0]))

        cav = always_redraw(ponte)

        def vibrante():
            t = tb.get_value()
            a = amp.get_value()
            ph = fase.get_value()

            def f(u):
                return np.array([xde(u), Y_STR + a * np.sin(np.pi * u / t) * np.cos(ph), 0.0])

            return ParametricFunction(f, t_range=(0.0, t, 0.004),
                                      color=GRUV_FG, stroke_width=5.5)

        vib = always_redraw(vibrante)

        def resto():
            t = tb.get_value()
            if t > 0.995:
                return DashedLine([X1, Y_STR, 0.0], [X1, Y_STR, 0.0],
                                  color=GRUV_GRAY, stroke_width=2.5).set_opacity(0.0)
            return DashedLine([xde(t), Y_STR, 0.0], [X1, Y_STR, 0.0],
                              color=GRUV_GRAY, stroke_width=2.5).set_opacity(0.5)

        res = always_redraw(resto)
        self.add(vib, res)
        self.wait(0.3)

        def dedilha(wav, ring, extra=None):
            """extra = (tracker, valor_alvo) de uma corda secundária, tocada junto."""
            self.tocar(wav)
            anims = [amp.animate.set_value(AMP)]
            if extra is not None:
                anims.append(extra[0].animate.set_value(extra[1]))
            self.play(*anims, run_time=0.12, rate_func=rate_functions.rush_into)
            self.wait(ring)
            anims_off = [amp.animate.set_value(0.0)]
            if extra is not None:
                anims_off.append(extra[0].animate.set_value(0.0))
            self.play(*anims_off, run_time=0.45)

        def corda_fixa(frac, y, cor, speed):
            """Uma corda de comprimento fixo (0 a frac da corda original),
            presa nas duas pontas, vibrando inteira em n=1."""
            pino_l = Dot([X0, y, 0.0], radius=0.08, color=GRUV_GRAY)
            pino_r = Dot([xde(frac), y, 0.0], radius=0.08, color=GRUV_GRAY)
            amp_t = ValueTracker(0.0)
            fase_t = ValueTracker(0.0)
            fase_t.add_updater(lambda m, dt: m.increment_value(speed * dt))
            self.add(fase_t)

            def fn():
                a = amp_t.get_value()
                ph = fase_t.get_value()

                def f(t):
                    x = X0 + frac * SPAN * t
                    y_ = y + a * np.sin(np.pi * t) * np.cos(ph)
                    return np.array([x, y_, 0.0])

                return ParametricFunction(f, t_range=(0.0, 1.0, 0.004),
                                          color=cor, stroke_width=5.0)

            vib_t = always_redraw(fn)
            return pino_l, pino_r, vib_t, amp_t, fase_t

        # ———— Corda 1 — a fundamental: Lá · 220 Hz ————
        label1 = Text("Lá · 220 Hz", font=FONT, color=GRUV_FG,
                      font_size=28).next_to(pino_r, RIGHT, buff=0.3)
        self.play(FadeIn(label1), run_time=0.4)
        dedilha("harpa_la_220.wav", 1.0)
        self.wait(0.5)

        # ———— A aresta desliza a 8/12 — nasce a corda da quinta ————
        self.play(FadeIn(cav), tb.animate.set_value(8 / 12),
                  cavx.animate.set_value(8 / 12), cavy.animate.set_value(CAV_Y_BITE),
                  run_time=1.1)
        caption1 = Text("8/12 · Diapente — a quinta 3:2", font=FONT, color=GRUV_YELLOW,
                        font_size=30, slant=ITALIC).move_to([0.0, CAPTION_Y, 0.0])
        self.play(FadeIn(caption1), run_time=0.6)

        pino_l2, pino_r2, vib2, amp2, fase2 = corda_fixa(8 / 12, Y_STR2, GRUV_YELLOW, SPEED2)
        label2 = Text("Mi₄ · 330 Hz", font=FONT, color=GRUV_YELLOW,
                      font_size=28).next_to(pino_r2, RIGHT, buff=0.3)
        self.play(FadeIn(pino_l2), FadeIn(pino_r2), run_time=0.5)
        self.add(vib2)
        dedilha("harpa_mi4_330.wav", 1.3, extra=(amp2, AMP2))
        self.play(FadeIn(label2), run_time=0.4)
        self.wait(0.8)

        # ———— A aresta desliza a 9/12 — nasce a corda da quarta ————
        # ———— (nova corda — a da quinta permanece como está) ————
        self.play(FadeOut(caption1), tb.animate.set_value(9 / 12),
                  cavx.animate.set_value(9 / 12), run_time=0.9)
        caption2 = Text("9/12 · Diatessaron — a quarta 4:3", font=FONT, color=GRUV_ORANGE,
                        font_size=30, slant=ITALIC).move_to([0.0, CAPTION_Y, 0.0])
        self.play(FadeIn(caption2), run_time=0.6)

        pino_l3, pino_r3, vib3, amp3, fase3 = corda_fixa(9 / 12, Y_STR3, GRUV_ORANGE, SPEED3)
        label3 = Text("Ré₄ · 293 Hz", font=FONT, color=GRUV_ORANGE,
                      font_size=28).next_to(pino_r3, RIGHT, buff=0.3)
        self.play(FadeIn(pino_l3), FadeIn(pino_r3), run_time=0.5)
        self.add(vib3)
        dedilha("harpa_re4_293.wav", 1.3, extra=(amp3, AMP3))
        self.play(FadeIn(label3), run_time=0.4)
        self.wait(1.2)

        # ———— A aresta recolhe · as três cordas se apagam ————
        self.play(FadeOut(caption2), FadeOut(label1), FadeOut(label2), FadeOut(label3),
                  FadeOut(pino_l2), FadeOut(pino_r2), FadeOut(pino_l3), FadeOut(pino_r3),
                  tb.animate.set_value(1.0), cavy.animate.set_value(CAV_Y_LOW),
                  run_time=0.9)
        self.wait(0.3)
        self.remove(vib, res, cav, fase, vib2, fase2, vib3, fase3)
        corda_fim = Line([X0, Y_STR, 0.0], [X1, Y_STR, 0.0],
                         color=GRUV_FG, stroke_width=5.5)
        self.add(corda_fim)

        # ———— O Epogdoon: 3/2 ÷ 4/3 = 9/8 ————
        eq = MathTex(r"\frac{3}{2} \div \frac{4}{3} = ", r"\frac{9}{8}",
                    color=GRUV_FG, font_size=64).move_to([0.0, 0.5, 0.0])
        eq[1].set_color(GRUV_YELLOW)
        epog = Text("Epogdoon — o tom inteiro", font=FONT, color=GRUV_YELLOW,
                    font_size=32, slant=ITALIC).move_to([0.0, -0.5, 0.0])
        self.play(FadeIn(eq), run_time=1.0)
        self.wait(0.5)
        self.play(FadeIn(epog), run_time=0.6)
        self.play(Circumscribe(eq[1], color=GRUV_YELLOW, buff=0.1), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(eq), FadeOut(epog), FadeOut(titulo), FadeOut(corda_fim),
                  FadeOut(pinos), run_time=0.9)

        # ———— A régua de oitavas planetárias ————
        sub = Text("a mesma razão, na leitura astrológica moderna",
                   font=FONT, color=GRUV_AQUA, font_size=32,
                   slant=ITALIC).move_to([0.0, 2.6, 0.0])
        self.play(FadeIn(sub), run_time=0.8)

        regua_y = 0.0
        freqs = [110, 220, 440, 880]
        xs = np.linspace(-4.5, 4.5, 4)
        regua = Line([xs[0], regua_y, 0.0], [xs[-1], regua_y, 0.0],
                    color=GRUV_GRAY, stroke_width=2.5)
        marcas = VGroup()
        for x, f in zip(xs, freqs):
            marcas.add(Line([x, regua_y - 0.1, 0.0], [x, regua_y + 0.1, 0.0],
                            color=GRUV_GRAY, stroke_width=2.5))
            marcas.add(Text(f"{f} Hz", font=FONT, color=GRUV_GRAY,
                            font_size=22).next_to([x, regua_y, 0.0], DOWN, buff=0.3))
        self.play(FadeIn(regua), FadeIn(marcas), run_time=0.9)
        self.wait(0.3)

        def par(xa, xb, nome_a, nome_b, cor):
            da = Dot([xa, regua_y, 0.0], radius=0.07, color=cor)
            db = Dot([xb, regua_y, 0.0], radius=0.07, color=cor)
            ta = Text(nome_a, font=FONT, color=cor,
                     font_size=26).next_to(da, UP, buff=0.55)
            tb_ = Text(nome_b, font=FONT, color=cor,
                      font_size=26).next_to(db, UP, buff=0.55)
            arco = ParametricFunction(
                lambda t: np.array([xa + (xb - xa) * t,
                                    regua_y + 0.9 * np.sin(np.pi * t), 0.0]),
                t_range=(0.0, 1.0, 0.01), color=cor, stroke_width=3.0,
            )
            return VGroup(da, db, ta, tb_, arco)

        par1 = par(xs[0], xs[1], "Mercúrio", "Urano", GRUV_YELLOW)
        par2 = par(xs[2], xs[3], "Marte", "Plutão", GRUV_ORANGE)
        self.play(FadeIn(par1), run_time=0.9)
        self.wait(0.6)
        self.play(FadeIn(par2), run_time=0.9)
        self.wait(0.6)

        caption = Text("oitavas superiores — 2:1", font=FONT, color=GRUV_FG,
                       font_size=28, slant=ITALIC).move_to([0.0, -2.6, 0.0])
        self.play(FadeIn(caption), run_time=0.8)
        self.wait(1.8)

        # ———— Encerramento ————
        self.play(FadeOut(sub), FadeOut(regua), FadeOut(marcas), FadeOut(par1),
                  FadeOut(par2), FadeOut(caption), run_time=1.0)
        self.wait(0.3)
