"""Sidebar navigation component for CodeGuru India."""
import streamlit as st


def render_sidebar() -> str:
    """Render navigation sidebar and return selected page."""
    with st.sidebar:
        st.title("🎓 CodeGuru India")
        
        # Language selector
        language_options = {
            "english": "🇬🇧 English",
            "hindi": "🇮🇳 हिंदी",
            "telugu": "🇮🇳 తెలుగు"
        }
        
        session_manager = st.session_state.session_manager
        current_lang = session_manager.get_language_preference()
        
        selected_lang = st.selectbox(
            "Language / भाषा / భాష",
            options=list(language_options.keys()),
            format_func=lambda x: language_options[x],
            index=list(language_options.keys()).index(current_lang),
            key="language_selector"
        )
        
        if selected_lang != current_lang:
            session_manager.set_language_preference(selected_lang)
            st.rerun()
        
        st.divider()
        
        # Navigation menu
        page_options = [
            ("Home", "🏠"),
            ("Upload Code", "📤"),
            ("Explanations", "💡"),
            ("Learning Paths", "🛤️"),
            ("Quizzes", "📝"),
            ("Flashcards", "🗂️"),
            ("Progress", "📊")
        ]
        
        selected_page = st.radio(
            "Navigation",
            options=[page[0] for page in page_options],
            format_func=lambda x: f"{[p[1] for p in page_options if p[0] == x][0]} {x}",
            index=0 if "current_page" not in st.session_state else 
                  [p[0] for p in page_options].index(st.session_state.current_page) 
                  if st.session_state.current_page in [p[0] for p in page_options] else 0
        )
        
        st.session_state.current_page = selected_page
        
        st.divider()
        
        # Progress indicator
        st.markdown("### 📈 Your Progress")
        st.progress(0.35, text="35% Complete")
        st.caption("Keep learning! 🚀")
    
    return selected_page
