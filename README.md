# AI PowerPoint Generator

Generate professional PowerPoint presentations from any topic using Claude AI and python-pptx.

## Setup

```bash
pip install -r requirements.txt
```

Set your Anthropic API key:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

## Usage

```bash
python generate.py "Your Topic Here"
```

The `.pptx` file is saved in the current directory.

## Example

```bash
python generate.py "Heavy Metal Music History"
# → Heavy Metal Music History.pptx (9 slides)
```

## How It Works

1. Sends the topic to Claude Opus 4.6, which generates structured slide content (titles, bullet points, speaker notes)
2. Builds a styled `.pptx` using python-pptx with a dark theme and accent colors
