from manim import *
from lnx import *

# proof-without-words | algebra | basic
#
# 1 + 3 + 5 + ... + (2n-1) = n^2
#
# The proof is a single picture. Start with one cell: a 1x1 square. To grow it
# into a 2x2 square you must add an L-shaped border (a "gnomon") made of exactly
# 3 cells. To grow 2x2 into 3x3 you add an L of 5 cells. Each gnomon for step k
# holds (k-1) cells up the new column, (k-1) cells along the new row and 1
# corner cell: 2k-1 cells, the k-th odd number.
#
# So adding the first n odd numbers is the same act as stacking n gnomons, and
# stacking n gnomons is the same act as building an n x n square. The visual
# does the whole argument: no algebra is needed at any point.
#
# Frame is 9 x 16 units. Safe area: |x| <= 3.8, |y| <= 5.6.

CELL = 0.62          # side of one unit cell in scene units
N_STEPS = 6          # build the square up to 6 x 6
SAFE_WIDTH = 7.2

# Bottom-left corner of the final N_STEPS x N_STEPS square, chosen so the whole
# square sits centered horizontally and slightly below the frame center, leaving
# room for the title above and the running equation below.
GRID_ORIGIN = np.array([-N_STEPS * CELL / 2, -1.05 - N_STEPS * CELL / 2, 0.0])

# One color per gnomon, cycled: consecutive L layers must never share a color or
# the staircase reads as a flat block.
GNOMON_COLORS = [ACCENT_CYAN, ACCENT_MAGENTA, ACCENT_YELLOW, ACCENT_PURPLE]


def fit_to_safe_width(mobject):
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def cell(col, row, color):
    """One unit square of the grid, indexed from the bottom-left corner."""
    square = Square(
        side_length=CELL,
        stroke_color=BG,
        stroke_width=2.5,
        fill_color=color,
        fill_opacity=0.9,
    )
    square.move_to(GRID_ORIGIN + np.array([(col + 0.5) * CELL, (row + 0.5) * CELL, 0.0]))
    square.set_z_index(2)
    return square


def gnomon(step, color):
    """The L-shaped layer that turns a (step-1) square into a step square.

    Its cells are exactly those with max(col, row) == step - 1, which is
    (step - 1) + (step - 1) + 1 = 2*step - 1 cells: the step-th odd number.
    Cells are ordered from the top of the new column, around the corner, out to
    the end of the new row, so LaggedStart draws the L as a single stroke.
    """
    k = step - 1
    cells = [cell(k, row, color) for row in range(k, -1, -1)]
    cells += [cell(col, k, color) for col in range(k - 1, -1, -1)]
    return VGroup(*cells)


class SumOfOddNumbers(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.14
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.85)
        self.add(watermark)

        # ---------------------------------------------------------- hook 0-2 s
        # The claim lands first, unproved and slightly absurd: adding odd numbers
        # keeps producing perfect squares. The picture then explains why.
        title = Tex(r"Suma de impares", font_size=58, color=WHITE)
        title.set_stroke(width=1)
        title.set_z_index(20)
        title.move_to(UP * 5.15)
        fit_to_safe_width(title)

        underline = Line(
            title.get_left() + DOWN * 0.28,
            title.get_right() + DOWN * 0.28,
            stroke_width=4,
        )
        underline.set_color(color=GRADIENT_MAIN)
        underline.set_z_index(20)

        claim = MathTex(
            r"1+3+5+\cdots+(2n-1)=", r"n^{2}",
            font_size=40,
        )
        claim[0].set_color(WHITE)
        claim[1].set_color(ACCENT_YELLOW)
        claim.set_stroke(width=1)
        claim.set_z_index(20)
        claim.move_to(UP * 4.15)
        fit_to_safe_width(claim)

        self.play(Write(title), run_time=0.6)
        self.play(Create(underline), run_time=0.3)
        self.play(Write(claim), run_time=0.9)

        question = Tex(r"\textquestiondown por qu\'e siempre un cuadrado?",
                       font_size=30, color=GREY_A)
        question.set_z_index(20)
        question.move_to(UP * 3.3)
        fit_to_safe_width(question)
        self.play(FadeIn(question, shift=UP * 0.15), run_time=0.5)
        self.wait(0.5)

        # ------------------------------------------------- beat 1: the one cell
        self.play(FadeOut(question), run_time=0.3)

        first = gnomon(1, GNOMON_COLORS[0])
        one_label = MathTex(r"1", font_size=34, color=BG)
        one_label.set_z_index(6)
        one_label.move_to(first[0].get_center())

        self.play(FadeIn(first, scale=0.5), run_time=0.6)
        self.play(Write(one_label), run_time=0.4)

        start_text = Tex(r"empezamos con 1 celda:\\un cuadrado $1\times 1$",
                         font_size=30, color=WHITE)
        start_text.set_z_index(20)
        start_text.move_to(DOWN * 4.5)
        fit_to_safe_width(start_text)
        self.play(FadeIn(start_text, shift=UP * 0.15), run_time=0.5)
        self.wait(0.6)
        self.play(FadeOut(start_text), FadeOut(one_label), run_time=0.4)

        # The running equation grows term by term underneath the square, so the
        # arithmetic and the picture advance in lockstep.
        running = MathTex(r"1", r"=", r"1^{2}", font_size=40)
        running[0].set_color(GNOMON_COLORS[0])
        running[2].set_color(ACCENT_YELLOW)
        running.set_stroke(width=1)
        running.set_z_index(20)
        running.move_to(DOWN * 3.9)
        self.play(Write(running), run_time=0.6)
        self.wait(0.4)

        # ------------------------------------- beat 2: each odd number is an L
        layers = VGroup(first)
        # Explanatory caption shown only on the first two growth steps; after
        # that the pattern speaks for itself and the captions would slow it down.
        captions = {
            2: r"le a\~nadimos una L de 3\\y queda un $2\times 2$",
            3: r"una L de 5 y queda $3\times 3$",
        }
        caption = None

        for step in range(2, N_STEPS + 1):
            odd = 2 * step - 1
            color = GNOMON_COLORS[(step - 1) % len(GNOMON_COLORS)]
            layer = gnomon(step, color)

            # The L appears cell by cell so the viewer can count it, then the
            # completed square is named. Lag shrinks as the L grows to keep the
            # per-step duration roughly constant.
            self.play(
                LaggedStart(
                    *[FadeIn(c, scale=0.6) for c in layer],
                    lag_ratio=0.9 / odd,
                ),
                run_time=0.75 + 0.05 * step,
            )
            layers.add(layer)

            new_running = MathTex(
                *[t for k in range(1, step + 1) for t in (str(2 * k - 1), "+")][:-1],
                "=", f"{step}^{{2}}",
                font_size=40,
            )
            for k in range(step):
                new_running[2 * k].set_color(
                    GNOMON_COLORS[k % len(GNOMON_COLORS)]
                )
            new_running[-1].set_color(ACCENT_YELLOW)
            new_running.set_stroke(width=1)
            new_running.set_z_index(20)
            new_running.move_to(DOWN * 3.9)
            fit_to_safe_width(new_running)

            anims = [ReplacementTransform(running, new_running)]

            if step in captions:
                new_caption = Tex(captions[step], font_size=30, color=GREY_A)
                new_caption.set_z_index(20)
                new_caption.move_to(DOWN * 4.75)
                fit_to_safe_width(new_caption)
                if caption is None:
                    anims.append(FadeIn(new_caption, shift=UP * 0.15))
                else:
                    anims.append(ReplacementTransform(caption, new_caption))
                caption = new_caption
            elif caption is not None:
                anims.append(FadeOut(caption))
                caption = None

            self.play(*anims, run_time=0.65)
            running = new_running
            self.wait(0.25)

        self.wait(0.4)

        # --------------------------------------- beat 3: why the L is 2n - 1
        # The count of the last L is made explicit: one arm, the other arm, and
        # the single corner cell shared between them.
        last = layers[-1]
        k = N_STEPS - 1
        column_arm = VGroup(*last[: k + 1])
        row_arm = VGroup(*last[k + 1:])

        arm_text = MathTex(
            r"\underbrace{" + str(k) + r"}_{\text{columna}}+"
            r"\underbrace{" + str(k) + r"}_{\text{fila}}+"
            r"\underbrace{1}_{\text{esquina}}=" + str(2 * N_STEPS - 1),
            font_size=34, color=WHITE,
        )
        arm_text.set_stroke(width=1)
        arm_text.set_z_index(20)
        arm_text.move_to(DOWN * 4.85)
        fit_to_safe_width(arm_text)

        self.play(
            column_arm.animate.set_fill(opacity=1.0).set_stroke(color=WHITE, width=2.5),
            row_arm.animate.set_fill(opacity=0.45),
            run_time=0.5,
        )
        self.play(
            column_arm.animate.set_fill(opacity=0.45).set_stroke(color=BG, width=2.5),
            row_arm.animate.set_fill(opacity=1.0).set_stroke(color=WHITE, width=2.5),
            run_time=0.5,
        )
        self.play(
            last.animate.set_fill(opacity=0.9).set_stroke(color=BG, width=2.5),
            FadeIn(arm_text, shift=UP * 0.15),
            run_time=0.6,
        )
        self.wait(1.1)

        # ------------------------------------------------------------ conclusion
        # The square is the answer: n L layers stacked are an n x n board.
        self.play(FadeOut(arm_text), run_time=0.35)

        board = Square(side_length=N_STEPS * CELL)
        board.move_to(GRID_ORIGIN + np.array([N_STEPS * CELL / 2, N_STEPS * CELL / 2, 0.0]))
        board.set_stroke(color=ACCENT_YELLOW, width=6)
        board.set_fill(opacity=0)
        board.set_z_index(8)

        side_label = MathTex(r"n", font_size=36, color=ACCENT_YELLOW)
        side_label.set_z_index(20)
        side_label.next_to(board, DOWN, buff=0.22)

        self.play(Create(board), run_time=0.8)
        self.play(Write(side_label), run_time=0.4)

        payoff = Tex(
            r"$n$ eles apiladas\\son un cuadrado $n\times n$",
            font_size=32, color=WHITE,
        )
        payoff.set_z_index(20)
        payoff.move_to(DOWN * 4.9)
        fit_to_safe_width(payoff)
        self.play(FadeIn(payoff, shift=UP * 0.15), run_time=0.6)
        self.wait(1.0)

        result_box = SurroundingRectangle(running, buff=0.28, corner_radius=0.14)
        result_box.set_stroke(width=4, color=GRADIENT_HIGHLIGHT)
        result_box.set_z_index(20)
        self.play(Create(result_box), run_time=0.7)
        self.wait(1.6)

        animate_End(scene=self)
