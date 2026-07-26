---
name: lnx-narracion
description: Añade narracion por voz y subtitulos quemados a una animacion Manim del proyecto Lnx, sincronizados palabra a palabra con las animaciones y colocados en la zona segura vertical de TikTok. Usar cuando se pida voz en off, locucion, narracion, subtitulos, captions, o convertir un video mudo existente en uno narrado.
---

# Narracion y subtitulos Lnx

Los subtitulos quemados son lo que mas sube la retencion: mucha gente ve sin sonido.
**Siempre van, con voz o sin ella.**

Para color, tipografia y zona segura, carga tambien `lnx-design`.
Para la estructura narrativa del video, `lnx-video`.

## Como funciona

`animation/lnx/voice.py` envuelve [manim-voiceover](https://github.com/ManimCommunity/manim-voiceover).
El motor de voz se elige en `lnx.yaml` (`voice.engine`) — el codigo de la escena
no cambia al cambiar de motor.

| Motor | Coste | Requiere |
|---|---|---|
| `gtts` | gratis | nada (por defecto) |
| `openai` | de pago | `OPENAI_API_KEY` |
| `elevenlabs` | freemium | `ELEVEN_API_KEY` |
| `azure` | capa gratuita | credenciales de Azure |
| `recorder` | gratis | microfono; graba por bloques |

Whisper (`voice.transcribe: true`) alinea el audio palabra a palabra, que es lo que
permite disparar animaciones en la palabra exacta.

## Escribir una escena narrada

Hereda de `LnxVoiceScene` en vez de `Scene`, y usa `self.preparar()` en lugar de
montar el fondo y el tex_template a mano:

```python
from manim import *
from lnx import *

class MiVideo(LnxVoiceScene):
    def construct(self):
        self.preparar()          # fondo + tipografia + motor de voz

        formula = MathTex(r"\sum_{n=1}^{\infty}\frac{1}{2^n}=1", font_size=90)

        with self.decir("Sumar infinitos numeros y que el resultado sea uno."):
            self.play(Write(formula))

        with self.decir("Esto es una serie geometrica."):
            self.play(Indicate(formula, color=ACCENT_YELLOW))

        animate_End(scene=self)
```

Reglas:
- **La animacion del bloque dura lo que dura la frase.** No pongas `self.wait()`
  dentro de un `with`: si la animacion acaba antes, manim-voiceover espera solo.
- Si la locucion y el subtitulo deben decir cosas distintas:
  `self.decir("texto narrado", "TEXTO EN PANTALLA")`.
- Una idea por bloque. Frases de 6 a 14 palabras; las largas se parten en 3 lineas
  y comen pantalla.

### Sincronizar con una palabra concreta

Marca la palabra con `<bookmark mark='...'/>` y espera hasta ella:

```python
with self.decir("Con solo <bookmark mark='clave'/>veintitres personas ya hay mas del cincuenta por ciento."):
    self.play(FadeIn(gente))
    self.wait_until_bookmark("clave")
    self.play(Indicate(numero_23, color=ACCENT_YELLOW))
```

Requiere `voice.transcribe: true` en `lnx.yaml`.

## Subtitulos

Se generan solos a partir del texto narrado. Todo se controla en `lnx.yaml`
(`subtitles`): `font_size`, `y`, `max_chars_por_linea`, `color`, `stroke_width`.

Cosas que ya estan resueltas y **no** hay que reimplementar en la escena:
- Reparto en varias lineas sin cortar palabras, centradas.
- Contorno oscuro **detras** del relleno (`background=True`). Si se pone delante,
  el contorno se come las letras y el texto desaparece.
- Colocacion en `y = -5.0`, por encima de la UI de TikTok.

Para desactivarlos en un video concreto: `subtitles.enabled: false` en `lnx.yaml`.

## Guion: escribir para el oido

- **Nada de leer formulas en LaTeX.** "uno partido por dos elevado a ene", no
  "\frac{1}{2^n}". El ojo lee la formula; la voz explica que significa.
- Frases cortas y afirmativas. El TTS puntua mal las subordinadas largas.
- Numeros en cifra en pantalla, en palabra en la narracion.
- El hook (0-2s) tambien se narra: es la primera frase, la que decide si se quedan.

## Renderizar

Igual que cualquier otro video:

```bash
.venv/Scripts/lnx.exe <slug>
```

El audio se cachea en `media/voiceovers/`, asi que re-renderizar no vuelve a llamar
al TTS salvo que cambie el texto.

**SoX** (opcional) permite ajustar la velocidad del audio para encajarlo en una
duracion dada. Sin el todo funciona, solo se pierde ese ajuste:
`winget install ChrisBagwell.SoX`.

## Checklist

- [ ] Cada `with self.decir(...)` contiene animacion, no esperas muertas.
- [ ] Ninguna frase supera las ~14 palabras.
- [ ] La narracion no lee LaTeX literal.
- [ ] Los subtitulos no tapan contenido importante (revisa un fotograma real).
- [ ] El video empieza narrando el hook.
- [ ] Renderizado sin errores y el mp4 tiene pista de audio
      (`ffprobe` debe mostrar `codec_type=audio`).
