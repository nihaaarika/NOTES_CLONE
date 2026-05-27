import streamlit as st
from modules.database import db
from datetime import datetime

st.title("📅 Everyday Notes")
st.markdown("---")

user_id = st.session_state.current_user['id']

col1, col2 = st.columns([3, 1])

with col1:
    selected_date = st.date_input("Select Date", value=datetime.now().date())

with col2:
    if st.button("📌 Today", use_container_width=True):
        selected_date = datetime.now().date()
        st.rerun()

date_str = selected_date.strftime("%Y-%m-%d")
existing_note = db.get_everyday_note_by_date(user_id, date_str)
note_content = existing_note['content'] if existing_note else ""
note_id = existing_note['id'] if existing_note else None

st.markdown(f"### {selected_date.strftime('%A, %B %d, %Y')}")

new_content = st.text_area(
    "",
    value=note_content,
    height=280,
    placeholder="Write your daily thoughts, mood, activities...",
    key="daily_note"
)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💾 Save", use_container_width=True, type="primary"):
        if new_content.strip():
            if existing_note:
                db.update_everyday_note(note_id, new_content)
                st.success("✅ Updated!")
            else:
                db.create_everyday_note(user_id, new_content)
                st.success("✅ Saved!")
            st.rerun()
        else:
            st.error("Write something")

st.markdown("---")
st.markdown("### 📚 Recent Notes")

all_notes = db.get_everyday_notes(user_id)

if all_notes:
    for note in all_notes[:10]:
        with st.container():
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"""
                <div style="border-left: 4px solid #667eea; padding-left: 1rem; margin-bottom: 1rem;">
                    <strong>📅 {note['note_date']}</strong><br>
                    <p>{note['content'][:150]}...</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("🗑️", key=f"del_{note['id']}", help="Delete"):
                    db.delete_everyday_note(note['id'])
                    st.rerun()
else:
    st.info("📝 No notes yet.")
