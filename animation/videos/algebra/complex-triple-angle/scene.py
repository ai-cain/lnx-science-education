from manim import *
from lnx import *

# two-paths-one-result | algebra | advanced
# El angulo triple SIN geometria: solo numeros complejos.
#
# La ruta 1 es la trigonometrica clasica (sumar angulos, dibujar triangulos,
# encadenar identidades). La ruta 2 es puro algebra: elevar al cubo el numero
# complejo unitario z = cos(t) + i sen(t) de dos maneras distintas.
#
#   De Moivre:   z^3 = cos(3t) + i sen(3t)
#   Newton:      z^3 = (c + i s)^3
#                    = c^3 + 3c^2 (i s) + 3c (i s)^2 + (i s)^3
#                    = c^3 + 3i c^2 s - 3 c s^2 - i s^3         (i^2=-1, i^3=-i)
#                    = (c^3 - 3 c s^2) + i (3 c^2 s - s^3)
#
# Igualar parte real con parte real y parte imaginaria con parte imaginaria
# entrega las DOS identidades de golpe. Con s^2 = 1 - c^2 y c^2 = 1 - s^2:
#
#   cos 3t = 4 cos^3 t - 3 cos t
#   sen 3t = 3 sen t - 4 sen^3 t
#
# Verificacion numerica (t = 20 grados, cos t = 0.9396926, sen t = 0.3420201):
#   4*(0.9396926)^3 - 3*(0.9396926) = 3.3190780 - 2.8190779 = 0.5000001
#   cos 60 grados                                            = 0.5000000   OK
#   3*(0.3420201) - 4*(0.3420201)^3 = 1.0260604 - 0.1600343 = 0.8660261
#   sen 60 grados                                            = 0.8660254   OK
# (Segunda verificacion, t = 50 grados: 4*cos^3 50 - 3*cos 50 = -0.7071068
#  y cos 150 = -0.7071068; 3*sen 50 - 4*sen^3 50 = 0.5000000 = sen 150.)
#
# El frame real mide 9 x 16 unidades. Zona segura: |x| <= 3.8, |y| <= 5.6.

SAFE_WIDTH = 7.2

REAL_COLOR = ACCENT_CYAN       # todo lo que termina siendo parte real
IMAG_COLOR = ACCENT_MAGENTA    # todo lo que termina siendo parte imaginaria
KEY_COLOR = ACCENT_YELLOW      # el resultado
NOTE_COLOR = ACCENT_PURPLE     # notas de apoyo

# Abreviaturas en pantalla: sin ellas las expansiones no caben en 9:16.
C = r"c"
S = r"s"


def fit_safe(mobject):
    """Ninguna formula puede salirse de la zona segura horizontal."""
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def step(*parts, font_size=42, color=WHITE):
    """MathTex por piezas, listo para TransformMatchingTex."""
    tex = MathTex(*parts, font_size=font_size, color=color)
    tex.set_stroke(width=1)
    tex.set_z_index(20)
    return fit_safe(tex)


def caption(text, font_size=30, color=GREY_A):
    """Linea de narracion en la parte baja, siempre dentro de la zona segura."""
    label = Tex(text, font_size=font_size, color=color)
    label.set_z_index(20)
    label.move_to(DOWN * 4.7)
    return fit_safe(label)


class ComplexTripleAngle(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.14
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.85)
        self.add(watermark)

        # ----------------------------------------------------------- hook 0-2 s
        # Arranca con la pregunta que todos resuelven dibujando triangulos, y
        # con la promesa de que aqui no se va a dibujar ninguno.
        question = MathTex(
            r"\cos 3\theta = \; ?",
            font_size=64, color=KEY_COLOR,
        )
        question.set_stroke(width=1)
        question.set_z_index(20)
        question.move_to(UP * 1.1)
        fit_safe(question)

        no_geometry = Tex(
            r"sin un solo tri\'angulo",
            font_size=38, color=WHITE,
        )
        no_geometry.set_z_index(20)
        no_geometry.next_to(question, DOWN, buff=0.7)
        fit_safe(no_geometry)

        self.play(Write(question), run_time=0.7)
        self.play(FadeIn(no_geometry, shift=UP * 0.2), run_time=0.5)

        strike = Line(
            no_geometry.get_left() + LEFT * 0.1,
            no_geometry.get_right() + RIGHT * 0.1,
            stroke_width=5,
        )
        strike.set_color(color=[ACCENT_MAGENTA, ACCENT_YELLOW])
        strike.set_z_index(21)
        self.play(Create(strike), run_time=0.4)
        self.wait(0.4)

        # ------------------------------------------- beat 1: el numero complejo
        # Un solo objeto carga toda la trigonometria: z sobre la circunferencia
        # unitaria. No se dibuja la circunferencia; se enuncia.
        self.play(
            FadeOut(question), FadeOut(no_geometry), FadeOut(strike),
            run_time=0.4,
        )

        title = Tex(r"Solo \'algebra", font_size=54, color=WHITE)
        title.set_stroke(width=1)
        title.set_z_index(20)
        title.move_to(UP * 5.2)
        fit_safe(title)

        underline = Line(
            title.get_left() + DOWN * 0.28,
            title.get_right() + DOWN * 0.28,
            stroke_width=4,
        )
        underline.set_color(color=GRADIENT_MAIN)
        underline.set_z_index(20)

        self.play(Write(title), run_time=0.6)
        self.play(Create(underline), run_time=0.3)

        z_def = MathTex(
            r"z = \cos\theta + i\,\operatorname{sen}\theta",
            font_size=44,
        )
        z_def[0][2:7].set_color(REAL_COLOR)
        z_def[0][8:].set_color(IMAG_COLOR)
        z_def.set_stroke(width=1)
        z_def.set_z_index(20)
        z_def.move_to(UP * 3.5)
        fit_safe(z_def)
        self.play(Write(z_def), run_time=0.8)

        shorthand = MathTex(
            r"c=\cos\theta,\qquad s=\operatorname{sen}\theta",
            font_size=32, color=GREY_B,
        )
        shorthand.set_z_index(20)
        shorthand.next_to(z_def, DOWN, buff=0.35)
        fit_safe(shorthand)
        self.play(FadeIn(shorthand), run_time=0.5)
        self.wait(0.5)

        # --------------------------------- beat 2: el mismo cubo por dos rutas
        # De Moivre da el resultado empaquetado; Newton lo da desarmado. Como es
        # el mismo numero, las dos escrituras tienen que coincidir pieza a pieza.
        route_left = Tex(r"De Moivre", font_size=32, color=NOTE_COLOR)
        route_left.set_z_index(20)
        route_left.move_to(UP * 2.15)
        moivre = step(
            r"z^3", r"=", r"\cos 3\theta", r"+", r"i\,\operatorname{sen} 3\theta",
            font_size=42,
        )
        moivre[2].set_color(REAL_COLOR)
        moivre[4].set_color(IMAG_COLOR)
        moivre.move_to(UP * 1.35)

        self.play(FadeIn(route_left), run_time=0.35)
        self.play(Write(moivre), run_time=0.9)
        self.wait(0.5)

        route_right = Tex(r"Binomio de Newton", font_size=32, color=NOTE_COLOR)
        route_right.set_z_index(20)
        route_right.move_to(DOWN * 0.25)
        newton = step(r"z^3", r"=", r"(", C, r"+", r"i" + S, r")^3", font_size=42)
        newton.move_to(DOWN * 1.1)

        self.play(FadeIn(route_right), run_time=0.35)
        self.play(Write(newton), run_time=0.7)

        same_number = caption(r"el mismo n\'umero, escrito de dos formas")
        self.play(FadeIn(same_number, shift=UP * 0.15), run_time=0.5)
        self.wait(0.8)

        # ------------------------------------ beat 3: desarrollar con el binomio
        # Aqui vive el video: TransformMatchingTex encadena las manipulaciones y
        # el ojo sigue cada termino de una linea a la siguiente.
        expanded = step(
            C + r"^3", r"+", r"3" + C + r"^2(i" + S + r")", r"+",
            r"3" + C + r"(i" + S + r")^2", r"+", r"(i" + S + r")^3",
            font_size=36,
        )
        expanded.move_to(DOWN * 1.1)

        self.play(FadeOut(same_number), run_time=0.3)
        self.play(TransformMatchingTex(newton, expanded), run_time=1.3)

        powers = MathTex(r"i^2=-1,\qquad i^3=-i", font_size=32, color=KEY_COLOR)
        powers.set_z_index(20)
        powers.move_to(DOWN * 2.35)
        fit_safe(powers)
        self.play(FadeIn(powers, shift=UP * 0.15), run_time=0.5)
        self.wait(0.7)

        simplified = step(
            C + r"^3", r"+", r"3i" + C + r"^2" + S, r"-",
            r"3" + C + S + r"^2", r"-", r"i" + S + r"^3",
            font_size=36,
        )
        simplified.move_to(DOWN * 1.1)
        self.play(TransformMatchingTex(expanded, simplified), run_time=1.3)
        self.wait(0.6)

        # ------------------------- beat 4: separar parte real y parte imaginaria
        self.play(FadeOut(powers), run_time=0.3)

        split = step(
            r"(" + C + r"^3-3" + C + S + r"^2)", r"+",
            r"i(3" + C + r"^2" + S + r"-" + S + r"^3)",
            font_size=38,
        )
        split[0].set_color(REAL_COLOR)
        split[2].set_color(IMAG_COLOR)
        split.move_to(DOWN * 1.1)
        self.play(TransformMatchingTex(simplified, split), run_time=1.3)

        separate = caption(r"parte real y parte imaginaria, separadas")
        self.play(FadeIn(separate, shift=UP * 0.15), run_time=0.5)
        self.wait(0.9)

        # --------------------------------------- beat 5: igualar pieza con pieza
        # Dos flechas hacen explicito el emparejamiento: real con real, imaginaria
        # con imaginaria. De ahi salen las dos identidades al mismo tiempo.
        arrow_real = Arrow(
            split[0].get_top() + UP * 0.05,
            moivre[2].get_bottom() + DOWN * 0.05,
            buff=0.08, color=REAL_COLOR, stroke_width=5,
            max_tip_length_to_length_ratio=0.09,
        )
        arrow_imag = Arrow(
            split[2].get_top() + UP * 0.05,
            moivre[4].get_bottom() + DOWN * 0.05,
            buff=0.08, color=IMAG_COLOR, stroke_width=5,
            max_tip_length_to_length_ratio=0.09,
        )
        for arrow in (arrow_real, arrow_imag):
            arrow.set_z_index(15)

        self.play(FadeOut(separate), run_time=0.3)
        self.play(GrowArrow(arrow_real), run_time=0.5)
        self.play(GrowArrow(arrow_imag), run_time=0.5)
        self.wait(0.6)

        pair = VGroup(
            MathTex(
                r"\cos 3\theta = " + C + r"^3 - 3" + C + S + r"^2",
                font_size=36, color=REAL_COLOR,
            ),
            MathTex(
                r"\operatorname{sen} 3\theta = 3" + C + r"^2" + S + r" - " + S + r"^3",
                font_size=36, color=IMAG_COLOR,
            ),
        )
        pair.arrange(DOWN, buff=0.45)
        pair.set_stroke(width=1)
        pair.set_z_index(20)
        pair.move_to(DOWN * 1.6)
        fit_safe(pair)

        self.play(
            FadeOut(arrow_real), FadeOut(arrow_imag),
            ReplacementTransform(split, pair),
            run_time=1.1,
        )
        self.wait(0.8)

        # -------------------------------- beat 6: dejar todo en un solo cociente
        # Con s^2 = 1 - c^2 (y c^2 = 1 - s^2) cada identidad queda en una sola
        # funcion. Esa es la forma que se memoriza.
        pythagoras = MathTex(
            r"s^2 = 1 - c^2, \qquad c^2 = 1 - s^2",
            font_size=32, color=KEY_COLOR,
        )
        pythagoras.set_z_index(20)
        pythagoras.move_to(DOWN * 3.5)
        fit_safe(pythagoras)
        self.play(FadeIn(pythagoras, shift=UP * 0.15), run_time=0.5)
        self.wait(0.7)

        final_pair = VGroup(
            MathTex(
                r"\cos 3\theta = 4\cos^3\theta - 3\cos\theta",
                font_size=36, color=REAL_COLOR,
            ),
            MathTex(
                r"\operatorname{sen} 3\theta = 3\operatorname{sen}\theta"
                r" - 4\operatorname{sen}^3\theta",
                font_size=36, color=IMAG_COLOR,
            ),
        )
        final_pair.arrange(DOWN, buff=0.5)
        final_pair.set_stroke(width=1)
        final_pair.set_z_index(20)
        final_pair.move_to(DOWN * 1.6)
        fit_safe(final_pair)

        self.play(
            ReplacementTransform(pair, final_pair),
            FadeOut(pythagoras),
            run_time=1.2,
        )

        result_box = SurroundingRectangle(final_pair, buff=0.3, corner_radius=0.14)
        result_box.set_stroke(width=4, color=GRADIENT_HIGHLIGHT)
        result_box.set_z_index(19)
        self.play(Create(result_box), run_time=0.7)
        self.wait(1.0)

        # -------------------------------------------- beat 7: prueba numerica
        # theta = 20 grados: los dos lados coinciden hasta el ultimo decimal.
        self.play(
            FadeOut(z_def), FadeOut(shorthand),
            FadeOut(route_left), FadeOut(route_right), FadeOut(moivre),
            run_time=0.5,
        )
        self.play(
            VGroup(final_pair, result_box).animate.move_to(UP * 2.6),
            run_time=0.7,
        )

        check_title = Tex(r"$\theta = 20^\circ$", font_size=36, color=WHITE)
        check_title.set_z_index(20)
        check_title.move_to(DOWN * 0.4)

        check = VGroup(
            MathTex(r"4\cos^3 20^\circ - 3\cos 20^\circ = 0{,}5000",
                    font_size=32, color=REAL_COLOR),
            MathTex(r"\cos 60^\circ = 0{,}5000",
                    font_size=32, color=GREY_A),
            MathTex(r"3\operatorname{sen} 20^\circ - 4\operatorname{sen}^3 20^\circ"
                    r" = 0{,}8660",
                    font_size=32, color=IMAG_COLOR),
            MathTex(r"\operatorname{sen} 60^\circ = 0{,}8660",
                    font_size=32, color=GREY_A),
        )
        check.arrange(DOWN, buff=0.42)
        check.set_z_index(20)
        check.move_to(DOWN * 2.6)
        fit_safe(check)

        self.play(FadeIn(check_title), run_time=0.4)
        self.play(
            LaggedStart(*[FadeIn(line, shift=UP * 0.12) for line in check],
                        lag_ratio=0.35),
            run_time=1.8,
        )
        self.wait(0.9)

        closing = Tex(
            r"un problema de trigonometr\'ia,\\resuelto con \'algebra pura",
            font_size=34, color=KEY_COLOR,
        )
        closing.set_z_index(20)
        closing.move_to(DOWN * 5.0)
        fit_safe(closing)
        self.play(FadeIn(closing, shift=UP * 0.15), run_time=0.6)
        self.wait(1.4)

        animate_End(scene=self)
