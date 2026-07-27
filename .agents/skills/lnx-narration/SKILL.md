---
name: lnx-narration
description: Add voice-over narration and burned-in subtitles to an Lnx Manim animation, synchronize words with animation beats, and keep captions inside the vertical TikTok safe area. Use for voice-over, narration, subtitles, captions, or converting a silent animation into a narrated video.
---

# Lnx Narration and Subtitles

Burned-in subtitles are mandatory because many viewers watch without sound.
Also load `lnx-design` for color, typography, and safe-area rules, and `lnx-video` for narrative structure.

## Architecture

`animation/lnx/voice.py` wraps [manim-voiceover](https://github.com/ManimCommunity/manim-voiceover).
Select the voice engine through `voice.engine` in `lnx.yaml`; scene code must remain engine-independent.

| Engine | Cost | Requirement |
|---|---|---|
| `gtts` | Free | None; default engine |
| `openai` | Paid | `OPENAI_API_KEY` |
| `elevenlabs` | Freemium | `ELEVEN_API_KEY` |
| `azure` | Free tier | Azure credentials |
| `recorder` | Free | Microphone; records in blocks |

Enable `voice.transcribe: true` to use Whisper word-level alignment.

## Write a narrated scene

Inherit from `LnxVoiceScene` instead of `Scene`.
The public runtime currently exposes the legacy methods `preparar()` and `decir()`.
Preserve these API identifiers until compatible English aliases exist.

```python
from manim import *
from lnx import *


class ExampleVideo(LnxVoiceScene):
    def construct(self):
        self.preparar()

        formula = MathTex(
            r"\sum_{n=1}^{\infty}\frac{1}{2^n}=1",
            font_size=90,
        )

        with self.decir("Add infinitely many numbers and still obtain one."):
            self.play(Write(formula))

        with self.decir("This is a geometric series."):
            self.play(Indicate(formula, color=ACCENT_YELLOW))

        animate_End(scene=self)
```

Rules:

- Make each animation block last as long as its narration.
- Do not add `self.wait()` inside a narration block; manim-voiceover handles remaining time.
- Use `self.decir("spoken text", "ON-SCREEN TEXT")` when narration and captions differ.
- Keep one idea per block and use sentences of 6-14 words.

### Synchronize to a word

```python
with self.decir(
    "With only <bookmark mark='key'/>twenty-three people, "
    "the probability exceeds fifty percent."
):
    self.play(FadeIn(people))
    self.wait_until_bookmark("key")
    self.play(Indicate(number_23, color=ACCENT_YELLOW))
```

This requires `voice.transcribe: true` in `lnx.yaml`.

## Subtitles

Generate subtitles from the narrated text and configure them under `subtitles` in `lnx.yaml`.
The configuration key `max_chars_por_linea` is a compatibility contract; do not rename it until the runtime schema changes.

The runtime already handles:

- Multi-line wrapping without splitting words.
- A dark stroke behind the glyph fill.
- Placement around `y = -5.0`, above TikTok controls.

Disable captions for one video with `subtitles.enabled: false`.

## Write for listening

- Never read raw LaTeX commands aloud.
- Use short declarative sentences.
- Show digits on screen but spell numbers in narration.
- Narrate the hook during the first two seconds.

## Render

```bash
.venv/Scripts/lnx.exe <slug>
```

Voice-over audio is cached in `media/voiceovers/`.
The TTS provider is called again only when narration text changes.
SoX is optional and supports time-stretching when audio must match a fixed duration.

## Checklist

- [ ] Every narration block contains animation rather than dead time.
- [ ] No sentence exceeds about 14 words.
- [ ] Narration never reads literal LaTeX.
- [ ] Captions do not cover important content in a real frame.
- [ ] The video narrates its hook immediately.
- [ ] The final MP4 contains an audio stream.
