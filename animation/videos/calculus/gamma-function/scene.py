#( Manim v0.19.0)
from manim import *
from lnx import backgroundLnx, BoxAnimation, SmartMathTex, MathPazoKpTemplate, logo_handler, animate_End, LOGO_SVG, LOGO_MAIN
import numpy as np
from scipy.integrate import quad
from scipy.special import gamma as scipy_gamma  # Usaremos esta como referencia
from scipy.special import erf  # Importamos la función error

class GraphSpecial(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()
        # plot_gamma(self)
        # plot_error(self)
        plot_exponential_integral(self)  # Llamamos a la nueva función para graficar E_n(z)

def plot_gamma(scene):
    # Configuración de ejes (tamaño original)
    x_range = [-4, 4, 1]
    y_range = [-5, 5, 1]

    x_range_0 = [x_range[0] - 1, x_range[1] + 1, 1]
    y_range_0 = [y_range[0] - 1, y_range[1] + 1, 1]
    ancho_permitido = 4
    ancho = 9

    x_length = ((x_range_0[1] - x_range_0[0]) / ancho) * ancho_permitido
    y_length = ((y_range_0[1] - y_range_0[0]) / ancho) * ancho_permitido

    axes = Axes(
        x_range=x_range_0,
        y_range=y_range_0,
        x_length=x_length,
        y_length=y_length,
        axis_config={
            "font_size": 16,
            "color": RED_A,
            "tip_width": 0.1,
            "tip_height": 0.1,
        },
        x_axis_config={
            "include_numbers": True,
            "numbers_to_exclude": [-5, 5],
        },
        y_axis_config={
            "include_numbers": True,
            "numbers_to_exclude": [-7, -6, 6],
        },
    )
    axes_labels = axes.get_axis_labels(
        MathTex("x", font_size=18).next_to(axes.x_axis, DOWN, buff=0.2),
        MathTex(r"\Gamma(x)", font_size=18).next_to(axes.y_axis, LEFT, buff=0.2),
    )

    # Función Gamma mejorada para valores negativos
    def gamma_extended(x):
        try:
            if x > 0:
                return np.clip(float(scipy_gamma(x)), y_range[0], y_range[1])
            elif x < 0 and not x.is_integer():
                return np.clip(np.pi / (np.sin(np.pi * x) * scipy_gamma(1 - x)), y_range[0], y_range[1])
            return None
        except:
            return None

    # Dominios de graficación con muestreo adaptativo
    domains = []
    for n in range(0, -x_range[0]):
        domains.append([-n - 0.99, -n - 0.01, 0.01])
    domains.append([0.01, -x_range[0], 0.05])

    # Graficación robusta
    gamma_graphs = VGroup()
    for domain in domains:
        start, end, step = domain
        x_vals = np.arange(start, end + step / 2, step)

        points = []
        for x in x_vals:
            y = gamma_extended(x)
            if y is not None and np.isfinite(y):
                points.append(axes.c2p(x, y))

        if len(points) > 1:
            graph = VMobject()
            graph.set_points_smoothly(points)
            graph.set_color_by_gradient(BLUE, GREEN, YELLOW)
            graph.set_stroke(
                width=1.8,
                opacity=1,
            )
            gamma_graphs.add(graph)

    scene.play(Create(axes), Write(axes_labels))
    scene.play(Create(gamma_graphs), run_time=3)
    scene.wait(2)

def plot_error(scene):
    # Configuración de ejes para la función error
    x_range = [0, 1.6, 0.2]
    y_range = [-4, 4, 1]

    x_range_0 = [x_range[0] - 0.2, x_range[1] + 0.2, 0.2]
    y_range_0 = [y_range[0] - 1, y_range[1] + 1, 1]
    ancho_permitido = 4
    ancho = 9

    x_length = ((x_range_0[1] - x_range_0[0]) / ancho) * ancho_permitido
    y_length = ((y_range_0[1] - y_range_0[0]) / ancho) * ancho_permitido

    axes = Axes(
        x_range=x_range_0,
        y_range=y_range_0,
        x_length=x_length,
        y_length=y_length,
        axis_config={
            "font_size": 16,
            "color": RED_A,
            "tip_width": 0.1,
            "tip_height": 0.1,
        },
        x_axis_config={
            "include_numbers": True,
        },
        y_axis_config={
            "include_numbers": True,
        },
    )
    axes_labels = axes.get_axis_labels(
        MathTex("x", font_size=18).next_to(axes.x_axis, DOWN, buff=0.2),
        MathTex(r"\mathrm{erf}(x)", font_size=18).next_to(axes.y_axis, LEFT, buff=0.2),
    )

    # Graficación de la función error
    x_vals = np.linspace(x_range[0], x_range[1], 100)
    points = [axes.c2p(x, erf(x)) for x in x_vals]

    error_graph = VMobject()
    error_graph.set_points_smoothly(points)
    error_graph.set_color_by_gradient(BLUE, GREEN, YELLOW)
    error_graph.set_stroke(
        width=1.8,
        opacity=1,
    )

    scene.play(Create(axes), Write(axes_labels))
    scene.play(Create(error_graph), run_time=3)
    scene.wait(2)

def plot_exponential_integral(scene):
    # Configuración de ejes para la integral exponencial
    x_range = [1, 10, 1]
    y_range = [0, 1, 0.1]

    x_range_0 = [x_range[0] - 1, x_range[1] + 1, 1]
    y_range_0 = [y_range[0] - 0.1, y_range[1] + 0.1, 0.1]
    ancho_permitido = 4
    ancho = 9

    x_length = ((x_range_0[1] - x_range_0[0]) / ancho) * ancho_permitido
    y_length = ((y_range_0[1] - y_range_0[0]) / ancho) * ancho_permitido

    axes = Axes(
        x_range=x_range_0,
        y_range=y_range_0,
        x_length=x_length,
        y_length=y_length,
        axis_config={
            "font_size": 16,
            "color": RED_A,
            "tip_width": 0.1,
            "tip_height": 0.1,
        },
        x_axis_config={
            "include_numbers": True,
        },
        y_axis_config={
            "include_numbers": True,
        },
    )
    axes_labels = axes.get_axis_labels(
        MathTex("z", font_size=18).next_to(axes.x_axis, DOWN, buff=0.2),
        MathTex(r"E_n(z)", font_size=18).next_to(axes.y_axis, LEFT, buff=0.2),
    )

    # Definición de la integral exponencial generalizada
    def exponential_integral(n, z):
        result, _ = quad(lambda t: np.exp(-z * t) / t**n, 1, np.inf)
        return result

    # Valores de n para graficar
    n_values = [0, 1, 2, 3, 5, 10]
    colors = [BLUE, GREEN, YELLOW, ORANGE, RED, PURPLE]

    # Graficación de E_n(z) para cada n
    graphs = VGroup()
    for n, color in zip(n_values, colors):
        x_vals = np.linspace(x_range[0], x_range[1], 100)
        points = [axes.c2p(x, exponential_integral(n, x)) for x in x_vals]

        graph = VMobject()
        graph.set_points_smoothly(points)
        graph.set_color(color)
        graph.set_stroke(
            width=1.8,
            opacity=1,
        )
        graphs.add(graph)

    scene.play(Create(axes), Write(axes_labels))
    scene.play(Create(graphs), run_time=3)
    scene.wait(2)