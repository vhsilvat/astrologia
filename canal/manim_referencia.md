# Manim CE — Referência Prática Destilada (MISTAGOGOS, v0.21.0)

Fonte: docs.manim.community `/en/stable` — que HOJE É a v0.21.0 (confirmado nas páginas de referência) — mais introspecção do pacote instalado. Por serem idênticas, não há divergências estável↔0.21.0; a tag **[0.21]** marca apenas notas específicas da versão/OpenGL do nosso pipeline.

---

## 1. CLI e flags de render
```bash
manim render -ql arquivo.py Cena           # 854x480 15fps (rascunho)
manim render -qh arquivo.py Cena           # 1920x1080 60fps (final)
# -qm 720p30 | -qp 1440p60 | -qk 2160p60
manim render -qh -a arquivo.py             # todas as cenas do arquivo
manim render -qn 5,12 arquivo.py Cena      # só animações 5..12
manim render --save_sections -ql arquivo.py Cena
manim render -qh --disable_caching --flush_cache arquivo.py Cena
manim render -s --format png -qh arquivo.py Cena    # último frame em PNG
```
- Flags-chave: `--format png|gif|mp4|webm|mov` · `-t` (alpha) · `--fps N` · `-r W,H` · `--renderer cairo|opengl` · `--seed N` · `--dry_run` · `-o nome` · `-0 zero_pad` · `--progress_bar [display|leave|none]` · `--tex_template f.tex` · `--no_latex_cleanup` (debug LaTeX mantém .log/.aux).
- Performance [0.21]: `--max-inflight-encoders 4` sobrepõe codificação ao render (default 1; 4 é bom em hardware típico); `--encoder-queue-size` só afeta codificação paralela.
- Saída: `media/videos/<arquivo>/<qualidade>/<Cena>.mp4` (+ `<Cena>.wav` com add_sound); parciais reusáveis em `partial_movie_files/`; SVGs LaTeX em `media/texts/`; PNGs em `media/images/`.

## 2. Scene e construct
```python
class Cena(Scene):
    def construct(self):
        d = Dot()
        self.add(d)                                  # entra sem animação (t não avança)
        self.play(d.animate.shift(RIGHT), run_time=2, rate_func=smooth)
        self.wait(1)                                 # congela o frame, t += 1
        self.remove(d)                               # sai sem animação
```
- `play(*anims, run_time=..., rate_func=..., lag_ratio=...)`; defaults de Animation: `run_time=1.0`, `rate_func=smooth`, `lag_ratio=0.0`, `suspend_mobject_updating=True` (updaters do próprio mob são suspensos durante sua animação).
- `lag_ratio`: 0 = todos em paralelo; 1 = estritamente sequencial; AnimationGroup=0, LaggedStart=0.05, Succession=1.
- `wait(duration=1.0, stop_condition=None, frozen_frame=None)` — stop_condition (função bool) encerra cedo.
- `play` também aceita `subcaption='txt', subcaption_duration=2, subcaption_offset=0` (legendas embutidas).

## 3. Mobjects essenciais, posicionamento e styling
```python
g = VGroup(
    Line(ORIGIN, RIGHT * 3, path_arc=0),             # Line(start, end, buff=0)
    Circle(radius=1),                                # default radius=1.0
    Arc(radius=1, start_angle=0, angle=PI / 2, arc_center=ORIGIN),
    Annulus(inner_radius=1, outer_radius=2, fill_opacity=1, stroke_width=0),
    Rectangle(width=4, height=2), Square(side_length=2),
    Polygon([2, -1, 0], [2, 1, 0], [-2, 1, 0], [-2, -1, 0]),   # z=0 SEMPRE (Cairo)
    Dot(ORIGIN, radius=0.08),
    Brace(txt, direction=DOWN, buff=0.2),
    Arrow(LEFT, RIGHT, buff=0.25), DoubleArrow(LEFT * 2, RIGHT * 2),
)
g.arrange(DOWN, buff=0.3).next_to(ORIGIN, UP)        # encadeável
```
- Posicionamento: `move_to(ponto|mob, aligned_edge=ORIGIN)` · `next_to(mob|ponto, direction=RIGHT, buff=0.25)` · `to_corner(UL)` · `to_edge(RIGHT, buff=0.5)` · `align_to(mob|ponto, direction)` · `arrange(direction=RIGHT, buff=0.25, center=True)` · `rotate(angle, axis=OUT, about_point=None, about_edge=None)`.
- Styling (VMobject): `set_stroke(color=None, width=None, opacity=None, background=False)` · `set_fill(color=None, opacity=None)` · `set_opacity(v)` · `set_color(c)` (hex `'#ebdbb2'` ou constantes).
- Ordem de desenho: ordem de `self.add(...)` + `set_z_index(v, family=True)`; fundo: `config.background_color` (ex. `'#282828'`).
- `Brace.get_text('y')` retorna **Tex** (LaTeX) já posicionado — para EB Garamond prefira `Text(...)` manual com `next_to(br, direction, buff)`.
- `VGroup` agrupa VMobjects; `Group` para mistos (ImageMobject, superfícies 3D).

## 4. Text vs Tex vs MathTex
```python
t = Text('A Forja de Pitágoras', font='EB Garamond', font_size=48,
         t2c={'Pitágoras': '#fabd2f'}, t2w={'Pitágoras': BOLD})
m = MathTex(r'\frac{12}{6}', '=', '2:1', tex_to_color_map={'2:1': YELLOW})
fatias = MathTex(r'{{12}} {{+}} {{6}}')     # duplas chaves isolam submobjects
```
- `Text(text, font='', font_size=48, t2c, t2f, t2s, t2w, t2g, gradient=None, line_spacing=-1, slant, weight, disable_ligatures=False)` — mapas `t2*` casam substrings exatas do texto.
- `Tex(*tex_strings, tex_environment='center')` · `MathTex(*tex_strings, substrings_to_isolate=None, tex_to_color_map=None, tex_environment='align*')`; fatias por índice: `m[0]`, `m[2]`.
- **Nenhuma das três tem parâmetro de baseline** — alinhe com `next_to(m, mob, aligned_edge=DOWN)`, `align_to` ou deslocamentos manuais.
- LaTeX: raw strings obrigatórias `r'...'`; erros de compilação mostram o log completo no terminal; template custom via `--tex_template`.

## 5. Catálogo de animações
```python
self.play(FadeIn(d, shift=UP * 0.3, scale=1.1), FadeOut(t))
self.play(Transform(sq, circ))              # sq assume a forma de circ (original persiste, distorcido)
self.play(ReplacementTransform(sq, circ))   # sq É REMOVIDO; circ entra no lugar — clear_updaters antes!
self.play(TransformFromCopy(orig, copia))   # orig intacta
self.play(LaggedStart(*[FadeIn(ch, shift=UP) for ch in letras], lag_ratio=0.15))
self.play(AnimationGroup(FadeIn(a), FadeIn(b), lag_ratio=0))
self.play(Succession(anim_a, anim_b))       # fila rígida
self.play(Circumscribe(m, color=RED, fade_in=True, buff=0.15), Indicate(d))
self.play(Flash(ORIGIN), FocusOn(d), GrowFromEdge(g, DOWN))
self.play(DrawBorderThenFill(txt), Wiggle(d), ApplyWave(line), Rotate(m, angle=PI))
mob.generate_target(); mob.target.shift(RIGHT); self.play(MoveToTarget(mob))
mob.save(); mob.shift(UP); self.play(Restore(mob))
self.play(FadeTransform(a, b))              # a esmaece virando b
```
- Introducers: `Write(vmobject, rate_func=linear)` · `Create(mobject, lag_ratio=1.0)` · `Uncreate(m)` (remover=True). **Segfault Write/Create com OpenGL em software → usar FadeIn** (experiência nossa; NÃO consta na doc oficial).
- `Write` já é `rate_func=linear` por default; `DrawBorderThenFill` usa `double_smooth` (run_time=2).
- `TransformMatchingShapes/Tex(m, alvo, transform_mismatches=False, fade_transform_mismatches=False, key_map=None)` — preserva partes idênticas; ideal para equações.
- `Circumscribe(shape=Rectangle|Circle, time_width=0.3, run_time=1, stroke_width=4)` · `Indicate(scale_factor=1.2, rate_func=there_and_back)`.

## 6. rate_functions
```python
from manim import rate_functions as rf
self.play(martelo.animate.shift(DOWN * 3), rate_func=rf.rush_into)   # acelera até o impacto
self.play(fase.animate.set_value(10), rate_func=linear)              # updaters / sync de áudio
self.play(FadeIn(x), rate_func=squish_rate_func(smooth, 0.2, 0.8))   # janela do run_time
```
- Top-level (`from manim import smooth`): `smooth` (default geral), `linear`, `there_and_back`, `there_and_back_with_pause`, `rush_from`, `rush_into`, `lingering`, `exponential_decay`, `sigmoid`, `slow_into`, `running_start`, `not_quite_there`, `wiggle`, `zero`, `sqrt`, `squish_rate_func`.
- Só via módulo `rf.`: famílias `ease_in_*`, `ease_out_*`, `ease_in_out_*` (quad, cubic, quart, quint, sine, back, bounce, circ, elastic, expo) + `smoothstep`, `smootherstep`, `double_smooth` — lista completa: `dir(rf)`.
- `squish_rate_func(f, a=0.4, b=0.6)`: comprime f na janela [a,b] do run_time (pausa/detone dentro de um play).
- Recomendação: `smooth` para quase tudo; `rush_into`+`rush_from` para golpes; `there_and_back` para indicações; **`linear` obrigatório em updaters e sincronização com áudio**.

## 7. Updaters contínuos
```python
fase, amp, speed = ValueTracker(0), ValueTracker(0), ValueTracker(4)
fase.add_updater(lambda m, dt: m.increment_value(speed.get_value() * dt))
corda = always_redraw(lambda: ParametricFunction(
    lambda u: np.array([X0 + u * SPAN,
                        Y_STR + amp.get_value() * np.sin(PI * u) * np.cos(fase.get_value()), 0]),
    t_range=(0, 1, 0.004)))
self.add(corda)                      # SEMPRE self.add: always_redraw não entra na cena sozinho [pitfall b, doc oficial]
self.play(amp.animate.set_value(0.35))
fase.clear_updaters(); self.remove(fase, corda)   # limpeza obrigatória no fim
```
- `ValueTracker(value=0)`: `get_value()`, `set_value(v)`, `increment_value(dv)`; animável: `self.play(tracker.animate.set_value(1))`.
- `always_redraw(fn)`: mob com updater `mob.become(fn())` por frame — **self.add obrigatório**; qualquer estado mutado fora de `fn` é descartado a cada frame.
- `mob.add_updater(fn, index=None, call_updater=False)` — `fn(mob)` ou `fn(mob, dt)` (dt chega a cada frame, roda em play e wait); `clear_updaters(recursive=True)`.

- `f_always(method, *arg_generators)` (top-level): atualiza `method` a cada frame com args gerados na hora — ex.: `pino.add_updater(f_always(pino.move_to, lambda: [x_de(k.get_value()), Y_STR, 0]))` (sem dt; use add_updater(fn, dt) quando precisar do delta).
- Animar mob que tem updaters: **`clear_updaters()` antes** [pitfall f] — a Animation suspende o updating do próprio alvo (`suspend_mobject_updating=True`), mas trackers e updaters de terceiros continuam e corrompem a interpolação; limpe também o target em ReplacementTransform. No fim da cena: `clear_updaters()` + `self.remove(...)`.

## 8. Câmera

```python
class Zoom(MovingCameraScene):
    def construct(self):
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.scale(0.5).move_to(alvo))   # zoom+pan
        self.play(Restore(self.camera.frame))
        # atalho: self.camera.auto_zoom(mobs, margin=0., animate=True)

class D3(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.move_camera(phi=30 * DEGREES, run_time=2)
        self.stop_ambient_camera_rotation()
```
- `MovingCameraScene`: `self.camera.frame` é animável (`.scale/.move_to/.set_width`); atalho `auto_zoom(mobjects, margin=0, only_mobjects_in_frame=False, animate=True)`.
- `ThreeDScene`: `set_camera_orientation(phi, theta, gamma, zoom, focal_distance, frame_center)` · `move_camera(..., added_anims=[...])` · `begin_ambient_camera_rotation(rate=0.02, about='theta')`; HUD: `add_fixed_in_frame_mobjects(m)`; rótulo com orientação fixa: `add_fixed_orientation_mobjects(m)`.
- **[0.21] OpenGL**: `OpenGLCamera` vive em `manim/renderer/opengl_renderer.py` e **NÃO tem `set_zoom`** [pitfall c confirmado na 0.21.0] → `zoom`/`frame_center` em `set_camera_orientation` só valem no Cairo (`ThreeDCamera` tem set_zoom/get_zoom). Em GL ajuste com `set_euler_angles/ set_phi/set_theta/set_gamma` e leia os ângulos de volta.

## 9. add_sound

```python
SONS = Path(__file__).resolve().parent / 'sons'
self.add_sound(str(SONS / 'tom_220.wav'))                  # dispara em t = self.time
self.play(golpe)                                           # som coincide com o início do play
self.add_sound(str(SONS / 'tom.wav'), time_offset=-0.05, gain=3)  # antecipa 50 ms
```
- Assinatura: `add_sound(sound_file: str, time_offset: float = 0, gain: float | None = None)`; fonte oficial: `time = self.time + time_offset` → **posição da timeline no momento da chamada**; não há acoplamento automático ao play seguinte — chame imediatamente ANTES do play alvo.
- `time_offset`: antecipa/atrasa na timeline (não recorta o início do próprio arquivo — para isso, trimme o WAV); `gain` em dB (pydub `apply_gain`); não-WAV é convertido a `pcm_s16le` via ffmpeg em temporário → entregue WAV nativo.
- Caminho: resolução interna relativa (cwd/media) → **sempre caminho absoluto via `Path(__file__)`** [pitfall e].
- Saída: `<Cena>.mp4` com áudio embutido + `<Cena>.wav` copiado na pasta de qualidade; `-s`, `--dry_run` e skip_animations não gravam som.

## 10. Vídeo longo: cenas separadas vs seções

```python
class ParteA(Scene): ...
class ParteB(Scene): ...
# manim render -qh -a arquivo.py  -> ParteA.mp4, ParteB.mp4 independentes
```

```bash
printf "file 'ParteA.mp4'\nfile 'ParteB.mp4'\n" > l.txt
ffmpeg -f concat -safe 0 -i l.txt -c copy final.mp4   # exige mesmo codec/fps/resolução
```
- Nativo [0.21]: cena única + `self.next_section(name='harpa', section_type='default.normal')` entre blocos + CLI `--save_sections` → um mp4 por seção em `media/videos/<arquivo>/<q>/sections/` + `sections.json` com timestamps (cortes de Shorts na edição). `DefaultSectionType` na 0.21.0 só expõe `default.normal`.
- Regra: seções p/ pós-produção (timeline e áudio continuam contínuos na cena única); classes separadas p/ blocos renderizados/reusados independentemente (o concat `-c copy` exige mesma `-q`, fps e resolução).

## 11. FAQ / pitfalls do pipeline
- **Cairo vs OpenGL**: Cairo (default) estável para 2D; GL (`--renderer opengl`) para 3D interativo. Em GL por software (xvfb), `Write`/`Create` segfaultam → `FadeIn` [pitfall a, experiência nossa; não consta na doc].
- **Caching**: parciais em `partial_movie_files/` reusados por hash; cenas com ValueTracker/updaters mudam o hash a cada execução → `--disable_caching` em cenas dinâmicas; `--flush_cache` p/ limpar.
- **Fontes**: `font='EB Garamond'` depende do Pango — verifique `fc-list | grep -i garamond`; sem a font, warning (`warn_missing_font=True`) e fallback silencioso.
- **LaTeX**: raw strings `r'...'` sempre; erros comuns: pacote faltando no texlive, `\\` no fim de `align*`, `%`/chaves não escapadas; debug com `--no_latex_cleanup` (mantém .log/.aux) e `--tex_template`.
- **Mapa dos nossos pitfalls**: (a) nosso; (b) CONFIRMADO — o exemplo oficial de always_redraw usa `self.add(...)`; (c) CONFIRMADO na 0.21.0; (d) geometria 2D opera no plano z=0; (e) caminho relativo frágil → absoluto; (f) regra nossa (não consta na doc).
- Frame: 14.22×8 unidades, origem no centro; fundo `config.background_color` (ex.: `'#282828'`); transparência com `-t`.

Refs: docs.manim.community/en/stable/reference · /en/stable/faq/index.html · /en/stable/guides/configuration.html
