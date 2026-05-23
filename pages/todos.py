import streamlit as st
from database import db
from datetime import datetime, timedelta

st.markdown("## ✓ Todo List")
st.markdown("Stay organized and track your tasks")

# Create new todo section
with st.expander("➕ Add New Task", expanded=False):
    col1, col2 = st.columns([2, 1])
    with col1:
        todo_title = st.text_input("Task Title", placeholder="What do you need to do?", key="new_todo_title")
    with col2:
        todo_priority = st.selectbox("Priority", ["low", "medium", "high"], key="new_todo_priority")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        todo_category = st.text_input("Category", placeholder="e.g., work, personal", key="new_todo_category")
    with col2:
        todo_due_date = st.date_input("Due Date", key="new_todo_due_date")
    with col3:
        st.write("")  # Spacing
    
    todo_description = st.text_area(
        "Description",
        placeholder="Add details...",
        height=100,
        label_visibility="collapsed",
        key="new_todo_description"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Add Task", use_container_width=True):
            if todo_title.strip():
                db.create_todo(
                    todo_title,
                    todo_description,
                    str(todo_due_date),
                    todo_priority,
                    todo_category
                )
                st.success("✅ Task added!")
                st.rerun()
            else:
                st.error("Please enter a task title")
    with col2:
        if st.button("Clear", use_container_width=True):
            st.rerun()

st.markdown("---")

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    show_completed = st.checkbox("Show Completed", value=True)
with col2:
    priority_filter = st.selectbox("Priority", ["all", "high", "medium", "low"])
with col3:
    category_filter = st.text_input("Category Filter", placeholder="Leave empty for all")

# Get todos
all_todos = db.get_all_todos()

# Filter todos
filtered_todos = []
for todo in all_todos:
    # Filter by completion status
    if not show_completed and todo['completed']:
        continue
    
    # Filter by priority
    if priority_filter != "all" and todo['priority'] != priority_filter:
        continue
    
    # Filter by category
    if category_filter and todo['category'] != category_filter:
        continue
    
    filtered_todos.append(todo)

# Display stats
col1, col2, col3, col4 = st.columns(4)
with col1:
    total = len(all_todos)
    st.metric("Total Tasks", total, delta=None)
with col2:
    completed = sum(1 for t in all_todos if t['completed'])
    st.metric("Completed", completed)
with col3:
    pending = sum(1 for t in all_todos if not t['completed'])
    st.metric("Pending", pending)
with col4:
    high_priority = sum(1 for t in all_todos if t['priority'] == 'high' and not t['completed'])
    st.metric("High Priority", high_priority)

st.markdown("---")

# Display todos organized by status and priority
if filtered_todos:
    # Separate by completion status
    pending_todos = [t for t in filtered_todos if not t['completed']]
    completed_todos = [t for t in filtered_todos if t['completed']]
    
    # Show pending todos
    if pending_todos:
        st.markdown("### 📋 Pending Tasks")
        
        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        pending_todos.sort(key=lambda x: (priority_order.get(x['priority'], 3), x.get('due_date', '')))
        
        for todo in pending_todos:
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([0.5, 3, 1, 1, 1])
                
                with col1:
                    # Checkbox to mark complete
                    if st.checkbox("", value=False, key=f"complete_{todo['id']}"):
                        db.update_todo(todo['id'], completed=1)
                        st.rerun()
                
                with col2:
                    # Task info
                    st.markdown(f"### {todo['title']}")
                    if todo['description']:
                        st.caption(todo['description'][:100])
                    
                    # Tags
                    tags_html = ""
                    if todo['category']:
                        tags_html += f'<span class="tag">{todo["category"]}</span>'
                    if todo['due_date']:
                        tags_html += f'<span class="tag">📅 {todo["due_date"]}</span>'
                    
                    if tags_html:
                        st.markdown(tags_html, unsafe_allow_html=True)
                
                with col3:
                    # Priority badge
                    priority_colors = {
                        "high": "🔴",
                        "medium": "🟡",
                        "low": "🟢"
                    }
                    st.markdown(f"**{priority_colors.get(todo['priority'], '⚪')} {todo['priority'].title()}**")
                
                with col4:
                    # Edit button
                    if st.button("✏️ Edit", key=f"edit_{todo['id']}", use_container_width=True):
                        st.session_state.editing_todo_id = todo['id']
                        st.rerun()
                
                with col5:
                    # Delete button
                    if st.button("🗑️", key=f"delete_{todo['id']}", use_container_width=True):
                        db.delete_todo(todo['id'])
                        st.success("Task deleted")
                        st.rerun()
                
                st.divider()
    
    # Show completed todos
    if completed_todos:
        with st.expander(f"✅ Completed ({len(completed_todos)})"):
            for todo in completed_todos:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"~~{todo['title']}~~")
                    st.caption(f"Completed on {todo['updated_at'][:10]}")
                
                with col2:
                    if st.button("↩️ Undo", key=f"undo_{todo['id']}", use_container_width=True):
                        db.update_todo(todo['id'], completed=0)
                        st.rerun()
                
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_comp_{todo['id']}", use_container_width=True):
                        db.delete_todo(todo['id'])
                        st.rerun()
                
                st.divider()

else:
    st.info("📭 No tasks found. Create one to get started!")

# Edit todo modal
if st.session_state.get("editing_todo_id"):
    todo_id = st.session_state.editing_todo_id
    todo = db.get_todo(todo_id)
    
    if todo:
        st.markdown("---")
        st.markdown(f"### Edit Task: {todo['title']}")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            edit_title = st.text_input("Title", value=todo['title'])
        with col2:
            edit_priority = st.selectbox("Priority", ["low", "medium", "high"], index=["low", "medium", "high"].index(todo['priority']))
        
        edit_category = st.text_input("Category", value=todo['category'] or "")
        edit_description = st.text_area("Description", value=todo['description'] or "", height=100)
        
        if todo['due_date']:
            from datetime import datetime
            due_date_obj = datetime.strptime(todo['due_date'], '%Y-%m-%d').date()
            edit_due_date = st.date_input("Due Date", value=due_date_obj)
        else:
            edit_due_date = st.date_input("Due Date")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Changes", use_container_width=True):
                db.update_todo(
                    todo_id,
                    edit_title,
                    edit_description,
                    None,
                    str(edit_due_date),
                    edit_priority,
                    edit_category
                )
                st.session_state.editing_todo_id = None
                st.success("✅ Task updated!")
                st.rerun()
        
        with col2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.editing_todo_id = None
                st.rerun()