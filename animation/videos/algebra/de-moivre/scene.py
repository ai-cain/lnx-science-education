from manim import *
from lnx import *

# visual-derivation | algebra | intermediate
# De Moivre: (cos t + i sen t)^n = cos nt + i sen nt.
#
# The single idea: on the unit circumference, multiplying by z is rotating by t.
# So raising z to the n-th power is repeating that same rotation n times, and the
# resulting angle is simply n*t. Nothing else is needed.
#
# The scene uses t = 40 deg so that z, z^2, z^3, z^4 land at 40, 80, 120 and 160
# degrees: four distinct points, all in the upper half, none overlapping.
#
# The frame is 9 x 16 units (x in [-4.5, 4.5], y in [-8, 8]).
# Safe area: |x| <= 3.8 and |y| <= 5.6.

SAFE_WIDTH = 7.2

# Radius of the unit circumference in scene units, and the center of the diagram.
# The center sits slightly below the frame center so the header stack (title plus
# formula) and the bottom caption both keep visible air.
RADIUS = 2.15
CENTER = np.array([0.0, -0.35, 0.0])

THETA = 40 * DEGREES

CIRCLE_COLOR = ACCENT_CYAN     # the unit circumference itself
VECTOR_COLOR = ACCENT_MAGENTA  # the current power of z
ARC_COLOR = ACCENT_YELLOW      # the accumulated angle
GHOST_COLOR = ACCENT_PURPLE    # the powers already visited


def fit_to_safe_width(mobject):
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def on_circle(angle, radius=RADIUS):
    """Scene point at a given angle on the unit circumference."""
    return CENTER + radius * np.array([np.cos(angle), np.sin(angle), 0.0])


class DeMoivre(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.14
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.85)
        self.add(watermark)

        def radius_line(angle, color, width=7):
            arrow = Arrow(
                CENTER, on_circle(angle), buff=0,
                color=color, stroke_width=width,
                max_tip_length_to_length_ratio=0.16,
            )
            arrow.set_z_index(6)
            return arrow

        def angle_arc(angle, radius_ratio=0.32):
            arc = Arc(
                radius=RADIUS * radius_ratio, start_angle=0, angle=angle,
                arc_center=CENTER, color=ARC_COLOR, stroke_width=6,
            )
            arc.set_z_index(5)
            return arc

        def power_label(tex, angle, color, font_size=32):
            """Label placed OUTSIDE the circumference, radially away from center."""
            label = MathTex(tex, font_size=font_size, color=color)
            label.add_background_rectangle(color=BG, opacity=0.9, buff=0.06)
            label.move_to(on_circle(angle, RADIUS + 0.55))
            label.set_z_index(15)
            return label

        # ---------------------------------------------------------- hook 0-2 s
        # Before any words: the arrow spins four steps around the circumference
        # and leaves a fan of powers behind. That fan IS the whole video.
        circle = Circle(radius=RADIUS, color=CIRCLE_COLOR, stroke_width=5)
        circle.move_to(CENTER)
        circle.set_z_index(2)

        axes = VGroup(
            Line(CENTER + LEFT * (RADIUS + 0.9), CENTER + RIGHT * (RADIUS + 0.9)),
            Line(CENTER + DOWN * (RADIUS + 0.9), CENTER + UP * (RADIUS + 0.9)),
        )
        axes.set_stroke(color=GREY_B, width=2, opacity=0.5)
        axes.set_z_index(1)

        title = Tex(r"F\'ormula de De Moivre", font_size=54, color=WHITE)
        title.set_stroke(width=1)
        title.set_z_index(20)
        title.move_to(UP * 5.3)
        fit_to_safe_width(title)

        underline = Line(
            title.get_left() + DOWN * 0.28,
            title.get_right() + DOWN * 0.28,
            stroke_width=4,
        )
        underline.set_color(color=[ACCENT_CYAN, ACCENT_MAGENTA])
        underline.set_z_index(20)

        self.add(axes, circle)
        spinner = radius_line(THETA, VECTOR_COLOR)
        self.play(Write(title), GrowArrow(spinner), run_time=0.7)
        self.play(Create(underline), run_time=0.3)

        # Four quick rotations of exactly THETA, dropping a ghost each time.
        ghosts = VGroup()
        for step in range(2, 5):
            ghost = radius_line((step - 1) * THETA, GHOST_COLOR, width=4)
            ghost.set_z_index(4)
            ghosts.add(ghost)
            self.add(ghost)
            self.play(
                Rotate(spinner, angle=THETA, about_point=CENTER),
                run_time=0.3,
            )
        self.wait(0.4)

        hook_line = Tex(
            r"elevar a la $n$ es\\repetir el mismo giro",
            font_size=34, color=GREY_A,
        )
        hook_line.set_z_index(20)
        hook_line.move_to(DOWN * 4.75)
        fit_to_safe_width(hook_line)
        self.play(FadeIn(hook_line, shift=UP * 0.15), run_time=0.5)
        self.wait(1.3)

        # ------------------------------------------- beat 1: who is z, exactly
        # Back to a clean circumference to introduce z with its angle t.
        self.play(FadeOut(ghosts), FadeOut(spinner), FadeOut(hook_line), run_time=0.4)

        z_vector = radius_line(THETA, VECTOR_COLOR)
        z_dot = Dot(on_circle(THETA), radius=0.075, color=VECTOR_COLOR)
        z_dot.set_z_index(7)
        theta_arc = angle_arc(THETA)
        theta_label = MathTex(r"\theta", font_size=34, color=ARC_COLOR)
        theta_label.move_to(CENTER + RADIUS * 0.52 * np.array(
            [np.cos(THETA / 2), np.sin(THETA / 2), 0.0]))
        theta_label.set_z_index(15)

        z_def = MathTex(r"z=\cos\theta+i\,\mathrm{sen}\,\theta", font_size=40)
        z_def.set_color(VECTOR_COLOR)
        z_def.set_stroke(width=1)
        z_def.set_z_index(20)
        z_def.move_to(UP * 4.4)
        fit_to_safe_width(z_def)

        radius_note = Tex(r"radio 1: solo importa el \'angulo",
                          font_size=30, color=GREY_A)
        radius_note.set_z_index(20)
        radius_note.move_to(DOWN * 4.75)
        fit_to_safe_width(radius_note)

        self.play(GrowArrow(z_vector), FadeIn(z_dot), run_time=0.5)
        self.play(Create(theta_arc), Write(theta_label), run_time=0.5)
        self.play(Write(z_def), run_time=1.0)
        self.play(FadeIn(radius_note, shift=UP * 0.15), run_time=0.5)
        self.wait(1.5)

        # --------------------------------- beat 2: multiplying by z is rotating
        self.play(FadeOut(radius_note), run_time=0.3)

        rule = Tex(r"multiplicar por $z$ = girar $\theta$",
                   font_size=32, color=WHITE)
        rule.set_z_index(20)
        rule.move_to(DOWN * 4.75)
        fit_to_safe_width(rule)
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.5)

        z_label = power_label(r"z", THETA, VECTOR_COLOR)
        self.play(Write(z_label), run_time=0.5)
        self.wait(1.2)

        # ------------------------- beat 3: z^2, z^3, z^4 one rotation at a time
        # The same arrow keeps turning; every step freezes a purple ghost plus a
        # label OUTSIDE the circumference, so the angles read 2t, 3t, 4t.
        current_arc = theta_arc
        trail = VGroup()
        labels = VGroup(z_label)

        step_texts = {
            2: r"z^{2}=\cos 2\theta+i\,\mathrm{sen}\,2\theta",
            3: r"z^{3}=\cos 3\theta+i\,\mathrm{sen}\,3\theta",
            4: r"z^{4}=\cos 4\theta+i\,\mathrm{sen}\,4\theta",
        }

        for n in range(2, 5):
            ghost = radius_line((n - 1) * THETA, GHOST_COLOR, width=4)
            ghost.set_z_index(4)
            trail.add(ghost)
            self.add(ghost)

            new_arc = angle_arc(n * THETA)
            self.play(
                Rotate(z_vector, angle=THETA, about_point=CENTER),
                z_dot.animate.move_to(on_circle(n * THETA)),
                Transform(current_arc, new_arc),
                theta_label.animate.move_to(
                    CENTER + RADIUS * 0.52 * np.array(
                        [np.cos(n * THETA / 2), np.sin(n * THETA / 2), 0.0])),
                run_time=1.0,
            )

            new_theta_label = MathTex(rf"{n}\theta", font_size=34, color=ARC_COLOR)
            new_theta_label.move_to(theta_label.get_center())
            new_theta_label.set_z_index(15)
            new_label = power_label(rf"z^{{{n}}}", n * THETA, GHOST_COLOR)
            labels.add(new_label)

            new_def = MathTex(step_texts[n], font_size=38)
            new_def.set_color(VECTOR_COLOR)
            new_def.set_stroke(width=1)
            new_def.set_z_index(20)
            new_def.move_to(UP * 4.4)
            fit_to_safe_width(new_def)

            self.play(
                Transform(theta_label, new_theta_label),
                Write(new_label),
                ReplacementTransform(z_def, new_def),
                run_time=0.6,
            )
            z_def = new_def
            self.wait(0.7)

        self.play(FadeOut(rule), run_time=0.3)
        count_note = Tex(r"$n$ giros de $\theta$ dan un \'angulo de $n\theta$",
                         font_size=30, color=ARC_COLOR)
        count_note.set_z_index(20)
        count_note.move_to(DOWN * 4.75)
        fit_to_safe_width(count_note)
        self.play(FadeIn(count_note, shift=UP * 0.15), run_time=0.5)
        self.wait(1.8)

        # --------------------------------------------------- beat 4: the payoff
        self.play(
            FadeOut(VGroup(circle, axes, z_vector, z_dot, current_arc,
                           theta_label, trail, labels)),
            FadeOut(z_def), FadeOut(count_note),
            run_time=0.6,
        )

        formula = MathTex(
            r"\left(\cos\theta+i\,\mathrm{sen}\,\theta\right)^{n}",
            r"=",
            r"\cos n\theta+i\,\mathrm{sen}\,n\theta",
            font_size=40,
        )
        formula[0].set_color(VECTOR_COLOR)
        formula[2].set_color(ARC_COLOR)
        formula.arrange(RIGHT, buff=0.18)
        formula.set_stroke(width=1)
        formula.set_z_index(21)
        formula.move_to(UP * 0.6)
        fit_to_safe_width(formula)

        self.play(Write(formula), run_time=1.4)
        self.wait(0.8)

        result_box = SurroundingRectangle(formula, buff=0.28, corner_radius=0.14)
        result_box.set_stroke(width=4, color=[ACCENT_YELLOW, ACCENT_MAGENTA])
        result_box.set_z_index(20)
        self.play(Create(result_box), run_time=0.6)

        closing = Tex(
            r"de esta sola f\'ormula salen\\\emph{todas} las identidades\\de \'angulo m\'ultiple",
            font_size=34, color=WHITE,
        )
        closing.set_z_index(21)
        closing.next_to(result_box, DOWN, buff=0.7)
        fit_to_safe_width(closing)
        self.play(FadeIn(closing, shift=UP * 0.2), run_time=0.8)
        self.wait(2.2)

        animate_End(scene=self)
