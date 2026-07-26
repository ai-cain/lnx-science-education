from manim import *
from lnx import *


class MathProblems(Scene):
    def construct(self):
        backgroundLnx(self) 
        self.camera.tex_template = MathPazoKpTemplate()
        grillado(self)
        imagen = ImageMobject(LOGO_MAIN)

        # Escalar imagen (horizontal x vertical)
        imagen.scale(0.4*0.4)  # primero escalar proporcionalmente

        # Mover imagen 2.8 unidades abajo del centro
        imagen.shift(DOWN * 2.9)

        # Mostrar imagen sin animación
        self.add(imagen)
         
        title=  Tex(r"\textbf{Desafío a la Comunidad}", font_size=30).shift(UP * 2.6)
        title.set_color_by_gradient(GOLD, ORANGE) 
        self.play(Write(title))

        # Basic Level
        basic_title = Tex(r"\textbf{Nivel 1}", font_size=25).next_to(title, DOWN, buff=0.6)  
        basic_title.set_color(YELLOW) # Aplicar gradiente de colores
        self.play(Write(basic_title))
        self.wait(0.5)
        
        prob1 = MathTex(
            r"\circ \int_0^{\pi} \frac{\sin x}{\sqrt{\sin x} + 1} \, \mathrm{d}x",
            font_size=22
        ).next_to(basic_title, DOWN, buff=0.8) 
        
        prob2 = MathTex(
            r"\circ \int_0^1 \ln^2(1+x^2) \, \mathrm{d}x",
            font_size=22
        ).next_to(prob1, DOWN, buff=0.8) 

        # Add animations here
        self.play(Write(prob1))
        self.wait(1)
        self.play(Write(prob2))
        self.wait(3)
        
        # Intermediate Level
        intermediate_title = Tex(r"\textbf{Nivel 2}", font_size=25).next_to(title, DOWN, buff=0.5)  
        intermediate_title.set_color(ORANGE)
        #-----------------
        

        
        # Agrupar y organizar verticalmente
        prob3 = MathTex(
            r"\circ \lim_{n \to \infty} \begin{pmatrix} 1-\frac{1}{n^2} & \frac{1}{n} \\ \frac{1}{n} & 1+\frac{1}{n} \end{pmatrix}^n",
            font_size=22  # Corrección: "font_size" en lugar de "font_siz"
        ).next_to(intermediate_title, DOWN, buff=0.7)
                
        
        prob4 = MathTex(
            r"\circ \int_{0}^{\infty} \frac{\ln^2(x)}{\cosh(x)  } \mathrm{d}x", 
            font_size=20
        ).next_to(prob3, DOWN, buff=0.7) 
        
        prob5 = MathTex(
            r"	\circ \int_0^{\infty} \frac{\ln(1+x^2)}{(1+x^3)^3} \mathrm{d}x",
            font_size=20
        ).next_to(prob4, DOWN, buff=0.7) 

        self.play(Transform(basic_title, intermediate_title),
                  FadeOut(prob1),
                  FadeOut(prob2)
                  )
        self.play(Write(prob3))
        self.wait(1)
        self.play(Write(prob4))
        self.wait(1)
        self.play(Write(prob5))
        self.wait(3)
 #------------------------------       
        # Advanced Level
        advanced_title = Tex(r"\textbf{Nivel 3}", font_size=25).next_to(title, DOWN, buff=0.8)  
        advanced_title.set_color(RED)
       

        prob6 = MathTex(
            r"\circ \, \text{ Dada }A = \begin{pmatrix} a & b \\ b & a \end{pmatrix}.\, \,  \text{Calcule,}\\[10pt]",  # 10pt de espacio extra
            r"\int_0^\infty \frac{\cos(Ax) + x \sin(Ax)}{x^2 + 1} \, \mathrm{d}x",
            #tex_environment="align*",  # Entorno alineado (opcional)
            font_size=18
        ).next_to(advanced_title, DOWN, buff=0.3)
        
        prob7 = MathTex(
            r"\circ \int_{-1}^1 \frac{\ln^2(1+x^2)}{\sqrt{1-x^2}} \, \mathrm{d}x",
            font_size=20
        ).next_to(prob6, DOWN, buff=0.3) 
        
        prob8 = MathTex(
            r"\circ \int_0^1 \frac{(\text{Li}_{6}{(x)} +x\text{Li}_{5}{(x)})  \text{Li}_{5}{(x)} }{x}  \, \mathrm{d}x",
            font_size=20
        ).next_to(prob7, DOWN, buff=0.3) 
        
        polylog_def = MathTex(
            r"\text{Donde }  \text{Li}_{n}{(x)}  = \sum_{k=1}^\infty \frac{x^k}{k^n} \text{ para } |x| \leq 1",
            font_size=18
        ).next_to(prob8, DOWN, buff=0.3).set_color(GOLD) 
         
        
        self.play(Transform( intermediate_title, advanced_title ),
                        FadeOut(prob3),
                        FadeOut(prob4),
                        FadeOut(prob5),
                        FadeOut(basic_title)
                        )
        self.play(Write(prob6))
        self.wait(1)
        self.play(Write(prob7))
        self.wait(1)
        self.play(Write(prob8))
        self.wait(1)
        self.play(Write(polylog_def))
        self.wait(3)

        # Expert Level
        expert_title = Tex(r"\textbf{Nivel 4}", font_size=25).next_to(title, DOWN, buff=0.7) .set_color(YELLOW_E) 
        
        prob9 = MathTex(
            r"\circ \lim_{n \to \infty} \left[ n^2 \ln \left( \lim_{t \to 0^+} \left( \int_0^1 \frac{\mathrm{d}x}{\sqrt[n]{x^n + t^n}} + \ln t \right) \right) \right]",
            font_size=20
        ).next_to(advanced_title, DOWN, buff=0.7) 
        
        prob10 = MathTex(
            r"\circ \lim_{x \to \infty} \left[ \frac{1}{x} \left( \frac{\zeta\left(1 + \frac{1}{x}\right)}{x} \right)^{\frac{x}{\gamma}}"
            r"\left( \frac{(2x)!}{x!} \right)^{\frac{1}{x}} - 4 \right] x",
            font_size=21
        ).next_to(prob9, DOWN, buff=0.7) 

        
        prob10_explanation = MathTex(
            r"\text{Donde } \zeta(s) \text{ es la función zeta de Riemann}",
            font_size=18
        ).next_to(prob10, DOWN, buff=0.7).set_color(GOLD) 
        prob10_explanation_2 = MathTex(
            r"\gamma \text{ es la constante de Euler-Mascheroni}.}",
            font_size=18
        ).next_to(prob10_explanation, DOWN, buff=0.2).set_color(GOLD) 
        
        self.play(Transform( advanced_title, expert_title  ),
                        FadeOut(prob6),
                        FadeOut(prob7),
                        FadeOut(prob8),
                        FadeOut(intermediate_title),
                        FadeOut(polylog_def)
                        )
        self.play(Write(prob9))
        self.wait(1)
        self.play(Write(prob10))
        self.play(Write(prob10_explanation))
        self.play(Write(prob10_explanation_2))
        
        self.wait(4)