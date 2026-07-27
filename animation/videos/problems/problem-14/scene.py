from manim import *
from lnx import backgroundLnx, BoxAnimation, SmartMathTex, MathPazoKpTemplate, logo_handler, animate_End, LOGO_SVG, LOGO_MAIN

# Clase principal de animación
class CompleteAnimation(Scene):
    def construct(self):
        # Fondo personalizado (probablemente con color o imagen)
        backgroundLnx(self)

        # Establecer el template LaTeX con fuentes elegantes (mathpazo + kpfonts)
        self.camera.tex_template = MathPazoKpTemplate()

        # Crear la caja animada con imagen y borde dorado
        box_anim = BoxAnimation(
            self,
            width=4.2,
            height=2.5,
            image_path=LOGO_MAIN,  # Imagen del logo en la esquina inferior izquierda
            box_stroke_color=GOLD,
        )
        box_anim.on()  # Mostrar caja y activar animaciones iniciales

        # Parámetros útiles para ajustar el contenido dentro de la caja
        box = box_anim.box
        content_width = box.width * 0.9
        content_height = box.height * 0.7

        # TEXTO: Enunciado del problema
        texto1 = MathTex( 
            r"\text{Calcule la integral:} ",
            font_size=22
        )

        # ECUACIÓN: Integral principal
        ecuacion = SmartMathTex(
            r"\int_{1}^{\infty} \frac{x^{\alpha} \ln^{b}(x)}{1 + x + x^2 + \dots + x^n} \, \mathrm{d}x",
            target_width=content_width,  # Escalar para que encaje dentro de la caja
            target_height=content_height * 0.6,
            font_size=25
        )

        # TEXTO: Condiciones de la integral
        texto2 = MathTex( 
            r"\text{donde } b \geq 0,\ n \in \mathbb{Z}^+,\ \alpha < n - 1",
            font_size=16
        )

        # Agrupar y alinear los elementos de arriba a abajo (centrados en la caja)
        grupo = VGroup(texto1, ecuacion, texto2).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        grupo.move_to(box.get_center())

        # ANIMACIONES de entrada: Escritura tipo "dibujado"
        self.play(Write(texto1),run_time=0.5)  # Escribir el enunciado
        self.wait(0.5)

        self.play(Write(ecuacion))  # Escribir la integral
        self.wait(0.5)

        self.play(Write(texto2),run_time=0.5)  # Escribir las condiciones
        self.wait(1)

        # Tiempo extra para que el espectador lea con calma 

        # SOLUCIÓN: etiqueta en la parte superior de la pantalla
        solucion_label = MathTex(r"  \text{Solución}  ", font_size=20, color=WHITE)
        fondoTextSolution = BackgroundRectangle(solucion_label, color=BLACK, fill_opacity=1)
        grupo2 = VGroup(fondoTextSolution, solucion_label).to_edge(UP)

        # TRANSICIÓN: Remover problema y mostrar "Solución"
        self.play(
            ReplacementTransform(grupo, grupo2, run_time=1),  # Cambiar el grupo de texto por la etiqueta "Solución"
            FadeOut(box_anim.box),                            # Desaparecer la caja
            FadeOut(box_anim.fill),                           # Desaparecer fondo de la caja
            box_anim.imagen.animate.scale(0.3).to_corner(DL), # Mover y escalar imagen a la esquina inferior izquierda
            run_time=1
        )

        # Pausa final
        self.wait(1)
        # solucion aqui dbemos escribir, todo lo de arriba siempre se va a repetir lo mismo

        #--------------------------------------------------------------------------------------------------------------#
        #--------------------------------------------------------------------------------------------------------------#
        #--------------------------------------------------------------------------------------------------------------#
        #--------------------------------------------------------------------------------------------------------------#
        #--------------------------------------------------------------------------------------------------------------#
        color3 = "#F3950D"
       
        # Definición de la integral general
        texto1 = MathTex(
            r"\text{Definimos la integral }",
            r" I(\alpha, b, n) ",
            font_size=20
        ).shift(UP*3)

        # Animate both parts of texto1
        self.play(Write(texto1[0]) )
        self.wait(0.2)
        self.play(Write(texto1[1]) )
        self.wait(0.5)
        
        solEq1 = MathTex(
            r"I(\alpha, ",
            r"b",
            r", n) = ",
            r"\int_{1}^{\infty} ",
            r"{x^{\alpha}\; ",  # Numerador (parte 1)
            r"\ln^{b}(x)",    # Numerador (parte 2, separada para animación)
            r"\over",
            r" 1 + x + x^2 + \dots + x^n}",  # Denominador
            r"\, \mathrm{d}x",
            font_size=20
        ).next_to(texto1, DOWN, buff=0.4)

        solEq1_copy= solEq1.copy()

        # Animate each part
        for part in solEq1:
            self.play(Write(part))
            self.wait(0.1)
        self.wait(0.3)

        # Case when b=0
        texto2 = MathTex(
            r"\text{Caso cuando }",
            r" b=0, \,",
            r" I(\alpha, 0, n) ",
            font_size=20
        ).move_to(texto1.get_center())

        # Transform the entire texto1 into texto2
        self.play(ReplacementTransform(texto1, texto2))
        self.wait(1)

        solEq2 = MathTex(
            r"0",
            r"1", 
            font_size=20
        )
        solEq2[0].move_to(solEq1[1].get_center())
        solEq2[1].move_to(solEq1[5].get_center())
        solEq2[0].set_color(color3)  # Si quieres colorear el 0
        solEq2[1].set_color(color3)  # Si quieres colorear el ln^1(x)

        self.play(Transform(solEq1[1],solEq2[0]),Transform(solEq1[5],solEq2[1]))
        self.wait(0.5)
        self.play(
            FadeOut(solEq1[5]),
            solEq1[1].animate.set_color(WHITE),  # Animación del cambio de color
            run_time=1
        )

        self.wait(0.5)
        texto3 = MathTex(
            r"\text{El denominador es una serie geométrica,}",
            font_size=20
        ).next_to(solEq1, DOWN)
        self.play(Write(texto3))
        self.wait(1)

        solEq3 = MathTex(
            r"1 + x + \cdots + x^n",
            r" =",
            r" {1 - x^{n+1}",
            r"  \over  ",
            r" 1 - x}",
            ",", 
            r"\quad \text{para } x \neq 1",
            font_size=20
        ).next_to(texto3, DOWN)
        
        for part in solEq3:
            self.play(Write(part),run_time=0.2)
            self.wait(0.1)
        
        self.wait(0.1)
        solEq3[2].set_color(RED)
        solEq3[3].set_color(RED)
        solEq3[4].set_color(RED)
        self.wait(0.2)  
 
        ecua3_copy_1 = solEq3[2].copy()
        ecua3_copy_2 = solEq3[4].copy()

        solEq3_copy3 = MathTex( 
            r" (1 - x)", 
            font_size=20
        ).set_color(YELLOW)
        solEq3_copy3.move_to(solEq1[5].get_center())  # Posición arriba

        self.play(
            FadeOut(solEq1[7]), # Esto reemplaza visualmente ecua1
            ecua3_copy_1.animate.move_to(solEq1[7].get_center()).set_color(YELLOW), 
            ecua3_copy_2.animate.move_to(solEq1[5].get_center()).set_color(YELLOW), 
            ReplacementTransform(ecua3_copy_2, solEq3_copy3),
            run_time=2,
            rate_func=smooth
        )
        #self.play(FadeIn(solEq1[6]), FadeIn(solEq1[8]))
        #self.wait(0.3)

        self.play(
            *[FadeOut(part) for part in solEq3],  # FadeOut de cada parte
            FadeOut(texto3),
            run_time=0.5
        )
       
        self.wait(0.5)

        texto5 = MathTex(
            r"\text{Haciendo el cambio de variable, }",
            font_size=20
        ).next_to(solEq1, DOWN, buff=0.4)

        solEq5 = MathTex(
            r"x = t^{-1/(n+1)}, \quad \mathrm{d}x = -\frac{1}{n+1}t^{-(n+2)/(n+1)} \, \mathrm{d}t",
            font_size=20
        ).next_to(texto5, DOWN, buff=0.4)

        self.play(Write(texto5))
        self.play(Write(solEq5))
        self.wait()
        # Integral después del cambio de variable
        texto6 = MathTex(
            r"\text{Simplificando la expresión,}",
            font_size=18
        ).next_to(solEq5, DOWN, buff=0.4)

        solEq6 = MathTex(
            r"I(\alpha, 0, n) =",
            r"\text{\quad } \, ",
            r"  \frac{1}{n+1}\int_{0}^{1} {t^{-(\alpha+1)/(n+1)}(1 - t^{-1/(n+1)})",
            r"\over ",
            r" \text{ \quad } \, ",
            r"t-1} ",
            r"\, \mathrm{d}t",
            font_size=16
            ).next_to(texto6, DOWN, buff=0.4)
        self.play(Write(texto6))
        self.wait()

        for part in solEq6:
            self.play(Write(part),run_time=0.2)
        self.wait(0.5)
 
        self.play(
            AnimationGroup(
                FadeOut(texto5),
                FadeOut(solEq5),
                texto6.animate.move_to(texto5.get_center()),
                solEq6.animate.move_to(solEq5.get_center()),
                rate_func=linear,  # También puedes usar: smooth, lambda t: t**2, etc.
                lag_ratio=0  # Ambas animaciones ocurren al mismo tiempo
            ),
            run_time=1
        ) 

        solEq6[5].set_color(YELLOW) 

        # Crear nuevos objetos MathTex para el símbolo "-" y "(1-t)"
        solEq6_copy5 = MathTex(r"(1-t)", font_size=18).move_to(solEq6[5].get_center())
        solEq6_copy4 = MathTex(r"-", font_size=18).move_to(solEq6[5].get_center()+0.35*LEFT).set_color(RED) 

        # Reemplazar el contenido de solEq6[5] y solEq6[4]
        self.play(Transform(solEq6[5], solEq6_copy5))
        self.wait(0.2)
        self.play(Write(  solEq6_copy4))  # Usar ReplacementTransform
        self.wait(0.5)

        # Mover el símbolo "-" a la posición deseada
        self.play(solEq6_copy4.animate.move_to(solEq6[0].get_center()+0.6*RIGHT))
        self.wait(0.5)
        
        # Propiedad de la función Digamma
        texto7 = MathTex(
            r"\text{Aplicando la propiedad de la función Digamma,}",
            font_size=18
        ).next_to(solEq6, DOWN, buff=0.4) 

        self.play(Write(texto7))
        self.wait(0.5)

        solEq8 = MathTex(
            r"\int_{0}^{1} \frac{t^{p-1} - t^{q-1}}{1 - t} \, \mathrm{d}t = \psi(q) - \psi(p), \quad \Re(p), \Re(q) > 0",
            font_size=16
        ).next_to(texto7, DOWN, buff=0.4) 

        solEq9 = MathTex(
            r"I(\alpha, 0, n) = \frac{1}{n+1} \left[ \psi\left(1-\frac{\alpha+1}{n+1}\right) - \psi\left(1-\frac{\alpha+2}{n+1}\right) \right]",
            font_size=18
        ).next_to(solEq8, DOWN, buff=0.4) 

        self.play(Write(solEq8))
        self.wait()
        self.play(Write(solEq9))
        self.wait()
        self.play(
            AnimationGroup(
                FadeOut(texto6),
                FadeOut(solEq6),
                FadeOut(texto6),
                FadeOut(texto7),
                FadeOut(solEq8),
                FadeOut(solEq6_copy4),
                solEq9.animate.move_to(texto6.get_center()), 
                rate_func=linear,  # También puedes usar: smooth, lambda t: t**2, etc.
                lag_ratio=0  # Ambas animaciones ocurren al mismo tiempo
            ),
            run_time=1
        )

        self.wait()

        # Diferenciación bajo el signo integral
        texto9 = MathTex(
            r"\text{Diferenciando bajo el signo integral,}",
            font_size=18
        ).next_to( solEq9, DOWN, buff=0.4) 

        solEq91 = MathTex(
            r"I(\alpha, b, n) = \frac{\partial^b}{\partial \alpha^b} I(\alpha, 0, n)",
            font_size=18
        ).next_to(texto9, DOWN, buff=0.4) 

        self.play(Write(texto9))
        self.wait()
        self.play(Write(solEq91))
        self.wait()

        # Derivada de la función Digamma
        texto10 = MathTex(
            r"\text{La } b\text{-ésima derivada de la función Digamma es, }",
            font_size=18
        ).next_to(solEq91, DOWN, buff=0.4) 

        solEq11 = MathTex(
            r"\frac{\mathrm{d}^b}{\mathrm{d} \alpha^b} \psi(f) = \psi^{(b)}(f) \cdot \left( \frac{\mathrm{d}f}{\mathrm{d}\alpha} \right)^b",
            font_size=18
        ).next_to(texto10, DOWN, buff=0.4) 

        self.play(Write(texto10))
        self.wait()
        self.play(Write(solEq11))
        self.wait()

        # Solución general final
        texto11 = MathTex(
            r"\text{Solución general final:}",
            font_size=18
        ).next_to(solEq11, DOWN, buff=0.4) 

        solEq12 = MathTex(
            r"\boldsymbol{ I(\alpha, b, n) = \frac{(-1)^b}{(n+1)^{b+1}} \left[ \psi^{(b)}\left(1-\frac{\alpha+1}{n+1}\right) - \psi^{(b)}\left(1-\frac{\alpha+2}{n+1}\right) \right]}",
            font_size=14
        ).next_to(texto11, DOWN, buff=0.4).set_color_by_gradient(RED, YELLOW)

        self.wait()
        #rectangle = Rectangle(width=4, height=2).next_to(texto11, DOWN, buff=0.4)   # puedes ajustar dimensiones aquí
        #rectangle.set_fill(PINK, opacity=0.5)  # color y opacidad
        

        self.play(
            AnimationGroup(
                FadeOut(texto10),
                FadeOut(solEq11), 
                #Create(rectangle),  # animación de creación
                Write(texto11),
                Write(solEq12) ,
                rate_func=linear,  # También puedes usar: smooth, lambda t: t**2, etc.
                lag_ratio=0  # Ambas animaciones ocurren al mismo tiempo
            ),
            run_time=1
        )
        self.play(
            AnimationGroup(
                texto11.animate.move_to(texto10.get_center()), 
                solEq12.animate.move_to(solEq11.get_center()), 
                rate_func=linear,  # También puedes usar: smooth, lambda t: t**2, etc.
                lag_ratio=0  # Ambas animaciones ocurren al mismo tiempo
            ),
            run_time=0.5
        ) 
 
        self.wait(1)
        pos99= solEq9.get_center()
        self.play(
            AnimationGroup(
                FadeOut(ecua3_copy_1),
                FadeOut(ecua3_copy_2),
                FadeOut(solEq1),
                FadeOut(texto10), 
                FadeOut(texto11),  
                FadeOut(texto1),
                FadeOut(texto2),
                FadeOut(texto9),
                FadeOut(solEq9),
                FadeOut(solEq91),
                FadeOut(solEq3_copy3),
                Write(solEq1_copy) , 
                solEq12.animate.move_to(pos99), 
                rate_func=linear,  # También puedes usar: smooth, lambda t: t**2, etc.
                lag_ratio=0  # Ambas animaciones ocurren al mismo tiempo
            ),
            run_time=1
        )
 
        # Finalizar la escena
        self.wait(1)

      
        # Gradiente para el texto "Ejemplos"
        ejemplo = MathTex(
            r"\text{Ejemplos: }",
            font_size=18
        ).next_to(solEq12, DOWN, buff=0.6)
        ejemplo.set_color_by_gradient(RED, ORANGE, YELLOW)  # Gradiente rojo-anaranjado-amarillo

        self.play(Write(ejemplo))
        self.wait(1)

        # Ejemplo 1: Mostrar cálculo completo
        ejemplo1_texto = MathTex(
            r"I\left( \frac{1}{2},1,3 \right) = \int_{1}^{\infty} \frac{ \sqrt{x} \ln(x)}{(1+x)(1+x^2)} \, dx",
            font_size=18
        ).next_to(ejemplo, DOWN, buff=0.4).set_color(WHITE)  # Texto en blanco
        ejemplo1_respuesta = MathTex(
            r"= \frac{1}{16} \left( \psi^{(1)}\left( \frac{3}{8} \right) - \psi^{(1)}\left( \frac{5}{8} \right) \right) = \frac{\pi^2}{16} \csc\left(\frac{3\pi}{8}\right)\cot\left(\frac{3\pi}{8}\right)",
            font_size=14
        ).next_to(ejemplo1_texto, DOWN, buff=0.4).set_color(BLUE)  # Respuesta en azul

        self.play(Write(ejemplo1_texto))
        self.wait(1)
        self.play(Write(ejemplo1_respuesta))
        self.wait(1)

        ejemplo2_texto = MathTex(
            r"I\left( \frac{1}{2},2,3 \right) = \int_{1}^{\infty} \frac{ \sqrt{x} \ln^2(x)}{(1+x)(1+x^2)} \, dx",
            font_size=18
        ).next_to(ejemplo1_respuesta, DOWN, buff=0.4).set_color(WHITE)  # Texto en blanco

        # Ejemplo 2: Mostrar solo la respuesta
        ejemplo2_respuesta = MathTex(
            r"I\left( \frac{1}{2},2,3 \right) = \frac{1}{64} \left( \psi^{(2)}\left( \frac{5}{8} \right) - \psi^{(2)}\left( \frac{3}{8} \right) \right) = \frac{\pi^3}{32} \csc^2\left(\frac{3\pi}{8}\right)\cot\left(\frac{3\pi}{8}\right)",
            font_size=14
        ).next_to(ejemplo2_texto, DOWN, buff=0.4).set_color(GREEN)  # Respuesta en verde

        self.play(Write(ejemplo2_texto))
        self.wait(1)
        self.play(Write(ejemplo2_respuesta))
        self.wait(1)
        
        # Limpiar todo lo que está en la pantalla
        self.clear()

        # Cargar el logo como SVG
        logo = SVGMobject(LOGO_SVG).scale(0.5)

        # Extraer los puntos del contorno del logo
        outline_path = VMobject()
        for submobject in logo:
            outline_path.append_points(submobject.get_points())
        outline_path.set_stroke(color=[YELLOW, ORANGE], width=2)  # Gradiente de amarillo a anaranjado

        # Animar el trazo del contorno
        self.play(Create(outline_path), run_time=1.5)
        self.wait(0.2)

        # Mostrar el logo completo con colores aplicados
        self.play(FadeOut(outline_path), run_time=0.5)
        self.play(FadeIn(logo))
        # Finalizar la escena
        self.wait(3)


#with tempconfig({"preview": True, "quality": "high_quality", "disable_caching": True}):
 #   scene = CompleteAnimation()
  #  scene.render()





 