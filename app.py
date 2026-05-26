import streamlit as st
import os
from pathlib import Path
from modules.database import db
import re

# Page configuration
st.set_page_config(
    page_title="Secret Diary",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize session state
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "setup_step" not in st.session_state:
    st.session_state.setup_step = -1
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

# Custom CSS for Secret Diary
def inject_custom_css():
    css = """
    <style>
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Geist', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    .stMainBlockContainer {
        padding: 3rem 2.5rem;
    }

    .setup-container {
        max-width: 500px;
        margin: 0 auto;
        background: white;
        border-radius: 16px;
        padding: 3rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }

    .setup-title {
        text-align: center;
        color: #667eea;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .setup-subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }

    .progress-bar {
        width: 100%;
        height: 4px;
        background: #e0e0e0;
        border-radius: 2px;
        margin-bottom: 2rem;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        transition: width 0.3s ease;
    }

    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        cursor: pointer;
        width: 100%;
        margin-top: 1rem;
    }

    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #e0e0e0 !important;
        padding: 0.75rem !important;
    }

    .stPasswordInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #e0e0e0 !important;
        padding: 0.75rem !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

inject_custom_css()

# SETUP FLOW
if st.session_state.setup_step >= 0:
    st.markdown('<div class="setup-container">', unsafe_allow_html=True)

    progress = (st.session_state.setup_step + 1) / 4 * 100
    st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width: {progress}%"></div></div>', unsafe_allow_html=True)

    # Step 0: Name
    if st.session_state.setup_step == 0:
        st.markdown('<div class="setup-title">🔒 Secret Diary</div>', unsafe_allow_html=True)
        st.markdown('<div class="setup-subtitle">Step 1 of 4</div>', unsafe_allow_html=True)
        st.markdown("### What's your name?")
        name = st.text_input("Full Name", key="setup_name")
        if st.button("Next"):
            if name.strip():
                st.session_state.user_data['name'] = name.strip()
                st.session_state.setup_step = 1
                st.rerun()
            else:
                st.error("Please enter your name")

    # Step 1: Email
    elif st.session_state.setup_step == 1:
        st.markdown('<div class="setup-title">🔒 Secret Diary</div>', unsafe_allow_html=True)
        st.markdown('<div class="setup-subtitle">Step 2 of 4</div>', unsafe_allow_html=True)
        st.markdown("### Your email (for recovery)")
        email = st.text_input("Email", key="setup_email")
        if st.button("Next"):
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(email_pattern, email):
                st.session_state.user_data['email'] = email.strip()
                st.session_state.setup_step = 2
                st.rerun()
            else:
                st.error("Please enter a valid email")

    # Step 2: Phone
    elif st.session_state.setup_step == 2:
        st.markdown('<div class="setup-title">🔒 Secret Diary</div>', unsafe_allow_html=True)
        st.markdown('<div class="setup-subtitle">Step 3 of 4</div>', unsafe_allow_html=True)
        st.markdown("### Your phone number")
        phone = st.text_input("Phone Number", key="setup_phone")
        if st.button("Next"):
            if phone.strip() and len(phone) >= 10:
                st.session_state.user_data['phone'] = phone.strip()
                st.session_state.setup_step = 3
                st.rerun()
            else:
                st.error("Please enter a valid phone number")

    # Step 3: Password
    elif st.session_state.setup_step == 3:
        st.markdown('<div class="setup-title">🔒 Secret Diary</div>', unsafe_allow_html=True)
        st.markdown('<div class="setup-subtitle">Step 4 of 4</div>', unsafe_allow_html=True)
        st.markdown("### Create your secret password")
        password = st.text_input("Password", type="password", key="setup_pass")
        confirm_password = st.text_input("Confirm Password", type="password", key="setup_pass_confirm")

        if st.button("Create Account"):
            if password != confirm_password:
                st.error("Passwords don't match")
            elif len(password) < 8:
                st.error("Password must be at least 8 characters")
            elif not any(c.isupper() for c in password):
                st.error("Password must contain uppercase letter")
            elif not any(c.isdigit() for c in password):
                st.error("Password must contain a number")
            else:
                user_id = db.create_user(
                    st.session_state.user_data['name'],
                    st.session_state.user_data['email'],
                    st.session_state.user_data['phone'],
                    password
                )
                st.session_state.is_authenticated = True
                st.session_state.current_user = {'id': user_id, 'name': st.session_state.user_data['name']}
                st.session_state.setup_step = -1
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# LOGIN FLOW
elif not st.session_state.is_authenticated:
    st.markdown('<div class="setup-container">', unsafe_allow_html=True)
    st.markdown('<div class="setup-title">🔒 Secret Diary</div>', unsafe_allow_html=True)
    st.markdown('<div class="setup-subtitle">Welcome back</div>', unsafe_allow_html=True)
    st.markdown("### Login to your diary")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        user = db.verify_user(email, password)
        if user:
            st.session_state.is_authenticated = True
            st.session_state.current_user = user
            st.rerun()
        else:
            st.error("Invalid email or password")

    st.markdown("---")
    if st.button("Create New Account"):
        st.session_state.setup_step = 0
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# MAIN APP (After Login)
else:
    # Sidebar with logout
    with st.sidebar:
        st.markdown(f"### 🔒 {st.session_state.current_user['name']}")
        st.markdown("---")

        selected = st.radio(
            "Menu",
            ["📝 Journaling", "💬 Secret Talk", "✨ Manifestations", "📅 Everyday Notes", "💳 Billing"],
            label_visibility="collapsed"
        )

        st.markdown("---")
        if st.button("🚪 Logout"):
            st.session_state.is_authenticated = False
            st.session_state.current_user = None
            st.rerun()

    # Route to pages
    pages = {
        "📝 Journaling": "pages/journaling.py",
        "💬 Secret Talk": "pages/secret_talk.py",
        "✨ Manifestations": "pages/manifestations.py",
        "📅 Everyday Notes": "pages/everyday_notes.py",
        "💳 Billing": "pages/billing.py",
    }

    Path("pages").mkdir(exist_ok=True)

    if selected in pages:
        page_file = pages[selected]
        if os.path.exists(page_file):
            with open(page_file, 'r', encoding='utf-8') as f:
                page_code = f.read()
            exec(page_code)
        else:
            st.info(f"Page {page_file} not found")