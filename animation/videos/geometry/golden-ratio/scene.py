from manim import *
from lnx import *

# proof-without-words | geometry | basic
#
# The golden rectangle is the only rectangle that stays similar to itself
# after removing the largest possible square. That single property yields
# 1/phi = phi - 1, equivalently phi^2 = phi + 1, with phi = (1+sqrt(5))/2.

PHI = (1.0 + np.sqrt(5.0)) / 2.0

UNIT = 2.55
BASE_LEFT = -2.05
BASE_BOTTOM = -1.55

SAFE_WIDTH = 7.2


def fit_to_safe_width(mobject):
    """Keep a header inside the horizontal safe area."""
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def make_rectangle(x, y, width, height, **kwargs):
    """Build a rectangle from its bottom-left corner."""
    rectangle = Rectangle(width=width, height=height, **kwargs)
    rectangle.move_to(np.array([x + width / 2.0, y + height / 2.0, 0.0]))
    return rectangle


def cut_square(x, y, width, height):
    """Remove the largest square and return (square_box, remaining_box).

    Boxes are (x, y, width, height) with (x, y) at the bottom-left corner.
    The square is taken from the side that keeps the leftover attached to
    the opposite edge, so successive cuts wind around the figure.
    """
    if width >= height:
        square = (x, y, height, height)
        remainder = (x + height, y, width - height, height)
    else:
        square = (x, y + height - width, width, width)
        remainder = (x, y, width, height - width)
    return square, remainder


def similarity_ratio(box):
    """Long side over short side of a box."""
    _, _, width, height = box
    long_side = max(width, height)
    short_side = min(width, height)
    return long_side / short_side


class GoldenRatio(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        base_box = (BASE_LEFT, BASE_BOTTOM, UNIT * PHI, UNIT)

        # The construction is only meaningful if every leftover keeps the
        # same proportion, so verify it before anything is drawn.
        verification_box = base_box
        for _ in range(4):
            assert abs(similarity_ratio(verification_box) - PHI) < 1e-9
            _, verification_box = cut_square(*verification_box)
        assert abs(similarity_ratio(verification_box) - PHI) < 1e-9

        golden_rectangle = make_rectangle(
            *base_box,
            color=ACCENT_CYAN,
            stroke_width=7,
        )
        golden_rectangle.set_fill(ACCENT_CYAN, opacity=0.08)
        golden_rectangle.set_z_index(2)

        # Beat 1 (0.0-2.0): the hook is the rectangle plus the question.
        hook = Tex(
            r"\textbf{¿Y si le quitas un cuadrado?}",
            font_size=44,
            color=WHITE,
        ).move_to(UP * 4.95)
        hook.set_stroke(width=1)
        hook.set_z_index(30)
        fit_to_safe_width(hook)

        self.play(
            Create(golden_rectangle),
            FadeIn(hook, shift=DOWN * 0.15),
            run_time=1.1,
        )

        # Length labels stay outside the figure, never over an edge.
        long_label = MathTex(r"\varphi", font_size=40, color=ACCENT_CYAN)
        long_label.next_to(golden_rectangle, DOWN, buff=0.28)
        long_label.set_z_index(30)
        short_label = MathTex(r"1", font_size=40, color=ACCENT_CYAN)
        short_label.next_to(golden_rectangle, LEFT, buff=0.28)
        short_label.set_z_index(30)

        self.play(
            FadeIn(long_label, shift=UP * 0.1),
            FadeIn(short_label, shift=RIGHT * 0.1),
            run_time=0.8,
        )

        # Beat 2 (2.0-9.0): remove the square and expose the leftover.
        square_box, remainder_box = cut_square(*base_box)
        first_square = make_rectangle(
            *square_box,
            color=ACCENT_YELLOW,
            stroke_width=5,
        )
        first_square.set_fill(ACCENT_YELLOW, opacity=0.24)
        first_square.set_z_index(3)
        right_angle_mark = RightAngle(
            Line(
                np.array([square_box[0], square_box[1], 0.0]),
                np.array([square_box[0] + square_box[2], square_box[1], 0.0]),
            ),
            Line(
                np.array([square_box[0], square_box[1], 0.0]),
                np.array([square_box[0], square_box[1] + square_box[3], 0.0]),
            ),
            length=0.28,
            color=WHITE,
        )
        right_angle_mark.set_z_index(6)

        first_remainder = make_rectangle(
            *remainder_box,
            color=ACCENT_MAGENTA,
            stroke_width=6,
        )
        first_remainder.set_fill(ACCENT_MAGENTA, opacity=0.18)
        first_remainder.set_z_index(4)

        square_note = Tex(
            r"\textbf{Quitamos el cuadrado de lado 1}",
            font_size=34,
            color=ACCENT_YELLOW,
        ).move_to(UP * 4.95)
        square_note.set_stroke(width=1)
        square_note.set_z_index(30)
        fit_to_safe_width(square_note)

        self.play(
            ReplacementTransform(hook, square_note),
            FadeIn(first_square),
            Create(right_angle_mark),
            run_time=1.0,
        )
        self.play(
            Create(first_remainder),
            run_time=0.9,
        )

        similar_note = Tex(
            r"\textbf{Lo que queda es semejante al original}",
            font_size=33,
            color=ACCENT_MAGENTA,
        ).move_to(UP * 4.95)
        similar_note.set_stroke(width=1)
        similar_note.set_z_index(30)
        fit_to_safe_width(similar_note)

        self.play(
            ReplacementTransform(square_note, similar_note),
            first_square.animate.set_fill(ACCENT_YELLOW, opacity=0.10),
            Indicate(first_remainder, color=ACCENT_MAGENTA, scale_factor=1.05),
            run_time=1.4,
        )

        # The leftover short side is phi - 1, labelled outside the figure.
        remainder_label = MathTex(
            r"\varphi-1",
            font_size=34,
            color=ACCENT_MAGENTA,
        )
        remainder_label.next_to(first_remainder, UP, buff=0.26)
        remainder_label.set_z_index(30)
        self.play(FadeIn(remainder_label, shift=DOWN * 0.1), run_time=0.7)
        self.wait(1.2)

        # Beat 3 (9.0-17.0): similarity becomes an equation.
        proportion = MathTex(
            r"\frac{\varphi}{1}",
            r"=",
            r"\frac{1}{\varphi-1}",
            font_size=44,
        ).move_to(UP * 3.55)
        proportion[0].set_color(ACCENT_CYAN)
        proportion[1].set_color(WHITE)
        proportion[2].set_color(ACCENT_MAGENTA)
        proportion.set_stroke(width=1)
        proportion.set_z_index(30)

        self.play(
            FadeOut(similar_note),
            Write(proportion),
            run_time=1.2,
        )
        self.play(
            Circumscribe(proportion, color=ACCENT_YELLOW, buff=0.14),
            run_time=1.3,
        )

        quadratic = MathTex(
            r"\varphi^2=\varphi+1",
            font_size=50,
            color=ACCENT_YELLOW,
        ).move_to(UP * 4.85)
        quadratic.set_stroke(width=1)
        quadratic.set_z_index(30)
        self.play(
            TransformMatchingTex(proportion.copy(), quadratic),
            run_time=1.3,
        )
        self.play(
            FadeOut(proportion),
            run_time=0.5,
        )
        self.wait(0.4)

        # Beat 4 (17.0-28.0): repeat the cut; the shape never changes.
        recursion_note = Tex(
            r"\textbf{Y se repite para siempre}",
            font_size=32,
            color=WHITE,
        ).move_to(UP * 3.75)
        recursion_note.set_stroke(width=1)
        recursion_note.set_z_index(30)
        self.play(
            FadeOut(remainder_label),
            FadeOut(right_angle_mark),
            FadeIn(recursion_note, shift=DOWN * 0.1),
            run_time=0.6,
        )

        square_palette = (ACCENT_PURPLE, ACCENT_CYAN, ACCENT_YELLOW)
        current_box = remainder_box
        current_remainder = first_remainder
        nested_squares = VGroup()
        for index, square_color in enumerate(square_palette):
            next_square_box, next_remainder_box = cut_square(*current_box)
            nested_square = make_rectangle(
                *next_square_box,
                color=square_color,
                stroke_width=4,
            )
            nested_square.set_fill(square_color, opacity=0.16)
            nested_square.set_z_index(5 + 2 * index)
            next_remainder = make_rectangle(
                *next_remainder_box,
                color=ACCENT_MAGENTA,
                stroke_width=4,
            )
            next_remainder.set_fill(ACCENT_MAGENTA, opacity=0.20)
            next_remainder.set_z_index(6 + 2 * index)

            self.play(
                FadeIn(nested_square),
                Create(next_remainder),
                current_remainder.animate.set_fill(opacity=0.06),
                run_time=0.85,
            )
            nested_squares.add(nested_square)
            current_box = next_remainder_box
            current_remainder = next_remainder

        self.play(
            Indicate(current_remainder, color=ACCENT_MAGENTA, scale_factor=1.2),
            run_time=1.2,
        )
        self.wait(0.5)

        self_similar_note = Tex(
            r"\textbf{Siempre la misma proporción}",
            font_size=32,
            color=ACCENT_MAGENTA,
        ).move_to(UP * 3.75)
        self_similar_note.set_stroke(width=1)
        self_similar_note.set_z_index(30)
        self.play(
            ReplacementTransform(recursion_note, self_similar_note),
            run_time=0.7,
        )
        self.wait(0.6)

        # Beat 5 (28.0-40.0): the numeric payoff and the unique inverse.
        value = MathTex(
            r"\varphi=\frac{1+\sqrt{5}}{2}=1{,}6180339887\ldots",
            font_size=36,
            color=WHITE,
        ).move_to(DOWN * 3.55)
        value.set_stroke(width=1)
        value.set_z_index(30)
        fit_to_safe_width(value)

        inverse_property = MathTex(
            r"\frac{1}{\varphi}=\varphi-1",
            font_size=46,
            color=ACCENT_CYAN,
        ).move_to(DOWN * 4.45)
        inverse_property.set_stroke(width=1)
        inverse_property.set_z_index(30)

        self.play(
            FadeOut(self_similar_note),
            Write(value),
            run_time=1.2,
        )
        self.play(
            Write(inverse_property),
            run_time=1.0,
        )

        payoff_box = SurroundingRectangle(
            inverse_property,
            color=ACCENT_YELLOW,
            buff=0.22,
            corner_radius=0.12,
            stroke_width=3,
        )
        payoff_box.set_color_by_gradient(*GRADIENT_HIGHLIGHT)
        payoff_box.set_z_index(29)
        self.play(Create(payoff_box), run_time=0.6)
        self.play(
            Indicate(quadratic, color=ACCENT_YELLOW, scale_factor=1.08),
            payoff_box.animate.set_stroke(width=5),
            rate_func=there_and_back,
            run_time=1.3,
        )

        unique_note = Tex(
            r"\textbf{El único número cuyo inverso es él menos uno}",
            font_size=30,
            color=WHITE,
        ).move_to(DOWN * 5.25)
        unique_note.set_stroke(width=1)
        unique_note.set_z_index(30)
        fit_to_safe_width(unique_note)
        self.play(FadeIn(unique_note, shift=UP * 0.12), run_time=0.8)
        self.wait(1.4)

        animate_End(scene=self)
