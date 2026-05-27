import streamlit as st
from modules.database import db
from datetime import datetime

st.title("💬 Secret Talk")
st.markdown("---")
st.markdown("*Express your feelings freely - frustration, anxiety, confusion, anything.*")

user_id = st.session_state.current_user['id']

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### What's on your mind?")
    thought = st.text_area(
        "",
        height=280,
        placeholder="Write whatever you're feeling...\n\n- Frustrated?\n- Anxious?\n- Confused?\n- Overwhelmed?\n\nLet it out here.",
        key="secret_thought"
    )

with col2:
    st.markdown("### Mood")
    mood = st.selectbox(
        "",
        ["😔 Sad", "😤 Frustrated", "😰 Anxious", "😕 Confused", "😤 Angry", "😟 Worried", "😶 Overwhelmed", "💭 Thinking"],
        key="mood_select"
    )

st.markdown("---")

if st.button("💾 Save Thought", use_container_width=True, type="primary"):
    if thought.strip():
        db.create_voice_note(
            user_id,
            f"secret_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            thought
        )
        st.success("✅ Saved securely!")
        st.rerun()
    else:
        st.error("Write something first")

st.markdown("### 📖 Your Thoughts")

notes = db.get_voice_notes(user_id)

if notes:
    for note in notes:
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                <div style="border-left: 4px solid #667eea; padding-left: 1rem; margin-bottom: 1rem;">
                    <strong>{note['entry_date']}</strong><br>
                    <p>{note['transcription'][:200]}...</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("🗑️", key=f"del_{note['id']}", help="Delete"):
                    db.delete_voice_note(note['id'])
                    st.rerun()
else:
    st.info("💭 No thoughts saved yet.")
