# AI Presentation Generator

Generate professional presentations from any topic using Claude AI. Outputs a styled `.pptx` or `.html` file with your choice of color theme.

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

## Usage

```bash
python generate.py "Your Topic"
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--theme` | `dark` | Color theme: `dark`, `light`, `corporate` |
| `--format` | `pptx` | Output format: `pptx` or `html` |
| `--output` | auto | Output file path |
| `--list-themes` | — | List available themes and exit |

## Examples

```bash
# Default: dark theme, pptx output
python generate.py "Heavy Metal Music History"

# HTML output with corporate theme
python generate.py "Q4 Business Review" --format html --theme corporate

# Light theme pptx with custom filename
python generate.py "Machine Learning" --theme light --output ml.pptx
```

## Themes

| Theme | Description |
|-------|-------------|
| `dark` | Dark background with light text (default) |
| `light` | Light background with dark text |
| `corporate` | Professional blue/slate palette |

## How It Works

1. Claude Opus 4.6 generates structured slide content (titles, bullets, speaker notes) for your topic
2. The content is rendered into your chosen format and theme

---

## Complete Presentation Suite

The [v3.0.0 release](https://github.com/Moodswing9/Headbanger-s-Little-Repository/releases/tag/v3.0.0) ships a full boardroom playbook alongside the tool.

### Decks

| File | What it is |
|------|------------|
| `AI_Presentation_Generator_Pitch.pptx` | 10-slide boardroom pitch, speaker notes included |
| `Closing_Slide.pptx` | Single closing slide — white background, three numbers, one command |
| `QA_Prep_Slides.pptx` | 12-slide Q&A deck — 10 hardest questions, bridging phrases, golden rule |
| `Objection_Handling_Slides.pptx` | 6 objections, preemptively neutralized |
| `Visual_Direction.pptx` | 12-slide design brief — dark theme, one accent per slide, embodies every rule it describes |

### Playbook

| File | What it is |
|------|------------|
| `EXECUTIVE_SUMMARY.md` | 60-word Goldman Sachs-style summary — problem, solution, proof, ask |
| `PRESENTATION_BLUEPRINT.md` | Strategic narrative framework |
| `PRESENTATION_SCRIPT.md` | Word-for-word speaker script with pause marks |
| `DATA_NARRATIVE.md` | McKinsey-style data narrative — raw numbers to boardroom decisions |
| `OBJECTION_SLIDES.md` | Concede-flip-close structure for 6 common objections |
| `CLOSING_SLIDE.md` | Master closer framework with full script |
| `QA_PREP.md` | 10 hardest questions with sharp answers + 3 bridging phrases |
| `VISUAL_DIRECTION.md` | Creative direction brief — palette, typography, layouts, chart rules, 3 design rules for a $10,000 deck |
| `CLAUDE.md` | Codebase guide for Claude Code |
