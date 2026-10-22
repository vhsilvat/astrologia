"""
MISTAGOGOS · protótipo "A harmonia do mundo" (Kepler, Harmonices Mundi, livro V)

Seis planetas giram em torno do Sol em órbitas keplerianas reais (elementos aproximados do JPL,
época 27/03/1996). Cada planeta é uma voz cuja frequência acompanha a velocidade angular
heliocêntrica: f = 98,12 Hz · ω / ω_mín(Saturno), como em Arthur, "The Harmony of the World",
dobrada em oitavas inteiras fixas por planeta. O áudio e a imagem usam o mesmo relógio
(fase da função `anos`), então o som é gerado já sincronizado com os quadros.

Uso: cd output && manim render -ql ../harmonicas/sinfonia.py Sinfonia
Paleta Gruvbox · EB Garamond.
"""

import wave
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Dot,
    FadeIn,
    Line,
    RoundedRectangle,
    Scene,
    Text,
    VGroup,
    ValueTracker,
    VMobject,
)

GRUV_BG = "#282828"
GRUV_FG = "#ebdbb2"
GRUV_YELLOW = "#fabd2f"
GRUV_ORANGE = "#fe8019"
GRUV_RED = "#fb4934"
GRUV_AQUA = "#8ec07c"
GRUV_BLUE = "#83a598"
GRUV_GRAY = "#a89984"
GRUV_NEUT = "#7c6f64"

FONT = "EB Garamond"
AQUI = Path(__file__).resolve().parent
WAV = AQUI / "wav" / "sinfonia_proto.wav"

JD0 = 2450169.5  # 27/03/1996 00:00 UTC
T_CENT = (JD0 - 2451545.0) / 36525.0
DUR = 45.0  # segundos de vídeo
RATE0, RATE1 = 0.03, 0.25  # anos simulados por segundo de vídeo, no início e no fim
SR = 44100
F_SATURNO = 98.12

# nome: (a, da, e, de, L, dL, varpi, dvarpi, cor, oitavas abaixo, ganho, intervalo de Kepler)
# elementos: JPL, "Keplerian Elements for Approximate Positions of the Major Planets" (1800-2050)
PLANETAS = {
    "Mercúrio": (0.38709927, 0.00000037, 0.20563593, 0.00001906, 252.25032350, 149472.67411175,
                 77.45779628, 0.16047689, GRUV_GRAY, 4, 0.16, "5:12"),
    "Vênus": (0.72333566, 0.00000390, 0.00677672, -0.00004107, 181.97909950, 58517.81538729,
              131.60246718, 0.00268329, GRUV_ORANGE, 3, 0.20, "24:25"),
    "Terra": (1.00000261, 0.00000562, 0.01671123, -0.00004392, 100.46457166, 35999.37244981,
              102.93768193, 0.32327364, GRUV_BLUE, 3, 0.24, "15:16"),
    "Marte": (1.52371034, 0.00001847, 0.09339410, 0.00007882, -4.55343205, 19140.30268499,
              -23.94362959, 0.44441088, GRUV_RED, 2, 0.28, "2:3"),
    "Júpiter": (5.20288700, -0.00011607, 0.04838624, -0.00013253, 34.39644051, 3034.74612775,
                14.72847983, 0.21252668, GRUV_YELLOW, 0, 0.40, "5:6"),
    "Saturno": (9.53667594, -0.00125060, 0.05386179, -0.00050991, 49.95424423, 1222.49362201,
                92.59887831, -0.41897216, GRUV_AQUA, 0, 0.50, "4:5"),
}


class Orbita:
    def __init__(self, a, da, e, de, L, dL, w, dw, cor, k, ganho, kepler):
        self.a = a + da * T_CENT
        self.e = e + de * T_CENT
        self.w = np.radians(w + dw * T_CENT)
        self.M0 = np.radians((L + dL * T_CENT) - (w + dw * T_CENT))
        self.n = 2 * np.pi / (self.a ** 1.5 * 365.25)  # rad/dia
        self.cor, self.k, self.ganho, self.kepler = cor, k, ganho, kepler
        q = np.sqrt(1 - self.e ** 2)
        self.om_min = self.n * q / (1 + self.e) ** 2
        self.om_max = self.n * q / (1 - self.e) ** 2

    def estado(self, anos):
        """Posição heliocêntrica (UA, plano da órbita) e velocidade angular (rad/dia)."""
        M = self.M0 + self.n * np.asarray(anos) * 365.25
        E = M.copy()
        for _ in range(8):
            E = E - (E - self.e * np.sin(E) - M) / (1 - self.e * np.cos(E))
        r = self.a * (1 - self.e * np.cos(E))
        x = self.a * (np.cos(E) - self.e)
        y = self.a * np.sqrt(1 - self.e ** 2) * np.sin(E)
        c, s = np.cos(self.w), np.sin(self.w)
        omega = self.n * np.sqrt(1 - self.e ** 2) / (1 - self.e * np.cos(E)) ** 2
        return c * x - s * y, s * x + c * y, omega, r


ORBITAS = {nome: Orbita(*p) for nome, p in PLANETAS.items()}
OM_REF = ORBITAS["Saturno"].om_min


def anos(t):
    """Anos simulados decorridos após t segundos de vídeo (taxa crescendo de forma exponencial)."""
    if RATE1 == RATE0:  # tempo linear
        return RATE0 * np.asarray(t)
    g = RATE1 / RATE0
    return RATE0 * DUR / np.log(g) * (g ** (np.asarray(t) / DUR) - 1.0)


def frequencia(o, t):
    _, _, om, _ = o.estado(anos(t))
    return F_SATURNO * om / OM_REF / 2 ** o.k


def gera_audio():
    t = np.arange(int(SR * DUR)) / SR
    mix = np.zeros_like(t)
    for nome, o in ORBITAS.items():
        fase = 2 * np.pi * np.cumsum(frequencia(o, t)) / SR
        mix += o.ganho * (np.sin(fase) + 0.30 * np.sin(2 * fase) + 0.10 * np.sin(3 * fase))
    env = np.minimum(1.0, np.minimum(t / 2.0, (DUR - t) / 2.5))
    mix *= env
    mix = mix / np.abs(mix).max() * 0.7
    WAV.parent.mkdir(exist_ok=True)
    with wave.open(str(WAV), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype("<i2").tobytes())


def texto(s, size=26, cor=GRUV_FG, **kw):
    return Text(s, font=FONT, color=cor, font_size=size, **kw)


def selo(s, cor, size=22):
    t = texto(s, size, cor)
    caixa = RoundedRectangle(corner_radius=0.08, width=t.width + 0.4, height=t.height + 0.24,
                             color=cor, stroke_width=2.0, fill_color=GRUV_BG, fill_opacity=0.9)
    t.move_to(caixa)
    return VGroup(caixa, t)


def texto_vivo(get_str, size=26, cor=GRUV_FG, borda=LEFT):
    """Text refeito só quando a string muda; ancorado pela borda indicada."""
    estado = {"s": get_str()}
    t = texto(estado["s"], size, cor)

    def upd(m):
        s = get_str()
        if s != estado["s"]:
            estado["s"] = s
            m.become(texto(s, size, cor).move_to(m.get_edge_center(borda), aligned_edge=borda))

    t.add_updater(upd)
    return t


K_VIS = 1.0
CENTRO = np.array([-3.4, -0.1, 0.0])


def tela(x, y):
    """Compressão radial sqrt(r), para que Mercúrio e Saturno caibam no mesmo quadro."""
    r = np.hypot(x, y)
    f = K_VIS / np.sqrt(r)
    return CENTRO + np.array([x * f, y * f, 0.0])


class Sinfonia(Scene):
    # ganchos para variantes (ver sinfonia_instrumentos.py)
    X_PAINEL = (0.55, 2.75, 5.15, 5.55)  # nome, início da trilha, fim da trilha, Hz
    ENTRADAS = {}  # planeta: segundo de vídeo em que a voz entra (padrão: 0)

    def prepara_audio(self):
        gera_audio()
        return WAV

    def rotulo_det(self, nome, o):
        return f"mín:máx {o.om_min / o.om_max:.2f} · Kepler {o.kepler}"

    def freq_painel(self, nome, o, tt):
        return frequencia(o, tt)

    def construct(self):
        self.camera.background_color = GRUV_BG
        self.add_sound(str(self.prepara_audio()))

        t = ValueTracker(0.0)
        t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(t)

        titulo = texto("a harmonia do mundo", 44, GRUV_YELLOW).to_edge(UP, buff=0.3)
        sub = texto("cada planeta canta a sua velocidade angular", 26, GRUV_GRAY).next_to(titulo, DOWN, buff=0.1)
        self.play(FadeIn(titulo), FadeIn(sub), run_time=1.0)

        # sol e órbitas
        sol = Dot(CENTRO, radius=0.13, color=GRUV_YELLOW)
        halo = Dot(CENTRO, radius=0.26, color=GRUV_YELLOW).set_opacity(0.18)
        trilhos, corpos, linhas = [], [], []
        fases = np.linspace(0, 2 * np.pi, 361)
        for nome, o in ORBITAS.items():
            M = fases
            E = M.copy()
            for _ in range(8):
                E = E - (E - o.e * np.sin(E) - M) / (1 - o.e * np.cos(E))
            x = o.a * (np.cos(E) - o.e)
            y = o.a * np.sqrt(1 - o.e ** 2) * np.sin(E)
            c, s = np.cos(o.w), np.sin(o.w)
            pts = [tela(c * xi - s * yi, s * xi + c * yi) for xi, yi in zip(x, y)]
            trilho = VMobject(stroke_color=o.cor, stroke_width=1.6, stroke_opacity=0.55)
            trilho.set_points_as_corners(pts)
            trilhos.append(trilho)

            corpo = Dot(CENTRO, radius=0.075 + 0.01 * (nome in ("Júpiter", "Saturno")), color=o.cor)

            def pos(m, o=o, nome=nome):
                x_, y_, _, _ = o.estado(anos(t.get_value()))
                m.move_to(tela(float(x_), float(y_)))
                m.set_opacity(1.0 if t.get_value() >= self.ENTRADAS.get(nome, 0.0) else 0.3)

            corpo.add_updater(pos)
            pos(corpo)
            corpos.append(corpo)

        self.play(FadeIn(sol), FadeIn(halo), *[FadeIn(tr) for tr in trilhos], run_time=1.5)
        self.add(*corpos)

        # painel das vozes
        painel, hzs = [], []
        ordem = list(ORBITAS.items())  # Mercúrio (agudo) em cima, Saturno (grave) embaixo
        y0, dy = 2.35, 0.82
        x_nome, x_ini, x_fim, x_hz = self.X_PAINEL
        for i, (nome, o) in enumerate(ordem):
            y = y0 - i * dy
            rot = texto(nome, 28, o.cor).move_to([x_nome, y + 0.08, 0], aligned_edge=LEFT)
            razao = o.om_min / o.om_max
            det = texto(self.rotulo_det(nome, o), 17, GRUV_GRAY).move_to(
                [x_nome, y - 0.22, 0], aligned_edge=LEFT)
            trilha = Line([x_ini, y, 0], [x_fim, y, 0], color=GRUV_NEUT, stroke_width=3)
            tiq = [Line([xx, y - 0.09, 0], [xx, y + 0.09, 0], color=GRUV_NEUT, stroke_width=3)
                   for xx in (x_ini, x_fim)]
            marca = Dot([x_ini, y, 0], radius=0.09, color=o.cor)

            def mexe(m, o=o, y=y):
                _, _, om, _ = o.estado(anos(t.get_value()))
                fr = (float(om) - o.om_min) / (o.om_max - o.om_min)
                m.move_to([x_ini + (x_fim - x_ini) * min(max(fr, 0.0), 1.0), y, 0])

            marca.add_updater(mexe)
            mexe(marca)

            def get_hz(o=o, nome=nome):
                if t.get_value() < self.ENTRADAS.get(nome, 0.0):
                    return "— Hz"
                return f"{float(self.freq_painel(nome, o, t.get_value())):.0f} Hz"

            hz = texto_vivo(get_hz, 26, GRUV_FG)
            hz.move_to([x_hz, y, 0], aligned_edge=LEFT)
            painel += [rot, det, trilha, *tiq, marca]
            hzs.append(hz)

        painel_g = VGroup(*painel)
        self.play(FadeIn(painel_g), run_time=1.2)
        self.add(*hzs)  # textos vivos entram sem FadeIn: o updater troca os pontos do Text

        def get_data():
            d = datetime(1996, 3, 27) + timedelta(days=float(anos(t.get_value())) * 365.25)
            return d.strftime("%d/%m/%Y")

        data = texto_vivo(get_data, 30, GRUV_FG, borda=LEFT)
        data.move_to([-6.6, -3.65, 0], aligned_edge=LEFT)
        tag = selo("INTERPRETÁVEL (convenção de Kepler)", GRUV_ORANGE).to_corner(RIGHT + DOWN, buff=0.35)
        self.add(data)
        self.play(FadeIn(tag), run_time=0.8)

        self.wait(DUR - t.get_value() - 0.05)
        t.clear_updaters()
