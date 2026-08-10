from manim import *
from lnx import *

# visual-derivation | trigonometry | advanced
# The half-angle (Weierstrass) substitution read straight off the unit circle.
#
# Let P = (cos t, sin t) on the unit circumference and let S = (-1, 0) be the
# projection pole. The chord SP meets the vertical axis x = 0 at height
#   m = sin t / (1 + cos t) = tan(t/2).
# The inscribed-angle theorem explains the halving: the central angle over the
# arc from E = (1, 0) to P equals theta, so the angle seen from S over the same
# arc is theta/2. Therefore the slope of SP is exactly tan(theta/2).
# Writing P in terms of that single parameter gives
#   sin(theta) = 2m / (1 + m^2),   cos(theta) = (1 - m^2) / (1 + m^2),
# so every rational expression in m becomes a trigonometric identity.
#
# The frame is 9 x 16 units. Safe area: |x| <= 3.8 and |y| <= 5.6.

SAFE_WIDTH = 7.2


def fit_to_safe_width(mobject):
    """Shrink a mobject so it never crosses the horizontal safe margins."""
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def make_label(tex, font_size, color, with_background=True):
    """Build a MathTex label that stays readable on top of the geometry."""
    label = MathTex(tex, font_size=font_size, color=color)
    if with_background:
        label.add_background_rectangle(color=BG, opacity=0.92, buff=0.06)
    label.set_z_index(12)
    return label


class HalfAngle(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        CIRCLE_COLOR = ACCENT_PURPLE   # the unit circumference
        RAY_COLOR = ACCENT_CYAN        # the projecting chord and the half angle
        PARAM_COLOR = ACCENT_YELLOW    # the parameter t and the projection axis
        FULL_COLOR = ACCENT_MAGENTA    # the central angle theta and its point
        AUX_COLOR = GREY_B

        # ------------------------------------------------------------ geometry
        center = np.array([0.0, 1.30, 0.0])
        R = 2.00
        theta_deg = 100.0
        t_value = np.tan(theta_deg * DEGREES / 2.0)

        def on_circle(deg):
            return center + R * np.array([
                np.cos(deg * DEGREES),
                np.sin(deg * DEGREES),
                0.0,
            ])

        E = on_circle(0.0)          # (1, 0), the reference point
        S = on_circle(180.0)        # (-1, 0), the projection pole
        P = on_circle(theta_deg)    # the moving point of the circumference
        T = center + np.array([0.0, R * t_value, 0.0])  # chord meets x = 0
        foot = np.array([P[0], center[1], 0.0])         # projection of P on the axis

        # ------------------------------------------------------------ hook 0-2s
        title = Tex(r"Ángulo mitad", font_size=62, color=WHITE)
        title.set_stroke(width=1)
        title.set_z_index(20)
        title.move_to(UP * 5.15)
        fit_to_safe_width(title)

        underline = Line(
            title.get_left() + DOWN * 0.30,
            title.get_right() + DOWN * 0.30,
            stroke_width=4,
        )
        underline.set_color(color=[ACCENT_YELLOW, ACCENT_MAGENTA])
        underline.set_z_index(20)

        circle = Circle(radius=R, color=CIRCLE_COLOR, stroke_width=5)
        circle.move_to(center)

        # The hook: the circumference and the title land together, immediately.
        self.play(
            Write(title),
            Create(circle),
            run_time=1.2,
        )
        self.play(Create(underline), run_time=0.5)

        axis_h = Line(
            center + LEFT * (R + 0.85), center + RIGHT * (R + 0.85),
            color=AUX_COLOR, stroke_width=2,
        )
        axis_v = Line(
            center + DOWN * (R + 0.55), center + UP * (R + 1.55),
            color=AUX_COLOR, stroke_width=2,
        )
        axis_h.set_stroke(opacity=0.65)
        axis_v.set_stroke(opacity=0.65)
        self.add(axis_h, axis_v)
        self.bring_to_back(axis_h, axis_v)

        # ------------------------------------------------- the point and theta
        dot_E = Dot(E, color=WHITE, radius=0.055)
        dot_P = Dot(P, color=FULL_COLOR, radius=0.075)
        radius_line = Line(center, P, color=FULL_COLOR, stroke_width=5)
        label_P = make_label(
            r"(\cos\theta,\ \sin\theta)", 28, FULL_COLOR
        ).next_to(dot_P, UP + LEFT * 0.2, buff=0.18)
        fit_to_safe_width(label_P)

        arc_theta = Angle(
            Line(center, E), Line(center, P), radius=0.60, color=FULL_COLOR,
        )
        label_theta = make_label(
            r"\theta", 32, FULL_COLOR, with_background=False
        ).move_to(
            Angle(Line(center, E), Line(center, P), radius=0.95)
            .point_from_proportion(0.5)
        )

        self.play(FadeIn(dot_E), Create(radius_line), FadeIn(dot_P), run_time=0.8)
        self.play(Create(arc_theta), Write(label_theta), run_time=0.6)
        self.play(Write(label_P), run_time=0.7)

        # The right angle that turns the coordinates into legs of a triangle.
        drop = DashedLine(P, foot, color=AUX_COLOR, stroke_width=3)
        right_angle = RightAngle(
            Line(foot, P), Line(foot, E), length=0.22, color=WHITE, stroke_width=4,
        )
        right_angle.set_z_index(8)
        self.play(Create(drop), Create(right_angle), run_time=0.6)
        self.wait(0.4)

        # --------------------------------------- stereographic projection from S
        dot_S = Dot(S, color=RAY_COLOR, radius=0.075)
        label_S = make_label(
            r"(-1,\,0)", 28, RAY_COLOR
        ).next_to(dot_S, DOWN + LEFT * 0.15, buff=0.20)
        chord = Line(S, T, color=RAY_COLOR, stroke_width=5)
        chord.set_z_index(4)

        self.play(FadeIn(dot_S), Write(label_S), run_time=0.6)
        self.play(Create(chord), run_time=1.0)

        dot_T = Dot(T, color=PARAM_COLOR, radius=0.075)
        # The length label sits outside the figure, to the right of the axis.
        label_t = make_label(r"t", 34, PARAM_COLOR, with_background=False)
        label_t.next_to(dot_T, RIGHT, buff=0.28)
        self.play(FadeIn(dot_T), Write(label_t), run_time=0.6)
        self.wait(0.8)

        # ------------------------------- inscribed angle: why theta/2 shows up
        arc_half = Angle(
            Line(S, E), Line(S, P), radius=1.15, color=RAY_COLOR,
        )
        label_half = make_label(
            r"\tfrac{\theta}{2}", 30, RAY_COLOR, with_background=False
        ).move_to(
            Angle(Line(S, E), Line(S, P), radius=1.62).point_from_proportion(0.5)
        )
        note = Tex(
            r"Ángulo inscrito: la mitad del central",
            font_size=30, color=RAY_COLOR,
        )
        note.set_z_index(20)
        note.move_to(np.array([0.0, -1.55, 0.0]))
        fit_to_safe_width(note)

        self.play(Create(arc_half), Write(label_half), run_time=0.8)
        self.play(Write(note), run_time=0.8)
        self.wait(0.6)

        definition = MathTex(
            r"t", r"=", r"\tan\!\left(\tfrac{\theta}{2}\right)",
            font_size=44,
        )
        definition[0].set_color(PARAM_COLOR)
        definition[2].set_color(RAY_COLOR)
        definition.set_stroke(width=1)
        definition.set_z_index(21)
        definition.move_to(np.array([0.0, -2.75, 0.0]))
        fit_to_safe_width(definition)

        self.play(
            TransformFromCopy(label_t, definition[0]),
            run_time=0.7,
        )
        self.play(Write(definition[1:]), run_time=0.8)
        self.wait(1.2)

        # ------------------------------------------- the substitution appears
        self.play(FadeOut(note), run_time=0.4)

        formulas = VGroup(
            MathTex(
                r"\sin\theta = \frac{2t}{1+t^{2}}", font_size=42,
            ),
            MathTex(
                r"\cos\theta = \frac{1-t^{2}}{1+t^{2}}", font_size=42,
            ),
        )
        formulas[0].set_color(FULL_COLOR)
        formulas[1].set_color(CIRCLE_COLOR)
        for formula in formulas:
            formula.set_stroke(width=1)
            formula.set_z_index(21)
        formulas.arrange(DOWN, buff=0.55)
        formulas.move_to(np.array([0.0, -4.05, 0.0]))
        fit_to_safe_width(formulas)

        self.play(
            TransformFromCopy(definition[0], formulas[0]),
            run_time=1.0,
        )
        self.play(
            TransformFromCopy(definition[0], formulas[1]),
            run_time=1.0,
        )
        self.wait(1.0)

        # The coordinates of P are now written with the single parameter t.
        self.play(
            Indicate(dot_P, color=PARAM_COLOR, scale_factor=1.6),
            Indicate(formulas, color=PARAM_COLOR, scale_factor=1.06),
            run_time=1.0,
        )
        self.wait(0.5)

        # ------------------------------------------------------------- payoff
        self.play(
            FadeOut(VGroup(
                label_P, label_S, label_theta, label_half, arc_theta, arc_half,
                drop, right_angle, radius_line,
            )),
            run_time=0.6,
        )

        payoff = Tex(
            r"Toda función racional en $t$\\es una identidad trigonométrica",
            font_size=32, color=WHITE,
        )
        payoff.set_stroke(width=1)
        payoff.set_z_index(22)
        payoff.move_to(np.array([0.0, -1.70, 0.0]))
        fit_to_safe_width(payoff)

        self.play(Write(payoff), run_time=1.2)

        result_box = SurroundingRectangle(formulas, buff=0.22, corner_radius=0.12)
        result_box.set_stroke(width=4, color=[ACCENT_YELLOW, ACCENT_MAGENTA])
        result_box.set_z_index(20)
        self.play(Create(result_box), run_time=0.8)
        self.wait(2.4)

        animate_End(scene=self)
