import ast
from dataclasses import dataclass
from pathlib import Path

from .config import DEFAULTS

VIDEOS_DIR = Path(__file__).resolve().parents[1] / "videos"


@dataclass
class VideoMeta:
    slug: str
    script: Path
    scene: str
    format: str = DEFAULTS["format"]
    fps: int = DEFAULTS["fps"]

    @property
    def dir(self) -> Path:
        return self.script.parent


def scenes_in(script: Path) -> list[str]:
    """Clases que heredan de algun *Scene de Manim, en orden de aparicion."""
    tree = ast.parse(script.read_text(encoding="utf-8"))
    return [
        node.name
        for node in tree.body
        if isinstance(node, ast.ClassDef)
        and any(
            isinstance(b, ast.Name) and b.id.endswith("Scene") for b in node.bases
        )
    ]


def discover() -> list[VideoMeta]:
    videos = []
    for script in sorted(VIDEOS_DIR.rglob("scene.py")):
        slug = script.parent.relative_to(VIDEOS_DIR).as_posix()
        for scene in scenes_in(script):
            videos.append(VideoMeta(slug=slug, script=script, scene=scene))
    return videos
