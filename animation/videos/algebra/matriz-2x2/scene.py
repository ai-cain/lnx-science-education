from manim import *
import numpy as np 
from lnx import backgroundLnx, BoxAnimation, SmartMathTex, MathPazoKpTemplate, logo_handler, animate_End, LOGO_SVG, LOGO_MAIN

class matrixTest(Scene):
	
	def construct(self):
		backgroundLnx(self)
		self.camera.tex_template = MathPazoKpTemplate()
	
		A = np.array([[2, 9], [-1, 11]])
		B = np.array([[3, 7], [0, -2]])
		C = np.dot(A, B)
		
		stuff = VGroup(Matrix(A), Matrix(B), Matrix(C))
		matrixA = stuff[0]
		matrixB = stuff[1]
		matrixC = stuff[2]

		font_size_main = 25
		matrix_height = 2.5 * font_size_main / 100

		matrixA.height = matrix_height
		matrixB.height = matrix_height
		matrixA.color = [GOLD_A, GOLD_D, ORANGE]  # Gradiente amarillo -> rojo
		matrixB.color = [BLUE_C, BLUE_E]  # Gradiente azul claro -> morado
		matrixC.color = [GREEN_D, GREEN_B]  # Gradiente azul claro -> morado

		# Apply stroke width to brackets and numbers of matrixA
		for element in matrixA.get_entries():
			element.set_stroke(width=2)
		for bracket in matrixA.get_brackets():
			bracket.set_stroke(width=2)

		# Apply stroke width to brackets and numbers of matrixB
		for element in matrixB.get_entries():
			element.set_stroke(width=2)
		for bracket in matrixB.get_brackets():
			bracket.set_stroke(width=2)
		
		Dot = Tex(".", color=WHITE, font_size = font_size_main*2).set_stroke(width=2)
		Equals = Tex("=", color=WHITE, font_size = font_size_main).set_stroke(width=2)
		bOpen = Tex("[", color=WHITE, font_size = font_size_main).set_stroke(width=2)
		bClose = Tex("]", color=WHITE, font_size=font_size_main).set_stroke(width=2)
		bOpen1 = Tex("[", color=WHITE, font_size=font_size_main*2).set_stroke(width=2)
		bClose1 = Tex("]", color=WHITE, font_size=font_size_main*2).set_stroke(width=2)

		title = Text("Multiplicación   de matrices", font_size=0.8*font_size_main).set_color_by_gradient("#FFD700", "#FFA500").set_stroke(width=1.2)
		title.move_to(UP * 2.9)
		self.play(Write(title))
		self.wait(0.5)

		altura_intermedia = UP * 2  # 1.5 unidades arriba del centro (ajusta el valor)
		posicion_final = altura_intermedia + LEFT * 1  # Combina altura + izquierda 
		self.play(Write(matrixA))
		self.play(matrixA.animate.scale(1).move_to(posicion_final)) #.to_corner(UP+LEFT*2))
		
		Dot.next_to(matrixA, RIGHT)
		self.play(Write(Dot))
		
		self.play(Write(matrixB))
		self.play(matrixB.animate.scale(1).next_to(Dot, RIGHT))
		
		# Posiciona "=" 0.7 unidades abajo del centro
		Equals.move_to(0.7 * DOWN)  

		# Calcula la posición de matrixC: derecha del "=" con espacio
		pos_matrixC = Equals.get_center() + RIGHT * (9*Equals.width/2 )
		matrixC.move_to(pos_matrixC)

		self.play(Write(Equals))
		matrixC.height = matrix_height  # Ajustar la altura de la matriz C
		#matrixC.set_font_size(font_size_main)  # Ajustar el tamaño de la fuente
		C_elements = VGroup(*matrixC)
		for i in C_elements[1:]:
			i.height = matrix_height
			i.set_stroke(width=2)  # Hacer los números más gruesos
			self.play(Write(i))
		C_elements = VGroup(*C_elements[0])
		A_rows = matrixA.get_rows()
		A = VGroup(A_rows[0], A_rows[0], A_rows[1], A_rows[1])
		B_columns = matrixB.get_columns()
		B = VGroup(B_columns[0], B_columns[1], B_columns[0], B_columns[1])
		
		A_rows = matrixA.get_rows()
		B_columns = matrixB.get_columns()

		
		for i in range(len(A_rows)):
			for j in range(len(B_columns)):
				_bOpen = bOpen.copy()
				_bClose = bClose.copy()
				_bOpen1 = bOpen1.copy()
				_bClose1 = bClose1.copy()
				_Dot = Dot.copy()
				_r = A_rows[i].copy()
				_c = B_columns[j].copy()
				ans = matrixC.get_entries()[i * len(B_columns) + j]
				
				_bOpen.next_to(matrixA, DOWN*3)
				self.play(Write(_bOpen))
				self.play(_r.set_color(RED_A).animate.next_to(_bOpen))
				_bClose.next_to(_r, RIGHT)
				self.play(Write(_bClose))
				_Dot.next_to(_bClose, RIGHT)
				self.play(Write(_Dot))
				_bOpen1.next_to(_Dot, RIGHT)
				self.play(Write(_bOpen1))
				self.play(_c.set_color(YELLOW).animate.next_to(_bOpen1))
				_bClose1.next_to(_c, RIGHT)
				self.play(Write(_bClose1))
				
				g = VGroup(_bOpen, _r, _bClose, _Dot, _bOpen1, _c, _bClose1)
				ans.font_size = 80 * font_size_main / 100
				ans.set_color(GREEN)
				ans.set_stroke(width=2)  # Hacer los números más gruesos
				self.play(Transform(g, ans))
		
			
		self.wait(2) 
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
		self.play(Create(outline_path), run_time=1)
		self.wait(0.2)

		# Mostrar el logo completo con colores aplicados
		self.play(FadeOut(outline_path), run_time=0.5)
		self.play(FadeIn(logo))
		# Finalizar la escena
		self.wait(0.5)

