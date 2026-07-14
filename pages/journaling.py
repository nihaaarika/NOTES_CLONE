import streamlit as st
from modules.database import db

st.title("📔 Journaling")
st.markdown("---")

user_id = st.session_state.current_user['id']

# ═════════════════════════════════════════════════════════════════════════════
# DATA
# ═════════════════════════════════════════════════════════════════════════════

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

BACKGROUNDS = {
    "White": "#ffffff", "Soft Pink": "#ea85a9", "Sky Blue": "#57a4ec",
    "Warm Sand": "#edd8b8", "Misty Gray": "#d5d9de", "Lavender": "#c9a6fd",
    "Mint": "#bcfadf", "Peach": "#efded3", "Dark Navy": "#1a1a30", "Dark Purple": "#31095c",
}
GRADIENTS = {
    "Sunset": "linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)",
    "Ocean": "linear-gradient(135deg, #667eea 0%, #64b5f6 100%)",
    "Purple Dream": "linear-gradient(135deg, #a855f7 0%, #ec4899 100%)",
    "Forest": "linear-gradient(135deg, #81c784 0%, #2e7d32 100%)",
    "Rose Gold": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
    "Golden Hour": "linear-gradient(135deg, #f9f871 0%, #f8b500 100%)",
    "Aurora": "linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%)",
    "Candy": "linear-gradient(135deg, #f6d365 0%, #fda085 100%)",
}
IMAGES = {
    "SunFlower": "download (1).jpeg",
    "Watercolor Peach": "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=1200&q=80",
    "Nature Green":     "https://images.unsplash.com/photo-1518173946687-a4c8892bbd9f?w=1200&q=80",
    "Pink Clouds":      "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200&q=80",
}
ALL_BG_NAMES = list(BACKGROUNDS.keys()) + list(GRADIENTS.keys()) + list(IMAGES.keys())

LEGACY = {
    "minimal": "White", "calm": "Misty Gray", "soft pink": "Soft Pink", "soft blue": "Sky Blue",
    "gradient sunset": "Sunset", "gradient ocean": "Ocean", "gradient forest": "Forest",
    "gradient pink": "Rose Gold", "Dark": "Dark Navy", "🌙 Dark Mode": "Dark Navy",
}

# ═════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═════════════════════════════════════════════════════════════════════════════

def resolve(name):
    if name in ALL_BG_NAMES:
        return name
    return LEGACY.get(name, "White")

def get_bg_style(name):
    key = resolve(name)
    if key in BACKGROUNDS:
        return f"background-color:{BACKGROUNDS[key]};"
    if key in GRADIENTS:
        return f"background:{GRADIENTS[key]};"
    if key in IMAGES:
        return f"background-image:url('{IMAGES[key]}');background-size:cover;background-position:center;"
    return "background-color:#ffffff;"

def get_bg_color(name):
    """Get the actual hex color for bg_color database column"""
    key = resolve(name)
    if key in BACKGROUNDS:
        return BACKGROUNDS[key]
    return "#ffffff"

def escape_html(text):
    """Escape HTML special characters to prevent XSS and rendering issues"""
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))

# ═════════════════════════════════════════════════════════════════════════════
# GOOGLE FONTS
# ═════════════════════════════════════════════════════════════════════════════

font_import = "&family=".join([f.replace(" ", "+", )for f in FONTS])
st.markdown(
    f'<link href="https://fonts.googleapis.com/css2?family={font_import}&display=swap" rel="stylesheet">',
    unsafe_allow_html=True
)

# ═════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ═════════════════════════════════════════════════════════════════════════════

if "selected_font" not in st.session_state:
    st.session_state.selected_font = "Lora"

# ═════════════════════════════════════════════════════════════════════════════
# WRITE SECTION
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("### ✍️ Write Your Entry")
write_col, style_col = st.columns([3, 1], gap="large")

with write_col:
    title = st.text_input("📌 Title", placeholder="Today's thoughts...", key="j_title")
    content = st.text_area("Content", placeholder="Write freely...", height=250,
                           label_visibility="collapsed", key="j_content")

with style_col:
    st.markdown("### 🎨 Styling")

    # ── Font Selector ──────────────────────────────────────────────────────
    st.markdown("**✏️ Font**")
    font_idx = FONTS.index(st.session_state.selected_font) if st.session_state.selected_font in FONTS else 0
    selected_font = st.selectbox(
        "Font", FONTS, index=font_idx,
        label_visibility="collapsed", key="j_font"
    )
    st.session_state.selected_font = selected_font

    # Font preview
    st.markdown(
        f'<p style="font-family:\'{selected_font}\',serif;font-size:18px;color:#aaa;margin-top:4px;">'
        f'Preview: The quick brown fox</p>',
        unsafe_allow_html=True
    )

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Text Color ───────────────────────────────────────────────────────────
    text_color = st.color_picker("🎨 Text Color", "#1e293b", key="j_color")

    # ── Background ─────────────────────────────────────────────────────────
    st.markdown("**🖼️ Background**")
    bg_name = st.selectbox(
        "Background", ALL_BG_NAMES, index=0,
        label_visibility="collapsed", key="j_bg"
    )
    st.markdown(
        f'<div style="{get_bg_style(bg_name)} height:55px;border-radius:10px;'
        f'border:2px solid #7c3aed;margin-top:6px;"></div>',
        unsafe_allow_html=True
    )

font = st.session_state.selected_font
bg_color = get_bg_color(bg_name)

# ═════════════════════════════════════════════════════════════════════════════
# LIVE PREVIEW
# ═════════════════════════════════════════════════════════════════════════════

if title.strip() or content.strip():
    st.markdown("---")
    st.markdown("### 👁️ Live Preview")
    preview_style = get_bg_style(bg_name)

    safe_title = escape_html(title)
    safe_content = escape_html(content)

    st.markdown(f"""
    <div style="{preview_style} padding:1.5rem;border-radius:14px;box-shadow:0 2px 12px rgba(0,0,0,0.15);">
        <h2 style="font-family:'{font}',serif;color:{text_color};margin:0 0 .8rem 0;">{safe_title}</h2>
        <p style="font-family:'{font}',serif;color:{text_color};line-height:1.8;margin:0;white-space:pre-wrap;">{safe_content}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# SAVE
# ═════════════════════════════════════════════════════════════════════════════

if st.button("💾 Save Entry", type="primary"):
    if title.strip() and content.strip():
        try:
            db.create_journal_entry(
                user_id,
                title.strip(),
                content.strip(),
                font_family=font,
                text_color=text_color,
                bg_color=bg_color,      # ← FIXED: was saving text_color here
                bg_theme=bg_name
            )
            st.success("✅ Entry saved!")
            st.session_state.j_title = ""
            st.session_state.j_content = ""
            st.rerun()
        except Exception as e:
            st.error(f"Save failed: {e}")
    else:
        st.error("Please fill in both title and content.")

# ═════════════════════════════════════════════════════════════════════════════
# SAVED ENTRIES
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("### 📚 Your Entries")
entries = db.get_journal_entries(user_id)

if entries:
    for entry in entries:
        f = entry.get('font_family') or 'Lora'
        col = entry.get('text_color') or '#1e293b'
        style = get_bg_style(entry.get('bg_theme') or 'White')
        uid = f"e{entry['id']}"
        text = entry['content'][:300] + ('...' if len(entry['content']) > 300 else '')

        safe_text = escape_html(text)
        safe_entry_title = escape_html(entry['title'])

        st.markdown(f"""
        <style>.{uid}{{
            padding:1.6rem;border-radius:14px;
            margin-bottom:1rem;box-shadow:0 2px 12px rgba(0,0,0,0.2);
            {style}
        }}</style>
        <div class="{uid}">
            <h3 style="font-family:'{f}',serif;color:{col};margin:0 0 .5rem 0;">{safe_entry_title}</h3>
            <p style="font-family:'{f}',serif;color:{col};line-height:1.8;margin:0 0 .8rem 0;white-space:pre-wrap;">{safe_text}</p>
            <small style="color:{col};opacity:.7;">📅 {entry['entry_date']}</small>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🗑️ Delete", key=f"del_{entry['id']}"):
            db.delete_journal_entry(entry['id'])
            st.rerun()
else:
    st.info("📝 No entries yet. Start writing above!")