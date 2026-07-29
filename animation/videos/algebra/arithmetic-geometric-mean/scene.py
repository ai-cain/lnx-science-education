from manim import *
from lnx import *

# visual-derivation | algebra (inequalities) | basic
# Pappus' semicircle construction reveals the arithmetic, geometric, and
# harmonic means through two nested right triangles.
#
# The actual frame is 9 x 16 units (x in [-4.5, 4.5], y in [-8, 8]).
# Safe area: |y| <= 5.6 and |x| <= 3.8.

SAFE_WIDTH = 7.2


def fit_to_safe_width(mobject):
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


class PythagoreanMeans(MovingCameraScene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()
        self.camera.frame.save_state()

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.14
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.85)
        self.add(watermark)

        arithmetic_color = ACCENT_YELLOW
        geometric_color = ACCENT_CYAN
        harmonic_color = GREEN
        first_part_color = ACCENT_MAGENTA
        second_part_color = ORANGE
        support_color = GREY_B

        # Hook: use the formulas directly; no unexplained mean abbreviations.
        hook_title = Tex(
            r"\textbf{¿Por qué se cumple?}",
            font_size=38,
            color=WHITE,
        ).move_to(UP * 5.15)
        inequality = MathTex(
            r"\frac{a+b}{2}",
            r"\geq",
            r"\sqrt{ab}",
            r"\geq",
            r"\frac{2ab}{a+b}",
            font_size=46,
        ).move_to(UP * 4.05)
        inequality[0].set_color(arithmetic_color)
        inequality[1].set_color(WHITE)
        inequality[2].set_color(geometric_color)
        inequality[3].set_color(WHITE)
        inequality[4].set_color(harmonic_color)
        inequality.set_stroke(width=1)
        fit_to_safe_width(inequality)

        domain_condition = MathTex(
            r"a,b>0",
            font_size=29,
            color=WHITE,
        ).next_to(inequality, DOWN, buff=0.16)

        self.play(
            FadeIn(hook_title, shift=UP * 0.12),
            Write(inequality),
            FadeIn(domain_condition),
            run_time=0.8,
        )
        self.play(
            inequality[0].animate.scale(1.06),
            inequality[2].animate.scale(1.06),
            inequality[4].animate.scale(1.06),
            rate_func=there_and_back,
            run_time=0.9,
        )
        self.wait(0.5)

        # Wide construction that still respects the horizontal safe area.
        radius = 3.45
        base_y = -0.35
        center = np.array([0.0, base_y, 0.0])
        left_endpoint = center + LEFT * radius
        right_endpoint = center + RIGHT * radius
        initial_split = -1.3
        split_tracker = ValueTracker(initial_split)

        def split_point():
            return center + RIGHT * split_tracker.get_value()

        def arc_point():
            horizontal = split_tracker.get_value()
            vertical = np.sqrt(max(radius**2 - horizontal**2, 0))
            return center + RIGHT * horizontal + UP * vertical

        def projection_foot():
            radius_vector = arc_point() - center
            split_vector = split_point() - center
            scale = np.dot(split_vector, radius_vector) / radius**2
            return center + scale * radius_vector

        def projection_support():
            start = split_point()
            end = projection_foot()
            if np.linalg.norm(end - start) < 1e-4:
                end = start + RIGHT * 1e-4
            return Line(
                start,
                end,
                color=support_color,
                stroke_width=3,
            )

        def harmonic_label_position():
            start = arc_point()
            end = projection_foot()
            direction = end - start
            normal = np.array([-direction[1], direction[0], 0])
            normal /= np.linalg.norm(normal)
            return (start + end) / 2 + normal * 0.32

        diameter = Line(
            left_endpoint,
            right_endpoint,
            color=WHITE,
            stroke_width=4,
        )
        semicircle = Arc(
            radius=radius,
            start_angle=0,
            angle=PI,
            arc_center=center,
            color=WHITE,
            stroke_width=4,
        )
        endpoint_dots = VGroup(
            Dot(left_endpoint, radius=0.07, color=WHITE),
            Dot(right_endpoint, radius=0.07, color=WHITE),
        )

        left_part = always_redraw(
            lambda: Line(
                left_endpoint,
                split_point(),
                color=first_part_color,
                stroke_width=8,
            ).set_z_index(3)
        )
        right_part = always_redraw(
            lambda: Line(
                split_point(),
                right_endpoint,
                color=second_part_color,
                stroke_width=8,
            ).set_z_index(3)
        )
        split_dot = always_redraw(
            lambda: Dot(
                split_point(),
                radius=0.085,
                color=arithmetic_color,
            ).set_z_index(6)
        )
        first_part_label = always_redraw(
            lambda: MathTex(
                "a",
                font_size=34,
                color=first_part_color,
            ).move_to((left_endpoint + split_point()) / 2 + DOWN * 0.42)
        )
        second_part_label = always_redraw(
            lambda: MathTex(
                "b",
                font_size=34,
                color=second_part_color,
            ).move_to((split_point() + right_endpoint) / 2 + DOWN * 0.42)
        )

        self.play(
            FadeOut(hook_title, shift=UP * 0.1),
            inequality.animate.scale(0.72).move_to(UP * 4.9),
            domain_condition.animate.move_to(UP * 4.2),
            Create(diameter),
            FadeIn(endpoint_dots),
            run_time=0.8,
        )
        self.add(
            left_part,
            right_part,
            split_dot,
            first_part_label,
            second_part_label,
        )
        self.play(
            split_tracker.animate.set_value(0.9),
            rate_func=smooth,
            run_time=1.0,
        )
        self.play(
            split_tracker.animate.set_value(initial_split),
            rate_func=smooth,
            run_time=0.8,
        )
        self.play(Create(semicircle), run_time=0.9)

        # The altitude theorem constructs the geometric mean.
        left_chord = always_redraw(
            lambda: Line(
                arc_point(),
                left_endpoint,
                color=support_color,
                stroke_width=3,
            )
        )
        right_chord = always_redraw(
            lambda: Line(
                arc_point(),
                right_endpoint,
                color=support_color,
                stroke_width=3,
            )
        )
        altitude = always_redraw(
            lambda: Line(
                split_point(),
                arc_point(),
                color=geometric_color,
                stroke_width=7,
            ).set_z_index(5)
        )
        geometric_segment_label = always_redraw(
            lambda: MathTex(
                "G",
                font_size=30,
                color=geometric_color,
            ).move_to(
                altitude.get_center()
                + (LEFT if split_tracker.get_value() < 0 else RIGHT) * 0.28
            ).set_z_index(9)
        )
        top_dot = always_redraw(
            lambda: Dot(
                arc_point(),
                radius=0.075,
                color=geometric_color,
            ).set_z_index(7)
        )
        altitude_right_angle = always_redraw(
            lambda: RightAngle(
                Line(split_point(), split_point() + RIGHT * 0.4),
                Line(split_point(), arc_point()),
                length=0.22,
                color=WHITE,
                stroke_width=2,
            ).set_z_index(8)
        )
        apex_right_angle = always_redraw(
            lambda: RightAngle(
                Line(arc_point(), left_endpoint),
                Line(arc_point(), right_endpoint),
                length=0.2,
                color=WHITE,
                stroke_width=2,
            ).set_z_index(8)
        )
        altitude_triangle_fill = always_redraw(
            lambda: Polygon(
                left_endpoint,
                arc_point(),
                right_endpoint,
                stroke_opacity=0,
                fill_color=geometric_color,
                fill_opacity=0.12,
            ).set_z_index(1)
        )

        self.play(
            FadeIn(altitude_triangle_fill),
            FadeIn(left_chord),
            FadeIn(right_chord),
            FadeIn(altitude),
            FadeIn(geometric_segment_label),
            FadeIn(top_dot),
            FadeIn(altitude_right_angle),
            FadeIn(apex_right_angle),
            run_time=1.0,
        )

        geometric_name = Tex(
            r"\textbf{Media geométrica}",
            font_size=29,
            color=geometric_color,
        ).move_to(DOWN * 1.35)
        geometric_definition = MathTex(
            r"h^2=ab",
            r"\quad\Longrightarrow\quad",
            r"G=\sqrt{ab}",
            font_size=37,
        ).move_to(DOWN * 2.05)
        geometric_definition[0].set_color(WHITE)
        geometric_definition[1].set_color(WHITE)
        geometric_definition[2].set_color(geometric_color)
        geometric_definition.set_stroke(width=1)
        fit_to_safe_width(geometric_definition)

        self.play(
            FadeIn(geometric_name, shift=UP * 0.08),
            Write(geometric_definition),
            run_time=0.8,
        )
        self.play(
            Indicate(altitude, color=geometric_color, scale_factor=1.03),
            run_time=0.7,
        )
        self.wait(0.5)

        # A radius is the arithmetic mean.
        arithmetic_radius = always_redraw(
            lambda: Line(
                center,
                arc_point(),
                color=arithmetic_color,
                stroke_width=6,
            ).set_z_index(4)
        )
        arithmetic_segment_label = always_redraw(
            lambda: MathTex(
                "A",
                font_size=30,
                color=arithmetic_color,
            ).move_to(
                arithmetic_radius.get_center()
                + normalize(
                    np.array(
                        [
                            (arc_point() - center)[1],
                            -(arc_point() - center)[0],
                            0,
                        ]
                    )
                )
                * 0.3
            ).set_z_index(9)
        )
        center_dot = Dot(
            center,
            radius=0.075,
            color=arithmetic_color,
        ).set_z_index(7)
        arithmetic_name = Tex(
            r"\textbf{Media aritmética}",
            font_size=29,
            color=arithmetic_color,
        ).move_to(DOWN * 1.55)
        arithmetic_definition = MathTex(
            r"A=R=\frac{a+b}{2}",
            font_size=37,
            color=arithmetic_color,
        ).move_to(DOWN * 2.25)
        arithmetic_definition.set_stroke(width=1)
        fit_to_safe_width(arithmetic_definition)

        self.play(
            FadeOut(altitude_triangle_fill),
            FadeOut(geometric_name),
            FadeOut(geometric_definition),
            FadeIn(arithmetic_radius),
            FadeIn(arithmetic_segment_label),
            FadeIn(center_dot),
            FadeIn(arithmetic_name, shift=UP * 0.08),
            Write(arithmetic_definition),
            run_time=0.9,
        )
        self.play(
            Indicate(arithmetic_radius, color=arithmetic_color, scale_factor=1.03),
            run_time=0.7,
        )
        self.wait(0.5)

        # The orthogonal projection constructs the harmonic mean.
        harmonic_focus = center + LEFT * 0.55 + UP * 0.9
        self.play(
            self.camera.frame.animate.scale(0.78).move_to(harmonic_focus),
            run_time=0.8,
        )

        projection_line = always_redraw(projection_support)
        harmonic_segment = always_redraw(
            lambda: Line(
                arc_point(),
                projection_foot(),
                color=harmonic_color,
                stroke_width=8,
            ).set_z_index(6)
        )
        harmonic_segment_label = always_redraw(
            lambda: MathTex(
                "H",
                font_size=30,
                color=harmonic_color,
            ).move_to(harmonic_label_position()).set_z_index(9)
        )
        projection_dot = always_redraw(
            lambda: Dot(
                projection_foot(),
                radius=0.065,
                color=harmonic_color,
            ).set_z_index(8)
        )
        large_similarity_triangle = always_redraw(
            lambda: Polygon(
                center,
                split_point(),
                arc_point(),
                stroke_opacity=0,
                fill_color=arithmetic_color,
                fill_opacity=0.16,
            ).set_z_index(1)
        )
        small_similarity_triangle = always_redraw(
            lambda: Polygon(
                arc_point(),
                split_point(),
                projection_foot(),
                stroke_opacity=0,
                fill_color=harmonic_color,
                fill_opacity=0.24,
            ).set_z_index(2)
        )
        projection_right_angle = RightAngle(
            Line(projection_foot(), split_point()),
            Line(projection_foot(), arc_point()),
            length=0.19,
            color=WHITE,
            stroke_width=2,
        ).set_z_index(9)

        harmonic_name = Tex(
            r"\textbf{Media armónica}",
            font_size=29,
            color=harmonic_color,
        ).move_to(DOWN * 1.55)

        self.play(
            FadeOut(arithmetic_name),
            FadeOut(arithmetic_definition),
            FadeIn(projection_line),
            FadeIn(harmonic_segment),
            FadeIn(harmonic_segment_label),
            FadeIn(projection_dot),
            FadeIn(harmonic_name, shift=UP * 0.08),
            run_time=0.8,
        )
        self.play(
            FadeIn(large_similarity_triangle),
            run_time=0.5,
        )
        self.play(
            FadeIn(small_similarity_triangle),
            FadeIn(projection_right_angle),
            run_time=0.6,
        )

        similarity_title = Tex(
            r"\textbf{Triángulos semejantes}",
            font_size=30,
            color=WHITE,
        ).move_to(DOWN * 1.55)
        similarity_ratio = MathTex(
            r"\frac{H}{G}=\frac{G}{A}",
            substrings_to_isolate=["H", "G", "A"],
            font_size=40,
            color=WHITE,
        ).move_to(DOWN * 2.25)
        similarity_ratio.set_color_by_tex("H", harmonic_color)
        similarity_ratio.set_color_by_tex("G", geometric_color)
        similarity_ratio.set_color_by_tex("A", arithmetic_color)
        similarity_ratio.set_stroke(width=1)

        self.play(
            ReplacementTransform(harmonic_name, similarity_title),
            Write(similarity_ratio),
            run_time=0.8,
        )
        self.play(
            Indicate(large_similarity_triangle, color=arithmetic_color),
            Indicate(small_similarity_triangle, color=harmonic_color),
            run_time=0.9,
        )

        harmonic_relation = MathTex(
            r"H=\frac{G^2}{A}=\frac{2ab}{a+b}",
            substrings_to_isolate=["H", "G", "A"],
            font_size=35,
            color=WHITE,
        )
        harmonic_relation.set_color_by_tex("H", harmonic_color)
        harmonic_relation.set_color_by_tex("G", geometric_color)
        harmonic_relation.set_color_by_tex("A", arithmetic_color)
        harmonic_reciprocal = MathTex(
            r"H=\frac{2}{\frac1a+\frac1b}",
            substrings_to_isolate=["H"],
            font_size=34,
            color=WHITE,
        )
        harmonic_reciprocal.set_color_by_tex("H", harmonic_color)
        harmonic_derivation = VGroup(
            harmonic_relation,
            harmonic_reciprocal,
        ).arrange(DOWN, buff=0.32).move_to(DOWN * 2.05)
        harmonic_derivation.set_stroke(width=1)
        fit_to_safe_width(harmonic_derivation)

        self.play(
            FadeOut(similarity_title),
            ReplacementTransform(similarity_ratio, harmonic_derivation),
            run_time=0.9,
        )
        self.play(
            Indicate(harmonic_segment, color=harmonic_color, scale_factor=1.04),
            run_time=0.7,
        )
        self.wait(0.5)

        # Clear the explanatory fills before moving the construction.
        self.play(
            Restore(self.camera.frame),
            FadeOut(harmonic_derivation),
            FadeOut(large_similarity_triangle),
            FadeOut(small_similarity_triangle),
            FadeOut(projection_right_angle),
            run_time=0.8,
        )

        geometric_comparison = MathTex(
            r"\text{radio}",
            r"\geq",
            r"\text{altura}",
            r"\geq",
            r"\text{proyección}",
            font_size=31,
        ).move_to(DOWN * 1.75)
        geometric_comparison[0].set_color(arithmetic_color)
        geometric_comparison[1].set_color(WHITE)
        geometric_comparison[2].set_color(geometric_color)
        geometric_comparison[3].set_color(WHITE)
        geometric_comparison[4].set_color(harmonic_color)
        fit_to_safe_width(geometric_comparison)
        self.play(Write(geometric_comparison), run_time=0.8)

        self.play(
            split_tracker.animate.set_value(2.35),
            rate_func=smooth,
            run_time=1.7,
        )
        self.play(
            split_tracker.animate.set_value(-2.35),
            rate_func=smooth,
            run_time=2.4,
        )
        self.play(
            FadeOut(arithmetic_segment_label),
            FadeOut(geometric_segment_label),
            FadeOut(harmonic_segment_label),
            split_tracker.animate.set_value(0),
            rate_func=smooth,
            run_time=1.7,
        )

        equality_segment_label = MathTex(
            r"A=G=H",
            substrings_to_isolate=["A", "G", "H"],
            font_size=31,
            color=WHITE,
        ).move_to(center + UP * radius * 0.52 + RIGHT * 0.55)
        equality_segment_label.set_color_by_tex("A", arithmetic_color)
        equality_segment_label.set_color_by_tex("G", geometric_color)
        equality_segment_label.set_color_by_tex("H", harmonic_color)
        equality_segment_label.set_z_index(10)
        equality_note = Tex(
            r"Igualdad cuando $a=b$",
            font_size=30,
            color=GREEN,
        ).move_to(DOWN * 1.75)
        self.play(
            FadeIn(equality_segment_label, shift=RIGHT * 0.08),
            ReplacementTransform(geometric_comparison, equality_note),
            run_time=0.6,
        )

        final_inequality = MathTex(
            r"\frac{a+b}{2}",
            r"\geq",
            r"\sqrt{ab}",
            r"\geq",
            r"\frac{2ab}{a+b}",
            font_size=42,
        ).move_to(DOWN * 2.55)
        final_inequality[0].set_color(arithmetic_color)
        final_inequality[1].set_color(WHITE)
        final_inequality[2].set_color(geometric_color)
        final_inequality[3].set_color(WHITE)
        final_inequality[4].set_color(harmonic_color)
        final_inequality.set_stroke(width=1.1)
        fit_to_safe_width(final_inequality)
        payoff_box = SurroundingRectangle(
            final_inequality,
            color=GOLD,
            buff=0.18,
            corner_radius=0.1,
            stroke_width=3,
        )

        self.play(
            FadeOut(equality_note),
            Write(final_inequality),
            Create(payoff_box),
            run_time=0.9,
        )
        self.play(
            Circumscribe(
                final_inequality,
                color=GOLD,
                buff=0.16,
                time_width=0.7,
            ),
            run_time=1.0,
        )
        self.wait(0.6)

        # A simple three-answer prompt invites comments after the proof.
        construction = VGroup(
            inequality,
            domain_condition,
            diameter,
            semicircle,
            endpoint_dots,
            left_chord,
            right_chord,
            altitude,
            geometric_segment_label,
            top_dot,
            altitude_right_angle,
            apex_right_angle,
            arithmetic_radius,
            arithmetic_segment_label,
            center_dot,
            projection_line,
            harmonic_segment,
            harmonic_segment_label,
            projection_dot,
            equality_segment_label,
            final_inequality,
            payoff_box,
        )
        self.play(
            FadeOut(construction),
            FadeOut(left_part),
            FadeOut(right_part),
            FadeOut(split_dot),
            FadeOut(first_part_label),
            FadeOut(second_part_label),
            run_time=0.7,
        )

        challenge_title = Tex(
            r"\textbf{Ahora tú}",
            font_size=42,
            color=arithmetic_color,
        ).move_to(UP * 3.75)
        challenge_values = MathTex(
            r"a=2,\qquad b=8",
            font_size=50,
            color=WHITE,
        ).move_to(UP * 2.45)
        arithmetic_challenge = MathTex(
            r"\frac{a+b}{2}=\ ?",
            font_size=38,
            color=arithmetic_color,
        )
        geometric_challenge = MathTex(
            r"\sqrt{ab}=\ ?",
            font_size=38,
            color=geometric_color,
        )
        harmonic_challenge = MathTex(
            r"\frac{2}{\frac1a+\frac1b}=\ ?",
            font_size=38,
            color=harmonic_color,
        )
        challenge = VGroup(
            arithmetic_challenge,
            geometric_challenge,
            harmonic_challenge,
        ).arrange(DOWN, buff=0.48).move_to(DOWN * 0.05)
        challenge.set_stroke(width=1)
        fit_to_safe_width(challenge)

        comment_prompt = Tex(
            r"\textbf{Comenta los tres resultados}",
            font_size=32,
            color=WHITE,
        ).move_to(DOWN * 2.75)
        prompt_box = SurroundingRectangle(
            comment_prompt,
            color=GOLD,
            buff=0.22,
            corner_radius=0.12,
            stroke_width=3,
        )
        prompt_box.set_color_by_gradient(YELLOW, ORANGE)

        self.play(
            FadeIn(challenge_title, shift=UP * 0.12),
            Write(challenge_values),
            run_time=0.6,
        )
        self.play(
            LaggedStart(
                Write(arithmetic_challenge),
                Write(geometric_challenge),
                Write(harmonic_challenge),
                lag_ratio=0.28,
            ),
            run_time=1.0,
        )
        self.play(
            FadeIn(comment_prompt, shift=UP * 0.1),
            Create(prompt_box),
            run_time=0.6,
        )
        self.wait(1.6)

        animate_End(scene=self)
