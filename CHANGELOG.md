# Changelog

## [4.6.1] — 2026-10-12
### Fixed
- Claude Code plugin manifest passes `claude plugin validate`: `repository` is a URL, `license` is MIT and the unsupported `components` field is gone
- Install docs: the plugin is now installed from the Moodswing9 marketplace (`claude plugin marketplace add Moodswing9/claude-plugins`, then `claude plugin install deck-generator@moodswing9`). The previously documented `npx skills add` installs only the skill, not the slash commands

### Changed
- Plugin renamed to `deck-generator`: Claude Code reserves plugin names starting with `claude-` for Anthropic. The repository name and the `/deck` and `/deck-remix` commands are unchanged

### Added
- CI validates the plugin manifest on every push and pull request

## [4.6.0] — 2026-06-18
### Changed
- SKILL.md documents Claude Opus 4.7 as the primary model, with a provider comparison (Opus 4.7, Haiku 4.5, NVIDIA Palmyra)
- `plugin.json` description corrected from Opus 4.6 to Opus 4.7

## [4.5.0] — 2026-05-15
### Added
- NVIDIA Palmyra-Creative-122B provider (`--provider nvidia`) via NVIDIA NIM
- Vision pass for `--remix`: Phi-4 multimodal describes embedded slide images; DePlot extracts chart data into tables
- Unsplash photo embedding (`--images`) — searches and embeds relevant photos per slide
- Streamlit web UI (`app.py`) — browser-based frontend for the generator
- GitHub Actions CI — pytest on Python 3.11 and 3.12
- `--slides N` flag to control slide count (4–20, default 12)
- `--no-notes` flag to omit speaker notes

### Changed
- `generate_content()` uses `thinking: {type: "adaptive"}` for deeper reasoning on complex topics

## [4.4.0] — 2026-05-09
### Added
- `--provider claude-haiku` — fast-draft generation with Claude Haiku 4.5, same slide schema as Opus without adaptive thinking
- 6 unit tests for the Haiku provider

## [4.3.0] — 2026-05-07
### Added
- Claude Code plugin: `/deck` and `/deck-remix` slash commands, `claude-deck-generator` skill and plugin manifest

## [4.2.0] — 2026-04-26
### Added
- `--vision` (with `--remix`) — analyses each image in the source deck with Phi-4 multimodal and extracts chart data with DePlot, adding visual context to the remix

## [4.1.0] — 2026-04-23
### Added
- `--provider nvidia` — generate slides with NVIDIA NIM (Palmyra-Creative-122B); same themes, formats and flags as the Anthropic path
- Slide image analysis (Phi-4 multimodal) and chart-to-table extraction (DePlot) helpers; requires `NVIDIA_API_KEY`

## [4.0.0] — 2026-04-21
### Added
- Claude Haiku 4.5 fast-draft provider (`--provider claude-haiku`) — 4,000-token ceiling, no adaptive thinking, same output schema
- `--slides` count control clamped to 4–20

## [3.0.0] — 2026-03-15
### Added
- `--remix old.pptx` — ingest existing deck via MarkItDown, rebuild with Claude while preserving structure and content

## [2.0.0] — 2026-03-15
### Added
- HTML output format (`--format html`) — self-contained single file with CSS custom properties
- 4 themes: `corporate`, `dark`, `minimal`, `vibrant`
- Speaker notes in PPTX and HTML output
- Custom slide builders: closing slide, objection handling deck, Q&A prep deck, visual direction brief

## [1.1.0] — 2026-03-15
### Added
- Generated pitch decks attached as release assets: PowerPoint, HTML, and an animated opening slide

## [1.0.0] — 2026-03-15
### Added
- Claude Opus 4.6 with adaptive thinking generates structured slide content
- PPTX output via `python-pptx` (blank layouts, all elements drawn manually)
- `SLIDE_SCHEMA` enforcing consistent JSON structure: title, subtitle, bullets, notes, quote, stat slide types
- Auto-derived output filename from topic
