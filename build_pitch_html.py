"""
build_pitch_html.py — generates AI_Presentation_Generator_Pitch.html

Content mirrors PRESENTATION_BLUEPRINT.md slide-for-slide.
Self-contained single HTML file, no external dependencies.
"""

SLIDES = [
    {
        "num": 1,
        "type": "hook",
        "title": "You spent 4 hours on your last presentation.",
        "body": None,
        "note": "No bullets. Just that line. Stop. Let it sit.",
    },
    {
        "num": 2,
        "type": "body",
        "title": "You know the number. You just haven't said it out loud.",
        "body": [
            "Ask the room: how long did your last important presentation take to build?",
            "Three hours? Four? Six, if it was a board deck?",
            "Now multiply that by every person in this building who builds decks.",
            "Multiply by 52 weeks.",
            "That number doesn't appear on your P&L. It should.",
        ],
        "note": "The audience generates the stat themselves. Their number is more powerful than any published figure.",
    },
    {
        "num": 3,
        "type": "body",
        "title": "You already know how to fix this. You just haven't done it.",
        "body": [
            "Templates don't help — you still write every word",
            "Canva and Slides are faster tools for the same slow process",
            "AI assistants give you a blank page with a chatbot attached",
        ],
        "note": "Anticipates objections before they form. The audience is nodding — they've tried those things.",
    },
    {
        "num": 4,
        "type": "pivot",
        "title": "What if the presentation wrote itself?",
        "body": ["Not assisted. Not templated. Written — from a single sentence you already know."],
        "note": "Short slide, long pause. Let it sit.",
    },
    {
        "num": 5,
        "type": "demo",
        "title": "Watch.",
        "body": None,
        "command": 'python generate.py "Your Topic" --theme corporate',
        "note": "No narration during generation. None. The silence does the selling.",
    },
    {
        "num": 6,
        "type": "body",
        "title": "Claude didn't fill a template. It made decisions.",
        "body": [
            "Generated narrative structure, not just bullet points",
            "Selected what to include and what to cut",
            "Wrote speaker notes so you know what to say",
            "Applied design theme in the same pass",
        ],
        "note": "The demo created emotion. This slide creates understanding.",
    },
    {
        "num": 7,
        "type": "body",
        "title": "Built to be trusted.",
        "body": [
            "Claude Opus 4.6 with adaptive thinking — the same model used in enterprise deployments",
            "Schema-constrained JSON output — typed, parseable, version-controllable. Same schema every run.",
            "python-pptx rendering — native Office format, no conversion artifacts",
            "Three themes (dark, light, corporate) — designed for real environments, not demos",
        ],
        "note": "Do NOT say 'deterministic' — LLM output varies per run. Say 'schema-constrained.' A technical person will catch it.",
    },
    {
        "num": 8,
        "type": "two-col",
        "title": "Boardroom or browser — same 60 seconds.",
        "col_a": {
            "heading": "PowerPoint (.pptx)",
            "items": [
                "Editable in Office",
                "Speaker notes intact",
                "Native formatting",
                "Enterprise-ready",
            ],
        },
        "col_b": {
            "heading": "HTML",
            "items": [
                "No install required",
                "Share a link",
                "Runs in any browser",
                "Zero dependencies",
            ],
        },
        "note": "Doubles the addressable use case without adding complexity.",
    },
    {
        "num": 9,
        "type": "body",
        "title": "The tool you build on, not around.",
        "body": [
            "Add a theme in 10 lines of Python — your brand, your colors, available via --theme",
            "Point --slides at any JSON file — your data, your structure, the tool handles layout and notes",
            "Wrap it in a web form: one field, one button, your whole team has access",
            "Schedule it: weekly status deck generated and emailed every Monday, zero human intervention",
        ],
        "note": "Transforms the audience from users to builders.",
    },
    {
        "num": 10,
        "type": "close",
        "title": "One command. Every presentation.",
        "command": 'python generate.py "Your Topic" --theme corporate',
        "note": "The close should be the simplest slide in the deck. No bullets. No logos.",
    },
    {
        "num": 11,
        "type": "ask",
        "title": "Run it before you leave this room.",
        "commands": [
            "pip install -r requirements.txt",
            'export ANTHROPIC_API_KEY=your-key',
            'python generate.py "Your next meeting"',
        ],
        "github": "github.com/Moodswing9/Headbanger-s-Little-Repository",
        "note": "The ask is specific, immediate, and low-risk. 'Run it' is not 'evaluate it.'",
    },
]

TOTAL = len(SLIDES)


def slide_html(s):
    num = s["num"]
    note_html = f'<div class="speaker-note"><strong>Speaker note:</strong> {s["note"]}</div>' if s.get("note") else ""
    counter = f'<div class="slide-num">{num} / {TOTAL}</div>'

    if s["type"] == "hook":
        return f"""
  <section class="slide hook-slide">
    {counter}
    <h2 class="hook-line">{s["title"]}</h2>
    {note_html}
  </section>"""

    if s["type"] == "pivot":
        body = f'<p class="pivot-sub">{s["body"][0]}</p>' if s.get("body") else ""
        return f"""
  <section class="slide pivot-slide">
    {counter}
    <h2 class="pivot-title">{s["title"]}</h2>
    {body}
    {note_html}
  </section>"""

    if s["type"] == "demo":
        return f"""
  <section class="slide demo-slide">
    {counter}
    <h2 class="demo-title">{s["title"]}</h2>
    <div class="cmd-block"><code>{s["command"]}</code></div>
    <p class="demo-sub">60 seconds of silence. Output appears.</p>
    {note_html}
  </section>"""

    if s["type"] == "two-col":
        a_items = "\n".join(f"<li>{x}</li>" for x in s["col_a"]["items"])
        b_items = "\n".join(f"<li>{x}</li>" for x in s["col_b"]["items"])
        return f"""
  <section class="slide body-slide">
    {counter}
    <h2 class="slide-title">{s["title"]}</h2>
    <div class="two-col">
      <div class="col">
        <div class="col-heading">{s["col_a"]["heading"]}</div>
        <ul>{a_items}</ul>
      </div>
      <div class="col">
        <div class="col-heading">{s["col_b"]["heading"]}</div>
        <ul>{b_items}</ul>
      </div>
    </div>
    {note_html}
  </section>"""

    if s["type"] == "close":
        return f"""
  <section class="slide close-slide">
    {counter}
    <h2 class="close-eyebrow">{s["title"]}</h2>
    <div class="cmd-block cmd-large"><code>{s["command"]}</code></div>
    {note_html}
  </section>"""

    if s["type"] == "ask":
        cmds = "\n".join(f"<div class='ask-cmd'><code>{c}</code></div>" for c in s["commands"])
        return f"""
  <section class="slide ask-slide">
    {counter}
    <h2 class="slide-title">{s["title"]}</h2>
    <div class="ask-commands">{cmds}</div>
    <div class="github-link">&#x1F4E6; {s["github"]}</div>
    {note_html}
  </section>"""

    # default: body slide with bullets
    bullets = ""
    if s.get("body"):
        items = "\n".join(f"<li>{b}</li>" for b in s["body"])
        bullets = f"<ul class='bullets'>{items}</ul>"
    return f"""
  <section class="slide body-slide">
    {counter}
    <h2 class="slide-title">{s["title"]}</h2>
    {bullets}
    {note_html}
  </section>"""


def build():
    slides_html = "\n".join(slide_html(s) for s in SLIDES)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>AI Presentation Generator — Pitch Deck</title>
  <style>
    :root {{
      --bg:     #0f172a;
      --slide:  #1e293b;
      --accent: #0ea5e9;
      --text:   #f1f5f9;
      --muted:  #94a3b8;
      --border: #334155;
      --red:    #ef4444;
      --code:   #0a0f1e;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg); color: var(--text);
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      min-height: 100vh; display: flex; flex-direction: column;
      align-items: center; padding: 2rem 1rem;
    }}
    /* ── Deck header ── */
    .deck-header {{
      width: 100%; max-width: 860px;
      border-bottom: 2px solid var(--border);
      padding-bottom: 1.2rem; margin-bottom: 2rem; text-align: center;
    }}
    .deck-header h1 {{ font-size: 1.7rem; color: var(--accent); }}
    .deck-header .sub {{ color: var(--muted); font-size: 0.85rem; margin-top: 0.4rem; }}
    /* ── Base slide ── */
    .slide {{
      background: var(--slide); border: 1px solid var(--border);
      border-radius: 10px; width: 100%; max-width: 860px;
      margin-bottom: 1.5rem; padding: 2.2rem 2.8rem;
      position: relative; box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    }}
    .slide-num {{
      position: absolute; top: 1rem; right: 1.5rem;
      font-size: 0.72rem; color: var(--muted);
    }}
    /* ── Hook ── */
    .hook-slide {{
      background: var(--bg); border-top: 4px solid var(--red);
      text-align: center; padding: 3.5rem 2.8rem;
    }}
    .hook-line {{
      font-size: 2.4rem; font-weight: 800; color: var(--text); line-height: 1.3;
    }}
    /* ── Pivot ── */
    .pivot-slide {{
      background: var(--bg); border-top: 4px solid var(--accent);
      text-align: center; padding: 3rem 2.8rem;
    }}
    .pivot-title {{ font-size: 2rem; color: var(--text); font-weight: 700; margin-bottom: 1rem; }}
    .pivot-sub {{ font-size: 1.1rem; color: var(--muted); font-style: italic; }}
    /* ── Body slide ── */
    .slide-title {{
      font-size: 1.5rem; color: var(--accent); font-weight: 700;
      margin-bottom: 1.2rem; padding-bottom: 0.5rem;
      border-bottom: 1px solid var(--border);
    }}
    .bullets {{ list-style: none; }}
    .bullets li {{
      padding: 0.38rem 0 0.38rem 1.5rem; position: relative;
      font-size: 1rem; line-height: 1.6; color: var(--text);
    }}
    .bullets li::before {{ content: '▸'; position: absolute; left: 0; color: var(--accent); }}
    /* ── Demo slide ── */
    .demo-slide {{ background: var(--bg); text-align: center; padding: 3rem 2.8rem; }}
    .demo-title {{ font-size: 3rem; font-weight: 800; color: var(--text); margin-bottom: 1.5rem; }}
    .demo-sub {{ color: var(--muted); font-size: 0.95rem; margin-top: 1rem; font-style: italic; }}
    /* ── Command blocks ── */
    .cmd-block {{
      background: var(--code); border: 1px solid var(--border);
      border-radius: 6px; padding: 0.9rem 1.2rem;
      font-family: 'Consolas', 'Courier New', monospace;
      font-size: 1rem; color: var(--accent);
      display: inline-block; margin: 0.5rem 0;
    }}
    .cmd-large {{ font-size: 1.15rem; padding: 1.1rem 1.6rem; }}
    /* ── Close slide ── */
    .close-slide {{
      background: var(--bg); border-top: 4px solid var(--accent);
      text-align: center; padding: 3rem 2.8rem;
    }}
    .close-eyebrow {{
      font-size: 1rem; color: var(--muted); font-weight: 600;
      letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 1.5rem;
    }}
    /* ── Ask slide ── */
    .ask-slide {{ background: var(--bg); border-top: 4px solid var(--accent); }}
    .ask-commands {{ display: flex; flex-direction: column; gap: 0.5rem; margin: 1rem 0 1.2rem; }}
    .ask-cmd {{
      background: var(--code); border: 1px solid var(--border);
      border-radius: 6px; padding: 0.6rem 1rem;
      font-family: 'Consolas', 'Courier New', monospace;
      font-size: 0.95rem; color: var(--accent);
    }}
    .github-link {{
      font-size: 0.9rem; color: var(--muted); margin-top: 0.5rem;
    }}
    /* ── Two-column ── */
    .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 0.5rem; }}
    .col-heading {{
      font-size: 0.85rem; font-weight: 700; color: var(--accent);
      text-transform: uppercase; letter-spacing: 0.08em;
      margin-bottom: 0.7rem; padding-bottom: 0.4rem;
      border-bottom: 1px solid var(--border);
    }}
    /* ── Speaker note ── */
    .speaker-note {{
      font-size: 0.8rem; color: var(--muted); line-height: 1.6;
      border-top: 1px solid var(--border); padding-top: 0.8rem; margin-top: 1.2rem;
    }}
  </style>
</head>
<body>

  <div class="deck-header">
    <h1>AI Presentation Generator — Pitch Deck</h1>
    <div class="sub">Type a topic. Get a boardroom-ready presentation in 60 seconds.</div>
  </div>

  {slides_html}

</body>
</html>"""

    out = "AI_Presentation_Generator_Pitch.html"
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Saved: {out}  ({len(SLIDES)} slides)")


if __name__ == "__main__":
    build()
