from manim import *
from lnx import *

# visual-derivation | trigonometry | intermediate
#
# Triple angle:  sin 3t = 3 sin t - 4 sin^3 t, derived geometrically.
#
# Construction: take a circumference of DIAMETER 1. A chord that subtends a
# central angle a has length 2R sin(a/2) = sin(a/2), so on this circumference
# "chord = sine of half its central angle". Place four points A0, A1, A2, A3
# separated by equal central angles 2t. Then
#
#   short chords  A0A1 = A1A2 = A2A3 = sin t      (central angle 2t)
#   diagonals     A0A2 = A1A3     = sin 2t        (central angle 4t)
#   long chord    A0A3            = sin 3t        (central angle 6t)
#
# Ptolemy on the cyclic quadrilateral A0 A1 A2 A3:
#   A0A2 * A1A3 = A0A1 * A2A3 + A1A2 * A0A3
#   sin^2 2t    = sin^2 t     + sin t * sin 3t
#
# Solve for the long chord and expand sin 2t = 2 sin t cos t:
#   sin 3t = (sin^2 2t - sin^2 t) / sin t
#          = (4 sin^2 t cos^2 t - sin^2 t) / sin t
#          = (4 sin^2 t (1 - sin^2 t) - sin^2 t) / sin t     <- cos^2 = 1 - sin^2
#          = (3 sin^2 t - 4 sin^4 t) / sin t
#          = 3 sin t - 4 sin^3 t
#
# The cubic term is born exactly at the sin^4 that appears when cos^2 t is
# traded for 1 - sin^2 t inside the squared diagonal.
#
# Numeric validation (t = 20 degrees):
#   sin 20  = 0.34202014
#   3*sin20 = 1.02606043
#   4*sin^3(20) = 4 * 0.04000876 = 0.16003503
#   1.02606043 - 0.16003503 = 0.86602540 = sin 60  -> exact match.
#
# The real frame is 9 x 16 units. Safe area: |x| <= 3.8, |y| <= 5.6.

SAFE_WIDTH = 7.2


def fit_to_safe_width(mobject):
    """Shrink a mobject so it never crosses the horizontal safe margins."""
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def make_label(tex, font_size, color, with_background=False):
    """MathTex label placed above geometry, optionally shielded from lines."""
    label = MathTex(tex, font_size=font_size, color=color)
    if with_background:
        label.add_background_rectangle(color=BG, opacity=0.92, buff=0.06)
    label.set_z_index(15)
    return label


class TripleAngle(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        SHORT_COLOR = ACCENT_CYAN     # chords of central angle 2t  -> sin t
        DIAG_COLOR = ACCENT_MAGENTA   # diagonals of central angle 4t -> sin 2t
        LONG_COLOR = ACCENT_YELLOW    # long chord, central angle 6t -> sin 3t
        ARC_COLOR = ACCENT_PURPLE     # the circumference itself
        AUX_COLOR = GREY_B            # radii and secondary marks

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.13
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.8)
        self.add(watermark)

        # ------------------------------------------------------------ geometry
        center = np.array([0.0, 2.35, 0.0])
        R = 2.0                       # drawn radius; the *math* radius is 1/2
        THETA = 35.0                  # degrees, so 6t = 210 deg fits nicely
        START = 160.0                 # angular position of A0

        def on_circle(deg):
            return center + R * np.array(
                [np.cos(deg * DEGREES), np.sin(deg * DEGREES), 0.0]
            )

        # Four points spaced by equal central angles of 2*THETA, going clockwise.
        P = [on_circle(START - 2 * THETA * k) for k in range(4)]

        def outward(point_a, point_b, distance=0.45):
            """Midpoint of a chord pushed away from the center of the figure."""
            mid = (point_a + point_b) / 2
            direction = mid - center
            norm = np.linalg.norm(direction)
            if norm < 1e-6:
                direction = np.array([0.0, -1.0, 0.0])
                norm = 1.0
            return mid + direction / norm * distance

        # ------------------------------------------------------- hook 0.0-2.0s
        title = Tex(r"El ángulo triple", font_size=58, color=WHITE)
        title.set_stroke(width=1)
        title.move_to(UP * 5.35)
        title.set_z_index(20)
        fit_to_safe_width(title)

        underline = Line(
            title.get_left() + DOWN * 0.3,
            title.get_right() + DOWN * 0.3,
            stroke_width=4,
        )
        underline.set_color(color=[ACCENT_CYAN, ACCENT_MAGENTA, ACCENT_YELLOW])
        underline.set_z_index(20)

        circumference = Circle(radius=R, color=ARC_COLOR, stroke_width=3)
        circumference.move_to(center)
        circumference.set_stroke(opacity=0.75)

        short_chords = VGroup(
            *[
                Line(P[k], P[k + 1], color=SHORT_COLOR, stroke_width=6)
                for k in range(3)
            ]
        )
        short_chords.set_z_index(4)
        dots = VGroup(*[Dot(point, color=WHITE, radius=0.06) for point in P])
        dots.set_z_index(6)

        # Hook: the circumference and three identical chords land immediately.
        self.play(Write(title), Create(circumference), run_time=0.9)
        self.play(
            Create(underline),
            LaggedStart(*[Create(chord) for chord in short_chords], lag_ratio=0.25),
            FadeIn(dots),
            run_time=1.0,
        )

        # ------------------------------------------- the unit-diameter contract
        diameter = Line(on_circle(90), on_circle(270), color=AUX_COLOR,
                        stroke_width=3)
        diameter.set_stroke(opacity=0.6)
        diameter_label = make_label(r"\text{diámetro}=1", 30, AUX_COLOR,
                                    with_background=True)
        diameter_label.next_to(circumference, LEFT, buff=0.12)
        rule = MathTex(
            r"\text{cuerda}=\operatorname{sen}\left(\tfrac{\text{ángulo central}}{2}\right)",
            font_size=30, color=WHITE,
        )
        rule.set_z_index(20)
        rule.move_to(np.array([0.0, -0.55, 0.0]))
        fit_to_safe_width(rule)

        self.play(Create(diameter), FadeIn(diameter_label), run_time=0.6)
        self.play(Write(rule), run_time=0.8)
        self.wait(0.4)
        self.play(FadeOut(diameter), FadeOut(diameter_label), run_time=0.4)

        # ------------------------------------------- central angles of size 2t
        radii = VGroup(
            *[
                Line(center, point, color=AUX_COLOR, stroke_width=2)
                for point in P
            ]
        )
        radii.set_stroke(opacity=0.45)
        radii.set_z_index(1)

        central_arcs = VGroup(
            *[
                Angle(
                    Line(center, P[k + 1]), Line(center, P[k]),
                    radius=0.5 + 0.16 * k, color=SHORT_COLOR, stroke_width=3,
                )
                for k in range(3)
            ]
        )
        central_arcs.set_z_index(3)

        self.play(Create(radii), Create(central_arcs), run_time=0.9)

        two_theta = make_label(r"2\theta", 28, SHORT_COLOR)
        two_theta.move_to(
            Angle(Line(center, P[1]), Line(center, P[0]), radius=1.05)
            .point_from_proportion(0.5)
        )
        self.play(Write(two_theta), run_time=0.5)

        # Each 2t-chord measures sin(t): three equal cyan segments.
        short_labels = VGroup(
            *[
                make_label(r"\operatorname{sen}\theta", 28, SHORT_COLOR)
                .move_to(outward(P[k], P[k + 1], 0.46))
                for k in range(3)
            ]
        )
        self.play(
            LaggedStart(*[Write(lbl) for lbl in short_labels], lag_ratio=0.2),
            run_time=1.0,
        )
        self.wait(0.3)
        self.play(FadeOut(central_arcs), FadeOut(two_theta), run_time=0.4)

        # --------------------------------------------------- the target: sin 3t
        long_chord = Line(P[0], P[3], color=LONG_COLOR, stroke_width=7)
        long_chord.set_z_index(5)
        long_label = make_label(r"\operatorname{sen}3\theta", 32, LONG_COLOR,
                                with_background=True)
        long_label.move_to(outward(P[0], P[3], 0.55))

        six_theta = make_label(r"6\theta", 28, LONG_COLOR)
        six_theta.move_to(
            Angle(Line(center, P[3]), Line(center, P[0]), radius=0.95)
            .point_from_proportion(0.5)
        )
        big_arc = Angle(
            Line(center, P[3]), Line(center, P[0]),
            radius=0.62, color=LONG_COLOR, stroke_width=3,
        )
        big_arc.set_z_index(3)

        self.play(Create(big_arc), Write(six_theta), run_time=0.6)
        self.play(Create(long_chord), Write(long_label), run_time=0.8)
        self.wait(0.4)
        self.play(FadeOut(big_arc), FadeOut(six_theta), FadeOut(rule),
                  run_time=0.4)

        # ------------------------------------------------- diagonals = sin 2t
        diagonals = VGroup(
            Line(P[0], P[2], color=DIAG_COLOR, stroke_width=5),
            Line(P[1], P[3], color=DIAG_COLOR, stroke_width=5),
        )
        diagonals.set_z_index(4)
        diag_label = make_label(r"\operatorname{sen}2\theta", 30, DIAG_COLOR,
                                with_background=True)
        diag_label.next_to(circumference, RIGHT, buff=0.15)
        diag_leader = Line(
            diag_label.get_left(), (P[1] + P[3]) / 2,
            color=DIAG_COLOR, stroke_width=2,
        )
        diag_leader.set_stroke(opacity=0.6)

        self.play(Create(diagonals), run_time=0.7)
        self.play(Create(diag_leader), FadeIn(diag_label), run_time=0.5)
        self.play(FadeOut(radii), run_time=0.3)
        self.wait(0.3)

        # --------------------------------------------------- Ptolemy's identity
        ptolemy_tag = Tex(r"Ptolomeo", font_size=32, color=WHITE)
        ptolemy_tag.set_z_index(20)
        ptolemy_tag.move_to(np.array([0.0, -0.35, 0.0]))

        step1 = MathTex(
            r"\operatorname{sen}^2 2\theta", r"=",
            r"\operatorname{sen}^2\theta", r"+",
            r"\operatorname{sen}\theta\,\operatorname{sen}3\theta",
            font_size=38,
        )
        step1[0].set_color(DIAG_COLOR)
        step1[2].set_color(SHORT_COLOR)
        step1[4].set_color(LONG_COLOR)
        step1.set_z_index(20)
        step1.move_to(np.array([0.0, -1.45, 0.0]))
        fit_to_safe_width(step1)

        self.play(Write(ptolemy_tag), run_time=0.5)
        self.play(Write(step1), run_time=1.1)
        self.wait(0.5)

        # Isolate the long chord, still the same object under study.
        step2 = MathTex(
            r"\operatorname{sen}3\theta", r"=",
            r"\frac{\operatorname{sen}^2 2\theta-\operatorname{sen}^2\theta}"
            r"{\operatorname{sen}\theta}",
            font_size=38,
        )
        step2[0].set_color(LONG_COLOR)
        step2.set_z_index(20)
        step2.move_to(np.array([0.0, -2.85, 0.0]))
        fit_to_safe_width(step2)

        self.play(TransformFromCopy(step1, step2), run_time=1.0)
        self.wait(0.4)

        # ------------------------------------------- where the cube is born
        step3 = MathTex(
            r"\operatorname{sen}^2 2\theta", r"=",
            r"4\operatorname{sen}^2\theta\,",
            r"\underbrace{\cos^2\theta}_{1-\operatorname{sen}^2\theta}",
            font_size=36,
        )
        step3[0].set_color(DIAG_COLOR)
        step3[3].set_color(ACCENT_PURPLE)
        step3.set_z_index(20)
        step3.move_to(np.array([0.0, -4.25, 0.0]))
        fit_to_safe_width(step3)

        self.play(Write(step3), run_time=1.0)
        self.wait(0.5)

        cube_note = Tex(
            r"aquí nace el término cúbico",
            font_size=30, color=ACCENT_PURPLE,
        )
        cube_note.set_z_index(20)
        cube_note.next_to(step3, DOWN, buff=0.3)
        fit_to_safe_width(cube_note)
        self.play(FadeIn(cube_note, shift=UP * 0.2), run_time=0.6)
        self.play(Indicate(step3[3], color=ACCENT_YELLOW, scale_factor=1.2),
                  run_time=0.7)
        self.wait(0.4)

        # ---------------------------------------------------------- the payoff
        # Clear the working area, keep the construction as the visual anchor.
        self.play(
            FadeOut(VGroup(ptolemy_tag, step1, step2, step3, cube_note)),
            run_time=0.6,
        )

        expanded = MathTex(
            r"\operatorname{sen}3\theta", r"=",
            r"\frac{3\operatorname{sen}^2\theta-4\operatorname{sen}^4\theta}"
            r"{\operatorname{sen}\theta}",
            font_size=40,
        )
        expanded[0].set_color(LONG_COLOR)
        expanded.set_z_index(20)
        expanded.move_to(np.array([0.0, -1.6, 0.0]))
        fit_to_safe_width(expanded)

        self.play(Write(expanded), run_time=1.0)
        self.wait(0.5)

        result = MathTex(
            r"\operatorname{sen}3\theta", r"=",
            r"3\operatorname{sen}\theta", r"-",
            r"4\operatorname{sen}^3\theta",
            font_size=46,
        )
        result[0].set_color(LONG_COLOR)
        result[2].set_color(SHORT_COLOR)
        result[4].set_color(ACCENT_PURPLE)
        result.set_stroke(width=1)
        result.set_z_index(21)
        result.move_to(np.array([0.0, -3.4, 0.0]))
        fit_to_safe_width(result)

        self.play(TransformMatchingShapes(expanded.copy(), result), run_time=1.2)
        self.play(FadeOut(expanded), run_time=0.4)

        result_box = SurroundingRectangle(result, buff=0.2, corner_radius=0.12)
        result_box.set_stroke(width=4, color=[ACCENT_CYAN, ACCENT_YELLOW])
        result_box.set_z_index(20)
        self.play(Create(result_box), run_time=0.7)
        self.play(Indicate(long_chord, color=ACCENT_YELLOW, scale_factor=1.0),
                  run_time=0.7)
        self.wait(1.4)

        animate_End(scene=self)
