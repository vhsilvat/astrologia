"""
MISTAGOGOS · demo de câmera 3D
Como girar os eixos no Manim: ThreeDScene controla phi (inclinação ~eixo x),
theta (órbita ~eixo z) e gamma (rolagem da lente) no momento do render.
Compatível com Cairo (render final 1080p60) e OpenGL (--preview interativo).
Paleta Gruvbox · Tipografia EB Garamond · Tons 220/440/660 Hz + acorde
"""

from pathlib import Path

import numpy as np

from manim import (
    DEGREES,
    DOWN,
    FadeIn,
    FadeOut,
    ITALIC,
    ParametricFunction,
    ThreeDAxes,
    ThreeDScene,
    Text,
    VGroup,
    ValueTracker,
    always_redraw,
)

# ———— Paleta Gruvbox ————
GRUV_BG = "#282828"      # fundo
GRUV_FG = "#ebdbb2"      # texto e linhas principais
GRUV_YELLOW = "#fabd2f"  # 2º harmônico · destaques
GRUV_GREEN = "#b8bb26"   # 3º harmônico
GRUV_AQUA = "#8ec07c"   # subtítulo
GRUV_BLUE = "#83a598"   # rótulos dos eixos
GRUV_GRAY = "#a89984"   # eixos

FONT = "EB Garamond"
SONS = Path(__file__).resolve().parent / "sons"  # pasta sons/ ao lado do script

X0, X1 = -3.0, 3.0
SPAN = X1 - X0
PHASE_SPEED = 4.0
ZS = [-1.6, 0.0, 1.6]                     # empilhamento simétrico no eixo z
CORES = [GRUV_FG, GRUV_YELLOW, GRUV_GREEN]
AMPS = [0.55, 0.48, 0.42]
ETIQUETAS = ["1:1 · f", "1:2 · 2f", "1:3 · 3f"]
SONS_MODOS = ["tom_fundamental_220.wav", "tom_oitava_440.wav", "tom_quinta_660.wav"]


class Harmonia3D(ThreeDScene):
    def construct(self):
        # Fundo Gruvbox: na câmera (Cairo) e no renderer (OpenGL), sem quebrar se ausente.
        try:
            self.camera.background_color = GRUV_BG
            if hasattr(self.renderer, "background_color"):
                self.renderer.background_color = GRUV_BG
        except Exception:
            pass

        # ———— Análise: leitura dos ângulos da câmera no log ————
        def camera_log(tag):
            try:
                phi = self.camera.get_phi() / DEGREES
                theta = self.camera.get_theta() / DEGREES
                gamma = self.camera.get_gamma() / DEGREES
            except AttributeError:
                # OpenGLCamera expõe euler_angles = [theta, phi, gamma] em radianos
                t_e, p_e, g_e = self.camera.euler_angles
                phi, theta, gamma = p_e / DEGREES, t_e / DEGREES, g_e / DEGREES
            print(f"[CAMERA {tag}] phi={phi:.1f}° theta={theta:.1f}° gamma={gamma:.1f}°")

        # ———— Sons: arquivos ao lado do script; aviso em vez de quebrar ————
        def tocar(arquivo):
            p = SONS / arquivo
            try:
                if p.exists():
                    self.add_sound(str(p))
                else:
                    print(f"[AVISO] som ausente (copie a pasta sons/ junto ao script): {p}")
            except Exception as e:
                print(f"[AVISO] som ignorado neste modo de render ({type(e).__name__})")

        # Vista inicial: 50° de órbita à esquerda, 72° de inclinação a partir do zênite.
        # Sem zoom/focal_distance/frame_center: a OpenGLCamera v0.21 não implementa
        # set_zoom/_frame_center — esses parâmetros são exclusivos da câmera Cairo.
        self.set_camera_orientation(
            phi=72 * DEGREES,
            theta=-50 * DEGREES,
        )
        camera_log("inicial")

        # Texto preso à TELA (não distorce com a câmera)
        titulo = VGroup(
            Text("Harmônicos da Corda · Vista 3D",
                 font=FONT, color=GRUV_FG, font_size=46),
            Text("phi · theta · gamma — os três eixos da câmera",
                 font=FONT, color=GRUV_AQUA, font_size=27, slant=ITALIC),
        ).arrange(DOWN, buff=0.2).move_to([0.0, 3.35, 0.0])
        self.add_fixed_in_frame_mobjects(titulo)
        self.play(FadeIn(titulo), run_time=1.2)

        # Eixos do mundo 3D com rótulos x · y · z (pilha centrada na origem)
        eixos = ThreeDAxes(
            x_range=[-4.2, 4.2, 1],
            y_range=[-1.2, 1.2, 1],
            z_range=[-2.2, 2.2, 1],
            axis_config={"color": GRUV_GRAY, "stroke_width": 2.0},
        )
        rot_x = Text("x", font=FONT, color=GRUV_BLUE, slant=ITALIC,
                     font_size=34).move_to(eixos.x_axis.get_end() + np.array([0.28, -0.28, 0.0]))
        rot_y = Text("y", font=FONT, color=GRUV_BLUE, slant=ITALIC,
                     font_size=34).move_to(eixos.y_axis.get_end() + np.array([0.3, 0.18, 0.0]))
        rot_z = Text("z", font=FONT, color=GRUV_BLUE, slant=ITALIC,
                     font_size=34).move_to(eixos.z_axis.get_end() + np.array([-0.3, 0.12, 0.0]))
        self.play(FadeIn(eixos), FadeIn(rot_x), FadeIn(rot_y), FadeIn(rot_z), run_time=1.4)

        # Fase global + amplitudes controláveis
        fase = ValueTracker(0.0)
        fase.add_updater(lambda m, dt: m.increment_value(PHASE_SPEED * dt))
        self.add(fase)
        amp1, amp2, amp3 = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        amps = (amp1, amp2, amp3)

        def fio3d(n, tracker, z, cor):
            """Corda vibrante no modo n: vibração em y, empilhada em z."""

            def build():
                ph = fase.get_value()
                a = tracker.get_value()

                def curva(t):
                    return np.array(
                        [X0 + SPAN * t,
                         a * np.sin(n * np.pi * t) * np.cos(n * ph),
                         z]
                    )

                return ParametricFunction(
                    curva, t_range=(0.0, 1.0, 0.005),
                    color=cor, stroke_width=5.0,
                )

            return always_redraw(build)

        fios = [fio3d(n + 1, amps[n], ZS[n], CORES[n]) for n in range(3)]

        def etiqueta(txt, z, cor):
            """Rótulo posicionado no mundo 3D, sempre de frente para a câmera."""
            m = Text(txt, font=FONT, color=cor, font_size=30)
            m.move_to([X1 + 0.55, 0.0, z])
            self.add_fixed_orientation_mobjects(m)
            return m

        # ———— 1 · Fundamental ————
        self.add(fios[0])
        et0 = etiqueta(ETIQUETAS[0], ZS[0], CORES[0])
        self.play(FadeIn(et0), amp1.animate.set_value(AMPS[0]), run_time=1.0)
        tocar(SONS_MODOS[0])
        self.wait(1.8)

        # ———— 2 · GIRAR EM X (phi): câmera sobe até a vista de cima e volta ————
        self.move_camera(phi=30 * DEGREES, run_time=2.0)
        camera_log("phi=30 (vista de cima)")
        self.wait(0.6)
        self.move_camera(phi=72 * DEGREES, run_time=2.0)
        camera_log("phi=72 (vista lateral)")

        # ———— 3 · GIRAR EM Z (theta): órbita contínua ao redor do eixo z ————
        self.begin_ambient_camera_rotation(rate=0.22)
        self.wait(2.4)
        self.stop_ambient_camera_rotation()
        camera_log("fim da órbita theta")

        # ———— 4 · ROLL (gamma): rolagem da lente e retorno ————
        self.move_camera(gamma=16 * DEGREES, run_time=1.4)
        camera_log("gamma=16 (roll)")
        self.move_camera(gamma=0.0, run_time=1.2)

        # ———— 5 · Modos superiores empilhados em z ————
        self.add(fios[1])
        et1 = etiqueta(ETIQUETAS[1], ZS[1], CORES[1])
        self.play(FadeIn(et1), amp2.animate.set_value(AMPS[1]), run_time=1.0)
        tocar(SONS_MODOS[1])
        self.wait(1.6)

        self.add(fios[2])
        et2 = etiqueta(ETIQUETAS[2], ZS[2], CORES[2])
        self.play(FadeIn(et2), amp3.animate.set_value(AMPS[2]), run_time=1.0)
        tocar(SONS_MODOS[2])
        self.wait(1.6)

        # ———— 6 · Harmonia Mundi: órbita final com acorde ————
        # Etiqueta inferior sai de cena para não colidir com o texto final.
        self.play(FadeOut(et0), run_time=0.35)
        final_txt = VGroup(
            Text("Harmonia Mundi", font=FONT, color=GRUV_YELLOW,
                 font_size=46, slant=ITALIC),
            Text("câmera orbitando o eixo z", font=FONT,
                 color=GRUV_FG, font_size=27),
        ).arrange(DOWN, buff=0.2).move_to([0.0, -3.0, 0.0])
        self.add_fixed_in_frame_mobjects(final_txt)
        self.begin_ambient_camera_rotation(rate=0.18)
        tocar("acorde_harmonico.wav")
        self.play(FadeIn(final_txt), run_time=0.7)
        self.wait(3.6)
        self.stop_ambient_camera_rotation()

        # ———— Encerramento ————
        self.play(
            *[a.animate.set_value(0.0) for a in amps],
            FadeOut(titulo), FadeOut(final_txt), FadeOut(eixos),
            FadeOut(rot_x), FadeOut(rot_y), FadeOut(rot_z),
            FadeOut(et1), FadeOut(et2),
            run_time=1.2,
        )
        self.remove(*fios)
        self.remove(fase, amp1, amp2, amp3)
        self.remove_fixed_in_frame_mobjects(titulo, final_txt)
        self.remove_fixed_orientation_mobjects(et1, et2)
        self.wait(0.3)
