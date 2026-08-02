from manim import *
from lnx import *

# proof-without-words | geometry | intermediate
# Mathematical reference: Euclid, Elements I.47 (the "windmill" proof).
#
# Model coordinates (right angle at A, legs 3 and 4, hypotenuse 5):
#   A = (0, 0)   B = (3, 0)   C = (0, 4)
#   Square on AB : B(3,0)  F(3,-3)  G(0,-3)  A(0,0)          area 9
#   Square on AC : C(0,4)  H(-4,4)  K(-4,0)  A(0,0)          area 16
#   Square on BC : B(3,0)  C(0,4)   E(4,7)   D(7,3)          area 25
#   Altitude foot L = (1.92, 1.44) with BL = 9/5 and CL = 16/5
#   M = L + (4, 3) = (5.92, 4.44) splits the hypotenuse square into
#   rectangle B-L-M-D (area 9) and rectangle C-L-M-E (area 16).
#
# Each leg square reaches its rectangle through three area preserving steps:
#   shear (same base, same height) -> 90 degree rotation -> shear.

FIGURE_SCALE = 0.62
FIGURE_CENTER = np.array([1.5, 2.0, 0.0])
FIGURE_SHIFT = np.array([0.0, -1.2, 0.0])

SAFE_WIDTH = 7.2


def point(x, y):
    """Map model coordinates to safe-area scene coordinates."""
    return (np.array([x, y, 0.0]) - FIGURE_CENTER) * FIGURE_SCALE + FIGURE_SHIFT


def polygon(vertices, color, fill_opacity=0.28, stroke_width=4):
    """Build a filled polygon from model coordinates."""
    return Polygon(
        *[point(x, y) for x, y in vertices],
        color=color,
        stroke_width=stroke_width,
        fill_color=color,
        fill_opacity=fill_opacity,
    )


def centroid(vertices):
    """Return the scene centroid of a model polygon."""
    return sum(point(x, y) for x, y in vertices) / len(vertices)


def fit_to_safe_width(mobject):
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def area_label(tex, vertices, color, font_size=30):
    label = MathTex(tex, font_size=font_size, color=color)
    label.move_to(centroid(vertices))
    label.set_stroke(width=1)
    label.set_z_index(30)
    return label


# Model vertices ------------------------------------------------------------
A = (0.0, 0.0)
B = (3.0, 0.0)
C = (0.0, 4.0)
F = (3.0, -3.0)
G = (0.0, -3.0)
H = (-4.0, 4.0)
K = (-4.0, 0.0)
D = (7.0, 3.0)
E = (4.0, 7.0)
L = (1.92, 1.44)
M = (5.92, 4.44)

SQUARE_AB = [B, F, G, A]
SQUARE_AC = [C, H, K, A]
SQUARE_BC = [B, C, E, D]

# Shear of the AB square: the side FB stays fixed, the opposite side slides
# along the same vertical line, so base and height are unchanged.
PARALLELOGRAM_AB = [B, F, (0.0, 1.0), C]
# Rotation by -90 degrees about B sends F -> A and C -> D.
ROTATED_AB = [B, A, (4.0, 3.0), D]
RECTANGLE_AB = [B, L, M, D]

# Shear of the AC square: the side CH stays fixed, the opposite side slides
# along the same horizontal line.
PARALLELOGRAM_AC = [C, H, (-1.0, 0.0), B]
# Rotation by +90 degrees about C sends H -> A and B -> E.
ROTATED_AC = [C, A, (4.0, 3.0), E]
RECTANGLE_AC = [C, L, M, E]


def validate_construction(tolerance=1e-9):
    """Check the areas that the proof claims are equal."""

    def shoelace(vertices):
        total = 0.0
        for index, (x1, y1) in enumerate(vertices):
            x2, y2 = vertices[(index + 1) % len(vertices)]
            total += x1 * y2 - x2 * y1
        return abs(total) / 2.0

    assert abs(shoelace(SQUARE_AB) - 9.0) < tolerance
    assert abs(shoelace(SQUARE_AC) - 16.0) < tolerance
    assert abs(shoelace(SQUARE_BC) - 25.0) < tolerance
    for chain in (
        (SQUARE_AB, PARALLELOGRAM_AB, ROTATED_AB, RECTANGLE_AB),
        (SQUARE_AC, PARALLELOGRAM_AC, ROTATED_AC, RECTANGLE_AC),
    ):
        reference = shoelace(chain[0])
        for shape in chain[1:]:
            assert abs(shoelace(shape) - reference) < tolerance
    # The altitude foot lies on the hypotenuse and the split is exact.
    assert abs(shoelace(RECTANGLE_AB) + shoelace(RECTANGLE_AC) - 25.0) < tolerance


validate_construction()


class PythagorasEuclid(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        # --- Hook (0.0 - 2.0 s): the windmill appears at once ---------------
        triangle = polygon([A, B, C], WHITE, fill_opacity=0.16, stroke_width=5)
        triangle.set_z_index(10)
        right_angle = RightAngle(
            Line(point(*A), point(*B)),
            Line(point(*A), point(*C)),
            length=0.24,
            color=WHITE,
            stroke_width=4,
        )
        right_angle.set_z_index(12)

        square_ab = polygon(SQUARE_AB, ACCENT_CYAN)
        square_ac = polygon(SQUARE_AC, ACCENT_MAGENTA)
        square_bc = polygon(SQUARE_BC, ACCENT_YELLOW, fill_opacity=0.20)

        title = Tex(
            r"\textbf{El molino de Euclides}",
            font_size=44,
            color=WHITE,
        ).move_to(UP * 5.0)
        title.set_z_index(40)
        subtitle = Tex(
            r"\textit{Elementos, I.47}",
            font_size=30,
            color=ACCENT_YELLOW,
        ).move_to(UP * 4.3)
        subtitle.set_z_index(40)
        fit_to_safe_width(title)

        self.play(
            Create(triangle),
            FadeIn(title, shift=DOWN * 0.12),
            run_time=0.9,
        )
        self.play(
            LaggedStart(
                Create(square_ab),
                Create(square_ac),
                Create(square_bc),
                lag_ratio=0.25,
            ),
            FadeIn(right_angle),
            run_time=1.3,
        )
        self.play(FadeIn(subtitle), run_time=0.4)

        label_ab = area_label(r"a^2", SQUARE_AB, ACCENT_CYAN, font_size=32)
        label_ac = area_label(r"b^2", SQUARE_AC, ACCENT_MAGENTA, font_size=32)
        label_bc = area_label(r"c^2", SQUARE_BC, ACCENT_YELLOW, font_size=32)
        self.play(
            LaggedStart(
                FadeIn(label_ab),
                FadeIn(label_ac),
                FadeIn(label_bc),
                lag_ratio=0.2,
            ),
            run_time=0.9,
        )
        self.wait(0.6)

        # --- The altitude splits the hypotenuse square ----------------------
        step_note = Tex(
            r"\textbf{Bajamos la altura desde el ángulo recto}",
            font_size=30,
            color=WHITE,
        ).move_to(UP * 3.35)
        step_note.set_z_index(40)
        fit_to_safe_width(step_note)

        altitude = Line(
            point(*A),
            point(*M),
            color=WHITE,
            stroke_width=4,
        )
        altitude.set_z_index(14)
        foot_dot = Dot(point(*L), radius=0.05, color=WHITE)
        foot_dot.set_z_index(15)

        self.play(FadeIn(step_note, shift=DOWN * 0.1), run_time=0.5)
        self.play(Create(altitude), FadeIn(foot_dot), run_time=1.2)

        rect_ab = polygon(RECTANGLE_AB, ACCENT_CYAN, fill_opacity=0.30)
        rect_ac = polygon(RECTANGLE_AC, ACCENT_MAGENTA, fill_opacity=0.30)
        rect_ab.set_z_index(2)
        rect_ac.set_z_index(2)
        self.play(
            FadeOut(label_bc),
            FadeIn(rect_ab),
            FadeIn(rect_ac),
            square_bc.animate.set_fill(opacity=0.0).set_stroke(
                color=ACCENT_YELLOW, opacity=0.75
            ),
            run_time=1.1,
        )
        self.wait(0.8)

        # --- Key step: square -> parallelogram -> rectangle -----------------
        shear_note = Tex(
            r"\textbf{Misma base y misma altura: la cizalla no cambia el área}",
            font_size=28,
            color=ACCENT_CYAN,
        ).move_to(UP * 3.35)
        shear_note.set_z_index(40)
        fit_to_safe_width(shear_note)
        self.play(
            ReplacementTransform(step_note, shear_note),
            FadeOut(label_ab),
            run_time=0.7,
        )

        moving_ab = square_ab.copy()
        moving_ab.set_z_index(6)
        moving_ab.set_fill(opacity=0.42)
        self.add(moving_ab)

        parallelogram_ab = polygon(
            PARALLELOGRAM_AB, ACCENT_CYAN, fill_opacity=0.42
        )
        parallelogram_ab.set_z_index(6)
        self.play(
            Transform(moving_ab, parallelogram_ab),
            run_time=2.4,
            rate_func=smooth,
        )
        self.wait(0.9)

        turn_note = Tex(
            r"\textbf{Un giro de $90^\circ$ sobre el vértice}",
            font_size=30,
            color=ACCENT_CYAN,
        ).move_to(UP * 3.35)
        turn_note.set_z_index(40)
        fit_to_safe_width(turn_note)
        self.play(ReplacementTransform(shear_note, turn_note), run_time=0.5)
        self.play(
            Rotate(moving_ab, angle=-PI / 2, about_point=point(*B)),
            run_time=1.9,
            rate_func=smooth,
        )
        self.wait(0.7)

        second_shear_note = Tex(
            r"\textbf{Otra cizalla: cae justo sobre su rectángulo}",
            font_size=29,
            color=ACCENT_CYAN,
        ).move_to(UP * 3.35)
        second_shear_note.set_z_index(40)
        fit_to_safe_width(second_shear_note)
        target_ab = polygon(RECTANGLE_AB, ACCENT_CYAN, fill_opacity=0.42)
        target_ab.set_z_index(6)
        self.play(ReplacementTransform(turn_note, second_shear_note), run_time=0.5)
        self.play(
            Transform(moving_ab, target_ab),
            run_time=2.3,
            rate_func=smooth,
        )
        self.play(
            Indicate(moving_ab, color=ACCENT_CYAN, scale_factor=1.03),
            run_time=1.0,
        )
        self.wait(0.6)

        # --- Same three steps for the other leg, faster ---------------------
        repeat_note = Tex(
            r"\textbf{El otro cateto repite los tres pasos}",
            font_size=30,
            color=ACCENT_MAGENTA,
        ).move_to(UP * 3.35)
        repeat_note.set_z_index(40)
        fit_to_safe_width(repeat_note)
        self.play(
            ReplacementTransform(second_shear_note, repeat_note),
            FadeOut(label_ac),
            run_time=0.6,
        )

        moving_ac = square_ac.copy()
        moving_ac.set_z_index(6)
        moving_ac.set_fill(opacity=0.42)
        self.add(moving_ac)

        parallelogram_ac = polygon(
            PARALLELOGRAM_AC, ACCENT_MAGENTA, fill_opacity=0.42
        )
        parallelogram_ac.set_z_index(6)
        self.play(
            Transform(moving_ac, parallelogram_ac),
            run_time=1.6,
            rate_func=smooth,
        )
        self.play(
            Rotate(moving_ac, angle=PI / 2, about_point=point(*C)),
            run_time=1.5,
            rate_func=smooth,
        )
        target_ac = polygon(RECTANGLE_AC, ACCENT_MAGENTA, fill_opacity=0.42)
        target_ac.set_z_index(6)
        self.play(
            Transform(moving_ac, target_ac),
            run_time=1.6,
            rate_func=smooth,
        )
        self.wait(0.7)

        # --- Payoff: the two rectangles fill the hypotenuse square ----------
        payoff_label_ab = area_label(r"a^2", RECTANGLE_AB, WHITE, font_size=30)
        payoff_label_ac = area_label(r"b^2", RECTANGLE_AC, WHITE, font_size=30)
        payoff_label_ab.set_z_index(40)
        payoff_label_ac.set_z_index(40)

        result = MathTex(
            r"a^2", r"+", r"b^2", r"=", r"c^2",
            font_size=52,
        ).move_to(UP * 3.5)
        result[0].set_color(ACCENT_CYAN)
        result[2].set_color(ACCENT_MAGENTA)
        result[4].set_color(ACCENT_YELLOW)
        result[1].set_color(WHITE)
        result[3].set_color(WHITE)
        result.set_stroke(width=1)
        result.set_z_index(40)

        self.play(
            FadeOut(repeat_note),
            FadeIn(payoff_label_ab),
            FadeIn(payoff_label_ac),
            square_bc.animate.set_stroke(width=7, opacity=1.0),
            run_time=0.9,
        )
        self.play(Write(result), run_time=1.2)
        self.play(
            Indicate(result, color=ACCENT_YELLOW, scale_factor=1.06),
            run_time=1.2,
        )
        self.wait(1.2)

        animate_End(scene=self)
