from manim import *
from lnx import *

# visual-hook | geometry | basic
# Mathematical reference:
# https://mathworld.wolfram.com/ThalesTheorem.html
#
# Every angle inscribed in a semicircumference is a right angle.
# Proof: the radius to the vertex splits the triangle into two isosceles
# triangles whose base angles satisfy 2*alpha + 2*beta = 180, so alpha + beta = 90.

CENTER = np.array([0.0, -0.9, 0.0])
RADIUS = 2.5
PROOF_ANGLE = 1.15


def arc_point(angle):
    """Return the point of the semicircumference at the given polar angle."""
    return CENTER + RADIUS * np.array([np.cos(angle), np.sin(angle), 0.0])


class ThalesTheorem(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        point_a = arc_point(PI)
        point_b = arc_point(0.0)

        # ---------------------------------------------------------------
        # Beat 1 (0.0-2.0 s) - hook: a right angle already locked in place.
        # ---------------------------------------------------------------
        semicircumference = Arc(
            radius=RADIUS,
            start_angle=0.0,
            angle=PI,
            arc_center=CENTER,
            color=ACCENT_CYAN,
            stroke_width=6,
        )
        diameter = Line(point_a, point_b, color=ACCENT_PURPLE, stroke_width=6)
        dot_a = Dot(point_a, radius=0.07, color=WHITE)
        dot_b = Dot(point_b, radius=0.07, color=WHITE)
        dot_o = Dot(CENTER, radius=0.07, color=ACCENT_YELLOW)

        label_a = MathTex("A", font_size=32, color=WHITE)
        label_a.next_to(point_a, DL, buff=0.18)
        label_b = MathTex("B", font_size=32, color=WHITE)
        label_b.next_to(point_b, DR, buff=0.18)
        label_o = MathTex("O", font_size=32, color=ACCENT_YELLOW)
        label_o.next_to(CENTER, DOWN, buff=0.22)
        for label in (label_a, label_b, label_o):
            label.set_z_index(30)

        tracker = ValueTracker(0.72)

        def moving_point():
            return arc_point(tracker.get_value())

        chord_pa = always_redraw(
            lambda: Line(
                moving_point(),
                point_a,
                color=ACCENT_MAGENTA,
                stroke_width=5,
            )
        )
        chord_pb = always_redraw(
            lambda: Line(
                moving_point(),
                point_b,
                color=ACCENT_YELLOW,
                stroke_width=5,
            )
        )
        dot_p = always_redraw(
            lambda: Dot(moving_point(), radius=0.09, color=WHITE)
        )
        right_angle = always_redraw(
            lambda: RightAngle(
                Line(moving_point(), point_a),
                Line(moving_point(), point_b),
                length=0.34,
                color=WHITE,
                stroke_width=4,
            )
        )
        label_p = always_redraw(
            lambda: MathTex("P", font_size=32, color=WHITE)
            .next_to(moving_point(), UP, buff=0.2)
            .set_z_index(30)
        )
        angle_readout = MathTex(r"90^{\circ}", font_size=36, color=WHITE)
        angle_readout.set_z_index(30)
        angle_readout.add_updater(
            lambda mobject: mobject.move_to(
                moving_point()
                + 0.95 * normalize(CENTER - moving_point())
            )
        )

        hook = Tex(
            r"\textbf{Muevo $P$ y el ángulo no cambia}",
            font_size=38,
            color=WHITE,
        )
        hook.move_to(UP * 5.05)
        hook.set_z_index(30)

        self.play(
            Create(semicircumference),
            Create(diameter),
            FadeIn(hook, shift=DOWN * 0.12),
            run_time=0.8,
        )
        self.play(
            FadeIn(dot_a),
            FadeIn(dot_b),
            FadeIn(label_a),
            FadeIn(label_b),
            Create(chord_pa),
            Create(chord_pb),
            FadeIn(dot_p),
            FadeIn(label_p),
            run_time=0.7,
        )
        self.add(right_angle, angle_readout)
        self.play(
            FadeIn(right_angle),
            FadeIn(angle_readout),
            run_time=0.4,
        )

        # ---------------------------------------------------------------
        # Beat 2 (2.0-9.5 s) - sweep P along the arc, the marker stays square.
        # ---------------------------------------------------------------
        self.play(tracker.animate.set_value(2.75), run_time=2.2)
        self.play(tracker.animate.set_value(0.35), run_time=2.6)
        self.play(tracker.animate.set_value(PROOF_ANGLE), run_time=1.6)
        self.wait(0.5)

        # ---------------------------------------------------------------
        # Beat 3 (9.5-14.0 s) - freeze the configuration and name it.
        # ---------------------------------------------------------------
        point_p = arc_point(PROOF_ANGLE)
        static_pa = Line(point_p, point_a, color=ACCENT_MAGENTA, stroke_width=5)
        static_pb = Line(point_p, point_b, color=ACCENT_YELLOW, stroke_width=5)
        static_p = Dot(point_p, radius=0.09, color=WHITE)
        static_label_p = MathTex("P", font_size=32, color=WHITE)
        static_label_p.next_to(point_p, UP, buff=0.2)
        static_label_p.set_z_index(30)
        static_right_angle = RightAngle(
            Line(point_p, point_a),
            Line(point_p, point_b),
            length=0.34,
            color=WHITE,
            stroke_width=4,
        )

        angle_readout.clear_updaters()
        self.remove(chord_pa, chord_pb, dot_p, label_p, right_angle)
        self.add(static_pa, static_pb, static_p, static_label_p, static_right_angle)

        title = Tex(
            r"\textbf{Teorema de Tales}",
            font_size=42,
            color=ACCENT_CYAN,
        )
        title.move_to(UP * 5.15)
        title.set_z_index(30)
        statement = Tex(
            r"Si $AB$ es un diámetro, el ángulo en $P$ mide $90^{\circ}$.",
            font_size=29,
            color=WHITE,
        )
        statement.move_to(UP * 4.35)
        statement.set_z_index(30)

        self.play(
            ReplacementTransform(hook, title),
            FadeOut(angle_readout),
            run_time=0.7,
        )
        self.play(FadeIn(statement, shift=DOWN * 0.1), run_time=0.7)
        self.wait(1.0)

        # ---------------------------------------------------------------
        # Beat 4 (14.0-21.0 s) - the radius OP creates two isosceles triangles.
        # ---------------------------------------------------------------
        radius_op = Line(CENTER, point_p, color=ACCENT_YELLOW, stroke_width=5)
        radius_note = Tex(
            r"Trazamos el radio $OP$: $\;OA=OP=OB$",
            font_size=29,
            color=ACCENT_YELLOW,
        )
        radius_note.move_to(UP * 4.35)
        radius_note.set_z_index(30)

        self.play(
            FadeIn(dot_o),
            FadeIn(label_o),
            run_time=0.4,
        )
        self.play(
            Create(radius_op),
            ReplacementTransform(statement, radius_note),
            run_time=0.9,
        )

        triangle_left = Polygon(
            point_a,
            point_p,
            CENTER,
            stroke_width=0,
            fill_color=ACCENT_MAGENTA,
            fill_opacity=0.28,
        )
        triangle_left.set_z_index(-1)
        triangle_right = Polygon(
            CENTER,
            point_p,
            point_b,
            stroke_width=0,
            fill_color=ACCENT_CYAN,
            fill_opacity=0.28,
        )
        triangle_right.set_z_index(-1)

        self.play(FadeIn(triangle_left), run_time=0.6)
        self.play(FadeIn(triangle_right), run_time=0.6)
        self.wait(0.6)

        # Base angles of each isosceles triangle, labelled outside the fills.
        alpha_at_a = MathTex(r"\alpha", font_size=34, color=ACCENT_MAGENTA)
        alpha_at_a.move_to(point_a + np.array([0.62, 0.24, 0.0]))
        alpha_at_p = MathTex(r"\alpha", font_size=34, color=ACCENT_MAGENTA)
        alpha_at_p.move_to(point_p + np.array([-0.52, -0.42, 0.0]))
        beta_at_b = MathTex(r"\beta", font_size=34, color=ACCENT_CYAN)
        beta_at_b.move_to(point_b + np.array([-0.66, 0.24, 0.0]))
        beta_at_p = MathTex(r"\beta", font_size=34, color=ACCENT_CYAN)
        beta_at_p.move_to(point_p + np.array([0.34, -0.52, 0.0]))
        for label in (alpha_at_a, alpha_at_p, beta_at_b, beta_at_p):
            label.set_z_index(30)

        self.play(
            FadeIn(alpha_at_a, scale=1.2),
            FadeIn(alpha_at_p, scale=1.2),
            run_time=0.7,
        )
        self.play(
            FadeIn(beta_at_b, scale=1.2),
            FadeIn(beta_at_p, scale=1.2),
            run_time=0.7,
        )
        self.wait(0.8)

        # ---------------------------------------------------------------
        # Beat 5 (21.0-32.0 s) - the angle sum collapses to 90 degrees.
        # ---------------------------------------------------------------
        sum_equation = MathTex(
            r"2\alpha + 2\beta = 180^{\circ}",
            font_size=42,
            color=WHITE,
        )
        sum_equation.move_to(UP * 4.30)
        sum_equation.set_z_index(30)
        sum_note = Tex(
            r"Los tres ángulos de $\triangle APB$ suman $180^{\circ}$.",
            font_size=28,
            color=GREY_B,
        )
        sum_note.move_to(UP * 3.55)
        sum_note.set_z_index(30)

        self.play(
            ReplacementTransform(radius_note, sum_equation),
            run_time=0.9,
        )
        self.play(FadeIn(sum_note, shift=DOWN * 0.08), run_time=0.6)
        self.wait(1.2)

        half_equation = MathTex(
            r"\alpha + \beta = 90^{\circ}",
            font_size=48,
            color=ACCENT_YELLOW,
        )
        half_equation.move_to(UP * 4.30)
        half_equation.set_z_index(30)
        divide_note = Tex(
            r"Dividimos entre $2$.",
            font_size=28,
            color=GREY_B,
        )
        divide_note.move_to(UP * 3.55)
        divide_note.set_z_index(30)

        self.play(
            TransformMatchingTex(sum_equation, half_equation),
            ReplacementTransform(sum_note, divide_note),
            run_time=1.2,
        )
        self.play(
            Indicate(half_equation, color=ACCENT_YELLOW, scale_factor=1.08),
            run_time=1.1,
        )
        self.wait(0.8)

        angle_p_equation = MathTex(
            r"\angle APB = \alpha + \beta = 90^{\circ}",
            font_size=38,
            color=WHITE,
        )
        angle_p_equation.move_to(UP * 4.30)
        angle_p_equation.set_z_index(30)
        self.play(
            TransformMatchingTex(half_equation, angle_p_equation),
            FadeOut(divide_note),
            run_time=1.0,
        )
        self.play(
            static_right_angle.animate.set_stroke(width=7),
            rate_func=there_and_back,
            run_time=1.1,
        )
        self.wait(0.7)

        # ---------------------------------------------------------------
        # Beat 6 (32.0-40.0 s) - payoff: the result holds for every P.
        # ---------------------------------------------------------------
        payoff = Tex(
            r"\textbf{Siempre recto, para todo $P$}",
            font_size=36,
            color=WHITE,
        )
        payoff.move_to(DOWN * 4.85)
        payoff.set_z_index(30)
        payoff_box = SurroundingRectangle(
            payoff,
            buff=0.22,
            corner_radius=0.14,
            stroke_width=3,
        )
        payoff_box.set_color_by_gradient(ACCENT_YELLOW, ACCENT_MAGENTA)
        payoff_box.set_z_index(29)

        self.play(
            FadeIn(payoff, shift=UP * 0.1),
            Create(payoff_box),
            run_time=0.8,
        )

        # Restore the live construction and sweep once more as proof of the claim.
        self.remove(
            static_pa,
            static_pb,
            static_p,
            static_label_p,
            static_right_angle,
        )
        moving_radius = always_redraw(
            lambda: Line(
                CENTER,
                moving_point(),
                color=ACCENT_YELLOW,
                stroke_width=5,
            )
        )
        moving_left = always_redraw(
            lambda: Polygon(
                point_a,
                moving_point(),
                CENTER,
                stroke_width=0,
                fill_color=ACCENT_MAGENTA,
                fill_opacity=0.28,
            ).set_z_index(-1)
        )
        moving_right = always_redraw(
            lambda: Polygon(
                CENTER,
                moving_point(),
                point_b,
                stroke_width=0,
                fill_color=ACCENT_CYAN,
                fill_opacity=0.28,
            ).set_z_index(-1)
        )
        self.remove(radius_op, triangle_left, triangle_right)
        self.remove(alpha_at_a, alpha_at_p, beta_at_b, beta_at_p)
        self.add(
            moving_left,
            moving_right,
            moving_radius,
            chord_pa,
            chord_pb,
            dot_p,
            label_p,
            right_angle,
        )
        self.play(tracker.animate.set_value(2.55), run_time=2.0)
        self.play(tracker.animate.set_value(0.6), run_time=2.0)
        self.wait(0.6)

        animate_End(scene=self)
