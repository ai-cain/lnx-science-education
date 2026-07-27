from manim import *

from lnx import *

class SquareSummation(Scene):
	def construct(self):
		# Fondo personalizado (probablemente con color o imagen)
		backgroundLnx(self)

        # Establecer el template LaTeX con fuentes elegantes (mathpazo + kpfonts)
		self.camera.tex_template = MathPazoKpTemplate()

		a = 3.5  # Tamaño del cuadrado (puedes cambiar este valor para probar)
		font_scale = a / 5
		# Apply gradient color to the square
		wholeSquare = Square(a).shift([0, a / 5, 0]).set_stroke(color=["#00F5FF", "#FF00F5"], width=4)  # Ajustar posición del cuadrado

		# region Expressions
		text_shift = [0, -a / 2, 0]
		 # Escala para reducir el tamaño de la fuente a la mitad
		half = MathTex(r"\frac{1}{2}", font_size=40 * font_scale).shift(text_shift)
		fourth = MathTex(r"\frac{1}{2}", "+", r"\frac{1}{4}", font_size=40 * font_scale).shift(text_shift)
		eighth = MathTex(r"\frac{1}{2}", "+", r"\frac{1}{4}", "+", r"\frac{1}{8}", font_size=40 * font_scale).shift(text_shift)
		sixteenth = MathTex(r"\frac{1}{2}", "+", r"\frac{1}{4}", "+", r"\frac{1}{8}", "+",
		                    r"\frac{1}{16}", font_size=40 * font_scale).shift(text_shift)
		semiFinal = MathTex(r"\frac{1}{2}", "+", r"\frac{1}{4}", "+", r"\frac{1}{8}",
		                    "+", r"\frac{1}{16}", "+", r"\dotsm", "=", "1", font_size=40 * font_scale).shift(text_shift)
		final = MathTex(r"\sum_{n=1}^{\infty}", r"\frac{1}{2^n}", "=", "1", font_size=40 * font_scale).shift(text_shift)
		# endregion

		# region Lines
		halfLine = Line(wholeSquare.get_top(), wholeSquare.get_bottom()).set_color(["#00F5FF", "#FF00F5"])
		fourthLine = Line(halfLine.get_center(), wholeSquare.get_right()).set_color(["#00F5FF", "#FF00F5"])
		eighthLine = Line(fourthLine.get_center(), fourthLine.get_center() + [0, a / 2, 0]).set_color(["#00F5FF", "#FF00F5"])
		sixteenthLine = Line(eighthLine.get_center(), eighthLine.get_center() + [a / 4, 0, 0]).set_color(["#00F5FF", "#FF00F5"])
		thirtysecondLine = Line(sixteenthLine.get_center(), sixteenthLine.get_center() + [0, a / 4, 0]).set_color(["#00F5FF", "#FF00F5"])
		sixtyfourthLine = Line(thirtysecondLine.get_center(), thirtysecondLine.get_center() + [a / 8, 0, 0]).set_color(["#00F5FF", "#FF00F5"])
		oneTwentyEighthLine = Line(sixtyfourthLine.get_center(), sixtyfourthLine.get_center() + [0, a / 8, 0]).set_color(["#00F5FF", "#FF00F5"])
		twoFiftySixthLine = Line(oneTwentyEighthLine.get_center(), oneTwentyEighthLine.get_center() + [a / 16, 0, 0]).set_color(["#00F5FF", "#FF00F5"])
		fiveTwelvthLine = Line(twoFiftySixthLine.get_center(), twoFiftySixthLine.get_center() + [0, a / 16, 0]).set_color(["#00F5FF", "#FF00F5"])
		oneThousandTwentyFourthLine = Line(fiveTwelvthLine.get_center(), fiveTwelvthLine.get_center() + [a / 32, 0, 0]).set_color(["#00F5FF", "#FF00F5"])
		# endregion

		# region Labels
		
		halfLabel = MathTex(r"\frac{1}{2}", font_size=40 * font_scale).next_to(halfLine, LEFT, [a / 4, 0, 0])
		fourthLabel = MathTex(r"\frac{1}{4}", font_size=40 * font_scale).next_to(fourthLine, DOWN * (a / 2))
		eighthLabel = MathTex(r"\frac{1}{8}", font_size=35 * font_scale).next_to(eighthLine, LEFT * (a / 2))
		sixteenthLabel = MathTex(r"\frac{1}{16}", font_size=30 * font_scale).next_to(sixteenthLine, DOWN * (a / 4))
		thirtysecondLabel = MathTex(r"\frac{1}{32}", font_size=25 * font_scale).next_to(thirtysecondLine, LEFT * (a / 4))
		sixtyfourthLabel = MathTex(r"\frac{1}{64}", font_size=20 * font_scale).next_to(sixtyfourthLine, DOWN * (a / 8))
		oneTwentyEighthLabel = MathTex(r"\frac{1}{128}", font_size=15 * font_scale).next_to(oneTwentyEighthLine, LEFT * (a / 16))
		twoFiftySixthLabel = MathTex(r"\frac{1}{256}", font_size=10 * font_scale).next_to(twoFiftySixthLine, DOWN * (a / 16))
		fiveTwelvthLabel = MathTex(r"\frac{1}{512}", font_size=5 * font_scale).next_to(fiveTwelvthLine, LEFT * (a / 32))
		oneThousandTwentyFourthLabel = MathTex(r"\frac{1}{1024}", font_size=4 * font_scale).next_to(oneThousandTwentyFourthLine,
		                                                                                           DOWN * (a / 32))
		# endregion
		##copy text label
		halfLabelCopy = halfLabel.copy()
		fourthLabelCopy = fourthLabel.copy()
		eighthLabelCopy = eighthLabel.copy()
		sixteenthLabelCopy = sixteenthLabel.copy()
		
		halfLabelCopy.font_size = 40 * font_scale
		fourthLabelCopy.font_size = 40 * font_scale 
		eighthLabelCopy.font_size = 40 * font_scale
		sixteenthLabelCopy.font_size = 40 * font_scale

		thirtysecondLabelCopy = thirtysecondLabel.copy()
		sixtyfourthLabelCopy = sixtyfourthLabel.copy()
		oneTwentyEighthLabelCopy = oneTwentyEighthLabel.copy()
		twoFiftySixthLabelCopy = twoFiftySixthLabel.copy()
		fiveTwelvthLabelCopy = fiveTwelvthLabel.copy()
		oneThousandTwentyFourthLabelCopy = oneThousandTwentyFourthLabel.copy()
		##
		all = VGroup(wholeSquare, halfLine, fourthLine, eighthLine, sixteenthLine, thirtysecondLine,
		             sixtyfourthLine, oneTwentyEighthLine, twoFiftySixthLine, fiveTwelvthLine,
		             oneThousandTwentyFourthLine,

		             halfLabel, fourthLabel, eighthLabel, sixteenthLabel, thirtysecondLabel,
		             sixtyfourthLabel, oneTwentyEighthLabel, twoFiftySixthLabel, fiveTwelvthLabel,
		             oneThousandTwentyFourthLabel,

		             semiFinal)

		self.play(Create(wholeSquare))
		self.wait(1)
#--------------------------- para el 1/2
		self.play(Create(halfLine), Create(halfLabel)) 
		self.play(Transform(halfLabelCopy,half))
		self.play(Write(half, run_time=0.2))
		self.remove(halfLabelCopy)  # Eliminación inmediata 
#--------------------------- para el 1/4
		self.play(Create(fourthLine), Create(fourthLabel))
		# Posición base (borde derecho de `fourth` alineado con borde derecho de `fourthLabelCopy`)
		target_position_4 = fourth.get_right() - [fourthLabelCopy.width, 0, 0]  
		target_position_4[1] = fourth.get_center()[1]  # Misma altura (Y)

		# Ajuste manual adicional (ejemplo: mover 0.2 unidades más a la derecha)
		target_position_4 += RIGHT * 0.1  # <- Cambia este valor según necesites

		# Animación:
		self.play(
			fourthLabelCopy.animate.move_to(target_position_4),
			TransformMatchingTex(half, fourth),
			run_time=1
		)
		self.remove(fourthLabelCopy)  # Eliminación inmediata
#--------------------------- para el 1/8
		self.play(Create(eighthLine), Create(eighthLabel))
 
		target_position_8 = eighth.get_right() - [eighthLabelCopy.width, 0, 0]  
		target_position_8[1] = eighth.get_center()[1]  # Misma altura (Y)

		# Ajuste manual adicional (ejemplo: mover 0.2 unidades más a la derecha)
		target_position_8 += RIGHT * 0.05  # <- Cambia este valor según necesites

		# Animación:
		self.play(
			eighthLabelCopy.animate.move_to(target_position_8).set_run_time(0.1),  # Más rápido (0.3 seg)
			TransformMatchingTex(fourth, eighth, run_time=1),  # Duración normal (1 seg)
			lag_ratio=0  # Sin retraso entre animaciones
		)
		self.remove(eighthLabelCopy)  # Eliminación inmediata 
#--------------------------- para el 1/16		

		self.play(Create(sixteenthLine), Create(sixteenthLabel))

		target_position_16 = sixteenth.get_right() - [sixteenthLabelCopy.width, 0, 0]  
		target_position_16[1] = sixteenth.get_center()[1]  # Misma altura (Y)

		# Ajuste manual adicional (ejemplo: mover 0.2 unidades más a la derecha)
		target_position_16 += RIGHT * 0.1  # <- Cambia este valor según necesites

		# Animación:
		self.play(
			sixteenthLabelCopy.animate.move_to(target_position_16).set_run_time(0.1),  # Más rápido (0.3 seg)
			TransformMatchingTex(eighth, sixteenth, run_time=1),  # Duración normal (1 seg)
			lag_ratio=0  # Sin retraso entre animaciones
		)
		self.remove(sixteenthLabelCopy)  # Eliminación inmediata 
 

#--------------------------- para el 1/32		

		self.play(Create(thirtysecondLine), Create(thirtysecondLabel))
		self.play(TransformMatchingTex(sixteenth, semiFinal))

		self.play(Create(sixtyfourthLine), Create(sixtyfourthLabel))

		self.play(Create(oneTwentyEighthLine), Create(oneTwentyEighthLabel))

		self.play(Create(twoFiftySixthLine), Create(twoFiftySixthLabel))

		self.play(Create(fiveTwelvthLine), Create(fiveTwelvthLabel))

		self.play(Create(oneThousandTwentyFourthLine), Create(oneThousandTwentyFourthLabel))
		self.wait(2)
		self.play(all.animate.scale(6, about_point=wholeSquare.get_corner(UR)))
		self.wait(1)
		self.play(all.animate.scale(1/6, about_point=wholeSquare.get_corner(UR)))
		self.wait(1.5)
		self.play(Transform(semiFinal, final))

		box = SurroundingRectangle(
            final, buff=0.1, 
            color=YELLOW,  # Base color 
            corner_radius=0.1
        )
		box.set_stroke(
            width=3, 
            color=[ "#FFEE00", "#9D00FF"]  # Gradient colors
        )
        
		self.play(
			Create(box),
			run_time=0.5
		)

		self.wait(1.5)

		animate_End(scene=self) # finalizar con logo

		#with tempconfig({"preview": True, "quality": "high_quality", "disable_caching": True}):
		#   scene = CompleteAnimation()
		#  scene.render()