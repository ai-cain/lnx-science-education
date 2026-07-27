---
name: lnx-video
description: Create an Lnx mathematics or physics educational video end to end: choose a narrative archetype, write beat-based pacing, implement the Manim scene in animation/videos/<topic>/<slug>/scene.py, and render it vertically for TikTok. Use whenever creating, scripting, or rendering a new basic, viral, university, or graduate-level animation.
---

# Lnx Video Production

Follow this seven-stage pipeline. Do not skip stages or write Python before stage 4.
Also load `lnx-design` for color, typography, layout, and safe-area rules.

## Stage 0 — Preflight

```bash
.venv/Scripts/lnx.exe list
```

Review existing video folders and record covered topics and treatments to avoid repetition.

## Stage 1 — Input gate

Use values supplied by the user. Otherwise apply these defaults and inform the user:

| Field | Default |
|---|---|
| `topic` | The least-covered catalog topic |
| `level` | `basic` |
| `format` | `vertical` |

Levels: `basic`, `intermediate`, and `advanced`.

## Stage 2 — Choose an archetype before the topic

| Archetype | Purpose | Typical level |
|---|---|---|
| `paradox` | Contradict intuition | Basic |
| `your-teacher-lied` | Correct a badly taught shortcut | Basic |
| `proof-without-words` | Deliver a purely visual proof | Basic |
| `visual-hook` | Open with an impossible-looking animation | Basic |
| `scale-comparison` | Make extreme magnitudes understandable | Basic |
| `geometric-limit` | Show an infinite process converging | Intermediate |
| `visual-derivation` | Reveal where a formula comes from | Intermediate |
| `worked-problem` | Solve one concrete problem step by step | Intermediate |
| `counterexample` | Break a plausible conjecture | Advanced |
| `unexpected-extension` | Generalize beyond the expected domain | Advanced |
| `two-paths-one-result` | Converge through independent proofs | Advanced |
| `hidden-invariant` | Reveal an unexpected conserved quantity | Advanced |

Do not repeat any of the last three archetypes or the immediately previous topic.

## Stage 3 — Beat script preview

Present this preview before writing Python:

```text
Archetype: <archetype>
Topic:     <topic> / <level>
Hook:      "<first-two-seconds image or line>"
Duration:  <total>s

BEATS
0.0-2.0  hook   <screen action>  -> <Manim class or animation>
2.0-8.0  setup  ...              -> ...
```

Hard rules:

- The hook occupies 0.0-2.0 seconds.
- No beat lasts more than six seconds without a substantial visual change.
- Cover exactly one concept per video.
- Target 30-45 seconds for basic videos and 60-90 seconds for intermediate or advanced videos.
- End with a framed payoff followed by `animate_End(scene=self)`.

## Stage 4 — Load only required recipes

Read only examples relevant to the approved beats:

- Equation transformations: `TransformMatchingTex`.
- Functions and areas: `Axes`, `plot`, and `get_area`.
- 3D scenes: `ThreeDScene`.
- Camera motion: `MovingCameraScene`.
- Minimal structure: `animation/videos/_template/example/scene.py`.

The shared API lives in `animation/lnx/`: `backgroundLnx`, `MathPazoKpTemplate`, `BoxAnimation`, `SmartMathTex`, `logo_handler`, `animate_End`, `grillado`, `vertical`, `BG`, `ACCENT_*`, `GRADIENT_*`, and `LOGO_*`.
Preserve legacy public API identifiers until the runtime provides compatible English aliases.

## Stage 5 — Implement the video

Create one file: `animation/videos/<topic>/<slug>/scene.py`.
The CLI discovers videos automatically; do not create a separate catalog entry.
Use an existing topic directory such as `calculus`, `algebra`, `geometry`, `trigonometry`, `physics`, `probability`, or `problems`.

```python
from manim import *
from lnx import *

# <archetype> | <topic> | <level>


class ExampleScene(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        # Implement approved beats here.

        animate_End(scene=self)
```

Use shared `lnx` constants instead of hard-coded colors or asset paths.
Write every identifier, comment, docstring, and technical artifact in English.

### Geometric constructions

- Label every visible support segment.
- Place length labels outside the figure rather than inside or over another line.
- Compute the outward normal from the figure center:

```python
center = (A + B + C) / 3


def outside_segment(P1, P2, distance=0.4):
    midpoint = (P1 + P2) / 2
    direction = P2 - P1
    normal = np.array([-direction[1], direction[0], 0]) / np.linalg.norm(direction)
    if np.dot(normal, midpoint - center) < 0:
        normal = -normal
    return midpoint + normal * distance
```

- Mark every right angle with `RightAngle(..., color=WHITE)`.
- Put text above geometry with explicit `z_index` values.
- Add a solid `BG` background only when a label crosses a colored line or loses contrast.
- Do not add background boxes automatically to isolated angle labels.

## Stage 6 — Render

```bash
.venv/Scripts/lnx.exe render <slug>
.venv/Scripts/lnx.exe render <slug> -q high
```

The CLI reads resolution and frame rate from `lnx.yaml`.

## Stage 7 — Quality checklist

- [ ] The hook appears before second two.
- [ ] No beat exceeds six seconds without visual change.
- [ ] Essential text uses `font_size >= 28`.
- [ ] Important content avoids the top and bottom 15% UI zones.
- [ ] No mobject leaves the frame or overlaps unintentionally.
- [ ] The scene uses `BG`, `MathPazoKpTemplate`, and `animate_End`.
- [ ] Colors and timing use project configuration and shared constants.
- [ ] The archetype differs from the last three videos.
- [ ] The video covers one concept.
- [ ] `lnx list` discovers the video and `lnx render <slug>` completes successfully.
