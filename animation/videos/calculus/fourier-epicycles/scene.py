from manim import *
from lnx import *

# visual-hook | calculus (complex Fourier series) | intermediate
# A chain of rotating Fourier vectors draws increasingly complex closed curves.
#
# The frame is 9 x 16 units (x in [-4.5, 4.5], y in [-8, 8]).
# Safe area: |y| <= 5.6 and |x| <= 3.8.

SAMPLE_COUNT = 720
TRACE_SAMPLE_COUNT = 1440
ACTIVE_RADIUS = 2.55
ACTIVE_ORIGIN = UP * 0.35
GALLERY_Y = -4.75
SAFE_WIDTH = 7.2
FORMULA_HEADER_Y = 5.2
CHAPTER_LABEL_Y = 3.8
EPICYCLE_COLORS = (
    ACCENT_CYAN,
    ACCENT_YELLOW,
    ORANGE,
    GREEN,
)


def normalize_path(points, radius=ACTIVE_RADIUS):
    centered = np.asarray(points, dtype=np.complex128)
    centered = centered - np.mean(centered)
    extent = np.max(np.abs(centered))
    if extent == 0:
        raise ValueError("A Fourier path must contain at least two distinct points.")
    return centered * (radius / extent)


def sample_polygon(vertices, sample_count=SAMPLE_COUNT):
    vertices = np.asarray(vertices, dtype=np.complex128)
    edge_count = len(vertices)
    positions = np.linspace(0, edge_count, sample_count, endpoint=False)
    points = []
    for position in positions:
        edge_index = int(position) % edge_count
        alpha = position - int(position)
        start = vertices[edge_index]
        end = vertices[(edge_index + 1) % edge_count]
        points.append((1 - alpha) * start + alpha * end)
    return normalize_path(points)


def resample_by_arc_length(points, sample_count=SAMPLE_COUNT):
    points = np.asarray(points, dtype=np.complex128)
    closed = np.concatenate([points, points[:1]])
    segment_lengths = np.abs(np.diff(closed))
    cumulative = np.concatenate([[0.0], np.cumsum(segment_lengths)])
    total_length = cumulative[-1]

    distances = np.linspace(0, total_length, sample_count, endpoint=False)
    indices = np.searchsorted(cumulative[1:], distances, side="right")
    indices = np.clip(indices, 0, len(points) - 1)

    local_start = cumulative[indices]
    local_length = segment_lengths[indices]
    alpha = np.divide(
        distances - local_start,
        local_length,
        out=np.zeros_like(distances),
        where=local_length > 0,
    )
    return closed[indices] + alpha * (closed[indices + 1] - closed[indices])


def sample_closed_catmull_rom(control_points, sample_count=SAMPLE_COUNT):
    control_points = np.asarray(control_points, dtype=np.complex128)
    segment_count = len(control_points)
    samples_per_segment = int(np.ceil(sample_count / segment_count))
    curve = []

    for index in range(segment_count):
        point_0 = control_points[(index - 1) % segment_count]
        point_1 = control_points[index]
        point_2 = control_points[(index + 1) % segment_count]
        point_3 = control_points[(index + 2) % segment_count]
        parameter = np.linspace(
            0,
            1,
            samples_per_segment,
            endpoint=False,
        )
        parameter_2 = parameter**2
        parameter_3 = parameter**3
        segment = 0.5 * (
            2 * point_1
            + (-point_0 + point_2) * parameter
            + (
                2 * point_0
                - 5 * point_1
                + 4 * point_2
                - point_3
            )
            * parameter_2
            + (
                -point_0
                + 3 * point_1
                - 3 * point_2
                + point_3
            )
            * parameter_3
        )
        curve.extend(segment)

    curve = np.asarray(curve[:sample_count])
    return resample_by_arc_length(curve, sample_count)


def circle_path(sample_count=SAMPLE_COUNT):
    parameter = np.linspace(0, TAU, sample_count, endpoint=False)
    return normalize_path(np.exp(1j * parameter))


def square_path(sample_count=SAMPLE_COUNT):
    return sample_polygon(
        [-1 - 1j, 1 - 1j, 1 + 1j, -1 + 1j],
        sample_count,
    )


def star_path(sample_count=SAMPLE_COUNT):
    vertices = []
    for index in range(10):
        angle = -PI / 2 + index * PI / 5
        radius = 1.0 if index % 2 == 0 else 0.42
        vertices.append(radius * np.exp(1j * angle))
    return sample_polygon(vertices, sample_count)


def heart_path(sample_count=SAMPLE_COUNT):
    parameter = np.linspace(0, TAU, sample_count, endpoint=False)
    x = 16 * np.sin(parameter) ** 3
    y = (
        13 * np.cos(parameter)
        - 5 * np.cos(2 * parameter)
        - 2 * np.cos(3 * parameter)
        - np.cos(4 * parameter)
    )
    points = resample_by_arc_length(x + 1j * y, sample_count)
    return normalize_path(points)


def butterfly_path(sample_count=SAMPLE_COUNT):
    control_points = [
        0 + 0.55j,
        0.55 + 1.10j,
        1.45 + 2.35j,
        2.55 + 2.10j,
        2.45 + 0.75j,
        1.45 + 0.15j,
        2.15 - 0.55j,
        1.55 - 1.90j,
        0.55 - 1.15j,
        0 - 0.45j,
        -0.55 - 1.15j,
        -1.55 - 1.90j,
        -2.15 - 0.55j,
        -1.45 + 0.15j,
        -2.45 + 0.75j,
        -2.55 + 2.10j,
        -1.45 + 2.35j,
        -0.55 + 1.10j,
    ]
    points = sample_closed_catmull_rom(
        control_points,
        sample_count,
    )
    return normalize_path(points)


def fourier_coefficients(points, term_count):
    point_count = len(points)
    coefficients = np.fft.fft(points) / point_count
    frequencies = np.fft.fftfreq(point_count, d=1 / point_count).astype(int)

    ranked = sorted(
        zip(frequencies, coefficients),
        key=lambda item: abs(item[1]),
        reverse=True,
    )
    return ranked[:term_count]


def endpoint_from_coefficients(coefficients, phase, origin=ACTIVE_ORIGIN):
    endpoint = complex(origin[0], origin[1])
    for frequency, coefficient in coefficients:
        endpoint += coefficient * np.exp(1j * frequency * phase)
    return np.array([endpoint.real, endpoint.imag, 0.0])


def precompute_trace_points(
    coefficients,
    origin=ACTIVE_ORIGIN,
    sample_count=TRACE_SAMPLE_COUNT,
):
    phases = np.linspace(0, TAU, sample_count)
    return np.array(
        [
            endpoint_from_coefficients(coefficients, phase, origin)
            for phase in phases
        ]
    )


def make_partial_trace(trace_points, phase, color):
    progress = np.clip(phase / TAU, 0.0, 1.0)
    point_count = max(
        2,
        min(
            len(trace_points),
            int(progress * (len(trace_points) - 1)) + 2,
        ),
    )
    trace = VMobject()
    trace.set_points_as_corners(trace_points[:point_count])
    trace.set_stroke(
        color=color,
        width=5,
        opacity=1,
    )
    trace.set_z_index(8)
    return trace


def make_epicycle_chain(coefficients, phase, origin=ACTIVE_ORIGIN):
    group = VGroup()
    center = np.array(origin, dtype=float)
    last_index = max(1, len(coefficients) - 1)

    for index, (frequency, coefficient) in enumerate(coefficients):
        radius = abs(coefficient)
        depth = index / last_index
        angle = np.angle(coefficient) + frequency * phase
        endpoint = center + radius * np.array(
            [np.cos(angle), np.sin(angle), 0.0]
        )

        if radius >= 0.0008:
            circle_color = EPICYCLE_COLORS[index % len(EPICYCLE_COLORS)]
            circle = Circle(
                radius=radius,
                color=circle_color,
                stroke_width=1.8 + 1.4 * depth,
                stroke_opacity=0.38 + 0.34 * depth,
                fill_color=circle_color,
                fill_opacity=0.018,
            ).move_to(center)
            circle.set_z_index(-10)

            vector = Line(
                center,
                endpoint,
                color=WHITE,
                stroke_width=2.3 - 0.8 * depth,
                stroke_opacity=0.88 - 0.28 * depth,
            )
            vector.set_z_index(5)
            group.add(circle, vector)

        center = endpoint

    endpoint_dot = Dot(
        center,
        radius=0.075,
        color=ACCENT_YELLOW,
    )
    endpoint_dot.set_z_index(15)
    group.add(endpoint_dot)
    return group


def fit_to_safe_width(mobject):
    if mobject.width > SAFE_WIDTH:
        mobject.scale_to_fit_width(SAFE_WIDTH)
    return mobject


class FourierEpicycles(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        watermark = SVGMobject(LOGO_RENDER)
        watermark.width = config.frame_width * 0.14
        watermark.to_corner(DR, buff=0.3)
        watermark.set_opacity(0.82)
        watermark.set_z_index(30)
        self.add(watermark)

        formula_header = MathTex(
            r"z(t)=",
            r"\sum_{n=-N}^{N}",
            r"c_n e^{i n t}",
            font_size=36,
        ).move_to(UP * FORMULA_HEADER_Y)
        formula_header[0].set_color(WHITE)
        formula_header[1].set_color(ACCENT_YELLOW)
        formula_header[2].set_color(ACCENT_CYAN)
        formula_header.set_stroke(width=1)
        formula_header.set_z_index(12)
        fit_to_safe_width(formula_header)

        formula_panel = SurroundingRectangle(
            formula_header,
            buff=0.22,
            corner_radius=0.14,
            color=ACCENT_CYAN,
            fill_color=SURFACE,
            fill_opacity=0.72,
            stroke_width=1.5,
            stroke_opacity=0.48,
        )
        formula_panel.set_z_index(10)

        chapter_label = Tex(
            r"\textbf{¿Puede una fórmula dibujar un corazón?}",
            font_size=30,
            color=WHITE,
        ).move_to(UP * CHAPTER_LABEL_Y)
        chapter_label.set_stroke(width=1)
        chapter_label.set_z_index(12)
        fit_to_safe_width(chapter_label)
        header_group = VGroup(
            formula_panel,
            formula_header,
            chapter_label,
        )

        gallery_slots = {
            "circle": np.array([-2.85, GALLERY_Y, 0.0]),
            "square": np.array([-1.45, GALLERY_Y, 0.0]),
            "star": np.array([0.0, GALLERY_Y, 0.0]),
            "heart": np.array([1.45, GALLERY_Y, 0.0]),
            "butterfly": np.array([2.85, GALLERY_Y, 0.0]),
        }
        gallery = VGroup()

        # Hook: reveal the emotional result before explaining the mechanism.
        heart_trace = self.draw_with_epicycles(
            points=heart_path(),
            term_count=35,
            duration=1.35,
            label=r"\textbf{35 círculos}",
            trace_color=ACCENT_MAGENTA,
            show_title=header_group,
        )

        hook_payoff = Tex(
            r"\textbf{Sí: con círculos que giran.}",
            font_size=34,
            color=ACCENT_YELLOW,
        ).move_to(DOWN * 3.55)
        hook_payoff.set_stroke(width=1)
        fit_to_safe_width(hook_payoff)
        self.play(FadeIn(hook_payoff, shift=UP * 0.12), run_time=0.45)
        self.wait(0.45)

        self.archive_trace(
            heart_trace,
            gallery_slots["heart"],
            gallery,
        )

        origin_message = Tex(
            r"\textbf{Todo empieza con un solo giro.}",
            font_size=34,
            color=WHITE,
        ).move_to(UP * CHAPTER_LABEL_Y)
        origin_message.set_stroke(width=1)
        fit_to_safe_width(origin_message)
        self.play(
            FadeOut(hook_payoff),
            Transform(chapter_label, origin_message),
            run_time=0.65,
        )

        circle_trace = self.draw_with_epicycles(
            points=circle_path(),
            term_count=1,
            duration=2.2,
            label=r"\textbf{1 círculo}",
            trace_color=ACCENT_CYAN,
        )
        self.archive_trace(
            circle_trace,
            gallery_slots["circle"],
            gallery,
        )

        square_trace = self.draw_with_epicycles(
            points=square_path(),
            term_count=15,
            duration=3.2,
            label=r"\textbf{15 círculos}",
            trace_color=ACCENT_CYAN,
        )
        self.archive_trace(
            square_trace,
            gallery_slots["square"],
            gallery,
        )

        star_trace = self.draw_with_epicycles(
            points=star_path(),
            term_count=25,
            duration=3.4,
            label=r"\textbf{25 círculos}",
            trace_color=ACCENT_YELLOW,
        )
        self.archive_trace(
            star_trace,
            gallery_slots["star"],
            gallery,
        )

        transition_message = Tex(
            r"\textbf{Cada giro añade detalle.}",
            font_size=34,
            color=ACCENT_MAGENTA,
        ).move_to(UP * CHAPTER_LABEL_Y)
        transition_message.set_stroke(width=1)
        fit_to_safe_width(transition_message)
        self.play(
            Transform(chapter_label, transition_message),
            run_time=0.55,
        )

        butterfly_trace = self.draw_with_epicycles(
            points=butterfly_path(),
            term_count=50,
            duration=5.4,
            label=r"\textbf{50 círculos}",
            trace_color=ACCENT_CYAN,
        )

        self.archive_trace(
            butterfly_trace,
            gallery_slots["butterfly"],
            gallery,
            fade_original=False,
        )

        meaning = Tex(
            r"\textbf{Lo simple puede dibujar lo imposible.}",
            font_size=34,
            color=WHITE,
        ).move_to(DOWN * 3.55)
        meaning.set_stroke(width=1)
        fit_to_safe_width(meaning)
        meaning_box = SurroundingRectangle(
            meaning,
            buff=0.2,
            corner_radius=0.12,
        )
        meaning_box.set_stroke(
            color=[ACCENT_YELLOW, ORANGE],
            width=4,
        )

        self.play(
            FadeOut(chapter_label, shift=UP * 0.1),
            Indicate(
                formula_header,
                color=ACCENT_YELLOW,
                scale_factor=1.04,
            ),
            FadeIn(meaning, shift=UP * 0.15),
            Create(meaning_box),
            butterfly_trace.animate.set_stroke(width=6),
            run_time=1.0,
        )
        self.play(
            Indicate(
                butterfly_trace,
                color=ACCENT_YELLOW,
                scale_factor=1.015,
            ),
            run_time=0.9,
        )
        self.wait(0.7)

        question = Tex(
            r"\textbf{¿Qué debería dibujar después?}",
            font_size=34,
            color=ACCENT_YELLOW,
        ).move_to(DOWN * 3.5)
        question.set_stroke(width=1)
        fit_to_safe_width(question)

        self.play(
            FadeOut(meaning),
            FadeOut(meaning_box),
            FadeIn(question, shift=UP * 0.15),
            *[
                thumbnail.animate.set_stroke(opacity=1)
                for thumbnail in gallery
            ],
            run_time=0.75,
        )
        self.wait(1.0)

        animate_End(scene=self)

    def draw_with_epicycles(
        self,
        points,
        term_count,
        duration,
        label,
        trace_color,
        show_title=None,
    ):
        coefficients = fourier_coefficients(points, term_count)
        phase = ValueTracker(0.0)
        trace_points = precompute_trace_points(coefficients)

        chain = always_redraw(
            lambda: make_epicycle_chain(
                coefficients,
                phase.get_value(),
            )
        )
        trace = always_redraw(
            lambda: make_partial_trace(
                trace_points,
                phase.get_value(),
                trace_color,
            )
        )
        count_label = Tex(
            label,
            font_size=31,
            color=trace_color,
        ).move_to(DOWN * 3.55)
        count_label.set_stroke(width=1)

        entry_rings = VGroup(
            *[
                Circle(
                    radius=0.35 + index * 0.18,
                    color=ACCENT_YELLOW,
                    stroke_width=2,
                    stroke_opacity=0.55 - index * 0.1,
                ).move_to(ACTIVE_ORIGIN)
                for index in range(4)
            ]
        )

        entry_animations = [
            FadeIn(chain),
            FadeIn(count_label, shift=UP * 0.12),
            LaggedStart(
                *[
                    Create(ring, rate_func=there_and_back)
                    for ring in entry_rings
                ],
                lag_ratio=0.08,
            ),
        ]
        if show_title is not None:
            entry_animations.append(FadeIn(show_title, shift=UP * 0.12))

        self.add(trace)
        self.play(*entry_animations, run_time=0.55)

        self.play(
            phase.animate.set_value(TAU),
            run_time=duration,
            rate_func=linear,
        )
        trace.clear_updaters()
        chain.clear_updaters()
        self.play(
            FadeOut(chain),
            FadeOut(count_label),
            run_time=0.35,
        )
        return trace

    def archive_trace(
        self,
        trace,
        slot,
        gallery,
        fade_original=True,
    ):
        thumbnail = trace.copy()
        thumbnail.set_stroke(width=3, opacity=0.72)
        thumbnail.scale_to_fit_height(0.75)
        thumbnail.move_to(slot)
        gallery.add(thumbnail)

        if fade_original:
            self.play(
                ReplacementTransform(trace, thumbnail),
                run_time=0.55,
                rate_func=smooth,
            )
        else:
            self.play(
                TransformFromCopy(trace, thumbnail),
                run_time=0.55,
                rate_func=smooth,
            )
