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

        # --------------------------------------------------------- hook 0 - 2 s
        # Primero la pregunta, para que el abanico ya llegue con un porque.
        title = Tex(r"Los vectores que no giran", font_size=52, color=WHITE)
        title.set_stroke(width=1)
        title.set_z_index(20)
        title.move_to(UP * TITLE_Y)
        fit_to_safe_width(title)

        underline = Line(
            title.get_left() + DOWN * 0.3, title.get_right() + DOWN * 0.3,
            stroke_width=4,
        )
        underline.set_color(color=[ACCENT_CYAN, ACCENT_MAGENTA])
        underline.set_z_index(20)

        self.play(Write(title), run_time=0.7)
        self.play(Create(underline), FadeIn(plane), run_time=0.6)

        # 24 direcciones unitarias: el abanico completo del plano.
        angles = [k * 15 * DEGREES for k in range(24)]
        RADIUS = 1.0
        fan = VGroup(*[
            vec([RADIUS * np.cos(a), RADIUS * np.sin(a)], GREY_B, width=4,
                opacity=0.85)
            for a in angles
        ])
        self.play(LaggedStart(*[GrowArrow(a) for a in fan],
                              lag_ratio=0.02), run_time=0.9)

        # Aplicamos A. Casi todas las flechas cambian de direccion; las de 45
        # y -45 grados (indices 3 y 21) solo cambian de largo.
        targets = VGroup(*[
            vec(apply_A([RADIUS * np.cos(a), RADIUS * np.sin(a)]), GREY_B,
                width=4, opacity=0.85)
            for a in angles
        ])
        for i, color in ((3, EIG_HI), (21, EIG_LO)):
            targets[i].set_color(color).set_opacity(1.0).set_stroke(width=7)

        caption = Tex(r"Aplico una transformaci\'on\ldots", font_size=34,
                      color=WHITE)
        caption.set_stroke(width=0.6)
        caption.set_z_index(20)
        caption.move_to(np.array([0.0, CAPTION_Y, 0.0]))
        fit_to_safe_width(caption)
        self.play(Write(caption), run_time=0.5)

        self.play(
            *[Transform(fan[i], targets[i]) for i in range(24)],
            run_time=1.6,
        )
        self.wait(0.3)

        # Las dos rectas invariantes: ahi viven los vectores que no giraron.
        line_hi = Line(plane.c2p(-3.4, -3.4), plane.c2p(3.4, 3.4),
                       color=EIG_HI, stroke_width=3)
        line_hi.set_stroke(opacity=0.45)
        line_lo = Line(plane.c2p(-3.4, 3.4), plane.c2p(3.4, -3.4),
                       color=EIG_LO, stroke_width=3)
        line_lo.set_stroke(opacity=0.45)

        new_caption = Tex(r"casi todos giran. Dos, no.", font_size=34,
                          color=WHITE)
        new_caption.set_stroke(width=0.6)
        new_caption.set_z_index(20)
        new_caption.move_to(np.array([0.0, CAPTION_Y, 0.0]))
        fit_to_safe_width(new_caption)

        self.play(
            Create(line_hi), Create(line_lo),
            Transform(caption, new_caption),
            *[fan[i].animate.set_opacity(0.18) for i in range(24)
              if i not in (3, 21)],
            run_time=1.0,
        )
        self.play(
            Indicate(fan[3], color=EIG_HI, scale_factor=1.12),
            Indicate(fan[21], color=EIG_LO, scale_factor=1.12),
            run_time=0.9,
        )
        self.wait(0.4)

        self.play(
            FadeOut(fan), FadeOut(line_hi), FadeOut(line_lo),
            FadeOut(caption),
            run_time=0.6,
        )

        # ------------------------------------------------- la matriz protagonista
        matrix_tex = MathTex(
            r"A=\begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}",
            font_size=44, color=WHITE,
        )
        matrix_tex.set_stroke(width=1)
        matrix_tex.set_z_index(20)
        matrix_tex.move_to(np.array([0.0, CAPTION_Y - 0.2, 0.0]))
        self.play(Write(matrix_tex), run_time=0.8)
        self.wait(0.4)

        # ---------------------------------------------- beat 1: el vector generico
        # Un vector cualquiera sale de su propia recta: cambia de direccion.
        u = np.array([2.2, 0.5])
        u_line = DashedLine(
            plane.c2p(-3.4, -3.4 * u[1] / u[0]),
            plane.c2p(3.4, 3.4 * u[1] / u[0]),
            color=GENERIC, stroke_width=2.5, dash_length=0.12,
        )
        u_line.set_stroke(opacity=0.5)
        u_arrow = vec(u, GENERIC)
        u_label = MathTex(r"\vec{u}", font_size=36, color=GENERIC)
        u_label.set_stroke(width=1)
        u_label.next_to(u_arrow.get_end(), DR, buff=0.12)

        self.play(Create(u_line), GrowArrow(u_arrow), Write(u_label),
                  run_time=0.8)

        Au = apply_A(u)                       # = (4.9, 3.2)
        Au_arrow = vec(Au, GENERIC)
        Au_label = MathTex(r"A\vec{u}", font_size=36, color=GENERIC)
        Au_label.set_stroke(width=1)
        Au_label.next_to(Au_arrow.get_end(), RIGHT, buff=0.12)

        beat1 = Tex(r"La transformaci\'on lo sac\'o de su recta.",
                    font_size=32, color=GENERIC)
        beat1.set_stroke(width=0.6)
        beat1.set_z_index(20)
        beat1.move_to(np.array([0.0, FORMULA_Y, 0.0]))
        fit_to_safe_width(beat1)

        ghost = u_arrow.copy().set_opacity(0.28)
        self.add(ghost)
        self.play(Transform(u_arrow, Au_arrow),
                  ReplacementTransform(u_label, Au_label), run_time=1.1)
        # El angulo entre la recta original y el resultado hace visible el giro.
        turn = Angle(u_line, Line(origin, Au_arrow.get_end()),
                     radius=0.7, color=WHITE, stroke_width=3)
        self.play(Create(turn), Write(beat1), run_time=0.8)
        self.wait(1.0)

        self.play(
            FadeOut(VGroup(u_arrow, ghost, u_line, Au_label, turn, beat1)),
            run_time=0.5,
        )

        # ------------------------------------- beat 2: el autovector v = (1,1)
        # Aqui el vector se queda clavado en su recta: solo cambia de largo.
        line_hi.set_stroke(opacity=0.55)
        self.play(Create(line_hi), run_time=0.5)

        eig_caption = Tex(r"El eigenespacio: la recta que $A$ respeta.",
                          font_size=30, color=EIG_HI)
        eig_caption.set_stroke(width=0.6)
        eig_caption.set_z_index(20)
        eig_caption.move_to(np.array([0.0, FORMULA_Y, 0.0]))
        fit_to_safe_width(eig_caption)
        self.play(Write(eig_caption), run_time=0.6)

        v = np.array([1.0, 1.0])
        v_arrow = vec(v, EIG_HI)
        v_label = MathTex(r"\vec{v}=(1,1)", font_size=34, color=EIG_HI)
        v_label.set_stroke(width=1)
        v_label.next_to(v_arrow.get_end(), UL, buff=0.1)
        self.play(GrowArrow(v_arrow), Write(v_label), run_time=0.7)
        self.wait(0.3)

        Av = apply_A(v)                       # = (3, 3)
        Av_arrow = vec(Av, EIG_HI)
        v_ghost = v_arrow.copy().set_opacity(0.3)
        self.add(v_ghost)
        self.play(
            Transform(v_arrow, Av_arrow),
            v_label.animate.next_to(plane.c2p(3, 3), UL, buff=0.1),
            run_time=1.1,
        )

        # Misma recta, tres veces mas largo: eso es exactamente Av = 3v.
        eq_hi = MathTex(r"A\vec{v}", r"=", r"3", r"\vec{v}",
                        font_size=46)
        eq_hi[0].set_color(EIG_HI)
        eq_hi[2].set_color(WHITE)
        eq_hi[3].set_color(EIG_HI)
        eq_hi.set_stroke(width=1)
        eq_hi.set_z_index(20)
        eq_hi.move_to(np.array([0.0, CAPTION_Y - 0.2, 0.0]))
        self.play(FadeOut(matrix_tex), FadeIn(eq_hi, shift=UP * 0.2),
                  run_time=0.7)
        self.play(Indicate(eq_hi[2], color=EIG_HI, scale_factor=1.5),
                  run_time=0.7)
        self.wait(0.7)

        self.play(
            FadeOut(VGroup(v_arrow, v_ghost, v_label, eig_caption)),
            FadeOut(line_hi),
            run_time=0.5,
        )

        # ----------------------------------- beat 3: el segundo, v = (1,-1)
        # lambda = 1: la direccion queda intacta y el largo tambien.
        line_lo.set_stroke(opacity=0.55)
        self.play(Create(line_lo), run_time=0.5)

        w = np.array([2.0, -2.0])
        w_arrow = vec(w, EIG_LO)
        w_label = MathTex(r"\vec{w}=(1,-1)", font_size=34, color=EIG_LO)
        w_label.set_stroke(width=1)
        w_label.next_to(w_arrow.get_end(), RIGHT, buff=0.12)

        eq_lo = MathTex(r"A\vec{w}", r"=", r"1", r"\vec{w}", font_size=46)
        eq_lo[0].set_color(EIG_LO)
        eq_lo[3].set_color(EIG_LO)
        eq_lo.set_stroke(width=1)
        eq_lo.set_z_index(20)
        eq_lo.move_to(np.array([0.0, CAPTION_Y - 0.2, 0.0]))

        beat3 = Tex(r"$\lambda=1$: ni se estira. Direcci\'on intacta.",
                    font_size=30, color=EIG_LO)
        beat3.set_stroke(width=0.6)
        beat3.set_z_index(20)
        beat3.move_to(np.array([0.0, FORMULA_Y, 0.0]))
        fit_to_safe_width(beat3)

        self.play(GrowArrow(w_arrow), Write(w_label), run_time=0.7)
        self.play(ReplacementTransform(eq_hi, eq_lo), run_time=0.7)
        # No hay nada que animar en la flecha, y ese es justo el punto: la
        # sacudida deja claro que A ya actuo y no cambio nada.
        self.play(Wiggle(w_arrow, scale_value=1.06), Write(beat3), run_time=1.0)
        self.wait(0.8)

        self.play(FadeOut(VGroup(w_arrow, w_label, beat3)), run_time=0.4)

        # ------------------------------ beat 4: los ejes propios y la dominancia
        line_hi.set_stroke(opacity=0.55)
        self.play(Create(line_hi), run_time=0.4)

        beat4 = Tex(r"Estirar $3$ en una recta, $1$ en la otra.",
                    font_size=30, color=WHITE)
        beat4.set_stroke(width=0.6)
        beat4.set_z_index(20)
        beat4.move_to(np.array([0.0, FORMULA_Y, 0.0]))
        fit_to_safe_width(beat4)

        # La cuadricula deformada muestra que esas dos rectas son los ejes
        # propios: la malla se estira a lo largo de ellas sin torcerlas.
        self.play(
            plane.animate.apply_matrix(MATRIX, about_point=origin),
            Write(beat4),
            run_time=1.6,
        )
        self.wait(0.6)
        self.play(
            plane.animate.apply_matrix(np.linalg.inv(MATRIX),
                                       about_point=origin),
            FadeOut(beat4),
            run_time=1.0,
        )

        # Metodo de la potencia: A^n u se alinea con la direccion dominante.
        power = Tex(r"Aplica $A$ una y otra vez:", font_size=32, color=WHITE)
        power.set_stroke(width=0.6)
        power.set_z_index(20)
        power.move_to(np.array([0.0, FORMULA_Y, 0.0]))
        fit_to_safe_width(power)
        self.play(Write(power), run_time=0.5)

        current = np.array([3.0, 0.4])
        SHOW_LEN = 2.4          # largo fijo: solo interesa la direccion
        arrow = vec(current / np.linalg.norm(current) * SHOW_LEN, GENERIC)
        exp_label = MathTex(r"A^{0}\vec{u}", font_size=34, color=GENERIC)
        exp_label.set_stroke(width=1)
        exp_label.next_to(arrow.get_end(), RIGHT, buff=0.12)
        self.play(GrowArrow(arrow), Write(exp_label), run_time=0.5)

        # Angulos: 7.6 -> 28.0 -> 39.2 -> 43.0 -> 44.5 grados. Converge a 45.
        for n in range(1, 5):
            current = apply_A(current)
            direction = current / np.linalg.norm(current) * SHOW_LEN
            new_arrow = vec(direction, GENERIC)
            new_label = MathTex(rf"A^{{{n}}}\vec{{u}}", font_size=34,
                                color=GENERIC)
            new_label.set_stroke(width=1)
            new_label.next_to(new_arrow.get_end(), RIGHT, buff=0.12)
            self.play(
                Transform(arrow, new_arrow),
                Transform(exp_label, new_label),
                run_time=0.45,
            )

        dominant = Tex(r"Se alinea con el $\lambda$ m\'as grande.",
                       font_size=30, color=EIG_HI)
        dominant.set_stroke(width=0.6)
        dominant.set_z_index(20)
        dominant.move_to(np.array([0.0, FORMULA_Y, 0.0]))
        fit_to_safe_width(dominant)
        self.play(
            Transform(power, dominant),
            arrow.animate.set_color(EIG_HI),
            Indicate(line_hi, color=EIG_HI, scale_factor=1.0),
            run_time=0.9,
        )
        self.wait(0.6)

        uses = Tex(r"PageRank, PCA, estabilidad.", font_size=32, color=WHITE)
        uses.set_stroke(width=0.6)
        uses.set_z_index(20)
        uses.move_to(np.array([0.0, FORMULA_Y, 0.0]))
        fit_to_safe_width(uses)
        self.play(Transform(power, uses), run_time=0.7)
        self.wait(0.9)

        # ------------------------------------------------------------- cierre
        self.play(
            FadeOut(VGroup(arrow, exp_label, line_hi, line_lo, plane,
                           eq_lo, power)),
            FadeOut(title), FadeOut(underline),
            run_time=0.7,
        )

        final = MathTex(r"A\vec{v}", r"=", r"\lambda", r"\vec{v}",
                        font_size=76)
        final[0].set_color(ACCENT_CYAN)
        final[2].set_color(ACCENT_YELLOW)
        final[3].set_color(ACCENT_CYAN)
        final.set_stroke(width=1.5)
        final.move_to(UP * 0.8)
        fit_to_safe_width(final)

        box = SurroundingRectangle(final, buff=0.3, corner_radius=0.16)
        box.set_stroke(width=4, color=[ACCENT_YELLOW, ACCENT_MAGENTA])

        self.play(Write(final), run_time=1.0)
        self.play(Create(box), run_time=0.7)
        self.wait(1.6)

        animate_End(scene=self)
