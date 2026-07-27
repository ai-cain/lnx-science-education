from manim import *
import random  
from lnx import *

class LoveEquationFinal(Scene):
    def construct(self):
        backgroundLnx(self)
        logo_handler(  scene=self, image_path=LOGO_MAIN, animation_style="fast", target_scale=0.5*0.6 ) #Mover logo con ajustes

        # Establecer el template LaTeX con fuentes elegantes (mathpazo + kpfonts)
        self.camera.tex_template = MathPazoKpTemplate()
        
        # Configuración visual
        self.camera.background_color = "#0A0A0A"  # Fondo negro
        text_color = "#E0E0E0"  # Gris claro
        love_color = "#FF6B6B"  # Rojo melancólico
        
        # 1. Texto inicial CENTRADO (0:00-0:03)
        hook = Text("El amor es una ecuación...", 
                   font_size=22, 
                   color=text_color )
        self.play(Write(hook), run_time=1.5)
        self.wait(0.5)
        
        # 2. Mover texto inicial ARRIBA (2.8 UP) (0:03-0:04)
        self.play(hook.animate.shift(UP * 2.6), run_time=1)
        
        # 3. Ecuación d(love)/dt CENTRADA (0:04-0:07)
        equation = MathTex(
            r"\frac{d(\text{love})}{dt} = -  \text{you}",
            font_size=25,
            color=text_color
        )
        self.play(Write(equation), run_time=1.5)
        self.wait(0.5)
        
        # 4. Mover ecuación d(love)/dt DEBAJO del texto inicial (0:07-0:08)
        equation.generate_target()
        equation.target.next_to(hook, DOWN, buff=0.6)
        self.play(MoveToTarget(equation), run_time=1)
        
        # 5. Transformar a solución love(t) = ... (0:08-0:12)
        solution = MathTex(
            r"\text{love}(t) = -\text{you} \cdot t + c",
            font_size=25,
            color=love_color
        )
        self.play(Write(solution), run_time=1.5)
        self.wait(0.5)

        # Crear una animación más suave para mover la solución
        solution.generate_target()
        solution.target.next_to(equation, DOWN, buff=0.6)
        self.play(MoveToTarget(solution, path_arc=PI / 4), run_time=1)
        
        # 7. Texto final (0:18-0:22)
        final_text = Text(
            "El amor se desvanece...\ny tú eres la causante", 
            font_size=22,
            color=love_color, 
            line_spacing=1.0
        )
        final_text.next_to(solution, DOWN, buff=0.5)
        self.play(Write(final_text), run_time=1.5)
        #self.play(FadeIn(final_text, shift=UP), run_time=1.5)

        self.wait(1)
#----------------------------------------------------- no tocar
        # Colores del cigarro
        naranja_oscuro = "#F4A300"
        naranja_claro = "#FEC660"
        gris_cuerpo = "#E6E6E6"
        rojo_brasa = "#FF4500"

        scaleValue = 0.8  # Escala del cigarro

        # Crear partes
        filtro1 = Rectangle(width=0.25*scaleValue, height=0.15*scaleValue, fill_color=naranja_claro, fill_opacity=1, stroke_color=BLACK, stroke_width=0.5)
        filtro2 = Rectangle(width=0.25*scaleValue, height=0.15*scaleValue, fill_color=naranja_oscuro, fill_opacity=1, stroke_color=BLACK, stroke_width=0.5)
        cuerpo = Rectangle(width=1.5*scaleValue, height=0.15*scaleValue, fill_color=gris_cuerpo, fill_opacity=1, stroke_color=BLACK, stroke_width=0.5)
        brasa = Rectangle(width=0.05*scaleValue, height=0.15*scaleValue, fill_color=rojo_brasa, fill_opacity=1, stroke_color=BLACK, stroke_width=0.5)
        
        # Posicionar
        filtro2.next_to(filtro1, RIGHT, buff=0)
        cuerpo.next_to(filtro2, RIGHT, buff=0)
        brasa.next_to(cuerpo, RIGHT, buff=0)
        cigarro = VGroup(filtro1, filtro2, cuerpo, brasa)
        cigarro.rotate(PI / 30)
        cigarro.move_to(DOWN * 2 + LEFT * 0.7) #---------------

        # Sombra
        sombra = cigarro.copy().set_fill(BLACK, opacity=0.2)
        sombra.shift(DOWN * 0.05 + LEFT * 0.05)
        sombra.z_index = -1

        self.add(sombra, cigarro)
        self.play(FadeIn(cigarro), run_time=1)

        # 🌫️ Función para crear un hilo de humo animado con suavidad
        def crear_animacion_humo():
            x_offset = random.uniform(-0.2, 0.4)
            y_offset = random.uniform(2.0, 3)
            start = brasa.get_corner(UR) + UP * 0.1 + RIGHT * random.uniform(0, 0.05)
            c1 = start + UP * 0.5 + RIGHT * 0.2
            c2 = c1 + UP * y_offset + RIGHT * x_offset

            humo = VMobject()
            humo.set_points_smoothly([start, c1, c2])
            humo.set_stroke(color=WHITE, width=3, opacity=0.0)

            # Animación personalizada: opacidad + subida + curvatura
            def update_humo(mob, alpha):
                new_points = [
                    interpolate(start, c1, alpha),
                    interpolate(c1, c2, alpha)
                ]
                mob.set_points_smoothly([start] + new_points)
                mob.set_opacity(min(1 - abs(alpha - 0.5) * 2, 0.2))  # Aparece, se queda y desaparece
                mob.shift(UP * alpha * 0.8)

            return humo, UpdateFromAlphaFunc(humo, update_humo)

        # Crear muchos humos animados suavemente
        humos = VGroup()
        animaciones = []

        for _ in range(8):
            humo, animacion = crear_animacion_humo()
            humos.add(humo)
            animaciones.append(animacion)

        self.add(*humos)
        self.play(LaggedStart(*animaciones, lag_ratio=0.1, run_time=4))  
    
        #animate_End(scene=self) # finalizar con logo
 

