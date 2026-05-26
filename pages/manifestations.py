import streamlit as st
from modules.database import db

st.markdown("# ✨ Manifestations")

user_id = st.session_state.current_user['id']

st.markdown("### Create Your Goals & Manifestations")

col1, col2 = st.columns([4, 1])

with col1:
    goal_text = st.text_input(
        "Add new manifestation",
        placeholder="What do you want to manifest?",
        label_visibility="collapsed"
    )

with col2:
    if st.button("➕ Add", use_container_width=True):
        if goal_text.strip():
            db.create_manifestation(user_id, goal_text.strip())
            st.success("✨ Goal added!")
            st.rerun()
        else:
            st.error("Please enter a goal")

# Display goals
st.markdown("---")
st.markdown("### My Goals")

# Filter option
filter_type = st.radio("Show", ["All", "Active Only"], horizontal=True)
completed_only = filter_type == "Completed Only"

manifestations = db.get_manifestations(user_id, completed_only=False)

if manifestations:
    for goal in manifestations:
        col1, col2, col3 = st.columns([0.5, 4, 1])

        with col1:
            is_completed = goal['completed']
            checkbox = st.checkbox(
                "Complete",
                value=is_completed,
                key=f"complete_{goal['id']}",
                label_visibility="collapsed"
            )

            if checkbox != is_completed:
                db.update_manifestation(goal['id'], completed=1 if checkbox else 0)
                st.rerun()

        with col2:
            status = "✅" if goal['completed'] else "🎯"
            st.markdown(f"{status} {goal['goal_text']}")

        with col3:
            if st.button("🗑️", key=f"delete_{goal['id']}", use_container_width=True):
                db.delete_manifestation(goal['id'])
                st.success("Goal removed")
                st.rerun()

else:
    st.info("No manifestations yet. What do you want to create?")

# Stats
st.markdown("---")
total_goals = len(manifestations)
completed_goals = sum(1 for g in manifestations if g['completed'])

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Goals", total_goals)
with col2:
    st.metric("Completed", completed_goals)
