from manim import *
from lnx import *

# proof-without-words | trigonometry | intermediate
# Product-to-sum identity:  2 sin A cos B = sin(A+B) + sin(A-B).
#
# Visual dissection on the unit circumference. Take
#   P = (cos(A+B), sin(A+B))   and   Q = (cos(A-B), sin(A-B)).
# Their heights over the horizontal diameter are sin(A+B) and sin(A-B).
# The midpoint M of the chord PQ therefore has height
#   y_M = ( sin(A+B) + sin(A-B) ) / 2.
# But OPQ is isosceles (|OP| = |OQ| = 1) and the half angle at O is B, so OM
# bisects the angle POQ: it points along the direction A and its length is
# cos B. Hence
#   y_M = cos B * sin A
# and doubling gives 2 sin A cos B = sin(A+B) + sin(A-B).
#
# The dissection is made literal at the bottom of the frame: the two heights
# are cut from the circumference and stacked into one bar, which is then
# matched against two copies of the segment sin A cos B.
#
# The actual frame is 9 x 16 units (x in [-4.5, 4.5], y in [-8, 8]).
# Safe area: |x| <= 3.8 and |y| <= 5.6.

SAFE_WIDTH = 7.2

# Angles of the construction, in degrees.
ANGLE_A = 55.0
ANGLE_B = 25.0


def fit_to_safe_width(mobject):
    """Shrink a mobject until it fits inside the horizontal safe area."""
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def make_label(tex, font_size, color, with_background=False):
    """Create a MathTex label, optionally shielded where it crosses a line."""
    label = MathTex(tex, font_size=font_size, color=color)
    if with_background:
        label.add_background_rectangle(color=BG, opacity=0.92, buff=0.06)
    label.set_z_index(12)
    return label


class ProductToSum(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        SUM_COLOR = ACCENT_YELLOW      # height sin(A+B)
        DIFF_COLOR = ACCENT_CYAN       # height sin(A-B)
        MID_COLOR = ACCENT_MAGENTA     # the midpoint height sin A cos B
        AUX_COLOR = ACCENT_PURPLE      # radii and chord
        GUIDE_COLOR = GREY_B           # circumference and diameter

        # ------------------------------------------------------------ geometry
        center = np.array([-1.15, 1.05, 0.0])
        R = 2.25

        def on_circle(deg):
            return center + R * np.array(
                [np.cos(deg * DEGREES), np.sin(deg * DEGREES), 0.0]
            )

        def foot(point):
            """Project a point orthogonally onto the horizontal diameter."""
            return np.array([point[0], center[1], 0.0])

        P = on_circle(ANGLE_A + ANGLE_B)   # height sin(A+B)
        Q = on_circle(ANGLE_A - ANGLE_B)   # height sin(A-B)
        M = (P + Q) / 2.0                  # midpoint of the chord

        # ------------------------------------------------------- hook 0.0-2.0s
        title = Tex(r"Producto a suma", font_size=58, color=WHITE)
        title.set_stroke(width=1)
        title.set_z_index(20)
        title.move_to(UP * 5.35)
        fit_to_safe_width(title)

        underline = Line(
            title.get_left() + DOWN * 0.3,
            title.get_right() + DOWN * 0.3,
            stroke_width=4,
        )
        underline.set_color(color=[ACCENT_YELLOW, ACCENT_MAGENTA])
        underline.set_z_index(20)

        circumference = Circle(radius=R, color=GUIDE_COLOR, stroke_width=2.5)
        circumference.move_to(center)
        circumference.set_stroke(opacity=0.65)
        diameter = Line(
            center + LEFT * R, center + RIGHT * R,
            color=GUIDE_COLOR, stroke_width=2.5,
        )
        diameter.set_stroke(opacity=0.55)

        self.play(Write(title), Create(circumference), run_time=0.9)
        self.play(Create(underline), Create(diameter), run_time=0.5)

        center_dot = Dot(center, color=WHITE, radius=0.05)
        center_label = make_label("O", 28, WHITE).next_to(center_dot, DL, buff=0.1)
        self.add(center_dot, center_label)
        self.wait(0.2)

        # ------------------------------------------- the two radii and heights
        radius_p = Line(center, P, color=AUX_COLOR, stroke_width=4)
        radius_q = Line(center, Q, color=AUX_COLOR, stroke_width=4)
        dot_p = Dot(P, color=SUM_COLOR, radius=0.06)
        dot_q = Dot(Q, color=DIFF_COLOR, radius=0.06)
        self.play(
            Create(radius_p), Create(radius_q),
            FadeIn(dot_p), FadeIn(dot_q),
            run_time=0.8,
        )

        height_p = Line(foot(P), P, color=SUM_COLOR, stroke_width=6)
        height_q = Line(foot(Q), Q, color=DIFF_COLOR, stroke_width=6)
        right_p = RightAngle(
            Line(foot(P), P), Line(foot(P), center + RIGHT * R),
            length=0.2, color=WHITE, stroke_width=3,
        )
        right_q = RightAngle(
            Line(foot(Q), Q), Line(foot(Q), center + RIGHT * R),
            length=0.2, color=WHITE, stroke_width=3,
        )

        # Length labels live outside the figure, never on top of a segment.
        label_p = make_label(r"\operatorname{sen}(A+B)", 30, SUM_COLOR)
        label_p.next_to(P, UP, buff=0.22)
        label_q = make_label(r"\operatorname{sen}(A-B)", 30, DIFF_COLOR)
        label_q.next_to(Q, RIGHT, buff=0.28)

        self.play(
            Create(height_p), Create(height_q),
            Create(right_p), Create(right_q),
            run_time=0.8,
        )
        self.play(Write(label_p), Write(label_q), run_time=0.7)
        self.wait(0.3)

        # ------------------------------------------------ chord and its midpoint
        chord = Line(P, Q, color=AUX_COLOR, stroke_width=4)
        chord.set_stroke(opacity=0.9)
        dot_m = Dot(M, color=MID_COLOR, radius=0.065)
        self.play(Create(chord), FadeIn(dot_m), run_time=0.7)

        # OM bisects the angle POQ, so it points along A and measures cos B.
        bisector = Line(center, M, color=MID_COLOR, stroke_width=5)
        right_m = RightAngle(
            Line(M, center), Line(M, P),
            length=0.2, color=WHITE, stroke_width=3,
        )
        label_cosb = make_label(r"\cos B", 30, MID_COLOR, with_background=True)
        label_cosb.move_to(
            (center + M) / 2 + np.array([-0.52, -0.34, 0.0])
        )
        self.play(Create(bisector), Create(right_m), run_time=0.7)
        self.play(Write(label_cosb), run_time=0.5)

        angle_a = Angle(
            Line(center, center + RIGHT * R), Line(center, M),
            radius=0.62, color=MID_COLOR,
        )
        angle_a_label = make_label("A", 28, MID_COLOR).move_to(
            Angle(
                Line(center, center + RIGHT * R), Line(center, M), radius=0.95,
            ).point_from_proportion(0.5)
        )
        angle_b = Angle(
            Line(center, M), Line(center, P), radius=0.95, color=ACCENT_YELLOW,
        )
        angle_b_label = make_label("B", 26, ACCENT_YELLOW).move_to(
            Angle(
                Line(center, M), Line(center, P), radius=1.3,
            ).point_from_proportion(0.5)
        )
        self.play(
            Create(angle_a), Write(angle_a_label),
            Create(angle_b), Write(angle_b_label),
            run_time=0.8,
        )
        self.wait(0.4)

        # The midpoint height is the mid-segment of the trapezoid.
        height_m = Line(foot(M), M, color=MID_COLOR, stroke_width=6)
        label_m = make_label(
            r"\operatorname{sen}A\,\cos B", 30, MID_COLOR, with_background=True
        )
        label_m.next_to(foot(M), DOWN, buff=0.22)
        self.play(Create(height_m), Write(label_m), run_time=0.8)
        self.wait(0.5)

        # ---------------------------------------------------- the dissection
        # Cut the two heights out of the construction and stack them into a
        # single bar; then compare against two copies of sen A cos B.
        BAR_SCALE = 1.62
        BAR_WIDTH = 0.62
        BASE_Y = -4.85
        LEFT_X = -1.75
        RIGHT_X = 1.35

        len_sum = np.sin((ANGLE_A + ANGLE_B) * DEGREES) * BAR_SCALE
        len_diff = np.sin((ANGLE_A - ANGLE_B) * DEGREES) * BAR_SCALE
        len_mid = np.sin(ANGLE_A * DEGREES) * np.cos(ANGLE_B * DEGREES) * BAR_SCALE

        def make_bar(length, color, bottom_y, x):
            bar = Rectangle(width=BAR_WIDTH, height=length)
            bar.set_stroke(color=color, width=3)
            bar.set_fill(color=color, opacity=0.28)
            bar.move_to(np.array([x, bottom_y + length / 2.0, 0.0]))
            return bar

        bar_diff = make_bar(len_diff, DIFF_COLOR, BASE_Y, LEFT_X)
        bar_sum = make_bar(len_sum, SUM_COLOR, BASE_Y + len_diff, LEFT_X)
        bar_mid_low = make_bar(len_mid, MID_COLOR, BASE_Y, RIGHT_X)
        bar_mid_high = make_bar(len_mid, MID_COLOR, BASE_Y + len_mid, RIGHT_X)

        self.play(
            TransformFromCopy(height_q, bar_diff),
            TransformFromCopy(height_p, bar_sum),
            run_time=1.0,
        )
        self.play(
            TransformFromCopy(height_m, bar_mid_low),
            TransformFromCopy(height_m, bar_mid_high),
            run_time=0.9,
        )

        equal_sign = MathTex("=", font_size=52, color=WHITE)
        equal_sign.set_z_index(15)
        equal_sign.move_to(
            np.array([(LEFT_X + RIGHT_X) / 2.0, BASE_Y + len_mid, 0.0])
        )
        two_tag = make_label(r"\times 2", 30, MID_COLOR)
        two_tag.next_to(bar_mid_high, RIGHT, buff=0.24)
        two_tag.shift(DOWN * len_mid / 2.0)
        self.play(Write(equal_sign), Write(two_tag), run_time=0.6)
        self.wait(0.6)

        # The two stacks reach exactly the same top line.
        level = DashedLine(
            np.array([LEFT_X - 0.75, BASE_Y + 2 * len_mid, 0.0]),
            np.array([RIGHT_X + 0.95, BASE_Y + 2 * len_mid, 0.0]),
            dash_length=0.12, color=WHITE, stroke_width=3,
        )
        level.set_z_index(14)
        self.play(Create(level), run_time=0.6)
        self.wait(0.6)

        # ----------------------------------------------------------- payoff
        # Clear the construction so the identity lands on a clean field.
        construction = VGroup(
            circumference, diameter, radius_p, radius_q, chord, bisector,
            height_p, height_q, height_m, right_p, right_q, right_m,
            angle_a, angle_a_label, angle_b, angle_b_label,
            label_p, label_q, label_m, label_cosb, center_label,
        )
        self.play(
            FadeOut(construction), FadeOut(dot_p), FadeOut(dot_q),
            FadeOut(dot_m), FadeOut(center_dot),
            run_time=0.7,
        )

        formula = MathTex(
            r"2\operatorname{sen}A\,\cos B",
            r"=",
            r"\operatorname{sen}(A+B)",
            r"+",
            r"\operatorname{sen}(A-B)",
            font_size=42,
        )
        formula[0].set_color(MID_COLOR)
        formula[2].set_color(SUM_COLOR)
        formula[4].set_color(DIFF_COLOR)
        formula.set_stroke(width=1)
        formula.set_z_index(21)
        formula.move_to(UP * 1.6)
        fit_to_safe_width(formula)

        self.play(Write(formula), run_time=1.4)

        result_box = SurroundingRectangle(formula, buff=0.2, corner_radius=0.12)
        result_box.set_stroke(width=4, color=[ACCENT_MAGENTA, ACCENT_YELLOW])
        result_box.set_z_index(20)
        self.play(Create(result_box), run_time=0.7)
        self.wait(1.6)

        animate_End(scene=self)
