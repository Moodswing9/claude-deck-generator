# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the generator
python generate.py "Your Topic"
python generate.py "Your Topic" --theme corporate --format html
python generate.py --list-themes

# Required environment variable
export ANTHROPIC_API_KEY=sk-ant-...
```

## Architecture

The entire tool lives in a single file: `generate.py`.

**Data flow:** CLI args → `generate_content()` (Claude API) → `build_pptx()` or `build_html()` → file on disk.

**`THEMES` dict** is the central config. Each theme entry contains two sets of keys:
- `bg`, `accent`, `text`, `subtext`, `divider` — `RGBColor` objects consumed by `build_pptx()`
- `background`, `slide_bg`, `primary`, `secondary`, `html_text`, `muted`, `border`, `code_bg`, `font_family` — hex strings consumed by `build_html()` via `_css()`

Adding a new theme means adding one dict entry with both sets of keys.

**`generate_content()`** calls `claude-opus-4-6` with `thinking: {type: "adaptive"}` and `output_config.format` set to `SLIDE_SCHEMA` (a JSON schema). The response is guaranteed to be valid JSON matching the schema — parse the first `text` block directly with `json.loads()`.

**`SLIDE_SCHEMA`** defines the structure Claude must return: `{title, slides: [{title, bullets[], notes}]}`. The first slide in `data["slides"]` is slide 2 (the HTML builder prepends a title slide from `data["title"]`); the pptx builder calls `_pptx_title_slide()` separately.

**`build_pptx()`** uses blank slide layout (`prs.slide_layouts[6]`) for all slides and draws everything manually via `add_textbox` and `add_shape` — it does not use PowerPoint's built-in layouts/placeholders.

**`build_html()`** outputs a self-contained single HTML file. All CSS is injected inline via `_css(theme)` using CSS custom properties. The `_slide_html()` helper applies special classes to slide 1 (title) and the last slide (closing).

## Key constraints

- `ANTHROPIC_API_KEY` must be set in the environment — the tool will raise an `AuthenticationError` without it.
- Output filename is auto-derived from the topic (alphanumeric + spaces/dashes/underscores, max 40 chars) if `--output` is not specified.
- `.pptx` files are gitignored except `AI_Presentation_Generator_Pitch.pptx`.

## Presentation assets

The repo also contains pitch materials for the tool itself:
- `PRESENTATION_BLUEPRINT.md` — narrative strategy and slide rationale
- `PRESENTATION_SCRIPT.md` — word-for-word speaker script with pause marks
- `DATA_NARRATIVE.md` — McKinsey-style data framework for pitching the tool
- `opening_slide.html` — animated terminal hook slide for live presentations
- `AI_Presentation_Generator_Pitch.pptx` / `.html` — the actual pitch deck
