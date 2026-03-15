"""
build_objection_slides_html.py — generates Objection_Handling_Slides.html

Content mirrors build_objection_slides.py and OBJECTION_SLIDES.md exactly.
Self-contained single HTML file, no external dependencies.
"""

OBJECTIONS = [
    {
        "number": 1,
        "headline": "\"The output won't be good enough to use directly.\"",
        "reframe_label": "CONCEDE FIRST",
        "reframe": "\"You're right. It's not finished. It's 80% done in 60 seconds.\"",
        "bullets": [
            "The tool generates structure, argument, and speaker notes — not pixel-perfect design",
            "Your job shrinks from \"build a deck\" to \"review and refine\" — 4 hours becomes 20 minutes",
            "Every deck you've ever approved went through revisions — this just moves you to revision 1 instantly",
        ],
        "quote": (
            "\"You don't judge a sous chef by the fact that they didn't plate it. "
            "You judge them by the fact that dinner is ready and you didn't have to cook.\""
        ),
        "note": (
            "Show the generated deck. Point to one slide that needed a tweak. "
            "Say: \"This took me 45 seconds to fix. The alternative was starting from scratch.\""
        ),
    },
    {
        "number": 2,
        "headline": "\"Our data is confidential. What goes to the API?\"",
        "reframe_label": "THE FACT",
        "reframe": "\"Only the topic goes to Claude. Nothing else.\"",
        "bullets": [
            "The tool sends one thing to the API: your topic sentence",
            "No documents. No internal data. No files. One sentence in, structured slides out.",
            "For air-gapped environments: swap the API call for a self-hosted model — the architecture is identical",
        ],
        "quote": (
            "\"You've typed topics into Google. This is the same surface area of exposure. "
            "The difference is Google has your entire search history.\""
        ),
        "note": (
            "If the room is enterprise-security conscious, point to the JSON schema output. "
            "The API call is auditable and transparent — it contains exactly what you type as the topic, nothing more."
        ),
    },
    {
        "number": 3,
        "headline": "\"We already have Canva, Google Slides, and templates.\"",
        "reframe_label": "THE DISTINCTION",
        "reframe": "\"Those tools solve the wrong problem.\"",
        "bullets": [
            "Templates give you empty boxes — you still write every word",
            "Canva makes formatting faster — the content problem remains untouched",
            "Google Slides is a canvas — this is a co-writer",
        ],
        "quote": (
            "\"Canva addresses the tool. This addresses the task. "
            "The task is: what do I say, in what order, and why does it matter? "
            "Canva never touches that. Neither does Slides. Neither does PowerPoint. This does.\""
        ),
        "note": (
            "Don't cite a formatting percentage stat — it's unverifiable and a skeptic will challenge it. "
            "Instead: ask them. \"How long did your last deck take, start to finish?\" Wait for the answer. "
            "Then say: \"This does that in 60 seconds. Want to watch again?\" Their own number is more powerful."
        ),
    },
    {
        "number": 4,
        "headline": "\"We'd be too dependent on Anthropic. What if costs spike?\"",
        "reframe_label": "THE REFRAME",
        "reframe": "\"You're already dependent on infrastructure you don't own.\"",
        "bullets": [
            "Your slides are in Google Drive — dependent on Google",
            "Your video calls run on AWS — dependent on Amazon",
            "Your email runs on Microsoft — dependent on Microsoft",
            "Claude API uptime: 99.9%. Cost per presentation: under $0.05 at current pricing.",
        ],
        "quote": (
            "\"The question isn't whether to depend on infrastructure. "
            "The question is whether the dependency is worth the return. "
            "At $0.05 a deck, the math is not complicated.\""
        ),
        "note": (
            "If they push on vendor lock-in: the JSON schema output is portable. "
            "Point --slides at any JSON file from any source. Swap the model in one line of code."
        ),
    },
    {
        "number": 5,
        "headline": "\"Our presentations require specialized knowledge AI can't replicate.\"",
        "reframe_label": "THE FLIP",
        "reframe": "\"Then you give it the knowledge. It handles everything else.\"",
        "bullets": [
            "Use --slides to feed your own JSON — your data, your structure, your domain expertise",
            "The tool generates the frame; your team fills the substance",
            "Claude was trained on a broad corpus of business writing, frameworks, and case studies",
        ],
        "quote": (
            "\"You don't ask a consultant to know your business on day one. "
            "You brief them. They build the deck. "
            "This is the same relationship — without the invoice.\""
        ),
        "note": (
            "Demo the --slides flag if time allows. Show a JSON file with pre-populated data going in, "
            "a fully formatted deck coming out. The tool becomes infrastructure, not a black box."
        ),
    },
    {
        "number": 6,
        "headline": "\"It won't match our brand guidelines.\"",
        "reframe_label": "THE CLOSE",
        "reframe": "\"10 lines of Python. Your brand is in.\"",
        "bullets": [
            "Themes are a dictionary in the source code — colors, fonts, layout in one place",
            "Adding a custom theme takes under 10 minutes and is immediately available via --theme",
            "The HTML output uses CSS custom properties — any designer can extend it without touching Python",
        ],
        "quote": (
            "\"The question isn't whether this can match your brand. "
            "The question is whether you want it to. "
            "If yes, it's a Friday afternoon project.\""
        ),
        "note": (
            "Show the THEMES dict. Count the lines out loud if the room is technical. "
            "If non-technical: \"Your designer tells us the hex codes. We're done before lunch.\""
        ),
    },
]

MASTER_CLOSE = (
    "<em>\"That's a real concern. Here's how I'd think about it —\"</em><br><br>"
    "[Answer in one sentence.]<br><br>"
    "<em>\"But here's what I'd ask you to hold onto: every concern you've raised is a "
    "configuration problem, not a fundamental problem. The fundamental question is whether "
    "you want to spend four hours building slides or twenty minutes reviewing them. "
    "Everything else is details.\"</em><br><br>"
    "[Stop. Do not add anything.]"
)

DELIVERY = [
    ("CONCEDE", "green", "Say \"You're right\" or \"That's a fair concern\" before anything else. It disarms."),
    ("FLIP", "amber", "Reframe the objection as a feature, a choice, or a non-issue with evidence."),
    ("CLOSE", "red", "End every objection slide with a forcing function. Not a summary. A question or a consequence."),
]

BADGE_COLORS = {
    "CONCEDE FIRST": "#f59e0b",
    "THE FACT":      "#0ea5e9",
    "THE DISTINCTION": "#f59e0b",
    "THE REFRAME":   "#f59e0b",
    "THE FLIP":      "#0ea5e9",
    "THE CLOSE":     "#22c55e",
}


def objection_html(obj):
    badge_color = BADGE_COLORS.get(obj["reframe_label"], "#0ea5e9")
    bullets_html = "\n".join(
        f'<li>{b}</li>' for b in obj["bullets"]
    )
    total = len(OBJECTIONS)
    return f"""
    <section class="slide objection-slide">
      <div class="slide-num">{obj["number"]} / {total}</div>
      <div class="obj-header">
        <span class="num-badge">{obj["number"]}</span>
        <h2 class="obj-headline">{obj["headline"]}</h2>
      </div>
      <div class="obj-reframe">
        <span class="reframe-badge" style="background:{badge_color}">{obj["reframe_label"]}</span>
        <span class="reframe-text">{obj["reframe"]}</span>
      </div>
      <ul class="bullets">{bullets_html}</ul>
      <blockquote class="quote">{obj["quote"]}</blockquote>
      <div class="speaker-note"><strong>Speaker note:</strong> {obj["note"]}</div>
    </section>"""


def build():
    objections_html = "\n".join(objection_html(o) for o in OBJECTIONS)

    delivery_html = "\n".join(
        f'<div class="delivery-row">'
        f'<span class="delivery-badge {color}">{label}</span>'
        f'<span class="delivery-desc">{desc}</span>'
        f'</div>'
        for label, color, desc in DELIVERY
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Objection Handling — AI Presentation Generator</title>
  <style>
    :root {{
      --bg:      #0f172a;
      --slide:   #1e293b;
      --accent:  #0ea5e9;
      --text:    #f1f5f9;
      --muted:   #94a3b8;
      --border:  #334155;
      --green:   #22c55e;
      --amber:   #f59e0b;
      --red:     #ef4444;
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
    .deck-header h1 {{ font-size: 1.9rem; color: var(--accent); }}
    .deck-header .sub {{
      color: var(--muted); font-size: 0.85rem; margin-top: 0.4rem;
    }}
    /* ── Slides ── */
    .slide {{
      background: var(--slide); border: 1px solid var(--border);
      border-radius: 10px; width: 100%; max-width: 860px;
      margin-bottom: 1.5rem; padding: 2rem 2.5rem;
      position: relative; box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    }}
    .slide-num {{
      position: absolute; top: 1rem; right: 1.5rem;
      font-size: 0.72rem; color: var(--muted);
    }}
    /* ── Title slide ── */
    .title-slide {{
      background: var(--bg); border-top: 4px solid var(--accent);
      text-align: center; padding: 3rem 2.5rem;
    }}
    .title-slide .eyebrow {{
      font-size: 0.8rem; font-weight: 700; letter-spacing: 0.12em;
      color: var(--muted); text-transform: uppercase; margin-bottom: 0.8rem;
    }}
    .title-slide h1 {{ font-size: 2.4rem; color: var(--text); margin-bottom: 0.5rem; }}
    .title-slide .tagline {{ color: var(--muted); font-size: 1rem; margin-top: 0.5rem; }}
    /* ── Objection slides ── */
    .obj-header {{
      display: flex; align-items: flex-start; gap: 0.75rem; margin-bottom: 0.9rem;
    }}
    .num-badge {{
      background: var(--accent); color: #fff; font-weight: 700;
      font-size: 0.85rem; border-radius: 4px;
      padding: 0.2rem 0.55rem; flex-shrink: 0; margin-top: 0.15rem;
    }}
    .obj-headline {{
      font-size: 1.25rem; color: var(--red); font-weight: 700; line-height: 1.4;
    }}
    .obj-reframe {{
      display: flex; align-items: center; gap: 0.75rem;
      background: rgba(255,255,255,0.04); border-radius: 6px;
      padding: 0.55rem 0.8rem; margin-bottom: 1rem;
    }}
    .reframe-badge {{
      color: #000; font-weight: 700; font-size: 0.72rem;
      border-radius: 4px; padding: 0.18rem 0.5rem;
      white-space: nowrap; flex-shrink: 0;
    }}
    .reframe-text {{ font-size: 1rem; font-weight: 700; color: var(--text); }}
    /* ── Bullets ── */
    .bullets {{ list-style: none; margin-bottom: 1rem; }}
    .bullets li {{
      padding: 0.35rem 0 0.35rem 1.4rem; position: relative;
      font-size: 0.97rem; line-height: 1.6; color: var(--text);
    }}
    .bullets li::before {{
      content: '▸'; position: absolute; left: 0; color: var(--accent);
    }}
    /* ── Quote ── */
    blockquote.quote {{
      border-left: 3px solid var(--accent);
      background: rgba(14,165,233,0.06);
      border-radius: 0 6px 6px 0;
      padding: 0.7rem 1rem; margin-bottom: 0.9rem;
      font-size: 0.97rem; font-style: italic; color: var(--text); line-height: 1.6;
    }}
    /* ── Speaker note ── */
    .speaker-note {{
      font-size: 0.82rem; color: var(--muted); line-height: 1.6;
      border-top: 1px solid var(--border); padding-top: 0.7rem;
    }}
    /* ── Master close slide ── */
    .master-close {{ background: var(--bg); border-top: 4px solid var(--green); }}
    .master-close h2 {{ font-size: 1.3rem; color: var(--muted); margin-bottom: 0.4rem; }}
    .master-close .subtitle {{ color: var(--text); font-size: 1rem; margin-bottom: 1rem; }}
    .close-box {{
      background: var(--slide); border: 1px solid var(--border);
      border-radius: 8px; padding: 1.2rem 1.5rem;
      font-size: 0.97rem; line-height: 1.8; color: var(--text);
    }}
    /* ── Delivery slide ── */
    .delivery-slide {{ background: var(--bg); }}
    .delivery-slide h2 {{ font-size: 1.3rem; color: var(--muted); margin-bottom: 0.4rem; }}
    .delivery-slide .subtitle {{ color: var(--text); font-size: 1rem; margin-bottom: 1.2rem; }}
    .delivery-row {{
      display: flex; align-items: center; gap: 1rem;
      padding: 0.7rem 0; border-bottom: 1px solid var(--border);
    }}
    .delivery-row:last-child {{ border-bottom: none; }}
    .delivery-badge {{
      font-weight: 700; font-size: 0.75rem; border-radius: 4px;
      padding: 0.2rem 0.6rem; min-width: 72px; text-align: center;
      flex-shrink: 0;
    }}
    .delivery-badge.green  {{ background: var(--green);  color: #000; }}
    .delivery-badge.amber  {{ background: var(--amber);  color: #000; }}
    .delivery-badge.red    {{ background: var(--red);    color: #fff; }}
    .delivery-desc {{ font-size: 0.97rem; color: var(--text); line-height: 1.5; }}
    .one-rule {{
      margin-top: 1.2rem; padding-top: 0.9rem; border-top: 1px solid var(--border);
      font-size: 0.9rem; font-weight: 700; color: var(--muted);
    }}
  </style>
</head>
<body>

  <div class="deck-header">
    <h1>Objection Handling</h1>
    <div class="sub">AI Presentation Generator &bull; 6 objections preemptively neutralized &bull; Concede — Flip — Close</div>
  </div>

  <!-- Title slide -->
  <section class="slide title-slide">
    <div class="eyebrow">Objection Handling</div>
    <h1>6 Objections. Sharp Answers.</h1>
    <div class="tagline">AI Presentation Generator &nbsp;·&nbsp; For: Technical decision-makers, founders, CTOs</div>
    <div class="tagline" style="margin-top:0.4rem">Every concern the room will have. Answered before they ask.</div>
    <div class="tagline" style="margin-top:0.3rem;font-size:0.85rem">Principle: concede first, flip second, close with a forcing function.</div>
  </section>

  <!-- Objection slides -->
  {objections_html}

  <!-- Master close -->
  <section class="slide master-close">
    <h2>THE OBJECTION MASTER CLOSE</h2>
    <div class="subtitle">Use this if someone raises a concern not covered above.</div>
    <div class="close-box">{MASTER_CLOSE}</div>
  </section>

  <!-- Delivery principles -->
  <section class="slide delivery-slide">
    <h2>DELIVERY PRINCIPLES</h2>
    <div class="subtitle">The concede — flip — close structure.</div>
    {delivery_html}
    <div class="one-rule">
      The one rule: Never argue. Concede, reframe, close.
      The audience came to be convinced, not defeated.
    </div>
  </section>

</body>
</html>"""

    out = "Objection_Handling_Slides.html"
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Saved: {out}")


if __name__ == "__main__":
    build()
