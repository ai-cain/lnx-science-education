# Lnx
1 608 104 076
Repositorio dedicado a la divulgación matemática mediante códigos predefinidos que generan animaciones de cálculo avanzado, problemas de integrales, límites y otros conceptos matemáticos utilizando LaTeX y Python.

## Descripción

Este proyecto tiene como objetivo facilitar la creación de contenido visual matemático de alta calidad. Los scripts predefinidos combinan el poder de LaTeX y Python (con la biblioteca [Manim](https://www.manim.community/)) para generar animaciones, gráficos y presentaciones ideales para educadores, estudiantes y entusiastas de las matemáticas. Los temas incluyen:

- **Cálculo avanzado**: Límites, derivadas, integrales y series.
- **Visualización matemática**: Representación gráfica de conceptos abstractos.
- **Problemas resueltos**: Animaciones que explican paso a paso problemas matemáticos.

## Requisitos

- **Python 3.8+**
- **Manim**: Biblioteca para animaciones matemáticas.
- **LaTeX**: Para renderizar ecuaciones y texto matemático.
- **Dependencias adicionales**: Ver `requirements.txt` (si existe).

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/asdcainicela/Lnx.git 
   cd Lnx
   ```

2. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

3. Asegúrate de tener LaTeX instalado y configurado en tu sistema.

## Uso

1. Navega al directorio de scripts:
   ```bash
   cd animation/scripts
   ```

2. Ejecuta un script con Manim:
   ```bash
   manim -pql calculus/sum.py
   ```
   - `-pql`: Renderiza en calidad baja con vista previa rápida.
   - Cambia las opciones según tus necesidades (`-pqh` para alta calidad).

3. Explora los scripts predefinidos y utilízalos para tus proyectos de divulgación matemática.

## Estructura del Proyecto

- `animation/scripts`: Contiene los scripts de Python para generar animaciones matemáticas.
- `animation/scripts/calculus`: Contiene scripts relacionados con cálculos matemáticos avanzados, como `sum.py`.
- `README.md`: Documentación del proyecto.
- Otros archivos y directorios relevantes.

## Ubicación de Archivos

- **Scripts principales**: Se encuentran en `animation/scripts`.
- **Ejemplo destacado**: El archivo `calculus/sum.py` genera una animación de una serie matemática.
- **Dependencias**: Si existe, el archivo `requirements.txt` contiene las bibliotecas necesarias.

## Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas o mejoras, abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).

## Contacto

Para preguntas o comentarios, contacta a lnx a traves de tiktok!.




