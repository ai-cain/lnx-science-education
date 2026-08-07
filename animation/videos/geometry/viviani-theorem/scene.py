from manim import *
from lnx import *

# hidden-invariant | geometry | intermediate
# Mathematical reference:
# https://mathworld.wolfram.com/VivianisTheorem.html
#
# Viviani's theorem: for any interior point of an equilateral triangle, the sum
# of the distances to the three sides equals the altitude of the triangle.

SIDE = 4.2
HEIGHT = SIDE * np.sqrt(3) / 2
BASE_Y = -2.6
CENTER_X = -0.6

VERTEX_A = np.array([CENTER_X - SIDE / 2, BASE_Y, 0.0])
VERTEX_B = np.array([CENTER_X + SIDE / 2, BASE_Y, 0.0])
VERTEX_C = np.array([CENTER_X, BASE_Y + HEIGHT, 0.0])
CENTROID = (VERTEX_A + VERTEX_B + VERTEX_C) / 3
INRADIUS = HEIGHT / 3

BAR_X = 2.85
BAR_WIDTH = 0.5

# Each side is paired with the color of its own distance segment.
SIDE_SPECS = (
    (VERTEX_A, VERTEX_B, ACCENT_CYAN),
    (VERTEX_B, VERTEX_C, ACCENT_MAGENTA),
    (VERTEX_C, VERTEX_A, ACCENT_YELLOW),
)


def foot_of_perpendicular(point, first, second):
    """Return the orthogonal projection of ``point`` onto line ``first-second``."""
    direction = second - first
    unit = direction / np.linalg.norm(direction)
    return first + np.dot(point - first, unit) * unit


def interior_point(time_value):
    """Return a point that always stays strictly inside the triangle."""
    angle = 1.15 * time_value
    radius = 0.94 * INRADIUS * (0.30 + 0.70 * abs(np.sin(0.83 * time_value + 0.4)))
    return CENTROID + radius * np.array([np.cos(angle), np.sin(1.37 * angle), 0.0])


def distances_from(point):
    """Return the three perpendicular distances, in SIDE_SPECS order."""
    return [
        float(np.linalg.norm(point - foot_of_perpendicular(point, first, second)))
        for first, second, _ in SIDE_SPECS
    ]


# The invariant is validated numerically before anything is drawn.
for _sample in np.linspace(0.0, 12.0, 240):
    assert abs(sum(distances_from(interior_point(_sample))) - HEIGHT) < 1e-9


def build_stacked_bar(point):
    """Return the stacked bar whose segments match the distance colors."""
    bar = VGroup()
    cursor = BASE_Y
    for length, (_, _, color) in zip(distances_from(point), SIDE_SPECS):
        segment = Rectangle(
            width=BAR_WIDTH,
            height=max(length, 1e-4),
            stroke_width=2,
            stroke_color=color,
            fill_color=color,
            fill_opacity=0.85,
        )
        segment.move_to(np.array([BAR_X, cursor + length / 2, 0.0]))
        bar.add(segment)
        cursor += length
    return bar


def build_distance_group(point):
    """Return perpendicular segments plus their right-angle marks."""
    group = VGroup()
    for first, second, color in SIDE_SPECS:
        foot = foot_of_perpendicular(point, first, second)
        segment = Line(point, foot, color=color, stroke_width=6)
        side_unit = (second - first) / np.linalg.norm(second - first)
        mark = RightAngle(
            Line(foot, foot + side_unit),
            Line(foot, point),
            length=0.17,
            color=WHITE,
            stroke_width=2.5,
        )
        group.add(VGroup(segment, mark))
    return group


class VivianiTheorem(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        tracker = ValueTracker(0.0)

        triangle = Polygon(
            VERTEX_A,
            VERTEX_B,
            VERTEX_C,
            color=WHITE,
            stroke_width=5,
        )
        triangle.set_fill(SURFACE, opacity=0.35)

        moving_point = always_redraw(
            lambda: Dot(
                interior_point(tracker.get_value()),
                radius=0.09,
                color=WHITE,
            ).set_z_index(12)
        )
        distance_group = always_redraw(
            lambda: build_distance_group(interior_point(tracker.get_value()))
        )
        stacked_bar = always_redraw(
            lambda: build_stacked_bar(interior_point(tracker.get_value()))
        )

        bar_top = Line(
            np.array([BAR_X - BAR_WIDTH * 0.9, BASE_Y + HEIGHT, 0.0]),
            np.array([BAR_X + BAR_WIDTH * 0.9, BASE_Y + HEIGHT, 0.0]),
            color=WHITE,
            stroke_width=4,
        )
        bar_top.set_z_index(15)
        bar_caption = Tex(
            r"\textbf{suma}",
            font_size=28,
            color=WHITE,
        ).move_to(np.array([BAR_X, BASE_Y + HEIGHT + 0.42, 0.0]))
        bar_caption.set_z_index(15)

        # Hook: the point, its three distances and the bar appear at once.
        hook = Tex(
            r"\textbf{Las tres distancias cambian...}",
            font_size=38,
            color=WHITE,
        ).move_to(UP * 4.9)
        hook.set_z_index(20)

        self.play(
            Create(triangle),
            FadeIn(hook, shift=UP * 0.12),
            run_time=0.8,
        )
        self.add(distance_group, moving_point, stacked_bar)
        self.play(
            FadeIn(distance_group),
            FadeIn(moving_point),
            FadeIn(stacked_bar),
            run_time=0.9,
        )
        self.play(Create(bar_top), FadeIn(bar_caption), run_time=0.5)

        # Drag beat: everything moves except the top of the bar.
        self.play(
            tracker.animate.set_value(3.2),
            rate_func=linear,
            run_time=4.2,
        )

        constant_note = Tex(
            r"\textbf{...pero la suma nunca se mueve}",
            font_size=34,
            color=ACCENT_YELLOW,
        ).move_to(UP * 4.1)
        constant_note.set_z_index(20)
        self.play(FadeIn(constant_note, shift=UP * 0.1), run_time=0.5)
        self.play(
            tracker.animate.set_value(6.6),
            Flash(
                np.array([BAR_X, BASE_Y + HEIGHT, 0.0]),
                color=ACCENT_YELLOW,
                flash_radius=0.55,
                line_length=0.18,
            ),
            rate_func=linear,
            run_time=3.6,
        )

        # The invariant is named: it is exactly the altitude.
        altitude_line = DashedLine(
            VERTEX_C,
            np.array([VERTEX_C[0], BASE_Y, 0.0]),
            color=ACCENT_PURPLE,
            stroke_width=5,
        )
        altitude_label = MathTex(
            r"h",
            font_size=34,
            color=ACCENT_PURPLE,
        ).move_to(np.array([VERTEX_C[0] - 0.34, BASE_Y + HEIGHT / 2, 0.0]))
        altitude_label.set_z_index(20)
        statement = MathTex(
            r"d_1+d_2+d_3",
            r"=",
            r"h",
            font_size=42,
        ).move_to(UP * 4.9)
        statement[0].set_color(WHITE)
        statement[1].set_color(ACCENT_YELLOW)
        statement[2].set_color(ACCENT_PURPLE)
        statement.set_z_index(20)

        self.play(
            FadeOut(hook),
            FadeOut(constant_note),
            Create(altitude_line),
            FadeIn(altitude_label),
            run_time=0.9,
        )
        self.play(Write(statement), run_time=0.9)
        self.play(
            tracker.animate.set_value(9.4),
            rate_func=linear,
            run_time=3.2,
        )

        # Freeze the configuration to build the proof on a fixed point.
        frozen_value = 10.6
        self.play(
            tracker.animate.set_value(frozen_value),
            rate_func=smooth,
            run_time=1.2,
        )
        frozen_point = interior_point(frozen_value)
        static_distances = build_distance_group(frozen_point)
        static_bar = build_stacked_bar(frozen_point)
        static_dot = Dot(frozen_point, radius=0.09, color=WHITE).set_z_index(12)
        self.remove(distance_group, stacked_bar, moving_point)
        self.add(static_distances, static_bar, static_dot)

        # Proof: three triangles with a common vertex at P tile the whole one.
        proof_title = Tex(
            r"\textbf{Por qué: tres triángulos}",
            font_size=34,
            color=ACCENT_CYAN,
        ).move_to(UP * 4.0)
        proof_title.set_z_index(20)
        sub_triangles = VGroup()
        for first, second, color in SIDE_SPECS:
            piece = Polygon(
                first,
                second,
                frozen_point,
                stroke_width=3,
                stroke_color=color,
                fill_color=color,
                fill_opacity=0.30,
            )
            sub_triangles.add(piece)
        sub_triangles.set_z_index(-1)

        self.play(
            FadeIn(proof_title, shift=UP * 0.1),
            LaggedStart(
                *[Create(piece) for piece in sub_triangles],
                lag_ratio=0.25,
            ),
            run_time=1.6,
        )
        self.wait(0.5)

        areas = MathTex(
            r"\frac{a\,d_1}{2}+\frac{a\,d_2}{2}+\frac{a\,d_3}{2}",
            r"=",
            r"\frac{a\,h}{2}",
            font_size=36,
        ).move_to(DOWN * 3.9)
        areas[0].set_color(WHITE)
        areas[1].set_color(ACCENT_YELLOW)
        areas[2].set_color(ACCENT_PURPLE)
        areas.set_z_index(20)
        base_note = Tex(
            r"\textbf{las tres bases miden lo mismo: } $a$",
            font_size=28,
            color=WHITE,
        ).move_to(DOWN * 4.7)
        base_note.set_z_index(20)

        self.play(Write(areas), run_time=1.3)
        self.play(FadeIn(base_note, shift=UP * 0.08), run_time=0.6)
        self.wait(0.8)

        conclusion = MathTex(
            r"d_1+d_2+d_3",
            r"=",
            r"h",
            font_size=44,
        ).move_to(DOWN * 4.1)
        conclusion[0].set_color(WHITE)
        conclusion[1].set_color(ACCENT_YELLOW)
        conclusion[2].set_color(ACCENT_PURPLE)
        conclusion.set_z_index(20)
        self.play(
            FadeOut(base_note),
            TransformMatchingTex(areas, conclusion),
            run_time=1.4,
        )
        self.play(
            Indicate(conclusion, color=ACCENT_YELLOW, scale_factor=1.06),
            run_time=1.1,
        )

        # Payoff: the invariant holds for every interior point.
        payoff = Tex(
            r"\textbf{Teorema de Viviani}",
            font_size=36,
            color=WHITE,
        ).move_to(UP * 4.9)
        payoff_box = SurroundingRectangle(
            payoff,
            color=ACCENT_YELLOW,
            buff=0.2,
            corner_radius=0.12,
            stroke_width=3,
        )
        payoff_box.set_z_index(19)
        payoff.set_z_index(20)
        self.play(
            FadeOut(statement),
            FadeOut(proof_title),
            FadeIn(payoff, shift=UP * 0.1),
            Create(payoff_box),
            run_time=0.9,
        )
        self.play(
            payoff_box.animate.set_stroke(width=5),
            rate_func=there_and_back,
            run_time=1.0,
        )
        self.wait(0.9)

        animate_End(scene=self)
