from manim import *
from lnx import *

# proof-without-words | algebra | intermediate
# Nicomachus' theorem: 1^3 + 2^3 + ... + n^3 = (1 + 2 + ... + n)^2.
#
# The sum of the first n cubes is the SQUARE of the n-th triangular number.
# With T_k = 1 + 2 + ... + k = k(k+1)/2, the identity reads
#       sum_{k=1..n} k^3 = T_n^2.
#
# Visual proof used here (n = 4, so T_4 = 10 and the big square is 10 x 10):
# take the square of side T_n and peel it into L-shaped gnomons. The k-th
# gnomon is the square of side T_k minus the square of side T_{k-1}, so it is
# a band of thickness T_k - T_{k-1} = k. Splitting that L into its two arms:
#       right arm  = k * T_k          (thickness k, height T_k)
#       top arm    = k * T_{k-1}      (thickness k, width T_{k-1})
#       total      = k * (T_k + T_{k-1}) = k * k^2 = k^3
# because T_k + T_{k-1} = k(k+1)/2 + (k-1)k/2 = k^2. So each gnomon is exactly
# k copies of a k x k square, i.e. k^3.
#
# Numeric check for n = 4 (T = 0, 1, 3, 6, 10):
#   k=1: 1*(1+0)  = 1    = 1^3
#   k=2: 2*(3+1)  = 8    = 2^3
#   k=3: 3*(6+3)  = 27   = 3^3
#   k=4: 4*(10+6) = 64   = 4^3
#   1 + 8 + 27 + 64 = 100 = 10^2 = (1+2+3+4)^2.   Correct.
#
# The real frame is 9 x 16 units (x in [-4.5, 4.5], y in [-8, 8]).
# Safe area: |x| <= 3.8 and |y| <= 5.6.

SAFE_WIDTH = 7.2

N = 4

# Triangular numbers T_0..T_N. TRI[k] = 1 + 2 + ... + k.
TRI = [k * (k + 1) // 2 for k in range(N + 1)]  # [0, 1, 3, 6, 10]
SIDE = TRI[N]  # 10 cells per side of the big square

# One cell of the big square, in scene units. 10 * 0.62 = 6.2 < SAFE_WIDTH.
UNIT = 0.62

# Bottom-left corner of the big square. The square grows up and to the right,
# so the corner is pushed down-left to keep the whole figure in the safe area.
GRID_ORIGIN = np.array([-3.1, -3.85, 0.0])

# One accent per gnomon, in peeling order k = 1..4.
GNOMON_COLORS = [ACCENT_CYAN, ACCENT_MAGENTA, ACCENT_YELLOW, ACCENT_PURPLE]


def fit_to_safe_width(mobject):
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def P(x, y):
    """Cell coordinate of the big square -> scene point."""
    return GRID_ORIGIN + np.array([x * UNIT, y * UNIT, 0.0])


def gnomon_points(k):
    """Corners of the k-th L-gnomon: square of side T_k minus square T_{k-1}."""
    inner, outer = TRI[k - 1], TRI[k]
    return [
        (inner, 0),
        (outer, 0),
        (outer, outer),
        (0, outer),
        (0, inner),
        (inner, inner),
    ]


class SumOfCubes(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.14
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.85)
        self.add(watermark)

        def make_gnomon(k, opacity=0.45):
            poly = Polygon(
                *[P(x, y) for x, y in gnomon_points(k)],
                stroke_color=GNOMON_COLORS[k - 1],
                stroke_width=5,
                fill_color=GNOMON_COLORS[k - 1],
                fill_opacity=opacity,
            )
            poly.set_z_index(3)
            return poly

        def make_grid():
            """Faint unit grid over the big square: every cell is 1 x 1."""
            lines = VGroup()
            for i in range(SIDE + 1):
                lines.add(Line(P(i, 0), P(i, SIDE)))
                lines.add(Line(P(0, i), P(SIDE, i)))
            lines.set_stroke(color=GREY_B, width=1.4, opacity=0.35)
            lines.set_z_index(5)
            return lines

        # ---------------------------------------------------------- hook 0-2 s
        # The finished mosaic lands on screen immediately: four coloured L's
        # that together are one perfect square. That image is the whole video.
        title = Tex(r"Suma de cubos", font_size=60, color=WHITE)
        title.set_stroke(width=1)
        title.set_z_index(20)
        title.move_to(UP * 5.35)
        fit_to_safe_width(title)

        underline = Line(
            title.get_left() + DOWN * 0.28,
            title.get_right() + DOWN * 0.28,
            stroke_width=4,
        )
        underline.set_color(color=[ACCENT_CYAN, ACCENT_MAGENTA])
        underline.set_z_index(20)

        mosaic = VGroup(*[make_gnomon(k) for k in range(1, N + 1)])

        self.add(title, underline)
        self.play(
            LaggedStart(*[FadeIn(g, scale=0.85) for g in mosaic], lag_ratio=0.18),
            run_time=1.2,
        )

        hook = Tex(
            r"sumar cubos no deber\'ia dar\\un cuadrado perfecto",
            font_size=32, color=GREY_A,
        )
        hook.set_z_index(20)
        hook.move_to(DOWN * 4.95)
        fit_to_safe_width(hook)
        self.play(FadeIn(hook, shift=UP * 0.15), run_time=0.6)
        self.wait(0.7)

        hook2 = Tex(r"y sin embargo siempre lo es", font_size=34, color=ACCENT_YELLOW)
        hook2.set_z_index(20)
        hook2.move_to(DOWN * 4.95)
        fit_to_safe_width(hook2)
        self.play(ReplacementTransform(hook, hook2), run_time=0.6)
        self.wait(0.8)

        # ------------------------------------------- beat 1: the outer square
        # The mosaic is really one square of side 1+2+3+4 = 10, area 10^2 = 100.
        self.play(mosaic.animate.set_fill(opacity=0.12).set_stroke(opacity=0.25),
                  FadeOut(hook2), run_time=0.6)

        grid = make_grid()
        outline = Square(side_length=SIDE * UNIT, stroke_color=WHITE, stroke_width=6)
        outline.move_to(P(SIDE / 2, SIDE / 2))
        outline.set_z_index(8)

        self.play(Create(outline), FadeIn(grid), run_time=1.0)

        side_label = MathTex(r"1+2+3+4=10", font_size=34, color=WHITE)
        side_label.set_stroke(width=1)
        side_label.set_z_index(20)
        side_label.next_to(outline, DOWN, buff=0.28)
        fit_to_safe_width(side_label)
        self.play(Write(side_label), run_time=0.8)

        area_label = MathTex(r"\text{\'area}=10^2=100", font_size=38, color=WHITE)
        area_label.set_stroke(width=1)
        area_label.set_z_index(20)
        area_label.move_to(UP * 3.95)
        fit_to_safe_width(area_label)
        self.play(Write(area_label), run_time=0.8)
        self.wait(0.6)

        # ------------------------------------ beat 2: peel the square into L's
        # Every gnomon is a band of thickness k. Its two arms measure k*T_k and
        # k*T_{k-1}, and T_k + T_{k-1} = k^2, so the L has area exactly k^3.
        peel_text = Tex(r"cada capa en $L$ mide $k^3$", font_size=32, color=GREY_A)
        peel_text.set_z_index(20)
        peel_text.move_to(DOWN * 4.95)
        fit_to_safe_width(peel_text)
        self.play(FadeIn(peel_text, shift=UP * 0.15), run_time=0.5)

        # Running sum built once so nothing shifts while terms appear.
        sum_tex = MathTex(
            r"1^3", r"+2^3", r"+3^3", r"+4^3", r"=100",
            font_size=42,
        )
        for index in range(N):
            sum_tex[index].set_color(GNOMON_COLORS[index])
        sum_tex[N].set_color(WHITE)
        sum_tex.set_stroke(width=1)
        sum_tex.set_z_index(20)
        sum_tex.move_to(UP * 3.95)
        fit_to_safe_width(sum_tex)
        for part in sum_tex:
            part.set_opacity(0.0)
        self.add(sum_tex)
        self.play(FadeOut(area_label), run_time=0.35)

        for k in range(1, N + 1):
            color = GNOMON_COLORS[k - 1]
            gnomon = mosaic[k - 1]

            # Dashed cut between the two arms of the L, so the split is visible.
            cut = DashedLine(
                P(TRI[k - 1], TRI[k - 1]), P(TRI[k - 1], TRI[k]),
                color=BG, stroke_width=3,
            )
            cut.set_z_index(9)

            arms = MathTex(
                rf"{k}\cdot({TRI[k]}+{TRI[k - 1]})={k}\cdot {k}^2={k ** 3}",
                font_size=34, color=color,
            )
            arms.set_stroke(width=1)
            arms.set_z_index(20)
            arms.move_to(DOWN * 4.95)
            fit_to_safe_width(arms)

            self.play(
                gnomon.animate.set_fill(opacity=0.55).set_stroke(opacity=1.0),
                Create(cut),
                run_time=0.5,
            )
            if k == 1:
                self.play(ReplacementTransform(peel_text, arms), run_time=0.5)
                previous_arms = arms
            else:
                self.play(ReplacementTransform(previous_arms, arms), run_time=0.5)
                previous_arms = arms

            self.play(sum_tex[k - 1].animate.set_opacity(1.0), run_time=0.45)
            self.play(
                gnomon.animate.set_fill(opacity=0.32),
                FadeOut(cut),
                run_time=0.4,
            )

        # ----------------------------------------------- beat 3: both readings
        # Same square, two ways of counting it: cube by cube, or side squared.
        self.play(FadeOut(previous_arms), run_time=0.35)
        self.play(sum_tex[N].animate.set_opacity(1.0), run_time=0.6)

        equals = MathTex(r"100=10^2=(1+2+3+4)^2", font_size=34, color=ACCENT_YELLOW)
        equals.set_stroke(width=1)
        equals.set_z_index(20)
        equals.move_to(DOWN * 4.95)
        fit_to_safe_width(equals)
        self.play(FadeIn(equals, shift=UP * 0.15), run_time=0.6)
        self.play(Indicate(outline, color=ACCENT_YELLOW, scale_factor=1.03), run_time=0.8)
        self.wait(0.8)

        # ----------------------------------------------------------- payoff
        self.play(
            FadeOut(mosaic), FadeOut(grid), FadeOut(outline),
            FadeOut(side_label), FadeOut(sum_tex), FadeOut(equals),
            FadeOut(title), FadeOut(underline),
            run_time=0.7,
        )

        closing = VGroup(
            MathTex(r"1^3+2^3+\cdots+n^3=(1+2+\cdots+n)^2", font_size=36),
            Tex(r"la suma de los cubos\\es el cuadrado de la suma",
                font_size=32, color=GREY_A),
        )
        closing[0].set_color(color=[ACCENT_CYAN, ACCENT_MAGENTA])
        closing.arrange(DOWN, buff=0.6)
        closing[0].set_stroke(width=1)
        closing.set_z_index(21)
        closing.move_to(ORIGIN)
        fit_to_safe_width(closing)

        self.play(Write(closing[0]), run_time=1.1)
        self.play(FadeIn(closing[1], shift=UP * 0.15), run_time=0.7)

        result_box = SurroundingRectangle(closing, buff=0.32, corner_radius=0.14)
        result_box.set_stroke(width=4, color=[ACCENT_YELLOW, ACCENT_PURPLE])
        result_box.set_z_index(20)
        self.play(Create(result_box), run_time=0.7)
        self.wait(1.8)

        animate_End(scene=self)
