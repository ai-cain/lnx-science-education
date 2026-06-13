from manim import *
from lnx import *

# visual-derivation | algebra | intermediate
# Where e^{i*theta} = cos(theta) + i*sin(theta) actually comes from.
#
# The exponential is defined by ONE property: its derivative is itself times a
# constant. Put the constant equal to i and the whole formula becomes a
# statement about motion:
#
#       z(0) = 1,        dz/dt = i * z.
#
# Multiplying a complex number by i rotates it a quarter turn, so the equation
# reads "the velocity is always perpendicular to the position". A velocity that
# is always perpendicular to the radius can never change |z| (the radial
# component of the velocity is zero), and since |dz/dt| = |i||z| = |z| = 1 the
# speed is constant and equal to 1. The only motion with those two properties
# is travelling around the unit circumference at unit speed: after a time t the
# travelled arc is t, so the swept angle is exactly t radians. Reading the
# coordinates of that point gives cos t and sin t, which IS the formula.
#
# Closing beat: t = pi is half a turn, landing on -1, so e^{i*pi} = -1.
#
# The real frame is 9 x 16 units (x in [-4.5, 4.5], y in [-8, 8]).
# Safe area: |x| <= 3.8 and |y| <= 5.6.

SAFE_WIDTH = 7.2

# Scene units per unit of the complex plane. Chosen so the unit circumference
# (radius 1) plus its labels fits comfortably inside the horizontal safe area.
UNIT = 1.55

# The plane is pushed slightly below center to leave room for the title and the
# differential equation stacked on top of it.
PLANE_ORIGIN = np.array([0.0, -0.9, 0.0])


def fit_to_safe_width(mobject):
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def P(x, y):
    """Complex-plane coordinate -> scene point."""
    return PLANE_ORIGIN + np.array([x * UNIT, y * UNIT, 0.0])


def C(theta, radius=1.0):
    """Point on the circumference of given radius at angle theta."""
    return P(radius * np.cos(theta), radius * np.sin(theta))


class EulerFormula(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        POS_COLOR = ACCENT_CYAN       # the position vector z
        VEL_COLOR = ACCENT_MAGENTA    # the velocity dz/dt = i*z
        ARC_COLOR = ACCENT_YELLOW     # the travelled arc = the angle theta
        RESULT_COLOR = ACCENT_PURPLE  # the payoff

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.14
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.85)
        self.add(watermark)

        # Axes drawn by hand: only two thin lines are needed and this keeps the
        # origin exactly at PLANE_ORIGIN regardless of any Axes internals.
        x_axis = Line(P(-2.1, 0), P(2.1, 0), stroke_color=GREY_B, stroke_width=2.5)
        y_axis = Line(P(0, -1.9), P(0, 1.9), stroke_color=GREY_B, stroke_width=2.5)
        axes = VGroup(x_axis, y_axis)
        axes.set_z_index(-3)

        circumference = Circle(radius=UNIT, stroke_color=GREY_A, stroke_width=2.5)
        circumference.set_stroke(opacity=0.45)
        circumference.move_to(P(0, 0))
        circumference.set_z_index(-2)

        # ---------------------------------------------------------- hook 0-2 s
        # No preamble: the point is already orbiting with its perpendicular
        # velocity arrow attached before any text explains anything.
        theta = ValueTracker(0.0)

        def position_arrow():
            arrow = Arrow(
                P(0, 0), C(theta.get_value()), buff=0,
                color=POS_COLOR, stroke_width=7,
                max_tip_length_to_length_ratio=0.22,
            )
            arrow.set_z_index(6)
            return arrow

        def velocity_arrow():
            t = theta.get_value()
            tip = C(t)
            # dz/dt = i*z rotates z a quarter turn counter-clockwise.
            direction = np.array([-np.sin(t), np.cos(t), 0.0]) * UNIT
            arrow = Arrow(
                tip, tip + direction, buff=0,
                color=VEL_COLOR, stroke_width=7,
                max_tip_length_to_length_ratio=0.22,
            )
            arrow.set_z_index(6)
            return arrow

        z_vector = always_redraw(position_arrow)
        v_vector = always_redraw(velocity_arrow)
        moving_dot = always_redraw(
            lambda: Dot(C(theta.get_value()), radius=0.075, color=WHITE).set_z_index(8)
        )

        self.add(axes, circumference, z_vector, v_vector, moving_dot)
        self.play(theta.animate.set_value(1.7), run_time=1.4, rate_func=linear)

        title = Tex(r"La f\'ormula de Euler", font_size=58, color=WHITE)
        title.set_stroke(width=1)
        title.set_z_index(20)
        title.move_to(UP * 5.35)
        fit_to_safe_width(title)

        underline = Line(
            title.get_left() + DOWN * 0.3,
            title.get_right() + DOWN * 0.3,
            stroke_width=4,
        )
        underline.set_color(color=[ACCENT_CYAN, ACCENT_MAGENTA])
        underline.set_z_index(20)

        self.play(Write(title), run_time=0.6)
        self.play(Create(underline), run_time=0.3)
        self.play(theta.animate.set_value(3.4), run_time=1.2, rate_func=linear)

        # -------------------------------------- beat 1: the defining equation
        # The exponential is the function that is its own derivative. With the
        # constant i, the equation is the whole video.
        ode = MathTex(r"z(0)=1,\qquad \frac{dz}{dt}=i\,z", font_size=42)
        ode[0].set_color(WHITE)
        ode.set_stroke(width=1)
        ode.set_z_index(20)
        ode.move_to(UP * 4.25)
        fit_to_safe_width(ode)

        self.play(Write(ode), run_time=0.9)

        meaning = Tex(
            r"multiplicar por $i$ es\\girar un cuarto de vuelta",
            font_size=32, color=VEL_COLOR,
        )
        meaning.set_z_index(20)
        meaning.move_to(DOWN * 4.7)
        fit_to_safe_width(meaning)
        self.play(FadeIn(meaning, shift=UP * 0.15), run_time=0.5)
        self.play(theta.animate.set_value(4.9), run_time=1.1, rate_func=linear)

        # ------------------------------- beat 2: velocity perpendicular to z
        # Freeze the motion and mark the right angle: this is the geometric
        # content of dz/dt = i*z.
        frozen = 0.9
        self.play(theta.animate.set_value(2 * PI + frozen), run_time=1.3, rate_func=linear)

        z_static = position_arrow()
        v_static = velocity_arrow()
        dot_static = Dot(C(frozen), radius=0.075, color=WHITE).set_z_index(8)
        self.remove(z_vector, v_vector, moving_dot)
        self.add(z_static, v_static, dot_static)

        tip = C(frozen)
        right_angle = RightAngle(
            Line(tip, P(0, 0)),
            Line(tip, tip + np.array([-np.sin(frozen), np.cos(frozen), 0.0]) * UNIT),
            length=0.28, color=WHITE, stroke_width=4,
        )
        right_angle.set_z_index(9)

        # Length labels live outside the figure, never on top of a line.
        z_label = MathTex(r"z", font_size=34, color=POS_COLOR)
        z_label.set_z_index(20)
        z_label.move_to(C(frozen - 0.42, 0.58))
        v_label = MathTex(r"i\,z", font_size=34, color=VEL_COLOR)
        v_label.set_z_index(20)
        v_label.move_to(C(frozen + 0.62, 1.72))

        self.play(FadeOut(meaning), run_time=0.3)
        self.play(Create(right_angle), Write(z_label), Write(v_label), run_time=0.8)

        perp_text = Tex(
            r"la velocidad es siempre\\perpendicular a la posici\'on",
            font_size=32, color=WHITE,
        )
        perp_text.set_z_index(20)
        perp_text.move_to(DOWN * 4.7)
        fit_to_safe_width(perp_text)
        self.play(FadeIn(perp_text, shift=UP * 0.15), run_time=0.5)
        self.wait(1.0)

        # ------------------------------------- beat 3: the two consequences
        consequences = VGroup(
            Tex(r"nada empuja hacia afuera: $|z|=1$", font_size=30, color=POS_COLOR),
            Tex(r"rapidez constante: $|iz|=|z|=1$", font_size=30, color=VEL_COLOR),
        )
        consequences.arrange(DOWN, buff=0.3)
        consequences.set_z_index(20)
        consequences.move_to(DOWN * 4.75)
        for line in consequences:
            fit_to_safe_width(line)

        self.play(ReplacementTransform(perp_text, consequences[0]), run_time=0.7)
        self.play(FadeIn(consequences[1], shift=UP * 0.15), run_time=0.6)
        self.wait(1.0)

        # ---------------------- beat 4: constant speed on a circumference
        # Arc travelled in time t equals t, so the swept angle IS t radians.
        self.play(
            FadeOut(consequences), FadeOut(right_angle),
            FadeOut(z_label), FadeOut(v_label),
            FadeOut(z_static), FadeOut(v_static), FadeOut(dot_static),
            run_time=0.5,
        )

        theta.set_value(0.0)
        self.add(z_vector, v_vector, moving_dot)

        arc = always_redraw(
            lambda: Arc(
                radius=UNIT, start_angle=0, angle=max(theta.get_value(), 1e-3),
                arc_center=P(0, 0), stroke_color=ARC_COLOR, stroke_width=8,
            ).set_z_index(4)
        )
        self.add(arc)

        arc_text = Tex(
            r"a rapidez 1, el arco recorrido\\es $t$: el \'angulo es $t$",
            font_size=32, color=ARC_COLOR,
        )
        arc_text.set_z_index(20)
        arc_text.move_to(DOWN * 4.7)
        fit_to_safe_width(arc_text)
        self.play(FadeIn(arc_text, shift=UP * 0.15), run_time=0.5)
        self.play(theta.animate.set_value(1.15), run_time=1.4, rate_func=linear)

        # Read the coordinates of the point: that is exactly the formula.
        t0 = 1.15
        cos_line = DashedLine(
            C(t0), P(0, np.sin(t0)), color=GREY_B, stroke_width=2.5,
        )
        sin_line = DashedLine(
            C(t0), P(np.cos(t0), 0), color=GREY_B, stroke_width=2.5,
        )
        cos_label = MathTex(r"\cos t", font_size=30, color=WHITE)
        cos_label.set_z_index(20)
        cos_label.next_to(P(np.cos(t0), 0), DOWN, buff=0.28)
        sin_label = MathTex(r"\operatorname{sen} t", font_size=30, color=WHITE)
        sin_label.set_z_index(20)
        sin_label.next_to(P(0, np.sin(t0)), LEFT, buff=0.28)

        self.play(FadeOut(arc_text), run_time=0.3)
        self.play(Create(cos_line), Create(sin_line), run_time=0.6)
        self.play(Write(cos_label), Write(sin_label), run_time=0.6)
        self.wait(0.6)

        # ----------------------------------------------- beat 5: the formula
        formula = MathTex(
            r"e^{i t}", r"=", r"\cos t", r"+", r"i\operatorname{sen} t",
            font_size=46,
        )
        formula[0].set_color(POS_COLOR)
        formula[2].set_color(WHITE)
        formula[4].set_color(WHITE)
        formula.set_stroke(width=1)
        formula.set_z_index(20)
        formula.move_to(DOWN * 4.6)
        fit_to_safe_width(formula)
        self.play(Write(formula), run_time=1.0)
        self.wait(0.9)

        # ------------------------------------------- beat 6: t = pi, half turn
        self.play(
            FadeOut(cos_line), FadeOut(sin_line),
            FadeOut(cos_label), FadeOut(sin_label),
            FadeOut(ode),
            run_time=0.5,
        )

        half_turn = Tex(r"media vuelta: $t=\pi$", font_size=34, color=ARC_COLOR)
        half_turn.set_z_index(20)
        half_turn.move_to(UP * 4.35)
        fit_to_safe_width(half_turn)
        self.play(FadeIn(half_turn, shift=DOWN * 0.15), run_time=0.4)

        self.play(theta.animate.set_value(PI), run_time=1.6, rate_func=smooth)

        minus_one = Dot(P(-1, 0), radius=0.09, color=RESULT_COLOR).set_z_index(10)
        minus_label = MathTex(r"-1", font_size=34, color=RESULT_COLOR)
        minus_label.set_z_index(20)
        minus_label.next_to(P(-1, 0), DOWN, buff=0.3)
        self.play(FadeIn(minus_one, scale=0.5), Write(minus_label), run_time=0.6)

        payoff = MathTex(r"e^{i\pi}", r"=", r"-1", font_size=52)
        payoff[0].set_color(POS_COLOR)
        payoff[2].set_color(RESULT_COLOR)
        payoff.set_stroke(width=1)
        payoff.set_z_index(21)
        payoff.move_to(DOWN * 4.6)
        fit_to_safe_width(payoff)
        self.play(ReplacementTransform(formula, payoff), run_time=0.9)

        payoff_box = SurroundingRectangle(payoff, buff=0.28, corner_radius=0.14)
        payoff_box.set_stroke(width=4, color=[ACCENT_YELLOW, ACCENT_PURPLE])
        payoff_box.set_z_index(20)
        self.play(Create(payoff_box), run_time=0.6)
        self.wait(1.6)

        animate_End(scene=self)
