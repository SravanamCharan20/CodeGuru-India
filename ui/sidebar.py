"""Sidebar navigation component."""
import streamlit as st


def render_sidebar() -> str:
    """
    Render sidebar navigation and return selected page.
    
    Returns:
        Selected page name
    """
    with st.sidebar:
        # Logo and title
        st.markdown("# 🎓 CodeGuru India")
        st.markdown('<p style="color: #666666; font-size: 14px; margin-top: -16px;">AI-Powered Code Learning</p>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Language selector
        st.markdown("### Language")
        language = st.selectbox(
            "Select Language",
            options=["English", "हिंदी (Hindi)", "తెలుగు (Telugu)"],
            label_visibility="collapsed"
        )
        
        # Store language in session state
        language_map = {
            "English": "english",
            "हिंदी (Hindi)": "hindi",
            "తెలుగు (Telugu)": "telugu"
        }
        st.session_state.selected_language = language_map.get(language, "english")
        
        st.markdown("---")
        
        # Navigation
        st.markdown("### Navigation")
        
        # Get current page from session state
        if "current_page" not in st.session_state:
            st.session_state.current_page = "Home"
        
        current_page = st.session_state.current_page
        
        # Navigation buttons (demo-focused)
        pages = [
            ("Home", "🏠"),
            ("Upload Code", "📤"),
            ("Codebase Chat", "💬"),
            ("Learning Memory", "🧠"),
            ("Quizzes", "📝"),
            ("Flashcards", "🎴"),
            ("Progress", "📊")
        ]

        valid_pages = {name for name, _ in pages}
        if current_page not in valid_pages:
            current_page = "Home"
            st.session_state.current_page = "Home"
        
        for page_name, icon in pages:
            # Determine button type based on current page
            button_type = "primary" if page_name == current_page else "secondary"
            
            # Create button
            if st.button(
                f"{icon} {page_name}",
                key=f"nav_{page_name}",
                type=button_type
            ):
                st.session_state.current_page = page_name
                st.rerun()
        
        st.markdown("---")
        
        # Backend status
        st.markdown("### Status")
        
        if st.session_state.get("backend_initialized", False):
            st.success("✓ AI Connected")
        else:
            if st.session_state.get("backend_error"):
                st.warning("⚠️ Using Mock Data")
                with st.expander("Details"):
                    st.caption(st.session_state.backend_error)
            else:
                st.info("⏳ Initializing...")
        
        st.markdown("---")
        
        # Help section
        with st.expander("ℹ️ Help"):
            st.markdown("""
            **How to use:**
            1. Upload repository or file
            2. Review Starter Guide
            3. Ask doubts in Codebase Chat
            4. Practice in Flashcards/Quizzes
            
            **Tip:** Use the sidebar to close/open it
            """)
    
    return st.session_state.current_page
