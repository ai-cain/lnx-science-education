from manim import *
from lnx import *

# hidden-invariant | geometry (conic sections) | avanzado
# Esferas de Dandelin: el corte de un cono por un plano oblicuo es una elipse
# y los puntos donde las dos esferas inscritas tocan el plano son sus focos.
#
# CONSTRUCCION ANALITICA (todo se calcula, nada se ajusta a ojo)
# ---------------------------------------------------------------
# Cono:   x^2 + y^2 = (z tan a)^2,  z >= 0,  vertice en el origen, eje Z.
# Plano:  z = c + m x           (equivalente:  m x - z + c = 0)
#
# Una esfera inscrita en el cono tiene centro (0, 0, h) sobre el eje y radio
# r = h sin(a). Imponer que su distancia al plano valga r:
#
#       |c - h| / sqrt(1 + m^2) = h sin(a)
#
# Con k = sin(a) sqrt(1 + m^2) las dos raices son
#
#       h1 = c / (1 + k)      (esfera inferior)
#       h2 = c / (1 - k)      (esfera superior)
#
# y existen (seccion eliptica) exactamente cuando k < 1.
#
# F1, F2 = pie de la perpendicular desde cada centro al plano.
# Circunferencia de tangencia con el cono de la esfera de altura h:
#       z = h cos^2(a),   radio = h cos(a) sin(a)
#
# Sobre una generatriz de angulo theta, A y B son los cortes con esas dos
# circunferencias, y su separacion es AB = cos(a) (h2 - h1): NO depende de
# theta. Como PF1 = PA y PF2 = PB (tangentes a una misma esfera desde P),
#       PF1 + PF2 = AB = constante.
#
# VERIFICACION NUMERICA (ejecutada antes de animar, 721 puntos):
#       AB = 2a = 1.6834788034532704
#       max(PF1+PF2) - min(PF1+PF2) = 1.33e-15
#       PF1 = PA y PF2 = PB en todos los puntos (residuo < 1e-15)
# Las mismas comprobaciones se repiten como asserts en _validate().

ALPHA = 20.0 * DEGREES          # semiangulo del cono
TAN_A = np.tan(ALPHA)
SIN_A = np.sin(ALPHA)
COS_A = np.cos(ALPHA)

M_SLOPE = 0.50                  # pendiente del plano de corte
C_HEIGHT = 2.0                  # altura del plano sobre el eje

K_FACTOR = SIN_A * np.sqrt(1.0 + M_SLOPE**2)
H_LOW = C_HEIGHT / (1.0 + K_FACTOR)
H_UP = C_HEIGHT / (1.0 - K_FACTOR)
R_LOW = H_LOW * SIN_A
R_UP = H_UP * SIN_A

Z_TC_LOW = H_LOW * COS_A**2      # altura de la circunferencia de tangencia
R_TC_LOW = H_LOW * COS_A * SIN_A
Z_TC_UP = H_UP * COS_A**2
R_TC_UP = H_UP * COS_A * SIN_A

CONE_TOP = H_UP + R_UP           # el cono debe envolver la esfera superior
SUM_CONST = COS_A * (H_UP - H_LOW)   # = AB = 2a

PLANE_NORMAL = np.array([M_SLOPE, 0.0, -1.0])

SCALE = 2.0
Z_CENTER = CONE_TOP / 2.0


def W(point):
    """Coordenadas matematicas -> coordenadas de escena."""
    p = np.asarray(point, dtype=float)
    return SCALE * np.array([p[0], p[1], p[2] - Z_CENTER])


def cone_point(z, theta):
    return np.array([z * TAN_A * np.cos(theta), z * TAN_A * np.sin(theta), z])


def ellipse_point(theta):
    """Punto de la elipse: interseccion del plano con la generatriz theta."""
    z = C_HEIGHT / (1.0 - M_SLOPE * TAN_A * np.cos(theta))
    return cone_point(z, theta)


def sphere_focus(h):
    """Pie de la perpendicular del centro (0,0,h) al plano de corte."""
    center = np.array([0.0, 0.0, h])
    t = (PLANE_NORMAL @ center + C_HEIGHT) / (PLANE_NORMAL @ PLANE_NORMAL)
    return center - t * PLANE_NORMAL


FOCUS_LOW = sphere_focus(H_LOW)
FOCUS_UP = sphere_focus(H_UP)


def tangency_low(theta):
    return np.array(
        [R_TC_LOW * np.cos(theta), R_TC_LOW * np.sin(theta), Z_TC_LOW]
    )


def tangency_up(theta):
    return np.array([R_TC_UP * np.cos(theta), R_TC_UP * np.sin(theta), Z_TC_UP])


def _validate(tolerance=1e-9):
    """Comprueba la construccion completa antes de dibujar nada."""
    assert K_FACTOR < 1.0, "el plano no produce una elipse"

    for h, r, focus in ((H_LOW, R_LOW, FOCUS_LOW), (H_UP, R_UP, FOCUS_UP)):
        center = np.array([0.0, 0.0, h])
        # tangente al plano: distancia centro-plano = radio, y el pie esta en el plano
        distance = abs(M_SLOPE * 0.0 - h + C_HEIGHT) / np.sqrt(1 + M_SLOPE**2)
        assert abs(distance - r) < tolerance
        assert abs(M_SLOPE * focus[0] - focus[2] + C_HEIGHT) < tolerance
        assert abs(np.linalg.norm(focus - center) - r) < tolerance

    sums = []
    for theta in np.linspace(0.0, TAU, 721):
        p = ellipse_point(theta)
        # P esta sobre el cono y sobre el plano
        assert abs(np.linalg.norm(p[:2]) - p[2] * TAN_A) < tolerance
        assert abs(M_SLOPE * p[0] - p[2] + C_HEIGHT) < tolerance

        a_pt, b_pt = tangency_low(theta), tangency_up(theta)
        pf1 = np.linalg.norm(p - FOCUS_LOW)
        pf2 = np.linalg.norm(p - FOCUS_UP)
        pa = np.linalg.norm(p - a_pt)
        pb = np.linalg.norm(p - b_pt)
        # tangentes desde P a una misma esfera
        assert abs(pf1 - pa) < tolerance
        assert abs(pf2 - pb) < tolerance
        assert abs(pa + pb - SUM_CONST) < tolerance
        sums.append(pf1 + pf2)

    assert max(sums) - min(sums) < 1e-12
    assert abs(np.mean(sums) - SUM_CONST) < tolerance
    return max(sums) - min(sums)


def fit_width(mobject, max_width=7.4):
    if mobject.width > max_width:
        mobject.scale_to_fit_width(max_width)
    return mobject


class DandelinSpheres(ThreeDScene):
    def construct(self):
        _validate()

        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        def fixed(*mobs):
            self.add_fixed_in_frame_mobjects(*mobs)
            self.remove(*mobs)
            return mobs[0] if len(mobs) == 1 else mobs

        self.set_camera_orientation(phi=72 * DEGREES, theta=-58 * DEGREES)

        # ---------------------------------------------------------------
        # Objetos 3D
        # ---------------------------------------------------------------
        cone = Surface(
            lambda u, v: W(cone_point(u, v)),
            u_range=[0.02, CONE_TOP],
            v_range=[0, TAU],
            resolution=(14, 32),
            checkerboard_colors=False,
            fill_color=ACCENT_PURPLE,
            fill_opacity=0.22,
            stroke_color=ACCENT_PURPLE,
            stroke_width=0.7,
            stroke_opacity=0.6,
        )

        plane_center_xy = np.array([0.137, 0.0])
        cut_plane = Surface(
            lambda u, v: W(
                [
                    plane_center_xy[0] + u * np.cos(v),
                    plane_center_xy[1] + u * np.sin(v),
                    C_HEIGHT
                    + M_SLOPE * (plane_center_xy[0] + u * np.cos(v)),
                ]
            ),
            u_range=[0.001, 1.35],
            v_range=[0, TAU],
            resolution=(6, 28),
            checkerboard_colors=False,
            fill_color=ACCENT_YELLOW,
            fill_opacity=0.16,
            stroke_width=0,
        )

        ellipse = ParametricFunction(
            lambda t: W(ellipse_point(t)),
            t_range=[0, TAU, 0.01],
            color=ACCENT_YELLOW,
            stroke_width=7,
        )
        ellipse.set_z_index(6)

        sphere_low = Sphere(
            center=W([0, 0, H_LOW]),
            radius=SCALE * R_LOW,
            resolution=(16, 24),
            checkerboard_colors=False,
            fill_color=ACCENT_CYAN,
            fill_opacity=0.28,
            stroke_color=ACCENT_CYAN,
            stroke_width=0.6,
            stroke_opacity=0.5,
        )
        sphere_up = Sphere(
            center=W([0, 0, H_UP]),
            radius=SCALE * R_UP,
            resolution=(16, 24),
            checkerboard_colors=False,
            fill_color=ACCENT_MAGENTA,
            fill_opacity=0.22,
            stroke_color=ACCENT_MAGENTA,
            stroke_width=0.6,
            stroke_opacity=0.45,
        )

        circle_low = ParametricFunction(
            lambda t: W(tangency_low(t)),
            t_range=[0, TAU, 0.02],
            color=ACCENT_CYAN,
            stroke_width=5,
        )
        circle_up = ParametricFunction(
            lambda t: W(tangency_up(t)),
            t_range=[0, TAU, 0.02],
            color=ACCENT_MAGENTA,
            stroke_width=5,
        )

        f1_dot = Dot3D(W(FOCUS_LOW), radius=0.10, color=ACCENT_CYAN)
        f2_dot = Dot3D(W(FOCUS_UP), radius=0.10, color=ACCENT_MAGENTA)
        f1_dot.set_z_index(10)
        f2_dot.set_z_index(10)

        f1_label = MathTex(r"F_1", font_size=34, color=ACCENT_CYAN)
        f2_label = MathTex(r"F_2", font_size=34, color=ACCENT_MAGENTA)
        f1_label.move_to(W(FOCUS_LOW) + 0.42 * DOWN + 0.34 * LEFT)
        f2_label.move_to(W(FOCUS_UP) + 0.42 * UP + 0.34 * RIGHT)

        # ---------------------------------------------------------------
        # HOOK (0 - 2 s): el cono ya se esta cortando
        # ---------------------------------------------------------------
        hook = Tex(
            r"\textbf{Todos saben que el corte es una elipse.}",
            font_size=36,
            color=WHITE,
        ).move_to(UP * 5.15)
        fit_width(hook)
        fixed(hook)

        self.play(
            Create(cone, run_time=0.9),
            FadeIn(hook, shift=UP * 0.12, run_time=0.7),
        )
        self.play(
            FadeIn(cut_plane, run_time=0.5),
            Create(ellipse, run_time=1.0),
        )

        hook2 = Tex(
            r"\textbf{¿Pero de dónde salen sus focos?}",
            font_size=40,
            color=ACCENT_YELLOW,
        ).move_to(UP * 4.35)
        fit_width(hook2)
        fixed(hook2)
        self.play(FadeIn(hook2, shift=UP * 0.12), run_time=0.6)
        self.begin_ambient_camera_rotation(rate=0.16)
        self.wait(2.0)

        # ---------------------------------------------------------------
        # BEAT 1: las dos esferas de Dandelin
        # ---------------------------------------------------------------
        beat1 = Tex(
            r"\textbf{Metemos dos esferas dentro del cono.}",
            font_size=34,
            color=WHITE,
        ).move_to(UP * 4.35)
        fit_width(beat1)
        fixed(beat1)
        self.play(ReplacementTransform(hook2, beat1), run_time=0.6)

        note_low = Tex(
            r"Tangente al cono en una circunferencia\\ "
            r"y al plano en \textbf{un} punto.",
            font_size=30,
            color=ACCENT_CYAN,
        ).move_to(DOWN * 4.85)
        fit_width(note_low)
        fixed(note_low)

        self.play(FadeIn(sphere_low, scale=0.6), run_time=1.0)
        self.play(Create(circle_low), FadeIn(note_low), run_time=1.0)
        self.play(FadeIn(f1_dot, scale=0.4), run_time=0.5)
        self.add_fixed_orientation_mobjects(f1_label)
        self.play(FadeIn(f1_label), run_time=0.4)
        self.wait(1.0)

        note_up = Tex(
            r"La segunda esfera hace lo mismo\\ por encima del plano.",
            font_size=30,
            color=ACCENT_MAGENTA,
        ).move_to(DOWN * 4.85)
        fit_width(note_up)
        fixed(note_up)

        self.play(
            FadeIn(sphere_up, scale=0.6),
            ReplacementTransform(note_low, note_up),
            run_time=1.1,
        )
        self.play(Create(circle_up), run_time=0.9)
        self.play(FadeIn(f2_dot, scale=0.4), run_time=0.5)
        self.add_fixed_orientation_mobjects(f2_label)
        self.play(FadeIn(f2_label), run_time=0.4)
        self.wait(1.2)

        reveal = Tex(
            r"\textbf{Esos dos puntos son los focos.}",
            font_size=36,
            color=ACCENT_YELLOW,
        ).move_to(DOWN * 4.85)
        fit_width(reveal)
        fixed(reveal)
        self.play(ReplacementTransform(note_up, reveal), run_time=0.6)
        self.play(
            Flash(f1_dot.get_center(), color=ACCENT_CYAN, flash_radius=0.5),
            Flash(f2_dot.get_center(), color=ACCENT_MAGENTA, flash_radius=0.5),
            run_time=1.0,
        )
        self.wait(1.2)
        self.stop_ambient_camera_rotation()

        # ---------------------------------------------------------------
        # BEAT 2: la demostracion
        # ---------------------------------------------------------------
        self.move_camera(phi=70 * DEGREES, theta=-48 * DEGREES, run_time=1.2)

        beat2 = Tex(
            r"\textbf{La demostración: un punto $P$ cualquiera.}",
            font_size=32,
            color=WHITE,
        ).move_to(UP * 4.35)
        fit_width(beat2)
        fixed(beat2)
        self.play(
            ReplacementTransform(beat1, beat2),
            FadeOut(reveal),
            cone.animate.set_fill(opacity=0.10).set_stroke(opacity=0.25),
            cut_plane.animate.set_fill(opacity=0.09),
            sphere_low.animate.set_fill(opacity=0.16).set_stroke(opacity=0.25),
            sphere_up.animate.set_fill(opacity=0.13).set_stroke(opacity=0.22),
            run_time=1.0,
        )

        theta_tracker = ValueTracker(0.55)

        def th():
            return theta_tracker.get_value()

        p_dot = always_redraw(
            lambda: Dot3D(W(ellipse_point(th())), radius=0.11, color=WHITE)
        )
        p_label = MathTex(r"P", font_size=36, color=WHITE)
        p_label.add_updater(
            lambda mob: mob.move_to(W(ellipse_point(th())) + 0.45 * UP)
        )

        generatrix = always_redraw(
            lambda: Line(
                W(cone_point(0.0, th())),
                W(cone_point(CONE_TOP, th())),
                color=ACCENT_YELLOW,
                stroke_width=3.5,
                stroke_opacity=0.85,
            )
        )
        a_dot = always_redraw(
            lambda: Dot3D(W(tangency_low(th())), radius=0.09, color=ACCENT_CYAN)
        )
        b_dot = always_redraw(
            lambda: Dot3D(W(tangency_up(th())), radius=0.09, color=ACCENT_MAGENTA)
        )

        seg_pf1 = always_redraw(
            lambda: Line(
                W(ellipse_point(th())),
                W(FOCUS_LOW),
                color=ACCENT_CYAN,
                stroke_width=6,
            )
        )
        seg_pf2 = always_redraw(
            lambda: Line(
                W(ellipse_point(th())),
                W(FOCUS_UP),
                color=ACCENT_MAGENTA,
                stroke_width=6,
            )
        )
        seg_pa = always_redraw(
            lambda: DashedLine(
                W(ellipse_point(th())),
                W(tangency_low(th())),
                color=ACCENT_CYAN,
                stroke_width=5,
                dash_length=0.10,
            )
        )
        seg_pb = always_redraw(
            lambda: DashedLine(
                W(ellipse_point(th())),
                W(tangency_up(th())),
                color=ACCENT_MAGENTA,
                stroke_width=5,
                dash_length=0.10,
            )
        )

        self.play(FadeIn(p_dot, scale=0.4), run_time=0.5)
        self.add_fixed_orientation_mobjects(p_label)
        self.play(FadeIn(p_label), run_time=0.3)

        gen_note = Tex(
            r"La generatriz por $P$ corta las dos\\ "
            r"circunferencias en $A$ y $B$.",
            font_size=30,
            color=ACCENT_YELLOW,
        ).move_to(DOWN * 4.9)
        fit_width(gen_note)
        fixed(gen_note)
        self.play(Create(generatrix), FadeIn(gen_note), run_time=0.9)
        self.play(FadeIn(a_dot, scale=0.4), FadeIn(b_dot, scale=0.4), run_time=0.6)
        self.wait(0.8)

        # Igualdad 1: PF1 = PA
        eq1 = MathTex(r"PF_1", r"=", r"PA", font_size=44)
        eq1[0].set_color(ACCENT_CYAN)
        eq1[2].set_color(ACCENT_CYAN)
        eq1.move_to(UP * 3.55)
        reason1 = Tex(
            r"tangentes a la \textbf{misma} esfera desde $P$",
            font_size=28,
            color=GREY_B,
        ).move_to(UP * 2.9)
        fit_width(reason1)
        fixed(eq1, reason1)

        self.play(
            Create(seg_pf1),
            Create(seg_pa),
            FadeOut(gen_note),
            run_time=0.9,
        )
        self.play(Write(eq1), FadeIn(reason1), run_time=0.9)
        self.play(Indicate(eq1, color=ACCENT_CYAN, scale_factor=1.08), run_time=1.0)

        # Igualdad 2: PF2 = PB
        eq2 = MathTex(r"PF_2", r"=", r"PB", font_size=44)
        eq2[0].set_color(ACCENT_MAGENTA)
        eq2[2].set_color(ACCENT_MAGENTA)
        eq2.move_to(UP * 2.2)
        fixed(eq2)

        self.play(Create(seg_pf2), Create(seg_pb), run_time=0.9)
        self.play(Write(eq2), run_time=0.7)
        self.play(
            Indicate(eq2, color=ACCENT_MAGENTA, scale_factor=1.08), run_time=1.0
        )
        self.wait(0.6)

        # La cadena
        chain = MathTex(
            r"PF_1+PF_2", r"=", r"PA+PB", r"=", r"AB",
            font_size=40,
        )
        chain[0].set_color(WHITE)
        chain[2].set_color(WHITE)
        chain[4].set_color(ACCENT_YELLOW)
        chain.move_to(UP * 3.0)
        fit_width(chain)
        ab_note = Tex(
            r"$AB$ = distancia entre las dos circunferencias\\ "
            r"a lo largo de la generatriz.",
            font_size=28,
            color=ACCENT_YELLOW,
        ).move_to(UP * 2.1)
        fit_width(ab_note)
        fixed(chain, ab_note)

        self.play(
            FadeOut(reason1),
            FadeOut(eq2),
            ReplacementTransform(eq1, chain),
            run_time=0.9,
        )
        self.play(FadeIn(ab_note, shift=UP * 0.08), run_time=0.6)
        self.wait(1.2)

        key = Tex(
            r"\textbf{y $AB$ no depende de $P$.}",
            font_size=36,
            color=ACCENT_YELLOW,
        ).move_to(UP * 2.1)
        fit_width(key)
        fixed(key)
        self.play(ReplacementTransform(ab_note, key), run_time=0.7)

        # Contador que no cambia
        counter_label = MathTex(
            r"PF_1+PF_2 =", font_size=40, color=WHITE
        )
        counter = DecimalNumber(
            SUM_CONST, num_decimal_places=3, font_size=40, color=ACCENT_YELLOW
        )
        counter.add_updater(
            lambda mob: mob.set_value(
                np.linalg.norm(ellipse_point(th()) - FOCUS_LOW)
                + np.linalg.norm(ellipse_point(th()) - FOCUS_UP)
            )
        )
        counter_group = VGroup(counter_label, counter).arrange(RIGHT, buff=0.25)
        counter_group.move_to(DOWN * 4.9)
        counter_box = SurroundingRectangle(
            counter_group,
            color=ACCENT_YELLOW,
            buff=0.22,
            corner_radius=0.12,
            stroke_width=3,
        )
        fixed(counter_box, counter_label, counter)

        self.play(Create(counter_box), FadeIn(counter_group), run_time=0.7)
        self.wait(0.6)

        move_note = Tex(
            r"\textbf{Mueve $P$ por toda la elipse: la suma no se mueve.}",
            font_size=30,
            color=WHITE,
        ).move_to(DOWN * 3.85)
        fit_width(move_note)
        fixed(move_note)
        self.play(FadeIn(move_note), run_time=0.5)

        self.play(
            theta_tracker.animate.set_value(0.55 + TAU),
            run_time=9.0,
            rate_func=linear,
        )
        self.wait(0.5)

        # ---------------------------------------------------------------
        # CIERRE
        # ---------------------------------------------------------------
        p_label.clear_updaters()
        counter.clear_updaters()

        closing = MathTex(
            r"PF_1+PF_2 = \text{constante}",
            font_size=46,
            color=ACCENT_YELLOW,
        ).move_to(UP * 3.0)
        fit_width(closing)
        definition = Tex(
            r"\textbf{Esa es, exactamente,}\\ "
            r"\textbf{la definición de elipse.}",
            font_size=38,
            color=WHITE,
        ).move_to(UP * 1.9)
        fit_width(definition)
        fixed(closing, definition)

        self.play(
            FadeOut(key),
            FadeOut(move_note),
            ReplacementTransform(chain, closing),
            run_time=0.9,
        )
        self.play(FadeIn(definition, shift=UP * 0.1), run_time=0.7)
        self.play(
            Indicate(closing, color=ACCENT_YELLOW, scale_factor=1.06),
            run_time=1.2,
        )

        self.play(
            FadeOut(seg_pa),
            FadeOut(seg_pb),
            FadeOut(generatrix),
            FadeOut(a_dot),
            FadeOut(b_dot),
            ellipse.animate.set_stroke(width=9),
            run_time=0.8,
        )
        self.move_camera(phi=58 * DEGREES, theta=-20 * DEGREES, run_time=2.2)
        self.wait(1.2)

        animate_End(scene=self)
