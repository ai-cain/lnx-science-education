from manim import *
from lnx import *

# proof-without-words | trigonometry | basic
# Double angle:  sin 2t = 2 sin t cos t.
#
# One isosceles triangle, two equal legs of length 1 and apex angle 2t, whose
# area is computed twice:
#   (1) with the SAS formula      A = (1/2) * 1 * 1 * sin(2t)
#   (2) by splitting it with the axis of symmetry, which produces two congruent
#       right triangles of legs sin(t) and cos(t):
#                                 A = (1/2) * (2 sin t) * (cos t)
# The factor 2 is not algebra: it is the mirrored half of the base. That is the
# whole point of the video.
#
# The actual frame is 9 x 16 units (x in [-4.5, 4.5], y in [-8, 8]).
# Safe area: |x| <= 3.8 and |y| <= 5.6.

SAFE_WIDTH = 7.2


def fit_to_safe_width(mobject):
    """Shrink a mobject so it never crosses the horizontal safe margins."""
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def make_label(tex, font_size, color, with_background=False):
    """Create a MathTex label that always sits above the geometry."""
    label = MathTex(tex, font_size=font_size, color=color)
    if with_background:
        label.add_background_rectangle(color=BG, opacity=0.92, buff=0.06)
    label.set_z_index(12)
    return label


class DoubleAngle(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        LEG_COLOR = ACCENT_CYAN        # the two equal legs, length 1
        BASE_COLOR = ACCENT_MAGENTA    # the base, length 2 sin t
        HEIGHT_COLOR = ACCENT_YELLOW   # the axis of symmetry, length cos t
        ANGLE_COLOR = ACCENT_PURPLE    # apex angles
        AUX_COLOR = GREY_B

        # ------------------------------------------------------------- geometry
        # Legs of length L drawn at +-theta from the vertical axis, so the apex
        # angle is exactly 2*theta and the figure is symmetric about x = 0.
        theta_deg = 34.0
        theta = theta_deg * DEGREES
        L = 2.55

        apex = np.array([0.0, 4.55, 0.0])
        half_base = L * np.sin(theta)
        height = L * np.cos(theta)
        left = apex + np.array([-half_base, -height, 0.0])
        right = apex + np.array([half_base, -height, 0.0])
        foot = apex + np.array([0.0, -height, 0.0])

        # ------------------------------------------------------------ hook 0-2s
        # The mirror move IS the hook: half a triangle flips over the axis and
        # the apex angle becomes 2*theta in front of the viewer.
        axis = DashedLine(
            apex + UP * 0.35, foot + DOWN * 0.45,
            color=AUX_COLOR, stroke_width=2.5, dash_length=0.12,
        )
        axis.set_stroke(opacity=0.55)

        half_triangle = Polygon(
            apex, foot, right,
            color=LEG_COLOR, stroke_width=5,
            fill_color=LEG_COLOR, fill_opacity=0.10,
        )
        mirrored = half_triangle.copy()
        mirrored.set_color(LEG_COLOR)

        self.play(Create(axis), run_time=0.35)
        self.play(Create(half_triangle), run_time=0.75)
        self.play(
            mirrored.animate.flip(axis=UP, about_point=foot),
            run_time=0.85,
        )

        triangle = Polygon(
            apex, left, right,
            color=LEG_COLOR, stroke_width=5,
            fill_color=LEG_COLOR, fill_opacity=0.10,
        )
        self.play(
            FadeIn(triangle),
            FadeOut(half_triangle),
            FadeOut(mirrored),
            run_time=0.35,
        )
        self.remove(half_triangle, mirrored)

        vertex_dots = VGroup(
            Dot(apex, color=WHITE, radius=0.06),
            Dot(left, color=WHITE, radius=0.06),
            Dot(right, color=WHITE, radius=0.06),
        )
        vertex_dots.set_z_index(8)
        self.add(vertex_dots)

        # ------------------------------------------------- setup: legs and 2t
        leg_left = Line(apex, left, color=LEG_COLOR, stroke_width=6)
        leg_right = Line(apex, right, color=LEG_COLOR, stroke_width=6)
        VGroup(leg_left, leg_right).set_z_index(5)

        # Length labels live outside the figure, never on top of a stroke.
        label_leg_left = make_label("1", 34, LEG_COLOR).move_to(
            (apex + left) / 2 + np.array([-0.52, 0.16, 0.0])
        )
        label_leg_right = make_label("1", 34, LEG_COLOR).move_to(
            (apex + right) / 2 + np.array([0.52, 0.16, 0.0])
        )

        apex_angle = Angle(
            Line(apex, left), Line(apex, right),
            radius=0.72, color=ANGLE_COLOR, stroke_width=5,
        )
        apex_angle.set_z_index(6)
        apex_label = make_label(r"2\theta", 34, ANGLE_COLOR)
        apex_label.move_to(apex + DOWN * 1.12)

        self.play(
            Create(leg_left), Create(leg_right),
            Write(label_leg_left), Write(label_leg_right),
            run_time=0.8,
        )
        self.play(Create(apex_angle), Write(apex_label), run_time=0.7)
        self.wait(0.4)

        # -------------------------------------------- area, first reading (SAS)
        stack_x = 0.0
        area_sas = MathTex(
            r"A=\tfrac{1}{2}\,\operatorname{sen}2\theta",
            font_size=44, color=WHITE,
        )
        area_sas.set_z_index(20)
        area_sas.move_to(np.array([stack_x, 1.35, 0.0]))
        fit_to_safe_width(area_sas)

        note_sas = Tex(
            r"dos lados $1$ y el \'angulo entre ellos",
            font_size=30, color=AUX_COLOR,
        )
        note_sas.set_z_index(20)
        note_sas.next_to(area_sas, DOWN, buff=0.24)
        fit_to_safe_width(note_sas)

        self.play(Write(area_sas), run_time=0.8)
        self.play(FadeIn(note_sas, shift=UP * 0.15), run_time=0.5)
        self.wait(0.6)

        # ------------------------------------ split it: the axis of symmetry
        altitude = Line(apex, foot, color=HEIGHT_COLOR, stroke_width=6)
        altitude.set_z_index(5)
        base = Line(left, right, color=BASE_COLOR, stroke_width=6)
        base.set_z_index(5)

        right_angle = RightAngle(
            Line(foot, right), Line(foot, apex),
            length=0.28, color=WHITE, stroke_width=4,
        )
        right_angle.set_z_index(9)

        half_left = Angle(
            Line(apex, left), Line(apex, foot),
            radius=0.98, color=ANGLE_COLOR, stroke_width=4,
        )
        half_right = Angle(
            Line(apex, foot), Line(apex, right),
            radius=0.98, color=ANGLE_COLOR, stroke_width=4,
        )
        VGroup(half_left, half_right).set_z_index(6)
        label_half_left = make_label(r"\theta", 30, ANGLE_COLOR).move_to(
            apex + np.array([-0.52, -1.28, 0.0])
        )
        label_half_right = make_label(r"\theta", 30, ANGLE_COLOR).move_to(
            apex + np.array([0.52, -1.28, 0.0])
        )

        self.play(
            Create(base),
            FadeOut(note_sas),
            run_time=0.6,
        )
        self.play(Create(altitude), Create(right_angle), run_time=0.7)
        self.play(
            FadeOut(apex_angle), FadeOut(apex_label),
            Create(half_left), Create(half_right),
            Write(label_half_left), Write(label_half_right),
            run_time=0.8,
        )
        self.wait(0.3)

        # -------------------------------------- the two legs of the half triangle
        # Height measured with a dimension line placed to the right of the
        # figure, so no length label ever lands on the drawing.
        dim_x = right[0] + 0.95
        dim_line = DoubleArrow(
            np.array([dim_x, foot[1], 0.0]),
            np.array([dim_x, apex[1], 0.0]),
            buff=0, stroke_width=3, color=HEIGHT_COLOR,
            tip_length=0.16,
        )
        dim_tick_top = DashedLine(
            apex, np.array([dim_x + 0.2, apex[1], 0.0]),
            color=AUX_COLOR, stroke_width=2, dash_length=0.1,
        )
        dim_tick_bottom = DashedLine(
            right, np.array([dim_x + 0.2, foot[1], 0.0]),
            color=AUX_COLOR, stroke_width=2, dash_length=0.1,
        )
        VGroup(dim_tick_top, dim_tick_bottom).set_stroke(opacity=0.5)
        label_height = make_label(r"\cos\theta", 32, HEIGHT_COLOR)
        label_height.next_to(dim_line, RIGHT, buff=0.16)

        brace_half = Brace(
            Line(foot, right), direction=DOWN, buff=0.18, color=BASE_COLOR,
        )
        label_half = make_label(r"\operatorname{sen}\theta", 32, BASE_COLOR)
        label_half.next_to(brace_half, DOWN, buff=0.12)

        self.play(
            Create(dim_tick_top), Create(dim_tick_bottom),
            Create(dim_line), Write(label_height),
            run_time=0.8,
        )
        self.play(GrowFromCenter(brace_half), Write(label_half), run_time=0.7)
        self.wait(0.5)

        # ------------------------------------ where the factor 2 really comes from
        # The mirrored half of the base is highlighted so the doubling is seen,
        # not asserted.
        mirror_flash = Line(foot, left, color=BASE_COLOR, stroke_width=9)
        mirror_flash.set_z_index(7)
        self.play(
            Create(mirror_flash),
            Flash(foot, color=BASE_COLOR, line_length=0.2, num_lines=10),
            run_time=0.7,
        )

        brace_base = Brace(base, direction=DOWN, buff=0.18, color=BASE_COLOR)
        label_base = make_label(
            r"2\operatorname{sen}\theta", 34, BASE_COLOR
        )
        label_base.next_to(brace_base, DOWN, buff=0.12)

        self.play(
            ReplacementTransform(brace_half, brace_base),
            ReplacementTransform(label_half, label_base),
            run_time=0.8,
        )
        self.play(FadeOut(mirror_flash), run_time=0.3)
        self.wait(0.4)

        # ------------------------------------- area, second reading (base-height)
        area_bh = MathTex(
            r"A=\tfrac{1}{2}\,(2\operatorname{sen}\theta)(\cos\theta)",
            font_size=42, color=WHITE,
        )
        area_bh.set_z_index(20)
        area_bh.move_to(np.array([stack_x, 0.05, 0.0]))
        fit_to_safe_width(area_bh)

        self.play(
            TransformFromCopy(label_base, area_bh),
            run_time=0.9,
        )
        self.wait(0.5)

        # ------------------------------------------------------------- payoff
        # Both readings measure the same triangle, so they are equal.
        result = MathTex(
            r"\operatorname{sen}2\theta", r"=",
            r"2\operatorname{sen}\theta\cos\theta",
            font_size=48,
        )
        result[0].set_color(ACCENT_CYAN)
        result[2].set_color(BASE_COLOR)
        result.set_stroke(width=1)
        result.set_z_index(21)
        result.move_to(np.array([stack_x, -1.75, 0.0]))
        fit_to_safe_width(result)

        self.play(
            TransformMatchingShapes(VGroup(area_sas, area_bh).copy(), result),
            run_time=1.2,
        )
        self.play(FadeOut(area_sas), FadeOut(area_bh), run_time=0.4)

        result_box = SurroundingRectangle(result, buff=0.22, corner_radius=0.14)
        result_box.set_stroke(width=4, color=[ACCENT_YELLOW, ACCENT_MAGENTA])
        result_box.set_z_index(20)
        self.play(Create(result_box), run_time=0.6)

        closing = Tex(
            r"el $2$ es la mitad reflejada de la base",
            font_size=32, color=ACCENT_YELLOW,
        )
        closing.set_z_index(21)
        closing.next_to(result_box, DOWN, buff=0.42)
        fit_to_safe_width(closing)
        self.play(Write(closing), run_time=0.8)
        self.wait(1.6)

        animate_End(scene=self)
