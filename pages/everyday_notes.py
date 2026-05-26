import streamlit as st
from modules.database import db
from datetime import datetime, timedelta

st.markdown("# 📅 Everyday Notes")

user_id = st.session_state.current_user['id']

# Date picker
col1, col2 = st.columns([2, 1])

with col1:
    selected_date = st.date_input("Select Date", value=datetime.now())

with col2:
    if st.button("Today", use_container_width=True):
        st.rerun()

# Get or create note for selected date
date_str = selected_date.strftime("%Y-%m-%d")
existing_note = db.get_everyday_note_by_date(user_id, date_str)
note_content = existing_note['content'] if existing_note else ""
note_id = existing_note['id'] if existing_note else None

# Text area for note
st.markdown(f"### Notes for {selected_date.strftime('%A, %B %d, %Y')}")
new_content = st.text_area(
    "Daily notes",
    value=note_content,
    height=300,
    placeholder="Write your daily thoughts...",
    label_visibility="collapsed"
)

# Save button
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("💾 Save", use_container_width=True):
        if new_content.strip():
            if existing_note:
                db.update_everyday_note(note_id, new_content)
                st.success("✏️ Note updated!")
            else:
                db.create_everyday_note(user_id, new_content)
                st.success("✨ Note saved!")
            st.rerun()
        else:
            st.error("Please add some content")

with col2:
    if st.button("Clear", use_container_width=True):
        st.rerun()

# Quick access to recent notes
st.markdown("---")
st.markdown("### 📋 Recent Notes (Last 7 Days)")

all_notes = db.get_everyday_notes(user_id)
recent_notes = all_notes[:7]

if recent_notes:
    for note in recent_notes:
        with st.expander(f"📅 {note['note_date']}", expanded=False):
            st.write(note['content'][:200] + "..." if len(note['content']) > 200 else note['content'])

            if st.button(f"🗑️ Delete", key=f"delete_note_{note['id']}"):
                db.delete_everyday_note(note['id'])
                st.success("Note deleted")
                st.rerun()
else:
    st.info("No notes yet. Start writing!")
