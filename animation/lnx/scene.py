from manim import *
from PIL import Image

from .assets import LOGO_SVG
from .config import CONSTANTS
from .theme import BG, SURFACE

BOX = CONSTANTS["box"]
LOGO = CONSTANTS["logo"]
STYLES = CONSTANTS["animation_styles"]
GRID = CONSTANTS["grid"]

class MathPazoKpTemplate(TexTemplate):
    def __init__(self):
        super().__init__()
        self.preamble = r"""
        \usepackage{mathpazo}
        \usepackage[nomath]{kpfonts}
        \usepackage[T1]{fontenc}
        \usepackage[spanish]{babel}
        \usepackage{amsmath} 
        """

def backgroundLnx(scene, fondo=BG):
    scene.camera.background_color = fondo
 
class BoxAnimation:
    def __init__(self, scene, **kwargs):
        self.scene = scene
        self.box = None
        self.fill = None
        self.imagen = None
        self.tracer = None
        self.params = {
            'width': BOX["width"],
            'height': BOX["height"],
            'image_path': None,
            'image_scale': BOX["image_scale"],
            'image_buff': BOX["image_buff"],
            'box_display_time': BOX["display_time"],
            'box_fill_color': SURFACE,
            'box_stroke_color': GOLD,
            'corner_radius': BOX["corner_radius"],
            'stroke_width': BOX["stroke_width"]
        }
        self.params.update(kwargs)
    
    def on(self):
        # Paso 1: Imagen
        if self.params['image_path']:
            self.imagen = ImageMobject(self.params['image_path'])
            self.imagen.scale(self.params['image_scale']).move_to(ORIGIN)
            self.scene.add(self.imagen)
            self.scene.wait(0.1)
        
        # Paso 2-3: Creación del rectángulo y posición de imagen
        self.box = RoundedRectangle(
            width=self.params['width'],
            height=self.params['height'],
            corner_radius=self.params['corner_radius'],
            stroke_width=self.params['stroke_width'],
            fill_opacity=0,
            stroke_color=[YELLOW, ORANGE, "#FF8C00"]
        )
        
        if self.imagen:
            self.imagen.next_to(self.box, DOWN, buff=self.params['image_buff'])
        
        # Paso 4: Animación de creación con tracer
        self.tracer = Dot(color=RED, radius=BOX["tracer_radius"])
        self.scene.add(self.tracer)
        self.tracer.move_to(self.box.get_bottom())
        
        self.scene.play(
            Create(self.box, run_time=BOX["create_run_time"]),
            UpdateFromFunc(self.tracer, lambda m: m.move_to(self.box.get_end())),
            run_time=BOX["create_run_time"]
        )
        self.scene.play(FadeOut(self.tracer))
        
        # Paso 5-6 modificados: Fondo y borde instantáneo
        self.fill = self.box.copy().set_style(
            fill_color=self.params['box_fill_color'],  
            fill_opacity=1,
            stroke_width=0
        )
        self.scene.add(self.fill)
        self.fill.z_index = -1
        
        # Cambio de color de borde inmediato
        self.box.set_stroke(color=self.params['box_stroke_color'])
        self.scene.add(self.box)
    
    def off(self):
        if not self.box:
            raise ValueError("Debes activar primero con on()")
        
        self.scene.play(
            FadeOut(self.box),
            FadeOut(self.fill),
            FadeOut(self.imagen),
            run_time=BOX["fade_run_time"]
        )

def logo_handler(scene, existing_logo=None, image_path=None, corner=DR,
                animation_style="elastic", initial_scale=LOGO["initial_scale"],
                target_scale=LOGO["target_scale"], buff=LOGO["buff"], fade_in=True):
    """
    Función universal para manejo de logos:
    
    1. Si existe existing_logo: Lo mueve a la esquina
    2. Si no existe: Carga image_path y lo anima desde el centro
    
    Parámetros:
    - existing_logo: Objeto de imagen existente (opcional)
    - image_path: Ruta si no hay logo existente (requerido si existing_logo es None)
    - corner: DR (default), DL, UR, UL
    - animation_style: "smooth", "elastic", "rush"
    - initial_scale: Escala inicial (solo para nuevo logo)
    - target_scale: Escala al finalizar animación
    - buff: Espacio desde la esquina
    - fade_in: Animación de entrada para nuevo logo
    """
    
    # Validación básica
    if existing_logo is None and image_path is None:
        raise ValueError("Debe proveer existing_logo o image_path")

    # Configuración de animación
    anim_config = {
        name: {
            "rate_func": getattr(rate_functions, cfg["rate_func"], None) or globals()[cfg["rate_func"]],
            "run_time": cfg["run_time"],
        }
        for name, cfg in STYLES.items()
    }
    
    # Caso 1: Logo existente
    if existing_logo is not None:
        logo = existing_logo
        scene.play(
            logo.animate.to_corner(corner, buff=buff).scale(target_scale),
            **anim_config[animation_style]
        )
    
    # Caso 2: Nuevo logo
    else:
        logo = ImageMobject(image_path).scale(initial_scale).move_to(ORIGIN)
        
        if fade_in:
            scene.play(FadeIn(logo, shift=UP*0.3), run_time=LOGO["fade_in_run_time"])
        
        scene.play(
            logo.animate.to_corner(corner, buff=buff).scale(target_scale),
            **anim_config[animation_style]
        )
    
    return logo

## finalizar el logo aquí va
def animate_End(scene, svg_path=LOGO_SVG, width_ratio=LOGO["end_width_ratio"], colors=[YELLOW, ORANGE]):
    """
    Cierre de marca: dibuja el contorno del logo y lo rellena.

    El logo se dimensiona como una fraccion del ancho del frame, asi que ocupa
    lo mismo en vertical que en horizontal.

    Args:
        scene (Scene): Escena donde se añade la animacion.
        svg_path (str): Ruta del SVG. Por defecto el logo de la marca.
        width_ratio (float): Ancho del logo como fraccion del ancho del frame.
        colors (list): Gradiente del contorno.
    """
    logo = SVGMobject(svg_path)
    logo.width = config.frame_width * width_ratio

    scene.clear()
    # Animación del contorno
    outline_path = VMobject()
    for submobject in logo:
        outline_path.append_points(submobject.get_points())
    outline_path.set_stroke(color=colors, width=LOGO["end_stroke_width"])

    scene.play(Create(outline_path), run_time=LOGO["end_run_time"])
    scene.play(
        FadeOut(outline_path, run_time=LOGO["end_run_time"]),
        FadeIn(logo, run_time=LOGO["end_run_time"]),
        lag_ratio=0
        )
    scene.wait(LOGO["end_wait"])





class SmartMathTex(MathTex):
    def __init__(self, tex, target_width, target_height, **kwargs):
        super().__init__(tex, **kwargs)
        self.initial_font_size = self.font_size
        self.target_width = target_width
        self.target_height = target_height
        self.auto_scale()

    def auto_scale(self):
        width_ratio = self.target_width / self.width
        height_ratio = self.target_height / self.height
        scale_factor = min(width_ratio, height_ratio, 1.0)
        self.scale(scale_factor * 0.95)
        self.font_size = self.initial_font_size * scale_factor

def grillado(scene):
    # Crear la grilla
    grid = NumberPlane(
        x_range=GRID["x_range"],
        y_range=GRID["y_range"],
        background_line_style={
            "stroke_color": YELLOW,
            "stroke_width": GRID["stroke_width"],
            "stroke_opacity": GRID["stroke_opacity"],
        },
        axis_config={"stroke_opacity": 0},  # Ocultar los ejes
    )
    scene.add(grid)  # Agregar la grilla a la escena