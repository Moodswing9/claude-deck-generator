<div align="center">

# 🎤 AI Presentation Generator

**Generate professional presentations from any topic using Claude AI — in seconds**

[![Version](https://img.shields.io/badge/version-4.1.0-6366f1?style=flat-square)](https://github.com/Moodswing9/claude-deck-generator/releases)
[![License](https://img.shields.io/badge/license-All%20Rights%20Reserved-ef4444?style=flat-square)](#license)
[![Powered by Claude](https://img.shields.io/badge/powered%20by-Claude%20AI-f59e0b?style=flat-square)](#)
[![Output](https://img.shields.io/badge/output-PPTX%20%7C%20HTML-22c55e?style=flat-square)](#usage)
[![NVIDIA NIM](https://img.shields.io/badge/NVIDIA-NIM-76b900?style=flat-square)](#provider-claude--or--nvidia-nim)

</div>

---

<div align="center">

![Sample generated deck — executive theme](docs/screenshot.png)

</div>

---

## Overview

Provide a topic, choose a theme, and get a polished `.pptx` or `.html` presentation — complete with structured slides and speaker notes. Backed by **Claude Opus 4.6** by default, with an alternate provider path through **NVIDIA NIM** (Writer Palmyra-Creative-122B). Supports remixing existing decks, controlling slide count, and embedding Unsplash photos.

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
| `--remix FILE` | — | Remix an existing `.pptx` — provider rebuilds it with new structure |
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

# Remix an existing deck
python generate.py "Q4 Business Review" --remix old_deck.pptx

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

1. The selected provider (**Claude Opus 4.6** or **Writer Palmyra-Creative-122B** via NVIDIA NIM) generates structured slide content — titles, bullets, speaker notes
2. Content is rendered into your chosen format and theme

---

## Provider: Claude *or* NVIDIA NIM

The CLI supports two interchangeable content providers via `--provider`. Both produce the same downstream JSON, so the renderer (`build_pptx()` / `build_html()`) is unchanged across providers.

| Provider | Model | When to use |
|:---|:---|:---|
| `anthropic` (default) | `claude-opus-4-6` with adaptive thinking + structured output | Default — best narrative quality, supports adaptive reasoning depth |
| `nvidia` | `writer/palmyra-creative-122b` via `https://integrate.api.nvidia.com/v1` | Self-hosted NIM endpoints, cost optimization, or when you want to keep the full pipeline on NVIDIA infra |

```bash
# Use Claude (default)
python generate.py "Q4 Business Review"

# Use NVIDIA NIM (Palmyra)
python generate.py "Q4 Business Review" --provider nvidia
```

> The repo also ships experimental utilities for `microsoft/phi-4-multimodal-instruct` (slide image analysis) and `google/deplot` (chart-to-table extraction). These are defined in `generate.py` but not yet wired into the default CLI flow — call them directly if you want to extract data from existing decks.

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

Copyright (c) 2026 Timur Poyraz. All rights reserved.

No part of this software may be reproduced, distributed, or modified in any form or by any means without express written permission from the copyright holder.

---

<div align="center">

Built by [Moodswing9](https://github.com/Moodswing9) · [Portfolio](https://moodswing9.github.io)

</div>
