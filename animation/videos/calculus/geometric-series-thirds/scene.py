from manim import *
from lnx import *

# geometric-limit | calculus | basic


class GeometricSeriesThirds(Scene):
    """Visual proof that 1/3 + 1/9 + 1/27 + ... = 1/2.

    A triangle is split by dividing its base into three equal segments and
    joining every division point to the apex. The three sub-triangles share the
    same height, so each one holds exactly one third of the area of the piece
    being split. At every step the left third is painted (the series term), the
    middle third is painted with a second color (its mirror partner) and the
    right third is split again. Painted and partner pieces are equal one to one,
    so together they exhaust the whole triangle and each family owns half of it.
    """

    # Base triangle geometry, kept inside the vertical safe area.
    APEX = np.array([0.0, 2.55, 0.0])
    BASE_LEFT = np.array([-3.4, -2.05, 0.0])
    BASE_RIGHT = np.array([3.4, -2.05, 0.0])
    STEPS = 6

    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        # --- Beat 1 (0.0-2.2s): hook, the question on screen immediately ---
        hook = MathTex(
            r"\frac{1}{3}+\frac{1}{9}+\frac{1}{27}+\cdots = \; ?",
            font_size=52,
        ).move_to(UP * 0.6)
        hook.set_color_by_gradient(*GRADIENT_HIGHLIGHT)
        hook.z_index = 5
        self.play(Write(hook), run_time=1.2)
        self.play(Indicate(hook, scale_factor=1.12, color=ACCENT_YELLOW), run_time=0.9)

        # --- Beat 2 (2.2-6.0s): the triangle appears, hook moves to the top ---
        title = Text("Infinitos sumandos, un área exacta", font_size=30)
        title.set_color(ACCENT_CYAN)
        title.move_to(UP * 5.0)
        title.z_index = 5

        outline = Polygon(
            self.APEX, self.BASE_LEFT, self.BASE_RIGHT
        ).set_stroke(color=GRADIENT_MAIN, width=5)
        outline.z_index = 3

        area_label = MathTex(r"\text{Área} = 1", font_size=34)
        area_label.set_color(ACCENT_YELLOW)
        area_label.next_to(outline, DOWN, buff=0.35)
        area_label.z_index = 5

        self.play(
            hook.animate.scale(0.66).move_to(UP * 4.15),
            run_time=0.8,
        )
        self.play(Write(title), run_time=0.6)
        self.play(Create(outline), run_time=1.1)
        self.play(FadeIn(area_label, shift=UP * 0.2), run_time=0.6)

        # --- Beat 3 (6.0-26.0s): six iterations of the three-way split ---
        running_sum = MathTex(r"S = \frac{1}{3}", font_size=40)
        running_sum.set_color(ACCENT_CYAN)
        running_sum.move_to(DOWN * 3.5)
        running_sum.z_index = 5

        painted_pieces = VGroup()
        partner_pieces = VGroup()
        cut_lines = VGroup()
        term_labels = VGroup()

        left_x = self.BASE_LEFT[0]
        right_x = self.BASE_RIGHT[0]
        base_y = self.BASE_LEFT[1]

        for step in range(self.STEPS):
            third = (right_x - left_x) / 3.0
            p0 = np.array([left_x, base_y, 0.0])
            p1 = np.array([left_x + third, base_y, 0.0])
            p2 = np.array([left_x + 2.0 * third, base_y, 0.0])

            painted = Polygon(self.APEX, p0, p1)
            painted.set_stroke(width=0).set_fill(ACCENT_CYAN, opacity=0.85)
            painted.z_index = 1

            partner = Polygon(self.APEX, p1, p2)
            partner.set_stroke(width=0).set_fill(ACCENT_MAGENTA, opacity=0.6)
            partner.z_index = 1

            cuts = VGroup(
                Line(self.APEX, p1).set_stroke(color=SURFACE, width=2.5),
                Line(self.APEX, p2).set_stroke(color=SURFACE, width=2.5),
            )
            cuts.z_index = 2

            painted_pieces.add(painted)
            partner_pieces.add(partner)
            cut_lines.add(cuts)

            if step == 0:
                self.play(Create(cuts), run_time=0.7)
                self.play(
                    FadeIn(painted),
                    FadeIn(partner),
                    run_time=0.7,
                )
                first_label = MathTex(r"\frac{1}{3}", font_size=34)
                first_label.set_color(BG)
                first_label.move_to(painted.get_center_of_mass())
                first_label.z_index = 6
                term_labels.add(first_label)
                self.play(FadeIn(first_label), Write(running_sum), run_time=0.8)
            else:
                # Each new term is one third of the piece that was left over.
                exponent = step + 1
                new_sum = MathTex(
                    "S = "
                    + " + ".join(
                        rf"\frac{{1}}{{{3 ** k}}}" for k in range(1, exponent + 1)
                    ),
                    font_size=40 if exponent <= 4 else 34,
                )
                new_sum.set_color(ACCENT_CYAN)
                new_sum.move_to(DOWN * 3.5)
                new_sum.z_index = 5

                anims = [
                    Create(cuts),
                    FadeIn(painted),
                    FadeIn(partner),
                    Transform(running_sum, new_sum),
                ]
                if step == 1:
                    second_label = MathTex(r"\frac{1}{9}", font_size=28)
                    second_label.set_color(ACCENT_YELLOW)
                    second_label.next_to(painted.get_center_of_mass(), UR, buff=0.55)
                    leader = Line(
                        second_label.get_corner(DL),
                        painted.get_center_of_mass(),
                    ).set_stroke(color=ACCENT_YELLOW, width=2)
                    second_label.z_index = 6
                    leader.z_index = 6
                    term_labels.add(second_label, leader)
                    anims += [FadeIn(second_label), Create(leader)]

                self.play(*anims, run_time=0.95 if step <= 2 else 0.7)

            left_x = left_x + 2.0 * third

        self.wait(0.4)

        # --- Beat 4 (26.0-34.0s): the pairing argument ---
        self.play(FadeOut(term_labels), FadeOut(area_label), run_time=0.5)

        pairing = Text("Cada pieza tiene su gemela", font_size=30)
        pairing.set_color(ACCENT_MAGENTA)
        pairing.move_to(DOWN * 4.55)
        pairing.z_index = 5
        self.play(Write(pairing), run_time=0.7)

        self.play(
            painted_pieces.animate.set_fill(opacity=1.0),
            partner_pieces.animate.set_fill(opacity=1.0),
            run_time=0.7,
        )
        self.play(
            Flash(
                painted_pieces[0].get_center_of_mass(),
                color=ACCENT_YELLOW,
                line_length=0.25,
                num_lines=10,
            ),
            Flash(
                partner_pieces[0].get_center_of_mass(),
                color=ACCENT_YELLOW,
                line_length=0.25,
                num_lines=10,
            ),
            run_time=0.9,
        )
        self.play(
            FadeOut(cut_lines),
            run_time=0.6,
        )

        halves_note = Text("Mitad y mitad", font_size=32)
        halves_note.set_color(ACCENT_YELLOW)
        halves_note.move_to(DOWN * 4.55)
        halves_note.z_index = 5
        self.play(FadeTransform(pairing, halves_note), run_time=0.7)
        self.wait(0.5)

        # --- Beat 5 (34.0-41.0s): framed payoff ---
        payoff = MathTex(
            r"\sum_{n=1}^{\infty}\frac{1}{3^{n}}=\frac{1}{2}",
            font_size=54,
        )
        payoff.set_color_by_gradient(*GRADIENT_HIGHLIGHT)
        payoff.move_to(DOWN * 3.7)
        payoff.z_index = 6

        self.play(
            FadeOut(hook),
            FadeOut(halves_note),
            Transform(running_sum, payoff),
            run_time=1.0,
        )

        frame = SurroundingRectangle(payoff, buff=0.22, corner_radius=0.12)
        frame.set_stroke(color=GRADIENT_HIGHLIGHT, width=4)
        frame.z_index = 6
        self.play(Create(frame), run_time=0.6)
        self.wait(1.4)

        animate_End(scene=self)
