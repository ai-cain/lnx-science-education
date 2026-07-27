---
name: lnx-design
description: Apply the Lnx visual identity—official palette, gradients, MathPazo/kpfonts typography, vertical 9:16 TikTok layout, safe areas, and scene structure—when creating or editing Manim animations or LaTeX documents that use template/Lnx*.sty.
---

# Lnx Visual Identity

Apply these rules to every Lnx Manim animation and LaTeX document.
Values marked **proposed** are not defined in the repository; use them only after informing the user.

## 1. Official palette

| Role | Value | Usage |
|---|---|---|
| Base background | `#111111` | The only scene background. Always call `backgroundLnx(self)`. |
| Surface | `#1f1f1f` | `BoxAnimation`, panels, and emphasis boxes. |
| Primary accent | `#00F5FF` | Main objects, curves, and geometric figures. |
| Secondary accent | `#FF00F5` | Contrast with cyan and the second endpoint of a gradient. |
| Key highlight | `#FFEE00` / `YELLOW` | Results, manipulated terms, and titles. |
| Warm highlight | `ORANGE` / `#FF8C00` | Yellow gradient pair and box borders. |
| Purple accent | `#9D00FF` | Gradient endpoint, special cases, or area fills only. |
| Brand gold | `GOLD` / `#FFD700` | Final `BoxAnimation` borders and brand titles. |
| Error | `#ff1744` | Errors, intersections, and warning tracers. |
| Correct | `GREEN` | Validated results. |
| Primary text | `WHITE` | Neutral text and structural symbols. |
| Secondary text | `#E0E0E0` | Notes and secondary captions; use sparingly. |

Contrast requirements on `#111111`:

- Cyan, yellow, gold, white, and green are safe for normal text.
- Use magenta only for thick strokes (`stroke_width >= 4`) or large text.
- Never use solid purple for text; use it only as a gradient endpoint or area fill.
- Use `#ff1744`, `RED_A`, or `RED_B` instead of pure `RED` for text.
- Never use dark gray text on the background or introduce a light scene background.

## 2. Gradients

Use only established combinations:

- `[#00F5FF, #FF00F5]` for the primary geometric figure.
- `[#FFEE00, #9D00FF]` for a highlighted final formula or result.
- `[YELLOW, ORANGE]` for the final logo and brand outlines. Never change this signature gradient.
- `[YELLOW, #FF8C00, ORANGE]` for warm boxes and figure borders.
- `[#FFD700, #FFA500]` for titles.
- `[BLUE, YELLOW, PURPLE]` for area fills with `fill_opacity=0.3-0.5`.

Do not use gradients for:

- Long explanatory text, small labels, or structural symbols.
- Axes, grids, or support geometry.
- Semantic states such as correct/incorrect or separate functions.
- More than one active focal element in the same visual moment.

## 3. Typography

- Set `self.camera.tex_template = MathPazoKpTemplate()` at the start of `construct`.
- Keep the existing `mathpazo`, `kpfonts[nomath]`, `fontenc T1`, `babel spanish`, and `amsmath` preamble.
- Use `MathTex` for mathematics and `Tex` for natural-language text that needs LaTeX accents.
- Use `Text` only when a non-LaTeX font is necessary.
- Use `SmartMathTex(tex, target_width, target_height)` to fit formulas into a target box.
- Add `set_stroke(width=1)` to `1.2` to key titles and formulas for mobile readability.

## 4. Standard scene structure

```python
from manim import *
from LnxScene import (
    backgroundLnx,
    MathPazoKpTemplate,
    SmartMathTex,
    BoxAnimation,
    animate_End,
)


class ExampleScene(Scene):
    def construct(self):
        backgroundLnx(self)
        self.camera.tex_template = MathPazoKpTemplate()

        watermark = ImageMobject("logo.png").scale(0.16).shift(DOWN * 3.2)
        self.add(watermark)

        # Hook -> development -> payoff

        animate_End(scene=self, svg_path="logo.svg")
```

Rules:

- Place the watermark at `DOWN * 3.2` or in a bottom corner without covering formulas.
- End every scene with `animate_End`.
- Run from the script directory when using relative `logo.png` or `logo.svg` paths.

## 5. Vertical TikTok format

- Render at 1080x1920 with a 9:16 frame.
- Keep essential content inside `|y| <= 5.6` and `|x| <= 3.8`.
- Leave at least 0.5 horizontal units of margin.
- Avoid important content in the lower-right area occupied by TikTok controls.
- Use `font_size >= 28` for essential text and `>= 20` only for temporary local labels.
- Target 25-40 seconds; remain within 15-60 seconds unless the topic requires more depth.
- Show the hook during the first two seconds. Never open with a logo or static title card.

## 6. Animation pacing

- Formula `Write` and `Create`: 0.2-0.5 seconds.
- Main transformations: about 1 second.
- Supporting motion: 0.1-0.5 seconds.
- Reading pauses: 0.5-1 second; never exceed 2 seconds for a static frame.
- Group simultaneous actions in one `self.play(...)` call.
- Accelerate repeated visual patterns progressively.

## 7. Completion checklist

1. `backgroundLnx(self)` is present and no second background exists.
2. `MathPazoKpTemplate()` is configured.
3. Every color comes from the official palette.
4. At most one focal gradient is active at a time.
5. No solid purple text appears.
6. Essential content stays inside the safe area.
7. Essential text uses `font_size >= 28`.
8. The hook appears within two seconds.
9. No static pause exceeds two seconds.
10. The watermark remains visible and `animate_End(...)` is the final scene action.
11. Review a vertical render at mobile scale before delivery.
12. Natural-language text renders accents correctly through LaTeX and Babel.
