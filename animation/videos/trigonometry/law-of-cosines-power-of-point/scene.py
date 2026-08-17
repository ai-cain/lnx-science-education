from manim import *
from lnx import *

# proof-without-words | trigonometry | advanced
# Law of Cosines via the POWER OF A POINT:  b^2 = a^2 + c^2 - 2ac*cos(B).
#
# The elegant twin of the circumcircle proof of the Law of Sines: no algebraic
# squaring anywhere. Draw the circle centred at C with radius b, so it passes
# through A. Every line through B meets it twice, and the product of the two
# distances is the same number (power of B):
#   line B-C:   the two hits are at a - b and a + b   =>  power = (a-b)(a+b)
#   line B-A:   one hit is A itself, the other is A'   =>  power = c * BA'
# Since C is equidistant from A and A', it lies on the perpendicular bisector of
# the chord AA' -- which is exactly the altitude from C onto AB. So its foot M is
# the midpoint of A and A': A' is the mirror image of A, it "bounces".
# In the right triangle C-M-B, BM = a*cos(B) by the plain definition of cosine,
# and BA' = 2*BM - c. Substituting:
#   c*(2a*cos B - c) = a^2 - b^2   =>   b^2 = a^2 + c^2 - 2ac*cos(B).
#
# The a^2, b^2, c^2 appear as a *power of a point* and the cosine as a ratio in a
# genuine right triangle: the only "operation" performed is a reflection.
#
# The actual frame is 9 x 16 units (x in [-4.5, 4.5], y in [-8, 8]).
# Safe area: |x| <= 3.8 and |y| <= 5.6.

SAFE_WIDTH = 7.2

# The construction is designed in "paper" coordinates and then scaled/lifted so
# the whole circle fits above the equation board.
SCALE = 1.2
LIFT = 0.1


def at(x, y):
    """Map a paper coordinate to its place inside the vertical frame."""
    return np.array([x * SCALE, y * SCALE + LIFT, 0.0])


def fit_to_safe_width(mobject):
    """Shrink a mobject so it never crosses the horizontal safe margins."""
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def make_label(tex, font_size, color, with_background=True):
    """Create a MathTex label with an optional background for line crossings."""
    label = MathTex(tex, font_size=font_size, color=color)
    if with_background:
        label.add_background_rectangle(color=BG, opacity=0.92, buff=0.06)
    label.set_z_index(12)
    return label


class LawOfCosinesPowerOfPoint(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.14
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.85)
        self.add(watermark)

        TRI_COLOR = ACCENT_PURPLE      # the triangle ABC
        CIRCLE_COLOR = GREY_B          # the auxiliary circle centred at C
        RADIUS_COLOR = ACCENT_MAGENTA  # radius b: C-A, C-P, C-Q
        SECANT_COLOR = ACCENT_YELLOW   # the two secants through B
        COS_COLOR = ACCENT_CYAN        # the right triangle C-M-B and cos B
        # Orange is reserved for the single "operation" of the whole proof: the
        # reflection of A onto A'.
        MIRROR_COLOR = "#FF8A00"

        # ------------------------------------------------------------- geometry
        # Sides a = 4.0, b = 2.8, c = 4.6. Two conditions shape the drawing:
        # a > b keeps the near intersection P between B and C, and AM = 1.4 keeps
        # the chord AA' long enough for the reflection to be visible.
        A = at(-2.3, -0.7)
        B = at(2.3, -0.7)
        C = at(-0.887, 1.717)

        b = np.linalg.norm(C - A)          # radius of the circle
        a = np.linalg.norm(C - B)
        u = (C - B) / a                    # unit vector from B towards C
        P = B + (a - b) * u                # near hit of line BC with the circle
        Q = B + (a + b) * u                # far hit, beyond the centre
        M = np.array([C[0], A[1], 0.0])    # foot of the altitude from C onto AB
        Aprime = 2 * M - A                 # the mirror image of A: it bounces

        def outward(point, origin, distance=0.40):
            direction = point - origin
            return point + direction / np.linalg.norm(direction) * distance

        # ------------------------------------------------------------ hook 0-3s
        title = Tex(r"Ley de Cosenos", font_size=62, color=WHITE)
        title.set_stroke(width=1)
        title.move_to(UP * 6.6)
        fit_to_safe_width(title)

        subtitle = Tex(r"por potencia de un punto", font_size=38,
                       color=ACCENT_YELLOW)
        subtitle.next_to(title, DOWN, buff=0.22)
        fit_to_safe_width(subtitle)

        underline = Line(
            subtitle.get_left() + DOWN * 0.28,
            subtitle.get_right() + DOWN * 0.28,
            stroke_width=4,
        )
        underline.set_color(color=[ACCENT_YELLOW, MIRROR_COLOR, ACCENT_MAGENTA])

        header = VGroup(title, subtitle, underline)
        header.set_z_index(20)

        self.play(Write(title), run_time=0.9)
        self.play(FadeIn(subtitle, shift=UP * 0.2), Create(underline),
                  run_time=0.6)
        self.wait(0.3)

        # ----------------------------------------------------- triangle ABC
        triangle = Polygon(
            A, B, C,
            color=TRI_COLOR, stroke_width=5,
            fill_color=TRI_COLOR, fill_opacity=0.07,
        )
        triangle.set_z_index(4)
        dots = VGroup(*[Dot(point, color=WHITE, radius=0.06)
                        for point in (A, B, C)])
        dots.set_z_index(11)
        centroid = (A + B + C) / 3
        vertex_labels = VGroup(
            make_label("A", 32, WHITE, False).move_to(outward(A, centroid)),
            make_label("B", 32, WHITE, False).move_to(outward(B, centroid)),
            make_label("C", 32, WHITE, False).move_to(outward(C, centroid)),
        )

        self.play(Create(triangle), FadeIn(dots), run_time=0.9)
        self.play(Write(vertex_labels), run_time=0.5)

        side_a = make_label("a", 32, SECANT_COLOR).move_to(
            (B + C) / 2 + RIGHT * 0.42
        )
        side_b = make_label("b", 32, RADIUS_COLOR).move_to(
            (C + A) / 2 + LEFT * 0.42
        )
        # "c" stays centred under the whole segment AB -- that is the side it
        # names, and pushing it aside (e.g. towards A'-B) reads as if it only
        # measured that shorter piece. Purple was unreadable against the dark
        # triangle fill, so "c" gets the mirror orange instead.
        side_c = make_label("c", 32, MIRROR_COLOR).move_to(
            (A + B) / 2 + DOWN * 0.42
        )
        self.play(Write(VGroup(side_a, side_b, side_c)), run_time=0.7)
        self.wait(0.4)

        # ------------------------------------- the circle centred at C, radius b
        circle = Circle(radius=b, color=CIRCLE_COLOR, stroke_width=3)
        circle.move_to(C)
        circle.set_stroke(opacity=0.75)

        radius_CA = Line(C, A, color=RADIUS_COLOR, stroke_width=6)
        radius_CA.set_z_index(5)

        self.play(Create(radius_CA), run_time=0.5)
        # The circle passes through A by construction (radius = CA).
        self.play(Create(circle), run_time=1.0)
        self.bring_to_back(circle)
        self.wait(0.3)

        # ---------------------------------------------- first secant: line B-C
        secant_BQ = Line(B, Q, color=SECANT_COLOR, stroke_width=5)
        secant_BQ.set_z_index(3)
        dot_P = Dot(P, color=SECANT_COLOR, radius=0.07).set_z_index(11)
        dot_Q = Dot(Q, color=SECANT_COLOR, radius=0.07).set_z_index(11)
        label_P = make_label("P", 28, SECANT_COLOR, False).move_to(
            P + np.array([0.34, -0.24, 0.0])
        )
        label_Q = make_label("Q", 28, SECANT_COLOR, False).move_to(
            outward(Q, C, 0.5)
        )

        self.play(Create(secant_BQ), run_time=0.8)
        self.play(FadeIn(dot_P, scale=2), FadeIn(dot_Q, scale=2),
                  Write(VGroup(label_P, label_Q)), run_time=0.6)

        # Both hits sit one radius away from C, so BP = a - b and BQ = a + b.
        radius_CP = DashedLine(C, P, color=RADIUS_COLOR, stroke_width=4,
                               dash_length=0.12)
        radius_CQ = DashedLine(C, Q, color=RADIUS_COLOR, stroke_width=4,
                               dash_length=0.12)
        self.play(Create(radius_CP), Create(radius_CQ), run_time=0.7)

        # P-B is a short stretch, so a midpoint brace would collide with the P
        # dot; each label instead sits well clear of both endpoints, offset
        # perpendicular to the secant.
        near_normal = rotate_vector(u, -PI / 2)
        far_normal = rotate_vector(u, PI / 2)

        tick_near = Line(
            (P + B) / 2 - near_normal * 0.1, (P + B) / 2 + near_normal * 0.1,
            color=SECANT_COLOR, stroke_width=4,
        )
        brace_near_label = make_label("a-b", 26, SECANT_COLOR).move_to(
            (P + B) / 2 + near_normal * 0.55
        )
        tick_far = Line(
            (B + Q) / 2 - far_normal * 0.1, (B + Q) / 2 + far_normal * 0.1,
            color=SECANT_COLOR, stroke_width=4,
        )
        brace_far_label = make_label("a+b", 26, SECANT_COLOR).move_to(
            (B + Q) / 2 + far_normal * 0.55
        )
        self.play(Create(tick_near), Write(brace_near_label), run_time=0.6)
        self.play(Create(tick_far), Write(brace_far_label), run_time=0.6)
        self.wait(0.4)

        # --------------------------------------------------- power of the point
        board_top = -3.1
        board_gap = 1.25

        eq1 = MathTex(r"\mathrm{pot}(B)", r"=", r"(a-b)(a+b)", r"=",
                      r"a^2-b^2", font_size=42)
        eq1[0].set_color(WHITE)
        eq1[2].set_color(SECANT_COLOR)
        eq1[4].set_color(SECANT_COLOR)
        eq1.set_stroke(width=1)
        eq1.set_z_index(21)
        eq1.move_to(np.array([0.0, board_top, 0.0]))
        fit_to_safe_width(eq1)

        self.play(
            TransformFromCopy(VGroup(brace_near_label[1], brace_far_label[1]),
                              eq1[2]),
            run_time=0.9,
        )
        self.play(Write(VGroup(eq1[0], eq1[1])), run_time=0.6)
        self.play(Write(VGroup(eq1[3], eq1[4])), run_time=0.6)
        self.wait(0.5)

        # The braces have done their job; keep the picture breathable.
        self.play(
            FadeOut(VGroup(tick_near, brace_near_label,
                           tick_far, brace_far_label,
                           radius_CP, radius_CQ)),
            run_time=0.5,
        )

        # --------------------------------- second secant: line B-A, hitting A'
        secant_BA = Line(B, A, color=SECANT_COLOR, stroke_width=5)
        secant_BA.set_z_index(3)
        self.play(Create(secant_BA), run_time=0.7)

        dot_Aprime = Dot(Aprime, color=MIRROR_COLOR, radius=0.07)
        dot_Aprime.set_z_index(11)
        # Dropped a little below the "c" row (which sits centred under all of
        # AB) so the two never compete for the same strip of the frame; the
        # a*cos B brace further down is shifted clear of this row too.
        label_Aprime = make_label("A'", 28, MIRROR_COLOR, False).move_to(
            Aprime + DOWN * 0.62 + LEFT * 0.15
        )
        radius_CAprime = Line(C, Aprime, color=RADIUS_COLOR, stroke_width=6)
        radius_CAprime.set_z_index(5)
        label_b2 = make_label("b", 28, RADIUS_COLOR).move_to(
            (C + Aprime) / 2 + RIGHT * 0.34
        )

        # The line enters at A and comes back out at A': it bounces off the
        # circle.
        self.play(FadeIn(dot_Aprime, scale=2), Write(label_Aprime),
                  run_time=0.6)
        self.play(Create(radius_CAprime), Write(label_b2), run_time=0.7)
        self.wait(0.3)

        eq2 = MathTex(r"\mathrm{pot}(B)", r"=", r"(BA)(BA')", r"=",
                      r"c \cdot BA'", font_size=42)
        eq2[0].set_color(WHITE)
        eq2[2].set_color(SECANT_COLOR)
        eq2[4].set_color(MIRROR_COLOR)
        eq2.set_stroke(width=1)
        eq2.set_z_index(21)
        eq2.move_to(np.array([0.0, board_top - board_gap, 0.0]))
        fit_to_safe_width(eq2)
        self.play(Write(eq2), run_time=1.1)
        self.wait(0.4)

        # The power does not care which line was used, so the two values agree.
        eq3 = MathTex(r"c \cdot BA'", r"=", r"a^2-b^2", font_size=44)
        eq3[0].set_color(MIRROR_COLOR)
        eq3[2].set_color(SECANT_COLOR)
        eq3.set_stroke(width=1)
        eq3.set_z_index(21)
        eq3.move_to(np.array([0.0, board_top - 2 * board_gap, 0.0]))

        self.play(
            TransformFromCopy(eq2[4], eq3[0]),
            TransformFromCopy(eq1[4], eq3[2]),
            Write(eq3[1]),
            run_time=1.1,
        )
        box3 = SurroundingRectangle(eq3, buff=0.16, corner_radius=0.1)
        box3.set_stroke(width=3, color=SECANT_COLOR)
        box3.set_z_index(20)
        self.play(Create(box3), run_time=0.6)
        self.wait(0.6)

        # The board is cleared: only the equality that matters stays, moved up.
        self.play(
            FadeOut(VGroup(eq1, eq2)),
            VGroup(eq3, box3).animate.move_to(np.array([0.0, board_top, 0.0])),
            run_time=0.9,
        )
        self.wait(0.3)

        # ------------------------------------- the altitude is the mirror axis
        altitude = Line(C, M, color=COS_COLOR, stroke_width=5)
        altitude.set_z_index(6)
        dot_M = Dot(M, color=COS_COLOR, radius=0.07).set_z_index(11)
        label_M = make_label("M", 28, COS_COLOR, False).move_to(
            M + DOWN * 0.34 + LEFT * 0.3
        )
        right_angle = RightAngle(
            Line(M, A), Line(M, C), length=0.24, color=COS_COLOR, stroke_width=4,
        )
        right_angle.set_z_index(7)

        self.play(Create(altitude), FadeIn(dot_M), Write(label_M),
                  Create(right_angle), run_time=0.9)

        # C is a radius away from both A and A', so the altitude is also the
        # perpendicular bisector of the chord AA': M is its midpoint.
        chord = Line(A, Aprime, color=MIRROR_COLOR, stroke_width=7)
        chord.set_z_index(8)
        self.play(Create(chord), run_time=0.6)
        self.play(
            Indicate(radius_CA, color=RADIUS_COLOR, scale_factor=1.0),
            Indicate(radius_CAprime, color=RADIUS_COLOR, scale_factor=1.0),
            run_time=0.9,
        )

        # The reflection itself: A bounces across M onto A'.
        bouncing = Dot(A, color=MIRROR_COLOR, radius=0.09).set_z_index(13)
        self.add(bouncing)
        self.play(bouncing.animate.move_to(Aprime), run_time=0.8)
        self.play(Flash(Aprime, color=MIRROR_COLOR, line_length=0.22),
                  run_time=0.6)
        self.remove(bouncing)

        halves = VGroup(
            BraceBetweenPoints(A, M, direction=UP, color=MIRROR_COLOR),
            BraceBetweenPoints(M, Aprime, direction=UP, color=MIRROR_COLOR),
        )
        halves_labels = VGroup(
            make_label("m", 26, MIRROR_COLOR).next_to(halves[0], UP, buff=0.05),
            make_label("m", 26, MIRROR_COLOR).next_to(halves[1], UP, buff=0.05),
        )
        self.play(GrowFromCenter(halves), Write(halves_labels), run_time=0.7)
        self.wait(0.4)

        # -------------------------------------------- cos B in a right triangle
        right_tri = Polygon(
            C, M, B, stroke_width=0, fill_color=COS_COLOR, fill_opacity=0.10,
        )
        right_tri.set_z_index(1)
        # M lies on ray B->A, so the angle at B between B->M and B->C is the
        # same interior angle B of the triangle -- force the non-reflex side.
        angle_B = Angle(Line(B, M), Line(B, C), radius=0.55, color=COS_COLOR,
                        stroke_width=4, other_angle=True)
        angle_B.set_z_index(9)
        label_B_angle = make_label("B", 26, COS_COLOR, False).move_to(
            Angle(Line(B, M), Line(B, C), radius=0.85,
                 other_angle=True).point_from_proportion(0.5)
        )
        self.play(FadeIn(right_tri), Create(angle_B), Write(label_B_angle),
                  run_time=0.8)

        brace_BM = BraceBetweenPoints(M, B, direction=DOWN, color=COS_COLOR)
        brace_BM.shift(DOWN * 0.95)
        label_BM = make_label(r"a\cos B", 28, COS_COLOR).next_to(
            brace_BM, DOWN, buff=0.15
        )
        self.play(GrowFromCenter(brace_BM), Write(label_BM), run_time=0.8)
        self.wait(0.5)

        # ------------------------------------------------------- the substitution
        # Where BA' = 2a*cos(B) - c actually comes from: AM = c - a*cos(B), so
        # m = AM = c - a*cos(B). Then A' sits between M and B (it is the
        # reflection of A across M), so BA' = BM - MA' = a*cos(B) - m -- and
        # substituting m collapses that into the single line below.
        row_y = board_top - board_gap

        m_eq = MathTex(r"m", r"=", r"c", r"-", r"a\cos B", font_size=40)
        m_eq[0].set_color(MIRROR_COLOR)
        m_eq[2].set_color(MIRROR_COLOR)
        m_eq[4].set_color(COS_COLOR)
        m_eq.set_stroke(width=1)
        m_eq.set_z_index(21)
        m_eq.move_to(np.array([0.0, row_y, 0.0]))
        fit_to_safe_width(m_eq)
        self.play(
            TransformFromCopy(halves_labels[1][1], m_eq[0]),
            run_time=0.7,
        )
        self.play(
            Write(m_eq[1]),
            TransformFromCopy(side_c[1], m_eq[2]),
            run_time=0.6,
        )
        self.play(
            Write(m_eq[3]),
            TransformFromCopy(label_BM[1], m_eq[4]),
            run_time=0.7,
        )
        self.wait(0.5)

        # A' lies between M and B, so BA' is the leftover after MA' = m is
        # removed from BM -- a subtraction, not an addition.
        ba_eq = MathTex(r"BA'", r"=", r"a\cos B", r"-", r"m", font_size=40)
        ba_eq[0].set_color(MIRROR_COLOR)
        ba_eq[2].set_color(COS_COLOR)
        ba_eq[4].set_color(MIRROR_COLOR)
        ba_eq.set_stroke(width=1)
        ba_eq.set_z_index(21)
        ba_eq.move_to(np.array([0.0, row_y - 0.85, 0.0]))
        fit_to_safe_width(ba_eq)
        self.play(
            TransformFromCopy(label_BM[1], ba_eq[2]),
            TransformFromCopy(m_eq[0], ba_eq[4]),
            run_time=0.8,
        )
        self.play(Write(VGroup(ba_eq[0], ba_eq[1], ba_eq[3])), run_time=0.7)
        self.wait(0.5)

        # Substituting m = c - a*cos(B) into BA' = a*cos(B) - m collapses to
        # a single expression in a and c: this is the line eq5 will use.
        eq4 = MathTex(r"BA'", r"=", r"2\,a\cos B", r"-", r"c", font_size=42)
        eq4[0].set_color(MIRROR_COLOR)
        eq4[2].set_color(COS_COLOR)
        eq4[4].set_color(TRI_COLOR)
        eq4.set_stroke(width=1)
        eq4.set_z_index(21)
        eq4.move_to(np.array([0.0, row_y, 0.0]))
        fit_to_safe_width(eq4)
        self.play(
            FadeOut(VGroup(m_eq, ba_eq)),
            FadeIn(eq4),
            run_time=0.9,
        )
        self.wait(0.5)

        eq5 = MathTex(r"c\,(2a\cos B - c)", r"=", r"a^2-b^2", font_size=42)
        eq5[0].set_color(COS_COLOR)
        eq5[2].set_color(SECANT_COLOR)
        eq5.set_stroke(width=1)
        eq5.set_z_index(21)
        eq5.move_to(np.array([0.0, board_top - 2 * board_gap, 0.0]))
        fit_to_safe_width(eq5)
        self.play(
            TransformFromCopy(eq4, eq5[0]),
            TransformFromCopy(eq3[2], eq5[2]),
            Write(eq5[1]),
            run_time=1.2,
        )
        self.wait(0.6)

        eq6 = MathTex(r"2ac\cos B", r"=", r"a^2-b^2+c^2", font_size=42)
        eq6[0].set_color(COS_COLOR)
        eq6[2].set_color(SECANT_COLOR)
        eq6.set_stroke(width=1)
        eq6.set_z_index(21)
        eq6.move_to(np.array([0.0, board_top - 3 * board_gap, 0.0]))
        fit_to_safe_width(eq6)
        self.play(TransformMatchingShapes(eq5.copy(), eq6), run_time=1.2)
        self.wait(0.6)

        # ------------------------------------------------------------ conclusion
        self.play(FadeOut(VGroup(eq3, box3, eq4, eq5)), run_time=0.6)

        formula = MathTex(r"b^2", r"=", r"a^2+c^2", r"-", r"2ac\cos B",
                          font_size=50)
        formula[0].set_color(RADIUS_COLOR)
        formula[2].set_color(SECANT_COLOR)
        formula[4].set_color(COS_COLOR)
        formula.set_stroke(width=1)
        formula.set_z_index(21)
        formula.move_to(np.array([0.0, board_top - board_gap, 0.0]))
        fit_to_safe_width(formula)

        self.play(TransformMatchingShapes(VGroup(eq6), formula), run_time=1.4)
        result_box = SurroundingRectangle(formula, buff=0.2, corner_radius=0.12)
        result_box.set_stroke(width=4, color=[RADIUS_COLOR, MIRROR_COLOR,
                                             ACCENT_YELLOW])
        result_box.set_z_index(20)
        self.play(Create(result_box), run_time=0.7)
        self.wait(0.6)

        # The whole proof in one line: a power of a point plus a reflection.
        closing = Tex(r"potencia de un punto $+$ un reflejo",
                      font_size=34, color=ACCENT_YELLOW)
        closing.set_z_index(21)
        closing.next_to(result_box, DOWN, buff=0.5)
        fit_to_safe_width(closing)
        self.play(FadeIn(closing, shift=UP * 0.2), run_time=0.7)
        self.wait(1.8)

        animate_End(scene=self)
