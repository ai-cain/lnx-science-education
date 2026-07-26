from manim import *
from lnx import *

# Clase principal de animación
class CompleteAnimation(Scene):
    def construct(self):
        # Fondo personalizado  
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate() #fonts PazoKp

        box_anim = BoxAnimation( self, image_path=LOGO_MAIN,  ) #box start
        box_anim.on()
         
        logo_handler(  scene=self, image_path=LOGO_MAIN ) #Mover logo con ajustes
        
        # 4. El resto de tu lógica original
        self.wait(2)
        #box_anim.off() # clear logo , si es que no hay logo_handler 
        
        #------------------------------------------
 
        # TEXTO: Enunciado del problema
        texto1 = MathTex( 
            r"\text{Ejemplo de plantilla de Lnx} ",
            font_size=22
        )
        self.play(Write(texto1),run_time=0.5)  # Escribir el enunciado

        self.wait(0.5)  # tiempo para cambiar a logo
    
        animate_End(scene=self) # finalizar con logo
 



 