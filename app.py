"""Main entry point for CodeGuru India application."""
import streamlit as st
from session_manager import SessionManager


def main():
    """Initialize and run the Streamlit application."""
    setup_page_config()
    initialize_session_state()
    
    # Import UI components
    from ui.sidebar import render_sidebar
    from ui.code_upload import render_code_upload
    from ui.explanation_view import render_explanation_view
    from ui.learning_path import render_learning_path
    from ui.quiz_view import render_quiz_view
    from ui.flashcard_view import render_flashcard_view
    from ui.progress_dashboard import render_progress_dashboard
    
    # Render sidebar and get selected page
    selected_page = render_sidebar()
    
    # Route to selected page
    route_to_page(selected_page)


def setup_page_config():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="CodeGuru India",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def initialize_session_state():
    """Initialize session state variables."""
    if "session_manager" not in st.session_state:
        st.session_state.session_manager = SessionManager()
    
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"


def route_to_page(page: str):
    """Route to the selected page component."""
    from ui.code_upload import render_code_upload
    from ui.explanation_view import render_explanation_view
    from ui.learning_path import render_learning_path
    from ui.quiz_view import render_quiz_view
    from ui.flashcard_view import render_flashcard_view
    from ui.progress_dashboard import render_progress_dashboard
    
    if page == "Home":
        st.title("🎓 Welcome to CodeGuru India")
        st.markdown("""
        ### Learn Code Faster with AI-Powered Explanations
        
        CodeGuru India helps you understand complex codebases through:
        - 🔍 **Smart Code Analysis** - Upload files or GitHub repos
        - 🗣️ **Voice Queries** - Ask questions in English, Hindi, or Telugu
        - 📚 **Interactive Learning** - Flashcards, quizzes, and learning paths
        - 📊 **Progress Tracking** - Monitor your growth over time
        - 🎯 **Simple Analogies** - Complex concepts explained simply
        
        Get started by uploading code or selecting a learning path!
        """)
    elif page == "Upload Code":
        render_code_upload()
    elif page == "Explanations":
        render_explanation_view()
    elif page == "Learning Paths":
        render_learning_path()
    elif page == "Quizzes":
        render_quiz_view()
    elif page == "Flashcards":
        render_flashcard_view()
    elif page == "Progress":
        render_progress_dashboard()


if __name__ == "__main__":
    main()
