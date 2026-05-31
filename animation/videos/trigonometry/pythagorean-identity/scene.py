from manim import *
from lnx import *

# proof-without-words | trigonometry | basic
# Pythagorean identity:  sin^2(t) + cos^2(t) = 1.
#
# A point on the unit circumference drops a right triangle whose legs are
# exactly cos(t) and sin(t) and whose hypotenuse is the radius, 1. Pythagoras
# on that triangle *is* the identity. Sweeping the angle changes both legs but
# never the sum of their squares.
#
# The frame is 9 x 16 units (x in [-4.5, 4.5], y in [-8, 8]).
# Safe area: |x| <= 3.8 and |y| <= 5.6.

SAFE_WIDTH = 7.2

CIRCLE_CENTER = np.array([0.0, 1.75, 0.0])
RADIUS = 2.15

COS_COLOR = ACCENT_YELLOW
SIN_COLOR = ACCENT_CYAN
HYP_COLOR = ACCENT_MAGENTA
ANGLE_COLOR = ACCENT_PURPLE


def fit_to_safe_width(mobject):
    """Shrink a mobject until it fits inside the horizontal safe area."""
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def make_label(tex, font_size, color):
    """Create a MathTex label that always reads above the geometry."""
    label = MathTex(tex, font_size=font_size, color=color)
    label.set_stroke(width=1)
    label.set_z_index(20)
    return label


class PythagoreanIdentity(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        theta = ValueTracker(55 * DEGREES)

        # ------------------------------------------------------------ geometry
        def point_on_circle():
            t = theta.get_value()
            return CIRCLE_CENTER + RADIUS * np.array([np.cos(t), np.sin(t), 0.0])

        def foot_point():
            """Orthogonal projection of the moving point onto the x axis."""
            P = point_on_circle()
            return np.array([P[0], CIRCLE_CENTER[1], 0.0])

        def build_hypotenuse():
            return Line(
                CIRCLE_CENTER, point_on_circle(),
                color=HYP_COLOR, stroke_width=6,
            ).set_z_index(4)

        def build_cos_leg():
            return Line(
                CIRCLE_CENTER, foot_point(),
                color=COS_COLOR, stroke_width=7,
            ).set_z_index(5)

        def build_sin_leg():
            return Line(
                foot_point(), point_on_circle(),
                color=SIN_COLOR, stroke_width=7,
            ).set_z_index(5)

        def build_right_angle():
            return RightAngle(
                Line(foot_point(), CIRCLE_CENTER),
                Line(foot_point(), point_on_circle()),
                length=0.26, color=WHITE, stroke_width=4,
            ).set_z_index(6)

        def build_angle_arc():
            return Angle(
                Line(CIRCLE_CENTER, CIRCLE_CENTER + RIGHT),
                Line(CIRCLE_CENTER, point_on_circle()),
                radius=0.55, color=ANGLE_COLOR, stroke_width=5,
            ).set_z_index(6)

        def build_moving_dot():
            return Dot(point_on_circle(), color=WHITE, radius=0.075).set_z_index(8)

        # Length labels live outside the triangle, never on top of a segment.
        def build_cos_label():
            label = make_label(r"\cos\theta", 32, COS_COLOR)
            label.move_to((CIRCLE_CENTER + foot_point()) / 2 + DOWN * 0.42)
            return label

        def build_sin_label():
            label = make_label(r"\operatorname{sen}\theta", 32, SIN_COLOR)
            label.move_to((foot_point() + point_on_circle()) / 2 + RIGHT * 0.62)
            return label

        def build_hyp_label():
            P = point_on_circle()
            direction = P - CIRCLE_CENTER
            normal = normalize(np.array([-direction[1], direction[0], 0.0]))
            label = make_label("1", 34, HYP_COLOR)
            label.move_to((CIRCLE_CENTER + P) / 2 + normal * 0.38)
            return label

        def build_theta_label():
            label = make_label(r"\theta", 30, ANGLE_COLOR)
            label.move_to(
                Angle(
                    Line(CIRCLE_CENTER, CIRCLE_CENTER + RIGHT),
                    Line(CIRCLE_CENTER, point_on_circle()),
                    radius=0.92,
                ).point_from_proportion(0.5)
            )
            return label

        # -------------------------------------------------------- hook 0-2s
        # The circumference and the point that will carry the whole proof.
        circumference = Circle(radius=RADIUS, color=GREY_B, stroke_width=3)
        circumference.move_to(CIRCLE_CENTER)
        circumference.set_stroke(opacity=0.8)
        center_dot = Dot(CIRCLE_CENTER, color=GREY_B, radius=0.05)

        static_dot = build_moving_dot()
        self.play(Create(circumference), run_time=0.9)
        self.play(FadeIn(static_dot, scale=2.2), FadeIn(center_dot), run_time=0.5)

        title = Tex(r"Radio 1, siempre", font_size=56, color=WHITE)
        title.set_stroke(width=1)
        title.set_z_index(25)
        title.move_to(UP * 5.3)
        fit_to_safe_width(title)
        self.play(Write(title), run_time=0.7)
        self.wait(0.2)

        # --------------------------------------------------- the right triangle
        static_hyp = build_hypotenuse()
        static_hyp_label = build_hyp_label()
        static_arc = build_angle_arc()
        static_theta_label = build_theta_label()
        self.play(Create(static_hyp), Write(static_hyp_label), run_time=0.8)
        self.play(Create(static_arc), Write(static_theta_label), run_time=0.6)

        static_cos = build_cos_leg()
        static_cos_label = build_cos_label()
        self.play(Create(static_cos), Write(static_cos_label), run_time=0.8)

        static_sin = build_sin_leg()
        static_sin_label = build_sin_label()
        self.play(Create(static_sin), Write(static_sin_label), run_time=0.8)

        static_right = build_right_angle()
        self.play(Create(static_right), run_time=0.5)
        self.wait(0.9)

        # ------------------------------------------------------------- Pythagoras
        pythagoras = MathTex(
            r"\operatorname{sen}^2\theta", r"+", r"\cos^2\theta", r"=", r"1^2",
            font_size=46,
        )
        pythagoras[0].set_color(SIN_COLOR)
        pythagoras[2].set_color(COS_COLOR)
        pythagoras[4].set_color(HYP_COLOR)
        pythagoras.set_stroke(width=1)
        pythagoras.set_z_index(25)
        pythagoras.move_to(DOWN * 2.6)
        fit_to_safe_width(pythagoras)

        # Each term flies out of the segment it measures.
        self.play(
            TransformFromCopy(static_sin_label, pythagoras[0]),
            TransformFromCopy(static_cos_label, pythagoras[2]),
            run_time=1.0,
        )
        self.play(
            Write(pythagoras[1]), Write(pythagoras[3]),
            TransformFromCopy(static_hyp_label, pythagoras[4]),
            run_time=0.8,
        )
        self.wait(0.6)

        # ---------------------------------------------------- live numeric proof
        readout_font = 34

        def make_row(tex, color, value_func, y):
            symbol = MathTex(tex, font_size=readout_font, color=color)
            number = DecimalNumber(
                value_func(), num_decimal_places=2,
                font_size=readout_font, color=color,
            )
            number.add_updater(lambda m: m.set_value(value_func()))
            row = VGroup(symbol, number).arrange(RIGHT, buff=0.22)
            row.set_stroke(width=1)
            row.set_z_index(25)
            row.move_to(np.array([0.0, y, 0.0]))
            return row

        row_sin = make_row(
            r"\operatorname{sen}^2\theta =", SIN_COLOR,
            lambda: np.sin(theta.get_value()) ** 2, -3.9,
        )
        row_cos = make_row(
            r"\cos^2\theta =", COS_COLOR,
            lambda: np.cos(theta.get_value()) ** 2, -4.6,
        )
        row_sum = make_row(
            r"\text{suma} =", HYP_COLOR,
            lambda: 1.0, -5.3,
        )
        readout = VGroup(row_sin, row_cos, row_sum)
        self.play(FadeIn(readout, shift=UP * 0.25), run_time=0.8)
        self.wait(0.8)

        # Swap the static construction for a version bound to the tracker.
        dynamic = VGroup(
            always_redraw(build_hypotenuse),
            always_redraw(build_cos_leg),
            always_redraw(build_sin_leg),
            always_redraw(build_right_angle),
            always_redraw(build_angle_arc),
            always_redraw(build_moving_dot),
            always_redraw(build_cos_label),
            always_redraw(build_sin_label),
            always_redraw(build_hyp_label),
            always_redraw(build_theta_label),
        )
        self.remove(
            static_hyp, static_cos, static_sin, static_right, static_arc,
            static_dot, static_cos_label, static_sin_label, static_hyp_label,
            static_theta_label,
        )
        self.add(dynamic)

        moving_title = Tex(r"Mueve el ángulo", font_size=48, color=WHITE)
        moving_title.set_stroke(width=1)
        moving_title.set_z_index(25)
        moving_title.move_to(title)
        fit_to_safe_width(moving_title)
        self.play(Transform(title, moving_title), run_time=0.6)

        # The legs stretch and shrink; the sum of their squares does not move.
        self.play(theta.animate.set_value(22 * DEGREES), run_time=2.4)
        self.wait(0.5)
        self.play(theta.animate.set_value(72 * DEGREES), run_time=2.8)
        self.wait(0.5)
        self.play(theta.animate.set_value(40 * DEGREES), run_time=2.0)
        self.wait(0.6)

        self.play(
            Indicate(row_sum, color=ACCENT_YELLOW, scale_factor=1.2),
            run_time=1.0,
        )
        self.wait(0.5)

        # ------------------------------------------------------------- payoff
        identity = MathTex(
            r"\operatorname{sen}^2\theta", r"+", r"\cos^2\theta", r"=", r"1",
            font_size=52,
        )
        identity[0].set_color(SIN_COLOR)
        identity[2].set_color(COS_COLOR)
        identity[4].set_color(HYP_COLOR)
        identity.set_stroke(width=1)
        identity.set_z_index(26)
        identity.move_to(DOWN * 2.6)
        fit_to_safe_width(identity)

        # Freeze the live numbers before they leave the screen.
        for row in readout:
            row[1].clear_updaters()

        self.play(
            FadeOut(readout, shift=DOWN * 0.3),
            TransformMatchingTex(pythagoras, identity),
            run_time=1.2,
        )

        result_box = SurroundingRectangle(identity, buff=0.2, corner_radius=0.12)
        result_box.set_stroke(width=4, color=[ACCENT_CYAN, ACCENT_MAGENTA])
        result_box.set_z_index(25)
        self.play(Create(result_box), run_time=0.7)
        self.wait(1.6)

        animate_End(scene=self)
