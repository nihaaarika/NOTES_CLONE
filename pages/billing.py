import streamlit as st
from modules.database import db
from datetime import datetime

st.title("💳 Billing & Expenses")
st.markdown("*Track expenses for trips, group outings, or shared costs.*")
st.markdown("---")

user_id = st.session_state.current_user['id']

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### ➕ Add Expense")
    description = st.text_input("What did you buy?", placeholder="Coffee with friends...")

with col2:
    amount = st.number_input("Amount", min_value=0.0, step=0.01, value=0.0)

with col3:
    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Entertainment", "Shopping", "Activities", "Accommodation", "Other"]
    )

col1, col2, col3 = st.columns(3)

with col1:
    paid_by = st.text_input("Paid by (name/initials)", placeholder="Your name")

with col2:
    expense_date = st.date_input("Date", datetime.now().date())

with col3:
    if st.button("💾 Add", use_container_width=True, type="primary"):
        if description.strip() and amount > 0 and paid_by.strip():
            db.create_expense(
                user_id,
                description,
                amount,
                category,
                paid_by
            )
            st.success("✅ Expense added!")
            st.rerun()
        else:
            st.error("Fill all fields")

st.markdown("---")

expenses = db.get_expenses(user_id)

if expenses:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Spent", f"${sum(e['amount'] for e in expenses):.2f}")
    with col2:
        st.metric("Expenses", len(expenses))
    with col3:
        categories = set(e['category'] for e in expenses)
        st.metric("Categories", len(categories))
    with col4:
        people = set(e['paid_by'] for e in expenses)
        st.metric("People", len(people))

    st.markdown("### 📋 Expense List")

    for expense in expenses:
        col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 0.5])

        with col1:
            st.markdown(f"**{expense['description']}** ({expense['category']})")
            st.caption(f"Paid by: {expense['paid_by']}")

        with col2:
            st.markdown(f"**${expense['amount']:.2f}**")
            st.caption(expense['expense_date'])

        with col3:
            st.caption("")

        with col4:
            if st.button("🗑️", key=f"del_{expense['id']}", help="Delete"):
                db.delete_expense(expense['id'])
                st.rerun()

    st.markdown("### 💰 Summary by Person")

    people_totals = {}
    for exp in expenses:
        paid_by = exp['paid_by']
        people_totals[paid_by] = people_totals.get(paid_by, 0) + exp['amount']

    for person, total in sorted(people_totals.items(), key=lambda x: x[1], reverse=True):
        st.markdown(f"**{person}:** ${total:.2f}")

else:
    st.info("💳 No expenses yet. Add your first expense!")
