"""Narracion y subtitulos para las escenas Lnx.

Envuelve manim-voiceover para que el motor de voz se elija desde lnx.yaml y los
subtitulos respeten la zona segura vertical de TikTok.

Uso en una escena:

    from manim import *
    from lnx import *

    class MiVideo(LnxVoiceScene):
        def construct(self):
            self.preparar()
            with self.decir("Con solo 23 personas ya hay mas de 50%"):
                self.play(Write(formula))
            animate_End(scene=self)
"""

from manim import *
from manim_voiceover import VoiceoverScene

from .config import CONFIG
from .scene import MathPazoKpTemplate, backgroundLnx
from .theme import BG

VOICE = CONFIG["voice"]
SUBS = CONFIG["subtitles"]


def _servicio():
    """Instancia el motor de TTS declarado en lnx.yaml."""
    engine = VOICE["engine"]

    if engine == "gtts":
        from manim_voiceover.services.gtts import GTTSService
        return GTTSService(lang=VOICE["lang"], tld=VOICE["tld"],
                           transcription_model=_modelo_whisper())

    if engine == "openai":
        from manim_voiceover.services.openai import OpenAIService
        cfg = VOICE["openai"]
        return OpenAIService(voice=cfg["voice"], model=cfg["model"],
                             transcription_model=_modelo_whisper())

    if engine == "elevenlabs":
        from manim_voiceover.services.elevenlabs import ElevenLabsService
        cfg = VOICE["elevenlabs"]
        return ElevenLabsService(voice_name=cfg["voice"], model=cfg["model"],
                                 transcription_model=_modelo_whisper())

    if engine == "azure":
        from manim_voiceover.services.azure import AzureService
        cfg = VOICE["azure"]
        return AzureService(voice=cfg["voice"], style=cfg["style"],
                            transcription_model=_modelo_whisper())

    if engine == "recorder":
        from manim_voiceover.services.recorder import RecorderService
        return RecorderService(transcription_model=_modelo_whisper())

    raise ValueError(
        f"Motor de voz '{engine}' no reconocido. "
        "Valores validos en lnx.yaml: gtts, openai, elevenlabs, azure, recorder."
    )


def _modelo_whisper():
    return VOICE["model"] if VOICE["transcribe"] else None


def _partir(texto, max_chars):
    """Reparte el texto en lineas sin cortar palabras."""
    lineas, actual = [], ""
    for palabra in texto.split():
        candidata = f"{actual} {palabra}".strip()
        if len(candidata) > max_chars and actual:
            lineas.append(actual)
            actual = palabra
        else:
            actual = candidata
    if actual:
        lineas.append(actual)
    return lineas


def subtitulo(texto):
    """Caption de marca, en la zona segura inferior.

    El texto se reparte en varias lineas en vez de encogerse, para que siga
    siendo legible en movil por larga que sea la frase.
    """
    lineas = _partir(texto, SUBS["max_chars_por_linea"])
    t = Paragraph(
        *lineas,
        alignment="center",
        font_size=SUBS["font_size"],
        color=SUBS["color"],
        line_spacing=SUBS["line_spacing"],
    )
    # background=True dibuja el contorno DETRAS del relleno; sin eso, el
    # contorno oscuro se pinta encima y se come las letras.
    t.set_stroke(color=BG, width=SUBS["stroke_width"], opacity=1, background=True)

    # Red de seguridad: si aun asi no cabe, se encoge lo justo.
    ancho_max = config.frame_width * SUBS["max_width_ratio"]
    if t.width > ancho_max:
        t.scale(ancho_max / t.width)

    t.move_to([0, SUBS["y"], 0])
    return t


class LnxVoiceScene(VoiceoverScene):
    """Escena Lnx con narracion y subtitulos automaticos."""

    def preparar(self):
        """Fondo, tipografia y motor de voz. Primera linea de construct()."""
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()
        self.set_speech_service(_servicio())

    def decir(self, texto, subtitulo_texto=None):
        """Narra `texto` mientras corren las animaciones del bloque `with`.

        Muestra el subtitulo si `subtitles.enabled` esta activo en lnx.yaml.
        Pasa `subtitulo_texto` para mostrar algo distinto de lo que se narra.
        """
        if not SUBS["enabled"]:
            return self.voiceover(text=texto)

        caption = subtitulo(subtitulo_texto or texto)
        self.add(caption)
        return _ConSubtitulo(self, texto, caption)


class _ConSubtitulo:
    """Context manager que quita el subtitulo al cerrar el bloque."""

    def __init__(self, scene, texto, caption):
        self.scene = scene
        self.caption = caption
        self._bloque = scene.voiceover(text=texto)

    def __enter__(self):
        return self._bloque.__enter__()

    def __exit__(self, *excepcion):
        resultado = self._bloque.__exit__(*excepcion)
        self.scene.remove(self.caption)
        return resultado
