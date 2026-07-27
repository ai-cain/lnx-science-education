from manim import *
from lnx import *

colorTitle= "#4FC3F7"  # Azul turquesa claro (para destacar)
colorFormula= "#33deea"  # Azul intenso (profundidad)
colorNameF = "#E1F5FE"  # Blanco azulado (legibilidad)
colornc = "#00B4D8"  # Turquesa brillante (énfasis)

fontSize1 = 27
buffSize=1.2
class Intro(ThreeDScene):
	def construct(self):
		
					
		title = Title("Volúmen en 3D", font_size=30).shift(DOWN*0.5)
		title.set_color_by_gradient(ORANGE, YELLOW)

		#text1 = Text("Today we will see the ", font_size=50)
		#text2 = Text("volume of different 3d shapes", font_size=50).next_to(text1, DOWN)

		self.play(Write(title))
		self.wait(1)
		#self.play(AddTextLetterByLetter(text1, run_time=0.5))
		#self.play(AddTextLetterByLetter(text2, run_time=0.5))
		#self.wait(2)
		#self.play(FadeOut(VGroup(title, text1, text2)))
		self.play(FadeOut( title ))
		#self.wait(2)

		CuboidVolume.construct(self)


class CuboidVolume(ThreeDScene):
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
		 

		title = MathTex(r"\text{Paralelepípedo}", font_size=45).shift(UP*2.7).set_color( colorTitle)

		scaleValue= 0.1
		sizeCubo = 2
		

		length = MathTex("l", font_size=fontSize1 , color=colorFormula).next_to(title, DOWN, buff=buffSize)
		area = MathTex("l", r"\cdot", "b", font_size=fontSize1 , color=colorFormula).next_to(title, DOWN, buff=buffSize)
		volume = MathTex("l", r"\cdot", "b", r"\cdot", "h", font_size=fontSize1, color=colorFormula ).next_to(title, DOWN, buff=buffSize) 
		label = [
			MathTex(r" \text{Longitud}", font_size=fontSize1, color=colorNameF).next_to(length, UP, buff=0.3),
			MathTex(r" \text{Área}", font_size=fontSize1, color=colorNameF).next_to(area, UP, buff=0.3),
			MathTex(r" \text{Volumen}", font_size=fontSize1, color=colorNameF).next_to(volume, UP, buff=0.3),
        ]
		
		dot = Dot()
		line = Rectangle(width=sizeCubo, height=0.0000001, color=BLUE_A)
		rect = Rectangle(width=sizeCubo, height=sizeCubo/2 , color=BLUE_D)
		cuboid = Prism(
            dimensions=[sizeCubo, sizeCubo/2, sizeCubo/2],  # Ancho, profundidad, altura
            fill_opacity=0.3,      # Opacidad del relleno (0 para solo borde)
            #fill_color=RED,       # Color del relleno
            stroke_color=WHITE,   # Color del borde
            stroke_width=2,      # Grosor del borde
        )
		#cuboid.rotate(-10 * DEGREES, Y_AXIS).rotate(-90 * DEGREES, X_AXIS).rotate(45 * DEGREES, Y_AXIS).shift([0, 0, 0])
		cuboid.rotate(45*DEGREES, Y_AXIS)      # Primera rotación horizontal
		cuboid.rotate(35.264*DEGREES, X_AXIS)  # Ángulo mágico isométrico
	
		self.play(Create(title))
		self.play(Create(dot))
		self.wait(0.2)
		self.play(ReplacementTransform(dot, line), Write(length), Write(label[0]))
		self.wait(1)
		self.play(ReplacementTransform(line, rect), TransformMatchingTex(length, area),
		          TransformMatchingShapes(label[0], label[1]))
		self.wait(1)
		self.play(rect.animate.shift([0, -1, 0]))
		self.play(Rotate(rect, -90 * DEGREES, X_AXIS))
		self.wait(0.000000001)
		self.play(Rotate(rect, 45 * DEGREES, Y_AXIS))
		self.play(Transform(rect, cuboid), TransformMatchingTex(area, volume),
		          TransformMatchingShapes(label[1], label[2]))
		self.wait(1.5)
		self.play(FadeOut(title, volume, label[2]))
		self.remove(cuboid, rect)
		#self.wait(2)
		SphereVolume.construct(self)


class SphereVolume(ThreeDScene):
	def construct(self): 
  
		title = MathTex(r"\text{Esfera}", font_size=45).shift(UP*2.7).set_color(colorTitle)

		radius = MathTex("r", font_size=fontSize1 , color=colorFormula).next_to(title, DOWN, buff=buffSize)
		area = MathTex(r"\pi", r"\cdot", "r^{2}", font_size=fontSize1, color=colorFormula ).next_to(title, DOWN, buff=buffSize)
		volume = MathTex(r"\frac{4}{3}", r"\pi", "r^{3}", font_size=fontSize1 , color=colorFormula).next_to(title, DOWN, buff=buffSize)

		label = [
				MathTex(r"\text{Radio}", font_size=fontSize1, color=colorNameF).next_to(radius,UP, buff=0.3),
				MathTex(r"\text{Área}", font_size=fontSize1, color=colorNameF).next_to(area, UP, buff=0.3),
				MathTex(r"\text{Volumen}", font_size=fontSize1, color=colorNameF).next_to(volume, UP, buff=0.3),
		]

		radiusValue=1

		dot = Dot().shift([0, -0.5, 0])
		line = Line([0, -0.5, 0], [radiusValue, -0.5, 0], color=BLUE_A)
		circle = Circle(radius=radiusValue, color=BLUE).shift([0,  -0.5, 0])

		sphere = Sphere(center=[0, -0.5, 0], radius=radiusValue, resolution=(30, 30)).rotate(40 * DEGREES, X_AXIS) #150,150

		self.play(Create(title))
		self.wait(0.5)
		self.play(Create(dot))
		self.wait(0.5)
		self.play(Create(line), Write(radius), Write(label[0]))
		self.wait(1)
		self.play(Create(circle, run_time=1),
		          Rotate(line, 360 * DEGREES, run_time=1, about_point=[0, -0.5, 0]),
		          TransformMatchingTex(radius, area),
		          TransformMatchingShapes(label[0], label[1]))
		self.wait(1)
		self.play(FadeOut(line, dot))
		self.play(circle.animate.rotate(40 * DEGREES, X_AXIS))
		self.wait(1)
		self.play(Rotate(circle, 360 * DEGREES, axis=[0, 1, 1], run_time=1, rate_func=linear),
		          Create(sphere, run_time=1))
		self.play(TransformMatchingTex(area, volume),
		          TransformMatchingShapes(label[1], label[2]))
		self.wait(1)
		self.play(FadeOut(VGroup(title, volume, label[2], sphere, circle)))
		#self.wait(2)
		CylinderVolume.construct(self)

class CylinderVolume(ThreeDScene):
	def construct(self):
		 
  
		title = MathTex(r"\text{Cilindro}", font_size=45).shift(UP*2.7).set_color(colorTitle)


		radius = MathTex("r", font_size=fontSize1 , color=colorFormula).next_to(title, DOWN, buff=buffSize)
		area = MathTex(r"\pi", r"\cdot", "r^{2}", font_size=fontSize1, color=colorFormula ).next_to(title, DOWN, buff=buffSize)
		volume = MathTex(r"\pi", r"\cdot", "r^{2}", r"\cdot", "h", font_size=fontSize1 , color=colorFormula).next_to(title, DOWN, buff=buffSize)

		label = [
				MathTex(r"\text{Radio}", font_size=fontSize1, color=colorNameF).next_to(radius, UP, buff=0.3),
				MathTex(r"\text{Área}", font_size=fontSize1, color=colorNameF).next_to(area, UP, buff=0.3),
				MathTex(r"\text{Volumen}", font_size=fontSize1, color=colorNameF).next_to(volume, UP, buff=0.3),
		]

		dot = Dot().shift([0, -1/2, 0])
		line = Line([0, -1/2, 0], [1.3/2, -1/2, 0], color= DARK_BLUE)
		circle = Circle(radius=1.3/2, color=BLUE_B).shift([0, -1/2, 0])
  
  

		cylinder = Cylinder(1.3/2, 4/2, Y_AXIS).shift([0, -1/2, 0])
		 

		self.play(Create(title))
		self.wait(0.5)
		self.play(Create(dot))
		self.play(Create(line), Write(radius), Write(label[0]))
		self.wait(1)
		self.play(Create(circle, run_time=1),
		          Rotate(line, 360 * DEGREES, run_time=1, about_point=[0, -1/2, 0]),
		          TransformMatchingTex(radius, area),
		          TransformMatchingShapes(label[0], label[1]))
		self.wait(1)
		self.play(FadeOut(line, dot))
		self.wait(0.5)
		self.play(circle.animate.shift([0, -2/2, 0]))
		self.play(Rotate(circle, -90 * DEGREES, X_AXIS))
		self.wait(0.000000001)
		self.play(Rotate(circle, 45 * DEGREES, Y_AXIS))
		self.wait(1)
		self.play(Transform(circle, cylinder),
		          TransformMatchingTex(area, volume),
		          TransformMatchingShapes(label[1], label[2]))
		self.wait(2)
		self.play(FadeOut(VGroup(title, volume, label[2], cylinder, circle))) 
