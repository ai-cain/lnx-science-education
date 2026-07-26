from manim import *
from lnx import *

# dos-caminos-mismo-resultado - calculo - avanzado
# El producto de Euler: sumar sobre TODOS los enteros o multiplicar
# sobre SOLO los primos da exactamente el mismo numero.

# Frame real: 9.0 x 16.0 -> x en [-4.5, 4.5], y en [-8.0, 8.0]
MAX_W = 7.4          # ancho util (zona segura |x| <= 3.7)
TOP = 5.0            # limite de zona segura superior
BOT = -5.0           # limite de zona segura inferior


def fit(mob, width=MAX_W, height=None):
    """Reduce el mobject si se sale de la caja segura."""
    factor = 1.0
    if mob.width > width:
        factor = width / mob.width
    if height is not None and mob.height * factor > height:
        factor = height / mob.height
    if factor < 1.0:
        mob.scale(factor)
    return mob


class ProductoDeEuler(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        self.hook()
        self.camino_suma()
        self.camino_primos()
        self.por_que_coinciden()
        self.payoff()

        animate_End(scene=self)

    # ------------------------------------------------------------ 0.0-9.0 hook
    def hook(self):
        suma = fit(MathTex(
            r"1+\tfrac{1}{4}+\tfrac{1}{9}+\tfrac{1}{16}+\cdots",
            font_size=80, color=ACCENT_CYAN,
        ))
        suma.set_stroke(width=1.4).move_to(UP * 3.3)

        vs = MathTex("=", font_size=104, color=WHITE).move_to(UP * 1.2)

        prod = fit(MathTex(
            r"\frac{1}{1-\frac{1}{4}}\cdot",
            r"\frac{1}{1-\frac{1}{9}}\cdot",
            r"\frac{1}{1-\frac{1}{25}}\cdots",
            font_size=68,
        ))
        prod.set_color(ACCENT_YELLOW).set_stroke(width=1.2).move_to(DOWN * 1.2)

        pregunta = fit(Tex(
            r"¿Todos los enteros \\ o s\'olo los primos?",
            font_size=72, color=WHITE,
        )).move_to(DOWN * 4.2)

        self.play(Write(suma), run_time=0.8)
        self.play(Write(vs), run_time=0.3)
        self.play(Write(prod), run_time=1.6)
        self.play(Indicate(suma, color=ACCENT_MAGENTA, scale_factor=1.08),
                  run_time=1.2)
        self.play(Indicate(prod, color=ACCENT_MAGENTA, scale_factor=1.08),
                  run_time=1.2)
        self.play(FadeIn(pregunta, shift=UP * 0.3), run_time=0.6)
        self.wait(1.2)
        self.play(Indicate(vs, color=ACCENT_MAGENTA, scale_factor=1.8),
                  run_time=1.0)
        self.wait(1.0)

        self.play(
            FadeOut(suma), FadeOut(vs), FadeOut(prod), FadeOut(pregunta),
            run_time=0.6,
        )

    # ------------------------------------------------------- 9.0-22.0 camino A
    def camino_suma(self):
        titulo = fit(Tex(r"Camino 1: sumar \emph{todos}", font_size=76,
                         color=ACCENT_CYAN)).move_to(UP * TOP)
        self.play(FadeIn(titulo, shift=DOWN * 0.3), run_time=0.6)

        zeta = fit(MathTex(
            r"\zeta(s)", "=", r"\sum_{n=1}^{\infty}\frac{1}{n^{s}}",
            font_size=96,
        ))
        zeta[0].set_color(ACCENT_YELLOW)
        zeta.set_stroke(width=1.4).move_to(UP * 2.4)
        self.play(Write(zeta), run_time=1.4)
        self.wait(1.0)

        expand = fit(MathTex(
            r"\frac{1}{1^{s}}+\frac{1}{2^{s}}+\frac{1}{3^{s}}"
            r"+\frac{1}{4^{s}}+\frac{1}{5^{s}}+\cdots",
            font_size=72, color=ACCENT_CYAN,
        )).move_to(DOWN * 0.4)
        self.play(TransformFromCopy(zeta[2], expand), run_time=1.5)
        self.wait(0.8)

        nota = fit(Tex(r"Cada entero aparece una vez", font_size=64,
                       color=WHITE)).move_to(DOWN * 3.0)
        self.play(FadeIn(nota, shift=UP * 0.25), run_time=0.5)
        self.play(LaggedStart(*[
            Indicate(t, color=ACCENT_MAGENTA, scale_factor=1.25)
            for t in expand[0][:11]
        ], lag_ratio=0.25), run_time=2.2)
        self.wait(1.0)

        self.zeta_ref = zeta
        self.play(
            zeta.animate.scale(0.55).move_to(UP * 5.5),
            FadeOut(titulo), FadeOut(expand), FadeOut(nota),
            run_time=1.0,
        )
        self.wait(0.4)

    # ------------------------------------------------------ 22.0-45.0 camino B
    def camino_primos(self):
        titulo = fit(Tex(r"Camino 2: s\'olo los primos", font_size=72,
                         color=ACCENT_YELLOW)).move_to(UP * 3.9)
        self.play(FadeIn(titulo, shift=DOWN * 0.3), run_time=0.6)

        # Criba de Eratostenes, 2..25, rejilla de 4 columnas
        nums = list(range(2, 26))
        celdas = VGroup(*[
            MathTex(str(n), font_size=62, color=WHITE) for n in nums
        ]).arrange_in_grid(rows=6, cols=4, buff=(0.95, 0.75))
        fit(celdas, 6.6, 4.6).move_to(UP * 0.2)
        self.play(LaggedStart(*[FadeIn(c) for c in celdas],
                              lag_ratio=0.05), run_time=1.8)
        self.wait(0.6)

        primos = {2, 3, 5, 7, 11, 13, 17, 19, 23}
        indice = {n: i for i, n in enumerate(nums)}

        etiqueta = Tex("", font_size=60).move_to(DOWN * 3.6)
        self.add(etiqueta)

        # aceleracion progresiva: cada pasada de la criba es mas rapida
        for p, dur in ((2, 1.5), (3, 1.1), (5, 0.8)):
            nueva = fit(Tex(rf"Fuera los m\'ultiplos de {p}", font_size=60,
                            color=ACCENT_MAGENTA), 7.0).move_to(DOWN * 3.6)
            tachados = [
                celdas[indice[n]] for n in nums
                if n % p == 0 and n != p
            ]
            if not tachados:
                continue
            self.play(
                Transform(etiqueta, nueva),
                celdas[indice[p]].animate.set_color(ACCENT_CYAN),
                LaggedStart(*[c.animate.set_opacity(0.12) for c in tachados],
                            lag_ratio=0.12),
                run_time=dur,
            )
            self.wait(0.4)

        resto = [celdas[indice[n]] for n in nums if n not in primos]
        vivos = [celdas[indice[n]] for n in nums if n in primos]
        self.play(
            *[c.animate.set_opacity(0.12) for c in resto],
            *[c.animate.set_color(ACCENT_CYAN) for c in vivos],
            FadeOut(etiqueta),
            run_time=1.0,
        )
        self.play(LaggedStart(*[
            Indicate(c, color=ACCENT_YELLOW, scale_factor=1.5) for c in vivos
        ], lag_ratio=0.25), run_time=3.2)

        prod = fit(MathTex(
            r"\prod_{p\ \text{primo}}\frac{1}{1-p^{-s}}",
            font_size=88, color=ACCENT_YELLOW,
        )).set_stroke(width=1.4).move_to(DOWN * 4.4)
        self.play(Write(prod), run_time=1.4)
        self.wait(1.2)

        self.play(
            FadeOut(celdas), FadeOut(titulo),
            prod.animate.move_to(DOWN * 1.5),
            run_time=1.0,
        )
        self.wait(0.5)
        self.prod_ref = prod

    # --------------------------------------------------- 45.0-64.0 el por que
    def por_que_coinciden(self):
        geo = fit(MathTex(
            r"\frac{1}{1-p^{-s}}", "=",
            r"1+\frac{1}{p^{s}}+\frac{1}{p^{2s}}+\cdots",
            font_size=68,
        ))
        geo.set_color(ACCENT_YELLOW).set_stroke(width=1.2).move_to(UP * 2.6)
        self.play(
            FadeOut(self.prod_ref, shift=DOWN * 0.4),
            Write(geo), run_time=1.4,
        )
        self.wait(1.0)

        mezcla = fit(MathTex(
            r"\left(1+\tfrac{1}{2^{s}}+\cdots\right)"
            r"\left(1+\tfrac{1}{3^{s}}+\cdots\right)\cdots",
            font_size=60, color=ACCENT_CYAN,
        )).move_to(UP * 0.6)
        self.play(Write(mezcla), run_time=1.6)
        self.play(Indicate(mezcla, color=ACCENT_MAGENTA, scale_factor=1.1),
                  run_time=1.0)
        self.wait(0.6)

        tfa = fit(MathTex(
            r"n = 2^{a}\,3^{b}\,5^{c}\cdots",
            font_size=84, color=ACCENT_MAGENTA,
        )).set_stroke(width=1.6).move_to(DOWN * 1.6)
        pie = fit(Tex(r"factorizaci\'on \'unica", font_size=60,
                      color=WHITE)).move_to(DOWN * 3.1)
        self.play(Write(tfa), run_time=1.0)
        self.play(FadeIn(pie, shift=UP * 0.25), run_time=0.5)
        self.play(Indicate(tfa, color=ACCENT_YELLOW, scale_factor=1.2),
                  run_time=1.2)
        self.wait(1.0)

        cierre = fit(Tex(r"cada $1/n^{s}$, una sola vez",
                         font_size=62, color=WHITE)).move_to(DOWN * 4.6)
        self.play(FadeIn(cierre, shift=UP * 0.25), run_time=0.6)
        self.play(Indicate(cierre, color=ACCENT_CYAN, scale_factor=1.1),
                  run_time=1.0)
        self.wait(1.2)

        self.play(
            FadeOut(geo), FadeOut(mezcla), FadeOut(tfa),
            FadeOut(pie), FadeOut(cierre), FadeOut(self.zeta_ref),
            run_time=0.8,
        )

    # --------------------------------------------------- 64.0-80.0 el payoff
    def payoff(self):
        ident = fit(MathTex(
            r"\sum_{n=1}^{\infty}\frac{1}{n^{s}}", "=",
            r"\prod_{p\ \text{primo}}\frac{1}{1-p^{-s}}",
            font_size=80,
        ), 6.6)
        ident[0].set_color(ACCENT_CYAN)
        ident[2].set_color(ACCENT_YELLOW)
        ident.set_stroke(width=1.4).move_to(UP * 3.0)

        self.play(Write(ident), run_time=1.8)

        marco = SurroundingRectangle(
            ident, buff=0.35, corner_radius=0.22,
            stroke_width=5, color=GRADIENT_HIGHLIGHT,
        )
        self.play(Create(marco), run_time=1.4)
        self.play(Indicate(ident, color=ACCENT_MAGENTA, scale_factor=1.06),
                  run_time=1.2)

        firma = fit(Tex(r"Identidad de Euler, 1737", font_size=62,
                        color=WHITE)).move_to(UP * 1.2)
        self.play(FadeIn(firma, shift=UP * 0.25), run_time=0.5)
        self.wait(1.2)

        caso = fit(MathTex(
            r"s=2:\quad \frac{\pi^{2}}{6}"
            r"=\prod_{p}\frac{1}{1-p^{-2}}",
            font_size=72, color=ACCENT_MAGENTA,
        )).set_stroke(width=1.4).move_to(DOWN * 1.6)
        self.play(Write(caso), run_time=1.5)
        self.play(Indicate(caso, color=ACCENT_YELLOW, scale_factor=1.12),
                  run_time=1.0)
        self.wait(0.8)

        remate = fit(Tex(r"$\pi$ sabe d\'onde est\'an los primos",
                         font_size=62, color=ACCENT_YELLOW)).move_to(DOWN * 4.4)
        self.play(FadeIn(remate, shift=UP * 0.3), run_time=0.6)
        self.play(Indicate(remate, color=WHITE, scale_factor=1.15),
                  run_time=1.2)
        self.wait(1.5)
