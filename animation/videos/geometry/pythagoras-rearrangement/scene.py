from manim import *
from lnx import *

# proof-without-words | geometry | basic
#
# Classic rearrangement proof of the Pythagorean theorem.
# A square of side (a+b) holds four congruent right triangles.
# Arrangement 1 leaves a single hole: a square of side c.
# Arrangement 2 leaves two holes: squares of sides a and b.
# Same triangles, same enclosing square, therefore c^2 = a^2 + b^2.

LEG_A = 2.0
LEG_B = 2.9
SIDE = LEG_A + LEG_B
SQUARE_CENTER = np.array([0.0, -0.75, 0.0])


def square_point(x, y):
    """Map local square coordinates (0..SIDE) to scene coordinates."""
    return SQUARE_CENTER + np.array([x - SIDE / 2, y - SIDE / 2, 0.0])


def triangle_from(p1, p2, p3, color):
    """Build one filled right triangle from local square coordinates."""
    triangle = Polygon(
        square_point(*p1),
        square_point(*p2),
        square_point(*p3),
        color=color,
        stroke_width=4,
        fill_color=color,
        fill_opacity=0.32,
    )
    triangle.set_z_index(4)
    return triangle


def hole_from(points, color, opacity=0.45):
    """Build one filled hole polygon from local square coordinates."""
    hole = Polygon(
        *[square_point(*point) for point in points],
        color=color,
        stroke_width=5,
        fill_color=color,
        fill_opacity=opacity,
    )
    hole.set_z_index(2)
    return hole


def validate_congruence(arrangement_one, arrangement_two, tolerance=1e-9):
    """Every triangle in both arrangements must have legs LEG_A and LEG_B."""
    expected = sorted(
        [LEG_A, LEG_B, np.hypot(LEG_A, LEG_B)]
    )
    for group in (arrangement_one, arrangement_two):
        for triple in group:
            vertices = [np.array(point, dtype=float) for point in triple]
            lengths = sorted(
                float(np.linalg.norm(vertices[index] - vertices[index - 1]))
                for index in range(3)
            )
            for actual, target in zip(lengths, expected):
                assert abs(actual - target) < tolerance


class PythagorasRearrangement(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        a, b, s = LEG_A, LEG_B, SIDE

        # Arrangement 1: four triangles hug the corners, the hole is a c-square.
        first_layout = [
            ((0, 0), (a, 0), (0, b)),
            ((a, 0), (s, 0), (s, a)),
            ((s, a), (s, s), (b, s)),
            ((0, b), (0, s), (b, s)),
        ]
        # Arrangement 2: the same triangles pair up into two rectangles.
        second_layout = [
            ((b, 0), (s, 0), (s, b)),
            ((b, 0), (s, b), (b, b)),
            ((0, b), (0, s), (b, s)),
            ((0, b), (b, s), (b, b)),
        ]
        validate_congruence(first_layout, second_layout)

        triangle_colors = [
            ACCENT_CYAN,
            ACCENT_MAGENTA,
            ACCENT_PURPLE,
            ACCENT_CYAN,
        ]

        outer_square = Polygon(
            square_point(0, 0),
            square_point(s, 0),
            square_point(s, s),
            square_point(0, s),
            color=WHITE,
            stroke_width=6,
        )
        outer_square.set_z_index(1)

        triangles = VGroup(
            *[
                triangle_from(*triple, color)
                for triple, color in zip(first_layout, triangle_colors)
            ]
        )
        targets = [
            triangle_from(*triple, color)
            for triple, color in zip(second_layout, triangle_colors)
        ]

        hole_c = hole_from(
            [(a, 0), (s, a), (b, s), (0, b)],
            ACCENT_YELLOW,
        )
        hole_b = hole_from([(0, 0), (b, 0), (b, b), (0, b)], ACCENT_YELLOW)
        hole_a = hole_from([(b, b), (s, b), (s, s), (b, s)], ACCENT_YELLOW)

        # Hook: the square and its four triangles land within the first seconds.
        title = Tex(
            r"\textbf{Mismos triángulos, mismo cuadrado}",
            font_size=38,
            color=WHITE,
        ).move_to(UP * 5.1)
        title.set_z_index(30)

        self.play(
            Create(outer_square),
            FadeIn(title, shift=UP * 0.12),
            run_time=0.8,
        )
        self.play(
            LaggedStart(
                *[FadeIn(triangle, scale=0.85) for triangle in triangles],
                lag_ratio=0.12,
            ),
            run_time=1.0,
        )

        # The hole is a square of side c: the first payoff image.
        label_c = MathTex(r"c^2", font_size=52, color=ACCENT_YELLOW)
        label_c.move_to(hole_c.get_center())
        label_c.set_z_index(20)

        self.play(FadeIn(hole_c), run_time=0.5)
        self.play(Write(label_c), run_time=0.6)
        self.play(
            Indicate(hole_c, color=ACCENT_YELLOW, scale_factor=1.05),
            run_time=1.0,
        )

        # Support labels stay outside the figure, never over a segment.
        right_angle = RightAngle(
            Line(square_point(0, 0), square_point(a, 0)),
            Line(square_point(0, 0), square_point(0, b)),
            length=0.32,
            color=WHITE,
        )
        right_angle.set_z_index(15)

        label_a = MathTex(r"a", font_size=40, color=ACCENT_CYAN)
        label_a.next_to(
            (square_point(0, 0) + square_point(a, 0)) / 2,
            DOWN,
            buff=0.28,
        )
        label_a.set_z_index(20)
        label_b = MathTex(r"b", font_size=40, color=ACCENT_MAGENTA)
        label_b.next_to(
            (square_point(a, 0) + square_point(s, 0)) / 2,
            DOWN,
            buff=0.28,
        )
        label_b.set_z_index(20)
        side_note = Tex(
            r"Lado del cuadrado grande: $a+b$",
            font_size=30,
            color=WHITE,
        ).move_to(DOWN * 4.35)
        side_note.set_z_index(20)

        self.play(
            Create(right_angle),
            FadeIn(label_a, shift=DOWN * 0.08),
            FadeIn(label_b, shift=DOWN * 0.08),
            run_time=0.8,
        )
        self.play(FadeIn(side_note, shift=UP * 0.08), run_time=0.6)
        self.wait(1.0)

        # The move: the same four triangles slide into the second arrangement.
        slide_note = Tex(
            r"\textbf{Deslizamos los mismos 4 triángulos}",
            font_size=32,
            color=ACCENT_YELLOW,
        ).move_to(UP * 4.3)
        slide_note.set_z_index(30)

        self.play(
            FadeIn(slide_note, shift=UP * 0.1),
            FadeOut(right_angle),
            run_time=0.6,
        )
        self.play(
            LaggedStart(
                *[
                    Transform(triangle, target)
                    for triangle, target in zip(triangles, targets)
                ],
                lag_ratio=0.18,
            ),
            FadeOut(label_c, scale=0.6),
            ReplacementTransform(hole_c, VGroup(hole_b, hole_a)),
            run_time=2.6,
        )
        self.wait(0.6)

        # The hole is now split into two squares of sides a and b.
        label_b2 = MathTex(r"b^2", font_size=50, color=ACCENT_YELLOW)
        label_b2.move_to(hole_b.get_center())
        label_b2.set_z_index(20)
        label_a2 = MathTex(r"a^2", font_size=44, color=ACCENT_YELLOW)
        label_a2.move_to(hole_a.get_center())
        label_a2.set_z_index(20)

        self.play(
            Write(label_b2),
            Write(label_a2),
            run_time=0.8,
        )
        self.play(
            Indicate(hole_b, color=ACCENT_YELLOW, scale_factor=1.04),
            Indicate(hole_a, color=ACCENT_YELLOW, scale_factor=1.04),
            run_time=1.2,
        )
        self.wait(0.6)

        # Payoff: the two holes have the same total area as the c-square.
        payoff = MathTex(
            r"c^2", r"=", r"a^2+b^2",
            font_size=56,
        ).move_to(DOWN * 4.45)
        payoff[0].set_color(ACCENT_YELLOW)
        payoff[1].set_color(WHITE)
        payoff[2].set_color(ACCENT_YELLOW)
        payoff.set_z_index(30)
        payoff_box = SurroundingRectangle(
            payoff,
            color=ACCENT_YELLOW,
            buff=0.24,
            corner_radius=0.12,
            stroke_width=3,
        )
        payoff_box.set_z_index(29)

        self.play(
            FadeOut(side_note),
            FadeOut(slide_note),
            FadeIn(payoff, shift=UP * 0.12),
            Create(payoff_box),
            run_time=0.9,
        )
        self.play(
            payoff_box.animate.set_stroke(width=6),
            rate_func=there_and_back,
            run_time=1.2,
        )
        self.wait(1.4)

        animate_End(scene=self)
