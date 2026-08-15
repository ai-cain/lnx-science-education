from pathlib import Path

import scipy.optimize

from manim import *
from lnx import *

# visual-derivation | calculus | intermediate
# Why your coffee cools down, using REAL measured data instead of a simulation.
#
# Data source:
#   "Project 1: Measuring Temperature & Newton's Law of Cooling - Coffee
#   Experiment Data", University of Manitoba course materials.
#   https://server.math.umanitoba.ca/~coopers5/pastcourses_unl_materials/project1_coffee_data.pdf
#   13 readings of a real cup of coffee over 48 minutes, room measured at 71 F.
#   Verbatim values live in data.csv next to this file.
#
# The mug on the left is driven by those readings, and the graph on the right
# pops in one dot per measurement as simulated time advances.
#
# The payoff: fitting T(t) = T_amb + dT * exp(-lambda t) to the measurements
# gives R^2 = 0.99, and that exponential is not a coincidence. It is what the
# heat equation predicts once the slowest mode dominates.
#
# The actual frame is 9 x 16 units (x in [-4.5, 4.5], y in [-8, 8]).
# Safe area: |y| <= 5.6 and |x| <= 3.8.

SAFE_WIDTH = 7.2

# ------------------------------------------------------------- measured data
DATA_FILE = Path(__file__).with_name("data.csv")
_rows = [
    line.split(",")
    for line in DATA_FILE.read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.startswith("#") and not line.startswith("t_min")
]
DATA_T = np.array([float(row[0]) for row in _rows])
DATA_C = np.array([float(row[2]) for row in _rows])

T_ENV = (71.0 - 32.0) * 5.0 / 9.0    # room temperature actually measured
T_MAX = float(DATA_T[-1])            # 48 minutes of recording

# Least squares on the measured points, keeping the measured ambient fixed.
# Fitting the temperatures directly rather than their logarithm: taking logs
# first silently reweights the cold tail and costs about 1.5 C of accuracy in
# the first minutes, which is exactly where the curve is most visible.
# Letting the ambient float fits better numerically but lands on 34.6 C, which
# is physically impossible for a room, so the two-parameter fit is the honest
# one and it is the one used here.
def _model(t, delta, decay):
    return T_ENV + delta * np.exp(-decay * t)


_params, _ = scipy.optimize.curve_fit(
    _model, DATA_T, DATA_C, p0=[DATA_C[0] - T_ENV, 0.03]
)
DELTA_T = float(_params[0])
DECAY = float(_params[1])

_residuals = DATA_C - _model(DATA_T, DELTA_T, DECAY)
R_SQUARED = float(
    1 - np.sum(_residuals**2) / np.sum((DATA_C - DATA_C.mean()) ** 2)
)


def fitted_temperature(t):
    return T_ENV + DELTA_T * np.exp(-DECAY * t)


def measured_temperature(t):
    """Linear interpolation between the readings that were actually taken."""
    return float(np.interp(t, DATA_T, DATA_C))


def heat_level(t):
    """How hot the coffee still is, normalised to [0, 1]."""
    return (measured_temperature(t) - T_ENV) / (DATA_C[0] - T_ENV)


def fit_to_safe_width(mobject):
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


class CoffeeCooling(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.14
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.85)
        self.add(watermark)

        COLD_COLOR = ManimColor(ACCENT_CYAN)
        WARM_COLOR = ManimColor(ACCENT_YELLOW)
        HOT_COLOR = ManimColor("#FF8A00")
        DATA_COLOR = ManimColor(ACCENT_CYAN)
        CURVE_COLOR = ManimColor(ACCENT_YELLOW)
        AUX_COLOR = GREY_B
        MUG_COLOR = GREY_A

        # Diverging ramp through a neutral middle. Going straight from cyan to
        # yellow would pass through green, and green coffee looks broken.
        _cold = np.array(COLD_COLOR.to_rgb())
        _mid = np.array(ManimColor("#F4EDE4").to_rgb())
        _hot = np.array(HOT_COLOR.to_rgb())

        def temp_color(level):
            level = float(np.clip(level, 0.0, 1.0))
            if level < 0.5:
                rgb = _cold + (_mid - _cold) * (level / 0.5)
            else:
                rgb = _mid + (_hot - _mid) * ((level - 0.5) / 0.5)
            return ManimColor(rgb)

        clock = ValueTracker(0.0)   # simulated minutes
        swirl = ValueTracker(0.0)   # drives the steam ribbons

        # ------------------------------------------------------------ hook 0-3s
        title = Tex(
            r"\textquestiondown Por qu\'e se enfr\'ia tu caf\'e?",
            font_size=54, color=WHITE,
        )
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

        self.play(Write(title), run_time=0.9)
        self.play(Create(underline), run_time=0.5)

        # ---------------------------------------------------------- the mug
        mug_center = np.array([-2.95, 2.35, 0.0])
        body_top = 0.72
        body_bottom = -0.72

        body = Polygon(
            mug_center + np.array([-0.7, body_top, 0]),
            mug_center + np.array([0.7, body_top, 0]),
            mug_center + np.array([0.55, body_bottom, 0]),
            mug_center + np.array([-0.55, body_bottom, 0]),
            color=MUG_COLOR,
            stroke_width=4,
        )
        body.round_corners(radius=0.13)
        body.set_fill(SURFACE, opacity=1.0)
        body.set_z_index(2)

        handle = Arc(
            radius=0.35, start_angle=-PI / 2, angle=PI,
            color=MUG_COLOR, stroke_width=7,
        )
        handle.move_to(mug_center + np.array([0.84, 0.07, 0]))
        handle.set_z_index(1)

        saucer = Ellipse(width=1.86, height=0.26, color=MUG_COLOR, stroke_width=4)
        saucer.set_fill(SURFACE, opacity=1.0)
        saucer.move_to(mug_center + np.array([0.0, body_bottom - 0.14, 0]))
        saucer.set_z_index(1)

        surface_center = mug_center + np.array([0.0, body_top, 0])
        liquid = Ellipse(width=1.3, height=0.32)
        liquid.set_stroke(width=0)
        liquid.move_to(surface_center)
        liquid.set_z_index(3)

        rim = Ellipse(width=1.4, height=0.36, color=MUG_COLOR, stroke_width=4)
        rim.move_to(surface_center)
        rim.set_z_index(4)

        def paint_liquid(mobject):
            mobject.set_fill(temp_color(heat_level(clock.get_value())), opacity=1.0)

        paint_liquid(liquid)

        mug = VGroup(saucer, handle, body, liquid, rim)
        self.play(FadeIn(mug, shift=UP * 0.2), run_time=1.0)

        # ----------------------------------------------------------- the steam
        # Ribbons that shorten and fade as the coffee gives up its heat.
        def build_steam():
            level = heat_level(clock.get_value())
            ribbons = VGroup()
            if level < 0.05:
                return ribbons
            length = 0.4 + 1.3 * level
            for index, dx in enumerate((-0.4, 0.0, 0.4)):
                phase = swirl.get_value() + index * 2.1

                def shape(s, dx=dx, phase=phase, length=length):
                    return surface_center + np.array([
                        dx + 0.16 * np.sin(3.2 * s + phase) * (0.35 + s / length),
                        0.11 + s,
                        0.0,
                    ])

                ribbon = ParametricFunction(
                    shape, t_range=[0, length, 0.02], stroke_width=5,
                )
                ribbon.set_stroke(color=WHITE, opacity=0.10 + 0.45 * level)
                ribbon.set_z_index(5)
                ribbons.add(ribbon)
            return ribbons

        steam = always_redraw(build_steam)
        swirl.add_updater(lambda m, dt: m.increment_value(dt * 2.4))
        self.add(swirl, steam)
        self.wait(0.8)

        # ----------------------------------------------------------- the graph
        axes = Axes(
            x_range=[0, T_MAX + 3, 10],
            y_range=[T_ENV - 8, DATA_C[0] + 8, 20],
            x_length=4.4,
            y_length=3.0,
            tips=False,
            axis_config={
                "stroke_color": AUX_COLOR,
                "stroke_width": 2,
                "include_ticks": False,
            },
        )
        axes.move_to(np.array([1.5, 2.2, 0.0]))
        axes.set_z_index(1)

        x_title = Tex(r"tiempo (min)", font_size=24, color=AUX_COLOR)
        x_title.next_to(axes, DOWN, buff=0.14)
        y_title = Tex(r"temperatura ($^\circ$C)", font_size=22, color=AUX_COLOR)
        y_title.rotate(PI / 2).next_to(axes, LEFT, buff=0.12)

        ambient = DashedLine(
            axes.c2p(0, T_ENV), axes.c2p(T_MAX + 3, T_ENV),
            color=COLD_COLOR, stroke_width=2.5, dash_length=0.07,
        )
        ambient.set_stroke(opacity=0.65)
        ambient_tag = Tex(r"ambiente", font_size=20, color=COLD_COLOR)
        ambient_tag.next_to(ambient, UP, buff=0.05).shift(RIGHT * 0.45)

        self.play(Create(axes), Write(x_title), Write(y_title), run_time=0.9)
        self.play(Create(ambient), FadeIn(ambient_tag), run_time=0.5)

        # Every dot is one real reading, revealed when its minute is reached.
        readings = VGroup(
            *[
                Dot(axes.c2p(t, temp), color=DATA_COLOR, radius=0.075)
                for t, temp in zip(DATA_T, DATA_C)
            ]
        )
        readings.set_z_index(7)
        for dot in readings:
            dot.set_opacity(0)

        def reveal_readings(group):
            now = clock.get_value()
            for dot, t in zip(group, DATA_T):
                dot.set_opacity(1.0 if now >= t - 1e-6 else 0.0)

        readings.add_updater(reveal_readings)
        self.add(readings)
        liquid.add_updater(paint_liquid)

        # ------------------------------------------------------- live readouts
        minutes = DecimalNumber(0, num_decimal_places=0, font_size=32, color=WHITE)
        minutes.add_updater(lambda m: m.set_value(clock.get_value()))
        minutes_tag = Tex(r"min", font_size=28, color=GREY_B)
        degrees = DecimalNumber(
            DATA_C[0], num_decimal_places=0, font_size=32, color=HOT_COLOR
        )

        def refresh_degrees(mobject):
            mobject.set_value(measured_temperature(clock.get_value()))
            mobject.set_color(temp_color(heat_level(clock.get_value())))

        degrees.add_updater(refresh_degrees)
        degrees_tag = Tex(r"$^\circ$C", font_size=28, color=GREY_B)

        readout = VGroup(minutes, minutes_tag, degrees, degrees_tag)
        readout.arrange(RIGHT, buff=0.16)
        readout.move_to(np.array([0.0, -0.3, 0.0]))
        readout.set_z_index(20)
        self.play(FadeIn(readout), run_time=0.5)

        source_note = Tex(
            r"13 mediciones reales de una taza de caf\'e",
            font_size=24, color=GREY_B,
        )
        source_note.move_to(DOWN * 1.05)
        source_note.set_z_index(20)
        fit_to_safe_width(source_note)
        self.play(FadeIn(source_note), run_time=0.5)

        # ------------------------------------------------- fast-forward cooling
        # The first minutes carry most of the drop, so they get more screen time.
        self.play(clock.animate.set_value(8.0), run_time=3.0, rate_func=linear)
        self.play(clock.animate.set_value(23.0), run_time=2.4, rate_func=linear)
        self.play(clock.animate.set_value(T_MAX), run_time=2.4, rate_func=linear)
        self.wait(0.8)

        readings.clear_updaters()
        liquid.clear_updaters()
        minutes.clear_updaters()
        degrees.clear_updaters()

        # ------------------------------------------------------------- the fit
        fit_curve = axes.plot(
            fitted_temperature, x_range=[0, T_MAX, 0.2], color=CURVE_COLOR,
        )
        fit_curve.set_stroke(width=5)
        fit_curve.set_z_index(5)
        self.play(Create(fit_curve), run_time=1.4)

        quality = MathTex(
            rf"R^2 = {R_SQUARED:.2f}", font_size=30, color=CURVE_COLOR
        )
        quality.set_z_index(21)
        quality.next_to(axes, DOWN, buff=0.14).shift(DOWN * 0.34)
        self.play(FadeOut(x_title), FadeIn(quality), run_time=0.5)
        self.wait(0.6)

        law = MathTex(
            r"T(t)", r"=", r"T_{\text{amb}}", r"+", r"\Delta T\,", r"e^{-\lambda t}",
            font_size=40,
        )
        law[0].set_color(CURVE_COLOR)
        law[2].set_color(COLD_COLOR)
        law[5].set_color(HOT_COLOR)
        law.set_stroke(width=1)
        law.set_z_index(21)
        law.move_to(DOWN * 2.3)
        fit_to_safe_width(law)
        self.play(
            FadeOut(source_note),
            FadeIn(law, shift=UP * 0.15),
            run_time=0.9,
        )
        self.wait(0.8)

        # ---------------------------------------------------------- the reason
        bridge = Tex(
            r"y esa exponencial no es casualidad",
            font_size=28, color=GREY_A,
        )
        bridge.set_z_index(21)
        bridge.move_to(DOWN * 3.3)
        fit_to_safe_width(bridge)
        self.play(FadeIn(bridge), run_time=0.7)

        equation = MathTex(
            r"\frac{\partial u}{\partial t}", r"=", r"\alpha",
            r"\frac{\partial^2 u}{\partial x^2}",
            font_size=48,
        )
        equation[0].set_color(HOT_COLOR)
        equation[3].set_color(CURVE_COLOR)
        equation.set_stroke(width=1)
        equation.set_z_index(21)
        equation.move_to(DOWN * 4.45)
        fit_to_safe_width(equation)
        self.play(Write(equation), run_time=1.0)

        caption = Tex(r"la ecuaci\'on del calor", font_size=26, color=GREY_B)
        caption.set_z_index(21)
        caption.next_to(equation, DOWN, buff=0.46)
        self.play(FadeIn(caption), run_time=0.5)
        self.wait(0.5)

        result_box = SurroundingRectangle(equation, buff=0.2, corner_radius=0.12)
        result_box.set_stroke(width=4, color=[WARM_COLOR, HOT_COLOR])
        result_box.set_z_index(20)
        self.play(Create(result_box), run_time=0.7)
        self.wait(1.6)

        swirl.clear_updaters()
        animate_End(scene=self)
