import streamlit as st
from modules.database import db
from datetime import datetime

st.title(" Journaling")
st.markdown("---")

user_id = st.session_state.current_user['id']

GOOGLE_FONTS = [
    "Lora", "Merriweather", "Playfair Display", "Crimson Text",
    "Courier Prime", "IBM Plex Mono", "JetBrains Mono", "Roboto Mono",
    "Open Sans", "Roboto", "Poppins", "Inter", "Work Sans",
    "Montserrat", "Raleway", "Oswald", "Bebas Neue", "Righteous",
    "Pacifico", "Caveat", "Dancing Script", "Great Vibes", "Satisfy",
    "Courgette", "Allura", "Shadows Into Light",
    "Cookie", "Fredoka One", "Lobster Two", "Fredoka", "Nunito",
    "Quicksand", "Comfortaa", "Varela Round", "Sora",
    "Source Serif Pro", "Source Sans Pro", "Inconsolata", "Ubuntu",
    "Fira Sans", "Exo", "Bitter", "PT Sans", "PT Serif", "Dosis", "Mulish",
    "Manrope", "DM Sans", "DM Serif Display", "Outfit",
    "Noto Sans", "Noto Serif", "Barlow", "Rubik", "Karla", "Vollkorn",
    "Libre Baskerville", "IM Fell English", "Crimson Pro", "Spectral",
    "Handlee", "Indie Flower", "Permanent Marker", "Caveat Brush", "VT323"
]

# Real Unsplash background images
BG_THEMES = {
    "⬜ Minimal White": {
        "type": "color",
        "bg": "#ffffff",
        "preview": "#ffffff"
    },
    "🌸 Soft Pink": {
        "type": "color",
        "bg": "#ffe8f0",
        "preview": "#ffe8f0"
    },
    "🌊 Watercolor Blue": {
        "type": "image",
        "url": "https://images.unsplash.com/photo-1557682250-33bd709cbe85?w=1200&q=80",
        "preview": "#b3d4f5"
    },
    "🌅 Watercolor Peach": {
        "type": "image",
        "url": "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=1200&q=80",
        "preview": "#f5c9a0"
    },
    "💜 Purple Dream": {
        "type": "image",
        "url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&q=80",
        "preview": "#c9b3f5"
    },
    "🌿 Soft Green": {
        "type": "image",
        "url": "https://images.unsplash.com/photo-1518173946687-a4c8892bbd9f?w=1200&q=80",
        "preview": "#b3d4b3"
    },
    "🌸 Pink Clouds": {
        "type": "image",
        "url": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200&q=80",
        "preview": "#f5b3c8"
    },
    "🌫️ Misty Gray": {
        "type": "color",
        "bg": "#f0f4f8",
        "preview": "#dde4ed"
    },
    "🌙 Dark Mode": {
        "type": "color",
        "bg": "#1a1a2e",
        "preview": "#1a1a2e"
    },
    "🍂 Warm Sand": {
        "type": "color",
        "bg": "#fef3e2",
        "preview": "#fce8b2"
    },
}

# Load all Google Fonts at once
def get_fonts_css():
    font_families = "|".join([f.replace(" ", "+") for f in GOOGLE_FONTS])
    return f"https://fonts.googleapis.com/css2?family={font_families}&display=swap"

st.markdown(f'<link href="{get_fonts_css()}" rel="stylesheet">', unsafe_allow_html=True)

# Visual font picker using HTML buttons
def render_font_picker(fonts, selected_font):
    font_buttons_html = ""
    for font in fonts:
        is_selected = font == selected_font
        border = "3px solid #7c3aed" if is_selected else "2px solid #e2e8f0"
        bg = "#f3e8ff" if is_selected else "#ffffff"
        font_buttons_html += f"""
        <div onclick="selectFont('{font}')"
             style="
                font-family: '{font}', serif;
                font-size: 15px;
                padding: 8px 14px;
                border: {border};
                border-radius: 8px;
                background: {bg};
                cursor: pointer;
                white-space: nowrap;
                color: #1e293b;
                transition: all 0.2s;
             ">
            {font}
        </div>
        """

    html = f"""
    <style>
        #font-picker-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            max-height: 220px;
            overflow-y: auto;
            padding: 10px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            margin-bottom: 8px;
        }}
        #font-picker-container div:hover {{
            border-color: #7c3aed !important;
            background: #faf5ff !important;
        }}
    </style>
    <div id="font-picker-container">
        {font_buttons_html}
    </div>
    <script>
    function selectFont(fontName) {{
        const input = window.parent.document.querySelector('[data-testid="stTextInput"] input[aria-label="selected_font_hidden"]') 
            || Array.from(window.parent.document.querySelectorAll('input')).find(el => el.value && {str(fonts)}.includes(el.value));
        
        // Use streamlit component communication
        window.parent.postMessage({{type: 'streamlit:setComponentValue', value: fontName}}, '*');
    }}
    </script>
    """
    return html

# Background picker
def render_bg_picker(themes, selected_theme):
    bg_buttons_html = ""
    for name, theme in themes.items():
        is_selected = name == selected_theme
        border = "3px solid #7c3aed" if is_selected else "2px solid transparent"

        if theme["type"] == "image":
            bg_style = f"background-image: url('{theme['url']}'); background-size: cover; background-position: center;"
        else:
            bg_style = f"background-color: {theme['bg']};"

        bg_buttons_html += f"""
        <div style="display: flex; flex-direction: column; align-items: center; gap: 4px; cursor: pointer;">
            <div style="
                width: 54px; height: 38px;
                {bg_style}
                border-radius: 8px;
                border: {border};
                box-shadow: 0 1px 4px rgba(0,0,0,0.15);
            "></div>
            <span style="font-size: 10px; color: #64748b; text-align: center; max-width: 60px; line-height: 1.2;">{name.split(' ', 1)[1] if ' ' in name else name}</span>
        </div>
        """

    return f"""
    <div style="display: flex; flex-wrap: wrap; gap: 10px; padding: 12px;
                background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px;">
        {bg_buttons_html}
    </div>
    """

col1, col2 = st.columns([3, 1], gap="large")

with col1:
    st.markdown("### ✍️ Write Your Entry")
    title = st.text_input("📌 Title", placeholder="Today's thoughts...")
    content = st.text_area("", placeholder="Write freely...", height=320, key="journal_content")

with col2:
    st.markdown("### 🎨 Styling")

    # Font selector — selectbox with visual label showing font name styled in that font
    st.markdown("**Font**")

    # Show current selected font preview
    selected_font = st.session_state.get("selected_font", "Lora")

    # Build selectbox with all fonts; label shows font name
    font_options = GOOGLE_FONTS
    current_index = font_options.index(selected_font) if selected_font in font_options else 0

    # Render visual font grid
    st.markdown(render_font_picker(GOOGLE_FONTS, selected_font), unsafe_allow_html=True)

    # Fallback selectbox that actually works for selection
    font = st.selectbox(
        "Select font",
        GOOGLE_FONTS,
        index=current_index,
        key="font_select",
        label_visibility="collapsed",
        format_func=lambda x: x  # plain name in dropdown
    )

    # Inject CSS to make each option in the select render in its own font
    font_css_rules = "\n".join([
        f"""option[value="{f}"] {{ font-family: '{f}', serif; }}"""
        for f in GOOGLE_FONTS
    ])
    st.markdown(f"""
    <style>
    {font_css_rules}
    select[data-testid] option {{
        padding: 4px 0;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Show live preview of selected font
    st.markdown(f"""
    <div style="
        font-family: '{font}', serif;
        font-size: 16px;
        padding: 8px 12px;
        background: #f3e8ff;
        border-radius: 8px;
        border-left: 3px solid #7c3aed;
        margin: 6px 0 12px 0;
        color: #1e293b;
    ">✨ {font}</div>
    """, unsafe_allow_html=True)

    text_color = st.color_picker("Text Color", "#1e293b")

    st.markdown("**Background**")
    bg_theme = st.selectbox(
        "Background theme",
        list(BG_THEMES.keys()),
        key="bg_select",
        label_visibility="collapsed"
    )

    # Show background preview swatches
    st.markdown(render_bg_picker(BG_THEMES, bg_theme), unsafe_allow_html=True)

    # Live background preview strip
    selected_bg = BG_THEMES[bg_theme]
    if selected_bg["type"] == "image":
        preview_style = f"background-image: url('{selected_bg['url']}'); background-size: cover; background-position: center;"
    else:
        preview_style = f"background-color: {selected_bg['bg']};"

    st.markdown(f"""
    <div style="
        {preview_style}
        height: 50px;
        border-radius: 10px;
        margin-top: 8px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.1);
    "></div>
    """, unsafe_allow_html=True)

st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("💾 Save Entry", use_container_width=True, type="primary"):
        if title.strip() and content.strip():
            db.create_journal_entry(
                user_id,
                title,
                content,
                font_family=font,
                text_color=text_color,
                bg_color=text_color,
                bg_theme=bg_theme
            )
            st.success("✅ Saved!")
            st.rerun()
        else:
            st.error("Add title and content")

st.markdown("### 📚 Your Entries")
entries = db.get_journal_entries(user_id)

if entries:
    for entry in entries:
        theme = BG_THEMES.get(entry['bg_theme'], {"type": "color", "bg": "#ffffff"})

        if theme.get("type") == "image":
            bg_html = f"background-image: url('{theme['url']}'); background-size: cover; background-position: center;"
        else:
            bg_html = f"background-color: {theme.get('bg', '#ffffff')};"

        st.markdown(f"""
        <div style="{bg_html} padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
            <h3 style="font-family: '{entry['font_family']}', serif; color: {entry['text_color']}; margin: 0;">
                {entry['title']}
            </h3>
            <p style="font-family: '{entry['font_family']}', serif; color: {entry['text_color']}; line-height: 1.8; margin: 1rem 0;">
                {entry['content'][:300]}...
            </p>
            <small style="color: #666;">{entry['entry_date']}</small>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Delete", key=f"del_{entry['id']}", use_container_width=True):
                db.delete_journal_entry(entry['id'])
                st.rerun()
else:
    st.info("📝 No entries yet. Start writing!")