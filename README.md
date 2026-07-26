# Lnx
1 608 104 076
Repositorio dedicado a la divulgación matemática mediante códigos predefinidos que generan animaciones de cálculo avanzado, problemas de integrales, límites y otros conceptos matemáticos utilizando LaTeX y Python.

## Descripción

Este proyecto tiene como objetivo facilitar la creación de contenido visual matemático de alta calidad. Combina Python + [Manim](https://www.manim.community/) para las animaciones y LaTeX para los documentos, con una identidad visual común. Ideal para educadores, estudiantes y entusiastas de las matemáticas. Los temas incluyen:

- **Cálculo avanzado**: Límites, derivadas, integrales y series.
- **Visualización matemática**: Representación gráfica de conceptos abstractos.
- **Problemas resueltos**: Animaciones que explican paso a paso problemas matemáticos.

## Requisitos

- **Python 3.10+**
- **LaTeX**: MiKTeX o TeX Live, disponible en el PATH.
- Manim y el resto de dependencias se instalan con el paso siguiente.

## Instalación

```bash
git clone https://github.com/asdcainicela/Lnx.git
cd Lnx
python -m venv .venv
.venv/Scripts/python.exe -m pip install -e .
```

Esto instala la librería `lnx` en modo editable y deja disponible el comando `lnx`.

Los skills externos no se versionan (pesan mucho); se reinstalan desde `skills-lock.json`:

```bash
npx skills install
```

Opcional: [SoX](http://sox.sourceforge.net/) (`winget install ChrisBagwell.SoX`) para que la narración pueda ajustar la velocidad del audio.

## Uso

```bash
lnx                       # menú interactivo: elige escena y calidad
lnx list                  # listar las escenas disponibles
lnx espiral-fibonacci     # renderizar lo que coincida con ese texto
```

Para crear un video nuevo, usa el skill `lnx-video`, que guía el proceso completo (arquetipo narrativo, guion en beats, escena Manim y render).

## Estructura del Proyecto

El repositorio tiene dos líneas de trabajo independientes:

| Ruta | Qué es |
|---|---|
| `animation/lnx/` | Librería compartida: estilo, utilidades de escena, config y CLI |
| `animation/videos/` | Un video por carpeta, con su `scene.py` |
| `docs-tex/` | Ejercicios, exámenes y documentos LaTeX |
| `template/` | Clase y estilos LaTeX propios (`LnxClase.cls`, `Lnx.sty`, ...) |
| `assets/logo/` | Logo en sus variantes, compartido por ambas líneas |
| `lnx.yaml` | Configuración global: resolución, fps, paleta y reglas de calidad |
| `.agents/skills/` | Skills: `lnx-design` (identidad visual), `lnx-video` (pipeline), `lnx-narracion` (voz y subtítulos) |

Detalle de la parte de video en [`animation/README.md`](animation/README.md).

## Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas o mejoras, abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).

## Contacto

Para preguntas o comentarios, contacta a lnx a traves de tiktok!.




