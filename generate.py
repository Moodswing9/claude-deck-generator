"""
generate.py - Presentation generator with color theme support.

Usage:
    python generate.py [--theme THEME] [--output OUTPUT] [--title TITLE]

Themes:
    dark        Dark background with light text (default)
    light       Light background with dark text
    corporate   Professional blue/grey corporate style
"""

import argparse
import json
import os
from datetime import datetime

# ---------------------------------------------------------------------------
# Theme definitions
# ---------------------------------------------------------------------------

THEMES = {
    "dark": {
        "name": "Dark",
        "background": "#1a1a2e",
        "slide_bg": "#16213e",
        "primary": "#e94560",
        "secondary": "#0f3460",
        "text": "#eaeaea",
        "muted": "#a0a0b0",
        "accent": "#533483",
        "border": "#0f3460",
        "code_bg": "#0d0d1a",
        "font_family": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    },
    "light": {
        "name": "Light",
        "background": "#f5f5f5",
        "slide_bg": "#ffffff",
        "primary": "#2563eb",
        "secondary": "#e5e7eb",
        "text": "#111827",
        "muted": "#6b7280",
        "accent": "#7c3aed",
        "border": "#d1d5db",
        "code_bg": "#f3f4f6",
        "font_family": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    },
    "corporate": {
        "name": "Corporate",
        "background": "#1e293b",
        "slide_bg": "#0f172a",
        "primary": "#0ea5e9",
        "secondary": "#1e40af",
        "text": "#f1f5f9",
        "muted": "#94a3b8",
        "accent": "#06b6d4",
        "border": "#334155",
        "code_bg": "#0a0f1e",
        "font_family": "'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    },
}

DEFAULT_THEME = "dark"

# ---------------------------------------------------------------------------
# Sample slide content
# ---------------------------------------------------------------------------

DEFAULT_SLIDES = [
    {
        "type": "title",
        "title": "Welcome to the Presentation",
        "subtitle": "Generated with theme support",
    },
    {
        "type": "content",
        "title": "Key Features",
        "bullets": [
            "Multiple color themes: dark, light, corporate",
            "Clean, responsive HTML output",
            "Easy to extend with new slides",
            "Command-line interface for quick generation",
        ],
    },
    {
        "type": "content",
        "title": "How It Works",
        "bullets": [
            "Define slides as Python dicts or load from JSON",
            "Pick a theme (dark, light, or corporate)",
            "Run generate.py to produce a self-contained HTML file",
            "Open the HTML file in any modern browser",
        ],
    },
    {
        "type": "code",
        "title": "Example Usage",
        "language": "bash",
        "code": (
            "# Generate with the default (dark) theme\n"
            "python generate.py\n\n"
            "# Generate with the light theme\n"
            "python generate.py --theme light\n\n"
            "# Generate with the corporate theme\n"
            "python generate.py --theme corporate --output my_deck.html"
        ),
    },
    {
        "type": "closing",
        "title": "Thank You",
        "subtitle": "Questions?",
    },
]

# ---------------------------------------------------------------------------
# HTML generation helpers
# ---------------------------------------------------------------------------


def _css(theme: dict) -> str:
    """Return the CSS block for the given theme."""
    t = theme
    return f"""
        :root {{
            --bg: {t['background']};
            --slide-bg: {t['slide_bg']};
            --primary: {t['primary']};
            --secondary: {t['secondary']};
            --text: {t['text']};
            --muted: {t['muted']};
            --accent: {t['accent']};
            --border: {t['border']};
            --code-bg: {t['code_bg']};
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            background: var(--bg);
            color: var(--text);
            font-family: {t['font_family']};
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 2rem 1rem;
        }}

        h1, h2, h3 {{
            color: var(--primary);
        }}

        .deck-title {{
            text-align: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid var(--border);
            width: 100%;
            max-width: 860px;
        }}

        .deck-title h1 {{
            font-size: 2rem;
        }}

        .deck-title .meta {{
            color: var(--muted);
            font-size: 0.85rem;
            margin-top: 0.4rem;
        }}

        .slide {{
            background: var(--slide-bg);
            border: 1px solid var(--border);
            border-radius: 10px;
            width: 100%;
            max-width: 860px;
            min-height: 320px;
            margin-bottom: 1.5rem;
            padding: 2.5rem 3rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
            position: relative;
            box-shadow: 0 4px 24px rgba(0,0,0,0.3);
        }}

        .slide-number {{
            position: absolute;
            top: 1rem;
            right: 1.5rem;
            font-size: 0.75rem;
            color: var(--muted);
        }}

        .slide-type-title {{
            text-align: center;
        }}

        .slide-type-title h2 {{
            font-size: 2.2rem;
            margin-bottom: 0.75rem;
        }}

        .slide-type-title .subtitle {{
            color: var(--muted);
            font-size: 1.2rem;
        }}

        .slide-type-closing {{
            text-align: center;
            border-top: 4px solid var(--primary);
        }}

        .slide-type-closing h2 {{
            font-size: 2.5rem;
            margin-bottom: 0.75rem;
        }}

        .slide h2 {{
            font-size: 1.6rem;
            margin-bottom: 1.2rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid var(--border);
        }}

        ul {{
            list-style: none;
            padding: 0;
        }}

        ul li {{
            padding: 0.45rem 0 0.45rem 1.6rem;
            position: relative;
            color: var(--text);
            font-size: 1.05rem;
            line-height: 1.6;
        }}

        ul li::before {{
            content: '▸';
            position: absolute;
            left: 0;
            color: var(--primary);
        }}

        pre {{
            background: var(--code-bg);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 1.2rem 1.5rem;
            overflow-x: auto;
            font-size: 0.9rem;
            line-height: 1.7;
            color: var(--accent);
            margin-top: 0.5rem;
        }}

        .theme-badge {{
            display: inline-block;
            background: var(--secondary);
            color: var(--primary);
            border-radius: 20px;
            padding: 0.2rem 0.9rem;
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            margin-top: 0.5rem;
        }}
    """


def _slide_html(slide: dict, index: int, total: int) -> str:
    """Render a single slide to HTML."""
    slide_type = slide.get("type", "content")
    title = slide.get("title", "")
    num_label = f'<span class="slide-number">{index}/{total}</span>'

    if slide_type == "title":
        subtitle = slide.get("subtitle", "")
        return f"""
        <section class="slide slide-type-title">
            {num_label}
            <h2>{title}</h2>
            <p class="subtitle">{subtitle}</p>
        </section>"""

    if slide_type == "closing":
        subtitle = slide.get("subtitle", "")
        return f"""
        <section class="slide slide-type-closing">
            {num_label}
            <h2>{title}</h2>
            <p class="subtitle" style="color: var(--muted); font-size: 1.1rem;">{subtitle}</p>
        </section>"""

    if slide_type == "code":
        code = slide.get("code", "")
        # Basic HTML escaping
        code = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f"""
        <section class="slide">
            {num_label}
            <h2>{title}</h2>
            <pre>{code}</pre>
        </section>"""

    # Default: content slide with bullets
    bullets = slide.get("bullets", [])
    items = "".join(f"<li>{b}</li>" for b in bullets)
    body = slide.get("body", "")
    body_html = f"<p style='margin-top:1rem; line-height:1.7;'>{body}</p>" if body else ""
    return f"""
    <section class="slide">
        {num_label}
        <h2>{title}</h2>
        <ul>{items}</ul>
        {body_html}
    </section>"""


def generate_html(
    slides: list,
    theme_key: str,
    title: str = "Presentation",
) -> str:
    """Generate a complete HTML presentation document."""
    if theme_key not in THEMES:
        raise ValueError(
            f"Unknown theme '{theme_key}'. Available themes: {', '.join(THEMES)}"
        )

    theme = THEMES[theme_key]
    total = len(slides)
    slides_html = "".join(
        _slide_html(slide, i + 1, total) for i, slide in enumerate(slides)
    )
    css = _css(theme)
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <style>{css}</style>
</head>
<body>
    <div class="deck-title">
        <h1>{title}</h1>
        <div class="meta">
            Generated on {generated_at}
            &nbsp;&bull;&nbsp;
            <span class="theme-badge">{theme['name']} theme</span>
        </div>
    </div>
    {slides_html}
</body>
</html>
"""


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an HTML presentation with a chosen color theme."
    )
    parser.add_argument(
        "--theme",
        choices=list(THEMES.keys()),
        default=DEFAULT_THEME,
        help=f"Color theme to use (default: {DEFAULT_THEME})",
    )
    parser.add_argument(
        "--output",
        default="presentation.html",
        help="Output HTML file path (default: presentation.html)",
    )
    parser.add_argument(
        "--title",
        default="Presentation",
        help="Presentation title (default: 'Presentation')",
    )
    parser.add_argument(
        "--slides",
        default=None,
        help="Path to a JSON file containing slide data (optional)",
    )
    parser.add_argument(
        "--list-themes",
        action="store_true",
        help="List available themes and exit",
    )
    return parser.parse_args()


def load_slides(path: str) -> list:
    """Load slide data from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("Slides JSON must be a list of slide objects.")
    return data


def main() -> None:
    args = parse_args()

    if args.list_themes:
        print("Available themes:")
        for key, theme in THEMES.items():
            marker = " (default)" if key == DEFAULT_THEME else ""
            print(f"  {key:<12} {theme['name']}{marker}")
        return

    slides = load_slides(args.slides) if args.slides else DEFAULT_SLIDES

    html = generate_html(slides, theme_key=args.theme, title=args.title)

    output_path = args.output
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Presentation generated: {output_path}  (theme: {args.theme})")


if __name__ == "__main__":
    main()
