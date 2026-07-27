from manim import *
import numpy as np

class JacobianoEsfera(ThreeDScene):
    def construct(self): 
        font_size = 20  # Variable para el tamaño de fuente
        animation_time = 1  # Tiempo base para animaciones

        self.camera.frame_center = [0, -1, 0]  # Ajuste de centro

        # Título
        titulo = Tex("Cálculo del Jacobiano en coordenadas esféricas", font_size=font_size).to_edge(UP)
        self.add_fixed_in_frame_mobjects(titulo)

        # Sistema de ecuaciones
        ecuaciones = VGroup(
            MathTex(r"x = \rho \sin\phi \cos\theta", font_size=font_size),
            MathTex(r"y = \rho \sin\phi \sin\theta", font_size=font_size),
            MathTex(r"z = \rho \cos\phi", font_size=font_size)
        ).arrange(DOWN).to_edge(LEFT)

        self.play(Write(ecuaciones), run_time=animation_time)
        self.wait(animation_time)

        # Matriz Jacobiana
        jacobiano_title = Tex("Matriz Jacobiana:", font_size=font_size).to_edge(LEFT)
        matriz_jacobiana = MathTex(
            r"J = \begin{bmatrix}"
            r"\frac{\partial x}{\partial \rho} & \frac{\partial x}{\partial \phi} & \frac{\partial x}{\partial \theta} \\"
            r"\frac{\partial y}{\partial \rho} & \frac{\partial y}{\partial \phi} & \frac{\partial y}{\partial \theta} \\"
            r"\frac{\partial z}{\partial \rho} & \frac{\partial z}{\partial \phi} & \frac{\partial z}{\partial \theta}"
            r"\end{bmatrix}",
            font_size=font_size
        ).next_to(jacobiano_title, DOWN, aligned_edge=LEFT)

        self.add_fixed_in_frame_mobjects(jacobiano_title)
        self.play(Write(matriz_jacobiana), run_time=animation_time * 2)
        self.wait(animation_time)

        # Derivadas parciales
        derivadas = VGroup(
            MathTex(r"\frac{\partial x}{\partial \rho} = \sin\phi \cos\theta", font_size=font_size),
            MathTex(r"\frac{\partial x}{\partial \phi} = \rho \cos\phi \cos\theta", font_size=font_size),
            MathTex(r"\frac{\partial x}{\partial \theta} = -\rho \sin\phi \sin\theta", font_size=font_size),
            MathTex(r"\frac{\partial y}{\partial \rho} = \sin\phi \sin\theta", font_size=font_size),
            MathTex(r"\frac{\partial y}{\partial \phi} = \rho \cos\phi \sin\theta", font_size=font_size),
            MathTex(r"\frac{\partial y}{\partial \theta} = \rho \sin\phi \cos\theta", font_size=font_size),
            MathTex(r"\frac{\partial z}{\partial \rho} = \cos\phi", font_size=font_size),
            MathTex(r"\frac{\partial z}{\partial \phi} = -\rho \sin\phi", font_size=font_size),
            MathTex(r"\frac{\partial z}{\partial \theta} = 0", font_size=font_size)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)

        self.play(Write(derivadas), run_time=animation_time * 3)
        self.wait(animation_time)

        # Determinante del Jacobiano
        det_label = Tex("Determinante del Jacobiano:", font_size=font_size).to_edge(DOWN)
        det_result = MathTex(r"\det(J) = \rho^2 \sin\phi", font_size=font_size).next_to(det_label, RIGHT)

        self.add_fixed_in_frame_mobjects(det_label)
        self.play(Write(det_label), run_time=animation_time)
        self.play(Write(det_result), run_time=animation_time)
        self.wait(animation_time)

        # Explicación visual
        arc = Arc(radius=0.5, start_angle=0, angle=PI/2, color=YELLOW)
        arrow = Arrow(start=ORIGIN, end=[0.5, 0.5, 0], buff=0, color=RED)
        note = Tex("Ángulo $\\phi$ afecta el área", font_size=font_size).next_to(arc, UR, buff=0.1)

        self.play(Create(arc), GrowArrow(arrow), Write(note), run_time=animation_time * 2)
        self.wait(animation_time)

