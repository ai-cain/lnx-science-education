from manim import *
from lnx import *

# proof-without-words | probabilidad | intermedio
# Teorema de Bayes leido como una comparacion de areas.
#
#   P(E|+) = P(+|E) P(E) / P(+)
#
# La formula es lo ULTIMO que aparece. El "aha" es geometrico: el cuadrado
# unitario es toda la poblacion, el eje horizontal la parte en enfermos (1%) y
# sanos (99%), y el eje vertical, dentro de cada columna, separa el resultado
# del test. Las dos regiones que dan positivo son entonces dos rectangulos:
#
#   verdaderos positivos: 0.01 * 0.99 = 0.0099
#   falsos positivos:     0.99 * 0.05 = 0.0495   (5 veces mas grande)
#
#   P(E|+) = 0.0099 / (0.0099 + 0.0495) = 0.0099 / 0.0594 = 1/6 = 16.67%
#
# En frecuencias naturales sobre 10 000 personas: 99 verdaderos positivos
# frente a 495 falsos positivos, 594 positivos en total, 99/594 = 1/6 exacto.
# El truco visual es que la sensibilidad (99%) actua sobre una columna
# ridiculamente estrecha, mientras que un 5% de error actua sobre casi toda la
# poblacion. Por eso el bloque morado aplasta al amarillo.
#
# El frame real es 9 x 16 unidades (x en [-4.5, 4.5], y en [-8, 8]).
# Zona segura: |y| <= 5.6 y |x| <= 3.8 (la UI de TikTok tapa el resto).

SAFE_WIDTH = 7.2

# --------------------------------------------------------------- datos exactos
PREVALENCIA = 0.01      # P(E)
SENSIBILIDAD = 0.99     # P(+|E)
FALSOS_POS = 0.05       # P(+|no E)

AREA_VP = PREVALENCIA * SENSIBILIDAD            # 0.0099
AREA_FP = (1 - PREVALENCIA) * FALSOS_POS        # 0.0495
POSTERIOR = AREA_VP / (AREA_VP + AREA_FP)       # exactamente 1/6

# --------------------------------------------------------------- layout global
# Lado del cuadrado unitario en pantalla. 3.4 deja margen dentro de |x| <= 3.8
# y permite colocar etiquetas a los lados sin salirse de la zona segura.
LADO = 3.4
CUADRO_CENTRO = np.array([0.0, 1.6, 0.0])
ESQUINA = CUADRO_CENTRO + np.array([-LADO / 2, -LADO / 2, 0.0])


def uv(u, v):
    """Pasa coordenadas del cuadrado unitario (u, v en [0,1]) a la pantalla."""
    return ESQUINA + np.array([u * LADO, v * LADO, 0.0])


def region(u0, u1, v0, v1, color, opacity=0.55, stroke=0.0):
    """Rectangulo del cuadrado unitario. El area en pantalla es proporcional
    al area de probabilidad: eso es todo el argumento del video."""
    rect = Rectangle(
        width=max((u1 - u0) * LADO, 0.001),
        height=max((v1 - v0) * LADO, 0.001),
        stroke_width=stroke,
        stroke_color=color,
        fill_color=color,
        fill_opacity=opacity,
    )
    rect.move_to(uv((u0 + u1) / 2, (v0 + v1) / 2))
    return rect


def fit_to_safe_width(mobject):
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def make_label(tex, font_size, color, with_background=True, math=False):
    """Etiqueta con fondo opcional para que se lea sobre las areas de color.

    Por defecto se construye con Tex: babel spanish esta cargado, asi que el
    texto corrido con tildes se compone bien y no hace falta meter palabras
    dentro de MathTex (donde \\text{} obliga a mezclar modos sin ganar nada).
    """
    cls = MathTex if math else Tex
    label = cls(tex, font_size=font_size, color=color)
    if with_background:
        label.add_background_rectangle(color=BG, opacity=0.9, buff=0.06)
    label.set_z_index(12)
    return label


class BayesAreas(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        ENFERMO = ACCENT_MAGENTA     # la columna del 1%
        SANO = ACCENT_CYAN           # el 99% restante, siempre en baja opacidad
        VERDADERO = ACCENT_YELLOW    # verdaderos positivos
        FALSO = ACCENT_PURPLE        # falsos positivos
        AUX = GREY_B

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.14
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.85)
        self.add(watermark)

        # ----------------------------------------------------------- hook 0-6 s
        # La pregunta tiene que estar completa antes del segundo 2, por eso el
        # dato y la pregunta entran juntos y la trampa ("99%") aparece sola.
        hook_dato = Tex(
            r"Un test detecta una enfermedad\\el $99\%$ de las veces.",
            font_size=44, color=WHITE,
        )
        hook_dato.move_to(UP * 4.4)
        fit_to_safe_width(hook_dato)

        hook_preg = Tex(
            r"Das positivo.\\¿Estás enfermo?",
            font_size=52,
        )
        hook_preg.set_color_by_gradient(*GRADIENT_HIGHLIGHT)
        hook_preg.move_to(UP * 1.9)
        fit_to_safe_width(hook_preg)

        self.play(FadeIn(hook_dato, shift=DOWN * 0.3), run_time=0.7)
        self.play(Write(hook_preg), run_time=1.0)

        intuicion = Tex(r"La intuición dice: $99\%$", font_size=40, color=AUX)
        intuicion.move_to(DOWN * 0.4)
        self.play(FadeIn(intuicion, shift=UP * 0.2), run_time=0.6)
        self.wait(0.8)

        # Tachar la respuesta intuitiva antes de explicar nada: el espectador ya
        # sabe que va a perder la apuesta y se queda a ver por que.
        tacha = Line(
            intuicion.get_left() + LEFT * 0.1,
            intuicion.get_right() + RIGHT * 0.1,
            color=ACCENT_MAGENTA, stroke_width=6,
        )
        self.play(Create(tacha), run_time=0.5)
        self.wait(0.6)

        self.play(
            FadeOut(hook_dato), FadeOut(hook_preg),
            FadeOut(intuicion), FadeOut(tacha),
            run_time=0.5,
        )

        # ------------------------------------------------- beat 1: la poblacion
        titulo = Tex(r"Toda la población", font_size=44, color=WHITE)
        titulo.move_to(UP * 5.0)
        fit_to_safe_width(titulo)

        marco = Rectangle(
            width=LADO, height=LADO,
            stroke_width=4, stroke_color=WHITE,
        )
        marco.move_to(CUADRO_CENTRO)
        marco.set_z_index(8)

        # El cuadrado unitario: area total = 1 = 10 000 personas.
        self.play(Write(titulo), Create(marco), run_time=1.0)

        personas = make_label(r"10\,000 personas", 32, WHITE, with_background=False)
        personas.next_to(marco, DOWN, buff=0.28)
        self.play(FadeIn(personas), run_time=0.5)
        self.wait(0.4)

        # Prevalencia 1%: la columna de enfermos es tan estrecha que en pantalla
        # es practicamente una linea. Ese es exactamente el punto.
        sanos = region(PREVALENCIA, 1.0, 0.0, 1.0, SANO, opacity=0.16)
        enfermos = region(0.0, PREVALENCIA, 0.0, 1.0, ENFERMO, opacity=1.0)
        enfermos.set_z_index(6)

        self.play(FadeIn(sanos), run_time=0.5)
        self.play(GrowFromEdge(enfermos, DOWN), run_time=0.8)

        # La columna mide 3 px de ancho, asi que la etiqueta va fuera con guia.
        et_enf = make_label(r"$1\%$ enfermos", 30, ENFERMO, with_background=False)
        et_enf.move_to(uv(0.0, 1.0) + UP * 0.45 + LEFT * 0.15)
        guia = Line(et_enf.get_bottom() + DOWN * 0.05, uv(0.005, 1.0), color=ENFERMO, stroke_width=2.5)

        et_sanos = make_label(r"$99\%$ sanos", 30, SANO, with_background=False)
        et_sanos.move_to(uv(0.55, 0.5))

        self.play(FadeIn(et_enf), Create(guia), run_time=0.6)
        self.play(FadeIn(et_sanos), run_time=0.5)
        self.wait(0.8)

        self.play(FadeOut(et_sanos), run_time=0.35)

        # ------------------------------------------- beat 2: el test, dos areas
        nuevo_titulo = Tex(r"¿Quién da positivo?", font_size=44, color=WHITE)
        nuevo_titulo.move_to(titulo.get_center())
        fit_to_safe_width(nuevo_titulo)
        self.play(
            FadeOut(titulo, shift=UP * 0.25),
            FadeIn(nuevo_titulo, shift=UP * 0.25),
            FadeOut(et_enf), FadeOut(guia),
            run_time=0.6,
        )

        # Dentro de CADA columna, la altura mide la proporcion que da positivo,
        # medida siempre desde el borde superior para que las dos franjas
        # positivas queden pegadas y sean comparables de un vistazo.
        vp = region(0.0, PREVALENCIA, 1 - SENSIBILIDAD, 1.0, VERDADERO, opacity=1.0)
        vp.set_z_index(7)
        fp = region(PREVALENCIA, 1.0, 1 - FALSOS_POS, 1.0, FALSO, opacity=0.95)
        fp.set_z_index(7)

        # Primero la sensibilidad, que es el dato que produce la falsa intuicion.
        self.play(GrowFromEdge(vp, DOWN), run_time=0.9)
        et_vp = make_label(r"$99\%$ de los enfermos", 28, VERDADERO)
        et_vp.move_to(uv(0.0, 1.0) + UP * 0.42 + RIGHT * 0.55)
        guia_vp = Line(et_vp.get_bottom() + DOWN * 0.05, uv(0.006, 0.98), color=VERDADERO, stroke_width=2.5)
        self.play(FadeIn(et_vp), Create(guia_vp), run_time=0.6)
        self.wait(0.5)

        # Y ahora el dato que nadie menciona: un 5% de error sobre casi todos.
        self.play(GrowFromEdge(fp, DOWN), run_time=0.9)
        et_fp = make_label(r"$5\%$ de los sanos", 28, FALSO)
        et_fp.next_to(fp, DOWN, buff=0.35)
        flecha_fp = Arrow(
            et_fp.get_top(), fp.get_bottom() + DOWN * 0.02,
            buff=0.06, color=FALSO, stroke_width=3, max_tip_length_to_length_ratio=0.25,
        )
        self.play(FadeIn(et_fp), GrowArrow(flecha_fp), run_time=0.6)
        self.wait(0.6)

        # Comparacion directa de las dos areas, todavia dentro del cuadrado.
        self.play(
            Indicate(vp, color=VERDADERO, scale_factor=1.0),
            Indicate(fp, color=FALSO, scale_factor=1.0),
            run_time=1.0,
        )
        self.wait(0.4)

        # ------------------------------------------- beat 3: sacar los positivos
        # Lo que sigue es el golpe: los dos rectangulos salen del cuadrado y se
        # comparan a la misma escala. Como son finisimos, se redibujan con el
        # mismo ancho y altura proporcional al AREA (0.0099 vs 0.0495 = 1 a 5).
        self.play(
            FadeOut(nuevo_titulo), FadeOut(et_vp), FadeOut(guia_vp),
            FadeOut(et_fp), FadeOut(flecha_fp), FadeOut(personas),
            run_time=0.5,
        )

        titulo3 = Tex(r"Solo los positivos", font_size=44, color=WHITE)
        titulo3.move_to(UP * 5.2)
        fit_to_safe_width(titulo3)

        # Escala de las barras: la de falsos positivos ocupa 3.2 unidades, la de
        # verdaderos 3.2/5 = 0.64. La razon 1:5 es exacta, no esta maquillada.
        BARRA_ANCHO = 1.5
        BARRA_MAX = 3.2
        alto_vp = BARRA_MAX * AREA_VP / AREA_FP
        alto_fp = BARRA_MAX

        base_y = -2.6
        barra_vp = Rectangle(
            width=BARRA_ANCHO, height=alto_vp,
            stroke_width=0, fill_color=VERDADERO, fill_opacity=1.0,
        )
        barra_vp.move_to(np.array([-1.05, base_y + alto_vp / 2, 0.0]))
        barra_fp = Rectangle(
            width=BARRA_ANCHO, height=alto_fp,
            stroke_width=0, fill_color=FALSO, fill_opacity=1.0,
        )
        barra_fp.move_to(np.array([1.05, base_y + alto_fp / 2, 0.0]))

        self.play(
            FadeOut(sanos), FadeOut(enfermos), FadeOut(marco),
            FadeIn(titulo3),
            ReplacementTransform(vp, barra_vp),
            ReplacementTransform(fp, barra_fp),
            run_time=1.4,
        )

        # Frecuencias naturales: refuerzan el area con numeros enteros.
        num_vp = make_label(r"99", 40, VERDADERO, with_background=False, math=True)
        num_vp.next_to(barra_vp, UP, buff=0.2)
        cap_vp = Tex(r"enfermos\\detectados", font_size=30, color=VERDADERO)
        cap_vp.next_to(barra_vp, DOWN, buff=0.25)

        num_fp = make_label(r"495", 40, FALSO, with_background=False, math=True)
        num_fp.next_to(barra_fp, UP, buff=0.2)
        cap_fp = Tex(r"sanos\\con falso positivo", font_size=30, color=FALSO)
        cap_fp.next_to(barra_fp, DOWN, buff=0.25)
        fit_to_safe_width(cap_fp)

        self.play(
            FadeIn(num_vp), FadeIn(cap_vp),
            FadeIn(num_fp), FadeIn(cap_fp),
            run_time=0.8,
        )
        self.wait(0.6)

        llave = BraceBetweenPoints(
            barra_fp.get_top() + RIGHT * 0.9,
            barra_vp.get_bottom() + LEFT * 0.9 + UP * alto_vp,
            direction=RIGHT,
        )
        et_llave = Tex(r"$5\times$ más", font_size=36, color=WHITE)
        et_llave.next_to(llave, RIGHT, buff=0.12)
        self.play(GrowFromCenter(llave), FadeIn(et_llave), run_time=0.8)
        self.wait(0.8)

        self.play(FadeOut(llave), FadeOut(et_llave), run_time=0.4)

        # El resultado sale de la fraccion de frecuencias, no de una formula.
        cuenta = MathTex(
            r"\frac{99}{99+495}", r"=", r"\frac{1}{6}", r"=", r"16.7\%",
            font_size=48,
        )
        cuenta[0].set_color(VERDADERO)
        cuenta[4].set_color(ACCENT_MAGENTA)
        cuenta.move_to(UP * 4.0)
        fit_to_safe_width(cuenta)
        self.play(
            TransformFromCopy(VGroup(num_vp, num_fp), cuenta[0]),
            run_time=0.9,
        )
        self.play(Write(cuenta[1:]), run_time=1.0)

        caja = SurroundingRectangle(cuenta[4], buff=0.14, corner_radius=0.1)
        caja.set_stroke(width=4, color=[ACCENT_YELLOW, ACCENT_MAGENTA])
        self.play(Create(caja), run_time=0.6)
        self.wait(1.2)

        # ------------------------------------------------- beat 4: recien Bayes
        self.play(
            FadeOut(titulo3), FadeOut(num_vp), FadeOut(num_fp),
            FadeOut(cap_vp), FadeOut(cap_fp),
            VGroup(cuenta, caja).animate.move_to(UP * 4.6).scale(0.8),
            VGroup(barra_vp, barra_fp).animate.scale(0.55).move_to(DOWN * 3.4),
            run_time=1.0,
        )

        bayes = MathTex(
            r"P(E\mid +)", r"=",
            r"\frac{P(+\mid E)\,P(E)}{P(+)}",
            font_size=52,
        )
        bayes[0].set_color(ACCENT_MAGENTA)
        bayes.move_to(UP * 1.9)
        fit_to_safe_width(bayes)
        self.play(Write(bayes), run_time=1.4)
        self.wait(0.4)

        # Cada simbolo es un area que ya se vio en pantalla: el numerador es la
        # barra amarilla y el denominador son las dos barras juntas.
        # Los recuadros se construyen a partir de la caja de la fraccion y no de
        # indices de submobjects: asi no dependen de como LaTeX parta el glifo.
        frac = bayes[2]
        barra_y = frac.get_center()[1]

        def caja_fraccion(arriba, color):
            alto = abs(frac.get_top()[1] - barra_y) if arriba else abs(barra_y - frac.get_bottom()[1])
            r = Rectangle(width=frac.width + 0.16, height=alto + 0.1)
            r.set_stroke(color=color, width=3)
            r.set_fill(opacity=0)
            r.move_to(np.array([
                frac.get_center()[0],
                barra_y + (alto / 2 + 0.05) * (1 if arriba else -1),
                0.0,
            ]))
            return r

        num_area = caja_fraccion(True, VERDADERO)
        den_area = caja_fraccion(False, WHITE)

        glosa_num = Tex(r"área amarilla", font_size=30, color=VERDADERO)
        glosa_num.next_to(bayes, DOWN, buff=0.45)
        glosa_den = Tex(r"las dos áreas juntas", font_size=30, color=WHITE)
        glosa_den.next_to(glosa_num, DOWN, buff=0.22)

        self.play(Create(num_area), FadeIn(glosa_num),
                  Indicate(barra_vp, color=VERDADERO, scale_factor=1.15), run_time=0.9)
        self.play(
            ReplacementTransform(num_area, den_area), FadeIn(glosa_den),
            Indicate(VGroup(barra_vp, barra_fp), color=WHITE, scale_factor=1.1),
            run_time=0.9,
        )
        self.wait(0.6)

        moraleja = Tex(
            r"Un test muy bueno\\sobre algo muy raro\\da sobre todo falsos positivos.",
            font_size=36, color=WHITE,
        )
        moraleja.move_to(DOWN * 0.9)
        fit_to_safe_width(moraleja)
        self.play(
            FadeOut(den_area), FadeOut(glosa_num), FadeOut(glosa_den),
            FadeIn(moraleja, shift=UP * 0.2),
            run_time=0.9,
        )
        self.wait(2.0)

        animate_End(scene=self)
