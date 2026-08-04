from manim import *
from lnx import *

# proof-without-words | geometry | intermediate
#
# Pythagoras by similarity: the altitude from the right angle splits the
# triangle into two triangles similar to the parent. From a^2 = c*p and
# b^2 = c*q, with p + q = c, we get a^2 + b^2 = c(p + q) = c^2.

SAFE_WIDTH = 7.2

# Model space uses the 3-4-5 right triangle.
MODEL_A = np.array([0.0, 0.0, 0.0])
MODEL_B = np.array([5.0, 0.0, 0.0])
MODEL_C = np.array([3.2, 2.4, 0.0])
MODEL_H = np.array([3.2, 0.0, 0.0])
MODEL_CENTER = np.array([2.5, 1.2, 0.0])

GEOMETRY_SCALE = 1.25
GEOMETRY_ORIGIN = np.array([0.0, -1.0, 0.0])


def fit_to_safe_width(mobject):
    """Shrink a label so it never crosses the vertical safe area."""
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def to_scene(model_point):
    """Map a model-space point into the scene layout."""
    return GEOMETRY_ORIGIN + GEOMETRY_SCALE * (model_point - MODEL_CENTER)


A = to_scene(MODEL_A)
B = to_scene(MODEL_B)
C = to_scene(MODEL_C)
H = to_scene(MODEL_H)
FIGURE_CENTER = (A + B + C) / 3


def validate_construction(tolerance=1e-9):
    """Check the right angle and the two similarity relations before drawing."""
    side_a = np.linalg.norm(B - C)
    side_b = np.linalg.norm(A - C)
    side_c = np.linalg.norm(B - A)
    segment_p = np.linalg.norm(B - H)
    segment_q = np.linalg.norm(A - H)

    assert abs(np.dot(A - C, B - C)) < tolerance
    assert abs(np.dot(C - H, B - H)) < tolerance
    assert abs(side_a**2 - side_c * segment_p) < tolerance
    assert abs(side_b**2 - side_c * segment_q) < tolerance
    assert abs(segment_p + segment_q - side_c) < tolerance
    assert abs(side_a**2 + side_b**2 - side_c**2) < tolerance


def outside_segment(first_point, second_point, distance=0.42):
    """Return a label anchor on the outer side of a segment."""
    midpoint = (first_point + second_point) / 2
    direction = second_point - first_point
    normal = np.array([-direction[1], direction[0], 0.0])
    normal = normal / np.linalg.norm(normal)
    if np.dot(normal, midpoint - FIGURE_CENTER) < 0:
        normal = -normal
    return midpoint + normal * distance


def make_triangle(vertices, color, fill_opacity=0.0, stroke_width=6):
    """Build one triangle outline with the shared Lnx styling."""
    triangle = Polygon(*vertices, color=color, stroke_width=stroke_width)
    triangle.set_fill(color, opacity=fill_opacity)
    return triangle


class PythagorasSimilarTriangles(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        validate_construction()

        # Vertex order is the similarity correspondence:
        # (right angle, alpha vertex, beta vertex).
        parent_order = [C, A, B]
        left_child_order = [H, A, C]
        right_child_order = [H, C, B]

        parent = make_triangle(parent_order, ACCENT_CYAN)
        parent.set_z_index(4)

        # --- Beat 0.0-2.0 | hook: the triangle and its altitude appear at once.
        hook = Tex(
            r"\textbf{Tres triángulos, la misma forma}",
            font_size=42,
            color=WHITE,
        ).move_to(UP * 5.0)
        hook.set_stroke(width=1)
        hook.set_z_index(30)
        fit_to_safe_width(hook)

        right_angle_c = RightAngle(
            Line(C, A),
            Line(C, B),
            length=0.34,
            color=WHITE,
            stroke_width=4,
        )
        right_angle_c.set_z_index(6)

        self.play(
            Create(parent),
            FadeIn(hook, shift=UP * 0.12),
            run_time=1.1,
        )
        self.play(Create(right_angle_c), run_time=0.6)

        altitude = Line(C, H, color=ACCENT_PURPLE, stroke_width=6)
        altitude.set_z_index(5)
        right_angle_h = RightAngle(
            Line(H, C),
            Line(H, B),
            length=0.3,
            color=WHITE,
            stroke_width=4,
        )
        right_angle_h.set_z_index(6)
        foot_dot = Dot(H, radius=0.055, color=ACCENT_PURPLE)
        foot_dot.set_z_index(7)

        self.play(Create(altitude), run_time=0.7)
        self.play(FadeIn(foot_dot), Create(right_angle_h), run_time=0.5)

        # --- Beat 2.5-8.5 | setup: name the sides outside the figure.
        label_a = MathTex("a", font_size=38, color=ACCENT_MAGENTA)
        label_a.move_to(outside_segment(C, B))
        label_b = MathTex("b", font_size=38, color=ACCENT_YELLOW)
        label_b.move_to(outside_segment(A, C))
        label_c = MathTex("c", font_size=38, color=ACCENT_CYAN)
        label_c.move_to(outside_segment(A, B))
        label_h = MathTex("h", font_size=34, color=ACCENT_PURPLE)
        label_h.move_to(H + LEFT * 0.42 + UP * 0.7)
        for label in (label_a, label_b, label_c, label_h):
            label.set_stroke(width=1)
            label.set_z_index(30)

        self.play(
            LaggedStart(
                FadeIn(label_c, shift=DOWN * 0.08),
                FadeIn(label_a, shift=RIGHT * 0.08),
                FadeIn(label_b, shift=LEFT * 0.08),
                FadeIn(label_h, shift=LEFT * 0.08),
                lag_ratio=0.25,
            ),
            run_time=1.4,
        )
        self.wait(0.5)

        # --- Beat 8.5-16.0 | the altitude splits the triangle in two children.
        left_child = make_triangle(
            left_child_order,
            ACCENT_YELLOW,
            fill_opacity=0.24,
            stroke_width=5,
        )
        left_child.set_z_index(3)
        right_child = make_triangle(
            right_child_order,
            ACCENT_MAGENTA,
            fill_opacity=0.24,
            stroke_width=5,
        )
        right_child.set_z_index(3)

        split_note = Tex(
            r"\textbf{La altura crea dos triángulos semejantes}",
            font_size=32,
            color=WHITE,
        ).move_to(UP * 4.1)
        split_note.set_stroke(width=1)
        split_note.set_z_index(30)
        fit_to_safe_width(split_note)

        self.play(
            FadeIn(left_child),
            FadeIn(right_child),
            FadeIn(split_note, shift=UP * 0.08),
            run_time=1.0,
        )
        self.wait(0.6)

        # Three copies travel to a row where they share one common size.
        slot_width = 1.95
        slot_y = -1.15
        slot_positions = (
            np.array([-2.35, slot_y, 0.0]),
            np.array([0.0, slot_y, 0.0]),
            np.array([2.35, slot_y, 0.0]),
        )
        slot_colors = (ACCENT_CYAN, ACCENT_YELLOW, ACCENT_MAGENTA)

        travelling = VGroup(
            make_triangle(parent_order, ACCENT_CYAN, 0.20, 5),
            left_child.copy(),
            right_child.copy(),
        )
        travelling.set_z_index(8)

        slot_targets = VGroup()
        for position, color in zip(slot_positions, slot_colors):
            target = make_triangle(parent_order, color, 0.20, 5)
            target.scale_to_fit_width(slot_width)
            target.move_to(position)
            target.set_z_index(8)
            slot_targets.add(target)

        figure_group = VGroup(
            parent,
            altitude,
            right_angle_c,
            right_angle_h,
            foot_dot,
            left_child,
            right_child,
            label_a,
            label_b,
            label_c,
            label_h,
        )

        self.add(travelling)
        self.play(
            FadeOut(figure_group),
            *[
                Transform(source, target)
                for source, target in zip(travelling, slot_targets)
            ],
            run_time=1.8,
        )

        slot_captions = VGroup()
        for caption_text, position, color in zip(
            (r"padre", r"hijo\ 1", r"hijo\ 2"),
            slot_positions,
            slot_colors,
        ):
            caption = MathTex(
                rf"\text{{{caption_text}}}",
                font_size=28,
                color=color,
            ).move_to(position + DOWN * 1.35)
            caption.set_stroke(width=1)
            caption.set_z_index(30)
            slot_captions.add(caption)

        same_shape = Tex(
            r"\textbf{Copias a escala del original}",
            font_size=34,
            color=ACCENT_YELLOW,
        ).move_to(DOWN * 3.4)
        same_shape.set_stroke(width=1)
        same_shape.set_z_index(30)
        fit_to_safe_width(same_shape)

        self.play(
            FadeIn(slot_captions, shift=UP * 0.08),
            FadeIn(same_shape, shift=UP * 0.1),
            run_time=0.8,
        )
        self.play(
            LaggedStart(
                *[
                    Indicate(triangle, color=WHITE, scale_factor=1.07)
                    for triangle in travelling
                ],
                lag_ratio=0.22,
            ),
            run_time=1.6,
        )
        self.wait(0.5)

        # --- Beat 16.0-24.0 | back to the figure with p and q on the hypotenuse.
        segment_q = Line(A, H, color=ACCENT_YELLOW, stroke_width=9)
        segment_q.set_z_index(5)
        segment_p = Line(H, B, color=ACCENT_MAGENTA, stroke_width=9)
        segment_p.set_z_index(5)
        label_q = MathTex("q", font_size=36, color=ACCENT_YELLOW)
        label_q.move_to((A + H) / 2 + DOWN * 0.42)
        label_p = MathTex("p", font_size=36, color=ACCENT_MAGENTA)
        label_p.move_to((H + B) / 2 + DOWN * 0.42)
        for label in (label_q, label_p):
            label.set_stroke(width=1)
            label.set_z_index(30)

        figure_back = VGroup(
            parent,
            altitude,
            right_angle_c,
            right_angle_h,
            foot_dot,
            label_a,
            label_b,
            label_h,
        )

        self.play(
            FadeOut(travelling),
            FadeOut(slot_captions),
            FadeOut(same_shape),
            FadeOut(split_note),
            FadeOut(hook),
            FadeIn(figure_back),
            run_time=0.9,
        )
        self.play(
            Create(segment_q),
            Create(segment_p),
            FadeIn(label_q, shift=DOWN * 0.06),
            FadeIn(label_p, shift=DOWN * 0.06),
            run_time=0.9,
        )

        ratio_left = MathTex(
            r"\frac{b}{c}=\frac{q}{b}",
            r"\;\Rightarrow\;",
            r"b^2=c\,q",
            font_size=38,
        ).move_to(UP * 4.55)
        ratio_left[0].set_color(WHITE)
        ratio_left[1].set_color(WHITE)
        ratio_left[2].set_color(ACCENT_YELLOW)
        ratio_right = MathTex(
            r"\frac{a}{c}=\frac{p}{a}",
            r"\;\Rightarrow\;",
            r"a^2=c\,p",
            font_size=38,
        ).move_to(UP * 3.65)
        ratio_right[0].set_color(WHITE)
        ratio_right[1].set_color(WHITE)
        ratio_right[2].set_color(ACCENT_MAGENTA)
        for ratio in (ratio_left, ratio_right):
            ratio.set_stroke(width=1)
            ratio.set_z_index(30)
            fit_to_safe_width(ratio)

        self.play(Write(ratio_left), run_time=1.1)
        self.play(Write(ratio_right), run_time=1.1)
        self.wait(0.8)

        # --- Beat 24.0-31.0 | add both relations and use p + q = c.
        split_identity = MathTex(
            r"p+q=c",
            font_size=38,
            color=ACCENT_CYAN,
        ).move_to(UP * 2.75)
        split_identity.set_stroke(width=1)
        split_identity.set_z_index(30)

        self.play(
            FadeIn(split_identity, shift=UP * 0.08),
            Indicate(segment_q, color=ACCENT_YELLOW, scale_factor=1.0),
            Indicate(segment_p, color=ACCENT_MAGENTA, scale_factor=1.0),
            run_time=1.2,
        )
        self.wait(0.6)

        sum_step = MathTex(
            r"a^2+b^2",
            r"=",
            r"c\,(p+q)",
            font_size=44,
        ).move_to(UP * 4.15)
        sum_step[0].set_color(WHITE)
        sum_step[1].set_color(ACCENT_YELLOW)
        sum_step[2].set_color(ACCENT_CYAN)
        sum_step.set_stroke(width=1)
        sum_step.set_z_index(30)
        fit_to_safe_width(sum_step)

        self.play(
            FadeOut(ratio_left),
            FadeOut(ratio_right),
            FadeOut(split_identity),
            FadeIn(sum_step, shift=UP * 0.1),
            run_time=1.0,
        )
        self.wait(0.8)

        # --- Beat 31.0-40.0 | payoff.
        result = MathTex(
            r"a^2+b^2",
            r"=",
            r"c^2",
            font_size=56,
        ).move_to(UP * 4.15)
        result[0].set_color(WHITE)
        result[1].set_color(ACCENT_YELLOW)
        result[2].set_color(ACCENT_CYAN)
        result.set_stroke(width=1)
        result.set_z_index(30)

        self.play(TransformMatchingTex(sum_step, result), run_time=1.3)
        self.play(
            Indicate(result, color=ACCENT_YELLOW, scale_factor=1.08),
            run_time=1.2,
        )

        payoff = Tex(
            r"\textbf{Semejanza: la prueba más corta}",
            font_size=34,
            color=WHITE,
        ).move_to(DOWN * 4.6)
        payoff.set_stroke(width=1)
        payoff.set_z_index(30)
        fit_to_safe_width(payoff)
        payoff_box = SurroundingRectangle(
            payoff,
            color=ACCENT_YELLOW,
            buff=0.22,
            corner_radius=0.12,
            stroke_width=3,
        )
        payoff_box.set_color_by_gradient(*GRADIENT_HIGHLIGHT)
        payoff_box.set_z_index(29)

        self.play(
            FadeIn(payoff, shift=UP * 0.1),
            Create(payoff_box),
            run_time=0.8,
        )
        self.play(
            payoff_box.animate.set_stroke(width=5),
            rate_func=there_and_back,
            run_time=1.1,
        )
        self.wait(1.2)

        animate_End(scene=self)
