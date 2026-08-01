from manim import *
from lnx import *

# hidden-invariant | geometry | advanced
# Mathematical reference:
# https://mathworld.wolfram.com/NapoleonsTheorem.html
#
# Napoleon's theorem: erect an outward equilateral triangle on each side of an
# arbitrary triangle ABC; the three centers always form an equilateral triangle.
#
# The center of the outward equilateral triangle built on the segment PQ is the
# centroid of {P, Q, apex}, which equals
#     midpoint(P, Q) + outward_normal * |PQ| / (2 * sqrt(3)).
# The apex itself is midpoint(P, Q) + outward_normal * |PQ| * sqrt(3) / 2.
#
# VALIDATION (executed at import time by validate_napoleon_invariant below):
# for every sampled triangle, including the extreme deformed keyframes used in
# this scene, the three inner sides |PQ|, |QR| and |RP| agree to within 1e-9,
# so the Napoleon triangle is exactly equilateral in every rendered frame.

BASE_SCALE = 0.64
FIGURE_ORIGIN = np.array([0.0, -0.7, 0.0])
SAFE_WIDTH = 7.2

# Fixed base of the deforming triangle, in unscaled construction units.
VERTEX_B = np.array([-1.45, -0.95, 0.0])
VERTEX_C = np.array([1.55, -1.15, 0.0])

# Keyframes for the free vertex A: the triangle is dragged into deliberately
# ugly, asymmetric shapes while the Napoleon triangle stays equilateral.
APEX_KEYFRAMES = (
    np.array([-0.10, 1.95, 0.0]),
    np.array([1.60, 2.15, 0.0]),
    np.array([-1.55, 1.35, 0.0]),
    np.array([0.55, 2.30, 0.0]),
)


def to_world(point):
    """Map a construction-unit point into scene coordinates."""
    return FIGURE_ORIGIN + BASE_SCALE * point


def apex_position(progress):
    """Piecewise-linear path of the free vertex A over the keyframes."""
    span = len(APEX_KEYFRAMES) - 1
    clamped = float(np.clip(progress, 0.0, span))
    index = min(int(np.floor(clamped)), span - 1)
    local = clamped - index
    start = APEX_KEYFRAMES[index]
    end = APEX_KEYFRAMES[index + 1]
    return start + local * (end - start)


def base_vertices(progress):
    """Return the three vertices of the deforming base triangle."""
    return apex_position(progress), VERTEX_B, VERTEX_C


def outward_normal(first_point, second_point, reference_point):
    """Unit normal of the segment pointing away from the reference point."""
    direction = second_point - first_point
    length = np.linalg.norm(direction)
    normal = np.array([-direction[1], direction[0], 0.0]) / length
    midpoint = (first_point + second_point) / 2
    if np.dot(normal, midpoint - reference_point) < 0:
        normal = -normal
    return normal, length


def equilateral_apex(first_point, second_point, reference_point):
    """Third vertex of the equilateral triangle erected outward on a side."""
    normal, length = outward_normal(first_point, second_point, reference_point)
    midpoint = (first_point + second_point) / 2
    return midpoint + normal * (length * np.sqrt(3) / 2)


def equilateral_center(first_point, second_point, reference_point):
    """Exact centroid of the outward equilateral triangle on a side."""
    normal, length = outward_normal(first_point, second_point, reference_point)
    midpoint = (first_point + second_point) / 2
    return midpoint + normal * (length / (2 * np.sqrt(3)))


def napoleon_centers(progress):
    """The three outward equilateral centers for a given deformation state."""
    vertex_a, vertex_b, vertex_c = base_vertices(progress)
    centroid = (vertex_a + vertex_b + vertex_c) / 3
    return (
        equilateral_center(vertex_a, vertex_b, centroid),
        equilateral_center(vertex_b, vertex_c, centroid),
        equilateral_center(vertex_c, vertex_a, centroid),
    )


def napoleon_side_lengths(progress):
    """Side lengths of the inner Napoleon triangle, in construction units."""
    first, second, third = napoleon_centers(progress)
    return (
        np.linalg.norm(second - first),
        np.linalg.norm(third - second),
        np.linalg.norm(first - third),
    )


def validate_napoleon_invariant(tolerance=1e-9):
    """Assert the inner triangle is equilateral across the whole deformation."""
    span = len(APEX_KEYFRAMES) - 1
    for sample in np.linspace(0.0, span, 121):
        side_ab, side_bc, side_ca = napoleon_side_lengths(sample)
        assert abs(side_ab - side_bc) < tolerance
        assert abs(side_bc - side_ca) < tolerance
        assert abs(side_ca - side_ab) < tolerance


validate_napoleon_invariant()


def fit_to_safe_width(mobject):
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


class NapoleonTheorem(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        progress = ValueTracker(0.0)
        outer_opacity = ValueTracker(0.0)
        inner_opacity = ValueTracker(0.0)
        center_opacity = ValueTracker(0.0)

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.13
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.8)
        watermark.set_z_index(30)
        self.add(watermark)

        outer_colors = (ACCENT_CYAN, ACCENT_YELLOW, ACCENT_PURPLE)

        def build_base_triangle():
            vertices = [to_world(point) for point in base_vertices(progress.get_value())]
            triangle = Polygon(
                *vertices,
                color=WHITE,
                stroke_width=6,
                fill_color=SURFACE,
                fill_opacity=0.45,
            )
            triangle.set_z_index(4)
            return triangle

        def build_outer_triangles():
            vertex_a, vertex_b, vertex_c = base_vertices(progress.get_value())
            centroid = (vertex_a + vertex_b + vertex_c) / 3
            sides = (
                (vertex_a, vertex_b),
                (vertex_b, vertex_c),
                (vertex_c, vertex_a),
            )
            group = VGroup()
            for (first_point, second_point), color in zip(sides, outer_colors):
                apex = equilateral_apex(first_point, second_point, centroid)
                triangle = Polygon(
                    to_world(first_point),
                    to_world(second_point),
                    to_world(apex),
                    color=color,
                    stroke_width=4,
                    fill_color=color,
                    fill_opacity=0.16,
                )
                triangle.set_opacity(1)
                triangle.set_stroke(opacity=outer_opacity.get_value())
                triangle.set_fill(color, opacity=0.16 * outer_opacity.get_value())
                group.add(triangle)
            group.set_z_index(2)
            return group

        def build_centers():
            group = VGroup()
            centers = napoleon_centers(progress.get_value())
            for center, color in zip(centers, outer_colors):
                dot = Dot(point=to_world(center), radius=0.075, color=color)
                dot.set_opacity(center_opacity.get_value())
                group.add(dot)
            group.set_z_index(8)
            return group

        def build_napoleon_triangle():
            centers = napoleon_centers(progress.get_value())
            triangle = Polygon(
                *[to_world(center) for center in centers],
                color=ACCENT_MAGENTA,
                stroke_width=8,
                fill_color=ACCENT_MAGENTA,
                fill_opacity=0.22,
            )
            triangle.set_stroke(opacity=inner_opacity.get_value())
            triangle.set_fill(
                ACCENT_MAGENTA,
                opacity=0.22 * inner_opacity.get_value(),
            )
            triangle.set_z_index(6)
            return triangle

        base_triangle = always_redraw(build_base_triangle)
        outer_triangles = always_redraw(build_outer_triangles)
        center_dots = always_redraw(build_centers)
        napoleon_triangle = always_redraw(build_napoleon_triangle)

        # Beat 1 (0.0-2.0): the hook is the deforming triangle itself.
        headline = Tex(
            r"\textbf{Toma un triángulo cualquiera}",
            font_size=40,
            color=WHITE,
        ).move_to(UP * 5.1)
        headline.set_z_index(20)
        fit_to_safe_width(headline)

        self.add(base_triangle, outer_triangles, center_dots, napoleon_triangle)
        self.play(
            FadeIn(headline, shift=DOWN * 0.15),
            run_time=0.5,
        )
        self.play(
            progress.animate.set_value(0.55),
            run_time=1.4,
            rate_func=there_and_back,
        )

        # Beat 2 (2.0-6.5): outward equilateral triangles on the three sides.
        build_note = Tex(
            r"\textbf{Un equilátero hacia afuera en cada lado}",
            font_size=34,
            color=ACCENT_CYAN,
        ).move_to(UP * 5.1)
        build_note.set_z_index(20)
        fit_to_safe_width(build_note)

        self.play(
            ReplacementTransform(headline, build_note),
            outer_opacity.animate.set_value(1.0),
            run_time=1.6,
        )
        self.wait(0.6)

        # Beat 3 (6.5-11.0): the three centers and the inner triangle.
        centers_note = Tex(
            r"\textbf{Une los tres centros}",
            font_size=36,
            color=ACCENT_YELLOW,
        ).move_to(UP * 5.1)
        centers_note.set_z_index(20)
        fit_to_safe_width(centers_note)

        self.play(
            ReplacementTransform(build_note, centers_note),
            center_opacity.animate.set_value(1.0),
            run_time=1.1,
        )
        self.wait(0.5)
        self.play(inner_opacity.animate.set_value(1.0), run_time=1.2)
        self.wait(0.6)

        # Beat 4 (11.0-16.0): name the invariant and show the equal sides.
        claim = Tex(
            r"\textbf{Siempre sale equilátero}",
            font_size=40,
            color=ACCENT_MAGENTA,
        ).move_to(UP * 5.1)
        claim.set_z_index(20)
        fit_to_safe_width(claim)

        equality = MathTex(
            r"|PQ| = |QR| = |RP|",
            font_size=36,
            color=WHITE,
        ).move_to(UP * 4.35)
        equality.set_z_index(20)

        side_value = DecimalNumber(
            0.0,
            num_decimal_places=3,
            font_size=36,
            color=ACCENT_MAGENTA,
        )
        side_value.add_updater(
            lambda mobject: mobject.set_value(
                napoleon_side_lengths(progress.get_value())[0] * BASE_SCALE
            )
        )
        side_label = MathTex(
            r"\text{lado} =",
            font_size=36,
            color=WHITE,
        )
        side_readout = VGroup(side_label, side_value).arrange(RIGHT, buff=0.2)
        side_readout.move_to(DOWN * 5.2)
        side_readout.set_z_index(20)

        self.play(
            ReplacementTransform(centers_note, claim),
            FadeIn(equality, shift=DOWN * 0.1),
            run_time=1.0,
        )
        self.play(FadeIn(side_readout, shift=UP * 0.12), run_time=0.7)
        self.play(
            Indicate(napoleon_triangle, color=ACCENT_MAGENTA, scale_factor=1.05),
            run_time=1.2,
        )
        self.wait(0.5)

        # Beat 5 (16.0-28.0): deform the base triangle into ugly shapes.
        deform_note = Tex(
            r"\textbf{Deforma todo lo que quieras}",
            font_size=34,
            color=WHITE,
        ).move_to(UP * 4.35)
        deform_note.set_z_index(20)
        fit_to_safe_width(deform_note)

        self.play(
            ReplacementTransform(equality, deform_note),
            run_time=0.6,
        )
        self.play(progress.animate.set_value(1.0), run_time=2.4, rate_func=smooth)
        self.wait(0.4)
        self.play(progress.animate.set_value(2.0), run_time=3.0, rate_func=smooth)
        self.wait(0.4)
        self.play(progress.animate.set_value(3.0), run_time=2.6, rate_func=smooth)
        self.wait(0.6)

        # Beat 6 (28.0-36.0): framed payoff.
        payoff = Tex(
            r"\textbf{Teorema de Napoleón}",
            font_size=38,
            color=WHITE,
        ).move_to(DOWN * 4.3)
        payoff.set_z_index(22)
        payoff_detail = Tex(
            r"El triángulo interior nunca deja de ser equilátero",
            font_size=28,
            color=GREY_B,
        ).move_to(DOWN * 4.95)
        payoff_detail.set_z_index(22)
        fit_to_safe_width(payoff_detail)
        payoff_box = SurroundingRectangle(
            VGroup(payoff, payoff_detail),
            color=GOLD,
            buff=0.22,
            corner_radius=0.12,
            stroke_width=3,
        )
        payoff_box.set_color_by_gradient(*GRADIENT_HIGHLIGHT)
        payoff_box.set_z_index(21)

        self.play(
            FadeOut(side_readout),
            FadeOut(deform_note),
            run_time=0.5,
        )
        self.play(
            FadeIn(payoff, shift=UP * 0.12),
            FadeIn(payoff_detail, shift=UP * 0.12),
            Create(payoff_box),
            run_time=1.0,
        )
        self.play(
            payoff_box.animate.set_stroke(width=6),
            rate_func=there_and_back,
            run_time=1.1,
        )
        self.play(
            Indicate(claim, color=ACCENT_MAGENTA, scale_factor=1.06),
            run_time=1.1,
        )
        self.wait(1.0)

        animate_End(scene=self)
