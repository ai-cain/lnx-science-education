from manim import *
from lnx import *

# transformacion-lineal | algebra lineal | intermedio
# Autovectores: las direcciones que una matriz NO gira.
#
# Con A = [[2,1],[1,2]]:
#   det(A - lambda I) = (2-lambda)^2 - 1 = 0  =>  lambda = 3, 1.
#   A (1, 1)  = (2+1, 1+2) = (3, 3) = 3 (1, 1)     ->  lambda = 3
#   A (1,-1)  = (2-1, 1-2) = (1,-1) = 1 (1,-1)     ->  lambda = 1
# Todo vector del plano es combinacion de esas dos direcciones, asi que la
# transformacion entera se reduce a "estirar 3 en una recta y 1 en la otra".
# Como 3 > 1, al aplicar A repetidamente cualquier vector generico se alinea
# con la direccion dominante (1,1): eso es el metodo de la potencia, el motor
# detras de PageRank, PCA y los analisis de estabilidad.
#
# El frame real es 9 x 16 (x en [-4.5, 4.5], y en [-8, 8]).
# Zona segura: |y| <= 5.6 y |x| <= 3.8.

config.frame_width = 9.0
config.frame_height = 16.0
config.pixel_width = int(round(config.pixel_height * 9 / 16))

# ---------------------------------------------------------------- layout
PLANE_CENTER = np.array([0.0, 0.8, 0.0])   # el plano vive en el tercio central
UNIT = 0.85                                # unidades de escena por unidad de dato
PLANE_X = 3.5                              # semi-rango horizontal en datos
PLANE_Y = 4.5                              # semi-rango vertical en datos
TITLE_Y = 5.35                             # dentro de |y| <= 5.6
CAPTION_Y = -4.35                          # bajo el plano, sobre la UI de TikTok
FORMULA_Y = -5.35
SAFE_WIDTH = 7.2

MATRIX = np.array([[2.0, 1.0], [1.0, 2.0]])

EIG_HI = ACCENT_YELLOW      # autovector dominante (1,1), lambda = 3
EIG_LO = ACCENT_MAGENTA     # autovector (1,-1), lambda = 1
GENERIC = ACCENT_CYAN       # vector cualquiera, el que si gira
GRID_COLOR = ACCENT_PURPLE


def fit_to_safe_width(mobject):
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


def apply_A(vec):
    return MATRIX @ np.asarray(vec, dtype=float)


class Eigenvectors(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.14
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.85)
        watermark.set_z_index(30)
        self.add(watermark)

        # ------------------------------------------------------------- el plano
        plane = NumberPlane(
            x_range=[-PLANE_X, PLANE_X, 1],
            y_range=[-PLANE_Y, PLANE_Y, 1],
            x_length=2 * PLANE_X * UNIT,
            y_length=2 * PLANE_Y * UNIT,
            background_line_style={
                "stroke_color": GRID_COLOR,
                "stroke_width": 1.6,
                "stroke_opacity": 0.35,
            },
            axis_config={"stroke_color": GREY_B, "stroke_width": 2,
                         "stroke_opacity": 0.8, "include_ticks": False},
        )
        plane.move_to(PLANE_CENTER)
        origin = plane.c2p(0, 0)

        def vec(data, color, width=6, opacity=1.0):
            """Flecha desde el origen del plano hasta las coordenadas de dato."""
            arrow = Arrow(
                origin, plane.c2p(data[0], data[1]),
                buff=0, color=color, stroke_width=width,
                max_tip_length_to_length_ratio=0.22,
                max_stroke_width_to_length_ratio=14,
            )
            arrow.set_opacity(opacity)
            return arrow

        # --------------------------------------------------------- hook 0 - 1.5 s
        # Titulo minimo
        title = Tex(r"¿Cuál NO gira?", font_size=60, color=ACCENT_YELLOW)
        title.set_stroke(width=1.2)
        title.set_z_index(20)
        title.move_to(UP * TITLE_Y)
        fit_to_safe_width(title)

        self.play(Write(title), FadeIn(plane), run_time=0.8)

        # 24 direcciones: abanico completo
        angles = [k * 15 * DEGREES for k in range(24)]
        RADIUS = 1.0
        fan = VGroup(*[
            vec([RADIUS * np.cos(a), RADIUS * np.sin(a)], GREY_B, width=5,
                opacity=0.8)
            for a in angles
        ])
        self.play(LaggedStart(*[GrowArrow(a) for a in fan],
                              lag_ratio=0.015), run_time=0.7)
        self.wait(0.3)

        # Aplicamos A con transformacion rapida y visualmente impactante
        targets = VGroup(*[
            vec(apply_A([RADIUS * np.cos(a), RADIUS * np.sin(a)]), GREY_B,
                width=5, opacity=0.8)
            for a in angles
        ])
        for i, color in ((3, EIG_HI), (21, EIG_LO)):
            targets[i].set_color(color).set_opacity(1.0).set_stroke(width=8)

        # Sin caption, solo accion
        self.play(
            *[Transform(fan[i], targets[i]) for i in range(24)],
            run_time=1.2,
        )
        self.wait(0.2)

        # Destaca SOLO los dos especiales
        line_hi = Line(plane.c2p(-3.4, -3.4), plane.c2p(3.4, 3.4),
                       color=EIG_HI, stroke_width=4)
        line_hi.set_stroke(opacity=0.5)
        line_lo = Line(plane.c2p(-3.4, 3.4), plane.c2p(3.4, -3.4),
                       color=EIG_LO, stroke_width=4)
        line_lo.set_stroke(opacity=0.5)

        self.play(
            Create(line_hi), Create(line_lo),
            *[fan[i].animate.set_opacity(0.15) for i in range(24)
              if i not in (3, 21)],
            run_time=0.9,
        )
        self.play(
            Indicate(fan[3], color=EIG_HI, scale_factor=1.15),
            Indicate(fan[21], color=EIG_LO, scale_factor=1.15),
            run_time=0.8,
        )
        self.wait(0.3)

        self.play(
            FadeOut(fan), FadeOut(line_hi), FadeOut(line_lo),
            run_time=0.5,
        )

        # Omitir la matriz numerica: es confusa

        # ---------------------------------------------- beat 1: el vector que GIRA
        u = np.array([2.2, 0.5])
        u_arrow = vec(u, GENERIC, width=7)

        self.play(GrowArrow(u_arrow), run_time=0.5)

        Au = apply_A(u)
        Au_arrow = vec(Au, GENERIC, width=7)

        ghost = u_arrow.copy().set_opacity(0.3)
        self.add(ghost)
        self.play(Transform(u_arrow, Au_arrow), run_time=0.9)
        self.wait(0.2)

        self.play(FadeOut(VGroup(u_arrow, ghost)), run_time=0.4)

        # ------------------------------------- beat 2 + 3: Los EIGENVECTORES (ambos juntos)
        # Simplificado: mostrar ambos rapidamente
        line_hi.set_stroke(opacity=0.55)
        line_lo.set_stroke(opacity=0.55)

        self.play(Create(line_hi), Create(line_lo), run_time=0.6)
        self.wait(0.2)

        # Primer eigenvector: (1,1) -> se estira 3x
        v = np.array([1.0, 1.0])
        v_arrow = vec(v, EIG_HI, width=7)
        self.play(GrowArrow(v_arrow), run_time=0.4)

        Av = apply_A(v)
        Av_arrow = vec(Av, EIG_HI, width=7)
        v_ghost = v_arrow.copy().set_opacity(0.3)
        self.add(v_ghost)
        self.play(Transform(v_arrow, Av_arrow), run_time=0.8)
        self.wait(0.2)

        # Ecuacion: simple
        eq_hi = MathTex(r"A\vec{v} = 3\vec{v}", font_size=52, color=EIG_HI)
        eq_hi.set_stroke(width=1.2)
        eq_hi.set_z_index(20)
        eq_hi.move_to(np.array([0.0, CAPTION_Y, 0.0]))
        self.play(FadeIn(eq_hi, scale=0.9), run_time=0.6)
        self.wait(0.3)

        self.play(FadeOut(VGroup(v_arrow, v_ghost, eq_hi)), run_time=0.4)

        # Segundo eigenvector: (1,-1) -> se queda igual (lambda=1)
        w = np.array([2.0, -2.0])
        w_arrow = vec(w, EIG_LO, width=7)
        self.play(GrowArrow(w_arrow), run_time=0.4)

        w_ghost = w_arrow.copy().set_opacity(0.3)
        self.add(w_ghost)
        # No se mueve: solo "wiggle" para mostrar que se aplico A
        self.play(Wiggle(w_arrow, scale_value=1.08, run_time=0.7))
        self.wait(0.2)

        eq_lo = MathTex(r"A\vec{w} = \vec{w}", font_size=52, color=EIG_LO)
        eq_lo.set_stroke(width=1.2)
        eq_lo.set_z_index(20)
        eq_lo.move_to(np.array([0.0, CAPTION_Y, 0.0]))
        self.play(FadeIn(eq_lo, scale=0.9), run_time=0.6)
        self.wait(0.3)

        self.play(
            FadeOut(VGroup(w_arrow, w_ghost, line_hi, line_lo, eq_lo)),
            run_time=0.4,
        )

        # ------------------------------ beat 4: La potencia (metodo de la potencia)
        # Rapido y visual: vector que gira hasta alinearse con eigenvector dominante
        line_hi.set_stroke(opacity=0.55)
        self.play(Create(line_hi), run_time=0.4)

        current = np.array([3.0, 0.4])
        SHOW_LEN = 2.4
        arrow = vec(current / np.linalg.norm(current) * SHOW_LEN, GENERIC, width=7)
        self.play(GrowArrow(arrow), run_time=0.4)

        # Aplicar A varias veces: el vector rota hacia (1,1)
        for n in range(1, 4):
            current = apply_A(current)
            direction = current / np.linalg.norm(current) * SHOW_LEN
            new_arrow = vec(direction, GENERIC, width=7)
            self.play(Transform(arrow, new_arrow), run_time=0.5)

        # Ahora esta alineado (magicamente) con el eigenvector dominante
        self.play(arrow.animate.set_color(EIG_HI), run_time=0.6)
        self.wait(0.3)

        self.play(
            FadeOut(VGroup(arrow, line_hi, line_lo, plane, title)),
            run_time=0.5,
        )

        # Cierre: formula limpia y corto
        final = MathTex(r"A\vec{v} = \lambda\vec{v}", font_size=80)
        final.set_color(ACCENT_YELLOW)
        final.set_stroke(width=1.5)
        final.move_to(UP * 1.2)

        box = SurroundingRectangle(final, buff=0.35, corner_radius=0.2)
        box.set_stroke(width=5, color=ACCENT_YELLOW)

        self.play(Write(final), run_time=0.9)
        self.play(Create(box), run_time=0.7)
        self.wait(1.2)

        animate_End(scene=self)
