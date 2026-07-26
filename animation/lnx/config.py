from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_FILE = REPO_ROOT / "lnx.yaml"

CONFIG = yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8"))

FORMATS = CONFIG["formats"]
DEFAULTS = CONFIG["defaults"]
THEME = CONFIG["theme"]
TYPOGRAPHY = CONFIG["typography"]
RULES = CONFIG["rules"]
CONSTANTS = CONFIG["constants"]
