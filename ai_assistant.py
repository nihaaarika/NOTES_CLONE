import streamlit as st
from ai_generator import get_ai_generator

st.markdown("## ✨ AI Writing Assistant")
st.markdown("Enhance your writing with AI-powered suggestions")

# Settings
with st.sidebar:
    st.markdown("### AI Settings")
    
    use_api = st.checkbox(
        "Use OpenAI API",
        value=False,
        help="Enable for better quality suggestions (requires API key)"
    )
    
    if use_api:
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-..."
        )
        if api_key:
            st.session_state.openai_api_key = api_key
    
    st.markdown("---")
    st.info("💡 AI Assistant is running in template mode. Add an OpenAI API key for enhanced suggestions.")

# Get AI generator
ai = get_ai_generator(use_openai=st.session_state.get("use_api", False))

# Tabs for different features
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "✍️ Continue Writing",
    "💡 Brainstorm",
    "✓ Check Grammar",
    "📝 Summarize",
    "📋 Generate Title"
])

# Tab 1: Continue Writing
with tab1:
    st.markdown("### Continue Writing")
    st.markdown("Let AI help you finish your thoughts")
    
    writing_text = st.text_area(
        "Your text",
        placeholder="Start typing...",
        height=200,
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        length = st.slider("Continuation length", 50, 300, 150, step=50)
    
    with col2:
        tone = st.selectbox("Tone", ["Professional", "Casual", "Creative"])
    
    with col3:
        st.write("")  # Spacing
    
    if st.button("🚀 Generate Continuation", use_container_width=True):
        if writing_text.strip():
            with st.spinner("Generating..."):
                continuation = ai.generate_continuation(writing_text, length)
                
                st.success("✅ Done!")
                st.markdown("#### Suggested Continuation:")
                st.info(continuation)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📋 Copy to Clipboard", key="copy_continuation"):
                        st.success("Copied!")
                with col2:
                    if st.button("🔄 Generate Again", key="regen_continuation"):
                        st.rerun()
        else:
            st.warning("Please enter some text first")

# Tab 2: Brainstorm
with tab2:
    st.markdown("### Brainstorm Ideas")
    st.markdown("Generate creative ideas on any topic")
    
    topic = st.text_input(
        "Topic",
        placeholder="What do you want to brainstorm about?",
        label_visibility="collapsed"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_ideas = st.slider("Number of ideas", 3, 10, 5)
    
    with col2:
        st.write("")  # Spacing
    
    if st.button("💭 Brainstorm Ideas", use_container_width=True):
        if topic.strip():
            with st.spinner("Generating ideas..."):
                ideas = ai.brainstorm_ideas(topic, num_ideas)
                
                st.success("✅ Ideas generated!")
                st.markdown("#### Your Ideas:")
                
                for idx, idea in enumerate(ideas, 1):
                    # Clean up bullet points if they exist
                    idea_text = str(idea).lstrip('- •0123456789.') if isinstance(idea, str) else str(idea)
                    st.markdown(f"**{idx}.** {idea_text}")
                
                if st.button("🔄 Generate More Ideas"):
                    st.rerun()
        else:
            st.warning("Please enter a topic")

# Tab 3: Check Grammar
with tab3:
    st.markdown("### Check Grammar & Style")
    st.markdown("Get suggestions to improve your writing")
    
    grammar_text = st.text_area(
        "Your text",
        placeholder="Paste text to check...",
        height=200,
        label_visibility="collapsed"
    )
    
    if st.button("🔍 Check Grammar", use_container_width=True):
        if grammar_text.strip():
            with st.spinner("Checking..."):
                result = ai.check_grammar(grammar_text)
                
                st.success("✅ Check complete!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Corrected Version:")
                    st.info(result.get('corrected', grammar_text))
                
                with col2:
                    st.markdown("#### Suggestions:")
                    suggestions = result.get('suggestions', [])
                    if suggestions:
                        for suggestion in suggestions:
                            st.write(f"• {suggestion}")
                    else:
                        st.success("No issues found!")
        else:
            st.warning("Please enter some text")

# Tab 4: Summarize
with tab4:
    st.markdown("### Summarize Text")
    st.markdown("Get a concise summary of your text")
    
    text_to_summarize = st.text_area(
        "Your text",
        placeholder="Paste longer text to summarize...",
        height=200,
        label_visibility="collapsed"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        summary_length = st.slider("Summary length", 50, 200, 100, step=50)
    
    with col2:
        st.write("")  # Spacing
    
    if st.button("📄 Summarize", use_container_width=True):
        if text_to_summarize.strip():
            with st.spinner("Summarizing..."):
                summary = ai.summarize(text_to_summarize, summary_length)
                
                st.success("✅ Summary created!")
                st.markdown("#### Summary:")
                st.info(summary)
                
                if st.button("📋 Copy Summary"):
                    st.success("Copied!")
        else:
            st.warning("Please enter some text")

# Tab 5: Generate Title
with tab5:
    st.markdown("### Generate Title")
    st.markdown("Create a catchy title for your content")
    
    content_for_title = st.text_area(
        "Your content",
        placeholder="Paste your content to generate a title...",
        height=200,
        label_visibility="collapsed"
    )
    
    if st.button("✨ Generate Title", use_container_width=True):
        if content_for_title.strip():
            with st.spinner("Generating title..."):
                title = ai.generate_title(content_for_title)
                
                st.success("✅ Title generated!")
                st.markdown("#### Suggested Title:")
                st.info(title)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📋 Copy Title", key="copy_title"):
                        st.success("Copied!")
                with col2:
                    if st.button("🔄 Generate Another", key="regen_title"):
                        st.rerun()
        else:
            st.warning("Please enter some content")

st.markdown("---")

# Tips section
with st.expander("💡 Tips for Best Results"):
    st.markdown("""
    **Writing Continuation:**
    - Start with a clear idea of where you want to go
    - The more context you provide, the better the suggestions
    
    **Brainstorming:**
    - Be specific with your topic
    - Ask for more ideas if the first batch doesn't suit you
    
    **Grammar Check:**
    - Works best with properly formatted text
    - The tool focuses on major issues
    
    **Summarization:**
    - Longer texts work better for summarization
    - Minimum 50 words recommended
    
    **Title Generation:**
    - More content = better titles
    - The tool analyzes your main ideas
    """)