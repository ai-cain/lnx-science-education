---
name: lnx-video
description: Genera un video educativo de matematicas o fisica del proyecto Lnx, de principio a fin - elige arquetipo narrativo, escribe el guion en beats, produce la escena Manim en animation/videos/<tema>/<slug>/scene.py y la renderiza en vertical 9:16 para TikTok. Usar siempre que se pida crear, guionizar o renderizar una animacion nueva, tanto de nivel basico/viral como avanzado/posgrado.
---

# Generador de videos Lnx

Pipeline de 7 etapas. **No saltes etapas ni escribas Python antes de la etapa 4.**
Para el color, tipografia y zona segura, carga tambien el skill `lnx-design`.

## Etapa 0 — Pre-flight

```bash
.venv/Scripts/lnx.exe list
```

Lista los videos existentes y mira sus carpetas: anota que temas y que tipo de tratamiento ya estan cubiertos, para no repetirte.

## Etapa 1 — Gate de entrada

Necesitas 3 datos. Si el usuario los dio, no preguntes; si faltan, usa estos defaults y avisa:

| Dato | Default |
|---|---|
| `topic` | el hueco menos cubierto del catalogo |
| `level` | `basico` |
| `format` | `vertical` |

`level` admite: `basico` (viral, cero prerrequisitos), `intermedio` (universitario), `avanzado` (posgrado).

## Etapa 2 — Elegir arquetipo ANTES que el tema

Dos videos con temas distintos pero misma macroestructura siguen pareciendo plantilla. El arquetipo manda.

| Arquetipo | Que hace | Nivel tipico |
|---|---|---|
| `paradoja` | Resultado que contradice la intuicion | basico |
| `tu-profe-te-mintio` | Desmonta una regla mal enseñada | basico |
| `demostracion-sin-palabras` | Prueba puramente visual, cero texto explicativo | basico |
| `hook-visual` | Abre con una animacion imposible, explica despues | basico |
| `comparacion-escalas` | Magnitudes que el cerebro no dimensiona | basico |
| `limite-geometrico` | Un proceso infinito que converge visualmente | intermedio |
| `derivacion-visual` | De donde sale realmente la formula | intermedio |
| `problema-resuelto` | Un problema concreto, paso a paso | intermedio |
| `contraejemplo` | Rompe una conjetura razonable | avanzado |
| `extension-inesperada` | Un concepto se generaliza mas alla de su dominio | avanzado |
| `dos-caminos-mismo-resultado` | Dos demostraciones independientes convergen | avanzado |
| `invariante-oculto` | Algo se conserva donde nadie lo esperaba | avanzado |

**Regla anti-repeticion:** el arquetipo elegido no puede coincidir con ninguno de los **3 videos mas recientes** del catalogo, y el `topic` no puede repetir el del video anterior.

## Etapa 3 — Guion en beats (PREVIEW, requiere aprobacion)

Presenta esto al usuario **antes de escribir una sola linea de Python**:

```
Arquetipo:  <archetype>
Tema:       <topic> / <level>
Hook:       "<la frase o imagen de los primeros 2 segundos>"
Duracion:   <total>s

BEATS
0.0-2.0   hook      <que se ve en pantalla>          -> <clase/animacion Manim>
2.0-8.0   setup     ...                              -> ...
...
```

Reglas duras del guion:
- El **hook ocupa 0.0-2.0s**. Si el gancho aparece despues del segundo 2, el video esta mal.
- **Ningun beat dura mas de 6s sin un cambio visual sustancial.**
- **Un solo concepto por video.** Si necesitas dos, son dos videos.
- Duracion objetivo: 30-45s para `basico`, 60-90s para `intermedio`/`avanzado`.
- Cierre con payoff (el resultado enmarcado) y luego `animate_End(scene=self)`.

## Etapa 4 — Cargar solo las recetas que necesitas

No leas toda la libreria. Segun los beats, abre unicamente lo que aplique:

- Transformar ecuaciones -> `TransformMatchingTex`; ver `animation/videos/calculus/serie-geometrica-mitades/scene.py`
- Graficar funciones / area -> `Axes` + `plot` + `get_area`; ver `calculus/area-bajo-la-curva/scene.py`
- Escenas 3D -> `ThreeDScene`; ver `geometry/solidos-3d/scene.py`
- Camara movil / zoom -> `MovingCameraScene`; ver `geometry/espiral-fibonacci/scene.py`
- Estructura minima de escena -> `animation/videos/_template/ejemplo/scene.py`

La API compartida esta en `animation/lnx/`: `backgroundLnx`, `MathPazoKpTemplate`, `BoxAnimation`, `SmartMathTex`, `logo_handler`, `animate_End`, `grillado`, `vertical`, y las constantes `BG`, `ACCENT_*`, `GRADIENT_*`, `LOGO_*`.

## Etapa 5 — Escribir el video

Crea **un unico archivo**: `animation/videos/<topic>/<slug>/scene.py`.

No hay catalogo ni archivos de metadatos que actualizar — `lnx` descubre el video solo.
`<topic>` es una de: `calculo`, `algebra`, `geometria`, `fisica`, `probability`, `problems`.

`scene.py` — esqueleto obligatorio:
```python
from manim import *
from lnx import *

# <archetype> · <topic> · <level>

class NombreDeLaClase(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        # beats aqui

        animate_End(scene=self)
```

Nada de colores ni rutas hardcodeadas: usa las constantes de `lnx`.

### Construcciones geometricas (triangulos, angulos, demostraciones visuales)

Cuando la escena arma una figura a partir de puntos calculados (no solo texto/formulas):

- **Todo segmento auxiliar que aparezca dibujado debe tener su etiqueta.** Si el
  video traza una linea (aunque sea de apoyo, tipo `cos(beta)`) y no la nombra,
  el espectador no sabe que representa y confunde esa linea con otra (p. ej. la
  confunde con la hipotenusa). No dejes segmentos "mudos".
- **Las etiquetas de longitud siempre van hacia afuera de la figura**, nunca
  hacia el interior ni encima de otra linea — igual que el "1" sobre la
  hipotenusa en `trigonometry/seno-suma-angulos`. Calcula un punto de
  referencia (centroide de los vertices) y desplaza cada etiqueta en la
  direccion perpendicular al segmento que se aleja de ese centro:
  ```python
  centro = (A + B + C + ...) / n  # vertices de la figura

  def afuera(P1, P2, dist=0.4):
      mid = (P1 + P2) / 2
      d = P2 - P1
      n = np.array([-d[1], d[0], 0]) / np.linalg.norm(d)
      if np.dot(n, mid - centro) < 0:
          n = -n
      return mid + n * dist
  ```
- **Angulos rectos siempre marcados y visibles**: usa `RightAngle(linea1, linea2, length=0.3-0.35, color=WHITE)`.
  Blanco (no un color de acento) para que no se confunda con las demas lineas
  y se note incluso cuando cruza otras lineas punteadas.
- **Todo texto sobre o cerca de una linea de color necesita fondo solido**
  (`mobj.add_background_rectangle(color=BG, opacity=0.9, buff=0.06)`), o se
  pierde contra el color de la linea (p. ej. texto blanco sobre linea amarilla).

## Etapa 6 — Renderizar

```bash
.venv/Scripts/lnx.exe render <slug>            # borrador rapido
.venv/Scripts/lnx.exe render <slug> -q high    # entrega final
```

El CLI aplica resolucion y fps desde `lnx.yaml` (vertical 1080x1920 por defecto).

## Etapa 7 — Checklist de calidad

Todas deben ser **si** antes de dar el video por terminado:

- [ ] El hook entra antes del segundo 2.
- [ ] Ningun beat pasa de 6s sin cambio visual.
- [ ] Ningun texto por debajo de `font_size=28`; las formulas clave grandes y centradas.
- [ ] Nada importante en el 15% superior ni en el 15% inferior (UI de TikTok).
- [ ] Ningun mobject se sale del encuadre ni se solapa.
- [ ] Fondo `BG`, tipografia `MathPazoKpTemplate`, cierre con `animate_End`.
- [ ] Colores y tiempos tomados de `lnx.yaml`, ninguno inline.
- [ ] El arquetipo no se repite respecto a los 3 videos anteriores.
- [ ] Un solo concepto.
- [ ] `lnx list` muestra el video y `lnx render <slug>` termina sin errores.
