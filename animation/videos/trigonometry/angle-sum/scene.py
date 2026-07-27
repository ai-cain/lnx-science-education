from manim import *
from lnx import *

# proof-without-words | trigonometry | intermediate
# sin(a+b) = sin(a)cos(b) + cos(a)sin(b), demonstrated with nested right
# triangles using the classical construction and no long explanatory text.
#
# The actual frame is 9 x 16 units (x in [-4.5, 4.5], y in [-8, 8]).
# Safe area: |y| <= 5.6 and |x| <= 3.8.

SAFE_WIDTH = 7.2


def fit_to_safe_width(mobject):
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def make_label(tex, font_size, color, with_background=True):
    """Create a MathTex label with an optional background for line crossings."""
    label = MathTex(tex, font_size=font_size, color=color)
    if with_background:
        label.add_background_rectangle(color=BG, opacity=0.92, buff=0.06)
    # Labels must always remain readable above the geometry.
    label.set_z_index(10)
    return label


class AngleSum(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.14
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.85)
        self.add(watermark)

        ALPHA_COLOR = ACCENT_CYAN
        BETA_COLOR = ACCENT_MAGENTA
        HYPOTENUSE_COLOR = ACCENT_YELLOW
        AUXILIARY_COLOR = GREY_B

        # A smaller angle sum opens the silhouette so the main triangle uses
        # the vertical frame width instead of looking like a narrow needle.
        radius = 7.0
        alpha = 32 * DEGREES
        beta = 23 * DEGREES

        offset = np.array([-3.0, -3.3, 0])
        O = ORIGIN + offset
        P = radius * np.array([
            np.cos(alpha + beta),
            np.sin(alpha + beta),
            0,
        ]) + offset
        H = np.array([P[0], offset[1], 0])
        M = radius * np.cos(beta) * np.array([
            np.cos(alpha),
            np.sin(alpha),
            0,
        ]) + offset
        N = np.array([M[0], offset[1], 0])
        K = np.array([H[0], M[1], 0])

        origin = O
        center = (O + P + M + N + H + K) / 6

        def outside_segment(A, B, distance=0.4):
            """Move the segment midpoint away from the figure center."""
            midpoint = (A + B) / 2
            direction = B - A
            normal = np.array([-direction[1], direction[0], 0])
            normal = normal / np.linalg.norm(normal)
            if np.dot(normal, midpoint - center) < 0:
                normal = -normal
            return midpoint + normal * distance

        # ---------------------------------------------------------- hook 0-2s
        title = MathTex(r"\sin(\alpha+\beta)", r"=", r"\,?\,", font_size=70)
        title[0].set_color(HYPOTENUSE_COLOR)
        title[2].set_color(BETA_COLOR)
        title.set_stroke(width=1)
        title.set_z_index(10)
        title.move_to(UP * 5.35)
        fit_to_safe_width(title)
        self.play(Write(title), run_time=0.9)
        self.wait(0.3)

        # ------------------------------------------------------- construction
        # The support line ends with the geometry. A long fixed tail made the
        # main triangle look artificially narrow.
        baseline = Line(
            O + LEFT * 0.25,
            N + RIGHT * 0.25,
            color=AUXILIARY_COLOR,
            stroke_width=2,
            stroke_opacity=0.55,
        )
        self.play(Create(baseline), run_time=0.6)

        alpha_ray = Line(origin, M, color=ALPHA_COLOR, stroke_width=4)
        alpha_arc = Angle(baseline, alpha_ray, radius=0.55, color=ALPHA_COLOR)
        alpha_label = make_label(
            r"\alpha", 36, ALPHA_COLOR, with_background=False
        ).move_to(
            Angle(baseline, alpha_ray, radius=0.9).point_from_proportion(0.5)
        )
        self.play(
            Create(alpha_ray),
            Create(alpha_arc),
            Write(alpha_label),
            run_time=0.7,
        )
        self.wait(0.2)

        hypotenuse = Line(origin, P, color=HYPOTENUSE_COLOR, stroke_width=6)
        beta_arc = Angle(alpha_ray, hypotenuse, radius=0.9, color=BETA_COLOR)
        beta_label = make_label(
            r"\beta", 36, BETA_COLOR, with_background=False
        ).move_to(
            Angle(alpha_ray, hypotenuse, radius=1.25).point_from_proportion(0.5)
        )
        self.play(
            Create(hypotenuse),
            Create(beta_arc),
            Write(beta_label),
            run_time=0.8,
        )

        unit_label = make_label("1", 34, WHITE).move_to(
            outside_segment(origin, P, 0.4)
        )
        self.play(FadeIn(unit_label), run_time=0.4)
        self.wait(0.4)

        def make_right_angle(vertex, endpoint_1, endpoint_2, length=0.15):
            """Create a right-angle marker whose rays start at the vertex."""
            return RightAngle(
                Line(vertex, endpoint_1),
                Line(vertex, endpoint_2),
                length=length,
                color=WHITE,
                stroke_width=2,
            )

        # Triangle 1: O-M-P. Its hypotenuse is 1, adjacent side is cos(beta),
        # and opposite side is sin(beta). Complete it before moving forward.
        point_m = Dot(M, color=WHITE, radius=0.06)
        perpendicular_pm = DashedLine(P, M, color=AUXILIARY_COLOR, stroke_width=2)
        right_angle_m = make_right_angle(M, origin, P)
        self.play(
            FadeIn(point_m),
            Create(perpendicular_pm),
            Create(right_angle_m),
            run_time=0.6,
        )

        om_label = make_label(r"\cos\beta", 28, ALPHA_COLOR).move_to(
            outside_segment(origin, M, 0.4)
        )
        mp_label = make_label(r"\sin\beta", 30, BETA_COLOR).move_to(
            outside_segment(M, P, 0.45)
        )
        self.play(Write(om_label), run_time=0.5)
        self.play(Write(mp_label), run_time=0.5)
        self.wait(0.4)

        # Triangle 2: O-N-M. Its hypotenuse is cos(beta), and its opposite side
        # is cos(beta)sin(alpha).
        point_n = Dot(N, color=WHITE, radius=0.06)
        perpendicular_mn = DashedLine(M, N, color=AUXILIARY_COLOR, stroke_width=2)
        right_angle_n = make_right_angle(N, origin, M)
        self.play(
            FadeIn(point_n),
            Create(perpendicular_mn),
            Create(right_angle_n),
            run_time=0.6,
        )
        alpha_region = Polygon(
            origin,
            N,
            M,
            fill_color=ALPHA_COLOR,
            fill_opacity=0.08,
            stroke_width=0,
        )
        self.play(FadeIn(alpha_region), run_time=0.25)
        self.bring_to_back(alpha_region)
        mn_label = make_label(r"\cos\beta\sin\alpha", 26, ALPHA_COLOR).move_to(
            outside_segment(M, N, 0.55)
        )
        self.play(Write(mn_label), run_time=0.6)
        self.wait(0.4)

        # Triangle 3: M-K-P. Its hypotenuse is sin(beta), and its opposite side
        # is sin(beta)cos(alpha).
        point_k = Dot(K, color=WHITE, radius=0.06)
        perpendicular_mk = DashedLine(M, K, color=AUXILIARY_COLOR, stroke_width=2)
        right_angle_k = make_right_angle(K, M, P)
        self.play(
            FadeIn(point_k),
            Create(perpendicular_mk),
            Create(right_angle_k),
            run_time=0.6,
        )
        beta_region = Polygon(
            M,
            K,
            P,
            fill_color=BETA_COLOR,
            fill_opacity=0.05,
            stroke_width=0,
        )
        self.play(FadeIn(beta_region), run_time=0.25)
        self.bring_to_back(beta_region)

        # The alpha angle repeats at M as an alternate interior angle between
        # M->K, which is parallel to the baseline, and M->P.
        repeated_alpha_arc = Angle(
            Line(M, K),
            Line(M, P),
            radius=0.4,
            color=ALPHA_COLOR,
            other_angle=True,
        )
        repeated_alpha_label = make_label(
            r"\alpha", 24, ALPHA_COLOR, with_background=False
        ).move_to(
            Angle(
                Line(M, K),
                Line(M, P),
                radius=0.62,
                other_angle=True,
            ).point_from_proportion(0.5)
        )
        self.play(
            Create(repeated_alpha_arc),
            Write(repeated_alpha_label),
            run_time=0.6,
        )
        self.wait(0.6)

        # Build the perpendicular that represents sin(alpha + beta) = P->H.
        # K->P is sin(beta)cos(alpha), while H->K equals the already displayed
        # M->N = cos(beta)sin(alpha). Only draw the upper dashed segment because
        # the lower component is already represented by M->N.
        perpendicular_ph = DashedLine(P, K, color=AUXILIARY_COLOR, stroke_width=2)
        point_h = Dot(H, color=WHITE, radius=0.06)
        right_angle_h = make_right_angle(H, origin, P)
        self.play(
            Create(perpendicular_ph),
            FadeIn(point_h),
            Create(right_angle_h),
            run_time=0.6,
        )
        self.wait(0.5)

        # Place the label to the right of K-P so it does not collide with the
        # yellow hypotenuse or its label.
        kp_label = make_label(r"\sin\beta\cos\alpha", 24, BETA_COLOR).move_to(
            K + (P - K) * 0.35 + RIGHT * 0.38
        )
        self.play(Write(kp_label), run_time=0.6)
        self.wait(0.6)

        # ----------------------------------------------------------- assembly
        # O-H-P is the geometric result. Fade the partial regions so only the
        # subtle yellow result fill remains.
        main_triangle = Polygon(
            origin,
            H,
            P,
            fill_color=HYPOTENUSE_COLOR,
            fill_opacity=0.10,
            stroke_width=0,
        )
        self.play(
            FadeOut(alpha_region),
            FadeOut(beta_region),
            FadeIn(main_triangle),
            run_time=0.5,
        )
        self.bring_to_back(main_triangle)

        # Close O-H in yellow without recoloring the full support line.
        bottom_edge = Line(origin, H, color=HYPOTENUSE_COLOR, stroke_width=6)
        bottom_edge.set_z_index(5)
        self.play(Create(bottom_edge), run_time=0.5)

        # P-H is the result being assembled, so it shares the hypotenuse color.
        result_edge = Line(H, P, color=HYPOTENUSE_COLOR, stroke_width=6)
        result_edge.set_z_index(5)
        self.play(Indicate(result_edge, scale_factor=1.0), run_time=0.8)
        self.wait(0.3)

        formula = MathTex(
            r"\sin(\alpha+\beta)",
            r"=",
            r"\sin\beta\cos\alpha",
            r"+",
            r"\cos\beta\sin\alpha",
            font_size=42,
        )
        formula[2].set_color(BETA_COLOR)
        formula[4].set_color(ALPHA_COLOR)
        formula[0].set_color(HYPOTENUSE_COLOR)
        formula.set_stroke(width=1)
        formula.set_z_index(21)
        formula.move_to(DOWN * 5.25)
        fit_to_safe_width(formula)

        # Assemble the formula from copies of objects already on screen.
        self.play(FadeOut(title[1]), FadeOut(title[2]), run_time=0.4)
        self.play(TransformFromCopy(title[0], formula[0]), run_time=1.0)
        self.play(Write(formula[1]), run_time=0.3)
        self.play(TransformFromCopy(kp_label[1], formula[2]), run_time=0.9)
        self.play(Write(formula[3]), run_time=0.3)
        self.play(TransformFromCopy(mn_label[1], formula[4]), run_time=0.9)
        self.wait(1.2)

        result_box = SurroundingRectangle(formula, buff=0.18, corner_radius=0.12)
        result_box.set_stroke(width=4, color=[YELLOW, ORANGE])
        result_box.set_z_index(20)
        self.play(Create(result_box), run_time=0.7)
        self.wait(1.6)

        animate_End(scene=self)
