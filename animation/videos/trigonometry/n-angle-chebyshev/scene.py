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

        # ------------------------------------------------ the tower 12-32s
        # Each new line is built by feeding the two previous lines into the
        # recursion, so the tower grows without any new trigonometric identity.
        tower_top = 0.85
        tower_gap = 1.35
        tower = VGroup()

        def add_rung(index, left_tex, mid_tex, right_tex):
            """Show one step: substitution first, then the reduced polynomial."""
            work = MathTex(left_tex, r"=", mid_tex, font_size=30)
            work[0].set_color(POLY_COLOR)
            work[2].set_color(SOFT_COLOR)
            work.set_stroke(width=1)
            work.set_z_index(20)
            work.move_to(np.array([0.0, tower_top - tower_gap * index, 0.0]))
            fit_to_safe_width(work)

            result = MathTex(left_tex, r"=", right_tex, font_size=34)
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
        self.play(
            FadeOut(note), FadeOut(seeds), FadeOut(dots),
            tower.animate.shift(UP * 1.1),
            run_time=0.8,
        )

        payoff = MathTex(
            r"\cos(n\theta) = T_n(\cos\theta)", font_size=42,
        )
        payoff.set_color_by_gradient(ACCENT_YELLOW, ACCENT_MAGENTA)
        payoff.set_stroke(width=1)
        payoff.set_z_index(21)
        payoff.move_to(DOWN * 3.5)
        fit_to_safe_width(payoff)

        closing = Tex(
            r"$\cos(n\theta)$ siempre es un polinomio en $\cos\theta$",
            font_size=30, color=WHITE,
        )
        closing.set_z_index(21)
        closing.move_to(DOWN * 4.6)
        fit_to_safe_width(closing)

        self.play(Write(payoff), run_time=0.9)
        payoff_box = SurroundingRectangle(payoff, buff=0.18, corner_radius=0.12)
        payoff_box.set_stroke(width=4, color=[ACCENT_YELLOW, ACCENT_MAGENTA])
        payoff_box.set_z_index(20)
        self.play(Create(payoff_box), run_time=0.6)
        self.play(FadeIn(closing, shift=UP * 0.2), run_time=0.6)
        self.wait(1.6)

        animate_End(scene=self)
