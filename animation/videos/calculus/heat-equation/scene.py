from manim import *
from lnx import *

# visual-derivation | calculus | intermediate
# The heat equation:  du/dt = alpha * d2u/dx2
#
# The everyday hook: everyone "solves" this equation at home while waiting for
# their coffee to cool down, and almost nobody knows it is a PDE.
#
# The insight that carries the video is the discrete reading of the second
# derivative: u_xx compares a point with the average of its neighbours, so the
# whole equation says nothing more than "every point drifts toward the average
# of its neighbours". Peaks (concave down) cool, valleys (concave up) warm, and
# the profile can only flatten out.
#
# The actual frame is 9 x 16 units (x in [-4.5, 4.5], y in [-8, 8]).
# Safe area: |y| <= 5.6 and |x| <= 3.8.

SAFE_WIDTH = 7.2

# ------------------------------------------------------------- exact solution
# Dirichlet boundary conditions on [0, 1] (both ends held cold), so the initial
# profile expands in sines and every mode decays as exp(-(n pi)^2 alpha t).
# Two bumps of different width make the smoothing clearly visible.
MODES = 40
ALPHA = 0.02


def _initial_profile(x):
    return np.exp(-((x - 0.35) / 0.09) ** 2) + 0.75 * np.exp(-((x - 0.72) / 0.06) ** 2)


_grid = np.linspace(0.0, 1.0, 2001)
_COEFFS = [
    2 * np.trapezoid(_initial_profile(_grid) * np.sin(n * np.pi * _grid), _grid)
    for n in range(1, MODES + 1)
]


def temperature(x, t):
    """Value of the solution u(x, t) of the heat equation."""
    return sum(
        _COEFFS[n - 1] * np.sin(n * np.pi * x) * np.exp(-((n * np.pi) ** 2) * ALPHA * t)
        for n in range(1, MODES + 1)
    )


def fit_to_safe_width(mobject):
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def make_label(tex, font_size, color, with_background=True):
    label = MathTex(tex, font_size=font_size, color=color)
    if with_background:
        label.add_background_rectangle(color=BG, opacity=0.92, buff=0.06)
    label.set_z_index(10)
    return label


class HeatEquation(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.14
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.85)
        self.add(watermark)

        # The palette ships plain hex strings, but interpolate_color needs real
        # ManimColor instances to blend the temperature ramp.
        COLD_COLOR = ManimColor(ACCENT_CYAN)
        WARM_COLOR = ManimColor(ACCENT_YELLOW)
        HOT_COLOR = ManimColor("#FF8A00")
        CURVE_COLOR = ACCENT_YELLOW
        COOLS_COLOR = ACCENT_CYAN
        WARMS_COLOR = "#FF8A00"
        AUX_COLOR = GREY_B

        _cold = np.array(COLD_COLOR.to_rgb())
        _warm = np.array(WARM_COLOR.to_rgb())
        _hot = np.array(HOT_COLOR.to_rgb())

        def temp_ramp(values):
            """Map temperatures in [0, 1] to the cold -> warm -> hot ramp."""
            v = np.clip(np.asarray(values, dtype=float), 0.0, 1.0)[:, None]
            lower = _cold + (_warm - _cold) * (v / 0.5)
            upper = _warm + (_hot - _warm) * ((v - 0.5) / 0.5)
            return np.where(v < 0.5, lower, upper)

        clock = ValueTracker(0.0)

        # ------------------------------------------------------------ hook 0-3s
        title = Tex(r"Ecuaci\'on del Calor", font_size=60, color=WHITE)
        title.set_stroke(width=1)
        title.set_z_index(20)
        title.move_to(UP * 5.5)
        fit_to_safe_width(title)

        underline = Line(
            title.get_left() + DOWN * 0.3,
            title.get_right() + DOWN * 0.3,
            stroke_width=4,
        )
        underline.set_color(color=[COLD_COLOR, WARM_COLOR, HOT_COLOR])
        underline.set_z_index(20)

        subtitle = Tex(
            r"la resuelves cada vez que esperas\\que se enfr\'ie tu caf\'e",
            font_size=32,
            color=GREY_A,
        )
        subtitle.set_z_index(20)
        subtitle.move_to(UP * 4.45)
        fit_to_safe_width(subtitle)

        self.play(Write(title), run_time=0.9)
        self.play(Create(underline), run_time=0.5)
        self.play(FadeIn(subtitle, shift=UP * 0.15), run_time=0.7)
        self.wait(0.8)

        # ------------------------------------------------------------- the rod
        # A metal bar whose colour is the temperature itself.
        bar_width = 6.6
        bar_height = 0.6
        bar_center = UP * 2.95
        samples = 512

        # A single resampled image instead of many thin rectangles: adjacent
        # rectangles leave antialiasing seams that make the bar look striped.
        _bar_x = (np.arange(samples) + 0.5) / samples

        def bar_image(t):
            pixels = (temp_ramp(temperature(_bar_x, t)) * 255).astype(np.uint8)
            image = ImageMobject(pixels.reshape(1, samples, 3))
            image.stretch_to_fit_width(bar_width)
            image.stretch_to_fit_height(bar_height)
            image.move_to(bar_center)
            return image

        bar = Group(bar_image(0.0))

        def paint_bar(group):
            group.submobjects = [bar_image(clock.get_value())]
        bar_frame = Rectangle(
            width=bar_width + 0.04,
            height=bar_height + 0.04,
            stroke_color=AUX_COLOR,
            stroke_width=2,
        ).move_to(bar_center)

        self.play(FadeOut(subtitle), run_time=0.4)
        self.play(FadeIn(bar), Create(bar_frame), run_time=0.9)
        self.wait(0.4)

        # ------------------------------------------------- temperature profile
        axes = Axes(
            x_range=[0, 1, 0.25],
            y_range=[0, 1.1, 0.5],
            x_length=bar_width,
            y_length=2.9,
            tips=False,
            axis_config={
                "stroke_color": AUX_COLOR,
                "stroke_width": 2,
                "include_ticks": False,
            },
        )
        axes.move_to(UP * 0.55)
        axes.set_z_index(1)

        u_label = make_label("u(x,t)", 30, CURVE_COLOR, with_background=False)
        u_label.next_to(axes, UP, buff=0.12).align_to(axes, LEFT)

        curve = axes.plot(
            lambda x: temperature(x, 0.0), x_range=[0, 1, 0.004], color=CURVE_COLOR
        )
        curve.set_stroke(width=5)
        curve.set_z_index(4)

        self.play(Create(axes), run_time=0.6)
        self.play(Create(curve), Write(u_label), run_time=1.1)
        self.wait(0.5)

        # -------------------------------------------------------- the equation
        equation = MathTex(
            r"\frac{\partial u}{\partial t}", r"=", r"\alpha",
            r"\frac{\partial^2 u}{\partial x^2}",
            font_size=52,
        )
        equation[0].set_color(HOT_COLOR)
        equation[3].set_color(CURVE_COLOR)
        equation.set_stroke(width=1)
        equation.set_z_index(21)
        equation.move_to(DOWN * 2.15)
        fit_to_safe_width(equation)
        self.play(Write(equation), run_time=1.0)
        self.wait(0.8)

        # --------------------------------------------- what the equation means
        # The second derivative compares a point with the average of its two
        # neighbours: that single reading explains the whole behaviour.
        def probe(x0, half_width, color, goes_up):
            """Show a point against the average of its two neighbours."""
            left_x, right_x = x0 - half_width, x0 + half_width
            left_point = axes.c2p(left_x, temperature(left_x, 0.0))
            right_point = axes.c2p(right_x, temperature(right_x, 0.0))
            here = axes.c2p(x0, temperature(x0, 0.0))
            average = (left_point + right_point) / 2

            chord = DashedLine(left_point, right_point, color=color, stroke_width=3)
            chord.set_z_index(6)
            neighbours = VGroup(
                Dot(left_point, color=color, radius=0.06),
                Dot(right_point, color=color, radius=0.06),
            )
            neighbours.set_z_index(7)
            average_dot = Dot(average, color=color, radius=0.07)
            average_dot.set_z_index(7)
            here_dot = Dot(here, color=WHITE, radius=0.07)
            here_dot.set_z_index(7)

            arrow = Arrow(
                here, average, buff=0.04, color=color,
                stroke_width=5, max_tip_length_to_length_ratio=0.35,
            )
            arrow.set_z_index(8)

            self.play(FadeIn(here_dot), FadeIn(neighbours), run_time=0.5)
            self.play(Create(chord), FadeIn(average_dot), run_time=0.6)
            self.play(GrowArrow(arrow), run_time=0.6)
            return VGroup(chord, neighbours, average_dot, here_dot, arrow)

        # A peak sits above the average of its neighbours, so it cools down.
        peak_probe = probe(0.35, 0.10, COOLS_COLOR, goes_up=False)
        peak_text = Tex(r"un pico est\'a por encima\\de sus vecinos: se enfr\'ia",
                        font_size=28, color=COOLS_COLOR)
        peak_text.set_z_index(21)
        peak_text.move_to(DOWN * 3.55)
        fit_to_safe_width(peak_text)
        self.play(FadeIn(peak_text), run_time=0.6)
        self.wait(1.0)

        # A valley sits below the average of its neighbours, so it warms up.
        self.play(FadeOut(peak_probe), FadeOut(peak_text), run_time=0.4)
        valley_probe = probe(0.53, 0.10, WARMS_COLOR, goes_up=True)
        valley_text = Tex(r"un valle est\'a por debajo\\de sus vecinos: se calienta",
                          font_size=28, color=WARMS_COLOR)
        valley_text.set_z_index(21)
        valley_text.move_to(DOWN * 3.55)
        fit_to_safe_width(valley_text)
        self.play(FadeIn(valley_text), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(valley_probe), FadeOut(valley_text), run_time=0.4)

        # ----------------------------------------------------------- evolution
        # Now let time run: every point chasing its neighbours' average can only
        # flatten the profile, and the sharpest bump disappears first.
        insight = Tex(
            r"cada punto se acerca al\\promedio de sus vecinos",
            font_size=32,
            color=WHITE,
        )
        insight.set_z_index(21)
        insight.move_to(DOWN * 3.5)
        fit_to_safe_width(insight)
        self.play(FadeIn(insight, shift=UP * 0.15), run_time=0.7)

        curve.add_updater(
            lambda mobject: mobject.become(
                axes.plot(
                    lambda x: temperature(x, clock.get_value()),
                    x_range=[0, 1, 0.004],
                    color=CURVE_COLOR,
                ).set_stroke(width=5).set_z_index(4)
            )
        )
        bar.add_updater(paint_bar)

        self.play(clock.animate.set_value(0.55), run_time=3.0, rate_func=linear)
        self.play(clock.animate.set_value(2.4), run_time=3.0, rate_func=linear)
        self.play(clock.animate.set_value(7.0), run_time=2.6, rate_func=smooth)

        curve.clear_updaters()
        bar.clear_updaters()
        self.wait(0.6)

        # ---------------------------------------------------------- conclusion
        self.play(FadeOut(insight), run_time=0.4)
        closing = Tex(
            r"el calor solo sabe promediar",
            font_size=34,
            color=WHITE,
        )
        closing.set_z_index(21)
        closing.move_to(DOWN * 3.45)
        fit_to_safe_width(closing)
        self.play(FadeIn(closing, shift=UP * 0.15), run_time=0.7)

        result_box = SurroundingRectangle(equation, buff=0.22, corner_radius=0.12)
        result_box.set_stroke(width=4, color=[WARM_COLOR, HOT_COLOR])
        result_box.set_z_index(20)
        self.play(Create(result_box), run_time=0.7)
        self.wait(1.8)

        animate_End(scene=self)
