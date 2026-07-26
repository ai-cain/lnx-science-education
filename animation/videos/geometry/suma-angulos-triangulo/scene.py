from manim import *
from lnx import *

class TrianguloSum180(Scene):
    def construct(self):

        # Variables de colores
        triangle_color_ab = "#00FFFF"  # Cian
        triangle_color_bc = RED  # Rojo (reemplaza al magenta)
        triangle_color_ca = "#FFFF00"  # Amarillo
        triangle_color_secondary = GREEN  # Para las líneas reversas
        line_parallel_color = WHITE
        label_color = WHITE

        angle_color_alpha =  triangle_color_bc
        angle_color_beta =  triangle_color_ca
        angle_color_theta = triangle_color_ab
        rectangle_color = BLUE

        gradient_colors = [YELLOW, "#FF8C00", ORANGE]  # Amarillo -> Naranja oscuro -> Naranja

        backgroundLnx(self)
        grillado(self)
        self.camera.tex_template = MathPazoKpTemplate()
        logo_handler(  scene=self, image_path=LOGO_MAIN, animation_style="fast", target_scale=0.5*0.6 ) #Mover logo con ajustes


        # Configuración para líneas suaves
        config.line_stroke_width = 4
        config.line_stroke_joint_style = "round"

        scaleValue = 1.5
        radiusValue = 0.5 * scaleValue / 2
        radiusValueText = 1.4 * radiusValue

        # Definir variables para los tamaños de fuente
        small_font_size = 25
        big_font_size = 30

        # Puntos del triángulo (equilátero para mejor visualización)
        punto_a = LEFT * scaleValue * 1.2
        punto_b = RIGHT * scaleValue * 1
        punto_c = UP * scaleValue * np.sqrt(3) / 1.3  # Altura para equilátero

        punto_paralelo = RIGHT * scaleValue * 0.9 / 1.4 

        # Líneas del triángulo
        linea_ab = Line(punto_a, punto_b, color=triangle_color_ab)
        linea_bc = Line(punto_b, punto_c, color=triangle_color_bc)
        linea_ca = Line(punto_c, punto_a, color=triangle_color_ca)

        linea_ba = Line(punto_b, punto_a, color=triangle_color_secondary)
        linea_cb = Line(punto_c, punto_b, color=triangle_color_secondary)
        linea_ac = Line(punto_a, punto_c, color=triangle_color_secondary)

        # Grupo del triángulo
        triangulo = VGroup(linea_ab, linea_bc, linea_ca)

        # Línea paralela a linea_ab que pasa por punto_c
        parallel_line = Line(
            punto_c - (punto_b - punto_a) / 2,
            punto_c + (punto_b - punto_a) / 2,
            color=line_parallel_color, 
        ) 
        parallel_line_1 = Line(
            punto_c,
            punto_c - (punto_b - punto_a) / 2,
            color=line_parallel_color
        )
        parallel_line_2 = Line(
            punto_c,
            punto_c + (punto_b - punto_a) / 2,
            color=line_parallel_color
        )

        # Etiqueta "//" en la línea paralela, posicionada un poco a la derecha
        parallel_label = MathTex(r"//", font_size=small_font_size, color=label_color).next_to(parallel_line, LEFT, buff=0.1).scale(0.5)
        parallel_label.shift(punto_paralelo)

        # Etiqueta "//" en la línea AB, posicionada un poco a la derecha
        ab_parallel_label = MathTex(r"//", font_size=small_font_size, color=label_color).next_to(linea_ab, LEFT, buff=0.1).scale(0.5)
        ab_parallel_label.shift(punto_paralelo)

        # --- Ángulos INTERNOS (arcos hacia adentro) ---
        arc_alpha = Angle(linea_ab, linea_ac, radius=radiusValue, color=angle_color_alpha)
        alpha_label = MathTex(r"\alpha", font_size=small_font_size, color=angle_color_alpha).move_to(
            Angle(linea_ab, linea_ac, radius=radiusValueText).point_from_proportion(0.5)
        )

        arc_beta = Angle(linea_bc, linea_ba, radius=radiusValue, color=angle_color_beta)
        beta_label = MathTex(r"\beta", font_size=small_font_size, color=angle_color_beta).move_to(
            Angle(linea_bc, linea_ba, radius=radiusValueText).point_from_proportion(0.5)
        )

        arc_theta = Angle(linea_ca, linea_cb, radius=radiusValue, color=angle_color_theta)
        theta_label = MathTex(r"\theta", font_size=small_font_size, color=angle_color_theta).move_to(
            Angle(linea_ca, linea_cb, radius=radiusValueText).point_from_proportion(0.5)
        )

        suma_angulos = MathTex(r"\alpha + \beta + \theta =","?" , font_size=big_font_size)
        angulo_180 = MathTex(r" 180^\circ", font_size=big_font_size)
        suma_angulos.next_to(triangulo, DOWN, buff=1.2)
        angulo_180.next_to(suma_angulos[0], RIGHT, buff=0.1)

        # ---- Animaciones ----------------
        # Dibujar triángulo
        self.play(
            LaggedStart(
                Create(linea_ab),
                Create(linea_bc),
                Create(linea_ca),
                lag_ratio=0.7
            ),
            run_time=2
        )
        self.wait(0.5)

        # Mostrar ángulos internos (arcos hacia adentro)
        self.play(
            Create(arc_alpha),
            Create(arc_beta),
            Create(arc_theta),
            FadeIn(alpha_label),
            FadeIn(beta_label),
            FadeIn(theta_label),
            run_time=1
        )
        self.wait(1)

        # Mostrar ecuación
        self.play(Write(suma_angulos))
        self.wait(1)
 
        # Mostrar línea paralela a AB pasando por C y sus etiquetas
        self.play(Create(parallel_line), Write(parallel_label), Write(ab_parallel_label))
        self.wait(1)

        # -------- Demostración: Copia y transformación de α a su ángulo alterno --------
        # Se construye usando la recta AC invertida (de C a A) y la línea paralela que pasa por C.
        arc_alpha_opuesto = Angle(
            parallel_line_1,
            Line(punto_c, punto_a),
            radius=radiusValue,
            color=angle_color_alpha
        )
        alpha_opuesto_label = MathTex(r"\alpha", font_size=small_font_size, color=angle_color_alpha).move_to(
            Angle(parallel_line_1, Line(punto_c, punto_a), radius=radiusValueText).point_from_proportion(0.5)
        )

        self.play(
            Transform(arc_alpha.copy(), arc_alpha_opuesto),
            Transform(alpha_label.copy(), alpha_opuesto_label),
            run_time=1
        )
        self.wait(0.5)

        arc_beta_opuesto = Angle(
            Line(punto_c, punto_b),
            parallel_line_2,
            radius=radiusValue,
            color=angle_color_beta
        )
        beta_opuesto_label = MathTex(r"\beta", font_size=small_font_size, color=angle_color_beta).move_to(
            Angle(Line(punto_c, punto_b), parallel_line_2, radius=radiusValueText).point_from_proportion(0.5)
        )

        self.play(
            Transform(arc_beta.copy(), arc_beta_opuesto),
            Transform(beta_label.copy(), beta_opuesto_label),
            run_time=1
        )
        self.wait(1)

        # En el punto C: ángulo de 180° con radio = radiusValue * 2 y etiqueta
        arc_180 = Arc(
            arc_center=punto_c,
            radius=radiusValue * 2,
            start_angle=PI,  # Ajusta la orientación según lo requieras
            angle=PI,           # 180° en radianes
            color=WHITE,
            stroke_width=0.5  # Temporario para crear el objeto base
        )
        label_180 = MathTex(r"180^\circ", font_size=small_font_size, color=WHITE).move_to(
            arc_180.point_from_proportion(0.5)
        )
        label_180.shift(DOWN * 0.25)

        self.play(Create(arc_180), Write(label_180))
        self.wait(1)

        self.play(
            Transform(suma_angulos[1], angulo_180),
            #Transform(angulo_180, angulo_180.copy().move_to(suma_angulos[1])),
            FadeOut(arc_180),
            FadeOut(label_180),
            run_time=1,
            lag_ratio=0.0
        )

        self.wait(1)

        rect = SurroundingRectangle(suma_angulos,
                                    color=rectangle_color,
                                    buff=0.25,
                                    corner_radius=0.1
                                    ) 
        rect.set_stroke(
            width=2, 
            color=[ ORANGE, RED]  # Gradient colors
        )
        

        self.play(
            Create(rect),
            run_time=1,
            lag_ratio=0.0
        )

        self.wait(1)
