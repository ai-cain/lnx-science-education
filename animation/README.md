# animation/

Todo lo relacionado con **video**. La parte de documentos LaTeX vive en [`docs-tex/`](../docs-tex/) y es independiente.

```
animation/
├── lnx/                    libreria compartida (codigo reutilizable, NO videos)
│   ├── scene.py            utilidades de escena: backgroundLnx, BoxAnimation, animate_End...
│   ├── theme.py            paleta, gradientes y formato vertical 9:16
│   ├── assets.py           rutas a assets/logo/
│   ├── meta.py             descubrimiento automatico de escenas
│   └── cli.py              comando `lnx list` / `lnx render`
└── videos/
    └── <tema>/<slug>/
        └── scene.py        la animacion
```

No hay archivos de metadatos: `lnx` descubre los videos recorriendo las carpetas y leyendo las clases `Scene` de cada `scene.py`. Los valores generales (resolucion, fps, paleta, tiempos, tamaños) viven en [`lnx.yaml`](../lnx.yaml) en la raiz.

La regla: **`lnx/` es libreria, `videos/` es contenido.** Si algo se usa en mas de un video, va a `lnx/`.

## Puesta en marcha

Requiere Python 3.10+ y LaTeX (MiKTeX o TeX Live) en el PATH.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -e .
```

Esto instala la libreria `lnx` en modo editable y el comando `lnx`.

## Uso

```bash
lnx                       # menu interactivo: elige escena y calidad
lnx list                  # solo listar las escenas
lnx espiral-fibonacci     # renderizar lo que coincida con ese texto
lnx calculus              # renderiza todas las escenas de calculus
```

Sin argumentos entra en modo interactivo: numera las escenas y pregunta cual renderizar (por numero, por texto, o Enter para todas) y con que calidad.

La resolucion y los fps salen de `lnx.yaml` segun el `format` del video (vertical por defecto). La salida va a `<carpeta del video>/media/`, que esta en `.gitignore`.

Tambien puedes invocar Manim directamente dentro de la carpeta de un video:

```bash
manim -ql scene.py NombreDeLaClase
```

## Crear un video nuevo

Usa el skill `lnx-video` (`.claude/skills/lnx-video/`), que guia el proceso completo: arquetipo narrativo, guion en beats, escena Manim y render. Para color y tipografia, el skill `lnx-design`.

A mano: copia `videos/_template/ejemplo/`, renombra la carpeta y la clase. Aparece en `lnx list` sin mas.
