import streamlit as st
from modules.database import db
from datetime import datetime

st.markdown("# 💬 Secret Talk")

user_id = st.session_state.current_user['id']

st.markdown("### 🎙️ Record Your Voice Thoughts")

# For now: text-based "voice notes" (voice recording requires streamlit-webrtc which adds complexity)
col1, col2 = st.columns([2, 1])

with col1:
    voice_note = st.text_area(
        "Your thoughts (as if speaking)",
        height=200,
        placeholder="Speak your mind freely...",
        label_visibility="collapsed"
    )

with col2:
    st.markdown("### Recording Options")
    record_type = st.radio("Type", ["Text-based", "Transcribe"], label_visibility="collapsed")

if st.button("💾 Save Voice Note", use_container_width=True):
    if voice_note.strip():
        db.create_voice_note(user_id, f"note_{datetime.now().isoformat()}.txt", voice_note)
        st.success("✨ Voice note saved!")
        st.rerun()
    else:
        st.error("Please add your thoughts")

# Display past voice notes
st.markdown("---")
st.markdown("### 🎙️ Past Recordings")

voice_notes = db.get_voice_notes(user_id)

if voice_notes:
    for note in voice_notes:
        with st.expander(f"🎙️ {note['entry_date']}", expanded=False):
            st.markdown(f"**{note['audio_filename']}**")
            st.write(note['transcription'])

            if st.button(f"🗑️ Delete", key=f"delete_voice_{note['id']}"):
                db.delete_voice_note(note['id'])
                st.success("Voice note deleted")
                st.rerun()
else:
    st.info("No voice notes yet. Record your first thought!")
