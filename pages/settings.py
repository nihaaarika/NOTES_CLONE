import streamlit as st
from database import db

st.markdown("## ⚙️ Settings")
st.markdown("Customize your app experience")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["🎨 Appearance", "💾 Data", "ℹ️ About", "🔧 Advanced"])

# Tab 1: Appearance
with tab1:
    st.markdown("### Theme & Appearance")
    
    preferences = db.get_preferences()
    
    col1, col2 = st.columns(2)
    
    with col1:
        theme = st.selectbox(
            "Theme",
            ["light", "dark", "auto"],
            index=["light", "dark", "auto"].index(preferences.get('theme', 'light'))
        )
        
        st.info("**Light:** Classic bright theme\n**Dark:** Easy on the eyes\n**Auto:** Matches system settings")
    
    with col2:
        accent_color = st.color_picker(
            "Accent Color",
            value=preferences.get('accent_color', '#6366f1')
        )
        st.caption("Used for buttons, highlights, and accents")
    
    st.markdown("---")
    
    # Font size
    col1, col2 = st.columns(2)
    
    with col1:
        font_size = st.slider(
            "Font Size",
            min_value=12,
            max_value=24,
            value=preferences.get('font_size', 16),
            step=1
        )
        st.caption(f"Current: {font_size}px")
    
    with col2:
        auto_save = st.checkbox(
            "Auto-save",
            value=bool(preferences.get('auto_save', 1)),
            help="Automatically save changes"
        )
    
    st.markdown("---")
    
    # Preview
    st.markdown("### Preview")
    st.markdown(f"""
    <div class="card" style="background: {accent_color}20; border-color: {accent_color};">
        <h3 style="color: {accent_color};">This is a preview</h3>
        <p>This shows how your settings will look throughout the app.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Appearance Settings", use_container_width=True):
            db.set_preferences(theme, accent_color, font_size, int(auto_save))
            st.success("✅ Settings saved!")
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset to Default", use_container_width=True):
            db.set_preferences("light", "#6366f1", 16, 1)
            st.success("✅ Settings reset to default!")
            st.rerun()

# Tab 2: Data Management
with tab2:
    st.markdown("### Data Management")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Count items
    notes = db.get_all_notes()
    todos = db.get_all_todos()
    entries = db.get_all_diary_entries()
    
    with col1:
        st.metric("Notes", len(notes))
    with col2:
        st.metric("Todos", len(todos))
    with col3:
        st.metric("Diary Entries", len(entries))
    with col4:
        total_items = len(notes) + len(todos) + len(entries)
        st.metric("Total Items", total_items)
    
    st.markdown("---")
    
    # Export options
    st.markdown("### Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Export your data as:**")
        
        if st.button("📄 Export as JSON", use_container_width=True):
            import json
            
            export_data = {
                "notes": notes,
                "todos": todos,
                "diary_entries": entries,
                "exported_at": str(__import__('datetime').datetime.now())
            }
            
            json_str = json.dumps(export_data, indent=2, default=str)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name="notion_clone_backup.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📊 Export as CSV", use_container_width=True):
            import csv
            import io
            
            # Create CSV for notes
            output = io.StringIO()
            writer = csv.writer(output)
            
            writer.writerow(["Type", "Title", "Content", "Date"])
            
            for note in notes:
                writer.writerow(["Note", note['title'], note['content'][:100], note['created_at']])
            
            for todo in todos:
                writer.writerow(["Todo", todo['title'], todo['description'][:100], todo['due_date']])
            
            for entry in entries:
                writer.writerow(["Diary", entry['title'], entry['content'][:100], entry['entry_date']])
            
            st.download_button(
                label="Download CSV",
                data=output.getvalue(),
                file_name="notion_clone_backup.csv",
                mime="text/csv"
            )
    
    st.markdown("---")
    
    # Dangerous actions
    st.markdown("### Danger Zone")
    st.warning("⚠️ These actions cannot be undone!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Delete All Notes", use_container_width=True):
            if st.checkbox("I understand, delete all notes"):
                for note in notes:
                    db.delete_note(note['id'])
                st.success("All notes deleted")
                st.rerun()
    
    with col2:
        if st.button("🗑️ Delete All Todos", use_container_width=True):
            if st.checkbox("I understand, delete all todos"):
                for todo in todos:
                    db.delete_todo(todo['id'])
                st.success("All todos deleted")
                st.rerun()

# Tab 3: About
with tab3:
    st.markdown("### About Notion Clone")
    
    st.markdown("""
    **Version:** 1.0.0
    
    **Created:** May 2026
    
    **Description:**
    A professional note-taking and productivity app built with Python and Streamlit.
    Keep your thoughts organized, manage your tasks, and maintain your diary—all in one beautiful place.
    
    ---
    
    ### Features
    - 📝 **Notes** - Rich text notes with tags and colors
    - ✓ **Todo Lists** - Task management with priorities
    - 📖 **Diary** - Personal journaling with mood tracking
    - ✨ **AI Assistant** - AI-powered writing suggestions
    - 🎨 **Customization** - Theme and appearance settings
    - 💾 **Data Management** - Export and backup options
    
    ---
    
    ### Technologies
    - **Backend:** Python, SQLite
    - **Frontend:** Streamlit
    - **AI:** OpenAI API (optional), Hugging Face Transformers
    - **Data:** JSON, CSV export
    
    ---
    
    ### Support
    For issues, suggestions, or feedback, please feel free to reach out.
    This app is built with ❤️ for productivity enthusiasts.
    """)

# Tab 4: Advanced
with tab4:
    st.markdown("### Advanced Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Database")
        
        if st.button("📊 Database Info", use_container_width=True):
            import os
            db_path = "data/notes.db"
            if os.path.exists(db_path):
                db_size = os.path.getsize(db_path) / 1024  # KB
                st.info(f"Database size: {db_size:.2f} KB")
            else:
                st.warning("Database file not found")
        
        if st.button("🔄 Repair Database", use_container_width=True):
            try:
                from database import NotesDatabase
                db_instance = NotesDatabase()
                db_instance.init_db()
                st.success("✅ Database repaired!")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with col2:
        st.markdown("#### Cache")
        
        if st.button("🧹 Clear Cache", use_container_width=True):
            st.cache_data.clear()
            st.success("✅ Cache cleared!")
            st.rerun()
        
        if st.button("🔄 Restart App", use_container_width=True):
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("### Developer Info")
    
    with st.expander("📋 System Information"):
        import streamlit as st_info
        import sys
        import sqlite3
        
        st.write(f"**Python Version:** {sys.version}")
        st.write(f"**Streamlit Version:** {st_info.__version__}")
        st.write(f"**SQLite Version:** {sqlite3.sqlite_version}")
        
        # Session state info
        st.write(f"**Session State Keys:** {len(st.session_state)}")
        
        with st.expander("View Session State"):
            st.json({k: str(v) for k, v in st.session_state.items()})

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; padding: 2rem; color: #64748b;'>
    <p>Made with ❤️ for better productivity</p>
    <p style='font-size: 0.85rem;'>© 2026 Notion Clone. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)