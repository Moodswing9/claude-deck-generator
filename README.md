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
