from manim import *
from lnx import *

# proof-without-words | trigonometry | intermediate-advanced
# Law of Sines:  a/sin A = b/sin B = c/sin C = 2R.
#
# The "pro" proof almost nobody sees in school. Instead of dropping altitudes,
# each side is handled with the circumcircle and the inscribed-angle theorem:
# for the chord BC (opposite vertex A) draw the diameter from B to its antipode
# D. Then angle D subtends the same chord as angle A, so they are equal, and
# triangle BDC is right-angled at C by Thales. Hence
#   sin A = sin D = a / (2R)   =>   a / sin A = 2R.
# Repeating the same construction for b and c gives 2R every time, and *that*
# is what proves the three ratios are equal to one another.
#
# The actual frame is 9 x 16 units (x in [-4.5, 4.5], y in [-8, 8]).
# Safe area: |y| <= 5.6 and |x| <= 3.8.

SAFE_WIDTH = 7.2


def fit_to_safe_width(mobject):
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def make_label(tex, font_size, color, with_background=True):
    """Create a MathTex label with an optional background for line crossings."""
    label = MathTex(tex, font_size=font_size, color=color)
    if with_background:
        label.add_background_rectangle(color=BG, opacity=0.92, buff=0.06)
    label.set_z_index(10)
    return label


class LawOfSines(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.14
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.85)
        self.add(watermark)

        SIDE_COLOR = ACCENT_YELLOW       # the chord being measured
        ANGLE_COLOR = ACCENT_CYAN        # inscribed angle and its twin
        DIAMETER_COLOR = ACCENT_MAGENTA  # diameter = 2R
        TRI_COLOR = ACCENT_PURPLE        # main triangle
        AUX_COLOR = GREY_B
        # Orange sits between the yellow and the magenta of the palette, so it
        # is reserved for the two beats that carry the proof: the Thales right
        # angle and the moment the three ratios land on the same 2R.
        THALES_COLOR = "#FF8A00"

        # ------------------------------------------------------ circle & vertices
        # A scalene triangle: 72.5 / 47.5 / 60 degrees, so no two constructions
        # ever look alike.
        center = np.array([0.0, 1.45, 0.0])
        R = 2.45

        def on_circle(deg):
            return center + R * np.array([
                np.cos(deg * DEGREES),
                np.sin(deg * DEGREES),
                0.0,
            ])

        A = on_circle(80)
        B = on_circle(200)
        C = on_circle(345)

        def antipode(P):
            return 2 * center - P

        def outside(P, distance=0.36):
            direction = P - center
            return P + direction / np.linalg.norm(direction) * distance

        # ------------------------------------------------------------ hook 0-2s
        title = Tex(r"Ley de Senos", font_size=64, color=WHITE)
        title.set_stroke(width=1)
        title.set_z_index(20)
        title.move_to(UP * 5.45)
        fit_to_safe_width(title)

        underline = Line(
            title.get_left() + DOWN * 0.32,
            title.get_right() + DOWN * 0.32,
            stroke_width=4,
        )
        underline.set_color(color=[ACCENT_YELLOW, THALES_COLOR, ACCENT_MAGENTA])
        underline.set_z_index(20)

        self.play(Write(title), run_time=0.9)
        self.play(Create(underline), run_time=0.5)
        self.wait(0.3)

        # --------------------------------------------------- triangle inscribed
        triangle = Polygon(
            A, B, C,
            color=TRI_COLOR, stroke_width=5,
            fill_color=TRI_COLOR, fill_opacity=0.06,
        )
        dots = VGroup(*[Dot(P, color=WHITE, radius=0.06) for P in (A, B, C)])
        vertex_labels = VGroup(
            make_label("A", 32, WHITE, with_background=False).move_to(outside(A)),
            make_label("B", 32, WHITE, with_background=False).move_to(outside(B)),
            make_label("C", 32, WHITE, with_background=False).move_to(outside(C)),
        )

        circle = Circle(radius=R, color=AUX_COLOR, stroke_width=2.5)
        circle.move_to(center)
        circle.set_stroke(opacity=0.7)

        self.play(Create(triangle), FadeIn(dots), run_time=0.9)
        self.play(Write(vertex_labels), run_time=0.5)

        # The circumcircle is the hidden object that ties everything together.
        self.play(Create(circle), run_time=0.9)
        self.bring_to_back(circle)
        self.wait(0.3)

        center_dot = Dot(center, color=DIAMETER_COLOR, radius=0.05)
        self.add(center_dot)

        # ------------------------------------------------------ equation stack
        equations = VGroup()
        stack_top = -2.0
        stack_gap = 1.5

        def build_step(chord_start, chord_end, apex, side_tex, angle_tex,
                       side_label_shift, fast=False):
            """Run the inscribed-angle argument for one side of the triangle.

            The chord runs chord_start -> chord_end and is seen from `apex`.
            The diameter is drawn from chord_start, so the right angle by
            Thales lands on chord_end. Returns the mobjects to clean up.
            """
            speed = 0.55 if fast else 1.0
            D = antipode(chord_start)

            # The side under study and the inscribed angle that sees it.
            side = Line(chord_start, chord_end, color=SIDE_COLOR, stroke_width=6)
            side.set_z_index(4)
            side_label = make_label(side_tex, 32, SIDE_COLOR).move_to(
                (chord_start + chord_end) / 2 + side_label_shift
            )
            arc_apex = Angle(
                Line(apex, chord_start), Line(apex, chord_end),
                radius=0.62, color=ANGLE_COLOR,
            )
            apex_label = make_label(
                angle_tex, 28, ANGLE_COLOR, with_background=False
            ).move_to(
                Angle(
                    Line(apex, chord_start), Line(apex, chord_end), radius=0.95,
                ).point_from_proportion(0.5)
            )
            self.play(
                Create(side), Write(side_label),
                Create(arc_apex), Write(apex_label),
                run_time=0.8 * speed,
            )

            # The key move: the diameter from one end of the chord.
            diameter = Line(chord_start, D, color=DIAMETER_COLOR, stroke_width=5)
            diameter.set_z_index(3)
            dot_D = Dot(D, color=WHITE, radius=0.06)
            label_D = make_label(
                "D", 30, DIAMETER_COLOR, with_background=False
            ).move_to(outside(D))
            two_R = make_label("2R", 30, DIAMETER_COLOR).move_to(
                (chord_start + D) / 2
                + normalize(np.array([-(D - chord_start)[1],
                                      (D - chord_start)[0], 0])) * 0.4
            )
            self.play(
                Create(diameter), FadeIn(dot_D), Write(label_D),
                run_time=0.8 * speed,
            )
            self.play(Write(two_R), run_time=0.5 * speed)

            # Thales: the triangle on a diameter is right-angled.
            closing = Line(D, chord_end, color=TRI_COLOR, stroke_width=4)
            closing.set_z_index(2)
            thales_fill = Polygon(
                chord_start, D, chord_end,
                stroke_width=0, fill_color=DIAMETER_COLOR, fill_opacity=0.08,
            )
            right_angle = RightAngle(
                Line(chord_end, chord_start), Line(chord_end, D),
                length=0.24, color=THALES_COLOR, stroke_width=4,
            )
            right_angle.set_z_index(6)
            self.play(
                Create(closing), FadeIn(thales_fill), Create(right_angle),
                run_time=0.7 * speed,
            )
            self.bring_to_back(thales_fill)

            # The twin angle at D sees the very same chord.
            arc_D = Angle(
                Line(D, chord_start), Line(D, chord_end),
                radius=0.52, color=ANGLE_COLOR,
            )
            twin_label = make_label(
                angle_tex, 26, ANGLE_COLOR, with_background=False
            ).move_to(
                Angle(
                    Line(D, chord_start), Line(D, chord_end), radius=0.88,
                ).point_from_proportion(0.5)
            )
            self.play(Create(arc_D), Write(twin_label), run_time=0.7 * speed)
            self.wait(0.3 * speed)

            # sin(angle) = side / 2R, so side / sin(angle) = 2R.
            equation = MathTex(
                r"\frac{" + side_tex + r"}{\sin " + angle_tex + r"}",
                r"=", r"2R",
                font_size=40,
            )
            equation[0][0].set_color(SIDE_COLOR)
            equation[2].set_color(DIAMETER_COLOR)
            equation.set_stroke(width=1)
            equation.set_z_index(21)
            equation.move_to(
                np.array([0.0, stack_top - stack_gap * len(equations), 0.0])
            )
            # The numerator flies out of the side already drawn on screen; the
            # fraction bar and the sine denominator are written right after it.
            self.play(
                TransformFromCopy(side_label[1], equation[0][0]),
                run_time=0.7 * speed,
            )
            self.play(Write(equation[0][1:]), run_time=0.6 * speed)
            self.play(
                Write(equation[1]),
                TransformFromCopy(two_R[1], equation[2]),
                run_time=0.6 * speed,
            )
            equations.add(equation)
            self.wait(0.4 * speed)

            return VGroup(
                side, side_label, arc_apex, apex_label, diameter, dot_D,
                label_D, two_R, closing, thales_fill, right_angle, arc_D,
                twin_label,
            )

        # --------------------------------------------- one construction per side
        # Side a = BC, seen from A. Diameter from B, right angle at C.
        step_a = build_step(B, C, A, "a", "A", DOWN * 0.42)
        self.play(FadeOut(step_a), run_time=0.5)

        # Side b = CA, seen from B. Diameter from C, right angle at A.
        step_b = build_step(C, A, B, "b", "B", RIGHT * 0.46, fast=True)
        self.play(FadeOut(step_b), run_time=0.4)

        # Side c = AB, seen from C. Diameter from A, right angle at B.
        step_c = build_step(A, B, C, "c", "C", LEFT * 0.46, fast=True)
        self.play(FadeOut(step_c), run_time=0.4)
        self.wait(0.6)

        # ------------------------------------------------------------ conclusion
        # Every ratio landed on the same 2R, which is exactly why they are equal.
        highlight = VGroup(*[eq[2] for eq in equations])
        self.play(
            *[Indicate(part, color=THALES_COLOR, scale_factor=1.3)
              for part in highlight],
            run_time=1.0,
        )
        self.wait(0.5)

        formula = MathTex(
            r"\frac{a}{\sin A}", r"=", r"\frac{b}{\sin B}", r"=",
            r"\frac{c}{\sin C}", r"=", r"2R",
            font_size=46,
        )
        formula[0][0].set_color(SIDE_COLOR)
        formula[2][0].set_color(SIDE_COLOR)
        formula[4][0].set_color(SIDE_COLOR)
        formula[6].set_color(DIAMETER_COLOR)
        formula.set_stroke(width=1)
        formula.set_z_index(21)
        formula.move_to(np.array([0.0, stack_top - stack_gap, 0.0]))
        fit_to_safe_width(formula)

        # The three separate results merge into the single statement.
        self.play(
            TransformMatchingShapes(equations, formula),
            run_time=1.4,
        )
        self.wait(0.5)

        result_box = SurroundingRectangle(formula, buff=0.18, corner_radius=0.12)
        result_box.set_stroke(width=4, color=[ACCENT_YELLOW, THALES_COLOR])
        result_box.set_z_index(20)
        self.play(Create(result_box), run_time=0.7)
        self.wait(1.8)

        animate_End(scene=self)
