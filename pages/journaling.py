import streamlit as st
from modules.database import db
import streamlit.components.v1 as components

st.title("📔 Journaling")
st.markdown("---")

user_id = st.session_state.current_user['id']

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
    "White": "#ffffff", "Soft Pink": "#ffe8f0", "Sky Blue": "#e8f4ff",
    "Warm Sand": "#fef3e2", "Misty Gray": "#f0f4f8", "Lavender": "#f0e6ff",
    "Mint": "#e6fff4", "Peach": "#fff0e6", "Dark Navy": "#1a1a2e", "Dark Purple": "#16002e",
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
    "Watercolor Blue":  "https://images.unsplash.com/photo-1557682250-33bd709cbe85?w=1200&q=80",
    "Watercolor Peach": "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=1200&q=80",
    "Nature Green":     "https://images.unsplash.com/photo-1518173946687-a4c8892bbd9f?w=1200&q=80",
    "Pink Clouds":      "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200&q=80",
}
ALL_BG_NAMES = list(BACKGROUNDS.keys()) + list(GRADIENTS.keys()) + list(IMAGES.keys())

LEGACY = {
    "minimal":"White","calm":"Misty Gray","soft pink":"Soft Pink","soft blue":"Sky Blue",
    "gradient sunset":"Sunset","gradient ocean":"Ocean","gradient forest":"Forest",
    "gradient pink":"Rose Gold","Dark":"Dark Navy","🌙 Dark Mode":"Dark Navy",
}

def resolve(name):
    if name in ALL_BG_NAMES: return name
    return LEGACY.get(name, "White")

def get_bg_style(name):
    key = resolve(name)
    if key in BACKGROUNDS:   return f"background-color: {BACKGROUNDS[key]} !important;"
    elif key in GRADIENTS:   return f"background: {GRADIENTS[key]} !important;"
    elif key in IMAGES:      return f"background-image: url('{IMAGES[key]}') !important; background-size: cover !important; background-position: center !important;"
    return "background-color: #ffffff !important;"

# Load Google Fonts
font_import = "&family=".join([f.replace(" ", "+") for f in FONTS])
st.markdown(f'<link href="https://fonts.googleapis.com/css2?family={font_import}&display=swap" rel="stylesheet">', unsafe_allow_html=True)

if "selected_font" not in st.session_state:
    st.session_state.selected_font = "Lora"

# ── WRITE SECTION ─────────────────────────────────────────────────────────────
st.markdown("### ✍️ Write Your Entry")
write_col, style_col = st.columns([3, 1], gap="large")

with write_col:
    title   = st.text_input("📌 Title", placeholder="Today's thoughts...", key="j_title")
    content = st.text_area("Content", placeholder="Write freely...", height=300,
                           label_visibility="collapsed", key="j_content")

with style_col:
    st.markdown("### 🎨 Styling")
    st.markdown("**✏️ Font**")

    # Build font rows — each row rendered in its own font, exactly like Canva
    font_rows = ""
    for f in FONTS:
        is_sel = "selected" if f == st.session_state.selected_font else ""
        font_rows += f'<div class="frow {is_sel}" data-font="{f}" style="font-family:\'{f}\',serif;">{f}</div>\n'

    picker = f"""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family={font_import}&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: transparent; font-size: 14px; }}
#search {{
    width: 100%;
    padding: 8px 12px;
    background: #2a2a3e;
    border: 1px solid #555;
    border-radius: 8px;
    color: #fff;
    font-size: 14px;
    outline: none;
    margin-bottom: 6px;
}}
#search::placeholder {{ color: #888; }}
#list {{
    max-height: 300px;
    overflow-y: auto;
    background: #1e1e2e;
    border: 1px solid #444;
    border-radius: 8px;
    padding: 4px 0;
}}
#list::-webkit-scrollbar {{ width: 5px; }}
#list::-webkit-scrollbar-thumb {{ background: #555; border-radius: 3px; }}
.frow {{
    padding: 10px 14px;
    font-size: 17px;
    color: #ddd;
    cursor: pointer;
    border-left: 3px solid transparent;
    transition: background 0.12s;
}}
.frow:hover {{ background: #2a2a3e; color: #fff; }}
.frow.selected {{
    background: #2d1f54;
    color: #c4b5fd;
    border-left: 3px solid #7c3aed;
}}
</style>
</head>
<body>
<input id="search" type="text" placeholder="🔍 Search fonts...">
<div id="list">
{font_rows}
</div>
<script>
  // scroll selected into view on load
  window.onload = function() {{
    const sel = document.querySelector('.frow.selected');
    if (sel) sel.scrollIntoView({{block:'center'}});
  }};

  document.querySelectorAll('.frow').forEach(function(row) {{
    row.addEventListener('click', function() {{
      document.querySelectorAll('.frow').forEach(r => r.classList.remove('selected'));
      this.classList.add('selected');
      window.parent.postMessage({{
        type: 'streamlit:setComponentValue',
        value: this.dataset.font
      }}, '*');
    }});
  }});

  document.getElementById('search').addEventListener('input', function() {{
    const q = this.value.toLowerCase();
    document.querySelectorAll('.frow').forEach(function(row) {{
      row.style.display = row.dataset.font.toLowerCase().includes(q) ? '' : 'none';
    }});
  }});
</script>
</body>
</html>
"""

    chosen = components.html(picker, height=370, scrolling=False)
    if chosen is not None:
        st.session_state.selected_font = chosen

    font = st.session_state.selected_font

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    text_color = st.color_picker("🎨 Text Color", "#1e293b", key="j_color")

    st.markdown("**🖼️ Background**")
    bg_name = st.selectbox("bg", ALL_BG_NAMES, index=0, label_visibility="collapsed", key="j_bg")
    bg_style = get_bg_style(bg_name)
    st.markdown(
        f'<div style="{bg_style} height: 55px; border-radius: 10px; border: 2px solid #7c3aed; margin-top: 6px;"></div>',
        unsafe_allow_html=True
    )

st.markdown("---")

if st.button("💾 Save Entry", type="primary"):
    if title.strip() and content.strip():
        db.create_journal_entry(user_id, title, content,
            font_family=font, text_color=text_color,
            bg_color=text_color, bg_theme=bg_name)
        st.success("✅ Entry saved!")
        st.rerun()
    else:
        st.error("Please fill in both title and content.")

# ── YOUR ENTRIES ──────────────────────────────────────────────────────────────
st.markdown("### 📚 Your Entries")
entries = db.get_journal_entries(user_id)

if entries:
    for entry in entries:
        f     = entry.get('font_family') or 'Lora'
        col   = entry.get('text_color')  or '#1e293b'
        style = get_bg_style(entry.get('bg_theme') or 'White')
        uid   = f"e{entry['id']}"
        text  = entry['content'][:300] + ('...' if len(entry['content']) > 300 else '')

        st.markdown(f"""
        <style>.{uid}{{
            {style.replace("!important;","").replace("!important","")}
            padding:1.6rem; border-radius:14px;
            margin-bottom:1rem; box-shadow:0 2px 12px rgba(0,0,0,0.2);
        }}</style>
        <div class="{uid}">
            <h3 style="font-family:'{f}',serif;color:{col};margin:0 0 .5rem 0;">{entry['title']}</h3>
            <p  style="font-family:'{f}',serif;color:{col};line-height:1.8;margin:0 0 .8rem 0;">{text}</p>
            <small style="color:{col};opacity:.7;">📅 {entry['entry_date']}</small>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🗑️ Delete", key=f"del_{entry['id']}"):
            db.delete_journal_entry(entry['id'])
            st.rerun()
else:
    st.info("📝 No entries yet. Start writing above!")