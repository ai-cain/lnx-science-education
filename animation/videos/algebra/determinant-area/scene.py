from manim import *
from lnx import *

# visual-derivation | algebra lineal | intermediate
# El determinante ES el factor de area.
#
# En el colegio el determinante se aprende como una receta: ad - bc. Pero esa
# resta no sale de la nada: es exactamente el area del paralelogramo que generan
# las columnas de la matriz, es decir, en cuanto se estira (o se encoge) el area
# de CUALQUIER figura al aplicar la transformacion.
#
# La matriz protagonista es
#       A = [[3, 1], [1, 2]],   det A = 3*2 - 1*1 = 5.
# Sus columnas son las imagenes de los vectores base: i=(1,0) -> (3,1) y
# j=(0,1) -> (1,2). El cuadrado unitario (area 1) se convierte en el
# paralelogramo generado por esas columnas (area 5).
#
# Para MEDIR ese area sin formulas se usa Cavalieri: deslizar el lado superior
# paralelo a la base no cambia el area. Con el deslizamiento
#       u = (3,1)  ->  u - v = (2,-1),   con v = (1,2),
# y como (2,-1).(1,2) = 0, el paralelogramo se vuelve un cuadrado recto de lado
# |v| = sqrt(5). Area = sqrt(5)*sqrt(5) = 5. Cinco cuadrados unitarios, sin
# haber usado la receta.
#
# Los dos casos limite son lo que hace memorable el video:
#   det = 0 con [[2,1],[4,2]]  ->  2*2 - 1*4 = 0: el plano entero colapsa sobre
#     la recta y = 2x. Area cero, informacion perdida, no hay inversa.
#   det < 0 con [[0,1],[1,0]]  ->  0*0 - 1*1 = -1: el plano se voltea. El signo
#     es la orientacion, y se ve con una figura asimetrica (una L).
#
# El frame real mide 9 x 16 unidades (x en [-4.5, 4.5], y en [-8, 8]).
# Zona segura: |y| <= 5.6 y |x| <= 3.8.

SAFE_WIDTH = 7.2

# Una sola unidad de rejilla para TODO el video. Al ser igual en x y en y, una
# matriz aplicada con ApplyMatrix sobre puntos de escena coincide exactamente
# con la misma matriz aplicada sobre coordenadas del plano: sin esta igualdad
# la deformacion se veria distorsionada.
UNIT = 0.85

# El origen no va al centro del frame: se baja y se corre a la izquierda para
# que el paralelogramo generado por (3,1) y (1,2), que crece hacia arriba y a la
# derecha, quede centrado en la zona segura.
PLANE_ORIGIN = np.array([-1.3, -1.15, 0.0])


def fit_to_safe_width(mobject):
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def make_label(tex, font_size, color, with_background=True):
    """MathTex con fondo opcional, para que se lea encima de la rejilla."""
    label = MathTex(tex, font_size=font_size, color=color)
    if with_background:
        label.add_background_rectangle(color=BG, opacity=0.92, buff=0.06)
    label.set_z_index(12)
    return label


def P(x, y):
    """Coordenada del plano -> punto de escena (independiente de los mobjects).

    Se calcula a mano y no con plane.c2p porque despues de deformar el plano con
    ApplyMatrix el sistema de coordenadas del NumberPlane ya no es confiable.
    """
    return PLANE_ORIGIN + np.array([x * UNIT, y * UNIT, 0.0])


class DeterminantArea(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.14
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.85)
        self.add(watermark)

        I_COLOR = ACCENT_CYAN        # primera columna, imagen de i
        J_COLOR = ACCENT_MAGENTA     # segunda columna, imagen de j
        AREA_COLOR = ACCENT_YELLOW   # el area, protagonista del video
        DET_COLOR = ACCENT_PURPLE    # el numero det A
        WARN_COLOR = "#FF8A00"       # reservado para los dos casos limite

        def make_plane():
            """Rejilla nueva y sin deformar, siempre con el mismo origen."""
            plane = NumberPlane(
                x_range=[-7, 7, 1],
                y_range=[-8, 9, 1],
                x_length=14 * UNIT,
                y_length=17 * UNIT,
                background_line_style={
                    "stroke_color": GREY_B,
                    "stroke_width": 1.6,
                    "stroke_opacity": 0.35,
                },
                axis_config={
                    "stroke_color": GREY_A,
                    "stroke_width": 2.5,
                    "include_ticks": False,
                },
            )
            plane.shift(PLANE_ORIGIN - plane.c2p(0, 0))
            plane.set_z_index(-5)
            return plane

        def polygon(points, color, opacity=0.35):
            poly = Polygon(
                *[P(x, y) for x, y in points],
                stroke_color=color, stroke_width=5,
                fill_color=color, fill_opacity=opacity,
            )
            poly.set_z_index(2)
            return poly

        def vector(x, y, color):
            arrow = Arrow(
                P(0, 0), P(x, y), buff=0,
                color=color, stroke_width=7,
                max_tip_length_to_length_ratio=0.22,
            )
            arrow.set_z_index(6)
            return arrow

        # ------------------------------------------------------------ hook 0-2s
        # Antes de cualquier explicacion: la rejilla se deforma de golpe y el
        # cuadrado unitario amarillo se estira. Eso es todo el video en 2 s.
        title = Tex(r"El Determinante", font_size=62, color=WHITE)
        title.set_stroke(width=1)
        title.set_z_index(20)
        title.move_to(UP * 5.45)
        fit_to_safe_width(title)

        underline = Line(
            title.get_left() + DOWN * 0.3,
            title.get_right() + DOWN * 0.3,
            stroke_width=4,
        )
        underline.set_color(color=[ACCENT_CYAN, ACCENT_MAGENTA])
        underline.set_z_index(20)

        plane = make_plane()
        unit_square = polygon([(0, 0), (1, 0), (1, 1), (0, 1)], AREA_COLOR, 0.45)

        self.add(plane, unit_square)
        self.play(Write(title), run_time=0.7)
        self.play(Create(underline), run_time=0.35)

        A = np.array([[3, 1], [1, 2]])
        hook_group = VGroup(plane, unit_square)
        self.play(
            ApplyMatrix(A, hook_group, about_point=P(0, 0)),
            run_time=1.1,
        )
        self.wait(0.5)

        hook_line = Tex(
            r"un n\'umero que dice\\cu\'anto se estira el \'area",
            font_size=32, color=GREY_A,
        )
        hook_line.set_z_index(20)
        hook_line.move_to(DOWN * 4.9)
        fit_to_safe_width(hook_line)
        self.play(FadeIn(hook_line, shift=UP * 0.15), run_time=0.6)
        self.wait(0.8)

        # ------------------------------------------------ beat 1: la matriz A
        # Se vuelve al plano sin deformar para contar la historia despacio.
        self.play(FadeOut(hook_group), FadeOut(hook_line), run_time=0.5)

        plane = make_plane()
        self.play(FadeIn(plane), run_time=0.5)

        matrix_tex = MathTex(
            r"A=\begin{pmatrix} 3 & 1 \\ 1 & 2 \end{pmatrix}",
            font_size=48,
        )
        # Cada columna se pinta con el color del vector base que le corresponde:
        # asi la matriz deja de ser un bloque de numeros y se lee como "las dos
        # flechas de la pantalla".
        matrix_tex[0][3].set_color(I_COLOR)   # 3
        matrix_tex[0][5].set_color(I_COLOR)   # 1 (abajo izquierda)
        matrix_tex[0][4].set_color(J_COLOR)   # 1 (arriba derecha)
        matrix_tex[0][6].set_color(J_COLOR)   # 2
        matrix_tex.set_stroke(width=1)
        matrix_tex.set_z_index(20)
        matrix_tex.move_to(UP * 4.35)
        fit_to_safe_width(matrix_tex)
        self.play(Write(matrix_tex), run_time=0.9)

        # Los vectores base y su imagen: la matriz solo dice a donde van i y j.
        i_hat = vector(1, 0, I_COLOR)
        j_hat = vector(0, 1, J_COLOR)
        unit_square = polygon([(0, 0), (1, 0), (1, 1), (0, 1)], AREA_COLOR, 0.45)
        area_one = make_label(r"\text{\'area}=1", 30, AREA_COLOR)
        area_one.move_to(P(0.5, 0.5))

        self.play(GrowArrow(i_hat), GrowArrow(j_hat), run_time=0.7)
        self.play(FadeIn(unit_square), run_time=0.5)
        self.bring_to_back(unit_square)
        self.play(Write(area_one), run_time=0.5)
        self.wait(0.6)

        # Deformacion completa: rejilla, vectores y cuadrado se mueven juntos.
        i_image = vector(3, 1, I_COLOR)
        j_image = vector(1, 2, J_COLOR)
        parallelogram = polygon([(0, 0), (3, 1), (4, 3), (1, 2)], AREA_COLOR, 0.30)
        deformed_plane = make_plane().apply_matrix(A, about_point=P(0, 0))

        self.play(FadeOut(area_one), run_time=0.3)
        self.play(
            Transform(plane, deformed_plane),
            Transform(i_hat, i_image),
            Transform(j_hat, j_image),
            Transform(unit_square, parallelogram),
            run_time=1.6,
        )

        i_label = make_label(r"(3,1)", 30, I_COLOR).move_to(P(3.05, 0.45))
        j_label = make_label(r"(1,2)", 30, J_COLOR).move_to(P(0.35, 2.25))
        self.play(Write(i_label), Write(j_label), run_time=0.7)

        columns_text = Tex(
            r"las columnas de $A$ son\\a d\'onde van $\hat{\imath}$ y $\hat{\jmath}$",
            font_size=30, color=WHITE,
        )
        columns_text.set_z_index(20)
        columns_text.move_to(DOWN * 4.55)
        fit_to_safe_width(columns_text)
        self.play(FadeIn(columns_text, shift=UP * 0.15), run_time=0.6)
        self.wait(1.0)

        # ------------------------------------- beat 2: medir el paralelogramo
        # Cavalieri: deslizar el lado de arriba paralelo a la base no cambia el
        # area. Se desliza u = (3,1) hasta u - v = (2,-1), que es perpendicular a
        # v = (1,2). El paralelogramo se endereza y queda un cuadrado de lado
        # sqrt(5): area 5, medida sin usar ninguna receta.
        self.play(
            FadeOut(columns_text), FadeOut(i_label), FadeOut(j_label),
            FadeOut(i_hat), FadeOut(j_hat), FadeOut(plane),
            run_time=0.5,
        )
        plane = make_plane().apply_matrix(A, about_point=P(0, 0))
        plane.set_stroke(opacity=0.18)
        self.add(plane)

        shear = ValueTracker(0.0)

        def sheared_points(t):
            ux, uy = 3 - t * 1, 1 - t * 2
            return [(0, 0), (ux, uy), (ux + 1, uy + 2), (1, 2)]

        moving = polygon(sheared_points(0.0), AREA_COLOR, 0.30)
        moving.add_updater(
            lambda m: m.become(polygon(sheared_points(shear.get_value()), AREA_COLOR, 0.30))
        )
        self.remove(unit_square)
        self.add(moving)

        base_line = Line(P(0, 0), P(1, 2), color=J_COLOR, stroke_width=6)
        base_line.set_z_index(7)
        slide_rail = DashedLine(P(2, -1), P(4.2, 3.4), color=GREY_B, stroke_width=2)
        slide_rail.set_z_index(1)

        cavalieri = Tex(
            r"deslizar el lado paralelo\\a la base no cambia el \'area",
            font_size=30, color=WHITE,
        )
        cavalieri.set_z_index(20)
        cavalieri.move_to(DOWN * 4.55)
        fit_to_safe_width(cavalieri)

        self.play(Create(base_line), Create(slide_rail), run_time=0.6)
        self.play(FadeIn(cavalieri, shift=UP * 0.15), run_time=0.5)
        self.play(shear.animate.set_value(1.0), run_time=1.8)
        moving.clear_updaters()

        # Ya es un cuadrado recto: se marca el angulo recto y los dos lados.
        right_angle = RightAngle(
            Line(P(0, 0), P(1, 2)), Line(P(0, 0), P(2, -1)),
            length=0.22, color=WARN_COLOR, stroke_width=4,
        )
        right_angle.set_z_index(9)
        side_a = make_label(r"\sqrt{5}", 28, WHITE).move_to(P(0.2, 1.25))
        side_b = make_label(r"\sqrt{5}", 28, WHITE).move_to(P(1.35, -0.75))
        self.play(Create(right_angle), Write(side_a), Write(side_b), run_time=0.8)

        area_five = MathTex(r"\sqrt{5}\cdot\sqrt{5}=5", font_size=42, color=AREA_COLOR)
        area_five.set_stroke(width=1)
        area_five.set_z_index(20)
        area_five.move_to(DOWN * 3.35)
        self.play(FadeOut(cavalieri), run_time=0.3)
        self.play(Write(area_five), run_time=0.8)
        self.wait(0.5)

        # El conteo explicito: cinco cuadrados unitarios caben en esa area.
        tally = VGroup(*[
            Square(side_length=UNIT, stroke_color=AREA_COLOR, stroke_width=3,
                   fill_color=AREA_COLOR, fill_opacity=0.45)
            for _ in range(5)
        ])
        tally.arrange(RIGHT, buff=0.12)
        tally.move_to(DOWN * 4.5)
        tally.set_z_index(20)
        self.play(
            LaggedStart(*[FadeIn(sq, scale=0.6) for sq in tally], lag_ratio=0.35),
            run_time=1.6,
        )
        count_text = Tex(r"5 cuadrados unitarios", font_size=30, color=GREY_A)
        count_text.set_z_index(20)
        count_text.next_to(tally, DOWN, buff=0.22)
        self.play(FadeIn(count_text), run_time=0.5)
        self.wait(0.7)

        # Recien ahora aparece la receta, y ya no es una receta.
        det_tex = MathTex(
            r"\det A = 3\cdot 2 - 1\cdot 1 = ", r"5",
            font_size=42,
        )
        det_tex[1].set_color(AREA_COLOR)
        det_tex[0].set_color(DET_COLOR)
        det_tex.set_stroke(width=1)
        det_tex.set_z_index(20)
        det_tex.move_to(DOWN * 3.35)
        fit_to_safe_width(det_tex)

        self.play(
            FadeOut(tally), FadeOut(count_text),
            ReplacementTransform(area_five, det_tex),
            run_time=1.0,
        )
        self.wait(1.0)

        # --------------------------------- beat 3: sirve para cualquier figura
        # El factor 5 no es del cuadrado unitario: es de la transformacion. Un
        # circulo cualquiera tambien multiplica su area por 5.
        self.play(
            FadeOut(moving), FadeOut(base_line), FadeOut(slide_rail),
            FadeOut(right_angle), FadeOut(side_a), FadeOut(side_b),
            FadeOut(plane), FadeOut(det_tex),
            run_time=0.5,
        )

        plane = make_plane()
        blob = Circle(radius=0.9 * UNIT, color=ACCENT_CYAN, stroke_width=5)
        blob.set_fill(ACCENT_CYAN, opacity=0.30)
        blob.move_to(P(0.6, 0.6))
        blob.set_z_index(3)

        any_shape = Tex(r"y no solo el cuadrado:\\cualquier figura",
                        font_size=32, color=WHITE)
        any_shape.set_z_index(20)
        any_shape.move_to(DOWN * 4.55)
        fit_to_safe_width(any_shape)

        self.play(FadeIn(plane), FadeIn(blob), run_time=0.6)
        self.play(FadeIn(any_shape, shift=UP * 0.15), run_time=0.5)
        self.wait(0.4)

        self.play(
            ApplyMatrix(A, VGroup(plane, blob), about_point=P(0, 0)),
            run_time=1.6,
        )
        factor = MathTex(r"\text{\'area}\times 5", font_size=44, color=AREA_COLOR)
        factor.set_stroke(width=1)
        factor.set_z_index(20)
        factor.move_to(DOWN * 3.35)
        self.play(Write(factor), run_time=0.7)
        self.wait(1.0)

        # ------------------------------------------- beat 4a: det = 0, colapso
        # [[2,1],[4,2]]: la segunda columna es la mitad de la primera, asi que
        # todo el plano cae sobre la recta y = 2x. Area cero: se perdio una
        # dimension entera y por eso no existe inversa.
        self.play(
            FadeOut(plane), FadeOut(blob), FadeOut(any_shape),
            FadeOut(factor), FadeOut(matrix_tex),
            run_time=0.5,
        )

        matrix_zero = MathTex(
            r"B=\begin{pmatrix} 2 & 1 \\ 4 & 2 \end{pmatrix}",
            font_size=48, color=WHITE,
        )
        matrix_zero.set_stroke(width=1)
        matrix_zero.set_z_index(20)
        matrix_zero.move_to(UP * 4.35)
        fit_to_safe_width(matrix_zero)

        plane = make_plane()
        blob = Circle(radius=0.9 * UNIT, color=ACCENT_CYAN, stroke_width=5)
        blob.set_fill(ACCENT_CYAN, opacity=0.30)
        blob.move_to(P(0.6, 0.6))
        blob.set_z_index(3)
        square_zero = polygon([(0, 0), (1, 0), (1, 1), (0, 1)], AREA_COLOR, 0.45)

        self.play(Write(matrix_zero), FadeIn(plane), run_time=0.8)
        self.play(FadeIn(blob), FadeIn(square_zero), run_time=0.5)

        B = np.array([[2, 1], [4, 2]])
        self.play(
            ApplyMatrix(B, VGroup(plane, blob, square_zero), about_point=P(0, 0)),
            run_time=1.8,
        )
        det_zero = MathTex(r"\det B = 2\cdot 2 - 1\cdot 4 = ", r"0", font_size=40)
        det_zero[0].set_color(WHITE)
        det_zero[1].set_color(WARN_COLOR)
        det_zero.set_stroke(width=1)
        det_zero.set_z_index(20)
        det_zero.move_to(DOWN * 3.35)
        fit_to_safe_width(det_zero)
        collapse_text = Tex(
            r"todo el plano cae en una recta:\\\'area cero, no hay inversa",
            font_size=30, color=WARN_COLOR,
        )
        collapse_text.set_z_index(20)
        collapse_text.move_to(DOWN * 4.6)
        fit_to_safe_width(collapse_text)

        self.play(Write(det_zero), run_time=0.7)
        self.play(FadeIn(collapse_text, shift=UP * 0.15), run_time=0.6)
        self.wait(1.2)

        # ------------------------------------ beat 4b: det < 0, la orientacion
        # [[0,1],[1,0]] intercambia i y j: refleja el plano respecto de y = x.
        # Con una L asimetrica el espejo es imposible de no ver.
        self.play(
            FadeOut(plane), FadeOut(blob), FadeOut(square_zero),
            FadeOut(det_zero), FadeOut(collapse_text), FadeOut(matrix_zero),
            run_time=0.5,
        )

        matrix_flip = MathTex(
            r"C=\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}",
            font_size=48, color=WHITE,
        )
        matrix_flip.set_stroke(width=1)
        matrix_flip.set_z_index(20)
        matrix_flip.move_to(UP * 4.35)
        fit_to_safe_width(matrix_flip)

        plane = make_plane()
        ele = polygon(
            [(0.3, 0.3), (1.8, 0.3), (1.8, 0.9), (0.9, 0.9), (0.9, 2.4), (0.3, 2.4)],
            ACCENT_YELLOW, 0.40,
        )
        mirror = DashedLine(P(-1.6, -1.6), P(3.2, 3.2), color=GREY_B, stroke_width=2)
        mirror.set_z_index(1)

        self.play(Write(matrix_flip), FadeIn(plane), run_time=0.8)
        self.play(FadeIn(ele), Create(mirror), run_time=0.6)
        self.wait(0.3)

        C = np.array([[0, 1], [1, 0]])
        self.play(
            ApplyMatrix(C, VGroup(plane, ele), about_point=P(0, 0)),
            run_time=1.6,
        )
        det_flip = MathTex(r"\det C = 0\cdot 0 - 1\cdot 1 = ", r"-1", font_size=40)
        det_flip[0].set_color(WHITE)
        det_flip[1].set_color(WARN_COLOR)
        det_flip.set_stroke(width=1)
        det_flip.set_z_index(20)
        det_flip.move_to(DOWN * 3.35)
        fit_to_safe_width(det_flip)
        flip_text = Tex(
            r"el signo negativo es\\el plano dado vuelta",
            font_size=30, color=WARN_COLOR,
        )
        flip_text.set_z_index(20)
        flip_text.move_to(DOWN * 4.6)
        fit_to_safe_width(flip_text)

        self.play(Write(det_flip), run_time=0.7)
        self.play(FadeIn(flip_text, shift=UP * 0.15), run_time=0.6)
        self.wait(1.2)

        # ----------------------------------------------------------- conclusion
        self.play(
            FadeOut(plane), FadeOut(ele), FadeOut(mirror),
            FadeOut(det_flip), FadeOut(flip_text), FadeOut(matrix_flip),
            run_time=0.6,
        )

        closing = VGroup(
            MathTex(r"|\det A| = \text{factor de \'area}", font_size=40),
            MathTex(r"\text{signo} = \text{orientaci\'on}", font_size=40),
        )
        closing[0].set_color(AREA_COLOR)
        closing[1].set_color(ACCENT_CYAN)
        closing.arrange(DOWN, buff=0.55)
        closing.set_stroke(width=1)
        closing.set_z_index(21)
        closing.move_to(ORIGIN)
        fit_to_safe_width(closing)

        self.play(Write(closing[0]), run_time=0.9)
        self.play(Write(closing[1]), run_time=0.9)

        result_box = SurroundingRectangle(closing, buff=0.3, corner_radius=0.14)
        result_box.set_stroke(width=4, color=[ACCENT_YELLOW, ACCENT_PURPLE])
        result_box.set_z_index(20)
        self.play(Create(result_box), run_time=0.7)
        self.wait(1.8)

        animate_End(scene=self)
