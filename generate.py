import os
import json
import sys
import anthropic
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

SLIDE_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "description": "Presentation title"},
        "slides": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "bullets": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "3-5 concise bullet points"
                    },
                    "notes": {"type": "string", "description": "Speaker notes"}
                },
                "required": ["title", "bullets", "notes"],
                "additionalProperties": False
            }
        }
    },
    "required": ["title", "slides"],
    "additionalProperties": False
}

THEME = {
    "bg": RGBColor(0x1A, 0x1A, 0x2E),
    "accent": RGBColor(0xE9, 0x4F, 0x37),
    "text": RGBColor(0xFF, 0xFF, 0xFF),
    "subtext": RGBColor(0xB0, 0xB0, 0xC0),
    "title_font": "Calibri",
    "body_font": "Calibri",
}


def generate_slide_content(topic: str) -> dict:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4096,
        thinking={"type": "adaptive"},
        system=(
            "You are an expert presentation designer. Generate professional, "
            "insightful slide content. Each slide should have a clear title and "
            "3-5 punchy bullet points. Include helpful speaker notes."
        ),
        messages=[{
            "role": "user",
            "content": (
                f"Create a professional 8-10 slide presentation about: {topic}\n\n"
                "Include: title slide, agenda, key sections, and a conclusion slide."
            )
        }],
        output_config={
            "format": {
                "type": "json_schema",
                "schema": SLIDE_SCHEMA
            }
        }
    )

    text = next(b.text for b in response.content if b.type == "text")
    return json.loads(text)


def set_background(slide, color: RGBColor):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_text_box(slide, text, left, top, width, height,
                 font_size=18, bold=False, color=None,
                 font_name="Calibri", align=PP_ALIGN.LEFT, wrap=True):
    txBox = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.name = font_name
    run.font.color.rgb = color or THEME["text"]
    return txBox


def add_accent_bar(slide, top=1.15):
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        Inches(0.5), Inches(top), Inches(0.08), Inches(0.6)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = THEME["accent"]
    shape.line.fill.background()


def create_title_slide(prs, title):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    set_background(slide, THEME["bg"])

    # Accent stripe
    stripe = slide.shapes.add_shape(1, 0, Inches(3.2), Inches(10), Inches(1.2))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = THEME["accent"]
    stripe.line.fill.background()

    # Title
    add_text_box(slide, title, 0.5, 1.6, 9, 1.5,
                 font_size=40, bold=True, align=PP_ALIGN.LEFT)

    # Subtitle
    add_text_box(slide, "AI-Generated Presentation", 0.5, 3.3, 9, 0.5,
                 font_size=18, color=THEME["subtext"], align=PP_ALIGN.LEFT)


def create_content_slide(prs, title, bullets, notes):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, THEME["bg"])

    # Accent bar
    add_accent_bar(slide, top=1.1)

    # Slide title
    add_text_box(slide, title, 0.7, 0.35, 8.8, 0.9,
                 font_size=26, bold=True)

    # Divider line
    line = slide.shapes.add_shape(1, Inches(0.5), Inches(1.15), Inches(9), Inches(0.03))
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(0x40, 0x40, 0x60)
    line.line.fill.background()

    # Bullet points
    txBox = slide.shapes.add_textbox(Inches(0.7), Inches(1.45), Inches(8.8), Inches(4.8))
    tf = txBox.text_frame
    tf.word_wrap = True

    for i, bullet in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_before = Pt(6)
        run = p.add_run()
        run.text = f"▸  {bullet}"
        run.font.size = Pt(18)
        run.font.name = THEME["body_font"]
        run.font.color.rgb = THEME["text"]

    # Speaker notes
    if notes:
        slide.notes_slide.notes_text_frame.text = notes


def build_presentation(data: dict, output_path: str):
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)

    create_title_slide(prs, data["title"])

    for slide_data in data["slides"]:
        create_content_slide(
            prs,
            slide_data["title"],
            slide_data["bullets"],
            slide_data.get("notes", "")
        )

    prs.save(output_path)
    print(f"Saved: {output_path}")


def main():
    topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Enter presentation topic: ").strip()
    if not topic:
        print("Error: topic required")
        sys.exit(1)

    print(f"Generating presentation on: {topic}")
    data = generate_slide_content(topic)

    safe_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in topic)[:40].strip()
    output_path = f"{safe_name}.pptx"

    build_presentation(data, output_path)
    print(f"Done! {len(data['slides'])} slides generated.")


if __name__ == "__main__":
    main()
