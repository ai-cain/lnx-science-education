from manim import *
from lnx import *

# your-teacher-lied | algebra | basic
# (a+b)^2 = a^2 + 2ab + b^2
#
# The most common algebra mistake is writing (a+b)^2 = a^2 + b^2. The visual
# reason it fails: a square of side (a+b) splits into FOUR pieces, not two.
# The a^2 and b^2 squares sit on the diagonal, and the two ab rectangles are
# exactly the term everybody forgets. Highlighting those two rectangles in the
# accent color IS the explanation; the algebra only names what is already seen.
#
# The real frame is 9 x 16 units (x in [-4.5, 4.5], y in [-8, 8]).
# Safe area: |x| <= 3.8 and |y| <= 5.6.

SAFE_WIDTH = 7.2

# Side lengths in scene units. a + b = 3.7 keeps the whole square inside
# x in [-1.85, 1.85], well within the safe area, with room for outside labels.
A_LEN = 2.3
B_LEN = 1.4
SIDE = A_LEN + B_LEN

# Bottom-left corner of the big square. The square is pushed slightly below
# center so the header formula and the closing line both get their own air.
ORIGIN_CORNER = np.array([-SIDE / 2.0, -SIDE / 2.0 - 0.55, 0.0])


def fit_to_safe_width(mobject):
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def P(x, y):
    """Square-local coordinate (0..SIDE) -> scene point."""
    return ORIGIN_CORNER + np.array([x, y, 0.0])


class BinomialSquare(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        A_COLOR = ACCENT_CYAN        # the a^2 square
        B_COLOR = ACCENT_PURPLE      # the b^2 square
        AB_COLOR = ACCENT_YELLOW     # the two forgotten ab rectangles
        WRONG_COLOR = ACCENT_MAGENTA # the mistake being corrected

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.14
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.85)
        self.add(watermark)

        def piece(x0, y0, width, height, color, opacity=0.35):
            rect = Rectangle(width=width, height=height)
            rect.set_stroke(color=color, width=5)
            rect.set_fill(color=color, opacity=opacity)
            rect.move_to(P(x0 + width / 2.0, y0 + height / 2.0))
            rect.set_z_index(2)
            return rect

        def label(tex, font_size, color):
            mob = MathTex(tex, font_size=font_size, color=color)
            mob.set_stroke(width=1)
            mob.set_z_index(15)
            return mob

        # -------------------------------------------------------- hook 0.0-2.0s
        # The mistake is on screen immediately, then it gets crossed out.
        wrong = MathTex(r"(a+b)^2", r"=", r"a^2+b^2", font_size=58)
        wrong[0].set_color(WHITE)
        wrong[2].set_color(WRONG_COLOR)
        wrong.set_stroke(width=1)
        wrong.set_z_index(20)
        wrong.move_to(UP * 2.0)
        fit_to_safe_width(wrong)

        self.play(Write(wrong), run_time=0.8)

        cross = Cross(wrong[2], stroke_color=WRONG_COLOR, stroke_width=8)
        cross.set_z_index(21)
        self.play(Create(cross), run_time=0.5)

        hook_line = Tex(
            r"el error m\'as com\'un del \'algebra.\\Mira POR QU\'E est\'a mal.",
            font_size=36, color=GREY_A,
        )
        hook_line.set_z_index(20)
        hook_line.move_to(DOWN * 1.2)
        fit_to_safe_width(hook_line)
        self.play(FadeIn(hook_line, shift=UP * 0.2), run_time=0.6)
        self.wait(0.9)

        # ------------------------------------- beat 1: the square of side a+b
        self.play(FadeOut(hook_line), FadeOut(cross), run_time=0.4)
        self.play(
            wrong.animate.scale(0.62).move_to(UP * 4.9),
            run_time=0.7,
        )
        crossed = Cross(wrong[2], stroke_color=WRONG_COLOR, stroke_width=5)
        crossed.set_z_index(21)
        self.add(crossed)

        big_square = Rectangle(width=SIDE, height=SIDE)
        big_square.set_stroke(color=GREY_A, width=6)
        big_square.set_fill(color=SURFACE, opacity=0.5)
        big_square.move_to(P(SIDE / 2.0, SIDE / 2.0))
        big_square.set_z_index(1)

        self.play(Create(big_square), run_time=1.0)

        # Side labels live OUTSIDE the figure: the bottom edge splits into a
        # and b, so the total side (a+b) is readable before any cut is drawn.
        bottom_a = Line(P(0, 0), P(A_LEN, 0), stroke_width=8, color=A_COLOR)
        bottom_b = Line(P(A_LEN, 0), P(SIDE, 0), stroke_width=8, color=B_COLOR)
        for edge in (bottom_a, bottom_b):
            edge.set_z_index(6)

        a_bottom = label("a", 40, A_COLOR).next_to(bottom_a, DOWN, buff=0.28)
        b_bottom = label("b", 40, B_COLOR).next_to(bottom_b, DOWN, buff=0.28)

        left_a = Line(P(0, 0), P(0, A_LEN), stroke_width=8, color=A_COLOR)
        left_b = Line(P(0, A_LEN), P(0, SIDE), stroke_width=8, color=B_COLOR)
        for edge in (left_a, left_b):
            edge.set_z_index(6)

        a_left = label("a", 40, A_COLOR).next_to(left_a, LEFT, buff=0.28)
        b_left = label("b", 40, B_COLOR).next_to(left_b, LEFT, buff=0.28)

        self.play(
            Create(bottom_a), Create(bottom_b),
            Create(left_a), Create(left_b),
            run_time=0.8,
        )
        self.play(
            Write(a_bottom), Write(b_bottom),
            Write(a_left), Write(b_left),
            run_time=0.7,
        )

        side_note = Tex(
            r"un cuadrado de lado $a+b$",
            font_size=34, color=WHITE,
        )
        side_note.set_z_index(20)
        side_note.move_to(DOWN * 4.5)
        fit_to_safe_width(side_note)
        self.play(FadeIn(side_note, shift=UP * 0.15), run_time=0.5)
        self.wait(0.8)

        # ------------------------------------- beat 2: the two obvious pieces
        # a^2 and b^2 appear first, because those are the only two terms the
        # wrong answer keeps.
        cut_v = Line(P(A_LEN, 0), P(A_LEN, SIDE), stroke_width=4, color=GREY_A)
        cut_h = Line(P(0, A_LEN), P(SIDE, A_LEN), stroke_width=4, color=GREY_A)
        for cut in (cut_v, cut_h):
            cut.set_z_index(7)

        self.play(
            FadeOut(side_note),
            Create(cut_v), Create(cut_h),
            run_time=0.8,
        )

        sq_a = piece(0, 0, A_LEN, A_LEN, A_COLOR, 0.45)
        sq_b = piece(A_LEN, A_LEN, B_LEN, B_LEN, B_COLOR, 0.45)
        lbl_a2 = label("a^2", 40, A_COLOR).move_to(sq_a.get_center())
        lbl_b2 = label("b^2", 32, B_COLOR).move_to(sq_b.get_center())

        self.play(FadeIn(sq_a), FadeIn(sq_b), run_time=0.7)
        self.play(Write(lbl_a2), Write(lbl_b2), run_time=0.6)

        two_note = Tex(
            r"estos dos s\'i los recuerdan todos",
            font_size=32, color=GREY_A,
        )
        two_note.set_z_index(20)
        two_note.move_to(DOWN * 4.5)
        fit_to_safe_width(two_note)
        self.play(FadeIn(two_note, shift=UP * 0.15), run_time=0.5)
        self.wait(1.0)

        # ------------------------------- beat 3: the two forgotten rectangles
        rect_1 = piece(A_LEN, 0, B_LEN, A_LEN, AB_COLOR, 0.55)
        rect_2 = piece(0, A_LEN, A_LEN, B_LEN, AB_COLOR, 0.55)
        lbl_ab1 = label("ab", 32, AB_COLOR).move_to(rect_1.get_center())
        lbl_ab2 = label("ab", 32, AB_COLOR).move_to(rect_2.get_center())

        missing_note = Tex(
            r"\ldots pero falta ESTO",
            font_size=38, color=AB_COLOR,
        )
        missing_note.set_z_index(20)
        missing_note.move_to(DOWN * 4.5)
        fit_to_safe_width(missing_note)

        self.play(FadeOut(two_note), run_time=0.3)
        self.play(
            FadeIn(rect_1, scale=0.8), FadeIn(rect_2, scale=0.8),
            run_time=0.8,
        )
        self.play(Write(lbl_ab1), Write(lbl_ab2), run_time=0.6)
        self.play(FadeIn(missing_note, shift=UP * 0.15), run_time=0.5)

        # Flash the two forgotten pieces so the eye lands exactly on them.
        self.play(
            Indicate(rect_1, color=AB_COLOR, scale_factor=1.06),
            Indicate(rect_2, color=AB_COLOR, scale_factor=1.06),
            run_time=0.9,
        )
        self.wait(0.6)

        two_ab = Tex(
            r"dos rect\'angulos de \'area $ab$",
            font_size=34, color=AB_COLOR,
        )
        two_ab.set_z_index(20)
        two_ab.move_to(DOWN * 4.5)
        fit_to_safe_width(two_ab)
        self.play(ReplacementTransform(missing_note, two_ab), run_time=0.7)
        self.wait(0.9)

        # ------------------------------------------- beat 4: the correct sum
        # The wrong header is replaced, never stacked over.
        right = MathTex(
            r"(a+b)^2", r"=", r"a^2", r"+", r"2ab", r"+", r"b^2",
            font_size=44,
        )
        right[0].set_color(WHITE)
        right[2].set_color(A_COLOR)
        right[4].set_color(AB_COLOR)
        right[6].set_color(B_COLOR)
        right.set_stroke(width=1)
        right.set_z_index(20)
        right.move_to(UP * 4.9)
        fit_to_safe_width(right)

        self.play(
            FadeOut(crossed), FadeOut(two_ab),
            ReplacementTransform(wrong, right),
            run_time=1.0,
        )
        self.play(
            Indicate(right[4], color=AB_COLOR, scale_factor=1.18),
            run_time=0.8,
        )
        self.wait(0.7)

        # ------------------------------------------------------- payoff frame
        closing = Tex(
            r"el $2ab$ es el \'area\\que te est\'as olvidando",
            font_size=36, color=WHITE,
        )
        closing.set_z_index(21)
        closing.move_to(DOWN * 4.45)
        fit_to_safe_width(closing)

        closing_box = SurroundingRectangle(closing, buff=0.28, corner_radius=0.14)
        closing_box.set_stroke(width=4, color=[ACCENT_YELLOW, ACCENT_CYAN])
        closing_box.set_z_index(20)

        self.play(FadeIn(closing, shift=UP * 0.15), run_time=0.7)
        self.play(Create(closing_box), run_time=0.7)
        self.wait(1.6)

        animate_End(scene=self)
