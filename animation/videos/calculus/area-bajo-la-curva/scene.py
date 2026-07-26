from manim import *
from math import sin, pi
from scipy.optimize import minimize_scalar
from lnx import backgroundLnx, BoxAnimation, SmartMathTex, MathPazoKpTemplate, logo_handler, animate_End, LOGO_SVG, LOGO_MAIN

class AreaBetweenCurve(Scene):
    def construct(self):
        # Configuración inicial
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()
        imagen = ImageMobject(LOGO_MAIN)

        # Escalar imagen (horizontal x vertical)
        imagen.scale(0.4*0.4)  # primero escalar proporcionalmente

        # Mover imagen x unidades abajo del centro
        imagen.shift(DOWN * 3.2)

        # Mostrar imagen sin animación
        self.add(imagen)

        # Funciones matemáticas
        def func1(x):
            return 4*x - x**2
        def func2(x):
            return 1*np.sin(np.pi*x/3) + x
        # Configurar ejes con rangos dinámicos
        def max_y_value():
            x_values = np.linspace(-0.1, 3.5, 100)
            y1 = 4*x_values - x_values**2
            y2 = 1*np.sin(np.pi*x_values/3) + x_values
            return max(np.max(y1), np.max(y2)) + 1  # Margen adicional
        
        ax = Axes(
            x_range=(-1, 4.5, 1),
            y_range=(-1, int(max_y_value()), 1),  # Rango dinámico
            x_length=3,
            y_length=3.5,
            axis_config={
                "font_size": 16, 
                "tip_width": 0.1,
                "tip_height": 0.1,
                "color": YELLOW_A,  # Pale yellow
                "stroke_width": 1,  # Match dashed line thickness
            },
            tips=True,  # Enable arrows on axes
        ).scale(0.9)

        # Add labels for x and y axes
        x_label = Tex("x", font_size=20).next_to(ax.x_axis.get_end(), 0.5*RIGHT, buff=0.2)
        y_label = Tex("y", font_size=20).next_to(ax.y_axis.get_end(), 0.5*LEFT, buff=0.2)
        
        # Gráficas con estilos mejorados
        graph1 = ax.plot(func1, color=GREEN_D, stroke_width=1.5, x_range=(-0.2, 4.1))
        graph2 = ax.plot(func2, color=BLUE_D, stroke_width =1.5, x_range=(-0.3, 4.1))
        area = ax.get_area(
            graph1,
            x_range=(0, 3),
            color=[BLUE, YELLOW, PURPLE],  # Gradient for the area
            bounded_graph=graph2
        )
#----------------------------------------------------------------------------# title and labels
        # Title and labels
        title = Tex("Encuentre el Área entre las Curvas", font_size=25).to_edge(UP).set_color_by_gradient(YELLOW, ORANGE, RED).set_stroke(width=1).shift(DOWN * 0.2)
        funcTex1 = MathTex(r"f(x)", " = ", r"4x-x^2", font_size=20).next_to(title, DOWN, buff=0.3).set_color(GREEN).set_stroke(width=1)
        funcTex2 = MathTex(r"g(x)"," = ", r"\sin\left(\frac{\pi x}{3}\right) + x", font_size=20).next_to(funcTex1, DOWN, buff=0.3).set_color(BLUE).set_stroke(width=1)
        dashedLine2 = DashedLine(ax.c2p(3, 3), ax.c2p(3,0), stroke_width=1)  # Thinner dashed line
        label2 = Tex("3", font_size=20).next_to(dashedLine2, DOWN, buff=0.1)  # Smaller label
        origin_label = Tex("0", font_size=20).set_color(BLACK).move_to(ax.c2p(0, 0))
        question = Tex("?").move_to(area.get_center()).shift(UP * 1, RIGHT * 0.25)



        # Calculate intersection points
        intersection_x1 = 0  # Replace with actual calculation if needed
        intersection_x2 = 3  # Replace with actual calculation if needed
        intersection_y1 = func1(intersection_x1)
        intersection_y2 = func1(intersection_x2) 
        dot1 = Dot(ax.c2p(intersection_x1, intersection_y1), color=RED, radius=0.05)
        dot2 = Dot(ax.c2p(intersection_x2, intersection_y2), color=RED, radius=0.05)

#----------------------------------------------------------------------------# animation the curves
        self.play(FadeIn(title))
        self.play(Create(funcTex1), Create(funcTex2))
        self.play(DrawBorderThenFill(ax, run_time=1))
        self.play(Write(x_label), Write(y_label), FadeIn(origin_label))
        self.play(Create(graph1),Create(graph2),run_time=1)
        self.play(Create(area))
        area.z_index = -1  # Set area to a lower z-index to appear below the curves
        # Add the intersection points
        self.play(Create(dot1), Create(dot2), run_time = 0.2)
        self.play(Create(dashedLine2), run_time = 0.2)
        self.play(Create(label2), run_time = 0.2)
        self.play(Write(question), run_time = 0.3)
#----------------------------------------------------------------------------# others
        # Animation for calculating the area
        funcTex1_copy = funcTex1[0].copy()  # Corregido: usar .copy() como método
        funcTex2_copy = funcTex2[0].copy()  # Corregido: usar .copy() como método

        areaMath = MathTex(r"A=\int", r"_{a}",r"^{b}",r"\left(",r"f(x)", "-", r"g(x)", r"\right) \, \mathrm{d}x" , font_size=20).set_stroke(width=1)
        areaMath.next_to(ax, 0.6*DOWN, buff=0.5)
        self.play(Write(areaMath[0]), run_time = 0.05) 
        self.play(Write(areaMath[1]), run_time = 0.05)
        self.play(Write(areaMath[2]), run_time = 0.05)
        self.play(Write(areaMath[3]), run_time = 0.05)
        self.play(Transform(funcTex1_copy, areaMath[4]), run_time=0.3)  # Cambiado a Transform
        self.play(Write(areaMath[5]), run_time = 0.05)
        self.play(Transform(funcTex2_copy, areaMath[6]), run_time=0.3)  # Cambiado a Transform
        self.play(Write(areaMath[7]), run_time = 0.8) 


        areaMath_eq1 = MathTex(r"A=\int", r"_{0}",r"^{3}",r"\left(",r"\left(",r"4x-x^2", r"\right)", "-",r"\left(", r"\sin\left(\frac{\pi x}{3}\right) + x", r"\right)", r"\right) \, \mathrm{d}x" , font_size=20).set_stroke(width=1)
        areaMath_eq1.next_to(areaMath, 0.2*DOWN, buff=0.5)
        funcTex1_copy2 = funcTex1[2].copy()
        funcTex2_copy2 = funcTex2[2].copy() 
        label2_3=label2.copy()  
        origin_label_0= origin_label.copy()

        self.play(Write(areaMath_eq1[0]), run_time = 0.08)  
        self.play(Transform(origin_label_0, areaMath_eq1[1]), run_time=0.3)  # Cambiado a Transform
        self.play(Transform(label2_3, areaMath_eq1[2]), run_time=0.3)  # Cambiado a Transform
        self.play(Write(areaMath_eq1[3]), run_time = 0.08)
        self.play(Write(areaMath_eq1[4]), run_time = 0.08)
        self.play(Transform(funcTex1_copy2, areaMath_eq1[5]), run_time=0.8)  # Cambiado a Transform
        self.play(Write(areaMath_eq1[6]), run_time = 0.08)
        self.play(Write(areaMath_eq1[7]), run_time = 0.08)
        self.play(Write(areaMath_eq1[8]), run_time = 0.08)
        self.play(Transform(funcTex2_copy2, areaMath_eq1[9]), run_time=0.8)  # Cambiado a Transform
        self.play(Write(areaMath_eq1[10]), run_time = 0.05)
        self.play(Write(areaMath_eq1[11]), run_time = 0.05)

#------------------------------- fadeout 
        self.play(AnimationGroup(
            #FadeOut(title),
            FadeOut(funcTex1), FadeOut(funcTex2),
            lag_ratio=0.1  # Optional: Add a slight delay between animations
        ))

        area_Math_eq1_aux = MathTex(r"A=\int_{0}^{3}\left(\left(4x-x^2\right) -\left(\sin\left(\frac{\pi x}{3}\right) + x\right)\right) \, \mathrm{d}x" , font_size=18).set_stroke(width=1) 
        area_Math_eq1_aux.next_to(title, DOWN, buff=0.4, aligned_edge=LEFT)
       
        self.play(FadeIn(area_Math_eq1_aux))
#-----------------------------------------------------------------------------# others
        areaMath_eq2 = MathTex(r"A=\int_0^3 \left( 3x-x^2- \sin\left(\frac{\pi x}{3}\right)\right)\, \mathrm{d}x", font_size=18).set_stroke(width=1)
        areaMath_eq2.next_to(area_Math_eq1_aux, DOWN, buff=0.3)  # Position below areaMath_eq1

        #self.play(Write(areaMath_eq2))
        self.play(AnimationGroup(
            #FadeOut(title),
            Write(areaMath_eq2),
            FadeOut(ax, run_time=0.3),
            FadeOut(x_label), FadeOut(y_label), FadeOut(origin_label),
            FadeOut(graph1), FadeOut(graph2, run_time=0.3),
            FadeOut(area),
            FadeOut(dot1), FadeOut(dot2, run_time=0.3),
            FadeOut(dashedLine2, run_time=0.3),
            FadeOut(label2, run_time=0.3),
            FadeOut(question, run_time=0.1),
            FadeOut(areaMath, run_time=0.1),
            FadeOut(funcTex1_copy2, run_time=0.1),#
            FadeOut(funcTex2_copy2, run_time=0.1), #
            FadeOut(funcTex2_copy, run_time=0.1),
            FadeOut(funcTex1_copy, run_time=0.1),
            FadeOut(origin_label_0, run_time=0.1),#
            FadeOut(label2_3, run_time=0.1),#
            FadeOut(areaMath_eq1, run_time=0.1),
            lag_ratio=0  # Optional: Add a slight delay between animations
        ))

        # Problema original
        problema = MathTex(
            r"A =", r" \int_0^3 (3x - x^2) dx", "-", r" \int_0^3 \sin\left(\frac{\pi x}{3}\right) dx",
            font_size=18
        ).set_stroke(width=1)

        problema.next_to(areaMath_eq2, DOWN, buff=0.5)
        #----------------
        color_int1 =YELLOW
        color_int2 = ORANGE
        #-------------
        problema[1].set_color(color_int1)  # Color for (3x - x^2)
        problema[3].set_color(color_int2)  # Color for sin(pi x / 3)
        
        
        self.play(Write(problema))
        self.wait()

        # Paso 2: Resolver primera parte (polinomio)
        paso2a = MathTex(
            r"\bullet \int_0^3 (3x - x^2) dx =\left. \frac{3x^2}{2} - \frac{x^3}{3} \bigg\rvert_0^3 =\frac{9}{2}",
            font_size=18
        ).set_stroke(width=1)   
        paso2a.set_color(color_int1)   
        paso2a.next_to(problema, DOWN, buff=0.4, aligned_edge=LEFT)
        # Paso 3: Resolver segunda parte (trigonométrica)
        paso3a = MathTex(
            r"\bullet \int_0^3 \sin\left(\tfrac{\pi x}{3}\right) dx = \left. -\frac{3}{\pi}\cos\left(\tfrac{\pi x}{3}\right) \bigg\rvert_0^3 =\frac{6}{\pi} ",
            font_size=18
        ).set_stroke(width=1)
        paso3a.set_color(color_int2)  # Color for sin(pi x / 3)
        paso3a.next_to(paso2a, DOWN, buff=0.4, aligned_edge=LEFT)
         
        
        self.play(Write(paso2a))
        self.wait(0.3)
        self.play(Write(paso3a))
        self.wait(0.3)

        # Paso 4: Combinar resultados
        paso4 = MathTex(
            r"A = \frac{9}{2} - \frac{6}{\pi} \approx 2.735 \text{ u}^2",
            font_size=18,
            color=RED
        ).set_stroke(width=1)
        
        paso4.next_to(paso3a, DOWN, buff=0.6)
        
        box = SurroundingRectangle(
            paso4, buff=0.1, 
            color=YELLOW,  # Base color
            corner_radius=0.1
        )
        box.set_stroke(
            width=3, 
            color=[ ORANGE, YELLOW]  # Gradient colors
        )
        
        self.play(
            Write(paso4),
            Create(box),
            run_time=0.5
        )
        self.wait(2)  