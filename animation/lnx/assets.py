from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
LOGO_DIR = REPO_ROOT / "assets" / "logo"

LOGO_SVG = str(LOGO_DIR / "logo.svg")
LOGO_DARK = str(LOGO_DIR / "logo_dark.png")
LOGO_LIGHT = str(LOGO_DIR / "logo_light.png")
LOGO_MAIN = str(LOGO_DIR / "logo_main.png")

# logo.svg tiene 3 capas de Inkscape (light/dark/main), cada una con su propio
# rectangulo de fondo de 180x180. Manim (SVGMobject) no respeta el
# style="display:none" de Inkscape y las dibuja todas superpuestas: de ahi el
# cuadrado de fondo visible al renderizar. Este archivo trae solo las letras
# (sin rects), pensado para usarse en escenas, nunca para editar en Inkscape.
LOGO_RENDER = str(LOGO_DIR / "logo_render.svg")
