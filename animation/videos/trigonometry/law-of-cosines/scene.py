from manim import *
from lnx import *

# visual-derivation | trigonometry | intermediate
# Law of Cosines:  c^2 = a^2 + b^2 - 2ab*cos(C).
#
# Derivation shown on screen: drop the altitude h from vertex A onto side CB.
# It splits the triangle into two right triangles that share h, so Pythagoras
# can be applied twice:
#   left  triangle:  h = b*sin(C),  CH = b*cos(C)
#   right triangle:  c^2 = h^2 + (a - b*cos(C))^2
# Expanding and using sin^2 + cos^2 = 1 collapses everything into
#   c^2 = a^2 + b^2 - 2ab*cos(C).
# When C = 90 degrees, cos(C) = 0 and the correction term vanishes, leaving the
# Pythagorean theorem.
#
# The actual frame is 9 x 16 units (x in [-4.5, 4.5], y in [-8, 8]).
# Safe area: |x| <= 3.8 and |y| <= 5.6.

SAFE_WIDTH = 7.2


def fit_to_safe_width(mobject):
    """Shrink a mobject so it never crosses the horizontal safe margins."""
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def make_label(tex, font_size, color, with_background=False):
    """Create a MathTex label placed above the geometry with explicit z_index."""
    label = MathTex(tex, font_size=font_size, color=color)
    if with_background:
        label.add_background_rectangle(color=BG, opacity=0.92, buff=0.06)
    label.set_z_index(12)
    return label


class LawOfCosines(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        SIDE_A = ACCENT_CYAN       # side a = CB
        SIDE_B = ACCENT_YELLOW     # side b = CA
        SIDE_C = ACCENT_MAGENTA    # side c = AB, the unknown
        HEIGHT_COLOR = ACCENT_PURPLE
        TRI_COLOR = ACCENT_PURPLE

        # ------------------------------------------------------------ geometry
        # A scalene triangle with the studied angle C on the left vertex.
        base_y = 0.55
        C = np.array([-1.90, base_y, 0.0])
        B = np.array([2.30, base_y, 0.0])
        angle_C = 55 * DEGREES
        b_len = 2.80
        A = C + b_len * np.array([np.cos(angle_C), np.sin(angle_C), 0.0])
        H = np.array([A[0], base_y, 0.0])  # foot of the altitude from A

        triangle = Polygon(
            A, B, C,
            color=TRI_COLOR, stroke_width=5,
            fill_color=TRI_COLOR, fill_opacity=0.07,
        )
        side_a = Line(C, B, color=SIDE_A, stroke_width=6).set_z_index(4)
        side_b = Line(C, A, color=SIDE_B, stroke_width=6).set_z_index(4)
        side_c = Line(A, B, color=SIDE_C, stroke_width=6).set_z_index(4)

        vertex_dots = VGroup(*[Dot(P, color=WHITE, radius=0.06) for P in (A, B, C)])
        vertex_dots.set_z_index(11)
        vertex_labels = VGroup(
            make_label("A", 30, WHITE).move_to(A + UP * 0.34),
            make_label("B", 30, WHITE).move_to(B + RIGHT * 0.30 + DOWN * 0.10),
            make_label("C", 30, WHITE).move_to(C + LEFT * 0.32 + DOWN * 0.10),
        )

        # Length labels live outside the figure, never on top of a line.
        label_a = make_label("a", 34, SIDE_A).move_to((C + B) / 2 + DOWN * 0.85)
        label_b = make_label("b", 34, SIDE_B).move_to((C + A) / 2 + LEFT * 0.45)
        label_c = make_label("c", 34, SIDE_C).move_to((A + B) / 2 + RIGHT * 0.45)

        # --------------------------------------------------------- hook 0-2 s
        title = Tex(r"Ley de Cosenos", font_size=60, color=WHITE)
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

        self.play(Write(title), run_time=0.7)
        self.play(
            Create(underline),
            Create(triangle),
            FadeIn(vertex_dots),
            run_time=0.9,
        )
        self.play(Write(vertex_labels), run_time=0.4)

        # ---------------------------------------------------- sides and angle
        arc_C = Angle(Line(C, B), Line(C, A), radius=0.60, color=WHITE, stroke_width=4)
        arc_C.set_z_index(6)
        angle_label = make_label("C", 30, WHITE).move_to(
            Angle(Line(C, B), Line(C, A), radius=1.00).point_from_proportion(0.5)
        )

        self.play(
            Create(side_a), Create(side_b), Create(side_c),
            run_time=0.8,
        )
        self.play(
            Write(label_a), Write(label_b), Write(label_c),
            Create(arc_C), Write(angle_label),
            run_time=0.8,
        )
        self.wait(0.4)

        # The unknown is c: everything below exists to measure it.
        question = MathTex(r"c^{2} = \;?", font_size=44, color=SIDE_C)
        question.set_z_index(20)
        question.move_to(np.array([0.0, -1.55, 0.0]))
        self.play(Write(question), run_time=0.6)
        self.wait(1.0)

        # ------------------------------------------------------- the altitude
        altitude = DashedLine(A, H, color=HEIGHT_COLOR, stroke_width=5)
        altitude.set_z_index(5)
        foot_dot = Dot(H, color=WHITE, radius=0.055).set_z_index(11)
        right_angle = RightAngle(
            Line(H, A), Line(H, B), length=0.26, color=WHITE, stroke_width=4
        )
        right_angle.set_z_index(7)
        label_h = make_label("h", 30, HEIGHT_COLOR, with_background=True).move_to(
            (A + H) / 2 + LEFT * 0.32
        )

        self.play(
            Create(altitude), FadeIn(foot_dot),
            Create(right_angle), Write(label_h),
            run_time=0.9,
        )
        self.wait(0.3)

        # The foot of the altitude cuts side a into b*cos(C) and a - b*cos(C).
        brace_left = BraceBetweenPoints(H, C, direction=DOWN, color=SIDE_B)
        brace_right = BraceBetweenPoints(B, H, direction=DOWN, color=SIDE_A)
        seg_left = MathTex(r"b\cos C", font_size=30, color=SIDE_B)
        seg_right = MathTex(r"a - b\cos C", font_size=30, color=SIDE_A)
        seg_left.set_z_index(12).next_to(brace_left, DOWN, buff=0.10)
        seg_right.set_z_index(12).next_to(brace_right, DOWN, buff=0.10)

        self.play(
            FadeOut(label_a),
            GrowFromCenter(brace_left), GrowFromCenter(brace_right),
            run_time=0.7,
        )
        self.play(Write(seg_left), Write(seg_right), run_time=0.8)
        self.wait(0.4)

        # --------------------------------------------- Pythagoras twice
        step_1 = MathTex(r"h = b\,\sin C", font_size=38, color=HEIGHT_COLOR)
        step_1.set_z_index(20).move_to(np.array([0.0, -2.55, 0.0]))
        fit_to_safe_width(step_1)

        step_2 = MathTex(
            r"c^{2} = h^{2} + (a - b\cos C)^{2}", font_size=38, color=WHITE
        )
        step_2.set_z_index(20).move_to(np.array([0.0, -3.45, 0.0]))
        fit_to_safe_width(step_2)

        self.play(ReplacementTransform(question, step_1), run_time=0.8)
        self.play(Write(step_2), run_time=1.0)
        self.wait(1.1)

        step_3 = MathTex(
            r"c^{2} = b^{2}\sin^{2} C + a^{2} - 2ab\cos C + b^{2}\cos^{2} C",
            font_size=30, color=WHITE,
        )
        step_3.set_z_index(20).move_to(np.array([0.0, -4.35, 0.0]))
        fit_to_safe_width(step_3)
        self.play(Write(step_3), run_time=1.1)
        self.wait(1.0)

        identity = MathTex(
            r"\sin^{2} C + \cos^{2} C = 1", font_size=30, color=ACCENT_YELLOW
        )
        identity.set_z_index(20).move_to(np.array([0.0, -5.05, 0.0]))
        fit_to_safe_width(identity)
        self.play(FadeIn(identity, shift=UP * 0.2), run_time=0.6)
        self.wait(0.6)

        # ------------------------------------------------------------- payoff
        result = MathTex(
            r"c^{2} = a^{2} + b^{2} - 2ab\cos C", font_size=42,
        )
        result.set_color_by_tex("c", WHITE)
        result.set_z_index(21).move_to(np.array([0.0, -3.30, 0.0]))
        fit_to_safe_width(result)

        self.play(
            FadeOut(step_1), FadeOut(identity),
            ReplacementTransform(VGroup(step_2, step_3), result),
            run_time=1.2,
        )
        result_box = SurroundingRectangle(result, buff=0.20, corner_radius=0.12)
        result_box.set_stroke(width=4, color=GRADIENT_HIGHLIGHT)
        result_box.set_z_index(20)
        self.play(Create(result_box), run_time=0.7)
        self.wait(1.4)

        # ------------------------------- the right-angle case gives Pythagoras
        note = Tex(r"Si $C = 90^\circ$, el término se anula", font_size=32, color=WHITE)
        note.set_z_index(20).move_to(np.array([0.0, -4.60, 0.0]))
        fit_to_safe_width(note)
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.6)

        # Highlight the correction term, then collapse it to zero.
        correction = result[0][-8:]
        self.play(Indicate(correction, color=ACCENT_MAGENTA, scale_factor=1.25),
                  run_time=0.8)

        pythagoras = MathTex(r"c^{2} = a^{2} + b^{2}", font_size=46, color=ACCENT_CYAN)
        pythagoras.set_z_index(21).move_to(result.get_center())
        pythagoras_box = SurroundingRectangle(
            pythagoras, buff=0.20, corner_radius=0.12
        )
        pythagoras_box.set_stroke(width=4, color=GRADIENT_HIGHLIGHT)
        pythagoras_box.set_z_index(20)

        self.play(
            TransformMatchingShapes(result, pythagoras),
            ReplacementTransform(result_box, pythagoras_box),
            run_time=1.1,
        )
        self.wait(1.6)

        animate_End(scene=self)
