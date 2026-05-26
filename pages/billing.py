import streamlit as st

st.markdown("# 💳 Billing & Subscription")

st.markdown("### Your Current Plan")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Plan", "Free Tier")

with col2:
    st.metric("Status", "Active")

with col3:
    st.metric("Days Remaining", "∞")

st.markdown("---")
st.markdown("### Available Plans")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### 🆓 Free
    - Unlimited journal entries
    - Unlimited notes
    - Basic styling
    - 1 user

    **$0/month**
    """)

with col2:
    st.markdown("""
    #### ⭐ Premium
    - All Free features
    - Advanced themes
    - Voice notes
    - Priority support
    - Export options

    **$4.99/month**
    """)

st.markdown("---")

st.markdown("### Account Information")
st.markdown(f"**Name:** {st.session_state.current_user['name']}")
st.markdown(f"**Email:** {st.session_state.current_user['email']}")

if st.button("Upgrade to Premium (Coming Soon)", disabled=True, use_container_width=True):
    pass

st.info("Premium features coming soon! 🚀")
