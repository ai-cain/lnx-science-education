from manim import *
from lnx import *

# visual-hook | algebra | basic
# Multiplying complex numbers = rotating and scaling.
#
# Hook: multiplying by i is a 90 degree turn. Two turns leave you pointing at
# -1, so i^2 = -1 stops being a rule to memorize and becomes a picture.
#
# Then the general law: for z, w in the complex plane,
#       |z*w| = |z| * |w|      and      arg(z*w) = arg z + arg w.
# Concrete case: z = 2 (angle 0, no - use z with angle 30) times w.
#   z = 1.6 * (cos 30, sin 30),  w = 1.25 * (cos 45, sin 45)
#   z*w = 2.0 * (cos 75, sin 75).
# Moduli multiply (1.6 * 1.25 = 2), arguments add (30 + 45 = 75).
#
# Real frame is 9 x 16 units. Safe area: |x| <= 3.8, |y| <= 5.6.

SAFE_WIDTH = 7.2

# Single grid unit for the whole video, identical in x and y so a rotation on
# scene points matches a rotation on plane coordinates without distortion.
UNIT = 1.15

# Origin sits below center: the action happens in the first quadrant, which
# grows up and to the right.
PLANE_ORIGIN = np.array([-1.1, -1.6, 0.0])

Z_MOD = 1.6
Z_ARG = 30.0
W_MOD = 1.25
W_ARG = 45.0


def fit_to_safe_width(mobject):
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def P(x, y):
    """Plane coordinate -> scene point, computed by hand so it stays valid
    even while the mobjects are being rotated."""
    return PLANE_ORIGIN + np.array([x * UNIT, y * UNIT, 0.0])


def polar(modulus, degrees):
    """Plane coordinate of a complex number given in polar form."""
    angle = degrees * DEGREES
    return modulus * np.cos(angle), modulus * np.sin(angle)


def make_label(tex, font_size, color):
    """MathTex readable on top of the grid."""
    label = MathTex(tex, font_size=font_size, color=color)
    label.add_background_rectangle(color=BG, opacity=0.92, buff=0.06)
    label.set_z_index(14)
    return label


class ComplexMultiplication(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        Z_COLOR = ACCENT_CYAN        # the number we start from
        W_COLOR = ACCENT_MAGENTA     # the number we multiply by
        RESULT_COLOR = ACCENT_YELLOW # the product
        ARC_COLOR = ACCENT_PURPLE    # angles

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.14
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.85)
        self.add(watermark)

        def make_plane():
            plane = NumberPlane(
                x_range=[-4, 4, 1],
                y_range=[-3, 6, 1],
                x_length=8 * UNIT,
                y_length=9 * UNIT,
                background_line_style={
                    "stroke_color": GREY_B,
                    "stroke_width": 1.6,
                    "stroke_opacity": 0.32,
                },
                axis_config={
                    "stroke_color": GREY_A,
                    "stroke_width": 2.5,
                    "include_ticks": False,
                },
            )
            plane.shift(PLANE_ORIGIN - plane.c2p(0, 0))
            plane.set_z_index(-5)
            return plane

        def vector(x, y, color, width=8):
            arrow = Arrow(
                P(0, 0), P(x, y), buff=0,
                color=color, stroke_width=width,
                max_tip_length_to_length_ratio=0.25,
            )
            arrow.set_z_index(6)
            return arrow

        # ----------------------------------------------------------- hook 0-2s
        # No title card first: the arrow is already on screen and turns.
        plane = make_plane()
        self.add(plane)

        one_vec = vector(2, 0, Z_COLOR)
        one_lab = make_label(r"1", 34, Z_COLOR).move_to(P(2.0, -0.45))
        self.add(one_vec, one_lab)

        hook = Tex(r"multiplicar por $i$\\es girar $90^\circ$",
                   font_size=40, color=WHITE)
        hook.set_stroke(width=1)
        hook.set_z_index(20)
        hook.move_to(UP * 5.0)
        fit_to_safe_width(hook)
        self.play(Write(hook), run_time=0.8)

        turn_arc = Arc(radius=1.5 * UNIT, start_angle=0, angle=PI / 2,
                       arc_center=P(0, 0), color=ARC_COLOR, stroke_width=5)
        turn_arc.set_z_index(4)
        i_vec = vector(0, 2, W_COLOR)
        i_lab = make_label(r"i", 34, W_COLOR).move_to(P(0.55, 2.05))

        self.play(
            Create(turn_arc),
            ReplacementTransform(one_vec, i_vec),
            ReplacementTransform(one_lab, i_lab),
            run_time=1.0,
        )
        self.wait(0.4)

        # Second 90 degree turn: we land on -1. That IS i^2 = -1.
        turn_arc2 = Arc(radius=1.5 * UNIT, start_angle=PI / 2, angle=PI / 2,
                        arc_center=P(0, 0), color=ARC_COLOR, stroke_width=5)
        turn_arc2.set_z_index(4)
        minus_vec = vector(-2, 0, RESULT_COLOR)
        minus_lab = make_label(r"-1", 34, RESULT_COLOR).move_to(P(-2.0, -0.5))

        self.play(
            Create(turn_arc2),
            ReplacementTransform(i_vec, minus_vec),
            ReplacementTransform(i_lab, minus_lab),
            run_time=1.0,
        )
        why = MathTex(r"i^{2}=-1", font_size=48, color=RESULT_COLOR)
        why.set_stroke(width=1)
        why.set_z_index(20)
        why.move_to(DOWN * 4.9)
        self.play(Write(why), run_time=0.7)
        self.wait(0.9)

        # ------------------------------------------- beat 1: la regla completa
        self.play(
            FadeOut(minus_vec), FadeOut(minus_lab), FadeOut(why),
            FadeOut(turn_arc), FadeOut(turn_arc2), FadeOut(hook),
            run_time=0.5,
        )

        rule = Tex(r"multiplicar = girar y estirar",
                   font_size=38, color=WHITE)
        rule.set_stroke(width=1)
        rule.set_z_index(20)
        rule.move_to(UP * 5.15)
        fit_to_safe_width(rule)
        self.play(Write(rule), run_time=0.8)

        zx, zy = polar(Z_MOD, Z_ARG)
        z_vec = vector(zx, zy, Z_COLOR)
        z_lab = make_label(r"z", 34, Z_COLOR).move_to(P(zx + 0.42, zy - 0.16))
        z_arc = Arc(radius=0.62 * UNIT, start_angle=0, angle=Z_ARG * DEGREES,
                    arc_center=P(0, 0), color=ARC_COLOR, stroke_width=4)
        z_arc.set_z_index(4)
        z_data = make_label(r"|z|=1.6,\ \ \arg z=30^\circ", 30, Z_COLOR)
        z_data.move_to(DOWN * 4.15)

        self.play(GrowArrow(z_vec), Write(z_lab), run_time=0.7)
        self.play(Create(z_arc), Write(z_data), run_time=0.7)
        self.wait(0.6)

        wx, wy = polar(W_MOD, W_ARG)
        w_vec = vector(wx, wy, W_COLOR)
        w_lab = make_label(r"w", 34, W_COLOR).move_to(P(wx - 0.5, wy + 0.3))
        w_data = make_label(r"|w|=1.25,\ \ \arg w=45^\circ", 30, W_COLOR)
        w_data.move_to(DOWN * 5.05)

        self.play(GrowArrow(w_vec), Write(w_lab), run_time=0.7)
        self.play(Write(w_data), run_time=0.6)
        self.wait(0.8)

        # ------------------------------------- beat 2: el producto, animado
        # z gira 45 grados mas y se estira 1.25 veces: eso es multiplicar por w.
        px, py = polar(Z_MOD * W_MOD, Z_ARG + W_ARG)
        product_vec = vector(px, py, RESULT_COLOR, width=9)

        product_arc = Arc(
            radius=0.62 * UNIT, start_angle=Z_ARG * DEGREES,
            angle=W_ARG * DEGREES, arc_center=P(0, 0),
            color=W_COLOR, stroke_width=4,
        )
        product_arc.set_z_index(4)

        moving = z_vec.copy().set_color(RESULT_COLOR)
        moving.set_z_index(8)
        self.add(moving)
        self.play(FadeOut(w_data), FadeOut(z_data), run_time=0.3)

        action = Tex(r"gira $45^\circ$ y se estira $1.25\times$",
                     font_size=32, color=RESULT_COLOR)
        action.set_stroke(width=1)
        action.set_z_index(20)
        action.move_to(DOWN * 4.35)
        fit_to_safe_width(action)
        self.play(FadeIn(action, shift=UP * 0.15), run_time=0.5)

        self.play(
            Rotate(moving, angle=W_ARG * DEGREES, about_point=P(0, 0)),
            Create(product_arc),
            run_time=1.2,
        )
        self.play(Transform(moving, product_vec), run_time=0.9)

        p_lab = make_label(r"z\,w", 34, RESULT_COLOR)
        p_lab.move_to(P(px + 0.55, py + 0.1))
        self.play(Write(p_lab), run_time=0.5)
        self.wait(0.7)

        # ------------------------------------------------ beat 3: los numeros
        self.play(FadeOut(action), run_time=0.3)

        mod_line = MathTex(r"|z\,w| = 1.6 \cdot 1.25 = 2",
                           font_size=36, color=RESULT_COLOR)
        arg_line = MathTex(r"\arg(z\,w) = 30^\circ + 45^\circ = 75^\circ",
                           font_size=36, color=ARC_COLOR)
        numbers = VGroup(mod_line, arg_line).arrange(DOWN, buff=0.4)
        numbers.set_stroke(width=1)
        numbers.set_z_index(20)
        numbers.move_to(DOWN * 4.5)
        fit_to_safe_width(numbers)

        self.play(Write(mod_line), run_time=0.8)
        self.play(Write(arg_line), run_time=0.9)
        self.wait(1.2)

        # ----------------------------------------------------------- payoff
        self.play(
            FadeOut(plane), FadeOut(z_vec), FadeOut(z_lab), FadeOut(z_arc),
            FadeOut(w_vec), FadeOut(w_lab), FadeOut(moving), FadeOut(p_lab),
            FadeOut(product_arc), FadeOut(numbers), FadeOut(rule),
            run_time=0.6,
        )

        closing = VGroup(
            MathTex(r"|z\,w| = |z|\,|w|", font_size=42, color=RESULT_COLOR),
            MathTex(r"\arg(z\,w) = \arg z + \arg w", font_size=38,
                    color=ACCENT_CYAN),
        )
        closing.arrange(DOWN, buff=0.55)
        closing.set_stroke(width=1)
        closing.set_z_index(21)
        closing.move_to(ORIGIN)
        fit_to_safe_width(closing)

        self.play(Write(closing[0]), run_time=0.8)
        self.play(Write(closing[1]), run_time=0.9)

        result_box = SurroundingRectangle(closing, buff=0.3, corner_radius=0.14)
        result_box.set_stroke(width=4, color=[ACCENT_YELLOW, ACCENT_PURPLE])
        result_box.set_z_index(20)
        self.play(Create(result_box), run_time=0.7)
        self.wait(1.6)

        animate_End(scene=self)
