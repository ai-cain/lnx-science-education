from manim import *
from lnx import *

# visual-derivation | trigonometry | basic
# Area of a triangle:  S = 1/2 * a * b * sin(C).
#
# Start from the school formula 1/2 * base * height, show that the height
# dropped from A onto the base a equals b * sin(C), and substitute. Then sweep
# the angle C: the area grows up to C = 90 degrees and shrinks afterwards, so
# the right angle is the maximum. That is the hook.
#
# The real frame is 9 x 16 units (x in [-4.5, 4.5], y in [-8, 8]).
# Safe area: |x| <= 3.8 and |y| <= 5.6.

SAFE_WIDTH = 7.2

# Fixed sides of the triangle; only the angle between them changes.
A_LEN = 4.0
B_LEN = 2.6
MAX_AREA = 0.5 * A_LEN * B_LEN

VERTEX_C = np.array([-1.9, -1.7, 0.0])
VERTEX_B = VERTEX_C + np.array([A_LEN, 0.0, 0.0])

# Angle sweep limits, chosen so the foot of the altitude never leaves the
# safe area even when the triangle becomes obtuse.
THETA_START = 38 * DEGREES
THETA_MAX = 90 * DEGREES
THETA_END = 120 * DEGREES

BAR_LEFT = -2.7
BAR_WIDTH = 5.4
BAR_Y = -3.55
BAR_HEIGHT = 0.34

SIDE_A_COLOR = ACCENT_CYAN
SIDE_B_COLOR = ACCENT_MAGENTA
HEIGHT_COLOR = ACCENT_YELLOW
TRI_COLOR = ACCENT_PURPLE


def fit_to_safe_width(mobject):
    """Shrink a mobject so it never crosses the horizontal safe margins."""
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def boxed_label(tex, font_size, color, with_background=True):
    """MathTex label kept above the geometry, optionally on a solid BG patch."""
    label = MathTex(tex, font_size=font_size, color=color)
    if with_background:
        label.add_background_rectangle(color=BG, opacity=0.92, buff=0.06)
    label.set_z_index(12)
    return label


class TriangleAreaSine(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        theta = ValueTracker(THETA_START)

        def apex():
            angle = theta.get_value()
            return VERTEX_C + B_LEN * np.array(
                [np.cos(angle), np.sin(angle), 0.0]
            )

        def foot():
            """Foot of the altitude dropped from A onto the base line."""
            point = apex()
            return np.array([point[0], VERTEX_C[1], 0.0])

        def area_value():
            return 0.5 * A_LEN * B_LEN * np.sin(theta.get_value())

        # ------------------------------------------------------------ hook 0-2s
        title = Tex(r"¿Cuándo es máxima el área?", font_size=52, color=WHITE)
        title.set_stroke(width=1)
        title.set_z_index(20)
        title.move_to(UP * 5.15)
        fit_to_safe_width(title)

        underline = Line(
            title.get_left() + DOWN * 0.30,
            title.get_right() + DOWN * 0.30,
            stroke_width=4,
        )
        underline.set_color(color=GRADIENT_MAIN)
        underline.set_z_index(20)

        triangle = always_redraw(
            lambda: Polygon(
                VERTEX_C, VERTEX_B, apex(),
                stroke_width=0,
                fill_color=TRI_COLOR,
                fill_opacity=0.28,
            )
        )
        side_a = Line(VERTEX_C, VERTEX_B, color=SIDE_A_COLOR, stroke_width=6)
        side_a.set_z_index(4)
        side_b = always_redraw(
            lambda: Line(
                VERTEX_C, apex(), color=SIDE_B_COLOR, stroke_width=6
            ).set_z_index(4)
        )
        side_c = always_redraw(
            lambda: Line(
                apex(), VERTEX_B, color=TRI_COLOR, stroke_width=5
            ).set_z_index(3)
        )

        self.play(
            Write(title),
            FadeIn(triangle, scale=0.85),
            run_time=1.1,
        )
        self.play(Create(underline), Create(side_a), run_time=0.7)

        # ------------------------------------------------------ labelled sides
        self.play(Create(side_b), Create(side_c), run_time=0.7)

        vertex_dots = VGroup(
            Dot(VERTEX_C, color=WHITE, radius=0.06),
            Dot(VERTEX_B, color=WHITE, radius=0.06),
            always_redraw(lambda: Dot(apex(), color=WHITE, radius=0.06)),
        )
        vertex_names = VGroup(
            boxed_label("C", 30, WHITE, False).move_to(
                VERTEX_C + LEFT * 0.34 + DOWN * 0.30
            ),
            boxed_label("B", 30, WHITE, False).move_to(
                VERTEX_B + RIGHT * 0.34 + DOWN * 0.30
            ),
            always_redraw(
                lambda: boxed_label("A", 30, WHITE, False).move_to(
                    apex() + normalize(apex() - VERTEX_B) * 0.36 + UP * 0.16
                )
            ),
        )

        # Length labels live outside the figure, never on top of a segment.
        label_a = boxed_label("a", 34, SIDE_A_COLOR, False).move_to(
            (VERTEX_C + VERTEX_B) / 2 + DOWN * 0.42
        )
        label_b = always_redraw(
            lambda: boxed_label("b", 34, SIDE_B_COLOR, False).move_to(
                (VERTEX_C + apex()) / 2
                + normalize(
                    np.array(
                        [
                            -(apex() - VERTEX_C)[1],
                            (apex() - VERTEX_C)[0],
                            0.0,
                        ]
                    )
                )
                * -0.42
            )
        )

        angle_arc = always_redraw(
            lambda: Angle(
                Line(VERTEX_C, VERTEX_B),
                Line(VERTEX_C, apex()),
                radius=0.55,
                color=HEIGHT_COLOR,
                stroke_width=5,
            ).set_z_index(6)
        )
        angle_name = always_redraw(
            lambda: boxed_label("C", 28, HEIGHT_COLOR, False).move_to(
                Angle(
                    Line(VERTEX_C, VERTEX_B),
                    Line(VERTEX_C, apex()),
                    radius=0.92,
                ).point_from_proportion(0.5)
            )
        )

        self.play(
            FadeIn(vertex_dots), Write(vertex_names),
            Write(label_a), Write(label_b),
            run_time=0.8,
        )
        self.play(Create(angle_arc), Write(angle_name), run_time=0.6)
        self.wait(0.3)

        # -------------------------------------------------- school formula beat
        formula_school = MathTex(
            r"S", r"=", r"\tfrac{1}{2}", r"\cdot", r"a", r"\cdot", r"h",
            font_size=46,
        )
        formula_school[4].set_color(SIDE_A_COLOR)
        formula_school[6].set_color(HEIGHT_COLOR)
        formula_school.set_stroke(width=1)
        formula_school.set_z_index(21)
        formula_school.move_to(UP * 3.75)
        fit_to_safe_width(formula_school)

        self.play(Write(formula_school), run_time=0.9)

        # The altitude and its right angle: this is the "height" of the formula.
        altitude = always_redraw(
            lambda: DashedLine(
                foot(), apex(),
                color=HEIGHT_COLOR, stroke_width=5, dash_length=0.14,
            ).set_z_index(5)
        )
        base_extension = always_redraw(
            lambda: Line(
                VERTEX_C, foot() + LEFT * 0.25,
                color=SIDE_A_COLOR, stroke_width=3,
            ).set_stroke(opacity=0.45 if foot()[0] < VERTEX_C[0] else 0.0)
        )
        right_angle = always_redraw(
            lambda: RightAngle(
                Line(foot(), VERTEX_B),
                Line(foot(), apex()),
                length=0.26,
                color=WHITE,
                stroke_width=4,
            ).set_z_index(7)
        )
        label_h = always_redraw(
            lambda: boxed_label("h", 34, HEIGHT_COLOR).move_to(
                (foot() + apex()) / 2
                + RIGHT * (0.42 if foot()[0] >= VERTEX_C[0] else -0.42)
            )
        )

        self.play(Create(base_extension), Create(altitude), run_time=0.7)
        self.play(Create(right_angle), Write(label_h), run_time=0.6)
        self.wait(0.4)

        # ------------------------------------------- the height is b * sin(C)
        formula_height = MathTex(
            r"h", r"=", r"b", r"\,\operatorname{sen} C",
            font_size=46,
        )
        formula_height[0].set_color(HEIGHT_COLOR)
        formula_height[2].set_color(SIDE_B_COLOR)
        formula_height[3].set_color(HEIGHT_COLOR)
        formula_height.set_stroke(width=1)
        formula_height.set_z_index(21)
        formula_height.move_to(UP * 2.85)
        fit_to_safe_width(formula_height)

        self.play(
            Indicate(label_h, color=HEIGHT_COLOR, scale_factor=1.35),
            run_time=0.6,
        )
        self.play(Write(formula_height), run_time=0.9)
        self.wait(0.5)

        # ------------------------------------------------------- substitution
        formula_final = MathTex(
            r"S", r"=", r"\tfrac{1}{2}", r"\cdot", r"a", r"\cdot", r"b",
            r"\,\operatorname{sen} C",
            font_size=48,
        )
        formula_final[4].set_color(SIDE_A_COLOR)
        formula_final[6].set_color(SIDE_B_COLOR)
        formula_final[7].set_color(HEIGHT_COLOR)
        formula_final.set_stroke(width=1)
        formula_final.set_z_index(21)
        formula_final.move_to(UP * 3.75)
        fit_to_safe_width(formula_final)

        self.play(
            TransformMatchingTex(formula_school, formula_final),
            formula_height.animate.set_opacity(0.45),
            run_time=1.2,
        )
        self.play(FadeOut(formula_height, shift=UP * 0.3), run_time=0.5)
        self.wait(0.3)

        # ------------------------------------------------- live area readout
        angle_readout = always_redraw(
            lambda: VGroup(
                MathTex(r"C =", font_size=34, color=HEIGHT_COLOR),
                DecimalNumber(
                    theta.get_value() / DEGREES,
                    num_decimal_places=0,
                    unit=r"^\circ",
                    font_size=34,
                    color=HEIGHT_COLOR,
                ),
            )
            .arrange(RIGHT, buff=0.16)
            .move_to(np.array([0.0, -2.72, 0.0]))
            .set_z_index(21)
        )

        bar_track = RoundedRectangle(
            width=BAR_WIDTH, height=BAR_HEIGHT, corner_radius=0.10,
            stroke_color=SURFACE, stroke_width=3,
            fill_color=SURFACE, fill_opacity=1.0,
        )
        bar_track.move_to(np.array([BAR_LEFT + BAR_WIDTH / 2, BAR_Y, 0.0]))
        bar_track.set_z_index(8)

        def make_bar():
            width = max(BAR_WIDTH * area_value() / MAX_AREA, 0.01)
            bar = Rectangle(
                width=width, height=BAR_HEIGHT - 0.08,
                stroke_width=0, fill_opacity=1.0,
            )
            bar.set_fill(color=GRADIENT_MAIN)
            bar.move_to(np.array([BAR_LEFT, BAR_Y, 0.0]), aligned_edge=LEFT)
            bar.set_z_index(9)
            return bar

        bar_fill = always_redraw(make_bar)

        area_readout = always_redraw(
            lambda: VGroup(
                MathTex(r"S =", font_size=36, color=WHITE),
                DecimalNumber(
                    area_value(),
                    num_decimal_places=2,
                    font_size=36,
                    color=WHITE,
                ),
            )
            .arrange(RIGHT, buff=0.16)
            .move_to(np.array([0.0, -4.35, 0.0]))
            .set_z_index(21)
        )

        self.play(
            FadeIn(angle_readout), FadeIn(bar_track),
            FadeIn(bar_fill), FadeIn(area_readout),
            run_time=0.8,
        )
        self.wait(0.3)

        # --------------------------------------- sweep: grow up to 90, then fall
        self.play(
            theta.animate.set_value(THETA_MAX),
            run_time=2.6,
            rate_func=rate_functions.ease_in_out_sine,
        )

        peak_note = Tex(r"área máxima", font_size=34, color=ACCENT_YELLOW)
        peak_note.set_z_index(21)
        peak_note.next_to(bar_track, UP, buff=0.28)

        self.play(
            Flash(bar_fill.get_right(), color=ACCENT_YELLOW, line_length=0.25),
            FadeIn(peak_note, shift=UP * 0.2),
            run_time=0.8,
        )
        self.wait(0.5)

        self.play(FadeOut(peak_note), run_time=0.3)
        self.play(
            theta.animate.set_value(THETA_END),
            run_time=1.8,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.play(
            theta.animate.set_value(THETA_MAX),
            run_time=1.6,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.wait(0.4)

        # ------------------------------------------------------------- payoff
        payoff = Tex(
            r"El área es máxima cuando $C = 90^\circ$",
            font_size=36, color=WHITE,
        )
        payoff.set_z_index(21)
        payoff.move_to(np.array([0.0, -5.05, 0.0]))
        fit_to_safe_width(payoff)

        result_box = SurroundingRectangle(
            formula_final, buff=0.20, corner_radius=0.12
        )
        result_box.set_stroke(width=4, color=GRADIENT_HIGHLIGHT)
        result_box.set_z_index(20)

        self.play(Create(result_box), Write(payoff), run_time=1.1)
        self.wait(1.6)

        animate_End(scene=self)
