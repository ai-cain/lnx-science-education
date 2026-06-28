from manim import *
from lnx import *

# paradox | algebra | intermediate
# The n-th roots of unity.
#
# School answer to "how many solutions does z^5 = 1 have?" is one: z = 1.
# The true answer is five. Over the complex numbers z^n = 1 has exactly n
# solutions, and they sit on the unit circumference as the vertices of a
# regular n-gon:
#       z_k = cos(2*pi*k/n) + i*sin(2*pi*k/n),   k = 0, 1, ..., n-1.
#
# Closing fact: for n >= 2 the roots add up to zero. Their centroid is the
# center of the circumference, so the sum of the position vectors vanishes.
#
# Real frame is 9 x 16 units (x in [-4.5, 4.5], y in [-8, 8]).
# Safe area: |x| <= 3.8 and |y| <= 5.6.

SAFE_WIDTH = 7.2

# Radius of the unit circumference in scene units. One "mathematical unit"
# equals this many scene units, so every root lands on the circumference.
R = 2.05

# The construction sits slightly below center to leave room for the title.
CENTER = np.array([0.0, -0.55, 0.0])


def fit_to_safe_width(mobject):
    """Shrink a mobject that would spill outside the horizontal safe area."""
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def root_point(k, n):
    """Scene point of the k-th n-th root of unity."""
    angle = TAU * k / n
    return CENTER + R * np.array([np.cos(angle), np.sin(angle), 0.0])


class RootsOfUnity(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        CIRC_COLOR = ACCENT_CYAN       # the unit circumference
        ROOT_COLOR = ACCENT_YELLOW     # the roots themselves
        POLY_COLOR = ACCENT_MAGENTA    # the regular polygon they form
        SUM_COLOR = ACCENT_PURPLE      # the vanishing sum

        def make_circumference():
            circ = Circle(radius=R, color=CIRC_COLOR, stroke_width=5)
            circ.move_to(CENTER)
            circ.set_z_index(2)
            return circ

        def make_roots(n):
            dots = VGroup(*[
                Dot(root_point(k, n), radius=0.09, color=ROOT_COLOR)
                for k in range(n)
            ])
            dots.set_z_index(8)
            return dots

        def make_polygon(n):
            poly = Polygon(
                *[root_point(k, n) for k in range(n)],
                stroke_color=POLY_COLOR, stroke_width=6,
                fill_color=POLY_COLOR, fill_opacity=0.18,
            )
            poly.set_z_index(4)
            return poly

        def make_spokes(n, color, width=3):
            spokes = VGroup(*[
                Line(CENTER, root_point(k, n), color=color, stroke_width=width)
                for k in range(n)
            ])
            spokes.set_z_index(6)
            return spokes

        # ------------------------------------------------------------ hook 0-2s
        # The question lands immediately, with the wrong school answer crossed
        # out and the right one taking its place.
        question = MathTex(r"z^5 = 1", font_size=76, color=WHITE)
        question.set_stroke(width=1)
        question.set_z_index(20)
        question.move_to(UP * 3.2)
        fit_to_safe_width(question)
        self.play(Write(question), run_time=0.7)

        wrong = Tex(r"``una soluci\'on''", font_size=40, color=GREY_B)
        wrong.set_z_index(20)
        wrong.next_to(question, DOWN, buff=0.55)
        self.play(FadeIn(wrong, shift=UP * 0.15), run_time=0.5)

        strike = Line(
            wrong.get_left() + LEFT * 0.1,
            wrong.get_right() + RIGHT * 0.1,
            color=ACCENT_MAGENTA, stroke_width=5,
        )
        strike.set_z_index(21)
        self.play(Create(strike), run_time=0.4)

        right = Tex(r"son \textbf{cinco}", font_size=44, color=ACCENT_YELLOW)
        right.set_z_index(20)
        right.move_to(wrong)
        self.play(
            FadeOut(wrong), FadeOut(strike),
            FadeIn(right, scale=1.2),
            run_time=0.6,
        )
        self.wait(0.5)

        # --------------------------------------- beat 1: the pentagon appears
        # The five roots are shown where they actually live: on the unit
        # circumference of the complex plane.
        self.play(
            question.animate.move_to(UP * 4.9).scale(0.72),
            FadeOut(right),
            run_time=0.6,
        )

        circumference = make_circumference()
        origin_dot = Dot(CENTER, radius=0.05, color=GREY_A)
        origin_dot.set_z_index(7)
        axes = VGroup(
            Line(CENTER + LEFT * (R + 0.7), CENTER + RIGHT * (R + 0.7),
                 color=GREY_B, stroke_width=2),
            Line(CENTER + DOWN * (R + 0.7), CENTER + UP * (R + 0.7),
                 color=GREY_B, stroke_width=2),
        )
        axes.set_z_index(0)

        self.play(Create(axes), run_time=0.4)
        self.play(Create(circumference), run_time=0.9)
        self.add(origin_dot)

        circ_label = Tex(r"circunferencia unitaria", font_size=28, color=CIRC_COLOR)
        circ_label.set_z_index(20)
        circ_label.move_to(DOWN * 4.95)
        fit_to_safe_width(circ_label)
        self.play(FadeIn(circ_label), run_time=0.4)

        roots5 = make_roots(5)
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in roots5], lag_ratio=0.25),
            run_time=1.3,
        )

        pentagon = make_polygon(5)
        self.play(Create(pentagon), run_time=1.0)
        self.wait(0.4)

        formula = MathTex(
            r"z_k=\cos\tfrac{2\pi k}{5}+i\,\sin\tfrac{2\pi k}{5}",
            font_size=34, color=WHITE,
        )
        formula.set_stroke(width=1)
        formula.set_z_index(20)
        formula.move_to(DOWN * 4.15)
        fit_to_safe_width(formula)
        self.play(FadeOut(circ_label), run_time=0.25)
        self.play(Write(formula), run_time=0.9)

        pentagon_note = Tex(r"un pent\'agono regular", font_size=30, color=POLY_COLOR)
        pentagon_note.set_z_index(20)
        pentagon_note.move_to(DOWN * 5.05)
        fit_to_safe_width(pentagon_note)
        self.play(FadeIn(pentagon_note, shift=UP * 0.15), run_time=0.5)
        self.wait(0.9)

        # ------------------------------------------- beat 2: n = 3, 5 and 8
        # Same rule, different n: the polygon simply gains sides.
        self.play(FadeOut(formula), FadeOut(pentagon_note), run_time=0.4)

        n_label = MathTex(r"n=5", font_size=44, color=ROOT_COLOR)
        n_label.set_stroke(width=1)
        n_label.set_z_index(20)
        n_label.move_to(DOWN * 4.3)
        self.play(
            ReplacementTransform(question, n_label),
            run_time=0.6,
        )

        count_note = Tex(r"$n$ ra\'ices, $n$ v\'ertices", font_size=30, color=WHITE)
        count_note.set_z_index(20)
        count_note.move_to(DOWN * 5.15)
        fit_to_safe_width(count_note)
        self.play(FadeIn(count_note), run_time=0.4)

        current_roots = roots5
        current_poly = pentagon

        for n in (3, 8):
            new_roots = make_roots(n)
            new_poly = make_polygon(n)
            new_label = MathTex(rf"n={n}", font_size=44, color=ROOT_COLOR)
            new_label.set_stroke(width=1)
            new_label.set_z_index(20)
            new_label.move_to(DOWN * 4.3)

            self.play(
                Transform(current_poly, new_poly),
                Transform(current_roots, new_roots),
                Transform(n_label, new_label),
                run_time=1.1,
            )
            self.wait(0.7)

        # ------------------------------------------ beat 3: the roots add to 0
        # Every root is a position vector from the center. Because the vertices
        # are symmetric about the center, their centroid IS the center, so the
        # vectors cancel exactly.
        self.play(FadeOut(count_note), FadeOut(current_poly), run_time=0.5)

        spokes = make_spokes(8, SUM_COLOR, width=4)
        self.play(
            LaggedStart(*[GrowFromPoint(s, CENTER) for s in spokes],
                        lag_ratio=0.12),
            run_time=1.2,
        )

        sum_note = Tex(r"cada ra\'iz es un vector", font_size=30, color=SUM_COLOR)
        sum_note.set_z_index(20)
        sum_note.move_to(DOWN * 5.15)
        fit_to_safe_width(sum_note)
        self.play(FadeIn(sum_note), run_time=0.4)
        self.wait(0.5)

        # Collapse everything into the center: the sum is zero.
        center_flash = Dot(CENTER, radius=0.14, color=SUM_COLOR)
        center_flash.set_z_index(12)
        self.play(
            FadeOut(sum_note),
            FadeOut(n_label),
            # Not exactly zero: a degenerate mobject can break stroke rendering.
            spokes.animate.scale(0.02, about_point=CENTER),
            current_roots.animate.move_to(CENTER).scale(0.35),
            circumference.animate.set_stroke(opacity=0.25),
            run_time=1.3,
        )
        self.add(center_flash)
        self.play(Flash(center_flash, color=SUM_COLOR, line_length=0.35,
                        num_lines=14, flash_radius=0.55), run_time=0.7)

        # ------------------------------------------------------------ payoff
        self.play(
            FadeOut(spokes), FadeOut(current_roots), FadeOut(axes),
            FadeOut(origin_dot), FadeOut(circumference), FadeOut(center_flash),
            run_time=0.5,
        )

        closing = VGroup(
            MathTex(r"z^n = 1 \;\Rightarrow\; n \text{ ra\'ices}", font_size=42),
            MathTex(r"z_0 + z_1 + \cdots + z_{n-1} = 0", font_size=40),
        )
        closing[0].set_color(ROOT_COLOR)
        closing[1].set_color(SUM_COLOR)
        closing.arrange(DOWN, buff=0.55)
        closing.set_stroke(width=1)
        closing.set_z_index(21)
        closing.move_to(ORIGIN)
        fit_to_safe_width(closing)

        self.play(Write(closing[0]), run_time=0.9)
        self.play(Write(closing[1]), run_time=0.9)

        result_box = SurroundingRectangle(closing, buff=0.32, corner_radius=0.14)
        result_box.set_stroke(width=4, color=[ACCENT_YELLOW, ACCENT_PURPLE])
        result_box.set_z_index(20)
        self.play(Create(result_box), run_time=0.7)
        self.wait(1.6)

        animate_End(scene=self)
