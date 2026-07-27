import logging
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from tqdm import tqdm

from .config import DEFAULTS, FORMATS
from .meta import discover

log = logging.getLogger("lnx")

QUALITY_FLAG = {"low": "-ql", "medium": "-qm", "high": "-qh", "prod": "-qk"}


def _setup_logging():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(levelname)-7s %(message)s"))
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    log.propagate = False  # manim engancha su propio handler al logger raiz


def _config_file(fmt):
    """Manim no recalcula frame_width al pasar -r, hay que fijarlo por config."""
    width, height = FORMATS[fmt]["frame"]
    path = Path(tempfile.gettempdir()) / f"lnx-{fmt}.cfg"
    path.write_text(f"[CLI]\nframe_width = {width}\nframe_height = {height}\n")
    return path


def mostrar(videos):
    log.info("%d escenas encontradas:", len(videos))
    for i, v in enumerate(videos, 1):
        print(f"  {i:>2}. {v.slug:<42} {v.scene}")


def _normalizar(texto):
    """Minusculas y sin separadores: 'Angle-Sum', 'ANGLESUM' y 'angle_sum'
    deben ser lo mismo para quien busca."""
    return re.sub(r"[^a-z0-9]", "", texto.lower())


def coincide(v, patron):
    """Busca tanto en el slug (carpeta) como en el nombre de la clase,
    porque eso es lo que se ve en 'lnx list' y lo que la gente escribe."""
    patron = _normalizar(patron)
    return patron in _normalizar(v.slug) or patron in _normalizar(v.scene)


def elegir(videos):
    """Menu interactivo: devuelve los videos a renderizar."""
    mostrar(videos)
    print()
    respuesta = input("Numero(s) a renderizar, texto a buscar, o Enter para todos: ").strip()

    if not respuesta:
        log.info("Seleccionados los %d videos.", len(videos))
        return videos

    if all(p.isdigit() for p in respuesta.replace(",", " ").split()):
        indices = [int(p) for p in respuesta.replace(",", " ").split()]
        elegidos = [videos[i - 1] for i in indices if 1 <= i <= len(videos)]
    else:
        elegidos = [v for v in videos if coincide(v, respuesta)]

    if not elegidos:
        log.error("Nada coincide con '%s'.", respuesta)
    else:
        log.info("Seleccionados: %s", ", ".join(v.scene for v in elegidos))
    return elegidos


def elegir_calidad():
    opciones = list(QUALITY_FLAG)
    print()
    for i, q in enumerate(opciones, 1):
        marca = "  (por defecto)" if q == DEFAULTS["quality"] else ""
        print(f"  {i}. {q}{marca}")
    respuesta = input("Calidad [Enter = por defecto]: ").strip()

    if not respuesta:
        return DEFAULTS["quality"]
    if respuesta.isdigit() and 1 <= int(respuesta) <= len(opciones):
        return opciones[int(respuesta) - 1]
    if respuesta in QUALITY_FLAG:
        return respuesta

    log.warning("Calidad '%s' desconocida, uso '%s'.", respuesta, DEFAULTS["quality"])
    return DEFAULTS["quality"]


def renderizar(videos, calidad):
    fallidos = []
    barra = tqdm(videos, desc="Renderizando", unit="video")
    for v in barra:
        barra.set_postfix_str(v.slug)
        ancho, alto = FORMATS[v.format]["resolution"]
        cmd = [sys.executable, "-m", "manim", QUALITY_FLAG[calidad], "--disable_caching",
               "-r", f"{ancho},{alto}", "--fps", str(v.fps),
               "--config_file", str(_config_file(v.format)),
               "--media_dir", str(v.dir / "media"), str(v.script), v.scene]
        proceso = subprocess.run(cmd, capture_output=True, text=True)
        if proceso.returncode == 0:
            log.debug("OK %s", v.slug)
        else:
            fallidos.append((v, proceso.stderr.strip().splitlines()[-6:]))
    barra.close()

    for v, error in fallidos:
        log.error("Fallo %s (%s):\n%s", v.slug, v.scene, "\n".join(error))

    ok = len(videos) - len(fallidos)
    if fallidos:
        log.warning("%d de %d renderizados.", ok, len(videos))
    else:
        log.info("%d de %d renderizados.", ok, len(videos))
        for v in videos:
            log.info("  %s", v.dir / "media")
    return 1 if fallidos else 0


def main():
    _setup_logging()
    argumentos = sys.argv[1:]

    videos = discover()
    if not videos:
        log.error("No hay ningun scene.py en animation/videos/.")
        return 1

    if argumentos and argumentos[0] in ("-h", "--help", "help"):
        print("Uso:")
        print("  lnx                    menu interactivo")
        print("  lnx list               listar las escenas")
        print("  lnx <texto>            renderizar las escenas que coincidan (calidad baja)")
        print("  lnx <texto> <calidad>  calidad: " + ", ".join(QUALITY_FLAG))
        return 0

    if argumentos and argumentos[0] == "list":
        mostrar(videos)
        return 0

    if argumentos:
        patron = argumentos[0]
        elegidos = [v for v in videos if coincide(v, patron)]
        if not elegidos:
            log.error("Nada coincide con '%s'. Prueba 'lnx list'.", patron)
            return 1
        log.info("Seleccionados: %s", ", ".join(v.scene for v in elegidos))

        if len(argumentos) > 1:
            calidad = argumentos[1].lower()
            if calidad not in QUALITY_FLAG:
                log.warning("Calidad '%s' desconocida, uso '%s'.", calidad, DEFAULTS["quality"])
                calidad = DEFAULTS["quality"]
        else:
            calidad = DEFAULTS["quality"]
    else:
        elegidos = elegir(videos)
        if not elegidos:
            return 1
        calidad = elegir_calidad()

    log.info("Calidad: %s", calidad)
    return renderizar(elegidos, calidad)


if __name__ == "__main__":
    sys.exit(main())
