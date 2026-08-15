from manim import *
from lnx import *

# paradoja-visual | geometry | intermedio
# Copo de Koch: perimetro infinito encerrando area finita.
#
# La regla es una sola: a cada segmento le quitas el tercio central y lo
# reemplazas por los dos lados de un triangulo equilatero. Un segmento se
# vuelve cuatro segmentos de longitud 1/3.
#
#   Perimetro:  cada iteracion multiplica por 4/3.
#               P_n = 3 (4/3)^n  ->  3, 4, 5.33, 7.11, 9.48, 12.64, ... -> infinito
#
#   Area:       la iteracion n agrega 3*4^(n-1) triangulos de area (1/9)^n,
#               es decir (3/4)(4/9)^n. La serie es geometrica de razon 4/9 < 1:
#               A_n = A_0 [ 1 + (3/5)(1 - (4/9)^n) ]  ->  (8/5) A_0 = 1.6 A_0
#
#   Dimension:  la curva se autoreplica en N = 4 copias a escala r = 1/3, asi que
#               D = log 4 / log 3 = 1.2619...  Ni linea (1) ni superficie (2).
#
# El golpe del video es el contraste SIMULTANEO de los dos contadores: uno se
# cuadruplica mientras el otro se estanca. Por eso ambas barras se normalizan
# contra su propio valor en n = 0 y comparten escala: la comparacion es honesta.
#
# El frame real es 9 x 16 (x en [-4.5, 4.5], y en [-8, 8]).
# Zona segura: |y| <= 5.6 y |x| <= 3.8.

# --------------------------------------------------------------------- formato
# El CLI del pipeline fija el formato vertical con -r; al renderizar a mano no.
# Ajustamos el frame a 9 x 16 conservando la altura en pixeles que pidio el CLI,
# para que -ql siga siendo rapido y la composicion nunca salga deformada.
config.frame_width, config.frame_height = 9.0, 16.0
config.pixel_width = int(round(config.pixel_height * 9 / 16))
if config.pixel_width % 2:
    config.pixel_width += 1

# ------------------------------------------------------------------- layout
SAFE_X = 3.8
SAFE_Y = 5.6

TITLE_Y = 5.15          # titulo pegado al borde superior de la zona segura
FLAKE_CENTER = np.array([0.0, 1.9, 0.0])
FLAKE_R = 2.15          # radio del circuncirculo del triangulo inicial

BAR_X0 = -1.55          # borde izquierdo comun de las dos barras
BAR_MAX = 5.15          # ancho maximo: BAR_X0 + BAR_MAX = 3.6 < SAFE_X
BAR_H = 0.34
ROW_P_Y = -3.15         # fila del perimetro
ROW_A_Y = -4.45         # fila del area

MAX_ITER = 5            # 3*4^5 = 3072 segmentos: el limite razonable

C_PERIM = ACCENT_MAGENTA   # lo que se dispara
C_AREA = ACCENT_CYAN       # lo que se estanca
C_RULE = ACCENT_YELLOW     # la regla de construccion
C_DIM = ACCENT_PURPLE      # la dimension fractal


def perimeter(n):
    """P_n / lado inicial, con lado 1: 3, 4, 5.33, 7.11, 9.48, 12.64."""
    return 3.0 * (4.0 / 3.0) ** n


def area(n):
    """A_n / A_0 = 1 + (3/5)(1 - (4/9)^n) -> 8/5."""
    return 1.0 + 0.6 * (1.0 - (4.0 / 9.0) ** n)


def koch_edge(p, q):
    """Los 4 puntos iniciales del reemplazo del segmento p->q (falta q)."""
    d = (q - p) / 3.0
    return [p, p + d, p + d + rotate_vector(d, -60 * DEGREES), p + 2 * d]


def koch_curve(p, q, iterations):
    """Curva de Koch abierta de p a q: 4^n + 1 puntos."""
    pts = [np.array(p, dtype=float), np.array(q, dtype=float)]
    for _ in range(iterations):
        nxt = []
        for a, b in zip(pts[:-1], pts[1:]):
            nxt.extend(koch_edge(a, b))
        nxt.append(pts[-1])
        pts = nxt
    return pts


def koch_snowflake(vertices, iterations):
    """Poligono cerrado: aplica la regla a cada lado del triangulo base."""
    pts = []
    for a, b in zip(vertices, vertices[1:] + vertices[:1]):
        pts.extend(koch_curve(a, b, iterations)[:-1])
    pts.append(pts[0])
    return pts


def as_vmobject(points, stroke_color, stroke_width=3.0, fill_opacity=0.0):
    """UN solo VMobject por corners. Con 3072 lados, miles de Line no sirven."""
    m = VMobject()
    m.set_points_as_corners(points)
    m.set_stroke(color=stroke_color, width=stroke_width)
    m.set_fill(color=C_AREA, opacity=fill_opacity)
    return m


class KochSnowflake(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.14
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.85)
        self.add(watermark)

        # Triangulo equilatero base, orientado CCW para que las puntas de Koch
        # (rotacion de -60 grados) salgan siempre hacia afuera.
        base = [
            FLAKE_CENTER + FLAKE_R * np.array(
                [np.cos(a * DEGREES), np.sin(a * DEGREES), 0.0]
            )
            for a in (90, 210, 330)
        ]
        # El grosor baja con la iteracion: a nivel 5 los lados miden ~1.5 px.
        widths = [5.0, 4.4, 3.8, 3.2, 2.6, 2.2]
        flakes = [
            as_vmobject(koch_snowflake(base, n), C_AREA, widths[n])
            for n in range(MAX_ITER + 1)
        ]

        # ------------------------------------------------------- hook (0 - 6 s)
        # Primero se ve la paradoja, despues se explica. El borde se eriza en
        # menos de dos segundos: es lo unico que tiene que pasar al inicio.
        title = Tex(r"Copo de Koch", font_size=60, color=WHITE)
        title.set_stroke(width=1).move_to(UP * TITLE_Y)
        underline = Line(
            title.get_left() + DOWN * 0.3, title.get_right() + DOWN * 0.3,
            stroke_width=4,
        ).set_color(color=[C_AREA, C_PERIM])

        flake = flakes[0].copy()
        self.play(Write(title), Create(flake), run_time=0.8)
        self.play(Create(underline), run_time=0.3)
        for n in range(1, MAX_ITER + 1):
            self.play(Transform(flake, flakes[n].copy()), run_time=0.34)

        hook = VGroup(
            Tex(r"Este contorno mide \textbf{infinito}.", font_size=38,
                color=C_PERIM),
            Tex(r"Lo que encierra, \textbf{no}.", font_size=38, color=C_AREA),
        ).arrange(DOWN, buff=0.28).move_to(np.array([0.0, -3.6, 0.0]))
        self.play(FadeIn(hook, shift=UP * 0.25), run_time=0.7)
        self.wait(1.0)
        self.play(FadeOut(hook), run_time=0.35)

        # ------------------------------------------------- beat 1: la regla
        # La regla se ve UNA vez, en un segmento grande y solo, antes de que el
        # ojo tenga que seguirla en 3, 12, 48 lados a la vez.
        self.play(
            flake.animate.become(flakes[0].copy()).scale(0.55).move_to(
                np.array([0.0, 3.9, 0.0])
            ),
            run_time=0.7,
        )

        rule_title = Tex(r"La regla", font_size=42, color=C_RULE)
        rule_title.move_to(np.array([0.0, 1.75, 0.0]))

        seg_y = 0.2
        P0 = np.array([-3.0, seg_y, 0.0])
        P3 = np.array([3.0, seg_y, 0.0])
        seg = Line(P0, P3, color=WHITE, stroke_width=7)
        self.play(FadeIn(rule_title, shift=DOWN * 0.2), Create(seg), run_time=0.7)

        # Los dos cortes que definen el tercio central.
        P1, P2 = P0 + (P3 - P0) / 3, P0 + 2 * (P3 - P0) / 3
        cuts = VGroup(*[Dot(p, color=C_RULE, radius=0.09) for p in (P1, P2)])
        thirds = VGroup(*[
            MathTex(r"\tfrac{1}{3}", font_size=30, color=C_RULE).next_to(
                Line(a, b), DOWN, buff=0.18
            )
            for a, b in ((P0, P1), (P1, P2), (P2, P3))
        ])
        self.play(FadeIn(cuts, scale=0.5), Write(thirds), run_time=0.7)
        self.wait(0.4)

        # Quitas el tercio central...
        middle = Line(P1, P2, color=WHITE, stroke_width=7)
        self.add(middle)
        left = Line(P0, P1, color=C_RULE, stroke_width=7)
        right = Line(P2, P3, color=C_RULE, stroke_width=7)
        self.remove(seg)
        self.add(left, right)
        self.play(FadeOut(middle, shift=DOWN * 0.6), FadeOut(thirds), run_time=0.6)

        # ...y lo reemplazas por los otros dos lados del triangulo equilatero.
        apex = P1 + rotate_vector((P3 - P0) / 3, -60 * DEGREES)
        tent = VMobject().set_points_as_corners([P1, apex, P2])
        tent.set_stroke(color=C_RULE, width=7)
        ghost = DashedVMobject(
            Polygon(P1, apex, P2, stroke_width=3, color=GREY_B), num_dashes=18
        )
        self.play(Create(tent), FadeIn(ghost), run_time=0.8)
        self.play(FadeOut(ghost), run_time=0.3)

        rule_text = Tex(
            r"1 segmento $\rightarrow$ 4 segmentos de $\tfrac{1}{3}$",
            font_size=36, color=WHITE,
        ).move_to(np.array([0.0, -2.1, 0.0]))
        factor = MathTex(
            r"\times \tfrac{4}{3}", r"\ \text{de longitud}",
            font_size=40,
        )
        factor[0].set_color(C_PERIM)
        factor.move_to(np.array([0.0, -3.3, 0.0]))
        self.play(Write(rule_text), run_time=0.7)
        self.play(FadeIn(factor, shift=UP * 0.2), run_time=0.6)
        self.wait(0.9)

        rule_group = VGroup(
            rule_title, left, right, tent, cuts, rule_text, factor
        )
        self.play(FadeOut(rule_group), run_time=0.5)

        # ---------------------------------------- beats 2 y 3: los dos contadores
        # El copo sube y deja libre el tercio inferior del frame para las barras.
        self.play(
            flake.animate.become(flakes[0].copy()),
            run_time=0.7,
        )

        n_track = ValueTracker(0.0)   # iteracion actual, siempre entera
        p_track = ValueTracker(perimeter(0))
        a_track = ValueTracker(area(0))

        def bar(tracker, base_value, color):
            """Barra normalizada contra su propio valor en n = 0.

            Ambas barras comparten escala, asi que la unica diferencia visible
            entre ellas es matematica, no de dibujo.
            """
            return always_redraw(
                lambda: Rectangle(
                    width=max(
                        1e-3,
                        BAR_MAX * (tracker.get_value() / base_value) / 4.25
                    ),
                    height=BAR_H,
                    stroke_width=0,
                    fill_color=color,
                    fill_opacity=0.9,
                ).align_to(np.array([BAR_X0, 0.0, 0.0]), LEFT)
                .set_y(ROW_P_Y if color == C_PERIM else ROW_A_Y)
            )

        n_label = VGroup(
            MathTex(r"n =", font_size=40, color=WHITE),
            DecimalNumber(0, num_decimal_places=0, font_size=40, color=WHITE),
        ).arrange(RIGHT, buff=0.18).move_to(np.array([0.0, -1.65, 0.0]))
        n_label[1].add_updater(
            lambda m: m.set_value(round(n_track.get_value()))
        )

        p_name = MathTex(r"P_n", font_size=36, color=C_PERIM)
        p_name.move_to(np.array([-3.35, ROW_P_Y, 0.0]))
        p_value = DecimalNumber(
            perimeter(0), num_decimal_places=2, font_size=34, color=C_PERIM
        )
        p_value.add_updater(lambda m: m.set_value(p_track.get_value()))
        p_value.add_updater(
            lambda m: m.move_to(np.array([-2.45, ROW_P_Y, 0.0]))
        )

        a_name = MathTex(r"A_n", font_size=36, color=C_AREA)
        a_name.move_to(np.array([-3.35, ROW_A_Y, 0.0]))
        a_value = DecimalNumber(
            area(0), num_decimal_places=3, font_size=34, color=C_AREA
        )
        a_value.add_updater(lambda m: m.set_value(a_track.get_value()))
        a_value.add_updater(
            lambda m: m.move_to(np.array([-2.45, ROW_A_Y, 0.0]))
        )

        p_bar = bar(p_track, perimeter(0), C_PERIM)
        a_bar = bar(a_track, area(0), C_AREA)

        formulas = VGroup(
            MathTex(r"P_n = 3\left(\tfrac{4}{3}\right)^{n}",
                    font_size=34, color=C_PERIM),
            MathTex(r"A_n = A_0\left[1 + \tfrac{3}{5}\left(1 - "
                    r"\left(\tfrac{4}{9}\right)^{n}\right)\right]",
                    font_size=30, color=C_AREA),
        ).arrange(DOWN, buff=0.3).move_to(np.array([0.0, -5.15, 0.0]))

        self.play(
            FadeIn(n_label), FadeIn(p_name), FadeIn(a_name),
            FadeIn(p_value), FadeIn(a_value),
            FadeIn(p_bar), FadeIn(a_bar),
            Write(formulas[0]),
            run_time=0.9,
        )
        self.play(Write(formulas[1]), run_time=0.7)
        # El area se rellena: a partir de aqui el copo ES una superficie.
        self.play(flake.animate.set_fill(C_AREA, opacity=0.22), run_time=0.5)
        self.wait(0.5)

        # Una iteracion por golpe: figura, contadores y barras se mueven juntos.
        for n in range(1, MAX_ITER + 1):
            target = flakes[n].copy().set_fill(C_AREA, opacity=0.22)
            self.play(
                Transform(flake, target),
                n_track.animate.set_value(n),
                p_track.animate.set_value(perimeter(n)),
                a_track.animate.set_value(area(n)),
                run_time=0.85,
                rate_func=rate_functions.ease_in_out_sine,
            )
            self.wait(0.35)

        # El veredicto de cada serie, uno al lado del otro.
        verdict_p = Tex(r"$\rightarrow \infty$", font_size=38, color=C_PERIM)
        verdict_p.move_to(np.array([2.9, ROW_P_Y, 0.0]))
        verdict_a = Tex(r"$\rightarrow \tfrac{8}{5}A_0$", font_size=34,
                        color=C_AREA)
        verdict_a.move_to(np.array([2.9, ROW_A_Y, 0.0]))
        self.play(
            FadeIn(verdict_p, shift=LEFT * 0.3),
            FadeIn(verdict_a, shift=LEFT * 0.3),
            run_time=0.7,
        )
        self.play(
            Indicate(p_bar, color=C_PERIM, scale_factor=1.06),
            Indicate(a_bar, color=C_AREA, scale_factor=1.06),
            run_time=0.9,
        )
        self.wait(0.9)

        # Por que una diverge y la otra no: razon 4/3 contra razon 4/9.
        reason = VGroup(
            MathTex(r"\left(\tfrac{4}{3}\right)^{n} \rightarrow \infty",
                    font_size=34, color=C_PERIM),
            MathTex(r"\sum \left(\tfrac{4}{9}\right)^{n} < \infty",
                    font_size=34, color=C_AREA),
        ).arrange(RIGHT, buff=0.7).move_to(np.array([0.0, -5.15, 0.0]))
        self.play(
            FadeOut(formulas), FadeIn(reason, shift=UP * 0.2), run_time=0.7
        )
        self.wait(1.2)

        # -------------------------------------------- beat 4: dimension fractal
        p_value.clear_updaters()
        a_value.clear_updaters()
        counters = VGroup(
            n_label, p_name, a_name, p_value, a_value, p_bar, a_bar,
            verdict_p, verdict_a, reason,
        )
        self.play(FadeOut(counters), FadeOut(flake), run_time=0.6)

        # Sin signos de apertura ni acentos: el template no lleva inputenc.
        dim_title = Tex(r"Su dimension no es un numero entero",
                        font_size=36, color=C_DIM)
        dim_title.move_to(np.array([0.0, 4.6, 0.0]))
        self.play(Write(dim_title), run_time=0.7)

        # La curva de nivel 4 se parte exactamente en 4 copias de nivel 3, cada
        # una a escala 1/3: los indices de los puntos hacen el corte solo.
        curve_pts = koch_curve(
            np.array([-3.4, 2.2, 0.0]), np.array([3.4, 2.2, 0.0]), 4
        )
        block = 4 ** 3
        colors = [C_AREA, C_RULE, C_PERIM, C_DIM]
        copies = VGroup(*[
            as_vmobject(
                curve_pts[i * block: (i + 1) * block + 1], colors[i], 4.0
            )
            for i in range(4)
        ])
        self.play(Create(copies), run_time=1.2)
        self.play(
            *[Indicate(c, color=colors[i], scale_factor=1.0)
              for i, c in enumerate(copies)],
            run_time=0.8,
        )

        selfsim = Tex(
            r"4 copias de si misma, a escala $\tfrac{1}{3}$",
            font_size=34, color=WHITE,
        ).move_to(np.array([0.0, -0.45, 0.0]))  # bajo las puntas (y_min = 0.24)
        self.play(FadeIn(selfsim, shift=UP * 0.2), run_time=0.6)

        # N = r^{-D}  =>  D = log N / log(1/r).
        dim = MathTex(
            r"D = \frac{\log 4}{\log 3}", r"= 1{,}2619\ldots",
            font_size=44,
        )
        dim[0].set_color(C_DIM)
        dim[1].set_color(WHITE)
        dim.arrange(RIGHT, buff=0.25).move_to(np.array([0.0, -2.2, 0.0]))
        self.play(Write(dim[0]), run_time=0.8)
        self.play(FadeIn(dim[1], shift=RIGHT * 0.2), run_time=0.6)

        box = SurroundingRectangle(dim, buff=0.2, corner_radius=0.12)
        box.set_stroke(width=4, color=[C_AREA, C_DIM])
        self.play(Create(box), run_time=0.6)

        closing = VGroup(
            Tex(r"Ni linea (1) ni superficie (2):", font_size=34, color=WHITE),
            Tex(r"algo intermedio.", font_size=34, color=C_DIM),
        ).arrange(DOWN, buff=0.25).move_to(np.array([0.0, -4.3, 0.0]))
        self.play(FadeIn(closing, shift=UP * 0.25), run_time=0.7)
        self.wait(1.6)

        animate_End(scene=self)
