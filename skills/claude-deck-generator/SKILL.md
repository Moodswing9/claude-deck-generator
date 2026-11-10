---
name: claude-deck-generator
description: AI-powered presentation generator — Claude Opus 5.5 with effort=high (full quality), Haiku draft mode (fast outline + cost preview, then upscale), or NVIDIA Palmyra. Remix existing decks with optional Phi-4 + DePlot vision pass. 4 themes, .pptx and .html output.
---

# Claude Deck Generator

AI-powered presentation generator. Produces polished `.pptx` or `.html` slide decks using Claude Opus 5.5 with adaptive thinking and `effort=high` — or Haiku for fast draft previews before upscaling.

## Trigger

Activate this skill when the user wants to:
- Generate a new presentation, deck, or slideshow
- Remix or rebuild an existing `.pptx` file
- Decide on theme, format, slide count, or provider
- Run `/deck` or `/deck-remix`

---

## Context-Aware Decision Guide

Use this to choose the right flags before running. Do not just pass the user's words through — apply judgment.

### Which theme?

| Situation | Theme |
|---|---|
| Engineering demo, developer talk, tech walkthrough | `dark` |
| Product pitch, investor deck, VC meeting | `executive` |
| Internal business review, team all-hands, OKR deck | `corporate` |
| Conference session, educational content, tutorial | `light` |
| Default when unclear | `dark` |

### How many slides?

| Context | Slides |
|---|---|
| 5-minute lightning talk | 5–7 |
| 15-minute standard talk | 10–12 |
| 30-minute deep dive | 14–16 |
| Workshop / training session | 16–20 |
| One-pager summary | 4–6 |
| Default | 12 |

### Draft mode or direct Opus?

Use `--draft` when:
- Slides ≥ 15 — expensive Opus run, worth previewing structure first
- Topic is broad or complex (architecture, research, multi-domain subject)
- User is unsure about the structure and wants to validate before committing
- User explicitly asks to "see the outline first" or "check before generating"

Run direct Opus (no `--draft`) when:
- Slides ≤ 12 and topic is well-defined
- User says "just generate it" or is in a hurry
- Remix mode (structure comes from the source deck)

**Note on draft mode in Claude Code:** `--draft` requires interactive terminal input (Enter to upscale). When invoked via `/deck`, tell the user to run the command directly in their terminal — Claude Code cannot respond to the stdin prompt.

### Vision pass on remix (`--vision`)?

Add `--vision` when the source deck contains:
- Charts or graphs that carry data (DePlot will extract the table)
- Product screenshots, architecture diagrams, or infographics (Phi-4 will describe them)
- Any slide where the visual IS the content and text alone won't capture it

Skip `--vision` when:
- Source deck is mostly text and bullet points
- User is in a hurry (vision adds ~30 s per 20 images)
- `NVIDIA_API_KEY` is not set

### Provider: Anthropic vs Haiku vs NVIDIA?

| `--provider anthropic` (default) | `--provider claude-haiku` | `--provider nvidia` |
|---|---|---|
| Best narrative quality, Opus 5.5 + adaptive thinking + effort=high | Fast, cheap — Haiku 5.5, thinking off | Lower cost per run, NVIDIA infra |
| Structured output via SLIDE_SCHEMA | Same JSON output, 4 000-token ceiling | Same JSON output — identical downstream rendering |
| Use for final/production decks | Use for quick iterations or volume runs | Use for drafts or when on NVIDIA infra |

---

## Few-Shot Examples

These show the correct command for a given user request. Apply the same judgment to new requests.

---

**User:** "Make me a deck about Kubernetes storage for a team knowledge-sharing session"
→ Educational content, ~15 min talk, likely developers
```bash
python generate.py "Kubernetes Storage Deep Dive" --theme dark --slides 12
```

---

**User:** "I need a board presentation on Q4 financial results — 10 slides, very polished"
→ Boardroom, executive audience, formal
```bash
python generate.py "Q4 Financial Results" --theme executive --slides 10
```

---

**User:** "Generate a 20-slide training deck on PPDM administration"
→ 20 slides is expensive — suggest/use draft mode, educational theme
```bash
python generate.py "PPDM Administration Training" --theme light --slides 20 --draft
```
*(Tell user to run this directly in terminal — draft mode needs interactive Enter)*

---

**User:** "Remix my old pitch deck but make it cleaner"
→ Remix, no specific theme preference → use executive (pitch = boardroom)
```bash
python generate.py "Product Pitch" --remix old_pitch.pptx --theme executive
```

---

**User:** "Remix this deck — it has a lot of architecture diagrams"
→ Vision pass needed for diagrams
```bash
python generate.py "Architecture Overview" --remix arch_deck.pptx --vision --theme dark
```
*(Mention: vision processes images in parallel, ~30 s for a 20-image deck)*

---

**User:** "I want to see the outline before you generate — my topic is machine learning infrastructure"
→ Explicit draft request, technical topic
```bash
python generate.py "Machine Learning Infrastructure" --theme dark --slides 14 --draft
```
*(Tell user to run in terminal — needs interactive confirmation)*

---

**User:** "Generate an HTML version I can present from a browser"
→ html format, pick theme by topic context
```bash
python generate.py "Your Topic" --format html --theme corporate
```

---

## All Flags

| Flag | Default | Description |
|---|---|---|
| `--theme` | `dark` | `dark` · `light` · `corporate` · `executive` |
| `--format` | `pptx` | `pptx` · `html` |
| `--slides N` | `12` | Integer 4–20 |
| `--draft` | off | Haiku preview + cost → Enter to upscale to Opus |
| `--provider` | `anthropic` | `anthropic` (Opus 5.5, default) · `claude-haiku` (Haiku 5.5, fast draft) · `nvidia` (Palmyra via NIM) |
| `--remix FILE` | — | Rebuild from existing `.pptx` via MarkItDown |
| `--vision` | off | Phi-4 + DePlot vision pass on remix images |
| `--images` | off | Embed Unsplash photos (needs `UNSPLASH_ACCESS_KEY`) |
| `--no-notes` | off | Omit speaker notes |
| `--output FILE` | auto | Custom output filename |

---

## Setup

```bash
cd path/to/claude-deck-generator
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
export NVIDIA_API_KEY=nvapi-...        # needed for --provider nvidia and --vision
export UNSPLASH_ACCESS_KEY=...         # needed for --images
```

---

## How It Works

1. **Content generation** — `generate_content()` calls Claude Opus 5.5 with `thinking: {type: "adaptive"}` and `output_config: {effort: "high"}`, enforcing `SLIDE_SCHEMA` — structured JSON every time. Haiku variant (`generate_content_haiku()`) is used for `--provider claude-haiku` or draft previews.
2. **Remix ingestion** — `ingest_pptx()` uses MarkItDown to extract text; `--vision` adds parallel Phi-4 (image descriptions) + DePlot (chart tables) via `asyncio.gather()`.
3. **Rendering** — `build_pptx()` or `build_html()` renders output with all elements drawn manually — no PowerPoint placeholder layouts.

---

## Key Constraints

- `ANTHROPIC_API_KEY` must be set — raises `AuthenticationError` without it
- Slide count clamped to 4–20 — values outside this range are silently clipped
- `--draft` requires interactive terminal — cannot be invoked via `/deck` in Claude Code
- `--provider claude-haiku` uses Haiku 5.5 with thinking off; useful for fast drafts or high-volume runs
- `--vision` requires `NVIDIA_API_KEY` and adds ~1–3 s per image (parallel, so total = max single image time × parallelism, not sum)
- `--images` requires `UNSPLASH_ACCESS_KEY`
