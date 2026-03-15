# Headbanger's Little Repository

A simple Python presentation generator that produces self-contained HTML slide decks with multiple color themes.

## Requirements

- Python 3.7+
- No external dependencies

## Quick Start

```bash
# Clone the repo
git clone https://github.com/Moodswing9/Headbanger-s-Little-Repository.git
cd Headbanger-s-Little-Repository

# Generate a presentation with the default (dark) theme
python generate.py

# Open the output in your browser
open presentation.html   # macOS
xdg-open presentation.html  # Linux
start presentation.html  # Windows
```

## Color Themes

Three built-in themes are available:

| Theme       | Description                                   |
|-------------|-----------------------------------------------|
| `dark`      | Dark background with light text (default)     |
| `light`     | Light background with dark text               |
| `corporate` | Professional blue/slate palette               |

### Selecting a Theme

Pass the `--theme` flag when running the generator:

```bash
# Dark theme (default)
python generate.py --theme dark

# Light theme
python generate.py --theme light

# Corporate theme
python generate.py --theme corporate
```

List all available themes:

```bash
python generate.py --list-themes
```

## Options

| Flag              | Default               | Description                                    |
|-------------------|-----------------------|------------------------------------------------|
| `--theme`         | `dark`                | Color theme (`dark`, `light`, `corporate`)     |
| `--output`        | `presentation.html`   | Output file path                               |
| `--title`         | `Presentation`        | Title shown in the browser tab and header      |
| `--slides`        | *(built-in sample)*   | Path to a JSON file with custom slide data     |
| `--list-themes`   | —                     | Print available themes and exit                |

## Custom Slides (JSON)

You can supply your own slides as a JSON file:

```json
[
  {
    "type": "title",
    "title": "My Presentation",
    "subtitle": "Subtitle goes here"
  },
  {
    "type": "content",
    "title": "Key Points",
    "bullets": ["First point", "Second point", "Third point"]
  },
  {
    "type": "code",
    "title": "Example Code",
    "code": "print('Hello, world!')"
  },
  {
    "type": "closing",
    "title": "Thank You",
    "subtitle": "Questions?"
  }
]
```

Then generate with:

```bash
python generate.py --slides my_slides.json --theme corporate --title "My Talk"
```

### Slide Types

| Type        | Required fields           | Optional fields       |
|-------------|---------------------------|-----------------------|
| `title`     | `title`                   | `subtitle`            |
| `content`   | `title`                   | `bullets`, `body`     |
| `code`      | `title`, `code`           | `language`            |
| `closing`   | `title`                   | `subtitle`            |

## Adding a Custom Theme

To add a new theme, extend the `THEMES` dictionary in `generate.py`:

```python
THEMES["ocean"] = {
    "name": "Ocean",
    "background": "#0a1628",
    "slide_bg": "#0d1f3c",
    "primary": "#38bdf8",
    "secondary": "#1e3a5f",
    "text": "#e0f2fe",
    "muted": "#7dd3fc",
    "accent": "#06b6d4",
    "border": "#1e3a5f",
    "code_bg": "#070f1f",
    "font_family": "'Segoe UI', sans-serif",
}
```

The new theme is immediately available via `--theme ocean`.
