"""
app.py - Streamlit web interface for the AI Presentation Generator.

Run locally:
    streamlit run app.py

Deploy:
    https://streamlit.io/cloud → connect GitHub repo → set ANTHROPIC_API_KEY secret
"""

import io
import tempfile
import os

import streamlit as st

from generate import (
    THEMES,
    DEFAULT_THEME,
    TOPIC_MAX_LENGTH,
    generate_content,
    build_pptx,
    build_html,
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

# ---------------------------------------------------------------------------
# Generate
# ---------------------------------------------------------------------------

if st.button("Generate Presentation", type="primary", use_container_width=True):
    if not topic_input.strip():
        st.error("Please enter a topic.")
    else:
        try:
            topic = validate_topic(topic_input)
        except SystemExit:
            st.error(f"Topic must be between 1 and {TOPIC_MAX_LENGTH} characters.")
            st.stop()

        theme = THEMES[theme_choice]
        safe = "".join(c if c.isalnum() or c in " _-" else "_" for c in topic)[:40].strip()
        filename = f"{safe}.{format_choice}"

        with st.spinner(f"Generating **{topic}**…"):
            try:
                data = generate_content(topic)
            except Exception as e:
                st.error(f"Failed to generate content: {e}")
                st.stop()

        st.success(f"Generated {len(data['slides'])} slides with the **{THEMES[theme_choice]['name']}** theme.")

        # Build the output file in memory
        if format_choice == "pptx":
            with tempfile.NamedTemporaryFile(suffix=".pptx", delete=False) as f:
                tmp_path = f.name
            try:
                build_pptx(data, theme, tmp_path)
                with open(tmp_path, "rb") as f:
                    file_bytes = f.read()
            finally:
                os.unlink(tmp_path)
            mime = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        else:
            buf = io.StringIO()
            with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as f:
                tmp_path = f.name
            try:
                build_html(data, theme, tmp_path)
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
            for i, slide in enumerate(data["slides"], 1):
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
