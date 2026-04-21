"""
app.py - Streamlit web interface for the AI Presentation Generator.

Run locally:
    streamlit run app.py

Deploy:
    https://streamlit.io/cloud → connect GitHub repo → set ANTHROPIC_API_KEY secret
"""

import io
import os
import tempfile

import streamlit as st

# Inject secrets into environment so generate.py can find them
for _key in ("ANTHROPIC_API_KEY", "UNSPLASH_ACCESS_KEY"):
    if _key not in os.environ and _key in st.secrets:
        os.environ[_key] = st.secrets[_key]

from generate import (
    THEMES,
    DEFAULT_THEME,
    TOPIC_MAX_LENGTH,
    SLIDES_MIN,
    SLIDES_MAX,
    SLIDES_DEFAULT,
    UNSPLASH_ACCESS_KEY,
    generate_content,
    fetch_slide_images,
    build_pptx,
    build_html,
    ingest_pptx,
    validate_topic,
)

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="AI Presentation Generator",
    page_icon="🎯",
    layout="centered",
)

st.title("AI Presentation Generator")
st.caption("Powered by Claude — enter a topic and get a polished deck in seconds.")

# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------

topic_input = st.text_input(
    "Presentation topic",
    placeholder="e.g. The Future of Renewable Energy",
    max_chars=TOPIC_MAX_LENGTH,
)

col1, col2 = st.columns(2)

with col1:
    theme_choice = st.selectbox(
        "Theme",
        options=list(THEMES.keys()),
        index=list(THEMES.keys()).index(DEFAULT_THEME),
        format_func=lambda k: THEMES[k]["name"],
    )

with col2:
    format_choice = st.selectbox(
        "Format",
        options=["pptx", "html"],
        format_func=lambda f: "PowerPoint (.pptx)" if f == "pptx" else "HTML (.html)",
    )

slide_count = st.slider(
    "Number of slides",
    min_value=SLIDES_MIN,
    max_value=SLIDES_MAX,
    value=SLIDES_DEFAULT,
    step=1,
)

col3, col4 = st.columns(2)

with col3:
    use_images = st.checkbox(
        "Embed Unsplash photos",
        value=False,
        disabled=not UNSPLASH_ACCESS_KEY,
        help=(
            "Adds a relevant photo to each content slide. Requires UNSPLASH_ACCESS_KEY."
            if not UNSPLASH_ACCESS_KEY
            else "Fetches one photo per content slide from Unsplash."
        ),
    )

with col4:
    include_notes = st.checkbox(
        "Include speaker notes",
        value=True,
        help="Uncheck to omit speaker notes from the output file.",
    )

remix_file = st.file_uploader(
    "Remix an existing deck (optional)",
    type=["pptx"],
    help=(
        "Upload a .pptx file — MarkItDown extracts the content and Claude uses it "
        "as source material to build an improved version."
    ),
)

# ---------------------------------------------------------------------------
# Generate
# ---------------------------------------------------------------------------

if st.button("Generate Presentation", type="primary", use_container_width=True):
    if not topic_input.strip():
        st.error("Please enter a topic.")
    else:
        try:
            topic = validate_topic(topic_input)
        except ValueError as e:
            st.error(str(e))
            st.stop()

        # Ingest the remix file if provided
        reference_markdown = ""
        if remix_file is not None:
            with st.spinner(f"Ingesting reference deck: {remix_file.name}…"):
                try:
                    with tempfile.NamedTemporaryFile(suffix=".pptx", delete=False) as tmp:
                        tmp.write(remix_file.read())
                        tmp_path = tmp.name
                    reference_markdown = ingest_pptx(tmp_path)
                except Exception as e:
                    st.error(f"Failed to read reference deck: {e}")
                    st.stop()
                finally:
                    try:
                        os.unlink(tmp_path)
                    except Exception:
                        pass

        theme = THEMES[theme_choice]
        safe = "".join(c if c.isalnum() or c in " _-" else "_" for c in topic)[:40].strip()
        filename = f"{safe}.{format_choice}"

        spinner_msg = (
            f"Remixing **{remix_file.name}** into **{topic}**…"
            if reference_markdown
            else f"Generating **{topic}**…"
        )
        with st.spinner(spinner_msg):
            try:
                data = generate_content(
                    topic,
                    reference_markdown=reference_markdown,
                    slide_count=slide_count,
                )
            except Exception as e:
                st.error(f"Failed to generate content: {e}")
                st.stop()

        images = {}
        if use_images:
            with st.spinner("Fetching Unsplash images…"):
                images = fetch_slide_images(data["slides"])

        st.success(
            f"Generated {len(data['slides'])} slides with the **{THEMES[theme_choice]['name']}** theme."
        )

        # Build the output file in memory
        if format_choice == "pptx":
            with tempfile.NamedTemporaryFile(suffix=".pptx", delete=False) as f:
                tmp_path = f.name
            try:
                build_pptx(data, theme, tmp_path, images, include_notes=include_notes)
                with open(tmp_path, "rb") as f:
                    file_bytes = f.read()
            finally:
                os.unlink(tmp_path)
            mime = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        else:
            with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as f:
                tmp_path = f.name
            try:
                build_html(data, theme, tmp_path, images, include_notes=include_notes)
                with open(tmp_path, "r", encoding="utf-8") as f:
                    file_bytes = f.read().encode("utf-8")
            finally:
                os.unlink(tmp_path)
            mime = "text/html"

        st.download_button(
            label=f"Download {filename}",
            data=file_bytes,
            file_name=filename,
            mime=mime,
            use_container_width=True,
        )

        # Slide preview
        with st.expander("Slide outline", expanded=True):
            st.markdown(f"### {data['title']}")
            if data.get("subtitle"):
                st.markdown(f"*{data['subtitle']}*")
            for i, slide in enumerate(data["slides"], 1):
                stype = slide.get("type", "content")
                if stype == "section":
                    st.markdown(f"**{i}. {slide['title']}** *(section break)*")
                elif stype == "quote":
                    st.markdown(f"**{i}. {slide['title']}** *(quote)*")
                    if slide.get("quote"):
                        st.markdown(f'  > "{slide["quote"]}"')
                elif stype == "stat":
                    st.markdown(f"**{i}. {slide['title']}** *(stat)*")
                    if slide.get("stat"):
                        st.markdown(f"  **{slide['stat']}** — {slide.get('stat_label', '')}")
                else:
                    st.markdown(f"**{i}. {slide['title']}**")
                    for bullet in slide["bullets"]:
                        st.markdown(f"- {bullet}")

# ---------------------------------------------------------------------------
# Sidebar — API key hint
# ---------------------------------------------------------------------------

with st.sidebar:
    st.header("Setup")
    st.markdown(
        "Set your Anthropic API key as an environment variable:\n"
        "```\nANTHROPIC_API_KEY=sk-ant-...\n```\n"
        "On Streamlit Cloud, add it under **Settings → Secrets**:\n"
        "```toml\nANTHROPIC_API_KEY = 'sk-ant-...'\n```"
    )
    st.divider()
    st.markdown("**Themes**")
    descriptions = {
        "dark": "Dark navy, red accent",
        "light": "White, blue accent",
        "corporate": "Dark slate, sky blue",
        "executive": "White, gold accent — boardroom ready",
    }
    for key, t in THEMES.items():
        st.markdown(f"- `{key}` — {descriptions.get(key, t['name'])}")
    st.divider()
    st.markdown("**Remix**")
    st.markdown(
        "Upload any `.pptx` file to use as a reference. "
        "MarkItDown extracts the content; Claude rebuilds it as a polished deck."
    )
