from manim import *
from lnx import *

# proof-without-words | geometry | basic
# Mathematical reference:
# https://mathworld.wolfram.com/InscribedAngle.html
#
# Configuration: chord AB subtends a 120 deg central arc, so every inscribed
# angle standing on the same arc measures exactly 60 deg.

SAFE_WIDTH = 7.2

CENTER = np.array([0.0, -0.5, 0.0])
RADIUS = 2.4

A_DEG = 210.0
B_DEG = 330.0
CENTRAL_DEG = 120.0
INSCRIBED_DEG = 60.0

# Vertex sweep along the major arc, far from A and B.
VERTEX_START_DEG = 135.0
VERTEX_MID_DEG = 90.0
VERTEX_END_DEG = 45.0


def circle_point(degrees):
    """Return the point of the circumference at the given polar angle."""
    radians = np.radians(degrees)
    return CENTER + RADIUS * np.array([np.cos(radians), np.sin(radians), 0.0])


def fit_to_safe_width(mobject):
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def inscribed_angle_degrees(vertex_degrees):
    """Measure the inscribed angle APB for a vertex on the major arc."""
    vertex = circle_point(vertex_degrees)
    first = circle_point(A_DEG) - vertex
    second = circle_point(B_DEG) - vertex
    cosine = np.dot(first, second) / (
        np.linalg.norm(first) * np.linalg.norm(second)
    )
    return np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))


def validate_configuration(tolerance=1e-9):
    """The inscribed angle must be constant and half of the central angle."""
    for sample in (VERTEX_START_DEG, VERTEX_MID_DEG, VERTEX_END_DEG, 110.0, 70.0):
        assert abs(inscribed_angle_degrees(sample) - INSCRIBED_DEG) < 1e-7
    assert abs(CENTRAL_DEG - 2 * INSCRIBED_DEG) < tolerance


validate_configuration()

POINT_A = circle_point(A_DEG)
POINT_B = circle_point(B_DEG)
# Antipode of the top vertex: it lies on the subtended arc and splits the proof.
POINT_Q = circle_point(VERTEX_MID_DEG + 180.0)


class InscribedAngle(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.13
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.8)
        self.add(watermark)

        circumference = Circle(radius=RADIUS, color=GREY_B, stroke_width=4)
        circumference.move_to(CENTER)

        chord = Line(POINT_A, POINT_B, color=ACCENT_MAGENTA, stroke_width=7)
        dot_a = Dot(POINT_A, radius=0.07, color=ACCENT_MAGENTA)
        dot_b = Dot(POINT_B, radius=0.07, color=ACCENT_MAGENTA)
        label_a = MathTex("A", font_size=32, color=ACCENT_MAGENTA)
        label_a.next_to(dot_a, DL, buff=0.18)
        label_b = MathTex("B", font_size=32, color=ACCENT_MAGENTA)
        label_b.next_to(dot_b, DR, buff=0.18)
        for label in (label_a, label_b):
            label.set_z_index(30)

        # Hook: two different observers, one identical angle.
        first_vertex = circle_point(VERTEX_START_DEG)
        second_vertex = circle_point(VERTEX_END_DEG)

        def observer_group(vertex, color, name, label_direction):
            legs = VGroup(
                Line(vertex, POINT_A, color=color, stroke_width=5),
                Line(vertex, POINT_B, color=color, stroke_width=5),
            )
            mark = Angle(
                Line(vertex, POINT_A),
                Line(vertex, POINT_B),
                radius=0.52,
                color=color,
                stroke_width=5,
            )
            dot = Dot(vertex, radius=0.08, color=color)
            tag = MathTex(name, font_size=32, color=color)
            tag.next_to(dot, label_direction, buff=0.22)
            tag.set_z_index(30)
            return VGroup(legs, mark, dot, tag)

        observer_one = observer_group(
            first_vertex, ACCENT_CYAN, "P_1", UL
        )
        observer_two = observer_group(
            second_vertex, ACCENT_YELLOW, "P_2", UR
        )

        hook = Tex(
            r"\textbf{Dos miradas, el mismo ángulo}",
            font_size=40,
            color=WHITE,
        ).move_to(UP * 5.0)
        hook.set_z_index(30)
        fit_to_safe_width(hook)

        self.play(
            Create(circumference),
            FadeIn(hook, shift=UP * 0.12),
            run_time=0.7,
        )
        self.play(
            Create(chord),
            FadeIn(dot_a),
            FadeIn(dot_b),
            FadeIn(label_a),
            FadeIn(label_b),
            run_time=0.6,
        )
        self.play(
            LaggedStart(
                FadeIn(observer_one),
                FadeIn(observer_two),
                lag_ratio=0.35,
            ),
            run_time=0.9,
        )

        equal_note = MathTex(
            r"\angle AP_1B = \angle AP_2B = 60^\circ",
            font_size=34,
            color=WHITE,
        ).move_to(UP * 4.1)
        equal_note.set_z_index(30)
        fit_to_safe_width(equal_note)
        self.play(Write(equal_note), run_time=0.8)
        self.play(
            Indicate(equal_note, color=ACCENT_YELLOW, scale_factor=1.06),
            run_time=1.1,
        )
        self.wait(0.7)

        # Beat: a single vertex slides along the arc and the angle never moves.
        vertex_tracker = ValueTracker(VERTEX_START_DEG)

        moving_dot = always_redraw(
            lambda: Dot(
                circle_point(vertex_tracker.get_value()),
                radius=0.09,
                color=ACCENT_CYAN,
            )
        )
        moving_legs = always_redraw(
            lambda: VGroup(
                Line(
                    circle_point(vertex_tracker.get_value()),
                    POINT_A,
                    color=ACCENT_CYAN,
                    stroke_width=5,
                ),
                Line(
                    circle_point(vertex_tracker.get_value()),
                    POINT_B,
                    color=ACCENT_CYAN,
                    stroke_width=5,
                ),
            )
        )
        moving_mark = always_redraw(
            lambda: Angle(
                Line(circle_point(vertex_tracker.get_value()), POINT_A),
                Line(circle_point(vertex_tracker.get_value()), POINT_B),
                radius=0.52,
                color=ACCENT_CYAN,
                stroke_width=5,
            )
        )
        moving_label = always_redraw(
            lambda: MathTex("P", font_size=32, color=ACCENT_CYAN)
            .next_to(
                circle_point(vertex_tracker.get_value()),
                normalize(
                    circle_point(vertex_tracker.get_value()) - CENTER
                ),
                buff=0.2,
            )
            .set_z_index(30)
        )

        live_readout = always_redraw(
            lambda: MathTex(
                r"\angle APB = "
                + f"{inscribed_angle_degrees(vertex_tracker.get_value()):.0f}"
                + r"^\circ",
                font_size=36,
                color=ACCENT_CYAN,
            )
            .move_to(UP * 4.1)
            .set_z_index(30)
        )

        self.play(
            FadeOut(observer_two),
            FadeOut(observer_one),
            FadeOut(equal_note),
            FadeIn(moving_dot),
            FadeIn(moving_legs),
            FadeIn(moving_mark),
            FadeIn(moving_label),
            FadeIn(live_readout),
            run_time=0.7,
        )

        move_note = Tex(
            r"\textbf{Mueve el vértice: el ángulo no cambia}",
            font_size=32,
            color=WHITE,
        ).move_to(UP * 5.0)
        move_note.set_z_index(30)
        fit_to_safe_width(move_note)
        self.play(ReplacementTransform(hook, move_note), run_time=0.5)

        self.play(
            vertex_tracker.animate.set_value(VERTEX_END_DEG),
            run_time=2.2,
            rate_func=smooth,
        )
        self.play(
            vertex_tracker.animate.set_value(VERTEX_MID_DEG),
            run_time=1.6,
            rate_func=smooth,
        )
        self.wait(0.5)

        # Beat: the subtended arc is what the angle really depends on.
        subtended_arc = Arc(
            radius=RADIUS,
            start_angle=np.radians(A_DEG),
            angle=np.radians(CENTRAL_DEG),
            arc_center=CENTER,
            color=ACCENT_MAGENTA,
            stroke_width=11,
        )
        subtended_arc.set_z_index(5)
        arc_note = Tex(
            r"\textbf{Todos ven el mismo arco}",
            font_size=32,
            color=ACCENT_MAGENTA,
        ).move_to(DOWN * 4.35)
        arc_note.set_z_index(30)
        fit_to_safe_width(arc_note)

        self.play(
            Create(subtended_arc),
            FadeIn(arc_note, shift=UP * 0.1),
            run_time=0.9,
        )
        self.wait(0.6)

        # Beat: the central angle standing on that very same arc.
        center_dot = Dot(CENTER, radius=0.07, color=WHITE)
        label_o = MathTex("O", font_size=30, color=WHITE)
        label_o.next_to(center_dot, RIGHT, buff=0.16)
        label_o.set_z_index(30)
        radius_a = Line(CENTER, POINT_A, color=ACCENT_PURPLE, stroke_width=6)
        radius_b = Line(CENTER, POINT_B, color=ACCENT_PURPLE, stroke_width=6)
        central_mark = Angle(
            Line(CENTER, POINT_A),
            Line(CENTER, POINT_B),
            radius=0.75,
            color=ACCENT_PURPLE,
            stroke_width=6,
            other_angle=True,
        )
        central_label = MathTex(r"120^\circ", font_size=34, color=ACCENT_PURPLE)
        central_label.move_to(CENTER + DOWN * 1.28)
        central_label.set_z_index(30)

        central_note = Tex(
            r"\textbf{Ángulo central sobre el mismo arco}",
            font_size=30,
            color=ACCENT_PURPLE,
        ).move_to(UP * 5.0)
        central_note.set_z_index(30)
        fit_to_safe_width(central_note)

        self.play(
            ReplacementTransform(move_note, central_note),
            FadeIn(center_dot),
            FadeIn(label_o),
            Create(radius_a),
            Create(radius_b),
            run_time=0.8,
        )
        self.play(
            Create(central_mark),
            FadeIn(central_label, shift=UP * 0.08),
            run_time=0.7,
        )
        self.wait(0.6)

        relation = MathTex(
            r"60^\circ",
            r"=",
            r"\tfrac{1}{2}\cdot 120^\circ",
            font_size=40,
        ).move_to(UP * 4.1)
        relation[0].set_color(ACCENT_CYAN)
        relation[1].set_color(WHITE)
        relation[2].set_color(ACCENT_PURPLE)
        relation.set_z_index(30)
        fit_to_safe_width(relation)

        self.play(
            FadeOut(live_readout),
            FadeIn(relation, shift=UP * 0.1),
            run_time=0.6,
        )
        self.wait(0.7)

        # Beat: the isosceles proof with the exterior-angle step.
        static_vertex = circle_point(VERTEX_MID_DEG)
        leg_pa = Line(static_vertex, POINT_A, color=ACCENT_CYAN, stroke_width=5)
        leg_pb = Line(static_vertex, POINT_B, color=ACCENT_CYAN, stroke_width=5)
        static_dot = Dot(static_vertex, radius=0.09, color=ACCENT_CYAN)
        static_label = MathTex("P", font_size=32, color=ACCENT_CYAN)
        static_label.next_to(static_dot, UP, buff=0.2)
        static_label.set_z_index(30)
        static_mark = Angle(
            Line(static_vertex, POINT_A),
            Line(static_vertex, POINT_B),
            radius=0.52,
            color=ACCENT_CYAN,
            stroke_width=5,
        )

        self.remove(moving_dot, moving_legs, moving_mark, moving_label)
        self.add(leg_pa, leg_pb, static_mark, static_dot, static_label)

        diameter = DashedLine(
            static_vertex,
            POINT_Q,
            color=ACCENT_YELLOW,
            stroke_width=5,
            dash_length=0.14,
        )
        dot_q = Dot(POINT_Q, radius=0.07, color=ACCENT_YELLOW)
        label_q = MathTex("Q", font_size=30, color=ACCENT_YELLOW)
        label_q.next_to(dot_q, DOWN, buff=0.18)
        label_q.set_z_index(30)

        proof_note = Tex(
            r"\textbf{Triángulos isósceles: } $OA=OB=OP=r$",
            font_size=30,
            color=WHITE,
        ).move_to(UP * 5.0)
        proof_note.set_z_index(30)
        fit_to_safe_width(proof_note)

        radius_p = Line(CENTER, static_vertex, color=ACCENT_PURPLE, stroke_width=6)

        self.play(
            ReplacementTransform(central_note, proof_note),
            FadeOut(arc_note),
            Create(radius_p),
            run_time=0.7,
        )
        self.play(
            Create(diameter),
            FadeIn(dot_q),
            FadeIn(label_q),
            run_time=0.7,
        )

        alpha_at_p = Angle(
            Line(static_vertex, POINT_A),
            Line(static_vertex, POINT_Q),
            radius=0.95,
            color=ACCENT_YELLOW,
            stroke_width=5,
        )
        alpha_at_a = Angle(
            Line(POINT_A, POINT_Q),
            Line(POINT_A, static_vertex),
            radius=0.55,
            color=ACCENT_YELLOW,
            stroke_width=5,
        )
        alpha_label_p = MathTex(r"\alpha", font_size=32, color=ACCENT_YELLOW)
        alpha_label_p.move_to(static_vertex + np.array([-0.72, -0.82, 0.0]))
        alpha_label_p.set_z_index(30)
        alpha_label_a = MathTex(r"\alpha", font_size=32, color=ACCENT_YELLOW)
        alpha_label_a.next_to(dot_a, UR, buff=0.42)
        alpha_label_a.set_z_index(30)

        exterior_step = MathTex(
            r"\angle AOQ = \alpha + \alpha = 2\alpha",
            font_size=34,
            color=ACCENT_YELLOW,
        ).move_to(UP * 4.1)
        exterior_step.set_z_index(30)
        fit_to_safe_width(exterior_step)

        self.play(
            FadeOut(relation),
            Create(alpha_at_p),
            Create(alpha_at_a),
            FadeIn(alpha_label_p),
            FadeIn(alpha_label_a),
            run_time=0.9,
        )
        self.play(Write(exterior_step), run_time=0.9)
        self.wait(0.8)

        symmetry_step = MathTex(
            r"\angle QOB = 2\beta",
            r"\quad\Longrightarrow\quad",
            r"\angle AOB = 2(\alpha+\beta)",
            font_size=30,
        ).move_to(UP * 4.1)
        symmetry_step[0].set_color(ACCENT_YELLOW)
        symmetry_step[1].set_color(WHITE)
        symmetry_step[2].set_color(ACCENT_PURPLE)
        symmetry_step.set_z_index(30)
        fit_to_safe_width(symmetry_step)

        beta_at_p = Angle(
            Line(static_vertex, POINT_Q),
            Line(static_vertex, POINT_B),
            radius=0.95,
            color=ACCENT_YELLOW,
            stroke_width=5,
        )
        beta_at_b = Angle(
            Line(POINT_B, static_vertex),
            Line(POINT_B, POINT_Q),
            radius=0.55,
            color=ACCENT_YELLOW,
            stroke_width=5,
        )
        beta_label_p = MathTex(r"\beta", font_size=32, color=ACCENT_YELLOW)
        beta_label_p.move_to(static_vertex + np.array([0.72, -0.82, 0.0]))
        beta_label_p.set_z_index(30)
        beta_label_b = MathTex(r"\beta", font_size=32, color=ACCENT_YELLOW)
        beta_label_b.next_to(dot_b, UL, buff=0.42)
        beta_label_b.set_z_index(30)

        self.play(
            ReplacementTransform(exterior_step, symmetry_step),
            Create(beta_at_p),
            Create(beta_at_b),
            FadeIn(beta_label_p),
            FadeIn(beta_label_b),
            run_time=1.0,
        )
        self.wait(0.9)

        # Payoff: the general statement of the inscribed angle theorem.
        payoff_group = VGroup(
            alpha_at_p,
            alpha_at_a,
            beta_at_p,
            beta_at_b,
            alpha_label_p,
            alpha_label_a,
            beta_label_p,
            beta_label_b,
            diameter,
            dot_q,
            label_q,
        )

        theorem_title = Tex(
            r"\textbf{Teorema del ángulo inscrito}",
            font_size=36,
            color=ACCENT_CYAN,
        ).move_to(UP * 5.0)
        theorem_title.set_z_index(30)
        fit_to_safe_width(theorem_title)

        theorem = MathTex(
            r"\angle APB",
            r"=",
            r"\tfrac{1}{2}\,\angle AOB",
            font_size=44,
        ).move_to(UP * 4.05)
        theorem[0].set_color(ACCENT_CYAN)
        theorem[1].set_color(WHITE)
        theorem[2].set_color(ACCENT_PURPLE)
        theorem.set_z_index(30)
        fit_to_safe_width(theorem)

        self.play(
            FadeOut(payoff_group),
            ReplacementTransform(proof_note, theorem_title),
            ReplacementTransform(symmetry_step, theorem),
            run_time=0.9,
        )

        payoff = Tex(
            r"\textbf{Siempre la mitad, sobre el mismo arco}",
            font_size=32,
            color=WHITE,
        ).move_to(DOWN * 4.45)
        payoff.set_z_index(30)
        fit_to_safe_width(payoff)
        payoff_box = SurroundingRectangle(
            payoff,
            buff=0.2,
            corner_radius=0.12,
            stroke_width=3,
        )
        payoff_box.set_color_by_gradient(ACCENT_CYAN, ACCENT_MAGENTA)
        payoff_box.set_z_index(29)

        self.play(
            FadeIn(payoff, shift=UP * 0.1),
            Create(payoff_box),
            run_time=0.7,
        )
        self.play(
            Indicate(subtended_arc, color=ACCENT_MAGENTA, scale_factor=1.0),
            payoff_box.animate.set_stroke(width=5),
            rate_func=there_and_back,
            run_time=1.2,
        )
        self.wait(1.2)

        animate_End(scene=self)
