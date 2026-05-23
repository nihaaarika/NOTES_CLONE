import streamlit as st
from database import db
from datetime import datetime
import json

st.markdown("## 📝 Notes")
st.markdown("Keep your thoughts organized and easily accessible")

# Layout with columns
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    search_query = st.text_input("🔍 Search notes", placeholder="Find by title or content...")

with col2:
    view_mode = st.selectbox("View", ["Grid", "List"], label_visibility="collapsed")

with col3:
    if st.button("✨ New Note", use_container_width=True):
        st.session_state.creating_note = True

st.markdown("---")

# Get notes
if search_query:
    notes = db.get_all_notes(search_query)
    st.caption(f"Found {len(notes)} note(s)")
else:
    notes = db.get_all_notes()

# Create new note modal
if st.session_state.get("creating_note", False):
    with st.container():
        st.markdown("### Create New Note")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            note_title = st.text_input("Note Title", placeholder="Give your note a title...")
        with col2:
            note_color = st.color_picker("Color", "#ffffff")
        
        note_content = st.text_area(
            "Content",
            placeholder="Start writing...",
            height=200,
            label_visibility="collapsed"
        )
        
        tags_input = st.text_input(
            "Tags",
            placeholder="Add tags separated by commas (e.g., work, important, ideas)"
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💾 Save Note", use_container_width=True):
                if note_title.strip():
                    tags = [t.strip() for t in tags_input.split(",") if t.strip()]
                    db.create_note(note_title, note_content, tags, note_color)
                    st.session_state.creating_note = False
                    st.success("✅ Note saved!")
                    st.rerun()
                else:
                    st.error("Please enter a title")
        
        with col2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.creating_note = False
                st.rerun()
        
        st.markdown("---")

# Display notes
if notes:
    if view_mode == "Grid":
        # Grid view (3 columns)
        cols = st.columns(3)
        for idx, note in enumerate(notes):
            col = cols[idx % 3]
            
            with col:
                # Card styling
                st.markdown(
                    f"""
                    <div class="card" style="border-left: 4px solid {note['color']};">
                        <h4>{note['title']}</h4>
                        <p style="font-size: 0.9rem; color: #64748b;">{note['content'][:100]}...</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Tags
                if note['tags']:
                    for tag in note['tags']:
                        st.markdown(f'<span class="tag">{tag}</span>', unsafe_allow_html=True)
                
                # Actions
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("✏️", key=f"edit_{note['id']}", help="Edit"):
                        st.session_state.editing_note_id = note['id']
                        st.rerun()
                
                with col2:
                    if st.button("📌", key=f"pin_{note['id']}", help="Pin"):
                        db.update_note(note['id'], pinned=1 - note['pinned'])
                        st.rerun()
                
                with col3:
                    if st.button("🗑️", key=f"delete_{note['id']}", help="Delete"):
                        db.delete_note(note['id'])
                        st.success("Note deleted")
                        st.rerun()
                
                st.caption(f"Updated: {note['updated_at'][:10]}")
                st.markdown("---")
    
    else:
        # List view
        for note in notes:
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 0.5])
            
            with col1:
                st.markdown(f"### {note['title']}")
                st.caption(note['content'][:150] + "...")
                
                if note['tags']:
                    tags_html = "".join([f'<span class="tag">{tag}</span>' for tag in note['tags']])
                    st.markdown(tags_html, unsafe_allow_html=True)
            
            with col2:
                if st.button("✏️ Edit", key=f"edit_list_{note['id']}", use_container_width=True):
                    st.session_state.editing_note_id = note['id']
                    st.rerun()
            
            with col3:
                if st.button("📌 Pin", key=f"pin_list_{note['id']}", use_container_width=True):
                    db.update_note(note['id'], pinned=1 - note['pinned'])
                    st.rerun()
            
            with col4:
                if st.button("🗑️ Delete", key=f"delete_list_{note['id']}", use_container_width=True):
                    db.delete_note(note['id'])
                    st.success("Note deleted")
                    st.rerun()
            
            with col5:
                st.caption(note['updated_at'][:10])
            
            st.markdown("---")

# Edit note modal
if st.session_state.get("editing_note_id"):
    note_id = st.session_state.editing_note_id
    note = db.get_note(note_id)
    
    if note:
        st.markdown(f"### Edit Note: {note['title']}")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            new_title = st.text_input("Title", value=note['title'])
        with col2:
            new_color = st.color_picker("Color", value=note['color'])
        
        new_content = st.text_area(
            "Content",
            value=note['content'],
            height=200,
            label_visibility="collapsed"
        )
        
        new_tags = st.text_input(
            "Tags",
            value=", ".join(note['tags']),
            placeholder="Separate by comma"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Changes", use_container_width=True):
                tags = [t.strip() for t in new_tags.split(",") if t.strip()]
                db.update_note(note_id, new_title, new_content, tags, new_color)
                st.session_state.editing_note_id = None
                st.success("✅ Note updated!")
                st.rerun()
        
        with col2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.editing_note_id = None
                st.rerun()

else:
    if not notes and not search_query:
        st.info("📭 No notes yet. Create your first note to get started!")
    elif not notes and search_query:
        st.info("🔍 No notes match your search. Try a different query.")