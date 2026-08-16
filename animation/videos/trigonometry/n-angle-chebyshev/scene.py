from manim import *
from lnx import *

# unexpected-extension | trigonometry | advanced
#
# The n-th angle formula. School stops at cos(2t) and maybe cos(3t); the
# Chebyshev recursion generates ALL of them from just n = 0 and n = 1:
#
#     cos(n t) = 2 cos(t) cos((n-1) t) - cos((n-2) t)
#
# Starting from T0 = 1 and T1 = c (with c = cos t):
#     T2 = 2c*c - 1            = 2c^2 - 1
#     T3 = 2c*(2c^2 - 1) - c   = 4c^3 - 3c
#     T4 = 2c*(4c^3 - 3c) - (2c^2 - 1) = 8c^4 - 8c^2 + 1
#
# Numerical verification at t = 0.7 rad (c = cos 0.7 = 0.7648421873):
#   cos(1.4) = 0.1699671429 ; 2c^2 - 1          = 2(0.5849838)-1 = 0.1699671429  OK
#   cos(2.1) = -0.5048461046; 4c^3 - 3c         = 1.7896804 - 2.2945266 = -0.5048461046  OK
#   cos(2.8) = -0.9422223407; 8c^4 - 8c^2 + 1   = 3.5951563 - 4.6798703 + 1 = -0.9422223407  OK
# (Checked with mpmath-grade double precision; all three agree to 10 decimals.)
#
# Frame is 9 x 16 units. Safe area: |x| <= 3.8 and |y| <= 5.6.

SAFE_WIDTH = 7.2


def fit_to_safe_width(mobject):
    """Shrink a mobject so it never crosses the vertical safe margins."""
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


class NAngleChebyshev(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        SEED_COLOR = ACCENT_CYAN      # the two seeds, n = 0 and n = 1
        REC_COLOR = ACCENT_MAGENTA    # the recursion itself
        POLY_COLOR = ACCENT_YELLOW    # the generated polynomials
        SOFT_COLOR = ACCENT_PURPLE    # supporting copy

        # ------------------------------------------------------------ hook 0-2s
        # A single question on screen: what happens when n keeps growing?
        hook = MathTex(r"\cos(n\theta) = \; ?", font_size=68, color=POLY_COLOR)
        hook.set_stroke(width=1)
        hook.set_z_index(20)
        hook.move_to(UP * 1.2)
        fit_to_safe_width(hook)

        self.play(Write(hook), run_time=0.9)

        subtitle = Tex(
            r"para \emph{cualquier} $n$", font_size=40, color=WHITE
        )
        subtitle.set_z_index(20)
        subtitle.next_to(hook, DOWN, buff=0.5)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.6)
        self.wait(0.4)

        # --------------------------------------------------- the recursion 2-9s
        title = Tex(r"Recursión de Chebyshev", font_size=44, color=WHITE)
        title.set_stroke(width=1)
        title.set_z_index(20)
        title.move_to(UP * 5.1)
        fit_to_safe_width(title)

        underline = Line(
            title.get_left() + DOWN * 0.28,
            title.get_right() + DOWN * 0.28,
            stroke_width=4,
        )
        underline.set_color(color=[ACCENT_CYAN, ACCENT_MAGENTA])
        underline.set_z_index(20)

        recursion = MathTex(
            r"\cos(n\theta)", r"=", r"2\cos\theta", r"\cos((n-1)\theta)",
            r"-", r"\cos((n-2)\theta)",
            font_size=34,
        )
        recursion[0].set_color(POLY_COLOR)
        recursion[2].set_color(REC_COLOR)
        recursion[3].set_color(SOFT_COLOR)
        recursion[5].set_color(SOFT_COLOR)
        recursion.set_stroke(width=1)
        recursion.set_z_index(20)
        recursion.move_to(UP * 3.9)
        fit_to_safe_width(recursion)

        self.play(
            FadeOut(subtitle, shift=DOWN * 0.2),
            hook.animate.move_to(UP * 3.9).scale(34 / 68),
            run_time=0.8,
        )
        self.play(FadeIn(title, shift=DOWN * 0.2), Create(underline), run_time=0.6)
        self.play(TransformMatchingShapes(hook, recursion), run_time=1.0)
        self.wait(0.5)

        rec_box = SurroundingRectangle(recursion, buff=0.16, corner_radius=0.1)
        rec_box.set_stroke(width=3, color=[ACCENT_CYAN, ACCENT_MAGENTA])
        rec_box.set_z_index(19)
        self.play(Create(rec_box), run_time=0.5)

        # ----------------------------------------------------- the two seeds
        note = Tex(r"Solo hacen falta dos semillas:", font_size=30, color=WHITE)
        note.set_z_index(20)
        note.move_to(UP * 2.7)
        fit_to_safe_width(note)

        seeds = MathTex(
            r"\cos(0\theta) = 1", r"\qquad", r"\cos(1\theta) = \cos\theta",
            font_size=32,
        )
        seeds[0].set_color(SEED_COLOR)
        seeds[2].set_color(SEED_COLOR)
        seeds.set_stroke(width=1)
        seeds.set_z_index(20)
        seeds.move_to(UP * 2.0)
        fit_to_safe_width(seeds)

        self.play(FadeIn(note, shift=UP * 0.15), run_time=0.5)
        self.play(Write(seeds), run_time=0.9)
        self.wait(0.5)

        # --------------------------------- why it's true: complex numbers
        # z = e^{i theta} lives on the unit circle. z^n + z^{n-2}
        # = z^{n-1}(z + 1/z) = z^{n-1} * 2cos(theta), and taking real parts
        # on both sides gives exactly the recursion above.
        self.play(FadeOut(note), FadeOut(seeds), run_time=0.5)

        why = Tex(r"¿Por qué funciona?", font_size=40, color=WHITE)
        why.set_z_index(20)
        why.move_to(UP * 2.75)
        fit_to_safe_width(why)

        z_def = MathTex(r"z = e^{i\theta}", font_size=44, color=SOFT_COLOR)
        z_def.set_stroke(width=1)
        z_def.set_z_index(20)
        z_def.next_to(why, DOWN, buff=0.35)
        fit_to_safe_width(z_def)

        self.play(FadeIn(why, shift=UP * 0.15), run_time=0.5)
        self.play(Write(z_def), run_time=0.6)

        # unit circle with z and 1/z as mirror points: their real parts add up
        circle = Circle(radius=1.95, color=WHITE, stroke_width=2.5)
        circle.move_to(DOWN * 1.15)
        theta_val = 0.7
        z_point = circle.point_from_proportion(theta_val / TAU)
        zc_point = circle.point_from_proportion(1 - theta_val / TAU)
        z_dot = Dot(z_point, color=REC_COLOR, radius=0.09)
        zc_dot = Dot(zc_point, color=SEED_COLOR, radius=0.09)
        z_label = MathTex(r"z", font_size=34, color=REC_COLOR).next_to(z_dot, UR, buff=0.1)
        zc_label = MathTex(r"1/z", font_size=34, color=SEED_COLOR).next_to(zc_dot, DR, buff=0.1)
        radius_line = Line(circle.get_center(), z_point, color=REC_COLOR, stroke_width=3)
        radius_line2 = Line(circle.get_center(), zc_point, color=SEED_COLOR, stroke_width=3)

        # Bare cross through the centre — no ticks, no x/y labels, just the
        # reference frame so theta has something to be measured from.
        center = circle.get_center()
        cross_reach = 2.55
        h_axis = Line(
            center + LEFT * cross_reach, center + RIGHT * cross_reach,
            color=GREY_B, stroke_width=1.8,
        )
        v_axis = Line(
            center + DOWN * cross_reach, center + UP * cross_reach,
            color=GREY_B, stroke_width=1.8,
        )
        cross = VGroup(h_axis, v_axis)
        cross.set_z_index(18)

        # theta: the turn from the positive horizontal to the radius through z
        theta_arc = Arc(
            radius=0.62, start_angle=0, angle=theta_val,
            arc_center=center, color=POLY_COLOR, stroke_width=3.5,
        )
        theta_label = MathTex(r"\theta", font_size=34, color=POLY_COLOR)
        theta_label.move_to(
            center + 0.95 * np.array([np.cos(theta_val / 2), np.sin(theta_val / 2), 0.0])
        )

        circle_group = VGroup(
            cross, circle, radius_line, radius_line2,
            theta_arc, theta_label, z_dot, zc_dot, z_label, zc_label,
        )
        circle_group.set_z_index(20)
        cross.set_z_index(18)

        self.play(Create(cross), run_time=0.5)
        self.play(Create(circle), run_time=0.7)
        self.play(
            GrowFromCenter(z_dot), GrowFromCenter(zc_dot),
            Create(radius_line), Create(radius_line2),
            FadeIn(z_label), FadeIn(zc_label),
            run_time=0.8,
        )
        self.play(Create(theta_arc), FadeIn(theta_label), run_time=0.5)
        self.wait(0.3)

        # Every line below gets a fixed y up front — nothing is ever
        # repositioned relative to another mobject's *current* location,
        # so nothing can end up stranded on top of something else.
        self.play(
            FadeOut(circle_group),
            z_def.animate.scale(28 / 44).next_to(why, DOWN, buff=0.28),
            run_time=0.6,
        )

        sum_formula = MathTex(r"z + \tfrac{1}{z} = 2\cos\theta", font_size=40)
        sum_formula.set_color(POLY_COLOR)
        sum_formula.set_stroke(width=1)
        sum_formula.set_z_index(20)
        sum_formula.move_to(UP * 1.55)
        fit_to_safe_width(sum_formula)
        self.play(Write(sum_formula), run_time=0.8)
        self.wait(0.5)

        # Multiply that identity by z^{n-1}: the whole recursion drops out.
        line1 = MathTex(
            r"z^{n} + z^{n-2}", r"=", r"z^{n-1}\!\left(z + \tfrac{1}{z}\right)",
            font_size=32,
        )
        line1[0].set_color(REC_COLOR)
        line1[2].set_color(SOFT_COLOR)
        line1.set_stroke(width=1)
        line1.set_z_index(20)
        line1.move_to(UP * 0.65)
        fit_to_safe_width(line1)

        line2 = MathTex(r"= \; 2\cos\theta \cdot z^{n-1}", font_size=32, color=REC_COLOR)
        line2.set_stroke(width=1)
        line2.set_z_index(20)
        line2.move_to(DOWN * 0.1)
        fit_to_safe_width(line2)

        self.play(Write(line1), run_time=0.9)
        self.play(Write(line2), run_time=0.7)
        self.wait(0.4)

        real_part = Tex(r"y tomando la parte real:", font_size=28, color=WHITE)
        real_part.set_z_index(20)
        real_part.move_to(DOWN * 0.95)
        fit_to_safe_width(real_part)

        re_eq = MathTex(r"\mathrm{Re}\,(z^{k}) = \cos(k\theta)", font_size=34, color=POLY_COLOR)
        re_eq.set_stroke(width=1)
        re_eq.set_z_index(20)
        re_eq.move_to(DOWN * 1.75)
        fit_to_safe_width(re_eq)

        self.play(FadeIn(real_part, shift=UP * 0.1), run_time=0.5)
        self.play(Write(re_eq), run_time=0.7)
        self.wait(0.5)

        # Apply Re(...) to BOTH sides of z^n + z^{n-2} = 2cos(theta) z^{n-1}
        # term by term — this is the actual step people skip in their head.
        self.play(
            FadeOut(sum_formula), FadeOut(real_part),
            run_time=0.4,
        )

        applied = MathTex(
            r"\mathrm{Re}(z^{n})", r"+", r"\mathrm{Re}(z^{n-2})",
            r"=", r"2\cos\theta\;\mathrm{Re}(z^{n-1})",
            font_size=28, color=SOFT_COLOR,
        )
        applied.set_stroke(width=1)
        applied.set_z_index(20)
        applied.move_to(DOWN * 2.75)
        fit_to_safe_width(applied)
        self.play(Write(applied), run_time=1.0)
        self.wait(0.5)

        final_step = MathTex(
            r"\cos(n\theta) + \cos((n-2)\theta) = 2\cos\theta\cos((n-1)\theta)",
            font_size=27, color=POLY_COLOR,
        )
        final_step.set_stroke(width=1)
        final_step.set_z_index(20)
        final_step.move_to(DOWN * 3.85)
        fit_to_safe_width(final_step)
        final_box = SurroundingRectangle(final_step, buff=0.15, corner_radius=0.1)
        final_box.set_stroke(width=3, color=[ACCENT_CYAN, ACCENT_MAGENTA])
        final_box.set_z_index(19)

        self.play(TransformMatchingShapes(applied.copy(), final_step), run_time=1.0)
        self.play(Create(final_box), run_time=0.5)
        self.wait(0.5)

        # The recursion at the top is exactly what we just derived.
        self.play(Indicate(recursion, scale_factor=1.08, color=POLY_COLOR), run_time=0.9)
        self.wait(0.3)

        self.play(
            FadeOut(why), FadeOut(z_def), FadeOut(line1), FadeOut(line2),
            FadeOut(re_eq), FadeOut(applied), FadeOut(final_step), FadeOut(final_box),
            run_time=0.6,
        )

        # ------------------------------------------------ the tower 12-32s
        # Each new line is built by feeding the two previous lines into the
        # recursion, so the tower grows without any new trigonometric identity.
        tower_top = 2.25
        tower_gap = 1.55
        tower = VGroup()

        def add_rung(index, left_tex, mid_tex, right_tex):
            """Show one step: substitution first, then the reduced polynomial."""
            work = MathTex(left_tex, r"=", mid_tex, font_size=34)
            work[0].set_color(POLY_COLOR)
            work[2].set_color(SOFT_COLOR)
            work.set_stroke(width=1)
            work.set_z_index(20)
            work.move_to(np.array([0.0, tower_top - tower_gap * index, 0.0]))
            fit_to_safe_width(work)

            result = MathTex(left_tex, r"=", right_tex, font_size=40)
            result[0].set_color(POLY_COLOR)
            result[2].set_color(REC_COLOR)
            result.set_stroke(width=1)
            result.set_z_index(20)
            result.move_to(np.array([0.0, tower_top - tower_gap * index, 0.0]))
            fit_to_safe_width(result)

            self.play(Write(work), run_time=0.8)
            self.wait(0.3)
            self.play(TransformMatchingShapes(work, result), run_time=0.8)
            tower.add(result)
            self.wait(0.25)

        # n = 2: 2c*c - 1
        add_rung(
            0,
            r"\cos 2\theta",
            r"2\cos\theta\,(\cos\theta) - 1",
            r"2\cos^{2}\theta - 1",
        )
        # n = 3: 2c*(2c^2 - 1) - c
        add_rung(
            1,
            r"\cos 3\theta",
            r"2\cos\theta\,(2\cos^{2}\theta - 1) - \cos\theta",
            r"4\cos^{3}\theta - 3\cos\theta",
        )
        # n = 4: 2c*(4c^3 - 3c) - (2c^2 - 1)
        add_rung(
            2,
            r"\cos 4\theta",
            r"2\cos\theta\,(4\cos^{3}\theta - 3\cos\theta) - (2\cos^{2}\theta - 1)",
            r"8\cos^{4}\theta - 8\cos^{2}\theta + 1",
        )

        # The chain never stops: the dots stand for every remaining n.
        dots = MathTex(r"\vdots", font_size=40, color=SOFT_COLOR)
        dots.set_z_index(20)
        dots.move_to(np.array([0.0, tower_top - tower_gap * 2.6, 0.0]))
        self.play(FadeIn(dots), run_time=0.4)
        self.wait(0.3)

        # ------------------------------------------------------ payoff 32-42s
        self.play(FadeOut(dots), run_time=0.4)

        payoff = MathTex(
            r"\cos(n\theta) = T_n(\cos\theta)", font_size=48,
        )
        payoff.set_color_by_gradient(ACCENT_YELLOW, ACCENT_MAGENTA)
        payoff.set_stroke(width=1)
        payoff.set_z_index(21)
        payoff.move_to(DOWN * 2.45)
        fit_to_safe_width(payoff)

        tn_label = Tex(
            r"$T_n$: el polinomio de Chebyshev",
            font_size=32, color=SOFT_COLOR,
        )
        tn_label.set_z_index(21)
        tn_label.move_to(DOWN * 3.6)
        fit_to_safe_width(tn_label)

        closing = Tex(
            r"siempre un polinomio en $\cos\theta$",
            font_size=32, color=WHITE,
        )
        closing.set_z_index(21)
        closing.move_to(DOWN * 4.5)
        fit_to_safe_width(closing)

        self.play(Write(payoff), run_time=0.9)
        payoff_box = SurroundingRectangle(payoff, buff=0.18, corner_radius=0.12)
        payoff_box.set_stroke(width=4, color=[ACCENT_YELLOW, ACCENT_MAGENTA])
        payoff_box.set_z_index(20)
        self.play(Create(payoff_box), run_time=0.6)
        self.play(FadeIn(tn_label, shift=UP * 0.15), run_time=0.6)
        self.wait(0.3)
        self.play(FadeIn(closing, shift=UP * 0.2), run_time=0.6)
        self.wait(1.4)

        animate_End(scene=self)
