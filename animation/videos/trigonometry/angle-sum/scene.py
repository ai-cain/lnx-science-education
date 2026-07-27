from manim import *
from lnx import *

# demostracion-sin-palabras | trigonometria | intermedio
# sin(a+b) = sin(a)cos(b) + cos(a)sin(b), demostrado con triangulos rectangulos
# anidados (construccion clasica), sin apoyarnos en texto explicativo largo.
#
# El frame real es 9 x 16 unidades (x en [-4.5, 4.5], y en [-8, 8]).
# Zona segura: |y| <= 5.6 y |x| <= 3.8.

SAFE_W = 7.2


def fit(m):
    if m.width > SAFE_W:
        m.scale_to_fit_width(SAFE_W)
    return m


def etiqueta(tex, font_size, color, con_fondo=True):
    """MathTex con fondo opcional para etiquetas que cruzan lineas."""
    t = MathTex(tex, font_size=font_size, color=color)
    if con_fondo:
        t.add_background_rectangle(color=BG, opacity=0.92, buff=0.06)
    # Las etiquetas siempre deben leerse por encima de la geometria.
    t.set_z_index(10)
    return t


class AngleSum(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        marca = SVGMobject(LOGO_RENDER)
        marca.width = config.frame_width * 0.14
        marca.to_corner(DR, buff=0.3)
        marca.set_opacity(0.85)
        self.add(marca)

        COLOR_A = ACCENT_CYAN      # angulo alpha / tramos "alpha"
        COLOR_B = ACCENT_MAGENTA   # angulo beta / tramos "beta"
        COLOR_HYP = ACCENT_YELLOW  # hipotenusa OP
        COLOR_AUX = GREY_B         # lineas auxiliares (perpendiculares)

        # Una suma angular menor abre la silueta: el triangulo principal deja
        # de verse como una aguja y aprovecha mejor el ancho del frame vertical.
        R = 7.0
        a = 32 * DEGREES
        b = 23 * DEGREES

        OFFSET = np.array([-3.0, -3.3, 0])
        O = ORIGIN + OFFSET
        P = R * np.array([np.cos(a + b), np.sin(a + b), 0]) + OFFSET
        H = np.array([P[0], OFFSET[1], 0])
        M = R * np.cos(b) * np.array([np.cos(a), np.sin(a), 0]) + OFFSET
        N = np.array([M[0], OFFSET[1], 0])
        K = np.array([H[0], M[1], 0])

        origen = O
        centro = (O + P + M + N + H + K) / 6

        def afuera(A, B, dist=0.4):
            """Punto medio de A-B desplazado hacia afuera de la figura (nunca hacia el centro)."""
            mid = (A + B) / 2
            d = B - A
            n = np.array([-d[1], d[0], 0])
            n = n / np.linalg.norm(n)
            if np.dot(n, mid - centro) < 0:
                n = -n
            return mid + n * dist

        # ---------------------------------------------------------- hook 0-2s
        titulo = MathTex(r"\sin(\alpha+\beta)", r"=", r"\,?\,", font_size=70)
        titulo[0].set_color(COLOR_HYP)
        titulo[2].set_color(COLOR_B)
        titulo.set_stroke(width=1)
        titulo.set_z_index(10)
        titulo.move_to(UP * 5.35)
        fit(titulo)
        self.play(Write(titulo), run_time=0.9)
        self.wait(0.3)

        # ------------------------------------------------------- construccion
        # La base termina donde termina la geometria; antes sobraba una cola
        # larga a la derecha que hacia que el triangulo pareciera mas estrecho.
        base = Line(
            O + LEFT * 0.25,
            N + RIGHT * 0.25,
            color=COLOR_AUX,
            stroke_width=2,
            stroke_opacity=0.55,
        )
        self.play(Create(base), run_time=0.6)

        rayo_a = Line(origen, M, color=COLOR_A, stroke_width=4)
        arco_a = Angle(base, rayo_a, radius=0.55, color=COLOR_A)
        etq_a = etiqueta(r"\alpha", 36, COLOR_A, con_fondo=False).move_to(
            Angle(base, rayo_a, radius=0.9).point_from_proportion(0.5)
        )
        self.play(Create(rayo_a), Create(arco_a), Write(etq_a), run_time=0.7)
        self.wait(0.2)

        hip = Line(origen, P, color=COLOR_HYP, stroke_width=6)
        arco_b = Angle(rayo_a, hip, radius=0.9, color=COLOR_B)
        etq_b = etiqueta(r"\beta", 36, COLOR_B, con_fondo=False).move_to(
            Angle(rayo_a, hip, radius=1.25).point_from_proportion(0.5)
        )
        self.play(Create(hip), Create(arco_b), Write(etq_b), run_time=0.8)

        etq_op = etiqueta("1", 34, WHITE).move_to(afuera(origen, P, 0.4))
        self.play(FadeIn(etq_op), run_time=0.4)
        self.wait(0.4)

        def escuadra(vertice, hacia1, hacia2, length=0.15):
            """Marca de 90 grados: las dos lineas SIEMPRE apuntan desde el
            vertice hacia afuera (nunca al reves), para que la escuadra caiga
            del lado correcto del angulo."""
            return RightAngle(
                Line(vertice, hacia1), Line(vertice, hacia2),
                length=length, color=WHITE, stroke_width=2,
            )

        # ---- triangulo 1: O-M-P (hipotenusa 1, cateto adyacente cos(b),
        # cateto opuesto sin(b)) — se completa entero antes de seguir.
        punto_m = Dot(M, color=WHITE, radius=0.06)
        perp_pm = DashedLine(P, M, color=COLOR_AUX, stroke_width=2)
        angulo_m = escuadra(M, origen, P)
        self.play(FadeIn(punto_m), Create(perp_pm), Create(angulo_m), run_time=0.6)

        etq_om = etiqueta(r"\cos\beta", 28, COLOR_A).move_to(afuera(origen, M, 0.4))
        etq_mp = etiqueta(r"\sin\beta", 30, COLOR_B).move_to(afuera(M, P, 0.45))
        self.play(Write(etq_om), run_time=0.5)
        self.play(Write(etq_mp), run_time=0.5)
        self.wait(0.4)

        # ---- triangulo 2: O-N-M (hipotenusa cos(b), cateto opuesto cos(b)sin(a))
        punto_n = Dot(N, color=WHITE, radius=0.06)
        perp_mn = DashedLine(M, N, color=COLOR_AUX, stroke_width=2)
        angulo_n = escuadra(N, origen, M)
        self.play(FadeIn(punto_n), Create(perp_mn), Create(angulo_n), run_time=0.6)
        zona_alpha = Polygon(
            origen, N, M,
            fill_color=COLOR_A,
            fill_opacity=0.08,
            stroke_width=0,
        )
        self.play(FadeIn(zona_alpha), run_time=0.25)
        self.bring_to_back(zona_alpha)
        etq_mn = etiqueta(r"\cos\beta\sin\alpha", 26, COLOR_A).move_to(afuera(M, N, 0.55))
        self.play(Write(etq_mn), run_time=0.6)
        self.wait(0.4)

        # ---- triangulo 3: M-K-P (hipotenusa sin(b), cateto opuesto sin(b)cos(a))
        punto_k = Dot(K, color=WHITE, radius=0.06)
        perp_mk = DashedLine(M, K, color=COLOR_AUX, stroke_width=2)
        angulo_k = escuadra(K, M, P)
        self.play(FadeIn(punto_k), Create(perp_mk), Create(angulo_k), run_time=0.6)
        zona_beta = Polygon(
            M, K, P,
            fill_color=COLOR_B,
            fill_opacity=0.05,
            stroke_width=0,
        )
        self.play(FadeIn(zona_beta), run_time=0.25)
        self.bring_to_back(zona_beta)

        # de donde sale sin(b)cos(a) y sin(b)sin(a): en M se repite el angulo
        # alpha (alterno interno entre M->K, paralela a la base, y M->P).
        arco_alpha2 = Angle(Line(M, K), Line(M, P), radius=0.4, color=COLOR_A, other_angle=True)
        etq_alpha2 = etiqueta(r"\alpha", 24, COLOR_A, con_fondo=False).move_to(
            Angle(Line(M, K), Line(M, P), radius=0.62, other_angle=True).point_from_proportion(0.5)
        )
        self.play(Create(arco_alpha2), Write(etq_alpha2), run_time=0.6)
        self.wait(0.6)


        # ---- ahora si, la perpendicular que arma lo que queremos demostrar:
        # sin(a+b) = P->H, partido en K->P (arriba, = sin(b)cos(a)) y H->K
        # (abajo, = cos(b)sin(a), ya mostrado como M->N). Solo se dibuja el
        # tramo de arriba: el de abajo ya esta representado por M->N.
        perp_ph = DashedLine(P, K, color=COLOR_AUX, stroke_width=2)
        punto_h = Dot(H, color=WHITE, radius=0.06)
        angulo_h = escuadra(H, origen, P)
        self.play(Create(perp_ph), FadeIn(punto_h), Create(angulo_h), run_time=0.6)
        self.wait(0.5)

        # a la derecha del segmento K-P (nunca a la izquierda: ahi pasa la
        # hipotenusa amarilla y se confunde con su etiqueta)
        etq_kp = etiqueta(r"\sin\beta\cos\alpha", 24, COLOR_B).move_to(
            K + (P - K) * 0.35 + RIGHT * 0.38
        )
        self.play(Write(etq_kp), run_time=0.6)
        self.wait(0.6)

        # ------------------------------------------------------- ensamblar
        # El triangulo O-H-P es el resultado geometrico: al ensamblarlo se
        # apagan los rellenos parciales y queda un unico fondo amarillo.
        triangulo_grande = Polygon(
            origen, H, P,
            fill_color=COLOR_HYP,
            fill_opacity=0.10,
            stroke_width=0,
        )
        self.play(
            FadeOut(zona_alpha),
            FadeOut(zona_beta),
            FadeIn(triangulo_grande),
            run_time=0.5,
        )
        self.bring_to_back(triangulo_grande)

        # Cierra O-H en amarillo sin recolorear toda la base auxiliar.
        segmento_oh = Line(origen, H, color=COLOR_HYP, stroke_width=6)
        segmento_oh.set_z_index(5)
        self.play(Create(segmento_oh), run_time=0.5)

        # PH es el resultado que estamos ensamblando: amarillo como la hipotenusa.
        segmento_ph = Line(H, P, color=COLOR_HYP, stroke_width=6)
        segmento_ph.set_z_index(5)
        self.play(Indicate(segmento_ph, scale_factor=1.0), run_time=0.8)
        self.wait(0.3)

        formula = MathTex(
            r"\sin(\alpha+\beta)", r"=",
            r"\sin\beta\cos\alpha", r"+", r"\cos\beta\sin\alpha",
            font_size=42,
        )
        formula[2].set_color(COLOR_B)
        formula[4].set_color(COLOR_A)
        formula[0].set_color(COLOR_HYP)
        formula.set_stroke(width=1)
        formula.set_z_index(21)
        formula.move_to(DOWN * 5.25)
        fit(formula)

        # nada se escribe de cero: todo baja como copia de lo que ya esta en pantalla.
        # "sin(a+b)" viene del titulo de arriba; cada termino viene de su etiqueta
        # en el dibujo (etq_kp -> sin(b)cos(a), etq_mn -> cos(b)sin(a)).
        self.play(FadeOut(titulo[1]), FadeOut(titulo[2]), run_time=0.4)
        self.play(TransformFromCopy(titulo[0], formula[0]), run_time=1.0)
        self.play(Write(formula[1]), run_time=0.3)
        self.play(TransformFromCopy(etq_kp[1], formula[2]), run_time=0.9)
        self.play(Write(formula[3]), run_time=0.3)
        self.play(TransformFromCopy(etq_mn[1], formula[4]), run_time=0.9)
        self.wait(1.2)

        caja = SurroundingRectangle(formula, buff=0.18, corner_radius=0.12)
        caja.set_stroke(width=4, color=[YELLOW, ORANGE])
        caja.set_z_index(20)
        self.play(Create(caja), run_time=0.7)
        self.wait(1.6)

        animate_End(scene=self)
