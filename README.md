<div align="center">

# 🎤 Claude Deck Generator

**Generate professional presentations from any topic using Claude AI — in seconds**

[![Version](https://img.shields.io/badge/version-4.6.1-6366f1?style=flat-square)](https://github.com/Moodswing9/claude-deck-generator/releases)
[![License](https://img.shields.io/badge/license-MIT-22c55e?style=flat-square)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/Moodswing9/claude-deck-generator/ci.yml?branch=main&style=flat-square&label=CI)](https://github.com/Moodswing9/claude-deck-generator/actions/workflows/ci.yml)
[![Powered by Claude](https://img.shields.io/badge/powered%20by-Claude%20Opus%204.7-f59e0b?style=flat-square)](#)
[![Output](https://img.shields.io/badge/output-PPTX%20%7C%20HTML-22c55e?style=flat-square)](#usage)
[![NVIDIA NIM](https://img.shields.io/badge/NVIDIA-NIM-76b900?style=flat-square)](#provider-claude--or--nvidia-nim)

</div>

---

<div align="center">

![AI Presentation Generator — pitch deck output, dark corporate theme](docs/screenshot.png)

</div>

---

## Overview

Provide a topic, choose a theme, and get a polished `.pptx` or `.html` presentation — complete with structured slides and speaker notes. Backed by **Claude Opus 4.7** by default, with an alternate provider path through **NVIDIA NIM** (Writer Palmyra-Creative-122B). Supports remixing existing decks, controlling slide count, and embedding Unsplash photos.

---

## Claude Code Plugin

Install as a Claude Code plugin to get `/deck` and `/deck-remix` slash commands directly in your terminal:

From a terminal:

```bash
claude plugin marketplace add Moodswing9/claude-plugins
claude plugin install deck-generator@moodswing9
```

This installs `/deck`, `/deck-remix` and the skill.

Or inside Claude Code: `/plugin marketplace add Moodswing9/claude-plugins`, then `/plugin install deck-generator@moodswing9`.

Only need the knowledge skill, without the slash commands? `npx skills add Moodswing9/claude-deck-generator -g` installs just the skill.

| Command | What it does |
|:---|:---|
| `/deck "Your Topic"` | Generate a new deck — theme, format, and slide count auto-suggested from context |
| `/deck "Topic" --draft` | Preview outline + cost with Haiku, then press Enter in your terminal to upscale to Opus |
| `/deck-remix old.pptx` | Rebuild an existing deck with fresh structure |
| `/deck-remix old.pptx --vision` | Remix with Phi-4 + DePlot vision pass — describes images and extracts chart tables before regeneration |

The skill applies judgment automatically: it suggests the right theme for your audience, flags when draft mode makes sense (large or complex decks), and warns when vision mode would add value.

---

## Setup

```bash
pip install -r requirements.txt

# Default provider (Claude)
export ANTHROPIC_API_KEY=sk-ant-...

# Alternate provider (NVIDIA NIM — used with --provider nvidia)
export NVIDIA_API_KEY=nvapi-...

# Optional — enables Unsplash photos (--images flag)
export UNSPLASH_ACCESS_KEY=your-unsplash-access-key
```

---

## Usage

```bash
python generate.py "Your Topic"
```

### Options

| Flag | Default | Description |
|:---|:---:|:---|
| `--theme` | `dark` | Color theme: `dark` · `light` · `corporate` · `executive` |
| `--format` | `pptx` | Output format: `pptx` or `html` |
| `--output` | auto | Output file path |
| `--slides N` | `12` | Number of slides to generate (4 – 20) |
| `--provider` | `anthropic` | Content provider: `anthropic` (Claude) or `nvidia` (Palmyra-Creative-122B via NIM) |
| `--draft` | off | Two-phase mode: Haiku previews the slide outline + cost estimate; press Enter to upscale to Opus |
| `--remix FILE` | — | Remix an existing `.pptx` — provider rebuilds it with new structure |
| `--vision` | off | With `--remix`: run Phi-4 + DePlot on every embedded image in parallel (requires `NVIDIA_API_KEY`) |
| `--no-notes` | off | Omit speaker notes from the output |
| `--images` | off | Embed Unsplash photos (requires `UNSPLASH_ACCESS_KEY`) |
| `--list-themes` | — | List available themes and exit |

### Examples

```bash
# Default: dark theme, pptx output
python generate.py "Heavy Metal Music History"

# HTML output with corporate theme
python generate.py "Q4 Business Review" --format html --theme corporate

# Light theme with custom filename
python generate.py "Machine Learning" --theme light --output ml.pptx

# Control slide count
python generate.py "Q4 Business Review" --slides 8

# Draft mode — Haiku previews structure + cost, Enter to upscale to Opus
python generate.py "Q4 Business Review" --draft

# Remix an existing deck (text only)
python generate.py "Q4 Business Review" --remix old_deck.pptx

# Remix WITH vision — Phi-4 + DePlot run on all images in parallel
python generate.py "Q4 Business Review" --remix old_deck.pptx --vision

# No speaker notes
python generate.py "Product Roadmap" --no-notes
```

---

## Themes

| Theme | Description |
|:---|:---|
| 🌑 `dark` | Dark background with light text — default |
| ☀️ `light` | Light background with dark text |
| 🏢 `corporate` | Professional blue / slate palette |
| 👔 `executive` | Warm off-white background with gold accent — boardroom ready |

---

## How It Works

1. The selected provider (**Claude Opus 4.7** or **Writer Palmyra-Creative-122B** via NVIDIA NIM) generates structured slide content — titles, bullets, speaker notes
2. Content is rendered into your chosen format and theme

---

## Provider: Claude *or* NVIDIA NIM

The CLI supports two interchangeable content providers via `--provider`. Both produce the same downstream JSON, so the renderer (`build_pptx()` / `build_html()`) is unchanged across providers.

| Provider | Model | When to use |
|:---|:---|:---|
| `anthropic` (default) | `claude-opus-4-7` with adaptive thinking + structured output | Default — best narrative quality, supports adaptive reasoning depth |
| `nvidia` | `writer/palmyra-creative-122b` via `https://integrate.api.nvidia.com/v1` | Self-hosted NIM endpoints, cost optimization, or when you want to keep the full pipeline on NVIDIA infra |

```bash
# Use Claude (default)
python generate.py "Q4 Business Review"

# Use NVIDIA NIM (Palmyra)
python generate.py "Q4 Business Review" --provider nvidia
```

### Vision-enriched remix (`--vision`)

When you remix an existing deck with `--remix old.pptx --vision`, the pipeline does **three** passes over the source:

1. **MarkItDown** extracts all text content (titles, bullets, speaker notes) → Markdown
2. **`microsoft/phi-4-multimodal-instruct`** runs on every embedded image to produce a written description of what's on the slide visually (logos, diagrams, screenshots, photos)
3. **`google/deplot`** runs on every embedded image to extract a data table, kept only if the output looks tabular (contains pipes + digits — non-charts produce noise that gets filtered out)

All three passes are concatenated into the reference markdown and handed to your chosen content provider (Claude or Palmyra), which rebuilds the deck with both textual and visual context preserved.

```bash
export NVIDIA_API_KEY=nvapi-...
python generate.py "Q4 Strategy Review" --remix old_deck.pptx --vision
```

Vision runs all images in **parallel** (`asyncio.gather` + `asyncio.to_thread`), so a 20-image deck takes ~30 seconds instead of ~4 minutes. Each image still makes two NIM calls (Phi-4 + DePlot). If your source deck is mostly text, skip `--vision` to save the round-trips entirely.

---

## Complete Presentation Suite

The [v4.0.0 release](https://github.com/Moodswing9/claude-deck-generator/releases/tag/v4.0.0) ships a full boardroom playbook alongside the generator.

### 📊 Decks

| File | Description |
|:---|:---|
| `AI_Presentation_Generator_Pitch.pptx` | 11-slide boardroom pitch with speaker notes |
| `Closing_Slide.pptx` | Single closing slide — white background, three numbers, one command |
| `QA_Prep_Slides.pptx` | 12-slide Q&A deck — 10 hardest questions, bridging phrases, golden rule |
| `Objection_Handling_Slides.pptx` | 9-slide deck — concede / flip / close framework for 6 objections |
| `Visual_Direction.pptx` | 12-slide design brief — one accent per slide, embodies every rule it describes |

### 📋 Playbook

| File | Description |
|:---|:---|
| `EXECUTIVE_SUMMARY.md` | 60-word Goldman Sachs-style summary — problem, solution, proof, ask |
| `PRESENTATION_BLUEPRINT.md` | Strategic narrative framework |
| `PRESENTATION_SCRIPT.md` | Word-for-word speaker script with pause marks |
| `DATA_NARRATIVE.md` | McKinsey-style data narrative — raw numbers to boardroom decisions |
| `OBJECTION_SLIDES.md` | Concede-flip-close structure for 6 common objections |
| `CLOSING_SLIDE.md` | Master closer framework with full script |
| `QA_PREP.md` | 10 hardest questions with sharp answers + 3 bridging phrases |
| `VISUAL_DIRECTION.md` | Creative direction brief — palette, typography, layouts, chart rules |

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

Built by [Moodswing9](https://github.com/Moodswing9) · [Portfolio](https://moodswing9.github.io)

</div>
