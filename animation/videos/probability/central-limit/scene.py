from math import lgamma

from manim import *
from lnx import *

# simulacion | probabilidad | intermedio
# Tablero de Galton y Teorema Central del Limite.
#
# La idea que casi nadie cuenta bien: la campana del tablero de Galton NO sale
# porque cada clavo sea 50/50. Sale porque estamos SUMANDO muchas decisiones
# independientes. Cambia el dado (uniforme, exponencial muy sesgada, bimodal),
# promedia n = 30 y la campana vuelve a aparecer, identica. Eso es el TCL:
#   (Xbar - mu) / (sigma / sqrt(n))  ->  N(0, 1).
#
# El frame real es 9 x 16 unidades (x en [-4.5, 4.5], y en [-8, 8]).
# Zona segura: |y| <= 5.6 y |x| <= 3.8.
#
# Todas las simulaciones se precalculan con numpy y semilla fija: en pantalla
# solo se animan geometrias ya resueltas, nunca updaters pesados.

SEED = 20240808
SAFE_W = 7.2

# --- tablero de Galton -------------------------------------------------------
ROWS = 11                 # filas de clavos = numero de decisiones por bolita
DX = 0.42                 # separacion horizontal entre clavos
DY = 0.36                 # separacion vertical entre filas
TOP_Y = 3.9               # y de la primera fila de clavos
DROP_Y = 4.9              # y de salida de las bolitas
BASE_Y = -5.0             # linea base del histograma
MAX_H = 4.6               # altura de la barra mas alta
BALL_R = 0.075

N_HOOK = 34               # bolitas del gancho
N_AVALANCHE = 236         # bolitas de la avalancha
N_TOTAL = N_HOOK + 1 + N_AVALANCHE   # +1 = la bolita en camara lenta


def fit(m):
    """Evita que un mobject se salga de la zona segura horizontal."""
    if m.width > SAFE_W:
        m.scale_to_fit_width(SAFE_W)
    return m


def bars_from_counts(counts, base_y, x_center, total_w, max_h, color,
                     max_count=None, opacity=0.92):
    """Histograma como VGroup de rectangulos, listo para Transform.

    Se usa un `max_count` fijo para que las barras crezcan de forma coherente
    entre pasadas en vez de re-escalarse en cada actualizacion.
    """
    n = len(counts)
    bw = total_w / n
    mc = max_count if max_count else max(max(counts), 1)
    group = VGroup()
    for i, c in enumerate(counts):
        h = max(c / mc * max_h, 1e-3)
        rect = Rectangle(
            width=bw * 0.86, height=h,
            stroke_width=0, fill_color=color, fill_opacity=opacity,
        )
        rect.move_to([x_center - total_w / 2 + bw * (i + 0.5), base_y + h / 2, 0])
        group.add(rect)
    return group


class CentralLimit(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        rng = np.random.default_rng(SEED)

        # ------------------------------------------------ precalculo del tablero
        # Cada bolita es una fila de +-1: su bin final es el numero de "derechas".
        steps = rng.integers(0, 2, size=(N_TOTAL, ROWS)) * 2 - 1
        bins = ((steps.sum(axis=1) + ROWS) // 2).astype(int)   # 0 .. ROWS

        counts_final = np.bincount(bins, minlength=ROWS + 1)
        MAXC = int(counts_final.max())
        UNIT = MAX_H / MAXC
        TOTAL_W = (ROWS + 1) * DX

        def bin_x(k):
            return (k - ROWS / 2) * DX

        # Trayectoria de la bolita i, y altura a la que aterriza (encima de la
        # pila que ya hay en su bin en ese momento).
        running = np.zeros(ROWS + 1, dtype=int)
        paths, lands = [], []
        for i in range(N_TOTAL):
            cum = np.concatenate(([0], np.cumsum(steps[i])))
            pts = [np.array([0.0, DROP_Y, 0.0])]
            for k in range(ROWS):
                pts.append(np.array([cum[k] * DX / 2, TOP_Y - k * DY, 0.0]))
            k_bin = bins[i]
            running[k_bin] += 1
            y_land = BASE_Y + running[k_bin] * UNIT - 0.04
            pts.append(np.array([bin_x(k_bin), TOP_Y - (ROWS - 1) * DY - 0.35, 0.0]))
            pts.append(np.array([bin_x(k_bin), y_land, 0.0]))
            paths.append(pts)
            lands.append(running.copy())

        # ------------------------------------------------------- clavos y base
        pegs = VGroup()
        for r in range(ROWS):
            for j in range(r + 1):
                pegs.add(Dot(
                    [(j - r / 2) * DX, TOP_Y - r * DY, 0.0],
                    radius=0.035, color=GREY_B,
                ))
        pegs.set_opacity(0.75)

        floor = Line(
            [-TOTAL_W / 2, BASE_Y, 0], [TOTAL_W / 2, BASE_Y, 0],
            stroke_width=3, color=GREY_B,
        ).set_opacity(0.6)

        bars = bars_from_counts(
            np.zeros(ROWS + 1), BASE_Y, 0, TOTAL_W, MAX_H,
            ACCENT_CYAN, max_count=MAXC,
        )
        self.add(pegs, floor, bars)

        def drop(indices, run_time, lag_ratio, color=ACCENT_MAGENTA):
            """Lanza un lote de bolitas y hace crecer el histograma a la vez.

            Un solo play() por lote: nunca una animacion por bolita.
            """
            anims = []
            for i in indices:
                dot = Dot(paths[i][0], radius=BALL_R, color=color)
                path = VMobject().set_points_as_corners(paths[i])
                anims.append(Succession(
                    MoveAlongPath(dot, path, run_time=1.1,
                                  rate_func=rate_functions.ease_in_quad),
                    FadeOut(dot, run_time=0.12),
                ))
            target = bars_from_counts(
                lands[indices[-1]], BASE_Y, 0, TOTAL_W, MAX_H,
                ACCENT_CYAN, max_count=MAXC,
            )
            self.play(
                LaggedStart(*anims, lag_ratio=lag_ratio),
                Transform(bars, target, rate_func=linear),
                run_time=run_time,
            )

        # ------------------------------------------------------- hook 0.0-6.5 s
        # Sin una sola palabra: solo el fenomeno. Caen bolitas al azar y la
        # campana empieza a dibujarse sola.
        drop(list(range(N_HOOK)), run_time=5.6, lag_ratio=0.055)

        # ------------------------------------------- beat 1: el mecanismo 6.5-22 s
        titulo = Tex(r"Cada clavo: izquierda o derecha", font_size=38,
                     color=WHITE)
        fit(titulo)
        titulo.move_to(UP * 5.35)
        self.play(FadeIn(titulo, shift=DOWN * 0.25), run_time=0.6)

        moneda = MathTex(r"P(\text{izq}) = P(\text{der}) = \tfrac{1}{2}",
                         font_size=34, color=ACCENT_YELLOW)
        fit(moneda)
        moneda.move_to(UP * 4.75)
        self.play(Write(moneda), run_time=0.7)

        # Una sola bolita en camara lenta, marcando su camino en amarillo.
        i_slow = N_HOOK
        slow_pts = paths[i_slow]
        bola = Dot(slow_pts[0], radius=0.13, color=ACCENT_YELLOW)
        bola.set_z_index(6)
        self.play(FadeIn(bola, scale=0.4), run_time=0.4)

        traza = VGroup().set_z_index(4)
        signos = VGroup()
        for k in range(ROWS):
            seg = Line(slow_pts[k], slow_pts[k + 1],
                       stroke_width=5, color=ACCENT_YELLOW)
            traza.add(seg)
            # Solo se etiquetan las primeras decisiones: despues ya se entendio.
            anims = [Create(seg), bola.animate.move_to(slow_pts[k + 1])]
            if k < 4 and k > 0:
                s = "+1" if steps[i_slow][k - 1] > 0 else "-1"
                lab = MathTex(s, font_size=28, color=ACCENT_YELLOW)
                lab.next_to(slow_pts[k + 1], RIGHT if s == "+1" else LEFT, buff=0.12)
                signos.add(lab)
                anims.append(FadeIn(lab, scale=0.6))
            self.play(*anims, run_time=0.42 if k < 4 else 0.16)

        # Tramo final: sale del ultimo clavo y cae a su casilla. Se anade a la
        # traza para que el fundido posterior se la lleve entera.
        cola = VMobject().set_points_as_corners(slow_pts[ROWS:])
        cola_traza = VMobject().set_points_as_corners(slow_pts[ROWS:])
        cola_traza.set_stroke(color=ACCENT_YELLOW, width=5).set_z_index(4)
        traza.add(cola_traza)
        self.play(MoveAlongPath(bola, cola), Create(cola_traza), run_time=0.6)
        self.play(FadeOut(bola), FadeOut(signos), run_time=0.4)

        suma = MathTex(
            r"X = \pm 1 \pm 1 \pm 1 \cdots \pm 1",
            font_size=36, color=ACCENT_YELLOW,
        )
        fit(suma)
        suma.move_to(UP * 4.75)
        self.play(ReplacementTransform(moneda, suma), run_time=0.8)

        idea = Tex(r"La posición final es una \emph{suma}", font_size=36,
                   color=WHITE)
        fit(idea)
        idea.move_to(UP * 5.35)
        self.play(ReplacementTransform(titulo, idea), run_time=0.7)
        self.wait(0.8)

        # ------------------------------------------ beat 2: la avalancha 22-40 s
        self.play(FadeOut(suma), FadeOut(traza), run_time=0.4)
        titulo2 = Tex(r"Cientos de bolitas", font_size=40, color=ACCENT_MAGENTA)
        fit(titulo2)
        titulo2.move_to(UP * 5.35)
        self.play(ReplacementTransform(idea, titulo2), run_time=0.6)

        start = N_HOOK + 1
        lote = 59
        for w, (rt, lag) in enumerate([(3.2, 0.030), (2.8, 0.022),
                                       (2.4, 0.018), (2.2, 0.014)]):
            idx = list(range(start + w * lote, start + (w + 1) * lote))
            drop(idx, run_time=rt, lag_ratio=lag)

        # La curva teorica es la binomial C(ROWS,k)/2^ROWS interpolada de forma
        # continua con lgamma (una normal pura sobreestima el pico en ~4%).
        # Altura esperada de la barra k = N_TOTAL * pmf(k) * UNIT.
        def envolvente(t):
            ln_p = (lgamma(ROWS + 1) - lgamma(t + 1) - lgamma(ROWS - t + 1)
                    - ROWS * np.log(2.0))
            return np.array([bin_x(t), BASE_Y + N_TOTAL * np.exp(ln_p) * UNIT, 0.0])

        curva = ParametricFunction(envolvente, t_range=[-0.7, ROWS + 0.7, 0.05])
        curva.set_stroke(color=ACCENT_YELLOW, width=6)
        curva.set_z_index(8)
        self.play(Create(curva), run_time=1.6)

        campana = Tex(r"la campana de Gauss", font_size=40, color=ACCENT_YELLOW)
        fit(campana)
        campana.move_to(UP * 5.35)
        self.play(ReplacementTransform(titulo2, campana), run_time=0.7)
        self.wait(1.2)

        # ------------------------------------- beat 3: el golpe real 40-70 s
        # La pregunta incomoda: ¿y si el paso no fuera 50/50?
        self.play(
            FadeOut(VGroup(pegs, floor, bars, curva, campana)),
            run_time=0.8,
        )

        pregunta = Tex(r"¿Y si el paso \emph{no} fuera 50/50?",
                       font_size=44, color=WHITE)
        fit(pregunta)
        pregunta.move_to(UP * 1.0)
        self.play(Write(pregunta), run_time=0.9)
        self.wait(0.9)
        self.play(FadeOut(pregunta, shift=UP * 0.4), run_time=0.5)

        # --- simulaciones de las tres fuentes (todas con la misma semilla) ---
        N_SRC, N_MEAN, N_SAMP = 6000, 4000, 30

        uni = rng.random(N_SRC) * 2.0
        uni_m = rng.random((N_MEAN, N_SAMP)).mean(axis=1) * 2.0

        exp_ = rng.exponential(1.0, N_SRC)
        exp_m = rng.exponential(1.0, (N_MEAN, N_SAMP)).mean(axis=1)

        def bimodal(shape):
            pick = rng.random(shape) < 0.5
            return np.where(pick, rng.normal(-1.0, 0.28, shape),
                            rng.normal(1.0, 0.28, shape))

        bim = bimodal(N_SRC)
        bim_m = bimodal((N_MEAN, N_SAMP)).mean(axis=1)

        def hist(data, nb=26, lo=None, hi=None):
            lo = np.percentile(data, 0.3) if lo is None else lo
            hi = np.percentile(data, 99.7) if hi is None else hi
            c, _ = np.histogram(np.clip(data, lo, hi), bins=nb, range=(lo, hi))
            return c

        def hist_medias(data, nb=26):
            # Rango simetrico mu +- 3.8 sigma: asi las tres campanas de promedios
            # quedan centradas en el panel y son comparables entre si.
            m, s = data.mean(), data.std()
            return hist(data, nb, m - 3.8 * s, m + 3.8 * s)

        casos = [
            ("Uniforme", hist(uni), hist_medias(uni_m), ACCENT_CYAN),
            ("Muy sesgada", hist(exp_), hist_medias(exp_m), ACCENT_MAGENTA),
            ("Bimodal", hist(bim), hist_medias(bim_m), ACCENT_PURPLE),
        ]

        SRC_BASE, SRC_H = 1.6, 1.8
        MEAN_BASE, MEAN_H = -3.9, 2.1
        PANEL_W = 5.4

        cab = Tex(r"Cambiemos la distribución de origen", font_size=36,
                  color=WHITE)
        fit(cab)
        cab.move_to(UP * 5.35)
        self.play(FadeIn(cab, shift=DOWN * 0.2), run_time=0.5)

        flecha = Arrow(
            [0, SRC_BASE - 0.35, 0], [0, MEAN_BASE + 0.05, 0],
            buff=0.0, stroke_width=6, color=ACCENT_YELLOW,
            max_tip_length_to_length_ratio=0.12,
        )
        promedio = MathTex(r"\text{promedio de } n = 30", font_size=32,
                           color=ACCENT_YELLOW)
        promedio.next_to(flecha, RIGHT, buff=0.18)
        fit(VGroup(flecha, promedio))

        miniaturas = VGroup()
        nombre_ant = src_ant = mean_ant = None

        for idx, (nombre, c_src, c_mean, color) in enumerate(casos):
            etiqueta = Tex(nombre, font_size=38, color=color)
            etiqueta.move_to([0, SRC_BASE + SRC_H + 0.55, 0])
            src = bars_from_counts(c_src, SRC_BASE, 0, PANEL_W, SRC_H, color)
            mean_bars = bars_from_counts(
                c_mean, MEAN_BASE, 0, PANEL_W, MEAN_H, ACCENT_YELLOW)

            if idx == 0:
                self.play(FadeIn(etiqueta, shift=DOWN * 0.2),
                          LaggedStart(*[GrowFromEdge(b, DOWN) for b in src],
                                      lag_ratio=0.02),
                          run_time=1.3)
                self.play(GrowArrow(flecha), FadeIn(promedio), run_time=0.6)
                self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in mean_bars],
                                      lag_ratio=0.02), run_time=1.3)
            else:
                # Las siguientes fuentes se transforman sobre las anteriores:
                # el ojo compara formas en el mismo sitio.
                self.play(
                    ReplacementTransform(nombre_ant, etiqueta),
                    ReplacementTransform(src_ant, src),
                    run_time=0.9,
                )
                self.play(ReplacementTransform(mean_ant, mean_bars), run_time=1.0)

            nombre_ant, src_ant, mean_ant = etiqueta, src, mean_bars

            mini = mean_bars.copy().scale(0.28)
            mini.set_fill(opacity=0.95)
            miniaturas.add(mini)
            self.wait(0.5)

        siempre = Tex(r"siempre la \emph{misma} campana", font_size=38,
                      color=ACCENT_YELLOW)
        fit(siempre)
        siempre.move_to(DOWN * 5.35)
        self.play(FadeIn(siempre, shift=UP * 0.3), run_time=0.6)
        self.wait(1.4)

        # ------------------------------------------------------- cierre 70-85 s
        self.play(
            FadeOut(VGroup(cab, nombre_ant, src_ant, flecha, promedio, siempre)),
            run_time=0.6,
        )

        miniaturas.arrange(RIGHT, buff=0.45, aligned_edge=DOWN)
        miniaturas.move_to(UP * 2.6)
        fit(miniaturas)
        self.play(ReplacementTransform(mean_ant, miniaturas), run_time=1.1)

        tcl = Tex(
            r"La media de muchas variables\\ independientes tiende a normal,\\"
            r"sea cual sea su distribución.",
            font_size=38, color=WHITE,
        )
        fit(tcl)
        tcl.move_to(UP * 0.25)
        self.play(Write(tcl), run_time=1.8)
        self.wait(0.8)

        formula = MathTex(
            r"\frac{\bar{X} - \mu}{\sigma / \sqrt{n}}",
            r"\;\longrightarrow\;",
            r"N(0, 1)",
            font_size=52,
        )
        formula[0].set_color(ACCENT_CYAN)
        formula[2].set_color_by_gradient(*GRADIENT_HIGHLIGHT)
        formula[2].set_stroke(width=1.2)
        formula.scale_to_fit_width(6.4)
        formula.move_to(DOWN * 3.2)
        self.play(Write(formula), run_time=1.4)

        caja = SurroundingRectangle(formula, buff=0.22, corner_radius=0.14)
        caja.set_stroke(width=5, color=[ACCENT_YELLOW, ACCENT_PURPLE])
        self.play(Create(caja), run_time=0.7)
        self.play(Indicate(formula[2], color=ACCENT_YELLOW, scale_factor=1.15),
                  run_time=0.8)
        self.wait(1.6)

        animate_End(scene=self)
