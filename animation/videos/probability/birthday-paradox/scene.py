from manim import *
from lnx import *

# paradoja | probabilidad | basico
# La paradoja del cumpleanos: con solo 23 personas ya hay mas de 50%.
#
# El frame real es 9 x 16 unidades (x en [-4.5, 4.5], y en [-8, 8]).
# Zona segura: |y| <= 5.6 y |x| <= 3.8 (la UI de TikTok tapa los extremos).


SAFE_W = 7.2


def fit(m):
    """Evita que un mobject se salga de la zona segura horizontal."""
    if m.width > SAFE_W:
        m.scale_to_fit_width(SAFE_W)
    return m


class ParadojaCumpleanos(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        N = 23

        # ---------------------------------------------------------- hook 0.0-2.5
        hook_1 = Tex(r"23 personas", font_size=82)
        hook_1.set_color_by_gradient(*GRADIENT_HIGHLIGHT)
        hook_1.set_stroke(width=1.2)
        hook_2 = Tex(r"¿Dos cumplen años\\ el mismo día?", font_size=48, color=WHITE)
        fit(hook_1)
        fit(hook_2)
        VGroup(hook_1, hook_2).arrange(DOWN, buff=0.7).move_to(UP * 3.0)

        self.play(Write(hook_1), run_time=0.5)
        self.play(FadeIn(hook_2, shift=UP * 0.4), run_time=0.5)

        intuicion = Tex(r"casi imposible", font_size=60, color=ACCENT_CYAN)
        intuicion.move_to(DOWN * 1.2)
        fit(intuicion)
        self.play(Write(intuicion), run_time=0.6)
        self.wait(0.9)

        # ------------------------------------------------- intuicion fallida 2.5-10
        cuenta_mala = MathTex(
            r"\frac{23}{365}", r"\approx", r"6\%",
            font_size=82, color=ACCENT_CYAN,
        ).move_to(DOWN * 1.2)
        fit(cuenta_mala)
        self.play(ReplacementTransform(intuicion, cuenta_mala), run_time=0.9)
        self.wait(1.0)

        tacha = Cross(cuenta_mala, stroke_width=10, color=RED_B)
        self.play(Create(tacha), run_time=0.6)
        self.wait(0.5)

        mal = Tex(r"Estás contando mal.", font_size=51, color=RED_B)
        fit(mal)
        mal.next_to(cuenta_mala, DOWN, buff=1.0)
        self.play(FadeIn(mal, shift=UP * 0.4), run_time=0.5)
        self.wait(1.4)

        self.play(
            FadeOut(VGroup(cuenta_mala, tacha, mal)),
            FadeOut(hook_2),
            hook_1.animate.scale(0.55).move_to(UP * 5.2),
            run_time=0.7,
        )

        # ------------------------------------------------------ el giro 10-24
        titulo = Tex(r"No cuentes personas:\\ cuenta parejas",
                     font_size=53, color=ACCENT_YELLOW)
        fit(titulo)
        titulo.move_to(UP * 3.9)
        self.play(Write(titulo), run_time=0.9)

        radio = 2.4
        centro = UP * 0.2
        puntos = [
            centro + radio * np.array(
                [np.cos(TAU * i / N + PI / 2), np.sin(TAU * i / N + PI / 2), 0.0]
            )
            for i in range(N)
        ]
        dots = VGroup(*[Dot(p, radius=0.11, color=ACCENT_YELLOW) for p in puntos])

        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.06),
            run_time=1.6,
        )
        self.wait(0.4)

        lineas = VGroup(*[
            Line(puntos[i], puntos[j], stroke_width=1.4,
                 color=ACCENT_CYAN, stroke_opacity=0.5)
            for i in range(N) for j in range(i + 1, N)
        ])
        lineas.set_z_index(-1)

        self.play(
            LaggedStart(*[Create(l) for l in lineas], lag_ratio=0.005),
            run_time=3.2,
        )
        self.wait(0.5)

        parejas = MathTex(
            r"\binom{23}{2}", r"=", r"253", r"\text{ parejas}",
            font_size=63,
        )
        parejas[2].set_color(ACCENT_YELLOW)
        fit(parejas)
        parejas.move_to(DOWN * 4.1)
        self.play(Write(parejas), run_time=1.0)
        self.play(Indicate(parejas[2], color=ACCENT_YELLOW, scale_factor=1.3), run_time=0.8)
        self.wait(0.8)

        # cada pareja es una oportunidad de coincidir
        par = Line(puntos[3], puntos[14], stroke_width=9, color=RED_B)
        self.play(
            dots[3].animate.set_color(RED_B).scale(1.8),
            dots[14].animate.set_color(RED_B).scale(1.8),
            Create(par),
            run_time=0.8,
        )
        oportunidad = Tex(r"253 oportunidades de coincidir",
                          font_size=39, color=WHITE)
        fit(oportunidad)
        oportunidad.move_to(DOWN * 5.0)
        self.play(
            parejas.animate.shift(UP * 0.35),
            FadeIn(oportunidad, shift=UP * 0.3),
            run_time=0.5,
        )
        self.wait(1.4)

        # ------------------------------------------------------ calculo 24-36
        self.play(
            FadeOut(lineas),
            FadeOut(dots),
            FadeOut(par),
            FadeOut(titulo),
            FadeOut(oportunidad),
            parejas.animate.scale(0.8).move_to(UP * 3.2),
            run_time=0.8,
        )

        etiqueta = Tex(r"Que \emph{nadie} coincida:", font_size=48, color=WHITE)
        fit(etiqueta)
        etiqueta.move_to(UP * 1.4)
        self.play(FadeIn(etiqueta, shift=UP * 0.3), run_time=0.5)

        prod = MathTex(
            r"\frac{365}{365}\cdot\frac{364}{365}\cdots\frac{343}{365}",
            font_size=58, color=ACCENT_CYAN,
        )
        fit(prod)
        prod.move_to(DOWN * 0.3)
        self.play(Write(prod), run_time=1.4)
        self.wait(1.0)

        aprox = MathTex(r"\approx", r"49{,}3\%", font_size=75, color=ACCENT_CYAN)
        fit(aprox)
        aprox.next_to(prod, DOWN, buff=1.0)
        self.play(Write(aprox), run_time=0.8)
        self.play(Indicate(aprox[1], color=ACCENT_CYAN, scale_factor=1.2), run_time=0.7)
        self.wait(1.2)

        # ------------------------------------------------------ payoff 36-45
        self.play(
            FadeOut(VGroup(etiqueta, prod, parejas)),
            aprox.animate.move_to(UP * 2.8),
            run_time=0.7,
        )

        final = MathTex(r"100\% - 49{,}3\%", r"=", r"50{,}7\%", font_size=63)
        final[2].set_color_by_gradient(*GRADIENT_HIGHLIGHT)
        final[2].set_stroke(width=1.2)
        final.scale_to_fit_width(6.4)  # deja aire para la caja de destaque
        final.move_to(DOWN * 0.2)
        self.play(Write(final), run_time=1.2)

        caja = SurroundingRectangle(final[2], buff=0.14, corner_radius=0.12)
        caja.set_stroke(width=5, color=[YELLOW, ORANGE])
        self.play(Create(caja), run_time=0.7)
        self.play(Indicate(final[2], color=ACCENT_YELLOW, scale_factor=1.2), run_time=0.8)
        self.wait(1.2)

        remate = Tex(r"Con 70 personas: 99,9\%", font_size=49, color=ACCENT_YELLOW)
        fit(remate)
        remate.move_to(DOWN * 3.4)
        self.play(FadeIn(remate, shift=UP * 0.4), run_time=0.6)
        self.wait(1.8)

        animate_End(scene=self)
