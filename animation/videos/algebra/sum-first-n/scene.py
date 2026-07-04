from manim import *
from lnx import *

# proof-without-words | algebra | basic
# 1 + 2 + 3 + ... + n = n(n+1)/2
#
# The staircase of triangular numbers is built with unit blocks: column i has
# i+1 blocks. A second identical staircase, turned 180 degrees and pushed one
# row up, interlocks with the first and completes an exact n x (n+1) rectangle.
# Two staircases = one rectangle, so one staircase = half of it.
#
# Column i of the original occupies rows 0..i. Rotating the whole staircase by
# PI about its bounding-box center maps column i -> column n-1-i and row r ->
# row n-1-r, so column j of the copy lands on rows j..n-1. Shifting it up by a
# single row leaves it on rows j+1..n, which is precisely the complement of the
# original inside a grid of n columns and n+1 rows.
#
# Vertical 9:16 frame. Safe area: x in [-3.8, 3.8], y in [-5.6, 5.6].

N = 6                     # number of steps
CELL = 0.55               # side of one unit block
GRID_W = N * CELL         # 3.30
GRID_H = (N + 1) * CELL   # 3.85

# Bottom-left corner of the final rectangle, chosen so the rectangle sits
# slightly below the frame center and leaves room for the header equation.
BASE = np.array([-GRID_W / 2, -0.30 - GRID_H / 2, 0.0])


def cell_center(col, row):
    """Center of the block at grid position (col, row), row 0 at the bottom."""
    return BASE + np.array([(col + 0.5) * CELL, (row + 0.5) * CELL, 0.0])


def make_block(col, row, color):
    block = Square(side_length=CELL)
    block.set_stroke(color=color, width=3)
    block.set_fill(color=color, opacity=0.42)
    block.move_to(cell_center(col, row))
    block.set_z_index(2)
    return block


def make_staircase(color):
    """Column i holds i+1 blocks; returns a VGroup of per-column VGroups."""
    columns = VGroup()
    for col in range(N):
        column = VGroup(*[make_block(col, row, color) for row in range(col + 1)])
        columns.add(column)
    return columns


class SumFirstN(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        FIRST_COLOR = ACCENT_CYAN      # the original staircase
        SECOND_COLOR = ACCENT_MAGENTA  # the rotated copy
        RESULT_COLOR = ACCENT_YELLOW   # the rectangle and the final formula

        # ----------------------------------------------------------- hook 0-2s
        # The staircase pops up column by column before a single word is said.
        title = MathTex(
            r"1+2+3+\cdots+n", font_size=52, color=WHITE,
        )
        title.set_stroke(width=1)
        title.set_z_index(20)
        title.move_to(UP * 5.05)

        stair = make_staircase(FIRST_COLOR)
        self.play(Write(title), run_time=0.5)
        self.play(
            LaggedStart(
                *[FadeIn(column, shift=UP * 0.25) for column in stair],
                lag_ratio=0.16,
            ),
            run_time=1.4,
        )

        question = MathTex(r"=\;?", font_size=52, color=RESULT_COLOR)
        question.set_stroke(width=1)
        question.set_z_index(20)
        question.next_to(title, DOWN, buff=0.32)
        self.play(Write(question), run_time=0.5)
        self.wait(0.5)

        # ------------------------------------------------- beat 1: count blocks
        # Naming n = 6 anchors the picture: the pile really is 1+2+...+6.
        counted = MathTex(
            r"1+2+3+4+5+6", font_size=34, color=FIRST_COLOR,
        )
        counted.set_stroke(width=1)
        counted.set_z_index(20)
        counted.move_to(DOWN * 3.05)

        base_brace = Brace(stair, DOWN, buff=0.18, color=GREY_B)
        base_brace.set_z_index(6)
        base_label = MathTex(r"n=6", font_size=32, color=GREY_A)
        base_label.set_z_index(20)
        base_label.next_to(base_brace, DOWN, buff=0.14)

        self.play(GrowFromCenter(base_brace), FadeIn(base_label), run_time=0.6)
        self.play(FadeIn(counted, shift=UP * 0.15), run_time=0.6)
        self.wait(0.9)

        self.play(
            FadeOut(base_brace), FadeOut(base_label), FadeOut(counted),
            run_time=0.4,
        )

        # ------------------------------------------ beat 2: duplicate the stair
        # The copy is born on top of the original and slides aside, so the
        # viewer sees that both piles are the same object.
        copy_stair = make_staircase(SECOND_COLOR)
        copy_hint = Tex(r"toma otra escalera igual", font_size=32, color=SECOND_COLOR)
        copy_hint.set_z_index(20)
        copy_hint.move_to(DOWN * 3.35)

        self.add(copy_stair)
        self.play(
            copy_stair.animate.shift(RIGHT * (GRID_W + 0.55)),
            stair.animate.shift(LEFT * (GRID_W + 0.55) / 2),
            run_time=0.9,
        )
        # Keep both piles inside the safe area while they are side by side.
        self.play(copy_stair.animate.shift(LEFT * (GRID_W + 0.55) / 2), run_time=0.01)
        self.play(FadeIn(copy_hint, shift=UP * 0.15), run_time=0.5)
        self.wait(0.8)

        # --------------------------------- beat 3: the turn and the interlock
        # This is the moment of the video: rotate 180 degrees and slot it in.
        turn_hint = Tex(r"g\'irala $180^\circ$", font_size=32, color=SECOND_COLOR)
        turn_hint.set_z_index(20)
        turn_hint.move_to(DOWN * 3.35)
        self.play(ReplacementTransform(copy_hint, turn_hint), run_time=0.4)

        self.play(
            Rotate(copy_stair, angle=PI, about_point=copy_stair.get_center()),
            run_time=1.2,
        )
        self.wait(0.4)

        fit_hint = Tex(r"y enc\'ajala", font_size=32, color=RESULT_COLOR)
        fit_hint.set_z_index(20)
        fit_hint.move_to(DOWN * 3.35)
        self.play(ReplacementTransform(turn_hint, fit_hint), run_time=0.4)

        # Final resting places: the original returns to the grid, the rotated
        # copy lands one row above its own rotated position.
        target_stair = make_staircase(FIRST_COLOR)
        target_copy = make_staircase(SECOND_COLOR)
        target_copy.rotate(PI, about_point=target_copy.get_center())
        target_copy.shift(UP * CELL)

        self.play(
            Transform(stair, target_stair),
            Transform(copy_stair, target_copy),
            run_time=1.6,
        )
        self.wait(0.6)

        # ------------------------------------------ beat 4: it is a rectangle
        rectangle = Rectangle(width=GRID_W, height=GRID_H)
        rectangle.set_stroke(color=RESULT_COLOR, width=6)
        rectangle.move_to(BASE + np.array([GRID_W / 2, GRID_H / 2, 0.0]))
        rectangle.set_z_index(8)

        width_brace = Brace(rectangle, DOWN, buff=0.16, color=GREY_B)
        width_brace.set_z_index(6)
        width_label = MathTex(r"n", font_size=34, color=WHITE)
        width_label.set_z_index(20)
        width_label.next_to(width_brace, DOWN, buff=0.12)

        height_brace = Brace(rectangle, RIGHT, buff=0.16, color=GREY_B)
        height_brace.set_z_index(6)
        height_label = MathTex(r"n+1", font_size=34, color=WHITE)
        height_label.set_z_index(20)
        height_label.next_to(height_brace, RIGHT, buff=0.12)

        self.play(FadeOut(fit_hint), Create(rectangle), run_time=0.7)
        self.play(
            GrowFromCenter(width_brace), FadeIn(width_label),
            GrowFromCenter(height_brace), FadeIn(height_label),
            run_time=0.7,
        )

        area_tex = MathTex(r"n\,(n+1)", font_size=40, color=RESULT_COLOR)
        area_tex.set_stroke(width=1)
        area_tex.set_z_index(20)
        area_tex.move_to(DOWN * 3.35)
        self.play(Write(area_tex), run_time=0.7)
        self.wait(0.9)

        # ------------------------------------------- beat 5: halve and conclude
        # Two staircases filled the rectangle, so one staircase is half of it.
        two_stairs = MathTex(
            r"2\cdot(1+2+\cdots+n)", r"=", r"n\,(n+1)",
            font_size=36,
        )
        two_stairs[0].set_color(FIRST_COLOR)
        two_stairs[2].set_color(RESULT_COLOR)
        two_stairs.set_stroke(width=1)
        two_stairs.set_z_index(20)
        two_stairs.move_to(DOWN * 3.35)

        self.play(
            FadeOut(width_brace), FadeOut(width_label),
            FadeOut(height_brace), FadeOut(height_label),
            ReplacementTransform(area_tex, two_stairs),
            run_time=0.9,
        )
        self.wait(0.9)

        # The magenta half fades away: what is left is exactly one staircase.
        self.play(copy_stair.animate.set_opacity(0.16), run_time=0.8)
        self.wait(0.5)

        result = MathTex(
            r"1+2+3+\cdots+n", r"=", r"\frac{n\,(n+1)}{2}",
            font_size=42,
        )
        result[0].set_color(FIRST_COLOR)
        result[2].set_color(RESULT_COLOR)
        result.set_stroke(width=1)
        result.set_z_index(21)
        result.move_to(DOWN * 3.45)

        self.play(
            FadeOut(title), FadeOut(question),
            ReplacementTransform(two_stairs, result),
            run_time=1.0,
        )

        result_box = SurroundingRectangle(result, buff=0.26, corner_radius=0.14)
        result_box.set_stroke(width=4, color=GRADIENT_HIGHLIGHT)
        result_box.set_z_index(20)
        self.play(Create(result_box), run_time=0.6)
        self.wait(1.6)

        animate_End(scene=self)
