from manim import config as manim_config

from .config import FORMATS, THEME, TYPOGRAPHY

BG = THEME["background"]
SURFACE = THEME["surface"]

ACCENT_CYAN = THEME["accent_cyan"]
ACCENT_MAGENTA = THEME["accent_magenta"]
ACCENT_YELLOW = THEME["accent_yellow"]
ACCENT_PURPLE = THEME["accent_purple"]

GRADIENT_MAIN = THEME["gradient_main"]
GRADIENT_HIGHLIGHT = THEME["gradient_highlight"]

MIN_FONT_SIZE = TYPOGRAPHY["min_font_size"]


def set_format(name="vertical"):
    """Aplica una resolucion de lnx.yaml. Solo necesario al llamar a manim a mano."""
    fmt = FORMATS[name]
    manim_config.pixel_width, manim_config.pixel_height = fmt["resolution"]
    manim_config.frame_width, manim_config.frame_height = fmt["frame"]


def vertical():
    set_format("vertical")
