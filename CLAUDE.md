# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the generator
python generate.py "Your Topic"
python generate.py "Your Topic" --theme corporate --format html
python generate.py "Your Topic" --images             # embed Unsplash photos
python generate.py "Your Topic" --remix old.pptx    # remix an existing deck via MarkItDown
python generate.py "Your Topic" --slides 8          # control slide count (4–20, default 12)
python generate.py "Your Topic" --no-notes          # omit speaker notes
python generate.py --list-themes

# Required environment variable
export ANTHROPIC_API_KEY=sk-ant-...

# Optional — enables --images flag
export UNSPLASH_ACCESS_KEY=your-unsplash-access-key
```

## Architecture

The core generation lives in `generate.py`, which is also imported by `app.py` (Streamlit web UI) and `healthcheck.py`. The `build_*.py` files are standalone one-off deck builders.

**Data flow:** CLI args → `generate_content()` (Claude API) → `build_pptx()` or `build_html()` → file on disk.

**`THEMES` dict** is the central config. Each theme entry contains two sets of keys:
- `bg`, `accent`, `text`, `subtext`, `divider` — `RGBColor` objects consumed by `build_pptx()`
- `background`, `slide_bg`, `primary`, `secondary`, `html_text`, `muted`, `border`, `code_bg`, `font_family` — hex strings consumed by `build_html()` via `_css()`

Adding a new theme means adding one dict entry with both sets of keys.

**`generate_content(topic, *, reference_markdown="", slide_count=12)`** calls `claude-opus-4-6` with `thinking: {type: "adaptive"}` and `output_config.format` set to `SLIDE_SCHEMA`. When `reference_markdown` is supplied (from `ingest_pptx()`), it is injected into the user message inside `<reference_deck>` tags and Claude rebuilds the deck from that material. `slide_count` is clamped to 4–20.

**`ingest_pptx(path)`** uses MarkItDown to convert an existing `.pptx` file into Markdown, extracting slide titles, text, tables, charts, and speaker notes. The result is passed as `reference_markdown` to `generate_content()`.

**`SLIDE_SCHEMA`** defines the structure Claude must return: `{title, subtitle, slides: [{type, title, bullets[], notes, quote?, attribution?, stat?, stat_label?}]}`. Slide types: `content`, `section`, `quote`, `stat`. The HTML builder prepends a title slide from `data["title"]`; the pptx builder calls `_pptx_title_slide()` separately.

**`build_pptx()`** uses blank slide layout (`prs.slide_layouts[6]`) for all slides and draws everything manually via `add_textbox` and `add_shape` — it does not use PowerPoint's built-in layouts/placeholders.

**`build_html()`** outputs a self-contained single HTML file. All CSS is injected inline via `_css(theme)` using CSS custom properties. The `_slide_html()` helper applies special classes to slide 1 (title) and the last slide (closing).

## Key constraints

- `ANTHROPIC_API_KEY` must be set in the environment — the tool will raise an `AuthenticationError` without it.
- Output filename is auto-derived from the topic (alphanumeric + spaces/dashes/underscores, max 40 chars) if `--output` is not specified.
- `.pptx` files are no longer gitignored — all presentation files are committed.

## Custom slide builders

One-off decks with bespoke layouts that `generate.py` can't produce:

| File | Output | Description |
|------|--------|-------------|
| `build_closing_slide.py` | `Closing_Slide.pptx` | Single closing slide — white bg, red bar, three metric rows, command block |
| `build_closing_slide_html.py` | `Closing_Slide.html` | HTML mirror of the closing slide — self-contained, no external dependencies |
| `build_objection_slides.py` | `Objection_Handling_Slides.pptx` | 9-slide objection deck — title + 6 objections (concede/flip/close) + master close + delivery principles |
| `build_objection_slides_html.py` | `Objection_Handling_Slides.html` | HTML mirror of the objection deck — self-contained, no external dependencies |
| `build_pitch_html.py` | `AI_Presentation_Generator_Pitch.html` | 11-slide pitch HTML — mirrors PRESENTATION_BLUEPRINT.md slide-for-slide, no fabricated stats |
| `build_pitch_slides.py` | `AI_Presentation_Generator_Pitch.pptx` | 11-slide pitch pptx — mirrors PRESENTATION_BLUEPRINT.md slide-for-slide, no fabricated stats |
| `build_qa_slides.py` | `QA_Prep_Slides.pptx` | 12-slide Q&A deck — numbered badge per question, bridging phrases, golden rule |
| `build_visual_direction_slides.py` | `Visual_Direction.pptx` | 12-slide design brief — dark theme, Signal Blue accent used once per slide |

Each builder is self-contained, requires only `python-pptx`, and uses `prs.slide_layouts[6]` (blank) with all elements drawn manually. No API call needed — content is hardcoded.

## Presentation assets

The repo ships a full boardroom playbook for pitching the tool itself:

| File | What it is |
|------|------------|
| `AI_Presentation_Generator_Pitch.pptx` / `.html` | 11-slide pitch deck, corporate theme |
| `Closing_Slide.pptx` | Single closing slide — white bg, three numbers, one command |
| `QA_Prep_Slides.pptx` | 12-slide Q&A deck — 10 hardest questions, bridging phrases, golden rule |
| `Objection_Handling_Slides.pptx` / `.html` | 6 objections preemptively neutralized |
| `Visual_Direction.pptx` | 12-slide design brief embodying every rule it describes |
| `opening_slide.html` | Animated terminal hook for live presentations |
| `PRESENTATION_BLUEPRINT.md` | Narrative strategy and slide rationale |
| `PRESENTATION_SCRIPT.md` | Word-for-word speaker script with pause marks |
| `DATA_NARRATIVE.md` | McKinsey-style data framework for pitching the tool |
| `EXECUTIVE_SUMMARY.md` | 60-word Goldman Sachs-style summary slide |
| `OBJECTION_SLIDES.md` | Concede-flip-close structure for 6 common objections |
| `CLOSING_SLIDE.md` | Master closer framework with full script |
| `QA_PREP.md` | 10 hardest questions with sharp answers + 3 bridging phrases |
| `VISUAL_DIRECTION.md` | Creative direction brief — palette, typography, layouts, chart rules |
