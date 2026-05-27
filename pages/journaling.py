import streamlit as st
from modules.database import db
from datetime import datetime

st.title("📝 Journaling")
st.markdown("---")

user_id = st.session_state.current_user['id']

GOOGLE_FONTS = [
    "Lora", "Merriweather", "Playfair Display", "Didot", "Crimson Text",
    "Courier Prime", "IBM Plex Mono", "JetBrains Mono", "Roboto Mono", "Space Mono",
    "Open Sans", "Roboto", "Poppins", "Inter", "Work Sans",
    "Montserrat", "Raleway", "Oswald", "Bebas Neue", "Righteous",
    "Pacifico", "Caveat", "Dancing Script", "Great Vibes", "Satisfy",
    "Courgette", "Allura", "Arizonia", "Salsa", "Shadows Into Light",
    "Cookie", "Fredoka One", "Lobster Two", "Fredoka", "Nunito",
    "Quicksand", "Comfortaa", "Varela Round", "Sora", "Kantumruy Pro",
    "Source Serif Pro", "Source Sans Pro", "Inconsolata", "Overpass", "Ubuntu",
    "Fira Sans", "Exo", "Questrial", "ABeeZee", "Abril Fatface",
    "Bitter", "PT Sans", "PT Serif", "Dosis", "Mulish",
    "Manrope", "DM Sans", "DM Serif Display", "Outfit", "Schibsted Grotesk",
    "Noto Sans", "Noto Serif", "Barlow", "Barlow Condensed", "Barlow Semi Condensed",
    "Rubik", "Rubik Mono One", "Karla", "Vollkorn", "Libre Baskerville",
    "IM Fell English", "Crimson Pro", "Spectral", "Gotu", "Handlee",
    "Indie Flower", "Permanent Marker", "Caveat Brush", "Homemade Apple", "VT323"
]

BG_THEMES = {
    "minimal": {"bg": "#ffffff"},
    "calm": {"bg": "#f0f4f8"},
    "soft pink": {"bg": "#ffe8f0"},
    "soft blue": {"bg": "#e8f4ff"},
    "gradient sunset": {"gradient": "linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)"},
    "gradient ocean": {"gradient": "linear-gradient(135deg, #667eea 0%, #64b5f6 100%)"},
    "gradient forest": {"gradient": "linear-gradient(135deg, #81c784 0%, #43a047 100%)"},
    "gradient pink": {"gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"},
}

# Import Google Fonts CSS
def get_fonts_css():
    fonts_str = "%20".join(GOOGLE_FONTS)
    return f"https://fonts.googleapis.com/css2?family={fonts_str.replace(' ', '+')}&display=swap"

st.markdown(f"""
<link href="{get_fonts_css()}" rel="stylesheet">
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1], gap="large")

with col1:
    st.markdown("### ✍️ Write Your Entry")
    title = st.text_input("📌 Title", placeholder="Today's thoughts...")
    content = st.text_area("", placeholder="Write freely...", height=320, key="journal_content")

with col2:
    st.markdown("### 🎨 Styling")
    font = st.selectbox("Font", GOOGLE_FONTS, index=0)
    text_color = st.color_picker("Text Color", "#1e293b")
    bg_theme = st.selectbox("Background", list(BG_THEMES.keys()))

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
        theme = BG_THEMES.get(entry['bg_theme'], {})
        bg_style = theme.get('bg', '#ffffff') if 'bg' in theme else theme.get('gradient', '#ffffff')

        if 'gradient' in theme:
            bg_html = f"background: {bg_style};"
        else:
            bg_html = f"background-color: {bg_style};"

        st.markdown(f"""
        <div style="{bg_html} padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;">
            <h3 style="font-family: '{entry['font_family']}'; color: {entry['text_color']};  margin: 0;">
                {entry['title']}
            </h3>
            <p style="font-family: '{entry['font_family']}'; color: {entry['text_color']}; line-height: 1.8; margin: 1rem 0;">
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
