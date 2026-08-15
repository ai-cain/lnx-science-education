from manim import *
from lnx import *

# euler-characteristic | geometry / topology | intermedio
# Formula de Euler para poliedros:  V - A + C = 2.
#
# La idea que se quiere transmitir no es la formula, sino por que la formula
# es sorprendente: cuatro solidos con numeros completamente distintos
#
#     cubo         8 - 12 +  6 = 2
#     tetraedro    4 -  6 +  4 = 2
#     octaedro     6 - 12 +  8 = 2
#     dodecaedro  20 - 30 + 12 = 2
#
# aterrizan en el mismo 2. Ese 2 no depende de la forma: depende de COMO estan
# conectadas las piezas. Por eso se puede deformar el cubo hasta dejarlo
# irreconocible (mover los vertices a donde uno quiera) y la cuenta no se
# mueve: es un invariante topologico, no una medida geometrica.
#
# El cierre rompe la regla a proposito: un toro triangulado da
#     32 - 96 + 64 = 0,
# y ahi aparece la formula general  chi = 2 - 2g  (g = numero de agujeros).
# La esfera tiene g = 0 -> chi = 2. El toro tiene g = 1 -> chi = 0.
#
# TODOS los conteos de este archivo se calculan en tiempo de ejecucion a partir
# de la lista de caras (ver `solid_counts`), nunca se escriben a mano: los
# numeros que salen en pantalla son literalmente los del mobject que se ve.
#
# El frame real es 9 x 16 unidades (x en [-4.5, 4.5], y en [-8, 8]).
# Zona segura: |y| <= 5.6 y |x| <= 3.8.
# En 3D los rotulos van SIEMPRE con add_fixed_in_frame_mobjects, porque la
# camara rota durante casi todo el video.

# ------------------------------------------------------------------ layout 9:16
TITLE_Y = 5.15          # cabecera, dentro de la zona segura
SUBTITLE_Y = 4.25       # frase corta bajo el titulo
COUNTER_Y = -3.55       # fila de contadores V / A / C
EQUATION_Y = -4.80      # la cuenta resuelta
SAFE_WIDTH = 7.2        # 2 * 3.8 menos un margen de respeto

TARGET_RADIUS = 2.55    # radio circunscrito de los solidos, en unidades de mundo

# ------------------------------------------------------------------ paleta Lnx
V_COLOR = ACCENT_YELLOW     # vertices
E_COLOR = ACCENT_CYAN       # aristas
F_COLOR = ACCENT_MAGENTA    # caras
CHI_COLOR = ACCENT_PURPLE   # el invariante

VERTEX_RADIUS = 0.085
EDGE_WIDTH = 3.5


def fit_to_safe_width(mobject):
    """Ningun rotulo puede desbordar el ancho seguro del frame vertical."""
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def unique_edges(faces_list):
    """Aristas sin repetir a partir de la lista de caras.

    Polyhedron.get_edges() devuelve un par por cada lado de cada cara, asi que
    cada arista aparece dos veces (una por cada cara que la comparte). Para
    CONTAR hay que quedarse con las aristas distintas.
    """
    edges = []
    seen = set()
    for face in faces_list:
        for a, b in zip(face, face[1:] + face[:1]):
            key = frozenset((a, b))
            if key not in seen:
                seen.add(key)
                edges.append((a, b))
    return edges


def solid_counts(vertex_coords, faces_list):
    """(V, A, C) leidos de la propia definicion del solido."""
    return len(vertex_coords), len(unique_edges(faces_list)), len(faces_list)


# ------------------------------------------------------- definiciones de solidos
def cube_data(radius=TARGET_RADIUS):
    """Cubo como poliedro explicito: 8 vertices, 12 aristas, 6 caras.

    Manim trae `Cube`, pero es un VGroup de 6 cuadrados sin grafo de vertices.
    Aqui hace falta el grafo para poder contar (y luego deformar) los vertices,
    asi que se construye como Polyhedron.
    """
    unit = radius / np.sqrt(3.0)   # el radio circunscrito de un cubo es a*sqrt(3)/2
    coords = [
        np.array([-unit, -unit, -unit]),   # 0
        np.array([+unit, -unit, -unit]),   # 1
        np.array([+unit, +unit, -unit]),   # 2
        np.array([-unit, +unit, -unit]),   # 3
        np.array([-unit, -unit, +unit]),   # 4
        np.array([+unit, -unit, +unit]),   # 5
        np.array([+unit, +unit, +unit]),   # 6
        np.array([-unit, +unit, +unit]),   # 7
    ]
    faces = [
        [0, 1, 2, 3],   # z-
        [4, 5, 6, 7],   # z+
        [0, 1, 5, 4],   # y-
        [3, 2, 6, 7],   # y+
        [0, 3, 7, 4],   # x-
        [1, 2, 6, 5],   # x+
    ]
    return coords, faces


def platonic_data(cls, radius=TARGET_RADIUS):
    """Vertices y caras de un solido platonico de manim, reescalado.

    Se instancia con arista 1 para medir su radio circunscrito y luego se pide
    la arista que deja el solido del tamano que ocupa bien el frame vertical.
    Asi los cuatro solidos se ven del mismo tamano en pantalla.
    """
    probe = cls(edge_length=1.0)
    reference = max(np.linalg.norm(v) for v in probe.vertex_coords)
    solid = cls(edge_length=radius / reference)
    return [np.array(v) for v in solid.vertex_coords], solid.faces_list


def torus_data(major=8, minor=4, big_radius=1.85, tube_radius=0.85):
    """Toro triangulado: una malla major x minor cerrada en las dos direcciones.

    Para cualquier malla cerrada de m x n cuadrilateros partidos en triangulos:
        V = m*n,  A = 3*m*n,  C = 2*m*n   ->   V - A + C = 0.
    Con m = 8 y n = 4 salen 32 - 96 + 64 = 0.
    """
    coords = []
    for i in range(major):
        u = TAU * i / major
        for j in range(minor):
            v = TAU * j / minor
            coords.append(np.array([
                (big_radius + tube_radius * np.cos(v)) * np.cos(u),
                (big_radius + tube_radius * np.cos(v)) * np.sin(u),
                tube_radius * np.sin(v),
            ]))

    def idx(i, j):
        return (i % major) * minor + (j % minor)

    faces = []
    for i in range(major):
        for j in range(minor):
            a, b = idx(i, j), idx(i + 1, j)
            c, d = idx(i + 1, j + 1), idx(i, j + 1)
            faces.append([a, b, c])   # cada cuadrilatero de la malla
            faces.append([a, c, d])   # se parte en dos triangulos
    return coords, faces


def build_solid(vertex_coords, faces_list, face_color):
    """Poliedro con vertices, aristas y caras visibles y con la paleta Lnx."""
    return Polyhedron(
        vertex_coords,
        faces_list,
        faces_config={
            "fill_color": face_color,
            "fill_opacity": 0.30,
            "stroke_width": 0,
            "stroke_opacity": 0,
        },
        graph_config={
            "vertex_type": Dot3D,
            "vertex_config": {"color": V_COLOR, "radius": VERTEX_RADIUS},
            "edge_config": {
                "stroke_color": E_COLOR,
                "stroke_width": EDGE_WIDTH,
                "stroke_opacity": 1.0,
            },
        },
    )


class EulerCharacteristic(ThreeDScene):
    # ------------------------------------------------------------- utilidades
    def fix(self, *mobjects, live=False):
        """Ancla rotulos al frame sin mostrarlos todavia.

        add_fixed_in_frame_mobjects hace dos cosas: registra la familia del
        mobject en la camara Y lo anade a la escena. Aqui solo interesa lo
        primero, asi que se quita de la escena inmediatamente y cada beat lo
        hace aparecer con su propia animacion.

        `live=True` es para los contadores: al cambiar de valor, un Integer
        regenera sus digitos, y esos submobjects nuevos NO estan registrados en
        la camara (se proyectarian en 3D). El updater vuelve a fijarlos en cada
        frame, que es barato y evita que los numeros se deformen al rotar.
        """
        for mobject in mobjects:
            self.add_fixed_in_frame_mobjects(mobject)
            self.remove(mobject)
            if live:
                mobject.add_updater(
                    lambda m: self.camera.add_fixed_in_frame_mobjects(m)
                )
        return mobjects[0] if len(mobjects) == 1 else mobjects

    def make_counter(self, letter, color, x):
        """Un contador 'V = n' anclado al frame, con el numero animable."""
        label = MathTex(letter + "=", font_size=40, color=color)
        number = Integer(0, font_size=40, color=color)
        number.next_to(label, RIGHT, buff=0.14)
        group = VGroup(label, number)
        group.move_to(np.array([x, COUNTER_Y, 0.0]))
        self.fix(label)
        self.fix(number, live=True)
        return group, number

    def count_up(self, items, number, kind, run_time):
        """Enciende las piezas una por una mientras el contador sube.

        El conteo tiene que SENTIRSE: el numero no salta, sube al mismo ritmo
        al que se van iluminando los vertices / aristas / caras.
        """
        if kind == "vertex":
            flashes = [Indicate(item, color=V_COLOR, scale_factor=2.1)
                       for item in items]
        elif kind == "edge":
            flashes = [
                ShowPassingFlash(
                    item.copy().set_stroke(color=WHITE, width=EDGE_WIDTH * 2.4),
                    time_width=0.6,
                )
                for item in items
            ]
        else:  # face
            flashes = [Indicate(item, color=F_COLOR, scale_factor=1.0)
                       for item in items]

        self.play(
            AnimationGroup(
                LaggedStart(*flashes, lag_ratio=0.18),
                ChangeDecimalToValue(number, len(items)),
                lag_ratio=0.0,
            ),
            run_time=run_time,
        )

    def solid_parts(self, solid, faces_list):
        """Vertices, aristas (sin duplicar) y caras del poliedro, en orden."""
        vertices = [solid.graph[i] for i in solid.graph.vertices]
        edges = []
        for a, b in unique_edges(faces_list):
            edges.append(solid.graph.edges.get((a, b)) or solid.graph.edges[(b, a)])
        faces = list(solid.faces)
        return vertices, edges, faces

    def euler_line(self, V, A, C, chi):
        """La cuenta resuelta, con cada numero del color de lo que cuenta."""
        line = MathTex(
            str(V), "-", str(A), "+", str(C), "=", str(chi), font_size=48,
        )
        line[0].set_color(V_COLOR)
        line[2].set_color(E_COLOR)
        line[4].set_color(F_COLOR)
        line[6].set_color(CHI_COLOR)
        line.move_to(np.array([0.0, EQUATION_Y, 0.0]))
        fit_to_safe_width(line)
        self.fix(line)
        return line

    # ------------------------------------------------------------- construccion
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        # Camara: un poco por encima del ecuador para que se lean las caras de
        # arriba y la silueta a la vez.
        self.set_camera_orientation(phi=68 * DEGREES, theta=-55 * DEGREES)

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.13
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.8)
        self.fix(watermark)
        self.add(watermark)

        # ---------------------------------------------------------- cabecera
        title = Tex(r"V $-$ A $+$ C", font_size=64, color=WHITE)
        title.move_to(np.array([0.0, TITLE_Y, 0.0]))
        fit_to_safe_width(title)
        self.fix(title)

        subtitle = Tex(r"Siempre da lo mismo", font_size=34, color=GREY_B)
        subtitle.move_to(np.array([0.0, SUBTITLE_Y, 0.0]))
        fit_to_safe_width(subtitle)
        self.fix(subtitle)

        # Contadores: V amarillo, A cian, C magenta. Se reutilizan en todo el
        # video, solo cambian de valor.
        counter_V, num_V = self.make_counter("V", V_COLOR, -2.45)
        counter_A, num_A = self.make_counter("A", E_COLOR, 0.0)
        counter_C, num_C = self.make_counter("C", F_COLOR, 2.45)
        counters = VGroup(counter_V, counter_A, counter_C)

        # ============================================================ HOOK 0-2s
        # El cubo entra ya girando en el primer segundo: nada de pantalla vacia.
        self.begin_ambient_camera_rotation(rate=0.26)

        cube_coords, cube_faces = cube_data()
        cube = build_solid(cube_coords, cube_faces, ACCENT_PURPLE)
        cube_V, cube_A, cube_C = solid_counts(cube_coords, cube_faces)

        self.play(FadeIn(cube, scale=0.55), run_time=0.7)
        self.play(Write(title), run_time=0.6)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.4)

        # ====================================================== BEAT 0: el cubo
        self.play(FadeIn(counters), run_time=0.4)
        cube_vertices, cube_edges, cube_faces_m = self.solid_parts(cube, cube_faces)

        self.count_up(cube_vertices, num_V, "vertex", run_time=2.2)
        self.count_up(cube_edges, num_A, "edge", run_time=2.6)
        self.count_up(cube_faces_m, num_C, "face", run_time=2.0)

        cube_line = self.euler_line(cube_V, cube_A, cube_C, cube_V - cube_A + cube_C)
        self.play(Write(cube_line), run_time=0.9)

        box = SurroundingRectangle(cube_line[6], buff=0.14, corner_radius=0.10)
        box.set_stroke(width=4, color=[ACCENT_YELLOW, ACCENT_PURPLE])
        self.fix(box)
        self.play(Create(box), run_time=0.6)
        self.wait(1.0)

        # ============================== BEAT 1: tetraedro y octaedro, mas rapido
        # Otros solidos, otros numeros, mismo final. Aqui todavia puede parecer
        # casualidad: por eso van seguidos y sin pausa.
        def swap_solid(old_solid, old_line, coords, faces, color, run_time=1.4):
            """Cambia de solido reiniciando los contadores y volviendo a contar."""
            new_solid = build_solid(coords, faces, color)
            V, A, C = solid_counts(coords, faces)

            self.play(
                FadeOut(old_solid, scale=0.55),
                FadeOut(old_line),
                num_V.animate.set_value(0),
                num_A.animate.set_value(0),
                num_C.animate.set_value(0),
                run_time=0.6,
            )
            self.play(FadeIn(new_solid, scale=0.55), run_time=0.6)

            vertices, edges, faces_m = self.solid_parts(new_solid, faces)
            self.count_up(vertices, num_V, "vertex", run_time=run_time)
            self.count_up(edges, num_A, "edge", run_time=run_time)
            self.count_up(faces_m, num_C, "face", run_time=run_time * 0.9)

            new_line = self.euler_line(V, A, C, V - A + C)
            self.play(Write(new_line), run_time=0.7)
            return new_solid, new_line

        self.play(FadeOut(box), run_time=0.3)

        tetra_coords, tetra_faces = platonic_data(Tetrahedron)
        tetra, tetra_line = swap_solid(
            cube, cube_line, tetra_coords, tetra_faces, ACCENT_CYAN, run_time=1.6,
        )
        self.wait(0.8)

        octa_coords, octa_faces = platonic_data(Octahedron)
        octa, octa_line = swap_solid(
            tetra, tetra_line, octa_coords, octa_faces, ACCENT_YELLOW, run_time=1.6,
        )
        self.wait(0.8)

        # =================================== BEAT 2: dodecaedro, la prueba fuerte
        # 20, 30 y 12 no se parecen en nada a 8, 12 y 6. Si aun asi sale 2,
        # deja de ser casualidad.
        dodeca_coords, dodeca_faces = platonic_data(Dodecahedron)
        dodeca, dodeca_line = swap_solid(
            octa, octa_line, dodeca_coords, dodeca_faces, ACCENT_MAGENTA,
            run_time=2.0,
        )

        never_2 = Tex(r"Numeros distintos, mismo 2", font_size=34, color=CHI_COLOR)
        never_2.move_to(np.array([0.0, SUBTITLE_Y, 0.0]))
        fit_to_safe_width(never_2)
        self.fix(never_2)
        self.play(
            FadeOut(subtitle, shift=UP * 0.2),
            FadeIn(never_2, shift=UP * 0.2),
            Indicate(dodeca_line[6], color=ACCENT_YELLOW, scale_factor=1.5),
            run_time=1.0,
        )
        self.wait(1.2)

        # ============================ BEAT 3: no es geometria, es como se conecta
        # Se vuelve al cubo y se le mueven los vertices a mano. Las aristas y las
        # caras siguen a sus vertices (el grafo del Polyhedron se actualiza solo),
        # asi que la FORMA cambia por completo pero la CONEXION no: ningun
        # vertice se crea, ninguna arista se rompe, ninguna cara se parte.
        # Por eso los tres contadores no se mueven.
        self.play(
            FadeOut(dodeca, scale=0.55),
            FadeOut(dodeca_line),
            FadeOut(never_2, shift=UP * 0.2),
            num_V.animate.set_value(0),
            num_A.animate.set_value(0),
            num_C.animate.set_value(0),
            run_time=0.6,
        )

        blob = build_solid(cube_coords, cube_faces, ACCENT_PURPLE)
        self.play(FadeIn(blob, scale=0.55), run_time=0.5)

        blob_vertices, blob_edges, blob_faces_m = self.solid_parts(blob, cube_faces)
        self.play(
            ChangeDecimalToValue(num_V, cube_V),
            ChangeDecimalToValue(num_A, cube_A),
            ChangeDecimalToValue(num_C, cube_C),
            run_time=0.8,
        )
        blob_line = self.euler_line(cube_V, cube_A, cube_C, 2)
        self.play(Write(blob_line), run_time=0.6)

        topology = Tex(r"Deformalo cuanto quieras", font_size=34, color=GREY_B)
        topology.move_to(np.array([0.0, SUBTITLE_Y, 0.0]))
        fit_to_safe_width(topology)
        self.fix(topology)
        self.play(FadeIn(topology, shift=UP * 0.2), run_time=0.4)

        # Desplazamientos deliberadamente feos: el solido deja de ser un cubo,
        # deja de ser convexo, y aun asi V, A y C no cambian.
        offsets = [
            np.array([-1.05, -0.45, -0.70]),
            np.array([+0.85, -1.15, +0.30]),
            np.array([+0.35, +0.95, -1.00]),
            np.array([-0.70, +0.40, +0.95]),
            np.array([-0.30, -0.90, +1.10]),
            np.array([+1.15, +0.25, -0.35]),
            np.array([-0.45, +1.05, +0.55]),
            np.array([+0.55, -0.35, -1.10]),
        ]
        self.play(
            *[
                vertex.animate.move_to(cube_coords[i] + offsets[i] * 0.72)
                for i, vertex in enumerate(blob_vertices)
            ],
            run_time=2.0,
        )
        # Segunda sacudida, para que se vea que no fue una postura afortunada.
        self.play(
            *[
                vertex.animate.move_to(cube_coords[i] * 0.55 - offsets[i] * 0.70)
                for i, vertex in enumerate(blob_vertices)
            ],
            run_time=1.8,
        )

        self.play(
            *[Indicate(counter, color=ACCENT_YELLOW, scale_factor=1.25)
              for counter in counters],
            Indicate(blob_line, color=ACCENT_YELLOW, scale_factor=1.1),
            run_time=1.0,
        )
        self.wait(0.5)

        not_geometry = Tex(r"No es geometria: es topologia", font_size=34,
                           color=CHI_COLOR)
        not_geometry.move_to(np.array([0.0, SUBTITLE_Y, 0.0]))
        fit_to_safe_width(not_geometry)
        self.fix(not_geometry)
        self.play(
            FadeOut(topology, shift=UP * 0.2),
            FadeIn(not_geometry, shift=UP * 0.2),
            run_time=0.6,
        )
        self.wait(1.0)

        # ================================ BEAT 4: romper la regla con un agujero
        # Todo lo anterior eran esferas deformadas. El toro no lo es, y ahi la
        # cuenta cambia: 32 - 96 + 64 = 0.
        torus_coords, torus_faces = torus_data()
        torus_V, torus_A, torus_C = solid_counts(torus_coords, torus_faces)
        torus = build_solid(torus_coords, torus_faces, ACCENT_CYAN)
        # El toro tiene 64 caras: recrearlas en cada frame no aporta nada porque
        # aqui ya no se deforma nada, y ahorra mucho tiempo de render.
        torus.clear_updaters()

        hole = Tex(r"?`Y si le hago un agujero?", font_size=34, color=ACCENT_YELLOW)
        hole.move_to(np.array([0.0, SUBTITLE_Y, 0.0]))
        fit_to_safe_width(hole)
        self.fix(hole)

        self.play(
            FadeOut(blob, scale=0.55),
            FadeOut(blob_line),
            FadeOut(not_geometry, shift=UP * 0.2),
            FadeIn(hole, shift=UP * 0.2),
            num_V.animate.set_value(0),
            num_A.animate.set_value(0),
            num_C.animate.set_value(0),
            run_time=0.8,
        )
        self.play(FadeIn(torus, scale=0.55), run_time=0.7)

        torus_vertices, torus_edges, torus_faces_m = self.solid_parts(
            torus, torus_faces,
        )
        self.count_up(torus_vertices, num_V, "vertex", run_time=2.0)
        self.count_up(torus_edges, num_A, "edge", run_time=2.4)
        self.count_up(torus_faces_m, num_C, "face", run_time=1.9)

        torus_line = self.euler_line(
            torus_V, torus_A, torus_C, torus_V - torus_A + torus_C,
        )
        self.play(Write(torus_line), run_time=0.9)

        zero_box = SurroundingRectangle(torus_line[6], buff=0.14, corner_radius=0.10)
        zero_box.set_stroke(width=4, color=[ACCENT_MAGENTA, ACCENT_PURPLE])
        self.fix(zero_box)
        self.play(Create(zero_box), run_time=0.5)
        self.wait(1.2)

        # ------------------------------------------------------------- cierre
        # El 2 no era magia: era el numero de agujeros disfrazado.
        self.stop_ambient_camera_rotation()

        general = MathTex(r"\chi", "=", "2", "-", "2g", font_size=54)
        general[0].set_color(CHI_COLOR)
        general[4].set_color(ACCENT_YELLOW)
        general.move_to(np.array([0.0, SUBTITLE_Y - 0.15, 0.0]))
        fit_to_safe_width(general)
        self.fix(general)

        gloss = Tex(r"g = numero de agujeros", font_size=30, color=GREY_B)
        gloss.move_to(np.array([0.0, SUBTITLE_Y - 1.05, 0.0]))
        fit_to_safe_width(gloss)
        self.fix(gloss)

        self.play(
            FadeOut(hole, shift=UP * 0.2),
            FadeIn(general, shift=UP * 0.2),
            run_time=0.7,
        )
        self.play(FadeIn(gloss), run_time=0.4)
        self.wait(1.2)

        # Las dos lecturas de la misma formula, una debajo de la otra.
        sphere_case = MathTex(
            r"\text{esfera: }", "g=0", r"\;\Rightarrow\;", r"\chi=2",
            font_size=38,
        )
        sphere_case[3].set_color(ACCENT_PURPLE)
        torus_case = MathTex(
            r"\text{toro: }", "g=1", r"\;\Rightarrow\;", r"\chi=0",
            font_size=38,
        )
        torus_case[3].set_color(ACCENT_CYAN)
        cases = VGroup(sphere_case, torus_case).arrange(DOWN, buff=0.35)
        cases.move_to(np.array([0.0, EQUATION_Y + 1.15, 0.0]))
        fit_to_safe_width(cases)
        self.fix(sphere_case, torus_case)

        self.play(
            FadeOut(torus_line), FadeOut(zero_box),
            FadeIn(sphere_case, shift=UP * 0.2),
            run_time=0.7,
        )
        self.play(FadeIn(torus_case, shift=UP * 0.2), run_time=0.5)
        self.wait(2.0)

        animate_End(scene=self)
