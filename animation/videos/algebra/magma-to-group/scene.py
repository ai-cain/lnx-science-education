from manim import *
from lnx import *

# unexpected-extension | algebra (group theory) | advanced
# A "group" is usually taught as THE basic algebraic structure. This video
# extends that expectation outward: a group is actually the rarest, most
# constrained point in a much larger hierarchy that starts from the magma
# (a set with a closed binary operation and nothing else) and adds one axiom
# at a time: associativity, identity, inverses.
#
# The actual frame is 9 x 16 units (x in [-4.5, 4.5], y in [-8, 8]).
# Safe area: |y| <= 5.6 and |x| <= 3.8.

SAFE_WIDTH = 7.2


def fit_to_safe_width(mobject):
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def make_label(text, font_size, color, with_background=True):
    label = Tex(text, font_size=font_size, color=color)
    if with_background:
        label.add_background_rectangle(color=BG, opacity=0.92, buff=0.06)
    label.set_z_index(10)
    return label


class MagmaToGroup(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.14
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.85)
        self.add(watermark)

        MAGMA_COLOR = GREY_B
        SEMIGROUP_COLOR = ACCENT_CYAN
        MONOID_COLOR = ACCENT_PURPLE
        GROUP_COLOR = ACCENT_YELLOW

        # ---------------------------------------------------------- hook 0-2s
        hook = Tex(r"Un GRUPO es solo la punta del iceberg", font_size=40)
        hook.set_color(GROUP_COLOR)
        hook.set_stroke(width=1)
        hook.move_to(UP * 5.3)
        fit_to_safe_width(hook)
        self.play(Write(hook), run_time=1.0)
        self.wait(0.6)

        # ------------------------------------------------- pyramid skeleton
        base_y = -3.1
        top_y = 4.6
        half_width_base = 3.1
        apex = np.array([0, top_y, 0])
        base_left = np.array([-half_width_base, base_y, 0])
        base_right = np.array([half_width_base, base_y, 0])

        pyramid = Polygon(
            apex, base_left, base_right,
            stroke_color=WHITE, stroke_width=2, fill_opacity=0,
        )
        self.play(FadeOut(hook), run_time=0.4)
        self.play(Create(pyramid), run_time=0.9)

        def band_at(t_bottom, t_top, color, opacity):
            """A trapezoid slice of the pyramid between two height ratios (0 = base, 1 = apex)."""
            left_bottom = base_left + (apex - base_left) * t_bottom
            right_bottom = base_right + (apex - base_right) * t_bottom
            left_top = base_left + (apex - base_left) * t_top
            right_top = base_right + (apex - base_right) * t_top
            return Polygon(
                left_bottom, right_bottom, right_top, left_top,
                fill_color=color, fill_opacity=opacity, stroke_width=0,
            )

        def band_center(t_bottom, t_top):
            """Center of a band, on the pyramid axis so labels stay inside."""
            t_mid = (t_bottom + t_top) / 2
            return np.array([0, base_y + (top_y - base_y) * t_mid, 0])

        # --------------------------------------------------------- magma 2-10s
        magma_band = band_at(0.0, 0.28, MAGMA_COLOR, 0.28)
        magma_label = make_label(r"MAGMA", 30, MAGMA_COLOR)
        magma_label.move_to(band_center(0.0, 0.28))
        magma_desc = MathTex(
            r"(S,\ast) \;:\; a \ast b \in S", font_size=30, color=MAGMA_COLOR
        )
        magma_desc.next_to(pyramid, DOWN, buff=0.35)
        fit_to_safe_width(magma_desc)

        self.play(FadeIn(magma_band), Write(magma_label), run_time=0.8)
        self.play(Write(magma_desc), run_time=1.0)
        self.wait(1.6)

        # One concrete witness per level keeps the hierarchy from feeling formal.
        def make_example(tex, color):
            example = MathTex(tex, font_size=26, color=color)
            example.next_to(magma_desc, DOWN, buff=0.30)
            return fit_to_safe_width(example)

        magma_example = make_example(
            r"\text{ej: } (\mathbb{Z}, -) \quad \text{resta: no asociativa}",
            MAGMA_COLOR,
        )
        self.play(FadeIn(magma_example, shift=UP * 0.15), run_time=0.8)
        self.wait(2.4)

        # ---------------------------------------------------- semigroup 10-20s
        semigroup_band = band_at(0.28, 0.52, SEMIGROUP_COLOR, 0.30)
        semigroup_label = make_label(r"SEMIGRUPO", 26, SEMIGROUP_COLOR)
        semigroup_label.move_to(band_center(0.28, 0.52))

        new_desc = MathTex(
            r"+\ (a\ast b)\ast c = a\ast(b\ast c)", font_size=28, color=SEMIGROUP_COLOR
        )
        new_desc.move_to(magma_desc.get_center())
        fit_to_safe_width(new_desc)

        self.play(FadeIn(semigroup_band), Write(semigroup_label), run_time=0.8)
        self.play(TransformMatchingTex(magma_desc, new_desc), run_time=1.0)
        self.wait(1.6)

        semigroup_example = make_example(
            r"\text{ej: } (\mathbb{Z}^{+}, +) \quad \text{sin neutro}",
            SEMIGROUP_COLOR,
        )
        self.play(
            FadeTransform(magma_example, semigroup_example), run_time=0.8
        )
        self.wait(2.4)
        prev_desc = new_desc
        prev_example = semigroup_example

        # -------------------------------------------------------- monoid 20-30s
        monoid_band = band_at(0.52, 0.74, MONOID_COLOR, 0.32)
        monoid_label = make_label(r"MONOIDE", 24, MONOID_COLOR)
        monoid_label.move_to(band_center(0.52, 0.74))

        monoid_desc = MathTex(
            r"+\ \exists\, e: e\ast a = a\ast e = a", font_size=26, color=MONOID_COLOR
        )
        monoid_desc.move_to(prev_desc.get_center())
        fit_to_safe_width(monoid_desc)

        self.play(FadeIn(monoid_band), Write(monoid_label), run_time=0.8)
        self.play(TransformMatchingTex(prev_desc, monoid_desc), run_time=1.0)
        self.wait(1.6)

        monoid_example = make_example(
            r"\text{ej: } (\mathbb{N}, +) \quad \text{sin inversos}",
            MONOID_COLOR,
        )
        self.play(FadeTransform(prev_example, monoid_example), run_time=0.8)
        self.wait(2.4)
        prev_desc = monoid_desc
        prev_example = monoid_example

        # --------------------------------------------------------- group 30-45s
        group_band = band_at(0.74, 1.0, GROUP_COLOR, 0.42)
        group_label = make_label(r"GRUPO", 24, GROUP_COLOR)
        group_label.move_to(band_center(0.74, 0.96))

        group_desc = MathTex(
            r"+\ \exists\, a^{-1}: a\ast a^{-1} = e", font_size=26, color=GROUP_COLOR
        )
        group_desc.move_to(prev_desc.get_center())
        fit_to_safe_width(group_desc)

        self.play(FadeIn(group_band), Write(group_label), run_time=0.8)
        self.play(TransformMatchingTex(prev_desc, group_desc), run_time=1.0)
        self.wait(1.6)

        group_example = make_example(
            r"\text{ej: } (\mathbb{Z}, +) \quad \text{grupo completo}",
            GROUP_COLOR,
        )
        self.play(FadeTransform(prev_example, group_example), run_time=0.8)
        self.wait(2.4)

        apex_dot = Dot(apex, color=GROUP_COLOR, radius=0.07)
        self.play(Indicate(apex_dot, scale_factor=3.0), FadeIn(apex_dot), run_time=0.9)
        self.wait(1.2)

        # ------------------------------------------------------- reveal 45-60s
        self.play(FadeOut(group_desc), FadeOut(group_example), run_time=0.5)

        hierarchy = MathTex(
            r"\text{Magma} \supset \text{Semigrupo} \supset \text{Monoide} \supset \text{Grupo}",
            font_size=24,
        )
        hierarchy[0][0:6].set_color(MAGMA_COLOR)
        hierarchy.set_z_index(20)
        hierarchy.move_to(DOWN * 5.15)
        fit_to_safe_width(hierarchy)
        self.play(Write(hierarchy), run_time=1.6)
        self.wait(2.4)

        self.play(
            Indicate(magma_band, scale_factor=1.0, color=MAGMA_COLOR),
            run_time=1.2,
        )
        self.wait(1.6)

        # ------------------------------------------------------- payoff 60-75s
        self.play(FadeOut(hierarchy), run_time=0.4)

        payoff = Tex(
            r"Casi cualquier conjunto\\con una operaci\'{o}n ya es un magma.\\El grupo es el caso extremo.",
            font_size=32,
        )
        payoff.set_color(WHITE)
        payoff.set_stroke(width=1)
        payoff.move_to(DOWN * 5.2)
        fit_to_safe_width(payoff)
        self.play(Write(payoff), run_time=1.6)
        self.wait(2.6)

        result_box = SurroundingRectangle(group_label, buff=0.22, corner_radius=0.12)
        result_box.set_stroke(width=4, color=[YELLOW, ORANGE])
        result_box.set_z_index(20)
        self.play(Create(result_box), run_time=0.8)
        self.wait(2.2)

        animate_End(scene=self)
