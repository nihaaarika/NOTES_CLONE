import streamlit as st
from modules.database import db
from datetime import datetime

st.title("📔 Journaling")
st.markdown("---")

user_id = st.session_state.current_user['id']

# ── Fonts list ──────────────────────────────────────────────────────────────
FONTS = [
    "Lora", "Merriweather", "Playfair Display", "Crimson Text",
    "Courier Prime", "IBM Plex Mono", "JetBrains Mono",
    "Open Sans", "Roboto", "Poppins", "Inter",
    "Montserrat", "Raleway", "Oswald", "Bebas Neue",
    "Pacifico", "Caveat", "Dancing Script", "Great Vibes", "Satisfy",
    "Courgette", "Allura", "Shadows Into Light",
    "Cookie", "Fredoka One", "Lobster Two", "Nunito",
    "Quicksand", "Comfortaa", "Varela Round",
    "Bitter", "PT Sans", "PT Serif", "Mulish",
    "Manrope", "DM Sans", "DM Serif Display", "Outfit",
    "Noto Serif", "Rubik", "Vollkorn", "Libre Baskerville",
    "Handlee", "Indie Flower", "Permanent Marker", "VT323"
]

# ── Backgrounds ─────────────────────────────────────────────────────────────
BACKGROUNDS = {
    "⬜ White": {"type": "color", "value": "#ffffff"},
    "🌸 Soft Pink": {"type": "color", "value": "#ffe8f0"},
    "☁️ Sky Blue": {"type": "color", "value": "#e8f4ff"},
    "🍂 Warm Sand": {"type": "color", "value": "#fef3e2"},
    "🌫️ Misty Gray": {"type": "color", "value": "#f0f4f8"},
    "🌙 Dark": {"type": "color", "value": "#1a1a2e"},
    "🌅 Sunset": {"type": "gradient", "value": "linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)"},
    "🌊 Ocean": {"type": "gradient", "value": "linear-gradient(135deg, #667eea 0%, #64b5f6 100%)"},
    "💜 Purple": {"type": "gradient", "value": "linear-gradient(135deg, #a855f7 0%, #ec4899 100%)"},
    "🌿 Forest": {"type": "gradient", "value": "linear-gradient(135deg, #81c784 0%, #2e7d32 100%)"},
    "🌸 Rose": {"type": "gradient", "value": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"},
    "🍋 Lemon": {"type": "gradient", "value": "linear-gradient(135deg, #f9f871 0%, #f8b500 100%)"},
    "🌺 Watercolor Blue": {
        "type": "image",
        "value": "https://images.unsplash.com/photo-1557682250-33bd709cbe85?w=1200&q=80"
    },
    "🌺 Watercolor Peach": {
        "type": "image",
        "value": "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=1200&q=80"
    },
    "🍃 Nature Green": {
        "type": "image",
        "value": "https://images.unsplash.com/photo-1518173946687-a4c8892bbd9f?w=1200&q=80"
    },
    "☁️ Pink Clouds": {
        "type": "image",
        "value": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200&q=80"
    },
}

# ── Load Google Fonts ────────────────────────────────────────────────────────
font_import = "&family=".join([f.replace(" ", "+") for f in FONTS])
st.markdown(
    f'<link href="https://fonts.googleapis.com/css2?family={font_import}&display=swap" rel="stylesheet">',
    unsafe_allow_html=True
)

# ── Helper: get background CSS ───────────────────────────────────────────────
def get_bg_css(theme_name):
    theme = BACKGROUNDS.get(theme_name, {"type": "color", "value": "#ffffff"})
    if theme["type"] == "color":
        return f"background-color: {theme['value']};"
    elif theme["type"] == "gradient":
        return f"background: {theme['value']};"
    else:
        return f"background-image: url('{theme['value']}'); background-size: cover; background-position: center;"

# ════════════════════════════════════════════════════════════════════════════
# WRITE SECTION
# ════════════════════════════════════════════════════════════════════════════
st.markdown("### ✍️ Write Your Entry")

write_col, style_col = st.columns([3, 1], gap="large")

with write_col:
    title = st.text_input("📌 Title", placeholder="Today's thoughts...")
    content = st.text_area("Content", placeholder="Write freely...", height=300,
                           label_visibility="collapsed")

with style_col:
    st.markdown("### 🎨 Styling")

    # ── Font picker ──────────────────────────────────────────────────────────
    st.markdown("**✏️ Font**")
    font = st.selectbox("Choose font", FONTS, index=0, label_visibility="collapsed")

    # Show preview of selected font
    st.markdown(
        f'<p style="font-family: \'{font}\', serif; font-size: 18px; '
        f'padding: 10px 14px; background: #f3e8ff; border-left: 4px solid #7c3aed; '
        f'border-radius: 6px; margin: 4px 0 14px 0; color: #1e293b;">'
        f'Hello in {font}</p>',
        unsafe_allow_html=True
    )

    # ── Text color ───────────────────────────────────────────────────────────
    text_color = st.color_picker("🎨 Text Color", "#1e293b")

    # ── Background picker ────────────────────────────────────────────────────
    st.markdown("**🖼️ Background**")
    bg_theme = st.selectbox("Choose background", list(BACKGROUNDS.keys()),
                            index=0, label_visibility="collapsed")

    # Show background preview
    bg_css = get_bg_css(bg_theme)
    st.markdown(
        f'<div style="{bg_css} height: 55px; border-radius: 10px; '
        f'border: 1px solid #e2e8f0; margin-top: 6px;"></div>',
        unsafe_allow_html=True
    )

st.markdown("---")

# ── Save button ──────────────────────────────────────────────────────────────
if st.button("💾 Save Entry", type="primary", use_container_width=False):
    if title.strip() and content.strip():
        db.create_journal_entry(
            user_id, title, content,
            font_family=font,
            text_color=text_color,
            bg_color=text_color,
            bg_theme=bg_theme
        )
        st.success("✅ Entry saved!")
        st.rerun()
    else:
        st.error("Please fill in both title and content.")

# ════════════════════════════════════════════════════════════════════════════
# YOUR ENTRIES
# ════════════════════════════════════════════════════════════════════════════
st.markdown("### 📚 Your Entries")
entries = db.get_journal_entries(user_id)

if entries:
    for entry in entries:
        entry_bg = get_bg_css(entry.get('bg_theme', '⬜ White'))
        entry_font = entry.get('font_family', 'Lora')
        entry_color = entry.get('text_color', '#1e293b')

        st.markdown(f"""
        <div style="{entry_bg} padding: 1.5rem; border-radius: 14px;
                    margin-bottom: 1rem; box-shadow: 0 2px 10px rgba(0,0,0,0.12);">
            <h3 style="font-family: '{entry_font}', serif;
                       color: {entry_color}; margin: 0 0 0.6rem 0;">
                {entry['title']}
            </h3>
            <p style="font-family: '{entry_font}', serif;
                      color: {entry_color}; line-height: 1.8; margin: 0 0 0.8rem 0;">
                {entry['content'][:300]}{'...' if len(entry['content']) > 300 else ''}
            </p>
            <small style="color: rgba(100,100,100,0.8);">📅 {entry['entry_date']}</small>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🗑️ Delete", key=f"del_{entry['id']}"):
            db.delete_journal_entry(entry['id'])
            st.rerun()
else:
    st.info("📝 No entries yet. Start writing above!")