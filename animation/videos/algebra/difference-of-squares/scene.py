from manim import *
from lnx import *

# proof-without-words | algebra | basic
# a^2 - b^2 = (a+b)(a-b), proved by cut and paste.
#
# Start from a square of side a and remove a square of side b from one corner.
# The remaining area is literally a^2 - b^2, and its shape is an L.
#
# Cut the L with a single straight cut into two rectangles:
#   R1 (bottom)  a       x (a-b)
#   R2 (top)     (a-b)   x b
# Rotate R2 a quarter turn and glue it to the right edge of R1. Nothing is
# added and nothing is lost, so the area is still a^2 - b^2, but now the
# figure is a plain rectangle of sides (a+b) and (a-b). That is the identity,
# with no algebra at all.
#
# Payoff: mental arithmetic. 53^2 - 47^2 = (53+47)(53-47) = 100 * 6 = 600.
#
# Frame is 9 x 16 units. Safe area: |x| <= 3.8, |y| <= 5.6.

SAFE_WIDTH = 7.2

# Side lengths in scene units. a + b = 4.1 keeps the final rectangle inside
# the safe width with room left for the length labels.
A_LEN = 3.0
B_LEN = 1.1
DIFF = A_LEN - B_LEN          # a - b = 1.9
SUM_LEN = A_LEN + B_LEN       # a + b = 4.1

# Vertical center of the working area: the figure sits above the formula band.
FIG_Y = 0.9

LABEL_GAP = 0.34              # distance from an edge to its length label


def fit_to_safe_width(mobject):
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def piece(width, height, center, color, opacity=0.38):
    """Filled rectangle used as a physical piece of paper."""
    rect = Rectangle(
        width=width, height=height,
        stroke_color=color, stroke_width=5,
        fill_color=color, fill_opacity=opacity,
    )
    rect.move_to(center)
    rect.set_z_index(2)
    return rect


def length_label(tex, color, font_size=32):
    """Length label, always placed outside the figure by the caller."""
    label = MathTex(tex, font_size=font_size, color=color)
    label.set_stroke(width=1)
    label.set_z_index(20)
    return label


class DifferenceOfSquares(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        BIG_COLOR = ACCENT_CYAN       # the square of side a
        HOLE_COLOR = ACCENT_MAGENTA   # the square of side b that is removed
        PIECE_COLOR = ACCENT_PURPLE   # the piece that travels
        RESULT_COLOR = ACCENT_YELLOW  # the final rectangle and the identity

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.14
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.85)
        self.add(watermark)

        # ------------------------------------------------------------ hook 0-2s
        # The square appears already built and the corner is bitten off right
        # away: the viewer sees the missing area before hearing any word.
        big_center = np.array([0.0, FIG_Y, 0.0])
        big_square = piece(A_LEN, A_LEN, big_center, BIG_COLOR, 0.32)

        big_corner_ur = big_center + np.array([A_LEN / 2, A_LEN / 2, 0.0])
        hole_center = big_corner_ur + np.array([-B_LEN / 2, -B_LEN / 2, 0.0])
        hole = piece(B_LEN, B_LEN, hole_center, HOLE_COLOR, 0.55)

        area_big = length_label(r"a^2", BIG_COLOR, 44).move_to(
            big_center + np.array([-0.55, -0.45, 0.0])
        )
        area_hole = length_label(r"b^2", HOLE_COLOR, 30).move_to(hole_center)

        self.play(FadeIn(big_square, scale=0.85), run_time=0.5)
        self.play(Write(area_big), run_time=0.4)
        self.play(FadeIn(hole, scale=0.6), Write(area_hole), run_time=0.6)

        title = MathTex(r"a^2 - b^2", font_size=64, color=WHITE)
        title.set_stroke(width=1)
        title.set_z_index(20)
        title.move_to(UP * 5.0)
        fit_to_safe_width(title)
        self.play(Write(title), run_time=0.6)
        self.wait(0.4)

        # --------------------------------------------- beat 1: the L is what is left
        # Removing the small square leaves an L. Its area is a^2 - b^2 by
        # construction, so from here on nothing may be added or thrown away.
        question = Tex(r"quitamos el cuadrado peque\~no", font_size=32, color=GREY_A)
        question.set_z_index(20)
        question.move_to(DOWN * 4.0)
        fit_to_safe_width(question)

        # The L is one polygon so it can be cut cleanly afterwards.
        x0 = big_center[0] - A_LEN / 2
        x1 = big_center[0] + A_LEN / 2
        y0 = big_center[1] - A_LEN / 2
        y1 = big_center[1] + A_LEN / 2
        ell = Polygon(
            np.array([x0, y0, 0.0]),
            np.array([x1, y0, 0.0]),
            np.array([x1, y1 - B_LEN, 0.0]),
            np.array([x1 - B_LEN, y1 - B_LEN, 0.0]),
            np.array([x1 - B_LEN, y1, 0.0]),
            np.array([x0, y1, 0.0]),
            stroke_color=BIG_COLOR, stroke_width=5,
            fill_color=BIG_COLOR, fill_opacity=0.32,
        )
        ell.set_z_index(2)

        self.play(FadeIn(question, shift=UP * 0.15), run_time=0.4)
        self.play(
            FadeOut(hole, scale=0.4), FadeOut(area_hole),
            FadeOut(area_big), FadeOut(big_square),
            FadeIn(ell),
            run_time=0.9,
        )

        # Side labels stay outside the figure, never over an edge.
        label_a_bottom = length_label(r"a", BIG_COLOR).next_to(
            ell, DOWN, buff=LABEL_GAP
        )
        label_a_left = length_label(r"a", BIG_COLOR).next_to(
            ell, LEFT, buff=LABEL_GAP
        )
        label_b_top = length_label(r"b", HOLE_COLOR, 30)
        label_b_top.move_to(np.array([x1 - B_LEN / 2, y1 + LABEL_GAP + 0.05, 0.0]))

        self.play(
            Write(label_a_bottom), Write(label_a_left), Write(label_b_top),
            run_time=0.7,
        )
        self.wait(0.6)

        # ------------------------------------------------- beat 2: one straight cut
        # A single horizontal cut at height a - b splits the L into two
        # rectangles. This is the only cut in the whole proof.
        cut_y = y1 - B_LEN
        cut_line = DashedLine(
            np.array([x0 - 0.25, cut_y, 0.0]),
            np.array([x1 + 0.25, cut_y, 0.0]),
            color=RESULT_COLOR, stroke_width=5,
        )
        cut_line.set_z_index(10)

        cut_text = Tex(r"un solo corte", font_size=32, color=RESULT_COLOR)
        cut_text.set_z_index(20)
        cut_text.move_to(DOWN * 4.0)
        fit_to_safe_width(cut_text)

        self.play(FadeOut(question), run_time=0.25)
        self.play(Create(cut_line), FadeIn(cut_text, shift=UP * 0.15), run_time=0.7)

        # bottom_piece: a x (a-b).  top_piece: (a-b) x b.
        bottom_center = np.array([big_center[0], (y0 + cut_y) / 2, 0.0])
        bottom_piece = piece(A_LEN, DIFF, bottom_center, BIG_COLOR, 0.32)
        top_center = np.array([x0 + DIFF / 2, (cut_y + y1) / 2, 0.0])
        top_piece = piece(DIFF, B_LEN, top_center, PIECE_COLOR, 0.45)

        self.play(
            FadeOut(ell), FadeIn(bottom_piece), FadeIn(top_piece),
            run_time=0.7,
        )
        self.play(
            top_piece.animate.shift(UP * 0.28),
            FadeOut(cut_line),
            run_time=0.5,
        )
        self.wait(0.4)

        # ------------------------------------ beat 3: rotate and glue, nothing lost
        # The final rectangle is (a+b) wide and (a-b) tall, centered on FIG_Y.
        final_center = np.array([0.0, FIG_Y - 0.2, 0.0])
        final_left = final_center[0] - SUM_LEN / 2
        bottom_target = np.array([final_left + A_LEN / 2, final_center[1], 0.0])
        top_target = np.array([final_left + A_LEN + B_LEN / 2, final_center[1], 0.0])

        move_text = Tex(r"giramos la pieza y la pegamos", font_size=32, color=GREY_A)
        move_text.set_z_index(20)
        move_text.move_to(DOWN * 4.0)
        fit_to_safe_width(move_text)

        self.play(
            FadeOut(cut_text),
            FadeOut(label_a_bottom), FadeOut(label_a_left), FadeOut(label_b_top),
            FadeIn(move_text, shift=UP * 0.15),
            run_time=0.5,
        )
        # The travelling piece keeps its size: a quarter turn turns the side of
        # length (a-b) into the height of the final rectangle.
        self.play(
            top_piece.animate.rotate(-PI / 2).move_to(top_target),
            bottom_piece.animate.move_to(bottom_target),
            run_time=1.8,
        )
        self.wait(0.5)

        # ----------------------------------------------- beat 4: read the rectangle
        rect_group = VGroup(bottom_piece, top_piece)
        outline = Rectangle(
            width=SUM_LEN, height=DIFF,
            stroke_color=RESULT_COLOR, stroke_width=7,
        )
        outline.move_to(final_center)
        outline.set_z_index(8)

        label_sum = length_label(r"a+b", RESULT_COLOR, 36)
        label_sum.next_to(outline, DOWN, buff=LABEL_GAP)
        label_diff = length_label(r"a-b", RESULT_COLOR, 36)
        label_diff.next_to(outline, RIGHT, buff=LABEL_GAP)

        self.play(Create(outline), run_time=0.7)
        self.play(Write(label_sum), Write(label_diff), run_time=0.7)
        self.wait(0.5)

        identity = MathTex(
            r"a^2 - b^2", r"=", r"(a+b)(a-b)",
            font_size=46,
        )
        identity[0].set_color(BIG_COLOR)
        identity[2].set_color(RESULT_COLOR)
        identity.set_stroke(width=1)
        identity.set_z_index(20)
        identity.move_to(DOWN * 2.6)
        fit_to_safe_width(identity)

        self.play(FadeOut(move_text), run_time=0.25)
        self.play(FadeOut(title), Write(identity), run_time=1.0)
        self.wait(1.0)

        # ------------------------------------------- beat 5: mental arithmetic payoff
        # The identity turns a two square subtraction into a one line product.
        self.play(
            FadeOut(rect_group), FadeOut(outline),
            FadeOut(label_sum), FadeOut(label_diff),
            identity.animate.move_to(UP * 4.6),
            run_time=0.9,
        )

        challenge = MathTex(r"53^2 - 47^2 = \; ?", font_size=52, color=WHITE)
        challenge.set_stroke(width=1)
        challenge.set_z_index(20)
        challenge.move_to(UP * 1.9)
        fit_to_safe_width(challenge)
        self.play(Write(challenge), run_time=0.8)
        self.wait(0.6)

        steps = VGroup(
            MathTex(r"(53+47)\,(53-47)", font_size=44, color=ACCENT_CYAN),
            MathTex(r"100 \times 6", font_size=48, color=ACCENT_PURPLE),
            MathTex(r"600", font_size=64, color=RESULT_COLOR),
        )
        steps.arrange(DOWN, buff=0.7)
        steps.set_stroke(width=1)
        steps.set_z_index(20)
        steps.move_to(DOWN * 1.3)
        fit_to_safe_width(steps)

        self.play(FadeIn(steps[0], shift=UP * 0.2), run_time=0.7)
        self.play(FadeIn(steps[1], shift=UP * 0.2), run_time=0.7)
        self.play(Write(steps[2]), run_time=0.8)

        result_box = SurroundingRectangle(steps[2], buff=0.28, corner_radius=0.14)
        result_box.set_stroke(width=4, color=[ACCENT_YELLOW, ACCENT_MAGENTA])
        result_box.set_z_index(20)
        self.play(Create(result_box), run_time=0.6)

        closing = Tex(r"sin calculadora", font_size=34, color=GREY_A)
        closing.set_z_index(20)
        closing.next_to(result_box, DOWN, buff=0.5)
        fit_to_safe_width(closing)
        self.play(FadeIn(closing, shift=UP * 0.15), run_time=0.5)
        self.wait(1.6)

        animate_End(scene=self)
