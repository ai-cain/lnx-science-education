from manim import *
from lnx import *

# hidden-invariant | geometry (circle packing) | intermediate
# Mathematical reference:
# https://mathworld.wolfram.com/DescartesCircleTheorem.html
#
# The construction uses the integral Descartes quadruple (-1, 2, 3, 6).
# Replacing the enclosing circle of curvature -1 gives the second solution 23.

SAFE_WIDTH = 7.2
GEOMETRY_SCALE = 2.8
GEOMETRY_ORIGIN = np.array([-0.9, -0.25, 0.0])


def fit_to_safe_width(mobject):
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def scaled_point(x, y):
    return GEOMETRY_ORIGIN + GEOMETRY_SCALE * np.array([x, y, 0.0])


def tangency_point(first_circle, second_circle):
    """Return the exact external tangency point of two tangent circles."""
    first_center, first_radius = first_circle
    second_center, second_radius = second_circle
    return first_center + (
        first_radius
        / (first_radius + second_radius)
        * (second_center - first_center)
    )


def validate_marker(
    marker_point,
    first_circle,
    second_circle,
    tolerance=1e-9,
):
    """Ensure a marker lies on both corresponding circumferences."""
    for center, radius in (first_circle, second_circle):
        assert abs(np.linalg.norm(marker_point - center) - radius) < tolerance


def validate_tangencies(circles, marker_points, tolerance=1e-9):
    """Validate the exact Descartes configuration before it is displayed."""
    inner_keys = ("k2", "k3", "k6")
    for index, first_key in enumerate(inner_keys):
        first_center, first_radius = circles[first_key]
        for second_key in inner_keys[index + 1 :]:
            second_center, second_radius = circles[second_key]
            actual = np.linalg.norm(first_center - second_center)
            expected = first_radius + second_radius
            assert abs(actual - expected) < tolerance

    outer_center, outer_radius = circles["outer"]
    for inner_key in inner_keys:
        inner_center, inner_radius = circles[inner_key]
        actual = np.linalg.norm(inner_center - outer_center)
        expected = outer_radius - inner_radius
        assert abs(actual - expected) < tolerance

    gap_center, gap_radius = circles["gap"]
    for inner_key in inner_keys:
        inner_center, inner_radius = circles[inner_key]
        actual = np.linalg.norm(gap_center - inner_center)
        expected = gap_radius + inner_radius
        assert abs(actual - expected) < tolerance

    for pair, marker_point in marker_points.items():
        validate_marker(
            marker_point,
            circles[pair[0]],
            circles[pair[1]],
            tolerance,
        )


def make_tangency_marker(point, color):
    """Create one solid point at an exact tangency."""
    marker = Dot(point=point, radius=0.035, color=color)
    marker.set_opacity(0.8)
    marker.set_z_index(20)
    return marker


def reflect_descartes_circle(bends, centers, replaced_index):
    """Return the other circle tangent to the unchanged Descartes triple."""
    other_indices = [
        index for index in range(len(bends)) if index != replaced_index
    ]
    reflected_bend = (
        2 * sum(bends[index] for index in other_indices)
        - bends[replaced_index]
    )
    reflected_bend_center = (
        2
        * sum(
            bends[index] * centers[index]
            for index in other_indices
        )
        - bends[replaced_index] * centers[replaced_index]
    )
    return reflected_bend, reflected_bend_center / reflected_bend


def validate_challenge_packing(circles, tolerance=1e-9):
    """Validate every local Descartes tangency used by the 8-circle challenge."""
    external_pairs = (
        ("k2", "k3"),
        ("k2", "k6"),
        ("k3", "k6"),
        ("gap", "k2"),
        ("gap", "k3"),
        ("gap", "k6"),
        ("k50", "k2"),
        ("k50", "k3"),
        ("k50", "gap"),
        ("k59", "k2"),
        ("k59", "k6"),
        ("k59", "gap"),
        ("k62", "k3"),
        ("k62", "k6"),
        ("k62", "gap"),
    )
    for first_key, second_key in external_pairs:
        first_center, first_radius = circles[first_key]
        second_center, second_radius = circles[second_key]
        actual = np.linalg.norm(first_center - second_center)
        expected = first_radius + second_radius
        assert abs(actual - expected) < tolerance

    outer_center, outer_radius = circles["outer"]
    for inner_key in ("k2", "k3", "k6"):
        inner_center, inner_radius = circles[inner_key]
        actual = np.linalg.norm(inner_center - outer_center)
        expected = outer_radius - inner_radius
        assert abs(actual - expected) < tolerance


class DescartesCircleTheorem(MovingCameraScene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()
        self.camera.frame.save_state()

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.14
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.85)
        self.add(watermark)

        circle_data = {
            "outer": (scaled_point(0, 0), GEOMETRY_SCALE),
            "k2": (scaled_point(1 / 2, 0), GEOMETRY_SCALE / 2),
            "k3": (scaled_point(0, 2 / 3), GEOMETRY_SCALE / 3),
            "k6": (scaled_point(1 / 2, 2 / 3), GEOMETRY_SCALE / 6),
            "gap": (
                scaled_point(8 / 23, 12 / 23),
                GEOMETRY_SCALE / 23,
            ),
        }
        marker_pairs = (
            ("k2", "k3"),
            ("k2", "k6"),
            ("k3", "k6"),
            ("gap", "k2"),
            ("gap", "k3"),
            ("gap", "k6"),
        )
        marker_points = {
            pair: tangency_point(circle_data[pair[0]], circle_data[pair[1]])
            for pair in marker_pairs
        }
        validate_tangencies(circle_data, marker_points)

        circle_specs = (
            ("k2", ACCENT_CYAN, 2),
            ("k3", ACCENT_YELLOW, 3),
            ("k6", ACCENT_MAGENTA, 6),
        )
        inner_circles = VGroup()
        curvature_labels = VGroup()
        for key, color, curvature in circle_specs:
            center, radius = circle_data[key]
            circle = Circle(
                radius=radius,
                color=color,
                stroke_width=6,
            ).move_to(center)
            label = MathTex(
                rf"\kappa={curvature}",
                font_size=29 if curvature != 6 else 25,
                color=color,
            ).move_to(center)
            label.set_stroke(width=1)
            inner_circles.add(circle)
            curvature_labels.add(label)

        gap_center, gap_radius = circle_data["gap"]
        unknown_circle = Circle(
            radius=gap_radius,
            color=WHITE,
            stroke_width=8,
        ).move_to(gap_center)
        unknown_circle.set_z_index(18)
        unknown_label = MathTex(
            r"r=?",
            font_size=32,
            color=WHITE,
        ).move_to(gap_center + LEFT * 0.12 + DOWN * 0.52)
        unknown_label.set_stroke(width=1)
        unknown_label.set_z_index(22)
        unknown_leader = Arrow(
            start=unknown_label.get_top() + UP * 0.02,
            end=gap_center + DOWN * (gap_radius + 0.015),
            buff=0.02,
            color=WHITE,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.28,
        )
        unknown_leader.set_z_index(21)
        unknown_target = VGroup(
            unknown_circle,
            unknown_label,
            unknown_leader,
        )

        initial_tangency_markers = VGroup(
            make_tangency_marker(marker_points[("k2", "k3")], GREEN),
            make_tangency_marker(marker_points[("k2", "k6")], ORANGE),
            make_tangency_marker(marker_points[("k3", "k6")], "#ff1744"),
        )

        # Hook: the exact curvilinear gap pulses before any formula appears.
        hook = Tex(
            r"\textbf{¿Qué circunferencia cabe aquí?}",
            font_size=42,
            color=WHITE,
        ).move_to(UP * 4.95)
        hook.set_stroke(width=1)
        task_prompt = Tex(
            r"\textbf{Calcula el radio de la circunferencia blanca}",
            font_size=36,
            color=WHITE,
        ).move_to(UP * 4.95)
        task_prompt.set_stroke(width=1)
        fit_to_safe_width(task_prompt)
        self.play(
            LaggedStart(
                *[Create(circle) for circle in inner_circles],
                lag_ratio=0.18,
            ),
            FadeIn(hook, shift=UP * 0.12),
            run_time=0.9,
        )
        self.play(
            LaggedStart(
                *[
                    FadeIn(marker)
                    for marker in initial_tangency_markers
                ],
                lag_ratio=0.2,
            ),
            run_time=0.75,
        )
        self.play(
            Create(unknown_circle),
            FadeIn(unknown_label, shift=UP * 0.06),
            GrowArrow(unknown_leader),
            run_time=0.9,
        )
        self.play(
            ReplacementTransform(hook, task_prompt),
            run_time=0.6,
        )
        self.wait(1.0)
        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.scale(0.72).move_to(unknown_circle),
            run_time=1.7,
        )
        self.wait(1.5)
        self.play(
            Restore(self.camera.frame),
            run_time=1.7,
        )
        self.wait(0.3)

        # Setup: curvature turns the three radii into the integers 2, 3, and 6.
        curvature_definition = MathTex(
            r"\kappa=\frac{1}{r}",
            font_size=42,
            color=WHITE,
        ).move_to(UP * 4.05)
        curvature_definition.set_stroke(width=1)
        self.play(
            Write(curvature_definition),
            FadeIn(curvature_labels),
            run_time=0.8,
        )
        self.play(
            LaggedStart(
                *[
                    Indicate(label, color=label.get_color(), scale_factor=1.08)
                    for label in curvature_labels
                ],
                lag_ratio=0.22,
            ),
            run_time=2.0,
        )
        self.wait(0.8)

        # The theorem is the single invariant driving both geometric solutions.
        theorem_title = Tex(
            r"\textbf{Teorema de las circunferencias de Descartes}",
            font_size=32,
            color=ACCENT_CYAN,
        ).move_to(UP * 5.0)
        theorem = MathTex(
            r"2\left(\kappa_1^2+\kappa_2^2+\kappa_3^2+\kappa_4^2\right)",
            r"=",
            r"\left(\kappa_1+\kappa_2+\kappa_3+\kappa_4\right)^2",
            font_size=33,
            color=WHITE,
        ).move_to(UP * 4.15)
        theorem[1].set_color(ACCENT_YELLOW)
        theorem.set_stroke(width=1)
        fit_to_safe_width(theorem)

        geometry_group = VGroup(
            inner_circles,
            curvature_labels,
            unknown_target,
        )
        self.play(FadeOut(initial_tangency_markers), run_time=0.35)
        self.play(
            ReplacementTransform(task_prompt, theorem_title),
            FadeOut(curvature_definition),
            Write(theorem),
            geometry_group.animate.shift(DOWN * 1.05),
            run_time=1.0,
        )
        self.play(
            Circumscribe(theorem, color=ACCENT_YELLOW, buff=0.12),
            run_time=1.4,
        )
        self.wait(0.9)

        # Substitute 2, 3, and 6, then expose the factorization.
        substitution = MathTex(
            r"2\left(2^2+3^2+6^2+\kappa^2\right)",
            r"=",
            r"\left(2+3+6+\kappa\right)^2",
            font_size=34,
            color=WHITE,
        ).move_to(UP * 4.15)
        substitution[1].set_color(ACCENT_YELLOW)
        substitution.set_stroke(width=1)
        fit_to_safe_width(substitution)

        quadratic = MathTex(
            r"\kappa^2-22\kappa-23=0",
            font_size=39,
            color=WHITE,
        ).move_to(UP * 3.25)
        quadratic.set_stroke(width=1)
        factorization = MathTex(
            r"(\kappa+1)(\kappa-23)=0",
            font_size=39,
            color=ACCENT_YELLOW,
        ).move_to(UP * 2.55)
        factorization.set_stroke(width=1)

        self.play(
            TransformMatchingTex(theorem, substitution),
            run_time=1.4,
        )
        self.play(Write(quadratic), run_time=1.1)
        self.play(
            TransformMatchingTex(quadratic.copy(), factorization),
            run_time=1.3,
        )
        self.play(
            Indicate(factorization, color=ACCENT_YELLOW, scale_factor=1.04),
            run_time=1.1,
        )
        self.wait(0.8)

        roots = MathTex(
            r"\kappa=-1",
            r"\qquad\text{o}\qquad",
            r"\kappa=23",
            font_size=45,
        ).move_to(UP * 3.35)
        roots[0].set_color(ORANGE)
        roots[1].set_color(WHITE)
        roots[2].set_color(GREEN)
        roots.set_stroke(width=1)
        self.play(
            FadeOut(substitution),
            FadeOut(factorization),
            ReplacementTransform(quadratic, roots),
            run_time=0.9,
        )
        self.play(
            roots[0].animate.scale(1.12),
            roots[2].animate.scale(1.12),
            rate_func=there_and_back,
            run_time=1.7,
        )

        # Negative curvature is the oriented enclosing circle.
        outer_center, outer_radius = circle_data["outer"]
        outer_circle = Circle(
            radius=outer_radius,
            color=ORANGE,
            stroke_width=6,
        ).move_to(outer_center + DOWN * 1.05)
        outer_note = Tex(
            r"$\kappa=-1$: circunferencia exterior",
            font_size=34,
            color=ORANGE,
        ).move_to(UP * 4.45)
        sign_note = Tex(
            r"\textit{El signo negativo identifica la circunferencia envolvente.}",
            font_size=28,
            color=GREY_B,
        ).move_to(UP * 3.75)
        self.play(
            FadeOut(theorem_title),
            roots.animate.scale(0.72).move_to(UP * 5.15),
            FadeIn(outer_note, shift=UP * 0.1),
            Create(outer_circle),
            run_time=1.4,
        )
        self.play(FadeIn(sign_note), run_time=0.6)
        self.play(
            Indicate(outer_circle, color=ORANGE, scale_factor=1.02),
            run_time=1.3,
        )
        self.wait(0.8)

        # The positive solution is the other circle tangent to the same triple.
        gap_circle = unknown_circle
        gap_tangency_markers = VGroup(
            make_tangency_marker(
                marker_points[("gap", "k2")] + DOWN * 1.05,
                ACCENT_CYAN,
            ),
            make_tangency_marker(
                marker_points[("gap", "k3")] + DOWN * 1.05,
                ACCENT_YELLOW,
            ),
            make_tangency_marker(
                marker_points[("gap", "k6")] + DOWN * 1.05,
                ACCENT_MAGENTA,
            ),
        )
        positive_note = MathTex(
            r"\kappa=23",
            r"\quad\Longrightarrow\quad",
            r"r=\frac{1}{23}",
            font_size=40,
        ).move_to(UP * 4.15)
        positive_note[0].set_color(GREEN)
        positive_note[1].set_color(WHITE)
        positive_note[2].set_color(ACCENT_YELLOW)
        positive_note.set_stroke(width=1)

        self.play(
            FadeOut(outer_note),
            FadeOut(sign_note),
            outer_circle.animate.set_stroke(opacity=0.18),
            FadeIn(positive_note, shift=UP * 0.1),
            FadeOut(unknown_label),
            FadeOut(unknown_leader),
            run_time=1.0,
        )
        self.wait(1.0)
        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.scale(0.62).move_to(gap_circle),
            run_time=1.7,
        )
        self.play(
            LaggedStart(
                *[
                    FadeIn(marker)
                    for marker in gap_tangency_markers
                ],
                lag_ratio=0.18,
            ),
            Flash(
                gap_circle.get_center(),
                color=ACCENT_YELLOW,
                flash_radius=0.45,
                line_length=0.12,
            ),
            run_time=1.0,
        )
        self.wait(1.5)
        self.play(
            Restore(self.camera.frame),
            FadeOut(gap_tangency_markers),
            run_time=0.7,
        )
        self.wait(1.0)
        self.play(
            gap_circle.animate.set_stroke(
                color=GREEN,
                width=7,
                opacity=1.0,
            ).set_fill(GREEN, opacity=0.22),
            run_time=0.7,
        )

        payoff = Tex(
            r"\textbf{¡Es tangente a las tres!}",
            font_size=36,
            color=WHITE,
        ).move_to(DOWN * 4.75)
        payoff_box = SurroundingRectangle(
            payoff,
            color=GOLD,
            buff=0.2,
            corner_radius=0.12,
            stroke_width=3,
        )
        payoff_box.set_color_by_gradient(ACCENT_YELLOW, ORANGE)
        self.play(
            FadeIn(payoff, shift=UP * 0.1),
            Create(payoff_box),
            run_time=0.7,
        )
        self.play(
            payoff_box.animate.set_stroke(width=5),
            rate_func=there_and_back,
            run_time=1.0,
        )
        self.wait(1.0)

        # Final challenge: eight circles come from repeated local 2D reflections.
        base_bends = (2, 3, 6, 23)
        base_centers = (
            complex(1 / 2, 0),
            complex(0, 2 / 3),
            complex(1 / 2, 2 / 3),
            complex(8 / 23, 12 / 23),
        )
        reflected_data = {
            "k50": reflect_descartes_circle(base_bends, base_centers, 2),
            "k59": reflect_descartes_circle(base_bends, base_centers, 1),
            "k62": reflect_descartes_circle(base_bends, base_centers, 0),
        }
        expected_reflections = {
            "k50": (50, complex(15 / 50, 24 / 50)),
            "k59": (59, complex(24 / 59, 30 / 59)),
            "k62": (62, complex(21 / 62, 36 / 62)),
        }
        for key, (expected_bend, expected_center) in expected_reflections.items():
            bend, center = reflected_data[key]
            assert bend == expected_bend
            assert abs(center - expected_center) < 1e-12

        challenge_scale = 3.0
        challenge_origin = np.array([-0.65, -1.95, 0.0])

        def challenge_point(center):
            return challenge_origin + challenge_scale * np.array(
                [center.real, center.imag, 0.0]
            )

        normalized_centers = {
            "outer": complex(0, 0),
            "k2": base_centers[0],
            "k3": base_centers[1],
            "k6": base_centers[2],
            "gap": base_centers[3],
            **{
                key: center
                for key, (_, center) in reflected_data.items()
            },
        }
        challenge_bends = {
            "outer": -1,
            "k2": 2,
            "k3": 3,
            "k6": 6,
            "gap": 23,
            **{
                key: bend
                for key, (bend, _) in reflected_data.items()
            },
        }
        challenge_circle_data = {
            key: (
                challenge_point(center),
                challenge_scale / abs(challenge_bends[key]),
            )
            for key, center in normalized_centers.items()
        }
        validate_challenge_packing(challenge_circle_data)

        challenge_styles = {
            "outer": (GREY_B, 3, 0.38, 0.0),
            "k2": (ACCENT_CYAN, 5, 1.0, 0.04),
            "k3": (ACCENT_YELLOW, 5, 1.0, 0.04),
            "k6": (ACCENT_MAGENTA, 3, 0.52, 0.02),
            "gap": (GREEN, 4, 0.9, 0.10),
            "k50": ("#ff1744", 7, 1.0, 0.22),
            "k59": (GREY_B, 2, 0.55, 0.04),
            "k62": (GREY_B, 2, 0.55, 0.04),
        }
        challenge_circles_by_key = {}
        for key in (
            "outer",
            "k2",
            "k3",
            "k6",
            "gap",
            "k50",
            "k59",
            "k62",
        ):
            center, radius = challenge_circle_data[key]
            color, stroke_width, opacity, fill_opacity = challenge_styles[key]
            challenge_circles_by_key[key] = Circle(
                radius=radius,
                color=color,
                stroke_width=stroke_width,
                stroke_opacity=opacity,
                fill_color=color,
                fill_opacity=fill_opacity,
            ).move_to(center)
        challenge_circles = VGroup(*challenge_circles_by_key.values())
        assert len(challenge_circles) == 8
        assert all(type(circle) is Circle for circle in challenge_circles)

        generalization_title = Tex(
            r"\textbf{La fórmula general}",
            font_size=36,
            color=ACCENT_CYAN,
        ).move_to(UP * 5.35)
        generalization = MathTex(
            r"n\sum_{i=1}^{n+2}\kappa_i^2",
            r"=",
            r"\left(\sum_{i=1}^{n+2}\kappa_i\right)^2",
            font_size=34,
            color=WHITE,
        ).move_to(UP * 4.35)
        generalization.set_stroke(width=1)
        generalization[0].set_color(ACCENT_CYAN)
        generalization[1].set_color(ACCENT_YELLOW)
        fit_to_safe_width(generalization)
        parameter_note = Tex(
            r"$n=\text{dimensión}:\quad n=2$ plano,\quad $n=3$ esferas",
            font_size=28,
            color=WHITE,
        ).move_to(UP * 3.42)
        local_rule_note = Tex(
            r"\textbf{8 circunferencias = repetir el caso $n=2$}",
            font_size=28,
            color=ACCENT_YELLOW,
        ).move_to(UP * 2.78)
        challenge_prompt = Tex(
            r"\textbf{Encuentra el radio de la mayor de las tres nuevas.}",
            font_size=30,
            color=WHITE,
        ).move_to(UP * 2.08)
        fit_to_safe_width(challenge_prompt)

        label_k2 = MathTex(
            r"\kappa=2", font_size=28, color=ACCENT_CYAN
        ).move_to(challenge_circle_data["k2"][0] + DOWN * 0.42)
        label_k3 = MathTex(
            r"\kappa=3", font_size=28, color=ACCENT_YELLOW
        ).move_to(challenge_circle_data["k3"][0] + LEFT * 0.18)
        label_k6 = MathTex(
            r"\kappa=6", font_size=20, color=ACCENT_MAGENTA
        ).move_to(np.array([1.58, -0.14, 0.0]))
        label_k6.set_opacity(0.68)
        leader_k6 = Line(
            label_k6.get_left() + LEFT * 0.03,
            challenge_circle_data["k6"][0] + RIGHT * challenge_circle_data["k6"][1],
            color=ACCENT_MAGENTA,
            stroke_width=1.6,
            stroke_opacity=0.55,
        )
        gap_center_challenge, gap_radius_challenge = (
            challenge_circle_data["gap"]
        )
        label_k23 = MathTex(
            r"\kappa=23", font_size=24, color=GREEN
        ).move_to(np.array([1.72, 0.54, 0.0]))
        leader_k23 = Line(
            label_k23.get_left() + LEFT * 0.04,
            gap_center_challenge
            + normalize(label_k23.get_left() - gap_center_challenge)
            * gap_radius_challenge,
            color=GREEN,
            stroke_width=2,
        )
        target_center, target_radius = challenge_circle_data["k50"]
        unknown_radius_label = MathTex(
            r"r=?", font_size=32, color="#ff1744"
        ).move_to(np.array([1.86, -0.72, 0.0]))
        unknown_radius_leader = Arrow(
            unknown_radius_label.get_left() + LEFT * 0.05,
            target_center
            + normalize(unknown_radius_label.get_left() - target_center)
            * target_radius,
            buff=0.02,
            color="#ff1744",
            stroke_width=3,
            max_tip_length_to_length_ratio=0.18,
        )
        challenge_annotations = VGroup(
            label_k2,
            label_k3,
            label_k6,
            leader_k6,
            label_k23,
            leader_k23,
            unknown_radius_label,
            unknown_radius_leader,
        )

        visible_proof = VGroup(
            theorem_title,
            roots,
            inner_circles,
            curvature_labels,
            outer_circle,
            gap_circle,
            positive_note,
            payoff,
            payoff_box,
        )
        self.play(
            FadeOut(visible_proof),
            FadeIn(generalization_title, shift=UP * 0.12),
            self.camera.frame.animate.scale(0.96).move_to(DOWN * 0.12),
            run_time=1.0,
        )
        self.play(
            Write(generalization),
            FadeIn(parameter_note, shift=UP * 0.08),
            run_time=1.0,
        )
        self.play(
            FadeIn(local_rule_note, shift=UP * 0.08),
            FadeIn(challenge_prompt, shift=UP * 0.08),
            run_time=0.8,
        )
        self.play(
            LaggedStart(
                *[Create(circle) for circle in challenge_circles],
                lag_ratio=0.08,
            ),
            run_time=1.4,
        )
        self.play(
            FadeIn(challenge_annotations),
            run_time=0.8,
        )
        self.wait(1.5)

        animate_End(scene=self)
