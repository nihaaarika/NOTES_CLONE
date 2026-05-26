import streamlit as st
from modules.database import db
from datetime import datetime

st.markdown("# 📝 Journaling")

user_id = st.session_state.current_user['id']

# Google Fonts list
FONTS = [
    "Lora", "Playfair Display", "Crimson Text",  # Elegant
    "Inter", "Roboto", "Poppins", "Montserrat",  # Modern
    "Caveat", "Great Vibes", "Pacifico",  # Handwriting
    "Abril Fatface", "Bitter", "Cormorant", "EB Garamond"
]

# Background themes
BG_THEMES = {
    "minimal": "#f8f9fa",
    "calm": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "flowers": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
    "hearts": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
    "fancy": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
    "nature": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
}

# Two columns: left for editor, right for styling
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.markdown("### Write your thoughts")
    title = st.text_input("Title", placeholder="Today's thoughts...")
    content = st.text_area("Content", height=300, placeholder="Write freely...")

with col2:
    st.markdown("### Styling Options")

    # Font selection
    font_family = st.selectbox("Font", FONTS, index=0)

    # Color pickers
    text_color = st.color_picker("Text Color", "#1e293b")
    bg_color = st.color_picker("Background Color", "#ffffff")

    # Background theme
    bg_theme = st.radio("Background Theme", list(BG_THEMES.keys()))

# Save button
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("💾 Save Entry", use_container_width=True):
        if title.strip() and content.strip():
            db.create_journal_entry(
                user_id,
                title,
                content,
                font_family=font_family,
                text_color=text_color,
                bg_color=bg_color,
                bg_theme=bg_theme
            )
            st.success("✨ Entry saved!")
            st.rerun()
        else:
            st.error("Please add title and content")

with col2:
    if st.button("Clear", use_container_width=True):
        st.rerun()

# Display past entries
st.markdown("---")
st.markdown("### 📚 Past Entries")

entries = db.get_journal_entries(user_id)

if entries:
    for entry in entries:
        with st.expander(f"📅 {entry['entry_date']} - {entry['title']}", expanded=False):
            # Apply custom styling
            st.markdown(f"""
            <div style="
                background-color: {entry['bg_color']};
                padding: 1.5rem;
                border-radius: 12px;
                color: {entry['text_color']};
                font-family: {entry['font_family']}, serif;
                line-height: 1.6;
            ">
                <h4>{entry['title']}</h4>
                <p>{entry['content']}</p>
            </div>
            """, unsafe_allow_html=True)

            # Edit and Delete buttons
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"✏️ Edit", key=f"edit_{entry['id']}"):
                    st.session_state.editing_entry_id = entry['id']
                    st.rerun()

            with col2:
                if st.button(f"🗑️ Delete", key=f"delete_{entry['id']}"):
                    db.delete_journal_entry(entry['id'])
                    st.success("Entry deleted")
                    st.rerun()
else:
    st.info("No journal entries yet. Start by writing your first entry!")
