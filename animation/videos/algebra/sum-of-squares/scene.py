from manim import *
from lnx import *

# proof-without-words | algebra | intermediate
#
# 1^2 + 2^2 + 3^2 + ... + n^2 = n(n+1)(2n+1)/6
#
# Se usa la version 2D del argumento de las tres piramides (mucho mas limpia de
# animar en vertical que el prisma 3D, y demuestra exactamente lo mismo).
#
# Se arma un triangulo escalonado T1 con n filas, donde la fila i tiene i celdas
# y en TODAS ellas se escribe el numero i:
#
#           1
#          2 2
#         3 3 3
#        4 4 4 4
#
# La suma de todas las celdas de T1 es 1*1 + 2*2 + ... + n*n = S, la suma de
# cuadrados que se quiere calcular.
#
# T2 y T3 son el MISMO triangulo girado 120 y 240 grados. En coordenadas
# (i = fila, j = posicion dentro de la fila, con 1 <= j <= i):
#
#       T1[i][j] = i
#       T2[i][j] = n - i + j
#       T3[i][j] = n + 1 - j
#
# Al sumar celda a celda:
#       i + (n - i + j) + (n + 1 - j) = 2n + 1     <-- constante, siempre
#
# O sea, el triangulo suma es un triangulo lleno de (2n+1). Como el triangulo
# tiene 1 + 2 + ... + n = n(n+1)/2 celdas:
#
#       3S = [n(n+1)/2] * (2n+1)   =>   S = n(n+1)(2n+1)/6
#
# El 6 del denominador = 3 copias * el 2 del numero triangular.
#
# VERIFICACION NUMERICA (n = 4, el caso que se anima):
#   S      = 1 + 4 + 9 + 16 = 30
#   celdas = 4*5/2 = 10 ; 2n+1 = 9 ; 10 * 9 = 90 = 3 * 30   OK
#   formula: 4*5*9/6 = 180/6 = 30                            OK
#   (n = 10) S = 385 ; 10*11*21/6 = 2310/6 = 385             OK
#
# El frame real mide 9 x 16 unidades. Zona segura: |x| <= 3.8, |y| <= 5.6.

SAFE_WIDTH = 7.2

N = 4                 # numero de filas del triangulo escalonado
CONST = 2 * N + 1     # 9 : valor constante de cada celda del triangulo suma
CELLS = N * (N + 1) // 2   # 10 : celdas del triangulo
TOTAL = CELLS * CONST      # 90 : el triple de la suma de cuadrados


def fit_to_safe_width(mobject):
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def t1_value(i, j):
    """Triangulo original: toda la fila i vale i."""
    return i


def t2_value(i, j):
    """Copia girada 120 grados."""
    return N - i + j


def t3_value(i, j):
    """Copia girada 240 grados."""
    return N + 1 - j


def const_value(i, j):
    """Triangulo suma: siempre 2n+1."""
    return CONST


class SumOfSquares(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        T1_COLOR = ACCENT_CYAN
        T2_COLOR = ACCENT_MAGENTA
        T3_COLOR = ACCENT_PURPLE
        RESULT_COLOR = ACCENT_YELLOW

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.14
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.85)
        watermark.set_z_index(30)
        self.add(watermark)

        # ------------------------------------------------------- constructores
        def make_cell(value, color, cell, font_size):
            """Una celda: cuadrado de color con su numero encima."""
            square = Square(side_length=cell)
            square.set_stroke(color=color, width=2.5)
            square.set_fill(color=color, opacity=0.28)
            square.set_z_index(2)
            label = MathTex(str(value), font_size=font_size, color=WHITE)
            label.set_z_index(6)
            label.move_to(square.get_center())
            return VGroup(square, label)

        def make_triangle(value_fn, color, cell=0.5, font_size=26):
            """Triangulo escalonado: la fila i tiene i celdas, centradas."""
            rows = VGroup()
            for i in range(1, N + 1):
                row = VGroup()
                for j in range(1, i + 1):
                    piece = make_cell(value_fn(i, j), color, cell, font_size)
                    piece.move_to(
                        RIGHT * ((j - (i + 1) / 2) * cell)
                        + DOWN * ((i - 1) * cell)
                    )
                    row.add(piece)
                rows.add(row)
            rows.move_to(ORIGIN)
            return rows

        def caption(tex, color=WHITE, font_size=30, y=-4.7):
            text = Tex(tex, font_size=font_size, color=color)
            text.set_z_index(20)
            text.move_to(UP * y)
            return fit_to_safe_width(text)

        # ------------------------------------------------------------ hook 0-2s
        # Arranca directo con la pregunta y cuatro cuadrados que crecen: se ve
        # de inmediato que "n al cuadrado" es literalmente un cuadrado.
        question = MathTex(
            r"1^2+2^2+3^2+\cdots+n^2 \;=\; ?",
            font_size=46, color=WHITE,
        )
        question.set_stroke(width=1)
        question.set_z_index(20)
        question.move_to(UP * 5.2)
        fit_to_safe_width(question)

        demo_squares = VGroup()
        for k in range(1, N + 1):
            block = VGroup()
            for a in range(k):
                for b in range(k):
                    unit = Square(side_length=0.3)
                    unit.set_stroke(color=T1_COLOR, width=2)
                    unit.set_fill(color=T1_COLOR, opacity=0.30)
                    unit.move_to(RIGHT * a * 0.3 + DOWN * b * 0.3)
                    block.add(unit)
            demo_squares.add(block)
        for block in demo_squares:
            block.set_z_index(2)
        demo_squares.arrange(RIGHT, buff=0.32, aligned_edge=DOWN)
        demo_squares.move_to(UP * 2.6)
        fit_to_safe_width(demo_squares)

        self.play(Write(question), run_time=0.8)
        self.play(
            LaggedStart(
                *[GrowFromEdge(block, DOWN) for block in demo_squares],
                lag_ratio=0.25,
            ),
            run_time=1.1,
        )

        counts = VGroup()
        for k, block in enumerate(demo_squares, start=1):
            tag = MathTex(f"{k*k}", font_size=30, color=T1_COLOR)
            tag.set_z_index(20)
            tag.next_to(block, DOWN, buff=0.22)
            counts.add(tag)
        self.play(LaggedStart(*[FadeIn(t) for t in counts], lag_ratio=0.2),
                  run_time=0.8)

        hook_line = caption(
            r"sin f\'ormula, solo contando", color=GREY_A, y=0.6)
        self.play(FadeIn(hook_line, shift=UP * 0.15), run_time=0.5)
        self.wait(0.7)

        # --------------------------------------------- beat 1: el triangulo T1
        # Cada cuadrado k x k se reordena como una fila de k celdas que valen k.
        # El triangulo entero suma exactamente S = 1^2 + 2^2 + ... + n^2.
        self.play(
            FadeOut(demo_squares), FadeOut(counts), FadeOut(hook_line),
            run_time=0.5,
        )

        big_cell = 0.72
        triangle = make_triangle(t1_value, T1_COLOR, cell=big_cell, font_size=34)
        triangle.move_to(UP * 1.3)

        self.play(
            LaggedStart(
                *[FadeIn(row, shift=DOWN * 0.2) for row in triangle],
                lag_ratio=0.3,
            ),
            run_time=1.4,
        )

        rule_text = caption(
            r"la fila $i$ tiene $i$ celdas\\y cada una vale $i$",
            font_size=32, y=-1.5,
        )
        self.play(FadeIn(rule_text, shift=UP * 0.15), run_time=0.6)
        self.wait(0.6)

        sum_text = MathTex(
            r"S=1^2+2^2+3^2+4^2=", r"30",
            font_size=38,
        )
        sum_text[0].set_color(WHITE)
        sum_text[1].set_color(T1_COLOR)
        sum_text.set_stroke(width=1)
        sum_text.set_z_index(20)
        sum_text.move_to(DOWN * 3.1)
        fit_to_safe_width(sum_text)
        self.play(Write(sum_text), run_time=0.9)
        self.wait(0.8)

        # ------------------------------------------- beat 2: las otras dos copias
        # T2 y T3 son el mismo triangulo girado 120 y 240 grados.
        self.play(
            FadeOut(rule_text),
            FadeOut(sum_text),
            run_time=0.4,
        )

        small_cell = 0.5
        tri1 = make_triangle(t1_value, T1_COLOR, cell=small_cell)
        tri2 = make_triangle(t2_value, T2_COLOR, cell=small_cell)
        tri3 = make_triangle(t3_value, T3_COLOR, cell=small_cell)

        plus_a = MathTex("+", font_size=40, color=GREY_A)
        plus_b = MathTex("+", font_size=40, color=GREY_A)
        for sign in (plus_a, plus_b):
            sign.set_z_index(20)

        row_group = VGroup(tri1, plus_a, tri2, plus_b, tri3)
        row_group.arrange(RIGHT, buff=0.24)
        row_group.move_to(UP * 2.2)
        fit_to_safe_width(row_group)

        self.play(ReplacementTransform(triangle, tri1), run_time=0.9)

        copies_text = caption(
            r"el mismo tri\'angulo,\\girado $120^\circ$ y $240^\circ$",
            font_size=32, y=0.15,
        )
        self.play(FadeIn(copies_text, shift=UP * 0.15), run_time=0.5)
        self.play(
            FadeIn(plus_a), FadeIn(tri2, shift=LEFT * 0.3),
            run_time=0.7,
        )
        self.play(
            FadeIn(plus_b), FadeIn(tri3, shift=LEFT * 0.3),
            run_time=0.7,
        )
        self.wait(0.8)

        # ------------------------------------- beat 3: sumar celda a celda -> 9
        # i + (n-i+j) + (n+1-j) = 2n+1 en TODA celda: el milagro del video.
        cell_sum = MathTex(
            r"i", r"+", r"(n-i+j)", r"+", r"(n+1-j)", r"=", r"2n+1",
            font_size=34,
        )
        cell_sum[0].set_color(T1_COLOR)
        cell_sum[2].set_color(T2_COLOR)
        cell_sum[4].set_color(T3_COLOR)
        cell_sum[6].set_color(RESULT_COLOR)
        cell_sum.set_stroke(width=1)
        cell_sum.set_z_index(20)
        cell_sum.move_to(DOWN * 1.1)
        fit_to_safe_width(cell_sum)

        self.play(FadeOut(copies_text), run_time=0.3)
        self.play(Write(cell_sum), run_time=1.1)
        self.wait(0.7)

        result_tri = make_triangle(
            const_value, RESULT_COLOR, cell=0.72, font_size=34)
        result_tri.move_to(DOWN * 3.0)

        self.play(
            TransformFromCopy(row_group, result_tri),
            run_time=1.5,
        )
        every_cell = caption(
            r"toda celda queda en $2n+1=9$",
            color=RESULT_COLOR, font_size=32, y=-5.0,
        )
        self.play(FadeIn(every_cell, shift=UP * 0.15), run_time=0.5)
        self.wait(1.0)

        # ------------------------------------------------ beat 4: el conteo final
        self.play(
            FadeOut(row_group), FadeOut(cell_sum), FadeOut(every_cell),
            run_time=0.5,
        )
        self.play(result_tri.animate.move_to(UP * 3.0), run_time=0.8)

        count_text = MathTex(
            r"1+2+3+4=", r"\tfrac{n(n+1)}{2}", r"=10",
            font_size=36,
        )
        count_text[1].set_color(ACCENT_CYAN)
        count_text.set_stroke(width=1)
        count_text.set_z_index(20)
        count_text.move_to(UP * 0.55)
        fit_to_safe_width(count_text)

        triple = MathTex(
            r"3S=", r"\tfrac{n(n+1)}{2}", r"\cdot", r"(2n+1)", r"=90",
            font_size=38,
        )
        triple[1].set_color(ACCENT_CYAN)
        triple[3].set_color(RESULT_COLOR)
        triple.set_stroke(width=1)
        triple.set_z_index(20)
        triple.move_to(DOWN * 0.9)
        fit_to_safe_width(triple)

        self.play(Write(count_text), run_time=0.9)
        self.wait(0.4)
        self.play(Write(triple), run_time=1.0)
        self.wait(0.9)

        # ------------------------------------------------------------ conclusion
        # 3 copias * el 2 del numero triangular = el 6 del denominador.
        final = MathTex(
            r"\sum_{k=1}^{n} k^2 = \frac{n(n+1)(2n+1)}{6}",
            font_size=44, color=RESULT_COLOR,
        )
        final.set_stroke(width=1)
        final.set_z_index(21)
        final.move_to(DOWN * 3.0)
        fit_to_safe_width(final)

        self.play(Write(final), run_time=1.3)

        final_box = SurroundingRectangle(final, buff=0.3, corner_radius=0.14)
        final_box.set_stroke(width=4, color=[ACCENT_YELLOW, ACCENT_PURPLE])
        final_box.set_z_index(20)
        self.play(Create(final_box), run_time=0.7)

        why_six = caption(
            r"el 6 son las 3 copias\\por el 2 del tri\'angulo",
            color=GREY_A, font_size=30, y=-5.0,
        )
        self.play(FadeIn(why_six, shift=UP * 0.15), run_time=0.6)
        self.wait(1.6)

        animate_End(scene=self)
