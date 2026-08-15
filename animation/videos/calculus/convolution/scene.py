from manim import *
from lnx import *

# mechanism-reveal | calculus (convolution) | advanced
#
#   (f * g)(t) = \int f(\tau) g(t-\tau) d\tau
#
# La convolucion se ensena como una formula y casi nadie ve la maquina que hay
# detras. La maquina tiene tres piezas y solo una es rara:
#   1. VOLTEAR : g(\tau) -> g(-\tau).  El espejo. Esto es lo que nadie entiende.
#   2. DESLIZAR: g(-\tau) -> g(t-\tau). El espejo se mueve con t.
#   3. INTEGRAR: el area del producto f(\tau) g(t-\tau) ES el valor (f*g)(t).
#
# Estructura: dos casos verificables. Rect * Rect da un TRIANGULO exacto (el
# solape crece lineal, satura, decrece), y Rect * Gaussiana suaviza los bordes,
# que es literalmente el desenfoque de una foto y el kernel de una CNN.
#
# El hermano de este video es fourier-epicycles: alli todo eran circulos
# girando y trazos cerrados; aqui todo son paneles apilados y area sombreada,
# asi que el lenguaje visual no se repite. El cierre los conecta: convolucion
# en el tiempo = multiplicacion en frecuencia.
#
# Todas las curvas de resultado se calculan por cuadratura y se validan contra
# np.convolve antes de animar: lo que se dibuja es el numero real.
#
# El frame es 9 x 16 (x en [-4.5, 4.5], y en [-8, 8]).
# Zona segura: |y| <= 5.6 y |x| <= 3.8.

SAFE_WIDTH = 7.2

# Malla de integracion. Densa para el calculo, mas rala para lo que se redibuja
# en cada frame (el coste de always_redraw es lineal en el numero de puntos).
TAU_MIN, TAU_MAX = -3.4, 3.4
DENSE_N = 1361                      # ~0.005 de paso: cuadratura fiable
DRAW_N = 341                        # ~0.02 de paso: suficiente para el ojo
TAU_DENSE = np.linspace(TAU_MIN, TAU_MAX, DENSE_N)
TAU_DRAW = np.linspace(TAU_MIN, TAU_MAX, DRAW_N)

T_MIN, T_MAX = -2.9, 2.9
T_SAMPLES = 481
T_GRID = np.linspace(T_MIN, T_MAX, T_SAMPLES)

# Geometria de los paneles apilados: f y g arriba (comparten eje tau), el
# resultado abajo con el MISMO x_length, para que la vertical de t una ambos.
PANEL_WIDTH = 6.9
TOP_CENTER = np.array([0.0, 2.15, 0.0])
BOTTOM_CENTER = np.array([0.0, -2.75, 0.0])
TITLE_Y = 5.25
STEP_Y = 4.35
NOTE_Y = -5.15

F_COLOR = ACCENT_CYAN
G_COLOR = ACCENT_MAGENTA
AREA_COLOR = ACCENT_YELLOW
RESULT_COLOR = ACCENT_YELLOW
AXIS_COLOR = GREY_B


def fit_to_safe_width(mobject):
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


# --------------------------------------------------------------- las senales
def rect(tau, half=0.75, amplitude=1.0):
    """Pulso rectangular centrado en 0."""
    return np.where(np.abs(tau) <= half, amplitude, 0.0)


def ramp_decay(tau):
    """Pulso claramente ASIMETRICO: sin el, el volteo seria invisible."""
    return np.where((tau >= 0.0) & (tau <= 1.6), np.exp(-1.6 * tau), 0.0)


def gaussian(tau, sigma=0.28):
    """Nucleo gaussiano de area 1: promedia sin cambiar la escala."""
    return np.exp(-(tau**2) / (2 * sigma**2)) / (sigma * np.sqrt(TAU))


# ------------------------------------------------------------- la cuadratura
def convolve_numeric(f, g, t_grid=T_GRID):
    """(f*g)(t) por trapecios sobre la malla densa, para cada t."""
    f_values = f(TAU_DENSE)
    return np.array(
        [np.trapezoid(f_values * g(t - TAU_DENSE), TAU_DENSE) for t in t_grid]
    )


def verify_against_fft(f, g, values, tolerance=2e-2):
    """Segunda opinion: np.convolve discreta sobre la misma malla.

    Si las dos rutas no coinciden, la curva animada estaria mintiendo, asi que
    preferimos fallar en tiempo de import antes que renderizar algo falso.
    """
    step = TAU_DENSE[1] - TAU_DENSE[0]
    discrete = np.convolve(f(TAU_DENSE), g(TAU_DENSE), mode="full") * step
    axis = 2 * TAU_MIN + step * np.arange(len(discrete))
    resampled = np.interp(T_GRID, axis, discrete)
    error = np.max(np.abs(resampled - values))
    scale = max(np.max(np.abs(values)), 1e-9)
    assert error / scale < tolerance, f"convolucion inconsistente: {error}"
    return values


CONV_RECT = verify_against_fft(rect, rect, convolve_numeric(rect, rect))
CONV_RAMP = verify_against_fft(rect, ramp_decay, convolve_numeric(rect, ramp_decay))
CONV_GAUSS = verify_against_fft(rect, gaussian, convolve_numeric(rect, gaussian))


# ------------------------------------------------------------------- dibujo
def make_axes(y_max, center, height):
    axes = Axes(
        x_range=[TAU_MIN, TAU_MAX, 1.0],
        y_range=[0.0, y_max, y_max],
        x_length=PANEL_WIDTH,
        y_length=height,
        tips=False,
        axis_config={
            "stroke_width": 2.0,
            "stroke_opacity": 0.55,
            "color": AXIS_COLOR,
            "include_ticks": False,
        },
    )
    axes.move_to(center)
    return axes


def polyline(axes, xs, ys, color, width=5.0, opacity=1.0):
    line = VMobject()
    line.set_points_as_corners([axes.c2p(x, y) for x, y in zip(xs, ys)])
    line.set_stroke(color=color, width=width, opacity=opacity)
    return line


def area_under(axes, xs, ys, color=AREA_COLOR, opacity=0.5):
    """Region sombreada bajo el producto: el integrando, no una decoracion."""
    top = [axes.c2p(x, y) for x, y in zip(xs, ys)]
    base = [axes.c2p(xs[-1], 0.0), axes.c2p(xs[0], 0.0)]
    region = VMobject()
    region.set_points_as_corners(top + base)
    region.set_fill(color=color, opacity=opacity)
    region.set_stroke(color=color, width=1.5, opacity=0.85)
    region.set_z_index(-2)
    return region


def panel_label(tex, color, font_size=30):
    label = MathTex(tex, font_size=font_size, color=color)
    label.add_background_rectangle(color=BG, opacity=0.9, buff=0.07)
    label.set_z_index(12)
    return label


class Convolution(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.14
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.8)
        watermark.set_z_index(30)
        self.add(watermark)

        # Ejes fijos durante todo el video: el ojo aprende el escenario una vez.
        self.top_axes = make_axes(1.75, TOP_CENTER, 2.30)
        self.bottom_axes = make_axes(1.75, BOTTOM_CENTER, 2.10)
        self.add(self.top_axes, self.bottom_axes)

        divider = DashedLine(
            LEFT * 3.55 + DOWN * 0.45,
            RIGHT * 3.55 + DOWN * 0.45,
            dash_length=0.12,
            stroke_width=1.6,
            color=AXIS_COLOR,
        ).set_stroke(opacity=0.35)
        self.add(divider)

        result_tag = MathTex(r"(f*g)(t)", font_size=30, color=RESULT_COLOR)
        result_tag.next_to(self.bottom_axes, UP, buff=0.12).align_to(
            self.bottom_axes, LEFT
        )
        result_tag.set_z_index(12)
        self.add(result_tag)

        # ------------------------------------------------------- HOOK (0-2 s)
        # La maquina completa corriendo, sin una sola palabra de explicacion.
        title = Tex(r"\textbf{Convolución}", font_size=54, color=WHITE)
        title.move_to(UP * TITLE_Y)
        title.set_stroke(width=1)
        title.set_z_index(20)
        fit_to_safe_width(title)
        underline = Line(
            title.get_left() + DOWN * 0.3,
            title.get_right() + DOWN * 0.3,
            stroke_width=4,
        ).set_color([F_COLOR, G_COLOR])
        underline.set_z_index(20)

        self.play(Write(title), Create(underline), run_time=0.7)

        hook = self.build_sweep(rect, rect, CONV_RECT)
        self.play(FadeIn(hook["static"]), FadeIn(hook["live"]), run_time=0.35)
        self.play(
            hook["tracker"].animate.set_value(T_MAX),
            run_time=3.2,
            rate_func=linear,
        )
        self.wait(0.25)

        hook_line = Tex(
            r"\textbf{Dos cuadrados. ¿Y sale un triángulo?}",
            font_size=32,
            color=AREA_COLOR,
        ).move_to(DOWN * NOTE_Y * 0 + DOWN * 5.15)
        hook_line.set_stroke(width=1)
        fit_to_safe_width(hook_line)
        self.play(FadeIn(hook_line, shift=UP * 0.12), run_time=0.4)
        self.wait(0.7)
        self.play(
            FadeOut(hook_line),
            FadeOut(hook["static"]),
            FadeOut(hook["live"]),
            run_time=0.4,
        )
        self.clear_sweep(hook)

        # ------------------------------------------------- BEAT 1: los 3 pasos
        # Con g ASIMETRICA, porque con una g simetrica el volteo no se ve y el
        # espectador se queda pensando que el paso 1 es un adorno.
        subtitle = Tex(
            r"\textbf{La máquina tiene tres piezas}",
            font_size=32,
            color=WHITE,
        ).move_to(UP * STEP_Y)
        subtitle.set_stroke(width=1)
        fit_to_safe_width(subtitle)
        self.play(
            Transform(title, subtitle),
            FadeOut(underline),
            run_time=0.5,
        )

        f_curve = polyline(self.top_axes, TAU_DRAW, rect(TAU_DRAW), F_COLOR)
        f_label = panel_label(r"f(\tau)", F_COLOR)
        f_label.move_to(self.top_axes.c2p(-2.55, 1.35))

        g_curve = polyline(
            self.top_axes, TAU_DRAW, ramp_decay(TAU_DRAW), G_COLOR
        )
        g_label = panel_label(r"g(\tau)", G_COLOR)
        g_label.move_to(self.top_axes.c2p(2.35, 1.35))

        self.play(
            Create(f_curve), FadeIn(f_label),
            Create(g_curve), FadeIn(g_label),
            run_time=0.9,
        )

        # --- Paso 1: VOLTEAR. Un espejo literal sobre el eje tau = 0.
        step_1 = Tex(r"\textbf{1. Voltear}", font_size=34, color=G_COLOR)
        step_1.move_to(DOWN * 5.15)
        step_1.set_stroke(width=1)
        mirror = DashedLine(
            self.top_axes.c2p(0.0, -0.06),
            self.top_axes.c2p(0.0, 1.7),
            dash_length=0.1,
            color=WHITE,
            stroke_width=2,
        ).set_stroke(opacity=0.6)

        self.play(FadeIn(step_1, shift=UP * 0.1), Create(mirror), run_time=0.5)
        self.play(
            g_curve.animate.flip(UP, about_point=self.top_axes.c2p(0.0, 0.0)),
            Transform(g_label, panel_label(r"g(-\tau)", G_COLOR).move_to(
                self.top_axes.c2p(2.35, 1.35)
            )),
            run_time=1.1,
            rate_func=smooth,
        )
        self.play(
            Indicate(g_curve, color=AREA_COLOR, scale_factor=1.0),
            run_time=0.7,
        )
        self.wait(0.3)

        # --- Paso 2: DESLIZAR. t es solo cuanto se ha movido el espejo.
        step_2 = Tex(r"\textbf{2. Deslizar}", font_size=34, color=G_COLOR)
        step_2.move_to(DOWN * 5.15)
        step_2.set_stroke(width=1)
        shift_x = self.top_axes.c2p(1.1, 0.0)[0] - self.top_axes.c2p(0.0, 0.0)[0]
        self.play(
            Transform(step_1, step_2),
            FadeOut(mirror),
            Transform(g_label, panel_label(r"g(t-\tau)", G_COLOR).move_to(
                self.top_axes.c2p(2.35, 1.35)
            )),
            run_time=0.5,
        )
        self.play(
            g_curve.animate.shift(RIGHT * shift_x),
            run_time=0.8,
            rate_func=there_and_back_with_pause,
        )
        self.wait(0.2)

        # --- Paso 3: INTEGRAR. El area del producto ES el valor de salida.
        step_3 = Tex(
            r"\textbf{3. Integrar el producto}", font_size=34, color=AREA_COLOR
        )
        step_3.move_to(DOWN * 5.15)
        step_3.set_stroke(width=1)
        fit_to_safe_width(step_3)
        self.play(Transform(step_1, step_3), run_time=0.45)

        ramp = self.build_sweep(rect, ramp_decay, CONV_RAMP, start=-0.35)
        self.play(
            FadeOut(f_curve), FadeOut(g_curve),
            FadeOut(f_label), FadeOut(g_label),
            FadeIn(ramp["static"]), FadeIn(ramp["live"]),
            run_time=0.5,
        )
        self.play(
            ramp["tracker"].animate.set_value(T_MAX),
            run_time=4.4,
            rate_func=linear,
        )
        self.wait(0.35)
        self.play(
            FadeOut(step_1),
            FadeOut(ramp["static"]),
            FadeOut(ramp["live"]),
            run_time=0.4,
        )
        self.clear_sweep(ramp)

        # ------------------------------- BEAT 2: caso limpio y comprobable
        claim = Tex(
            r"\textbf{Caso 1: dos pulsos iguales}",
            font_size=32,
            color=F_COLOR,
        ).move_to(UP * STEP_Y)
        claim.set_stroke(width=1)
        fit_to_safe_width(claim)
        self.play(Transform(title, claim), run_time=0.45)

        rect_case = self.build_sweep(rect, rect, CONV_RECT)
        note = Tex(
            r"\textbf{el solape crece, satura y cae}",
            font_size=30,
            color=WHITE,
        ).move_to(DOWN * 5.15)
        note.set_stroke(width=1)
        fit_to_safe_width(note)

        self.play(
            FadeIn(rect_case["static"]),
            FadeIn(rect_case["live"]),
            FadeIn(note, shift=UP * 0.1),
            run_time=0.5,
        )
        self.play(
            rect_case["tracker"].animate.set_value(0.0),
            run_time=2.6,
            rate_func=linear,
        )
        self.play(
            rect_case["tracker"].animate.set_value(T_MAX),
            run_time=2.6,
            rate_func=linear,
        )

        # El triangulo exacto: 3 unidades de base, altura = 2 x el semiancho.
        payoff = Tex(
            r"\textbf{Cuadrado} $*$ \textbf{cuadrado} $=$ \textbf{triángulo}",
            font_size=31,
            color=AREA_COLOR,
        ).move_to(DOWN * 5.15)
        payoff.set_stroke(width=1)
        fit_to_safe_width(payoff)
        self.play(
            Transform(note, payoff),
            Indicate(rect_case["trace"], color=WHITE, scale_factor=1.03),
            run_time=1.0,
        )
        self.wait(0.7)
        self.play(
            FadeOut(note),
            FadeOut(rect_case["static"]),
            FadeOut(rect_case["live"]),
            FadeOut(rect_case["trace"]),
            run_time=0.4,
        )
        self.clear_sweep(rect_case, fade_trace=False)

        # ------------------------------- BEAT 3: el nucleo que promedia
        claim_2 = Tex(
            r"\textbf{Caso 2: pulso $*$ gaussiana}",
            font_size=32,
            color=G_COLOR,
        ).move_to(UP * STEP_Y)
        claim_2.set_stroke(width=1)
        fit_to_safe_width(claim_2)
        self.play(Transform(title, claim_2), run_time=0.45)

        gauss_case = self.build_sweep(rect, gaussian, CONV_GAUSS)
        note_2 = Tex(
            r"\textbf{cada punto = promedio de sus vecinos}",
            font_size=29,
            color=WHITE,
        ).move_to(DOWN * 5.15)
        note_2.set_stroke(width=1)
        fit_to_safe_width(note_2)

        self.play(
            FadeIn(gauss_case["static"]),
            FadeIn(gauss_case["live"]),
            FadeIn(note_2, shift=UP * 0.1),
            run_time=0.5,
        )
        self.play(
            gauss_case["tracker"].animate.set_value(T_MAX),
            run_time=4.6,
            rate_func=linear,
        )

        # Los bordes verticales se volvieron rampas: eso es desenfocar.
        blur_note = Tex(
            r"\textbf{Los bordes se suavizan: eso es desenfocar}",
            font_size=29,
            color=AREA_COLOR,
        ).move_to(DOWN * 5.15)
        blur_note.set_stroke(width=1)
        fit_to_safe_width(blur_note)
        self.play(Transform(note_2, blur_note), run_time=0.6)

        cnn_note = Tex(
            r"\textbf{y es el \emph{kernel} de una red convolucional}",
            font_size=29,
            color=ACCENT_PURPLE,
        ).move_to(DOWN * 5.15)
        cnn_note.set_stroke(width=1)
        fit_to_safe_width(cnn_note)
        self.wait(0.6)
        self.play(Transform(note_2, cnn_note), run_time=0.6)
        self.wait(0.6)

        self.play(
            FadeOut(note_2),
            FadeOut(gauss_case["static"]),
            FadeOut(gauss_case["live"]),
            FadeOut(gauss_case["trace"]),
            FadeOut(result_tag),
            FadeOut(divider),
            FadeOut(self.top_axes),
            FadeOut(self.bottom_axes),
            run_time=0.6,
        )
        self.clear_sweep(gauss_case, fade_trace=False)

        # ------------------------------------------------------------ CIERRE
        formula = MathTex(
            r"(f*g)(t)", r"=", r"\int_{-\infty}^{\infty}",
            r"f(\tau)", r"\,g(t-\tau)", r"\,d\tau",
            font_size=40,
        )
        formula[0].set_color(RESULT_COLOR)
        formula[3].set_color(F_COLOR)
        formula[4].set_color(G_COLOR)
        formula.set_stroke(width=1)
        formula.move_to(UP * 1.1)
        fit_to_safe_width(formula)

        closing_title = Tex(
            r"\textbf{Y aquí está el atajo}", font_size=34, color=WHITE
        ).move_to(UP * STEP_Y)
        closing_title.set_stroke(width=1)
        fit_to_safe_width(closing_title)

        self.play(Transform(title, closing_title), run_time=0.4)
        self.play(Write(formula), run_time=1.5)
        self.wait(0.5)

        # El puente con el video de epiciclos: Fourier convierte esta integral
        # cara en una multiplicacion punto a punto.
        bridge = MathTex(
            r"\mathcal{F}\{f*g\}", r"=", r"\mathcal{F}\{f\}", r"\cdot",
            r"\mathcal{F}\{g\}",
            font_size=40,
        )
        bridge[0].set_color(RESULT_COLOR)
        bridge[2].set_color(F_COLOR)
        bridge[4].set_color(G_COLOR)
        bridge[3].set_color(ACCENT_PURPLE)
        bridge.set_stroke(width=1)
        bridge.move_to(DOWN * 1.4)
        fit_to_safe_width(bridge)

        self.play(TransformFromCopy(formula, bridge), run_time=1.3)

        bridge_box = SurroundingRectangle(bridge, buff=0.22, corner_radius=0.12)
        bridge_box.set_stroke(width=4, color=[AREA_COLOR, ACCENT_PURPLE])
        final_note = Tex(
            r"\textbf{Convolucionar en el tiempo}\\[2pt]"
            r"\textbf{es multiplicar en frecuencia}",
            font_size=33,
            color=WHITE,
        ).move_to(DOWN * 3.7)
        final_note.set_stroke(width=1)
        fit_to_safe_width(final_note)

        self.play(Create(bridge_box), FadeIn(final_note, shift=UP * 0.12), run_time=0.9)
        self.play(Indicate(bridge[3], color=AREA_COLOR, scale_factor=1.6), run_time=0.8)
        self.wait(1.4)

        animate_End(scene=self)

    # ------------------------------------------------------------- maquinaria
    def build_sweep(self, f, g, values, start=T_MIN):
        """Monta el barrido completo para un par (f, g).

        Devuelve los mobjects estaticos, los vivos (always_redraw) y el
        ValueTracker de t. La curva del resultado esta PRECALCULADA por
        cuadratura: el updater solo recorta cuantos puntos se ven.
        """
        tracker = ValueTracker(start)
        top = self.top_axes
        bottom = self.bottom_axes

        f_draw = f(TAU_DRAW)
        f_curve = polyline(top, TAU_DRAW, f_draw, F_COLOR)
        f_curve.set_z_index(4)
        f_label = panel_label(r"f(\tau)", F_COLOR).move_to(top.c2p(-2.6, 1.4))
        g_label = panel_label(r"g(t-\tau)", G_COLOR).move_to(top.c2p(2.25, 1.4))
        static = VGroup(f_curve, f_label, g_label)

        # Puntos del resultado ya en coordenadas de pantalla: recortar es barato.
        trace_points = np.array([bottom.c2p(t, v) for t, v in zip(T_GRID, values)])

        def visible_count():
            progress = np.clip(
                (tracker.get_value() - T_MIN) / (T_MAX - T_MIN), 0.0, 1.0
            )
            return int(progress * (T_SAMPLES - 1))

        def make_g():
            shifted = g(tracker.get_value() - TAU_DRAW)
            curve = polyline(top, TAU_DRAW, shifted, G_COLOR)
            curve.set_z_index(3)
            return curve

        def make_area():
            product = f(TAU_DRAW) * g(tracker.get_value() - TAU_DRAW)
            return area_under(top, TAU_DRAW, product)

        def make_trace():
            count = visible_count()
            line = VMobject()
            if count < 1:
                line.set_points_as_corners([trace_points[0], trace_points[0]])
            else:
                line.set_points_as_corners(trace_points[: count + 1])
            line.set_stroke(color=RESULT_COLOR, width=5)
            line.set_z_index(6)
            return line

        def make_cursor():
            t = np.clip(tracker.get_value(), T_MIN, T_MAX)
            value = float(np.interp(t, T_GRID, values))
            dot = Dot(bottom.c2p(t, value), radius=0.085, color=RESULT_COLOR)
            dot.set_z_index(9)
            link = DashedLine(
                top.c2p(t, 0.0),
                bottom.c2p(t, value),
                dash_length=0.11,
                stroke_width=2,
                color=AREA_COLOR,
            ).set_stroke(opacity=0.45)
            link.set_z_index(1)
            return VGroup(link, dot)

        g_curve = always_redraw(make_g)
        area = always_redraw(make_area)
        trace = always_redraw(make_trace)
        cursor = always_redraw(make_cursor)

        return {
            "tracker": tracker,
            "static": static,
            "live": VGroup(g_curve, area, cursor),
            "trace": trace,
            "values": values,
        }

    def clear_sweep(self, sweep, fade_trace=True):
        """Corta los updaters y saca todo de la escena."""
        for group in (sweep["live"], sweep["trace"]):
            for mobject in [group, *group.submobjects]:
                mobject.clear_updaters()
        self.remove(sweep["static"], sweep["live"], sweep["trace"])
