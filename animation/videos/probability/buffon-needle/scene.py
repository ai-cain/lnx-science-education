from manim import *
from lnx import *

import numpy as np

# montecarlo | probabilidad | intermedio
# La aguja de Buffon: pi sale de tirar palitos al suelo.
#
# Sobre un piso de lineas paralelas separadas una distancia d dejamos caer
# agujas de longitud L = d. La aguja cruza una linea si la distancia de su
# centro a la linea mas cercana es menor que (L/2) sin(theta), donde theta es
# el angulo respecto a las lineas. Promediando sobre theta uniforme en [0, pi]:
#
#   E[(L/2) sin(theta)] = (L/2) * (2/pi) = L/pi
#   P(cruce) = 2 * (L/pi) / d = 2L / (pi d)      (con L = d:  2/pi ~ 0.6366)
#
# y despejando pi:   pi ~ 2 L N / (d C),  N tiradas, C cruces.
# El pi aparece porque el promedio de sin(theta) sobre medio periodo es 2/pi:
# ahi esta escondida la circunferencia.
#
# La simulacion usa numpy con semilla FIJA (184): el render es reproducible y
# el valor final que se ve en pantalla es siempre el mismo: 400 tiradas, 255
# cruces, pi ~ 3,1373 (error 0,14%).
#
# El frame real es 9 x 16 unidades (x en [-4.5, 4.5], y en [-8, 8]).
# Zona segura: |y| <= 5.6 y |x| <= 3.8.

SAFE_W = 7.2

# --- geometria del piso -------------------------------------------------------
D = 0.9                 # separacion entre lineas
L = D                   # caso simple: aguja tan larga como la separacion
N_LINES = 6             # 6 lineas => 5 franjas completas (sin efecto de borde)
Y0 = -1.35              # linea mas baja
X_HALF = 3.55           # medio ancho del piso

# --- simulacion ---------------------------------------------------------------
SEED = 184              # elegida para que la convergencia se vea: 3,64 -> 3,137
SEED_HOOK = 0           # el gancho promete 3,14 y su muestra da 3,148
N_TOTAL = 400
N_HOOK = 170


def fit(m):
    """Evita que un mobject se salga de la zona segura horizontal."""
    if m.width > SAFE_W:
        m.scale_to_fit_width(SAFE_W)
    return m


def line_y(k):
    return Y0 + k * D


def simulate(n, seed):
    """Devuelve centros, angulos y si cruza, para n agujas reproducibles."""
    rng = np.random.default_rng(seed)
    xs = rng.uniform(-X_HALF + 0.25, X_HALF - 0.25, n)
    # El centro cae uniformemente sobre las 5 franjas completas: asi la
    # probabilidad teorica es exactamente 2L/(pi d), sin efectos de borde.
    ys = rng.uniform(line_y(0), line_y(N_LINES - 1), n)
    th = rng.uniform(0, PI, n)
    half = 0.5 * L * np.sin(th)
    # distancia del centro a la linea de abajo dentro de su franja
    frac = (ys - line_y(0)) % D
    crosses = (frac < half) | (frac > D - half)
    return xs, ys, th, crosses


def needle_mobject(x, y, theta, crossed, width=3.0):
    """Una aguja: magenta si cruza una linea, cyan si no."""
    dx = 0.5 * L * np.cos(theta)
    dy = 0.5 * L * np.sin(theta)
    start = np.array([x - dx, y - dy, 0.0])
    end = np.array([x + dx, y + dy, 0.0])
    color = ACCENT_MAGENTA if crossed else ACCENT_CYAN
    return Line(start, end, stroke_width=width, color=color)


class BuffonNeedle(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        # ------------------------------------------------------ el piso rayado
        floor = VGroup(*[
            Line(
                np.array([-X_HALF, line_y(k), 0.0]),
                np.array([X_HALF, line_y(k), 0.0]),
                stroke_width=2.5, color=GREY_B, stroke_opacity=0.55,
            )
            for k in range(N_LINES)
        ])
        floor.set_z_index(-1)

        # ----------------------------------------------------------- hook 0-6s
        # Primero la promesa, y de inmediato la prueba: una lluvia de agujas y
        # un numero que se planta en 3,14. Todo antes del segundo 6.
        hook = Tex(r"¿$\pi$ tirando palitos\\ al piso?", font_size=60, color=WHITE)
        hook.set_stroke(width=1)
        fit(hook)
        hook.move_to(UP * 5.0)
        self.play(Write(hook), run_time=0.8)

        xs_h, ys_h, th_h, cr_h = simulate(N_HOOK, SEED_HOOK)
        hook_needles = VGroup(*[
            needle_mobject(xs_h[i], ys_h[i], th_h[i], cr_h[i], width=2.2)
            for i in range(N_HOOK)
        ])
        hook_needles.set_stroke(opacity=0.9)

        self.play(FadeIn(floor), run_time=0.4)
        # Se sueltan en tandas: 170 animaciones sueltas matarian el render.
        for lote in range(0, N_HOOK, 34):
            self.play(
                FadeIn(hook_needles[lote:lote + 34], shift=DOWN * 0.25),
                run_time=0.22,
            )

        hook_pi = MathTex(r"\pi \approx 3{,}14", font_size=76)
        hook_pi.set_color_by_gradient(*GRADIENT_HIGHLIGHT)
        hook_pi.set_stroke(width=1.2)
        hook_pi.move_to(DOWN * 3.6)
        self.play(FadeIn(hook_pi, scale=1.4), run_time=0.7)
        self.wait(1.0)

        self.play(
            FadeOut(hook_needles), FadeOut(hook_pi), FadeOut(hook),
            run_time=0.6,
        )

        # ------------------------------------------- beat 1: el montaje 6-24s
        titulo = Tex(r"La aguja de Buffon", font_size=56, color=ACCENT_YELLOW)
        fit(titulo)
        titulo.move_to(UP * 5.1)
        self.play(Write(titulo), run_time=0.8)

        # La regla del juego: separacion d, aguja de la misma longitud.
        brace_d = BraceBetweenPoints(
            np.array([-X_HALF + 0.2, line_y(1), 0.0]),
            np.array([-X_HALF + 0.2, line_y(2), 0.0]),
            direction=LEFT, color=WHITE,
        )
        label_d = MathTex("d", font_size=40, color=WHITE)
        label_d.next_to(brace_d, LEFT, buff=0.12)
        self.play(GrowFromCenter(brace_d), Write(label_d), run_time=0.7)

        regla = Tex(r"Aguja de largo $L = d$", font_size=38, color=WHITE)
        fit(regla)
        regla.move_to(UP * 4.1)
        self.play(FadeIn(regla, shift=DOWN * 0.3), run_time=0.5)
        self.wait(0.5)

        # Tres tiradas a mano para fijar el criterio: cruza / no cruza.
        demos = [
            (-1.9, line_y(3) + 0.10, 75 * DEGREES, True),   # cruza
            (0.6, line_y(2) + 0.45, 8 * DEGREES, False),    # no cruza
            (2.3, line_y(4) - 0.05, 55 * DEGREES, True),    # cruza
        ]
        veredictos = VGroup()
        for i, (x, y, th, cr) in enumerate(demos):
            aguja = needle_mobject(x, y, th, cr, width=6.0)
            # Cae desde arriba y aterriza girando: se lee como "tirada".
            self.play(
                FadeIn(aguja, shift=DOWN * 1.2, scale=1.1),
                run_time=0.55,
            )
            texto = r"\textbf{cruza}" if cr else r"no cruza"
            color = ACCENT_MAGENTA if cr else ACCENT_CYAN
            v = Tex(texto, font_size=34, color=color)
            v.next_to(aguja, UP if cr else DOWN, buff=0.22)
            self.play(FadeIn(v, scale=1.2), run_time=0.35)
            veredictos.add(aguja, v)
            self.wait(0.35)

        self.wait(0.5)
        self.play(FadeOut(veredictos), FadeOut(regla), run_time=0.5)
        self.play(FadeOut(brace_d), FadeOut(label_d), run_time=0.4)

        # ------------------------------------------- beat 2: la lluvia 24-46s
        xs, ys, th, crosses = simulate(N_TOTAL, SEED)
        acumulado = np.cumsum(crosses)          # cruces tras k tiradas
        total_cruces = int(acumulado[-1])
        pi_final = 2.0 * L * N_TOTAL / (D * total_cruces)

        needles = [
            needle_mobject(xs[i], ys[i], th[i], crosses[i], width=2.2)
            for i in range(N_TOTAL)
        ]
        for n in needles:
            n.set_stroke(opacity=0.88)

        # --- tablero de contadores (debajo del piso, dentro de |y| <= 5.6) ---
        tracker = ValueTracker(0)

        def k_actual():
            return max(1, min(N_TOTAL, int(round(tracker.get_value()))))

        lbl_total = Tex(r"tiradas", font_size=30, color=GREY_A)
        num_total = DecimalNumber(0, num_decimal_places=0, font_size=52,
                                  color=WHITE)
        lbl_cruz = Tex(r"cruces", font_size=30, color=GREY_A)
        num_cruz = DecimalNumber(0, num_decimal_places=0, font_size=52,
                                 color=ACCENT_MAGENTA)

        col_total = VGroup(num_total, lbl_total).arrange(DOWN, buff=0.12)
        col_cruz = VGroup(num_cruz, lbl_cruz).arrange(DOWN, buff=0.12)
        tablero = VGroup(col_total, col_cruz).arrange(RIGHT, buff=1.5)
        tablero.move_to(DOWN * 3.05)

        formula_vivo = MathTex(
            r"\frac{2L}{d}\cdot\frac{N}{C}", r"=", font_size=44, color=WHITE,
        )
        num_pi = DecimalNumber(0, num_decimal_places=4, font_size=58,
                               color=ACCENT_YELLOW)
        estimacion = VGroup(formula_vivo, num_pi).arrange(RIGHT, buff=0.25)
        estimacion.move_to(DOWN * 4.6)
        fit(estimacion)

        # Un solo updater por numero: barato aunque haya 400 agujas en escena.
        num_total.add_updater(lambda m: m.set_value(k_actual()))
        num_cruz.add_updater(lambda m: m.set_value(int(acumulado[k_actual() - 1])))
        num_pi.add_updater(
            lambda m: m.set_value(
                2.0 * L * k_actual() / (D * max(1, int(acumulado[k_actual() - 1])))
            )
        )

        self.play(FadeIn(tablero), FadeIn(estimacion), run_time=0.6)

        # Las agujas se van sumando a un unico VGroup ya presente en escena:
        # nada se re-dibuja, solo se agregan mobjects nuevos cuadro a cuadro.
        lluvia = VGroup()
        self.add(lluvia)

        def sumar(grupo):
            k = min(N_TOTAL, int(tracker.get_value()))
            while len(grupo) < k:
                grupo.add(needles[len(grupo)])

        # Primer tramo lento: se ve caer aguja por aguja y el numero saltar.
        self.play(
            tracker.animate.set_value(40),
            UpdateFromFunc(lluvia, sumar),
            run_time=3.0, rate_func=linear,
        )
        # Segundo tramo: aceleron. El estimador se estabiliza a la vista.
        self.play(
            tracker.animate.set_value(N_TOTAL),
            UpdateFromFunc(lluvia, sumar),
            run_time=7.0, rate_func=rate_functions.ease_in_out_sine,
        )

        for m in (num_total, num_cruz, num_pi):
            m.clear_updaters()
        num_total.set_value(N_TOTAL)
        num_cruz.set_value(total_cruces)
        num_pi.set_value(pi_final)

        caja_pi = SurroundingRectangle(num_pi, buff=0.14, corner_radius=0.1)
        caja_pi.set_stroke(width=4, color=[YELLOW, ORANGE])
        self.play(Create(caja_pi), Indicate(num_pi, color=ACCENT_YELLOW,
                                            scale_factor=1.2), run_time=0.9)
        self.wait(1.4)

        # ---------------------------------------- beat 3: por que aparece pi
        self.play(
            FadeOut(lluvia), FadeOut(floor), FadeOut(tablero),
            FadeOut(estimacion), FadeOut(caja_pi), FadeOut(titulo),
            run_time=0.8,
        )

        pregunta = Tex(r"¿De dónde sale el $\pi$?", font_size=52,
                       color=ACCENT_YELLOW)
        fit(pregunta)
        pregunta.move_to(UP * 5.1)
        self.play(Write(pregunta), run_time=0.7)

        respuesta = Tex(r"Del ángulo.", font_size=42, color=WHITE)
        respuesta.move_to(UP * 4.2)
        self.play(FadeIn(respuesta, shift=DOWN * 0.3), run_time=0.5)

        # --- diagrama grande de una sola aguja girando ---
        DB = 3.0                      # separacion ampliada, para que se lea
        y_bot, y_top = 0.2, 0.2 + DB
        cx, cy = -1.0, (y_bot + y_top) / 2
        centro = np.array([cx, cy, 0.0])

        l1 = Line(np.array([-3.4, y_bot, 0.0]), np.array([3.4, y_bot, 0.0]),
                  stroke_width=3, color=GREY_B)
        l2 = Line(np.array([-3.4, y_top, 0.0]), np.array([3.4, y_top, 0.0]),
                  stroke_width=3, color=GREY_B)
        self.play(Create(l1), Create(l2), run_time=0.6)

        theta = ValueTracker(20 * DEGREES)

        def punta(signo):
            a = theta.get_value()
            return centro + signo * 0.5 * DB * np.array(
                [np.cos(a), np.sin(a), 0.0]
            )

        aguja = always_redraw(
            lambda: Line(punta(-1), punta(+1), stroke_width=8,
                         color=ACCENT_MAGENTA)
        )
        # La proyeccion vertical: exactamente lo que decide si hay cruce.
        proy = always_redraw(
            lambda: DashedLine(
                np.array([1.9, cy - 0.5 * DB * np.sin(theta.get_value()), 0.0]),
                np.array([1.9, cy + 0.5 * DB * np.sin(theta.get_value()), 0.0]),
                stroke_width=7, color=ACCENT_CYAN, dash_length=0.12,
            )
        )
        guias = always_redraw(
            lambda: VGroup(*[
                DashedLine(punta(s), np.array([1.9, punta(s)[1], 0.0]),
                           stroke_width=2, color=GREY_C, dash_length=0.09)
                for s in (-1, +1)
            ])
        )
        arco = always_redraw(
            lambda: Angle(
                Line(punta(-1), punta(-1) + RIGHT),
                Line(punta(-1), punta(+1)),
                radius=0.55, color=ACCENT_YELLOW, stroke_width=4,
            )
        )
        lbl_theta = always_redraw(
            lambda: MathTex(r"\theta", font_size=38, color=ACCENT_YELLOW)
            .move_to(punta(-1) + np.array([0.85, 0.34, 0.0]))
        )
        lbl_proy = MathTex(r"L\sin\theta", font_size=40, color=ACCENT_CYAN)
        lbl_proy.move_to(np.array([3.0, cy, 0.0]))

        self.play(Create(aguja), run_time=0.5)
        self.play(Create(arco), Write(lbl_theta), run_time=0.5)
        self.play(Create(proy), Create(guias), Write(lbl_proy), run_time=0.7)

        # El barrido del angulo: la proyeccion crece, se llena, se apaga.
        self.play(theta.animate.set_value(90 * DEGREES), run_time=1.5)
        self.wait(0.3)
        self.play(theta.animate.set_value(160 * DEGREES), run_time=1.5)
        self.play(theta.animate.set_value(55 * DEGREES), run_time=1.2)

        self.play(
            FadeOut(VGroup(l1, l2, aguja, proy, guias, arco, lbl_theta,
                           lbl_proy)),
            FadeOut(respuesta),
            run_time=0.6,
        )

        # El promedio de sin sobre medio giro: aqui esta el pi escondido.
        promedio = MathTex(
            r"\frac{1}{\pi}\int_0^{\pi}\sin\theta\,d\theta",
            r"=", r"\frac{2}{\pi}",
            font_size=52,
        )
        promedio[2].set_color(ACCENT_YELLOW)
        fit(promedio)
        promedio.move_to(UP * 2.4)
        self.play(Write(promedio), run_time=1.4)
        self.play(Indicate(promedio[2], color=ACCENT_YELLOW, scale_factor=1.3),
                  run_time=0.7)
        self.wait(0.9)

        prob = MathTex(
            r"P(\text{cruce})", r"=", r"\frac{2L}{\pi d}",
            font_size=54,
        )
        prob[2].set_color(ACCENT_MAGENTA)
        fit(prob)
        prob.move_to(DOWN * 0.3)
        self.play(TransformFromCopy(promedio[2], prob[2]), run_time=0.8)
        self.play(Write(VGroup(prob[0], prob[1])), run_time=0.7)
        self.wait(1.2)

        # ------------------------------------------------------------- cierre
        despeje = MathTex(
            r"\pi", r"\approx", r"\frac{2LN}{dC}",
            font_size=66,
        )
        despeje[0].set_color_by_gradient(*GRADIENT_HIGHLIGHT)
        despeje[0].set_stroke(width=1.2)
        despeje[2].set_color(ACCENT_CYAN)
        fit(despeje)
        despeje.move_to(DOWN * 3.0)
        self.play(TransformFromCopy(prob[2], despeje[2]), run_time=0.9)
        self.play(Write(VGroup(despeje[0], despeje[1])), run_time=0.7)

        caja = SurroundingRectangle(despeje, buff=0.2, corner_radius=0.12)
        caja.set_stroke(width=5, color=[YELLOW, ORANGE])
        self.play(Create(caja), run_time=0.6)
        self.wait(0.8)

        # Y el numero real que produjo esta simulacion, para cerrar el circulo.
        cuenta = MathTex(
            r"\frac{2\cdot " + str(N_TOTAL) + r"}{" + str(total_cruces) + r"}",
            r"=", f"{pi_final:.4f}".replace(".", "{,}"),
            font_size=48,
        )
        cuenta[2].set_color(ACCENT_YELLOW)
        fit(cuenta)
        cuenta.move_to(DOWN * 5.0)
        self.play(FadeIn(cuenta, shift=UP * 0.3), run_time=0.7)
        self.play(Indicate(cuenta[2], color=ACCENT_YELLOW, scale_factor=1.25),
                  run_time=0.8)
        self.wait(1.8)

        animate_End(scene=self)
