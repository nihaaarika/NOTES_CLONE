import streamlit as st
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Notion Clone",
    page_icon="📔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "accent_color" not in st.session_state:
    st.session_state.accent_color = "#6366f1"

# Custom CSS for professional styling
def inject_custom_css():
    css = """
    <style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    :root {
        --primary: #6366f1;
        --secondary: #8b5cf6;
        --accent: #ec4899;
        --bg-light: #ffffff;
        --bg-dark: #0f172a;
        --text-light: #1e293b;
        --text-dark: #e2e8f0;
        --border-light: #e2e8f0;
        --border-dark: #1e293b;
    }
    
    /* Global Typography */
    body {
        font-family: 'Geist', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    /* Streamlit Overrides */
    .stMainBlockContainer {
        padding: 2rem 2.5rem;
        background: transparent;
    }
    
    .stSidebar {
        background: linear-gradient(180deg, #1a1f35 0%, #0f172a 100%);
        padding: 1.5rem;
    }
    
    .stSidebar [data-testid="stMarkdownContainer"] {
        color: #e2e8f0;
    }
    
    /* Card Styling */
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .card:hover {
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.15);
        border-color: #6366f1;
        transform: translateY(-2px);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button:hover {
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4);
        transform: translateY(-2px);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px;
        padding: 0.75rem !important;
        font-family: 'Geist Mono', monospace;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    /* Sidebar Navigation */
    .sidebar-nav {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        margin-bottom: 2rem;
    }
    
    .sidebar-nav-item {
        padding: 1rem;
        border-radius: 8px;
        color: #cbd5e1;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .sidebar-nav-item:hover {
        background: rgba(99, 102, 241, 0.1);
        color: #6366f1;
    }
    
    .sidebar-nav-item.active {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
    }
    
    /* Code Block */
    .code-block {
        background: #0f172a;
        border-radius: 8px;
        padding: 1rem;
        color: #e2e8f0;
        font-family: 'Geist Mono', monospace;
        overflow-x: auto;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeInUp 0.5s ease-out;
    }
    
    /* Tags */
    .tag {
        display: inline-block;
        background: #e0e7ff;
        color: #6366f1;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

inject_custom_css()

# Sidebar Navigation
with st.sidebar:
    st.markdown("### 📔 **Notion Clone**")
    st.markdown("---")
    
    selected = st.radio(
        "Navigation",
        ["📝 Notes", "✓ Todo List", "📖 Diary", "✨ AI Assistant", "⚙️ Settings"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown(
        """
        <div style='font-size: 0.85rem; color: #cbd5e1; margin-top: 2rem;'>
        **Your personal productivity hub**
        
        Keep notes, manage todos, and write your diary—all in one beautiful place.
        </div>
        """,
        unsafe_allow_html=True
    )

# Route to pages
pages = {
    "📝 Notes": "pages/notes.py",
    "✓ Todo List": "pages/todos.py",
    "📖 Diary": "pages/diary.py",
    "✨ AI Assistant": "pages/ai_assistant.py",
    "⚙️ Settings": "pages/settings.py",
}

# Create pages directory if it doesn't exist
Path("pages").mkdir(exist_ok=True)

# Display selected page
if selected in pages:
    page_file = pages[selected]
    if os.path.exists(page_file):
        with open(page_file, 'r') as f:
            page_code = f.read()
        exec(page_code)
    else:
        st.info(f"Page {page_file} not found. Creating pages now...")