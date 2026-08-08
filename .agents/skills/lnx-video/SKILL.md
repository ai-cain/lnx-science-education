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

### Discovery and validation references

- Use [MathWorld's Quadrilaterals index](https://mathworld.wolfram.com/topics/Quadrilaterals.html) as an elegant discovery catalog for geometric video ideas.
- Treat indexes as ideation aids, not theorem sources. Before implementation, validate every formula, hypothesis, and sign convention against the specific theorem page; for example, use [Descartes Circle Theorem](https://mathworld.wolfram.com/DescartesCircleTheorem.html) for a Descartes-circle video.

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
For Spanish visible text, use `circunferencia` for a stroke, locus, tangency, or curvature; use `círculo` only for a filled disk, planar region, or area. Keep the Manim API name `Circle`.

### Geometric constructions

- Label every visible support segment.
- Place length labels outside the figure rather than inside or over another line.
- For tangent circles, calculate each tangency point from the centers and radii;
  mark it with exactly one small solid `Dot` and validate that it lies on both
  circumferences. Never combine a ring and a dot for one tangency point. Keep
  tangency dots small, slightly subdued, and secondary to the construction
  (`radius` around `0.035`, opacity around `0.8`); do not animate them with
  dramatic scaling or individual flashes.
- Never pose a geometric unknown without keeping the exact target object
  visible throughout its derivation. Mark it with `?`, keep its label or leader
  aligned whenever the construction moves, and transform that same object
  directly into the solved result instead of removing it and drawing a
  replacement later.
- Treat a focal zoom as a camera operation: keep the target geometry fixed in
  center and size, animate only `self.camera.frame`, then restore the camera.
  Never simulate a zoom with `GrowFromCenter`, a scaling `Indicate`, or a
  replacement target.
- When introducing a small unknown, zoom the complete scene toward that
  unchanged target and restore the baseline camera before revealing the
  method. Save the camera state before every independent zoom/restore cycle.
- State the exact task before introducing the method or theorem: identify the
  target object, name the requested quantity (for example, radius rather than
  merely “the circle”), pause for recognition, and only then reveal formulas.
- Make payoff copy name the mathematical relation that was proved (for
  example, “tangent to all three”), not a vague spatial impression such as
  “fills the gap” or “fills the empty space.”
- Explain the semantics of every parameter in a generalized formula. Never
  confuse dimension with the number of visible objects; build a large
  configuration by repeatedly applying the correct local relation (for
  example, an 8-circle planar Descartes packing repeats the four-circle
  relation with `n=2`, not `n=8`).
  For Descartes' generalization, `n=3` means tangent spheres in 3D, not more
  planar circles; do not switch to a sphere challenge unless the scene is
  designed as a genuine 3D construction.
- In vertical final challenges, give the top stack enough air: separate title,
  formula, parameter note, local-rule note, and prompt with visible vertical
  gaps; if needed, slightly reduce formula size and move the construction down
  instead of compressing the header.
- Do not place labels for tiny adjacent objects directly inside the contact
  cluster. Put secondary labels outside with short leader lines, staggered
  vertically, and keep the primary unknown label visually dominant.
- Show dense local markers only during the relevant zoom, then remove them
  before returning to the complete construction.
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

## Stage 8 — Persist key learnings

Before reporting completion:

1. Collect every item that will appear under `## Key Learnings`.
2. Convert each reusable learning into a concrete rule, checklist item, or
   minimal recipe in the most relevant project skill.
3. Save the same decision, bug fix, preference, or discovery to Engram.
4. Do not duplicate prose: update an existing rule when the learning refines it.

Production rules learned from visual review:

- For a focal geometric reveal, use
  `create -> wait(0.8-1.0) -> zoom -> wait(0.8-1.0) -> restore -> wait(0.8-1.0)`
  so the viewer can register both the local relation and the complete figure.
- When a result moves into an occupied header region, fade out or transform the
  previous header first. Results replace headers; they never stack over them.
- Never `Circumscribe` a group whose members are far apart vertically. It
  creates a tall meaningless rectangle; highlight the local object or the
  payoff text instead.
