from manim import *
from lnx import *

# visual-derivation | geometry | intermediate
# Mathematical reference:
# https://mathworld.wolfram.com/HeronsFormula.html
#
# Triangle 13-14-15 (a = BC = 14, b = CA = 13, c = AB = 15).
#   s = (13 + 14 + 15) / 2 = 21
#   Area = sqrt(21 * (21-13) * (21-14) * (21-15)) = sqrt(21*8*7*6)
#        = sqrt(7056) = 84   -> verified integer area
#   Inradius r = Area / s = 84 / 21 = 4
# Equal tangent lengths from each vertex:
#   from A: s - a = 7, from B: s - b = 8, from C: s - c = 6
#   7 + 8 + 6 = 21 = s, and each side is recovered: 8+6=14, 8+7=15, 7+6=13.

SAFE_WIDTH = 7.2

# Raw Euclidean model of the 13-14-15 triangle.
RAW_B = np.array([0.0, 0.0, 0.0])
RAW_C = np.array([14.0, 0.0, 0.0])
RAW_A = np.array([9.0, 12.0, 0.0])
RAW_INCENTER = np.array([8.0, 4.0, 0.0])
RAW_INRADIUS = 4.0

GEOMETRY_SCALE = 0.40
GEOMETRY_PIVOT = np.array([7.0, 4.0, 0.0])
GEOMETRY_ORIGIN = np.array([0.0, -1.15, 0.0])


def fit_to_safe_width(mobject):
    """Keep wide text inside the vertical safe area."""
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def scene_point(raw_point):
    """Map a point of the raw triangle model into scene coordinates."""
    return GEOMETRY_ORIGIN + GEOMETRY_SCALE * (raw_point - GEOMETRY_PIVOT)


POINT_A = scene_point(RAW_A)
POINT_B = scene_point(RAW_B)
POINT_C = scene_point(RAW_C)
INCENTER = scene_point(RAW_INCENTER)
INRADIUS = GEOMETRY_SCALE * RAW_INRADIUS
TRIANGLE_CENTER = (POINT_A + POINT_B + POINT_C) / 3.0


def outside_segment(first_point, second_point, distance=0.42):
    """Return a label anchor pushed outward from a side of the triangle."""
    midpoint = (first_point + second_point) / 2.0
    direction = second_point - first_point
    normal = np.array([-direction[1], direction[0], 0.0])
    normal = normal / np.linalg.norm(normal)
    if np.dot(normal, midpoint - TRIANGLE_CENTER) < 0:
        normal = -normal
    return midpoint + normal * distance


def foot_on_segment(first_point, second_point, center):
    """Orthogonal projection of the incenter onto a side: the tangency point."""
    direction = second_point - first_point
    unit = direction / np.linalg.norm(direction)
    projection = np.dot(center - first_point, unit)
    return first_point + unit * projection


def validate_tangency(point, first_point, second_point, tolerance=1e-9):
    """Check that a tangency point lies on the side and on the circumference."""
    assert abs(np.linalg.norm(point - INCENTER) - INRADIUS) < tolerance
    side_length = np.linalg.norm(second_point - first_point)
    covered = (
        np.linalg.norm(point - first_point)
        + np.linalg.norm(point - second_point)
    )
    assert abs(covered - side_length) < tolerance


def make_tangency_marker(point, color):
    """One small solid dot per tangency, secondary to the construction."""
    marker = Dot(point=point, radius=0.035, color=color)
    marker.set_opacity(0.8)
    marker.set_z_index(20)
    return marker


class HeronFormula(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        # --- Exact construction data, validated before anything is drawn. ---
        touch_bc = foot_on_segment(POINT_B, POINT_C, INCENTER)
        touch_ab = foot_on_segment(POINT_A, POINT_B, INCENTER)
        touch_ca = foot_on_segment(POINT_C, POINT_A, INCENTER)
        validate_tangency(touch_bc, POINT_B, POINT_C)
        validate_tangency(touch_ab, POINT_A, POINT_B)
        validate_tangency(touch_ca, POINT_C, POINT_A)

        # Numeric check of the claim this video proves.
        semi_perimeter = (13 + 14 + 15) / 2
        heron_area = np.sqrt(
            semi_perimeter
            * (semi_perimeter - 13)
            * (semi_perimeter - 14)
            * (semi_perimeter - 15)
        )
        assert abs(heron_area - 84.0) < 1e-9
        assert abs(heron_area / semi_perimeter - RAW_INRADIUS) < 1e-9

        triangle = Polygon(
            POINT_A,
            POINT_B,
            POINT_C,
            color=ACCENT_CYAN,
            stroke_width=6,
        )
        triangle.set_fill(ACCENT_CYAN, opacity=0.08)
        triangle.set_z_index(2)

        # --- Beat 0.0-2.0 | Hook: three lengths, no angles. ---
        hook = Tex(
            r"\textbf{Solo los tres lados.\\ ¿Cuánto mide el área?}",
            font_size=42,
            color=WHITE,
        ).move_to(UP * 4.85)
        hook.set_z_index(30)
        fit_to_safe_width(hook)

        label_a = MathTex(r"14", font_size=36, color=ACCENT_CYAN)
        label_a.move_to(outside_segment(POINT_B, POINT_C, 0.42))
        label_b = MathTex(r"13", font_size=36, color=ACCENT_CYAN)
        label_b.move_to(outside_segment(POINT_C, POINT_A, 0.42))
        label_c = MathTex(r"15", font_size=36, color=ACCENT_CYAN)
        label_c.move_to(outside_segment(POINT_A, POINT_B, 0.42))
        side_labels = VGroup(label_a, label_b, label_c)
        side_labels.set_z_index(30)

        self.play(
            Create(triangle),
            FadeIn(hook, shift=UP * 0.12),
            run_time=0.9,
        )
        self.play(
            LaggedStart(
                *[FadeIn(label, scale=1.15) for label in side_labels],
                lag_ratio=0.18,
            ),
            run_time=0.9,
        )

        # --- Beat 2.0-7.0 | No angle, no height is allowed. ---
        forbidden_height = DashedLine(
            POINT_A,
            foot_on_segment(POINT_B, POINT_C, POINT_A),
            color=ACCENT_MAGENTA,
            stroke_width=4,
        )
        forbidden_height.set_z_index(3)
        forbidden_cross = Cross(
            forbidden_height,
            stroke_color=ACCENT_MAGENTA,
            stroke_width=6,
            scale_factor=0.55,
        )
        forbidden_cross.set_z_index(4)
        no_height_note = Tex(
            r"\textbf{Sin ángulos y sin altura}",
            font_size=34,
            color=ACCENT_MAGENTA,
        ).move_to(UP * 3.55)
        no_height_note.set_z_index(30)

        self.play(Create(forbidden_height), run_time=0.6)
        self.play(
            Create(forbidden_cross),
            FadeIn(no_height_note, shift=UP * 0.08),
            run_time=0.7,
        )
        self.wait(0.6)
        self.play(
            FadeOut(forbidden_height),
            FadeOut(forbidden_cross),
            FadeOut(no_height_note),
            run_time=0.5,
        )

        # --- Beat 7.0-13.0 | The inscribed circumference enters. ---
        incircle = Circle(radius=INRADIUS, color=ACCENT_YELLOW, stroke_width=6)
        incircle.move_to(INCENTER)
        incircle.set_z_index(5)
        incenter_dot = Dot(INCENTER, radius=0.05, color=ACCENT_YELLOW)
        incenter_dot.set_z_index(21)
        radius_line = Line(INCENTER, touch_bc, color=ACCENT_YELLOW, stroke_width=4)
        radius_line.set_z_index(6)
        radius_label = MathTex(r"r", font_size=32, color=ACCENT_YELLOW)
        radius_label.move_to(INCENTER + DOWN * 0.42 + LEFT * 0.32)
        radius_label.set_z_index(30)

        incircle_note = Tex(
            r"\textbf{Circunferencia inscrita}",
            font_size=34,
            color=ACCENT_YELLOW,
        ).move_to(UP * 3.55)
        incircle_note.set_z_index(30)

        self.play(
            ReplacementTransform(hook, incircle_note),
            Create(incircle),
            FadeIn(incenter_dot),
            run_time=1.0,
        )
        self.play(
            Create(radius_line),
            FadeIn(radius_label, shift=UP * 0.06),
            run_time=0.7,
        )

        markers = VGroup(
            make_tangency_marker(touch_bc, ACCENT_YELLOW),
            make_tangency_marker(touch_ab, ACCENT_YELLOW),
            make_tangency_marker(touch_ca, ACCENT_YELLOW),
        )
        self.play(
            LaggedStart(
                *[FadeIn(marker) for marker in markers],
                lag_ratio=0.2,
            ),
            run_time=0.8,
        )
        self.wait(0.4)

        # --- Beat 13.0-22.0 | Equal tangent pairs x, y, z. ---
        tangent_note = Tex(
            r"\textbf{Tangentes iguales desde cada vértice}",
            font_size=32,
            color=ACCENT_PURPLE,
        ).move_to(UP * 3.55)
        tangent_note.set_z_index(30)

        tangent_specs = (
            # (vertex, first touch, second touch, symbol, value, color)
            (POINT_A, touch_ab, touch_ca, r"x", r"x=7", ACCENT_MAGENTA),
            (POINT_B, touch_ab, touch_bc, r"y", r"y=8", ACCENT_PURPLE),
            (POINT_C, touch_bc, touch_ca, r"z", r"z=6", ACCENT_YELLOW),
        )
        tangent_groups = []
        for vertex, first_touch, second_touch, symbol, _, color in tangent_specs:
            first_segment = Line(vertex, first_touch, color=color, stroke_width=7)
            second_segment = Line(vertex, second_touch, color=color, stroke_width=7)
            first_segment.set_z_index(7)
            second_segment.set_z_index(7)
            first_label = MathTex(symbol, font_size=30, color=color)
            first_label.move_to(outside_segment(vertex, first_touch, 0.34))
            second_label = MathTex(symbol, font_size=30, color=color)
            second_label.move_to(outside_segment(vertex, second_touch, 0.34))
            first_label.set_z_index(30)
            second_label.set_z_index(30)
            tangent_groups.append(
                VGroup(first_segment, second_segment, first_label, second_label)
            )

        self.play(
            ReplacementTransform(incircle_note, tangent_note),
            FadeOut(side_labels),
            FadeOut(radius_line),
            FadeOut(radius_label),
            run_time=0.6,
        )
        for group in tangent_groups:
            self.play(FadeIn(group, shift=UP * 0.05), run_time=0.6)
        self.wait(0.5)

        # --- Beat 22.0-28.0 | The tangent lengths add up to s. ---
        sides_from_tangents = MathTex(
            r"y+z=14,\quad x+y=15,\quad x+z=13",
            font_size=30,
            color=WHITE,
        ).move_to(UP * 4.75)
        sides_from_tangents.set_z_index(30)
        fit_to_safe_width(sides_from_tangents)

        semi_line = MathTex(
            r"x+y+z",
            r"=",
            r"\frac{a+b+c}{2}",
            r"=",
            r"s=21",
            font_size=34,
        ).move_to(UP * 3.7)
        semi_line[0].set_color(ACCENT_PURPLE)
        semi_line[2].set_color(WHITE)
        semi_line[4].set_color(ACCENT_YELLOW)
        semi_line.set_z_index(30)
        fit_to_safe_width(semi_line)

        self.play(
            FadeOut(tangent_note),
            Write(sides_from_tangents),
            run_time=0.9,
        )
        self.play(Write(semi_line), run_time=1.0)
        self.play(
            Indicate(semi_line[4], color=ACCENT_YELLOW, scale_factor=1.12),
            run_time=1.0,
        )
        self.wait(0.5)

        # --- Beat 28.0-35.0 | Area = r * s. ---
        for group in tangent_groups:
            group.set_z_index(7)
        spokes = VGroup(
            Line(INCENTER, POINT_A, color=ACCENT_CYAN, stroke_width=3),
            Line(INCENTER, POINT_B, color=ACCENT_CYAN, stroke_width=3),
            Line(INCENTER, POINT_C, color=ACCENT_CYAN, stroke_width=3),
        )
        spokes.set_z_index(6)

        area_relation = MathTex(
            r"\text{Área}",
            r"=",
            r"r\,s",
            r"=",
            r"4\cdot 21=84",
            font_size=38,
        ).move_to(UP * 2.85)
        area_relation[0].set_color(WHITE)
        area_relation[2].set_color(ACCENT_YELLOW)
        area_relation[4].set_color(ACCENT_MAGENTA)
        area_relation.set_z_index(30)
        fit_to_safe_width(area_relation)

        self.play(
            FadeOut(VGroup(*tangent_groups)),
            Create(spokes),
            run_time=0.8,
        )
        self.play(Write(area_relation), run_time=1.0)
        self.wait(0.8)

        # --- Beat 35.0-42.0 | Heron's formula as the payoff. ---
        heron = MathTex(
            r"\text{Área}=\sqrt{s(s-a)(s-b)(s-c)}",
            font_size=36,
            color=WHITE,
        ).move_to(UP * 4.75)
        heron.set_z_index(30)
        fit_to_safe_width(heron)

        heron_numbers = MathTex(
            r"\sqrt{21\cdot 8\cdot 7\cdot 6}",
            r"=",
            r"84",
            font_size=40,
        ).move_to(UP * 3.75)
        heron_numbers[0].set_color(ACCENT_PURPLE)
        heron_numbers[1].set_color(WHITE)
        heron_numbers[2].set_color(ACCENT_MAGENTA)
        heron_numbers.set_z_index(30)
        fit_to_safe_width(heron_numbers)

        self.play(
            FadeOut(sides_from_tangents),
            FadeOut(semi_line),
            FadeOut(area_relation),
            FadeIn(heron, shift=UP * 0.1),
            run_time=0.9,
        )
        self.play(Write(heron_numbers), run_time=1.0)
        self.play(
            Circumscribe(heron_numbers, color=ACCENT_YELLOW, buff=0.14),
            run_time=1.2,
        )

        payoff = Tex(
            r"\textbf{El área sale de las tres longitudes}",
            font_size=32,
            color=WHITE,
        ).move_to(DOWN * 4.9)
        payoff.set_z_index(30)
        fit_to_safe_width(payoff)
        payoff_box = SurroundingRectangle(
            payoff,
            buff=0.2,
            corner_radius=0.12,
            stroke_width=3,
        )
        payoff_box.set_color_by_gradient(*GRADIENT_HIGHLIGHT)
        payoff_box.set_z_index(29)

        self.play(
            FadeIn(payoff, shift=UP * 0.1),
            Create(payoff_box),
            triangle.animate.set_fill(ACCENT_CYAN, opacity=0.20),
            run_time=0.9,
        )
        self.wait(1.4)

        animate_End(scene=self)
