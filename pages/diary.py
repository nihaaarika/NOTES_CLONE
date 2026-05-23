import streamlit as st
from database import db
from datetime import datetime, timedelta

st.markdown("## 📖 Diary")
st.markdown("Your personal space for reflection and memories")

# Date selector
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    selected_date = st.date_input("📅 Select Date", key="diary_date")

with col2:
    if st.button("← Yesterday", use_container_width=True):
        st.session_state.diary_date = selected_date - timedelta(days=1)
        st.rerun()

with col3:
    if st.button("Tomorrow →", use_container_width=True):
        st.session_state.diary_date = selected_date + timedelta(days=1)
        st.rerun()

st.markdown("---")

# Get or create diary entry
entry = db.get_diary_entry(str(selected_date))

if entry:
    st.markdown(f"### {entry['title'] if entry['title'] else 'Untitled Entry'}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        mood_emoji = {
            "happy": "😄",
            "sad": "😢",
            "neutral": "😐",
            "excited": "🤩",
            "stressed": "😰",
            "calm": "😌"
        }
        current_mood = entry.get('mood', 'neutral')
        st.caption(f"Mood: {mood_emoji.get(current_mood, '😐')} {current_mood.title()}")
    
    with col2:
        st.caption(f"Created: {entry['created_at'][:10]}")
    
    with col3:
        if st.button("✏️ Edit", use_container_width=True):
            st.session_state.editing_diary = True

else:
    st.markdown(f"### New Entry - {selected_date.strftime('%B %d, %Y')}")
    st.session_state.editing_diary = True

# Display or edit entry
if st.session_state.get("editing_diary", False) or not entry:
    st.markdown("#### Create/Edit Entry")
    
    # Title
    entry_title = st.text_input(
        "Title (Optional)",
        value=entry['title'] if entry else "",
        placeholder="Give your entry a title"
    )
    
    # Mood selector
    col1, col2, col3 = st.columns(3)
    with col1:
        mood_options = ["happy", "sad", "neutral", "excited", "stressed", "calm"]
        current_mood = entry.get('mood', 'neutral') if entry else 'neutral'
        mood_index = mood_options.index(current_mood) if current_mood in mood_options else 2
        mood = st.selectbox("How are you feeling?", mood_options, index=mood_index)
    
    with col2:
        st.write("")  # Spacing
    
    with col3:
        st.write("")  # Spacing
    
    # Content
    content = st.text_area(
        "What's on your mind?",
        value=entry['content'] if entry else "",
        height=300,
        placeholder="Write freely here...",
        label_visibility="collapsed"
    )
    
    # Tags
    tags = st.text_input(
        "Tags",
        value=", ".join(entry['tags']) if entry else "",
        placeholder="Add tags separated by commas"
    )
    
    # Word count
    word_count = len(content.split()) if content else 0
    st.caption(f"📝 {word_count} words")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Save Entry", use_container_width=True):
            if content.strip():
                tag_list = [t.strip() for t in tags.split(",") if t.strip()]
                
                if entry:
                    db.update_diary_entry(
                        str(selected_date),
                        entry_title,
                        content,
                        mood,
                        tag_list
                    )
                    st.success("✅ Entry updated!")
                else:
                    db.create_diary_entry(
                        str(selected_date),
                        entry_title,
                        content,
                        mood,
                        tag_list
                    )
                    st.success("✅ Entry saved!")
                
                st.session_state.editing_diary = False
                st.rerun()
            else:
                st.error("Please write something before saving")
    
    with col2:
        if st.button("Cancel", use_container_width=True):
            st.session_state.editing_diary = False
            st.rerun()
    
    with col3:
        if entry and st.button("🗑️ Delete Entry", use_container_width=True):
            db.delete_diary_entry(str(selected_date))
            st.success("Entry deleted")
            st.session_state.editing_diary = False
            st.rerun()

else:
    # Display entry
    with st.container():
        st.markdown(f"### {entry['title'] if entry['title'] else 'Untitled Entry'}")
        st.write(entry['content'])
        
        # Display tags
        if entry['tags']:
            st.markdown("**Tags:**")
            tags_html = "".join([f'<span class="tag">{tag}</span>' for tag in entry['tags']])
            st.markdown(tags_html, unsafe_allow_html=True)
        
        # Entry info
        col1, col2, col3 = st.columns(3)
        with col1:
            mood_emoji = {
                "happy": "😄",
                "sad": "😢",
                "neutral": "😐",
                "excited": "🤩",
                "stressed": "😰",
                "calm": "😌"
            }
            st.caption(f"Mood: {mood_emoji.get(entry['mood'], '😐')} {entry['mood'].title()}")
        
        with col2:
            word_count = len(entry['content'].split())
            st.caption(f"📝 {word_count} words")
        
        with col3:
            st.caption(f"Last updated: {entry['updated_at'][:10]}")

st.markdown("---")

# Past entries timeline
st.markdown("### 📚 Recent Entries")

all_entries = db.get_all_diary_entries()

if all_entries:
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown("**Timeline**")
        for entry in all_entries[:10]:  # Show last 10 entries
            entry_date = datetime.strptime(entry['entry_date'], '%Y-%m-%d').strftime('%b %d, %Y')
            mood_emoji = {
                "happy": "😄",
                "sad": "😢",
                "neutral": "😐",
                "excited": "🤩",
                "stressed": "😰",
                "calm": "😌"
            }
            emoji = mood_emoji.get(entry['mood'], '😐')
            
            if st.button(f"{emoji} {entry_date} - {entry['title'][:30] if entry['title'] else 'Untitled'}", use_container_width=True, key=f"entry_{entry['entry_date']}"):
                st.session_state.diary_date = datetime.strptime(entry['entry_date'], '%Y-%m-%d').date()
                st.rerun()
    
    with col2:
        st.markdown("**Statistics**")
        
        total_entries = len(all_entries)
        total_words = sum(len(e['content'].split()) for e in all_entries)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Entries", total_entries)
        with col2:
            st.metric("Total Words", total_words)
        
        # Mood distribution
        mood_counts = {}
        for entry in all_entries:
            mood = entry.get('mood', 'neutral')
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
        
        if mood_counts:
            st.markdown("**Mood Distribution**")
            for mood, count in sorted(mood_counts.items(), key=lambda x: x[1], reverse=True):
                mood_emoji = {
                    "happy": "😄",
                    "sad": "😢",
                    "neutral": "😐",
                    "excited": "🤩",
                    "stressed": "😰",
                    "calm": "😌"
                }
                emoji = mood_emoji.get(mood, '😐')
                st.write(f"{emoji} {mood.title()}: {count}")

else:
    st.info("📭 No diary entries yet. Start writing today!")