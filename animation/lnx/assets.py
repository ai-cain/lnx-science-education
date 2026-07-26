from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
LOGO_DIR = REPO_ROOT / "assets" / "logo"

LOGO_SVG = str(LOGO_DIR / "logo.svg")
LOGO_DARK = str(LOGO_DIR / "logo_dark.png")
LOGO_LIGHT = str(LOGO_DIR / "logo_light.png")
LOGO_MAIN = str(LOGO_DIR / "logo_main.png")
