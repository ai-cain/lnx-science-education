from manim import *
from lnx import *
 

class LinearEquation(Scene):
    def construct(self): 
        backgroundLnx(self)
        title = Text("Resuelve", font_size=34).shift(UP * 3)
        title.set_color_by_gradient(ORANGE, YELLOW)  # Aplicar gradiente de colores
        expr = MathTex(r" \frac{2x+5}{3} = 7 ", font_size=55).shift(UP * 1)

        question = MathTex(r" x=?", font_size=50).next_to(expr, DOWN, buff=1.3)  

        rect = SurroundingRectangle(
            question,
            buff=0.25,
            corner_radius=0.1,
            )
        rect.set_color_by_gradient(YELLOW,  ORANGE)  # Aplicar gradiente veo que no sirve xd
        
        grillado(self)
        self.add(title)
        self.wait(0.2)
        self.play(Write(expr))
        self.wait(1) 
        self.play(
            Succession(
                Wait(1.0), 
                Write(question), 
            ),
            Create(rect, run_time=1.0),
        ) 
        self.wait(3)  





 