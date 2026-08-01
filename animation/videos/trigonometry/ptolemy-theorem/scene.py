from manim import *
from lnx import *

# proof-without-words | trigonometry | intermediate
# Ptolemy's theorem: in a cyclic quadrilateral ABCD (vertices in this cyclic
# order) the product of the diagonals equals the sum of the products of the
# two pairs of opposite sides:
#
#       AC * BD = AB * CD + BC * AD
#
# The construction below inscribes ABCD in a circumference of radius R = 2.4
# centred at (0, 1.6), with the vertices at 20, 105, 190 and 290 degrees.
# Every chord obeys  chord = 2 R sin(delta / 2)  with delta the central arc.
#
# Numerical validation of the exact coordinates used in this scene:
#   A = ( 2.25526,  2.42085)   B = (-0.62117,  3.91822)
#   C = (-2.36354,  1.18324)   D = ( 0.82085, -0.65526)
#   AB = 3.2428330   BC = 3.2428330   CD = 3.6770133   AD = 3.3941125
#   AC = 4.7817346   BD = 4.7954315
#   AC * BD             = 22.9304803156493
#   AB * CD + BC * AD   = 22.9304803156493   -> equal to 1e-14
#
# Taking BD as a diameter of length 1 turns Ptolemy's identity into the sine
# addition formula sin(A + B) = sin A cos B + cos A sin B, which is the payoff.
#
# The actual frame is 9 x 16 units (x in [-4.5, 4.5], y in [-8, 8]).
# Safe area: |x| <= 3.8 and |y| <= 5.6.

SAFE_WIDTH = 7.2


def fit_to_safe_width(mobject):
    """Shrink a mobject so it never crosses the horizontal safe area."""
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


class PtolemyTheorem(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.14
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.85)
        self.add(watermark)

        DIAGONAL_COLOR = ACCENT_CYAN     # AC and BD
        PAIR_ONE_COLOR = ACCENT_YELLOW   # opposite sides AB and CD
        PAIR_TWO_COLOR = ACCENT_MAGENTA  # opposite sides BC and AD
        QUAD_COLOR = ACCENT_PURPLE       # the quadrilateral outline
        AUX_COLOR = GREY_B               # the circumference

        # ------------------------------------------------------------ geometry
        center = np.array([0.0, 1.6, 0.0])
        R = 2.4

        def on_circle(deg):
            return center + R * np.array([
                np.cos(deg * DEGREES),
                np.sin(deg * DEGREES),
                0.0,
            ])

        # Cyclic order A -> B -> C -> D around the circumference.
        A = on_circle(20)
        B = on_circle(105)
        C = on_circle(190)
        D = on_circle(290)

        centroid = (A + B + C + D) / 4

        def outward(P, distance=0.4):
            """Push a vertex label radially away from the figure."""
            direction = P - centroid
            return P + direction / np.linalg.norm(direction) * distance

        def outside_segment(P1, P2, distance=0.42):
            """Place a length label outside the quadrilateral, off the line."""
            midpoint = (P1 + P2) / 2
            direction = P2 - P1
            normal = np.array([-direction[1], direction[0], 0.0])
            normal = normal / np.linalg.norm(normal)
            if np.dot(normal, midpoint - centroid) < 0:
                normal = -normal
            return midpoint + normal * distance

        def label(tex, font_size, color, shaded=False):
            item = MathTex(tex, font_size=font_size, color=color)
            if shaded:
                item.add_background_rectangle(color=BG, opacity=0.92, buff=0.06)
            item.set_z_index(12)
            return item

        # ------------------------------------------------------- hook 0.0-2.0s
        title = Tex(r"Teorema de Ptolomeo", font_size=58, color=WHITE)
        title.set_stroke(width=1)
        title.set_z_index(20)
        title.move_to(UP * 5.4)
        fit_to_safe_width(title)

        underline = Line(
            title.get_left() + DOWN * 0.3,
            title.get_right() + DOWN * 0.3,
            stroke_width=4,
        )
        underline.set_color(color=[ACCENT_CYAN, ACCENT_MAGENTA])
        underline.set_z_index(20)

        circle = Circle(radius=R, color=AUX_COLOR, stroke_width=2.5)
        circle.move_to(center)
        circle.set_stroke(opacity=0.7)

        # The circumference lands together with the title so the first frames
        # already carry the image, not just a heading.
        self.play(Write(title), Create(circle), run_time=1.1)
        self.play(Create(underline), run_time=0.4)

        dots = VGroup(*[Dot(P, color=WHITE, radius=0.06) for P in (A, B, C, D)])
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.15), run_time=0.5)

        # ------------------------------------------- the cyclic quadrilateral
        quad = Polygon(
            A, B, C, D,
            color=QUAD_COLOR, stroke_width=5,
            fill_color=QUAD_COLOR, fill_opacity=0.06,
        )
        quad.set_z_index(2)

        vertex_labels = VGroup(
            label("A", 32, WHITE).move_to(outward(A)),
            label("B", 32, WHITE).move_to(outward(B)),
            label("C", 32, WHITE).move_to(outward(C)),
            label("D", 32, WHITE).move_to(outward(D)),
        )

        self.play(Create(quad), run_time=1.0)
        self.play(Write(vertex_labels), run_time=0.6)

        caption = Tex(
            r"Cuadril\'atero inscrito en una circunferencia",
            font_size=30, color=WHITE,
        )
        caption.set_z_index(20)
        caption.move_to(UP * 4.55)
        fit_to_safe_width(caption)
        self.play(FadeIn(caption, shift=DOWN * 0.15), run_time=0.5)
        self.wait(0.4)

        # ------------------------------------------------- the two diagonals
        diagonal_ac = Line(A, C, color=DIAGONAL_COLOR, stroke_width=6)
        diagonal_bd = Line(B, D, color=DIAGONAL_COLOR, stroke_width=6)
        VGroup(diagonal_ac, diagonal_bd).set_z_index(4)

        diagonals_caption = Tex(
            r"Las diagonales", font_size=32, color=DIAGONAL_COLOR,
        )
        diagonals_caption.set_z_index(20)
        diagonals_caption.move_to(caption.get_center())
        fit_to_safe_width(diagonals_caption)

        self.play(
            Create(diagonal_ac), Create(diagonal_bd),
            FadeTransform(caption, diagonals_caption),
            run_time=1.0,
        )
        self.wait(0.5)

        # ------------------------------------- the two pairs of opposite sides
        side_ab = Line(A, B, color=PAIR_ONE_COLOR, stroke_width=7)
        side_cd = Line(C, D, color=PAIR_ONE_COLOR, stroke_width=7)
        side_bc = Line(B, C, color=PAIR_TWO_COLOR, stroke_width=7)
        side_ad = Line(D, A, color=PAIR_TWO_COLOR, stroke_width=7)
        VGroup(side_ab, side_cd, side_bc, side_ad).set_z_index(3)

        # Length labels always sit outside the quadrilateral, never on a line.
        label_ab = label("AB", 28, PAIR_ONE_COLOR).move_to(
            outside_segment(A, B)
        )
        label_cd = label("CD", 28, PAIR_ONE_COLOR).move_to(
            outside_segment(C, D)
        )
        label_bc = label("BC", 28, PAIR_TWO_COLOR).move_to(
            outside_segment(B, C)
        )
        label_ad = label("AD", 28, PAIR_TWO_COLOR).move_to(
            outside_segment(D, A)
        )

        sides_caption = Tex(
            r"Los lados opuestos, por parejas",
            font_size=30, color=WHITE,
        )
        sides_caption.set_z_index(20)
        sides_caption.move_to(caption.get_center())
        fit_to_safe_width(sides_caption)

        self.play(
            Create(side_ab), Create(side_cd),
            Write(label_ab), Write(label_cd),
            FadeTransform(diagonals_caption, sides_caption),
            run_time=0.9,
        )
        self.play(
            Create(side_bc), Create(side_ad),
            Write(label_bc), Write(label_ad),
            run_time=0.9,
        )
        self.wait(0.4)

        # -------------------------------------------------- the identity
        equation = MathTex(
            r"AC \cdot BD", r"=", r"AB \cdot CD", r"+", r"BC \cdot AD",
            font_size=42,
        )
        equation[0].set_color(DIAGONAL_COLOR)
        equation[2].set_color(PAIR_ONE_COLOR)
        equation[4].set_color(PAIR_TWO_COLOR)
        equation.set_stroke(width=1)
        equation.set_z_index(21)
        equation.move_to(np.array([0.0, -2.35, 0.0]))
        fit_to_safe_width(equation)

        # Each term flies out of the geometry that produced it.
        self.play(
            TransformFromCopy(VGroup(diagonal_ac, diagonal_bd), equation[0]),
            run_time=0.9,
        )
        self.play(Write(equation[1]), run_time=0.35)
        self.play(
            TransformFromCopy(VGroup(side_ab, side_cd), equation[2]),
            run_time=0.8,
        )
        self.play(Write(equation[3]), run_time=0.35)
        self.play(
            TransformFromCopy(VGroup(side_bc, side_ad), equation[4]),
            run_time=0.8,
        )
        self.wait(0.4)

        equation_box = SurroundingRectangle(
            equation, buff=0.18, corner_radius=0.12,
        )
        equation_box.set_stroke(width=4, color=[ACCENT_CYAN, ACCENT_MAGENTA])
        equation_box.set_z_index(20)
        self.play(Create(equation_box), run_time=0.6)
        self.wait(0.4)

        # -------------------------------------------- numeric check on screen
        # Values measured on the very coordinates drawn above (see header).
        numbers = MathTex(
            r"4{,}7817 \cdot 4{,}7954", r"=", r"22{,}930",
            font_size=32,
        )
        numbers[0].set_color(DIAGONAL_COLOR)
        numbers[2].set_color(WHITE)
        numbers.set_z_index(21)
        numbers.move_to(np.array([0.0, -3.35, 0.0]))
        fit_to_safe_width(numbers)

        numbers_two = MathTex(
            r"3{,}2428 \cdot 3{,}6770", r"+", r"3{,}2428 \cdot 3{,}3941",
            r"=", r"22{,}930",
            font_size=32,
        )
        numbers_two[0].set_color(PAIR_ONE_COLOR)
        numbers_two[2].set_color(PAIR_TWO_COLOR)
        numbers_two[4].set_color(WHITE)
        numbers_two.set_z_index(21)
        numbers_two.move_to(np.array([0.0, -4.1, 0.0]))
        fit_to_safe_width(numbers_two)

        self.play(FadeIn(numbers, shift=UP * 0.15), run_time=0.7)
        self.play(FadeIn(numbers_two, shift=UP * 0.15), run_time=0.7)
        self.play(
            Indicate(numbers[2], color=ACCENT_YELLOW, scale_factor=1.25),
            Indicate(numbers_two[4], color=ACCENT_YELLOW, scale_factor=1.25),
            run_time=0.9,
        )
        self.wait(0.5)

        # ------------------------------------------------------- the payoff
        # With BD a diameter of length 1, Ptolemy's identity becomes the sine
        # addition formula: this is where sin(A + B) actually comes from.
        self.play(
            FadeOut(numbers), FadeOut(numbers_two),
            FadeOut(sides_caption),
            run_time=0.5,
        )

        payoff_title = Tex(
            r"Si $BD$ es un di\'ametro de longitud $1$:",
            font_size=30, color=WHITE,
        )
        payoff_title.set_z_index(21)
        payoff_title.move_to(np.array([0.0, -3.35, 0.0]))
        fit_to_safe_width(payoff_title)

        payoff = MathTex(
            r"\sin(A + B)", r"=", r"\sin A \cos B", r"+", r"\cos A \sin B",
            font_size=38,
        )
        payoff[0].set_color(DIAGONAL_COLOR)
        payoff[2].set_color(PAIR_ONE_COLOR)
        payoff[4].set_color(PAIR_TWO_COLOR)
        payoff.set_stroke(width=1)
        payoff.set_z_index(21)
        payoff.move_to(np.array([0.0, -4.35, 0.0]))
        fit_to_safe_width(payoff)

        self.play(FadeIn(payoff_title, shift=UP * 0.15), run_time=0.6)
        self.play(
            TransformMatchingShapes(equation.copy(), payoff),
            run_time=1.3,
        )
        self.wait(0.4)

        payoff_box = SurroundingRectangle(payoff, buff=0.18, corner_radius=0.12)
        payoff_box.set_stroke(width=4, color=[ACCENT_YELLOW, ACCENT_MAGENTA])
        payoff_box.set_z_index(20)
        self.play(Create(payoff_box), run_time=0.6)
        self.wait(1.6)

        animate_End(scene=self)
