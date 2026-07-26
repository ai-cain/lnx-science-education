# lnx — libreria compartida

Codigo reutilizable por todas las animaciones. Aqui **no** hay videos; los videos estan en `../videos/`.

Importa siempre desde el paquete, nunca por ruta relativa:

```python
from manim import *
from lnx import *
```

## API

### `scene.py` — utilidades de escena

| Elemento | Uso |
|---|---|
| `backgroundLnx(scene, fondo=BG)` | Fija el fondo oscuro de marca. Primera linea de todo `construct`. |
| `MathPazoKpTemplate()` | Template LaTeX (mathpazo + kpfonts + babel spanish). Asignar a `self.camera.tex_template`. |
| `BoxAnimation(scene, **kwargs)` | Caja redondeada animada con trazador. `.on()` para mostrar, `.off()` para ocultar. |
| `SmartMathTex(tex, target_width, target_height)` | `MathTex` que se autoescala para caber en un area dada. |
| `logo_handler(scene, ...)` | Coloca o mueve el logo a una esquina. |
| `animate_End(scene)` | Cierre de marca con el logo SVG. Ultima linea de todo `construct`. |
| `grillado(scene)` | Grilla de fondo tenue para composicion. |

### `config.py` / `theme.py` — configuracion e identidad visual

`config.py` carga [`lnx.yaml`](../../lnx.yaml) (raiz del repo) y expone `CONFIG`, `FORMATS`, `DEFAULTS`, `THEME`, `TYPOGRAPHY`, `RULES`. Ahi se cambian resolucion, fps, paleta y reglas de calidad — no en el codigo.

`theme.py` reexpone la paleta como constantes de Python: `BG`, `SURFACE`, `ACCENT_CYAN`, `ACCENT_MAGENTA`, `ACCENT_YELLOW`, `ACCENT_PURPLE`, `GRADIENT_MAIN`, `GRADIENT_HIGHLIGHT`, `MIN_FONT_SIZE`.

`set_format("vertical")` / `vertical()` aplican una resolucion de `lnx.yaml`. El CLI ya lo hace via `-r`; solo hace falta si ejecutas `manim` a mano.

Nunca escribas un hex dentro de un `scene.py`: si falta un color, se añade a `lnx.yaml`. Reglas completas en el skill `lnx-design`.

### `assets.py` — rutas

`LOGO_SVG`, `LOGO_DARK`, `LOGO_LIGHT`, `LOGO_MAIN` apuntan a `assets/logo/` en absoluto, asi que funcionan sea cual sea el directorio desde el que renderices.

### `voice.py` — narracion y subtitulos

`LnxVoiceScene` es una escena con voz en off y subtitulos quemados, construida sobre
[manim-voiceover](https://github.com/ManimCommunity/manim-voiceover). El motor de TTS
se elige en `lnx.yaml` (`voice.engine`: gtts, openai, elevenlabs, azure o recorder)
sin tocar el codigo de la escena.

```python
class MiVideo(LnxVoiceScene):
    def construct(self):
        self.preparar()                      # fondo + tipografia + motor de voz
        with self.decir("Una frase corta."):
            self.play(Write(formula))
        animate_End(scene=self)
```

`subtitulo(texto)` construye el caption suelto si lo necesitas aparte. Detalle completo
en el skill `lnx-narracion`.

### `meta.py` / `cli.py` — descubrimiento de videos

`discover()` recorre `../videos/**/scene.py` y extrae las clases que heredan de algun `*Scene` de Manim, sin ningun archivo de metadatos que mantener. Es lo que alimenta `lnx list` y `lnx render`.
