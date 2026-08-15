import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import brentq

from manim import *
from lnx import *

# visual-derivation | calculus | advanced
# La braquistocrona: la curva de bajada mas rapida entre dos puntos.
#
# Johann Bernoulli, 1696. Entre A y B hay infinitas rampas; la que minimiza el
# tiempo de caida NO es la recta. Por conservacion de energia una bolita que
# parte del reposo lleva v = sqrt(2 g y) tras bajar una altura y, asi que el
# tiempo total de recorrido es el funcional
#
#     T[y] = int ds / v = int sqrt((1 + y'^2) / (2 g y)) dx.
#
# Minimizarlo (Euler-Lagrange, o el argumento optico de Bernoulli via la ley de
# Snell) da la cicloide  x = r(t - sin t),  y = -r(1 - cos t).
#
# El gancho del video es el contraste: la cicloide es la MAS LARGA de las tres
# rampas y aun asi llega primero, porque baja empinada al principio y compra
# velocidad temprano. La velocidad vale mas que la distancia.
#
# Segundo golpe: la misma cicloide es TAUTOCRONA (Huygens, 1659). Sueltes la
# bolita donde la sueltes, tarda exactamente pi*sqrt(r/g) en llegar al fondo.
#
# Todo lo que se ve en pantalla esta calculado, no inventado:
#   - r y el rango de t se resuelven con brentq para que la cicloide pase
#     exactamente por A y por B (se verifica abajo, error ~1e-15).
#   - Los tres tiempos de bajada se integran numericamente y se contrastan con
#     el valor exacto de la cicloide, sqrt(r/g) * T.
#   - El movimiento de las bolitas sigue la dinamica real: se precalcula la
#     tabla tiempo -> parametro y se interpola. Nada de MoveAlongPath uniforme.
#   - La tautocrona se comprueba soltando desde cuatro alturas distintas.
# Ejecuta `python scene.py` para imprimir todas esas comprobaciones.
#
# El frame real mide 9 x 16 unidades (x en [-4.5, 4.5], y en [-8, 8]).
# Zona segura: |y| <= 5.6 y |x| <= 3.8.

SAFE_WIDTH = 7.2

G = 9.81                       # gravedad, en unidades de escena por segundo^2

# Extremos de la carrera, en coordenadas "de fisica" (y hacia arriba).
A_PT = np.array([-2.9, 3.2])
B_PT = np.array([2.7, 0.0])
OFFSET = np.array([0.0, 1.0, 0.0])   # sube el escenario dentro de la zona segura

DX = B_PT[0] - A_PT[0]         # 5.6 de avance horizontal
DY = A_PT[1] - B_PT[1]         # 3.2 de caida

# Camara lenta: los tiempos reales son de ~1.4 s y en pantalla no se leerian.
# Se multiplican los tres por el MISMO factor, asi que las proporciones (que es
# lo que el video afirma) se mantienen intactas.
SLOWMO = 2.6


# --------------------------------------------------------------- la cicloide
# x = r(t - sin t), y = -r(1 - cos t) con la cuspide en A. Imponer que pase por
# B deja una sola ecuacion en T, porque el cociente x/y elimina a r:
#     (T - sin T) / (1 - cos T) = DX / DY.
def _cycloid_shape(T):
    return (T - np.sin(T)) / (1 - np.cos(T)) - DX / DY


T_END = brentq(_cycloid_shape, 1e-9, 2 * np.pi - 1e-9)
R_CYC = DY / (1 - np.cos(T_END))
# T_END > pi, asi que la cicloide baja por debajo de B y vuelve a subir: es el
# caso interesante, y ademas es el que la hace mas larga que las otras dos.

# ---------------------------------------------------------- el arco de circulo
# Arco por A y B cuyo radio se elige para que su longitud quede estrictamente
# entre la recta y la cicloide. Asi la cicloide es, sin discusion, la MAS LARGA
# de las tres, que es justo la afirmacion del gancho.
CHORD = float(np.linalg.norm(B_PT - A_PT))
ARC_TARGET = 6.72

R_ARC = brentq(
    lambda Rc: 2 * Rc * np.arcsin(CHORD / (2 * Rc)) - ARC_TARGET,
    CHORD / 2 + 1e-9, 100.0,
)
_mid = (A_PT + B_PT) / 2
_dir = (B_PT - A_PT) / CHORD
_normal = np.array([_dir[1], -_dir[0]])                  # apunta bajo la cuerda
C_ARC = _mid - _normal * np.sqrt(R_ARC**2 - (CHORD / 2) ** 2)
TH_0 = np.arctan2(A_PT[1] - C_ARC[1], A_PT[0] - C_ARC[0])
TH_1 = np.arctan2(B_PT[1] - C_ARC[1], B_PT[0] - C_ARC[0])
while TH_1 < TH_0:
    TH_1 += 2 * np.pi


# ------------------------------------------------- las tres rampas, p en [0,1]
def pos_line(p):
    return A_PT + (B_PT - A_PT) * p


def vel_line(p):
    return B_PT - A_PT


def pos_arc(p):
    th = TH_0 + (TH_1 - TH_0) * p
    return C_ARC + R_ARC * np.array([np.cos(th), np.sin(th)])


def vel_arc(p):
    th = TH_0 + (TH_1 - TH_0) * p
    return R_ARC * (TH_1 - TH_0) * np.array([-np.sin(th), np.cos(th)])


def pos_cycloid(p):
    t = T_END * p
    return A_PT + np.array([R_CYC * (t - np.sin(t)), -R_CYC * (1 - np.cos(t))])


def vel_cycloid(p):
    t = T_END * p
    return T_END * np.array([R_CYC * (1 - np.cos(t)), -R_CYC * np.sin(t)])


class Ramp:
    """Una rampa con su dinamica real precalculada.

    El tiempo de bajada es  int ds / v  con  v = sqrt(2 g h),  donde h es lo que
    la bolita ya bajo respecto del punto de suelta. El integrando diverge como
    1/sqrt(h) al arrancar, asi que se integra en la variable q con p = q^2: el
    2q del jacobiano cancela exactamente la singularidad y la cuadratura queda
    limpia. De paso, la tabla acumulada da la inversa tiempo -> parametro que
    mueve la bolita.
    """

    def __init__(self, pos, vel, color, label, samples=4001):
        self.pos, self.vel, self.color, self.label = pos, vel, color, label

        q = np.linspace(0.0, 1.0, samples)
        self.params = q**2
        speeds = np.array([float(np.linalg.norm(vel(p))) for p in self.params])
        drops = np.array([A_PT[1] - pos(p)[1] for p in self.params])

        integrand = np.zeros(samples)
        ok = drops > 1e-12
        integrand[ok] = 2 * q[ok] * speeds[ok] / np.sqrt(2 * G * drops[ok])
        integrand[0] = integrand[1]        # el limite en q=0 es finito
        self.times = cumulative_trapezoid(integrand, q, initial=0.0)
        self.total = float(self.times[-1])

        self.length = float(
            np.trapezoid(speeds, self.params)
            if hasattr(np, "trapezoid") else np.trapz(speeds, self.params)
        )

    def point(self, p):
        xy = self.pos(p)
        return np.array([xy[0], xy[1], 0.0]) + OFFSET

    def point_at_time(self, tau):
        """Donde esta la bolita despues de tau segundos simulados."""
        p = float(np.interp(min(tau, self.total), self.times, self.params))
        return self.point(p)


RAMPS = [
    Ramp(pos_line, vel_line, ACCENT_CYAN, r"recta"),
    Ramp(pos_arc, vel_arc, ACCENT_MAGENTA, r"circunferencia"),
    Ramp(pos_cycloid, vel_cycloid, ACCENT_YELLOW, r"cicloide"),
]
LINE_RAMP, ARC_RAMP, CYC_RAMP = RAMPS
RACE_END = max(ramp.total for ramp in RAMPS)


# ----------------------------------------------------------- la tautocrona
# Un arco completo de cicloide (t de 0 a 2pi) es un cuenco. Necesita 2*pi*r de
# ancho, asi que lleva su propio radio para caber en la zona segura; el radio de
# la braquistocrona daria 10.1 unidades y se saldria del cuadro.
R_BOWL = 1.10
BOWL_TOP = 2.6                      # altura de las cuspides del cuenco


def bowl_point(t):
    return np.array([
        R_BOWL * (t - np.sin(t)) - np.pi * R_BOWL,
        BOWL_TOP - R_BOWL * (1 - np.cos(t)),
        0.0,
    ])


class BowlDrop:
    """Bolita soltada en t0 sobre el cuenco, cayendo hasta el fondo (t = pi)."""

    def __init__(self, t0, samples=3001):
        self.t0 = t0
        q = np.linspace(0.0, 1.0, samples)
        self.ts = t0 + (np.pi - t0) * q**2
        drops = R_BOWL * (np.cos(t0) - np.cos(self.ts))
        speeds = R_BOWL * np.sqrt(np.maximum(2 * (1 - np.cos(self.ts)), 0.0))

        integrand = np.zeros(samples)
        ok = drops > 1e-12
        integrand[ok] = (
            speeds[ok] * (np.pi - t0) * 2 * q[ok] / np.sqrt(2 * G * drops[ok])
        )
        integrand[0] = integrand[1]
        self.times = cumulative_trapezoid(integrand, q, initial=0.0)
        self.total = float(self.times[-1])

    def point_at_time(self, tau):
        t = float(np.interp(min(tau, self.total), self.times, self.ts))
        return bowl_point(t)


BOWL_T0 = [0.45, 0.95, 1.55, 2.25]
BOWL_DROPS = [BowlDrop(t0) for t0 in BOWL_T0]
TAUTO_EXACT = np.pi * np.sqrt(R_BOWL / G)
BOWL_END = max(drop.total for drop in BOWL_DROPS)


def fit_to_safe_width(mobject):
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


class Brachistochrone(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.14
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.85)
        self.add(watermark)

        AUX_COLOR = GREY_B
        WIN_COLOR = ManimColor(ACCENT_YELLOW)

        # ------------------------------------------------------------ hook 0-2s
        # El titulo dura poco a proposito: lo que engancha es la carrera, y las
        # tres bolitas tienen que estar cayendo antes del segundo 2.
        title = Tex(r"\textquestiondown Cu\'al baja antes?", font_size=54,
                    color=WHITE)
        title.set_stroke(width=1)
        title.set_z_index(20)
        title.move_to(UP * 5.35)
        fit_to_safe_width(title)

        underline = Line(
            title.get_left() + DOWN * 0.3, title.get_right() + DOWN * 0.3,
            stroke_width=4,
        )
        underline.set_color(color=[ACCENT_CYAN, ACCENT_MAGENTA, ACCENT_YELLOW])
        underline.set_z_index(20)
        self.play(Write(title), Create(underline), run_time=0.6)

        A_dot = Dot(LINE_RAMP.point(0.0), color=WHITE, radius=0.075)
        B_dot = Dot(LINE_RAMP.point(1.0), color=WHITE, radius=0.075)
        A_tag = MathTex("A", font_size=32, color=WHITE)
        A_tag.next_to(A_dot, UL, buff=0.06)
        B_tag = MathTex("B", font_size=32, color=WHITE)
        B_tag.next_to(B_dot, UR, buff=0.06)
        endpoints = VGroup(A_dot, B_dot, A_tag, B_tag).set_z_index(12)

        curves = VGroup()
        for ramp in RAMPS:
            curve = ParametricFunction(
                ramp.point, t_range=[0.0, 1.0, 0.004],
                stroke_width=6, color=ramp.color,
            )
            curve.set_z_index(4)
            curves.add(curve)

        # Las tres rampas nacen a la vez: la comparacion es el contenido.
        self.play(FadeIn(endpoints), Create(curves, lag_ratio=0.0), run_time=0.9)

        balls = VGroup()
        for ramp in RAMPS:
            ball = Dot(ramp.point(0.0), color=ramp.color, radius=0.13)
            ball.set_stroke(WHITE, width=2)
            ball.set_z_index(15)
            balls.add(ball)
        self.play(FadeIn(balls, scale=1.6), run_time=0.35)

        # ------------------------------------------------------- la carrera
        clock = ValueTracker(0.0)   # segundos simulados, no de pantalla

        def follow(ball, ramp):
            ball.add_updater(lambda m: m.move_to(
                ramp.point_at_time(clock.get_value())))

        for ball, ramp in zip(balls, RAMPS):
            follow(ball, ramp)

        readout = VGroup(
            DecimalNumber(0, num_decimal_places=2, font_size=34, color=WHITE),
            Tex(r"s", font_size=30, color=AUX_COLOR),
        ).arrange(RIGHT, buff=0.12)
        readout[0].add_updater(lambda m: m.set_value(clock.get_value()))
        readout.move_to(np.array([0.0, 0.15, 0.0]))
        readout.set_z_index(20)

        slowmo = Tex(r"c\'amara lenta", font_size=28, color=AUX_COLOR)
        slowmo.next_to(readout, DOWN, buff=0.22)
        slowmo.set_z_index(20)
        self.add(readout, slowmo)

        self.play(
            clock.animate.set_value(RACE_END),
            run_time=RACE_END * SLOWMO, rate_func=linear,
        )
        for ball in balls:
            ball.clear_updaters()
        readout[0].clear_updaters()

        # La amarilla gana: se marca en el instante en que ya se vio ganar.
        winner_ring = Circle(radius=0.3, color=WIN_COLOR, stroke_width=5)
        winner_ring.move_to(balls[2]).set_z_index(14)
        winner = Tex(r"gana la \textbf{cicloide}", font_size=40, color=WIN_COLOR)
        winner.set_stroke(width=1)
        winner.move_to(np.array([0.0, 0.15, 0.0])).set_z_index(20)
        fit_to_safe_width(winner)
        self.play(
            FadeOut(readout), FadeOut(slowmo),
            Create(winner_ring), FadeIn(winner, shift=UP * 0.15),
            run_time=0.7,
        )
        self.wait(0.5)

        # --------------------------------------------------- beat 1: la paradoja
        # Los numeros de esta tabla salen de la integracion, no de la nada.
        rows = VGroup()
        header = VGroup(
            Tex(r"rampa", font_size=30, color=AUX_COLOR),
            Tex(r"largo", font_size=30, color=AUX_COLOR),
            Tex(r"tiempo", font_size=30, color=AUX_COLOR),
        )
        rows.add(*header)
        for ramp in RAMPS:
            rows.add(
                Tex(ramp.label, font_size=30, color=ramp.color),
                MathTex(f"{ramp.length:.2f}", font_size=30, color=ramp.color),
                MathTex(f"{ramp.total:.2f}\\,\\mathrm{{s}}",
                        font_size=30, color=ramp.color),
            )
        rows.arrange_in_grid(rows=4, cols=3, buff=(0.55, 0.3), col_alignments="lcc")
        rows.move_to(np.array([0.0, -1.5, 0.0]))
        rows.set_z_index(20)
        fit_to_safe_width(rows)

        self.play(FadeOut(winner), FadeOut(winner_ring), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(cell) for cell in rows],
                              lag_ratio=0.05), run_time=1.4)
        self.wait(0.4)

        # El golpe: la fila amarilla tiene el largo MAYOR y el tiempo MENOR.
        longest = rows[10]      # largo de la cicloide
        fastest = rows[11]      # tiempo de la cicloide
        self.play(
            Indicate(longest, color=WHITE, scale_factor=1.4),
            Indicate(fastest, color=WHITE, scale_factor=1.4),
            run_time=1.0,
        )

        paradox = Tex(
            r"es la m\'as \textbf{larga} y aun as\'i llega \textbf{primero}",
            font_size=34, color=WHITE,
        )
        paradox.set_stroke(width=1)
        paradox.move_to(np.array([0.0, -3.3, 0.0])).set_z_index(20)
        fit_to_safe_width(paradox)
        self.play(FadeIn(paradox, shift=UP * 0.15), run_time=0.8)
        self.wait(0.6)

        why = Tex(
            r"baja empinada al principio:\\ gana velocidad temprano",
            font_size=32, color=ACCENT_YELLOW,
        )
        why.move_to(np.array([0.0, -4.5, 0.0])).set_z_index(20)
        fit_to_safe_width(why)
        self.play(FadeIn(why, shift=UP * 0.15), run_time=0.8)

        # Segunda pasada de la carrera con la explicacion ya en pantalla: se ve
        # a la amarilla despegarse en el primer tercio y no devolver la ventaja.
        clock.set_value(0.0)
        for ball, ramp in zip(balls, RAMPS):
            ball.move_to(ramp.point(0.0))
            follow(ball, ramp)
        self.play(
            clock.animate.set_value(RACE_END),
            run_time=RACE_END * SLOWMO * 0.8, rate_func=linear,
        )
        for ball in balls:
            ball.clear_updaters()
        self.wait(0.4)

        # ----------------------------------------------------- beat 2: la fisica
        self.play(
            FadeOut(rows), FadeOut(paradox), FadeOut(why),
            FadeOut(curves[0]), FadeOut(curves[1]),
            FadeOut(balls[0]), FadeOut(balls[1]),
            run_time=0.7,
        )

        # Conservacion de energia: toda la altura perdida se vuelve velocidad.
        level = DashedLine(
            LINE_RAMP.point(0.0) + LEFT * 0.35,
            np.array([3.5, LINE_RAMP.point(0.0)[1], 0.0]),
            color=AUX_COLOR, stroke_width=2, dash_length=0.09,
        )
        level.set_stroke(opacity=0.6)
        probe_p = 0.62
        probe = CYC_RAMP.point(probe_p)
        drop_arrow = DoubleArrow(
            np.array([probe[0], LINE_RAMP.point(0.0)[1], 0.0]), probe,
            buff=0.0, stroke_width=3, color=ACCENT_CYAN,
            tip_length=0.16,
        )
        drop_tag = MathTex("y", font_size=34, color=ACCENT_CYAN)
        drop_tag.next_to(drop_arrow, RIGHT, buff=0.1)
        probe_dot = Dot(probe, color=ACCENT_YELLOW, radius=0.1).set_z_index(15)
        self.play(Create(level), run_time=0.4)
        self.play(GrowFromCenter(drop_arrow), FadeIn(drop_tag),
                  FadeIn(probe_dot), run_time=0.7)

        energy = MathTex(r"v", r"=", r"\sqrt{2gy}", font_size=44)
        energy[0].set_color(ACCENT_MAGENTA)
        energy[2].set_color(ACCENT_CYAN)
        energy.set_stroke(width=1)
        energy.move_to(np.array([0.0, -0.7, 0.0])).set_z_index(20)
        fit_to_safe_width(energy)
        self.play(Write(energy), run_time=0.9)

        energy_tag = Tex(r"conservaci\'on de la energ\'ia",
                         font_size=28, color=AUX_COLOR)
        energy_tag.next_to(energy, DOWN, buff=0.2).set_z_index(20)
        self.play(FadeIn(energy_tag), run_time=0.5)
        self.wait(0.5)

        # El tiempo total es una integral, y depende de la curva entera.
        functional = MathTex(
            r"T[y]", r"=", r"\int_A^B \frac{ds}{v}", r"=",
            r"\int_0^{x_B}\!\sqrt{\frac{1+y'^2}{2gy}}\;dx",
            font_size=38,
        )
        functional[0].set_color(WIN_COLOR)
        functional.set_stroke(width=1)
        functional.arrange(RIGHT, buff=0.14)
        functional.move_to(np.array([0.0, -2.35, 0.0])).set_z_index(20)
        fit_to_safe_width(functional)
        self.play(
            FadeOut(energy_tag),
            TransformFromCopy(energy[0], functional[2]),
            run_time=0.8,
        )
        self.play(Write(functional[0:2]), run_time=0.7)
        self.play(Write(functional[3:]), run_time=1.1)
        self.wait(0.5)

        ask = Tex(r"\textquestiondown qu\'e curva $y(x)$ lo hace m\'inimo?",
                  font_size=32, color=AUX_COLOR)
        ask.move_to(np.array([0.0, -3.4, 0.0])).set_z_index(20)
        fit_to_safe_width(ask)
        self.play(FadeIn(ask), run_time=0.6)
        self.wait(0.6)

        answer = MathTex(
            r"x = r(t - \sin t)", r"\\", r"y = -r(1 - \cos t)",
            font_size=40, color=WIN_COLOR,
        )
        answer.set_stroke(width=1)
        answer.move_to(np.array([0.0, -4.5, 0.0])).set_z_index(20)
        fit_to_safe_width(answer)
        self.play(Write(answer), run_time=1.2)

        # Los valores concretos de esta cicloide, resueltos para pasar por B.
        fitted = MathTex(
            rf"r = {R_CYC:.2f}", r"\qquad", rf"t \in [0,\ {T_END:.2f}]",
            font_size=32, color=AUX_COLOR,
        )
        fitted.next_to(answer, DOWN, buff=0.28).set_z_index(20)
        fit_to_safe_width(fitted)
        self.play(FadeIn(fitted), Flash(curves[2], color=WIN_COLOR,
                                        line_length=0.15, num_lines=18),
                  run_time=0.9)
        self.wait(0.8)

        # --------------------------------------------- beat 3: la tautocrona
        self.play(
            FadeOut(VGroup(
                title, underline, level, drop_arrow, drop_tag, probe_dot,
                energy, functional, ask, answer, fitted, curves[2], balls[2],
                endpoints,
            )),
            run_time=0.8,
        )

        tauto_title = Tex(r"y hay un segundo milagro", font_size=44, color=WHITE)
        tauto_title.set_stroke(width=1)
        tauto_title.move_to(UP * 5.3).set_z_index(20)
        fit_to_safe_width(tauto_title)
        self.play(Write(tauto_title), run_time=0.8)

        bowl = ParametricFunction(
            bowl_point, t_range=[0.0, 2 * np.pi, 0.01],
            stroke_width=7, color=ACCENT_MAGENTA,
        )
        bowl.set_z_index(4)
        self.play(Create(bowl), run_time=1.2)

        bowl_tag = Tex(r"la misma cicloide", font_size=32, color=ACCENT_MAGENTA)
        bowl_tag.move_to(np.array([0.0, BOWL_TOP + 0.75, 0.0])).set_z_index(20)
        self.play(FadeIn(bowl_tag), run_time=0.5)

        # Cuatro alturas de suelta bien distintas: casi arriba y casi al fondo.
        drop_balls = VGroup()
        for drop in BOWL_DROPS:
            ball = Dot(bowl_point(drop.t0), color=ACCENT_CYAN, radius=0.13)
            ball.set_stroke(WHITE, width=2)
            ball.set_z_index(15)
            drop_balls.add(ball)
        self.play(LaggedStart(*[FadeIn(b, scale=1.6) for b in drop_balls],
                              lag_ratio=0.12), run_time=0.9)

        heights = Tex(r"alturas distintas", font_size=32, color=ACCENT_CYAN)
        heights.move_to(np.array([0.0, -0.9, 0.0])).set_z_index(20)
        self.play(FadeIn(heights), run_time=0.5)

        bowl_clock = ValueTracker(0.0)

        def follow_bowl(ball, drop):
            ball.add_updater(lambda m: m.move_to(
                drop.point_at_time(bowl_clock.get_value())))

        # Dos pasadas: la primera sorprende, la segunda deja comprobarlo.
        for pass_index in range(2):
            bowl_clock.set_value(0.0)
            for ball, drop in zip(drop_balls, BOWL_DROPS):
                ball.move_to(bowl_point(drop.t0))
                follow_bowl(ball, drop)
            self.play(
                bowl_clock.animate.set_value(BOWL_END),
                run_time=BOWL_END * SLOWMO, rate_func=linear,
            )
            for ball in drop_balls:
                ball.clear_updaters()
            if pass_index == 0:
                self.play(Flash(bowl_point(np.pi), color=WHITE,
                                line_length=0.2, num_lines=16), run_time=0.5)

        together = Tex(r"llegan \textbf{a la vez}", font_size=40, color=WIN_COLOR)
        together.set_stroke(width=1)
        together.move_to(np.array([0.0, -0.9, 0.0])).set_z_index(20)
        fit_to_safe_width(together)
        self.play(FadeOut(heights), FadeIn(together, shift=UP * 0.15),
                  run_time=0.6)

        tauto_law = MathTex(r"t", r"=", r"\pi\sqrt{\dfrac{r}{g}}", font_size=46)
        tauto_law[2].set_color(ACCENT_MAGENTA)
        tauto_law.set_stroke(width=1)
        tauto_law.move_to(np.array([0.0, -2.4, 0.0])).set_z_index(20)
        fit_to_safe_width(tauto_law)
        self.play(Write(tauto_law), run_time=0.9)

        no_depend = Tex(r"no depende de d\'onde la sueltes",
                        font_size=32, color=AUX_COLOR)
        no_depend.next_to(tauto_law, DOWN, buff=0.3).set_z_index(20)
        fit_to_safe_width(no_depend)
        self.play(FadeIn(no_depend), run_time=0.6)

        law_box = SurroundingRectangle(tauto_law, buff=0.2, corner_radius=0.12)
        law_box.set_stroke(width=4, color=[ACCENT_YELLOW, ACCENT_MAGENTA])
        law_box.set_z_index(19)
        self.play(Create(law_box), run_time=0.6)
        self.wait(0.8)

        # ------------------------------------------------------------- cierre
        self.play(
            FadeOut(VGroup(bowl, bowl_tag, drop_balls, together,
                           tauto_law, no_depend, law_box, tauto_title)),
            run_time=0.7,
        )

        credit = VGroup(
            Tex(r"Johann Bernoulli lo propuso en 1696", font_size=36,
                color=WHITE),
            Tex(r"Newton lo resolvi\'o en una noche", font_size=36,
                color=ACCENT_YELLOW),
        ).arrange(DOWN, buff=0.5)
        credit.set_stroke(width=1)
        credit.move_to(ORIGIN).set_z_index(20)
        for line in credit:
            fit_to_safe_width(line)
        self.play(FadeIn(credit[0], shift=UP * 0.2), run_time=0.9)
        self.play(FadeIn(credit[1], shift=UP * 0.2), run_time=0.9)
        self.wait(1.4)

        animate_End(scene=self)


def _verify():
    """Comprobaciones numericas del video. `python scene.py` las imprime."""
    print(f"cicloide: r = {R_CYC:.9f}   t en [0, {T_END:.9f}]"
          f"  (T/pi = {T_END / np.pi:.4f})")
    print(f"  pasa por B: dx = {R_CYC * (T_END - np.sin(T_END)):.12f}"
          f" (objetivo {DX})")
    print(f"              dy = {R_CYC * (1 - np.cos(T_END)):.12f}"
          f" (objetivo {DY})")
    print(f"arco de circulo: R = {R_ARC:.6f}, centro = {C_ARC}")
    print(f"  |A-C| = {np.linalg.norm(A_PT - C_ARC):.12f}"
          f"   |B-C| = {np.linalg.norm(B_PT - C_ARC):.12f}")
    print("\ntiempos de bajada (integrados):")
    for ramp in RAMPS:
        print(f"  {ramp.label:15s} L = {ramp.length:.4f}"
              f"   t = {ramp.total:.6f} s")
    exact = np.sqrt(R_CYC / G) * T_END
    print(f"  cicloide exacta  sqrt(r/g)*T = {exact:.6f} s"
          f"   (error {abs(exact - CYC_RAMP.total):.2e})")
    assert CYC_RAMP.total < ARC_RAMP.total < LINE_RAMP.total, "la cicloide debe ganar"
    assert CYC_RAMP.length > ARC_RAMP.length > LINE_RAMP.length, \
        "la cicloide debe ser la mas larga"
    print("  OK: la mas larga y la mas rapida son la misma curva")

    print(f"\ntautocrona (r = {R_BOWL}):  pi*sqrt(r/g) = {TAUTO_EXACT:.6f} s")
    for drop in BOWL_DROPS:
        print(f"  suelta en t0 = {drop.t0:.2f}  ->  {drop.total:.6f} s"
              f"   (error {abs(drop.total - TAUTO_EXACT):.2e})")
    spread = max(d.total for d in BOWL_DROPS) - min(d.total for d in BOWL_DROPS)
    print(f"  dispersion entre las cuatro: {spread:.2e} s")
    assert spread < 1e-4, "los tiempos de la tautocrona deben coincidir"
    print("  OK: todas llegan al fondo a la vez")


if __name__ == "__main__":
    _verify()
