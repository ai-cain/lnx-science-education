---
name: lnx-design
description: Aplica la identidad visual Lnx (paleta, gradientes, tipografía MathPazo/kpfonts, formato vertical 9:16 para TikTok y estructura de escena) al crear o editar cualquier animación Manim de animation/scripts/ o cualquier documento LaTeX que use template/Lnx*.sty.
---

# Identidad visual Lnx

Reglas obligatorias para animaciones Manim y documentos LaTeX del proyecto.
Todo valor marcado **(propuesto)** no está definido en el repo: úsalo, pero avísale al usuario para que lo confirme.

## 1. Paleta oficial

Extraída de `animation/scripts/calculus/*.py` y `template/Lnx.sty`.

| Rol | Hex | Uso |
|---|---|---|
| Fondo base | `#111111` | Único fondo de escena. Siempre vía `backgroundLnx(self)`. (`LnxblackF` en LaTeX) |
| Superficie / caja | `#1f1f1f` | Relleno de `BoxAnimation`, paneles, cajas de destaque. (`LnxblackC` `#1e1e1e` en LaTeX) |
| Acento primario (cian) | `#00F5FF` | Objeto protagonista, curvas y figuras principales. |
| Acento secundario (magenta) | `#FF00F5` | Segundo término de un gradiente, contraste con el cian. |
| Resaltado (amarillo) | `#FFEE00` / `YELLOW` | Resultado clave, término que se está manipulando, títulos. |
| Resaltado cálido (naranja) | `ORANGE` / `#FF8C00` | Par del amarillo en gradientes; bordes de caja. |
| Acento morado | `#9D00FF` | Tercer color en gradientes; casos especiales / condiciones. |
| Marca / oro | `GOLD`, `#FFD700` | Borde final de `BoxAnimation`, títulos de marca. |
| Alerta / error | `RED`, `#ff1744` | Puntos de intersección, marcas de "esto está mal", el `tracer`. |
| Correcto | `GREEN` | Resultado validado. |
| Texto | `WHITE` (`#FFFFFF`) | Texto neutro y símbolos estructurales (`=`, `[`, `]`). |
| Texto secundario | `#E0E0E0` | Notas y subtítulos (usar poco). |

Contraste sobre `#111111` (WCAG, texto normal necesita ≥4.5:1):

- `#00F5FF` ≈ 15.5:1, `#FFEE00` ≈ 16.7:1, `#FFD700` ≈ 14.0:1, `WHITE` ≈ 18.9:1, `GREEN` ≈ 11:1 → todos válidos.
- `#FF00F5` ≈ 5.4:1 y `#9D00FF` ≈ 2.0:1 → **el magenta solo en trazos gruesos (`stroke_width>=4`), el morado NUNCA como color sólido de texto**; solo como extremo de un gradiente o relleno de área.
- `RED` puro ≈ 4.0:1 → para texto usa `#ff1744` o `RED_A`/`RED_B`, no `RED`.
- Prohibido: texto en `#1f1f1f`–`#333333` sobre el fondo, y cualquier fondo claro (rompe el look nocturno de la marca).

## 2. Gradientes

Pares/tríos ya en uso — usa estos, no inventes otros:

- `["#00F5FF", "#FF00F5"]` — figura geométrica protagonista (cuadrado, líneas de subdivisión).
- `["#FFEE00", "#9D00FF"]` — fórmula/resultado final destacado.
- `[YELLOW, ORANGE]` — logo final (`animate_End`), contornos de marca. **Es el gradiente firma; no lo cambies.**
- `[YELLOW, "#FF8C00", ORANGE]` — bordes de cajas y figuras cálidas.
- `["#FFD700", "#FFA500"]` — títulos con `set_color_by_gradient`.
- `[BLUE, YELLOW, PURPLE]` — rellenos de área bajo curva (`fill_opacity` 0.3–0.5).

Cuándo **NO** usar gradiente:

- Texto explicativo largo, etiquetas pequeñas (`font_size < 24`) y símbolos estructurales → `WHITE` plano.
- Ejes, grillas y elementos de soporte → color plano con opacidad baja (ver `grillado()`: `YELLOW`, `stroke_opacity=0.1`).
- Cuando ya hay otro gradiente en pantalla: máximo **un** elemento con gradiente por momento visual.
- Para codificar significado (correcto/incorrecto, f(x) vs g(x)) → colores planos distinguibles.

## 3. Tipografía

- **Siempre** `self.camera.tex_template = MathPazoKpTemplate()` (de `LnxScene.py`) al inicio de `construct`. Nunca la fuente por defecto de Manim.
- Preamble: `mathpazo` + `kpfonts[nomath]` + `fontenc T1` + `babel spanish` + `amsmath`.
- Matemática → `MathTex`; texto en español → `Tex` (para acentos correctos vía babel). `Text` solo si necesitas una fuente no-LaTeX; si lo usas, mantén el mismo tamaño relativo.
- Ajuste automático a una caja: usa `SmartMathTex(tex, target_width, target_height)`.
- LaTeX: los documentos cargan `\RequirePackage{mathpazo}` + `kpfonts` desde `LnxPost.sty` / `Lnx.sty`; no redefinas la fuente en el `.tex`.
- Añade `set_stroke(width=1)`–`1.2` a títulos y fórmulas clave para que "engorden" y se lean en móvil (patrón ya usado en `areaInt.py`, `matrix_2x2.py`).

## 4. Estructura estándar de escena

```python
from manim import *
from LnxScene import backgroundLnx, MathPazoKpTemplate, SmartMathTex, BoxAnimation, animate_End

class MiEscena(Scene):
    def construct(self):
        backgroundLnx(self)                                  # 1. fondo #111111
        self.camera.tex_template = MathPazoKpTemplate()      # 2. tipografía
        logo = ImageMobject("logo.png").scale(0.4*0.4).shift(DOWN*3.2)
        self.add(logo)                                       # 3. marca de agua fija
        # 4. hook -> desarrollo -> resultado
        ...
        animate_End(scene=self, svg_path="logo.svg")         # 5. cierre de marca
```

Reglas:

- El logo de agua va abajo (`DOWN*3.2`, escala `0.4*0.4`) o en esquina vía `logo_handler(..., corner=DR)`; nunca tapando la fórmula.
- `animate_End` **siempre** cierra la animación (limpia la escena y anima el logo con `[YELLOW, ORANGE]`).
- Ejecuta desde el directorio del script: `logo.png` y `logo.svg` se referencian como rutas relativas.

## 5. Formato TikTok vertical

- Render vertical: `manim -pqh --resolution 1080,1920 script.py MiEscena` (o `config.pixel_width=1080; config.pixel_height=1920; config.frame_height=16; config.frame_width=9`). **(propuesto: no hay `manim.cfg` en el repo; conviene añadir uno con `pixel_width=1080`, `pixel_height=1920`, `frame_rate=60`.)**
- Zonas seguras: el contenido esencial vive en el 70 % central vertical. Con `frame_height=16` (y ≈ ±8), evita **y > 5.6** (UI superior) y **y < -5.6** (caption, botones, usuario). El logo de agua a `DOWN*3.2` está dentro de la zona segura.
- Márgenes laterales: deja ≥0.5 unidades de cada lado; los botones de la derecha de TikTok comen ~15 % del ancho en la franja inferior-derecha.
- Tamaño mínimo legible en móvil: `font_size >= 28` para texto que el espectador debe leer; `>= 20` solo para etiquetas efímeras junto a un objeto; nunca por debajo de 15 salvo efecto visual deliberado (como la cola de fracciones en `sum.py`).
- Duración: **15–60 s**; el punto dulce es 25–40 s.
- **Hook en los primeros 2 s**: la pregunta o la figura sorprendente aparece de inmediato. Nada de logos, títulos largos o pantallas vacías al inicio.

## 6. Ritmo de animación

- `Write` / `Create` de fórmulas: `run_time=0.2–0.5`.
- `Transform` / `TransformMatchingTex` principal: `run_time=1`.
- Movimientos de apoyo simultáneos: `run_time=0.1–0.5` (más rápidos que la transformación que acompañan).
- Cierre con logo: `Create` 0.5 + fade cruzado 0.5 + `wait(0.5)` (ya lo hace `animate_End`).
- `self.wait()`: 0.5–1 s tras un paso, **máximo 2 s** tras el resultado final. Nunca dejes una pantalla estática >2 s: si necesitas tiempo de lectura, añade movimiento (un `Indicate`, un color que cambia, un zoom leve).
- Agrupa animaciones simultáneas con `self.play(a, b, ...)` en vez de encadenarlas; el vídeo debe sentirse denso.
- Aceleración progresiva: cada iteración repetida de un mismo patrón debe durar menos que la anterior.

## 7. Checklist antes de dar por terminada una animación

1. `backgroundLnx(self)` presente y sin ningún otro fondo.
2. `self.camera.tex_template = MathPazoKpTemplate()` presente.
3. Todos los colores salen de la tabla §1; sin hex inventados.
4. Máximo un gradiente activo por pantalla; gradientes solo de los pares de §2.
5. Ningún texto en morado sólido; contraste verificado sobre `#111111`.
6. Todo el contenido esencial dentro de |y| ≤ 5.6 y sin salirse lateralmente.
7. `font_size >= 28` en todo lo que deba leerse.
8. Hook visible en los primeros 2 s.
9. Duración total 15–60 s; ningún `wait` > 2 s ni pantalla estática larga.
10. Logo de agua visible durante el desarrollo y `animate_End(...)` como última línea.
11. Render de prueba en vertical 1080×1920 revisado en móvil (o al 30 % de tamaño en pantalla).
12. Texto en español con `Tex`/babel: acentos y "ñ" correctos.
