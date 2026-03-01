"""Sidebar navigation component."""

import streamlit as st


def render_sidebar() -> str:
    """
    Render sidebar navigation and return selected page.

    Returns:
        Selected page name
    """
    with st.sidebar:
        st.markdown(
            """
            <div class="cg-sidebar-brand">
                <div class="title">CodeGuru India</div>
                <div class="sub">AI Code Learning Platform</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        language_options = ["English", "हिंदी (Hindi)", "తెలుగు (Telugu)"]
        language_map = {
            "English": "english",
            "हिंदी (Hindi)": "hindi",
            "తెలుగు (Telugu)": "telugu",
        }
        reverse_language_map = {value: key for key, value in language_map.items()}
        current_lang_key = st.session_state.get("selected_language", "english")
        default_label = reverse_language_map.get(current_lang_key, "English")

        st.markdown('<div class="cg-nav-caption">Language</div>', unsafe_allow_html=True)
        selected_language_label = st.selectbox(
            "Language",
            options=language_options,
            index=language_options.index(default_label) if default_label in language_options else 0,
            label_visibility="collapsed",
            key="sidebar_language_selector",
        )
        st.session_state.selected_language = language_map.get(selected_language_label, "english")
        if "session_manager" in st.session_state:
            st.session_state.session_manager.set_language_preference(st.session_state.selected_language)

        st.markdown('<div class="cg-nav-caption">Navigation</div>', unsafe_allow_html=True)
        pages = [
            "Home",
            "Upload Code",
            "Codebase Chat",
            "Explanations",
            "Learning Paths",
            "Learning Memory",
            "Progress",
        ]
        page_labels = {
            "Home": "🏠 Home",
            "Upload Code": "📤 Upload Code",
            "Codebase Chat": "💬 Codebase Chat",
            "Explanations": "🧾 Explanations",
            "Learning Paths": "🛤️ Learning Paths",
            "Learning Memory": "🧠 Learning Memory",
            "Progress": "📊 Progress",
        }

        if "current_page" not in st.session_state or st.session_state.current_page not in pages:
            st.session_state.current_page = "Home"

        selected_page = st.radio(
            "Pages",
            options=pages,
            index=pages.index(st.session_state.current_page),
            format_func=lambda item: page_labels.get(item, item),
            label_visibility="collapsed",
            key="sidebar_page_selector",
        )

        if selected_page != st.session_state.current_page:
            st.session_state.current_page = selected_page
            st.rerun()

        st.markdown('<div class="cg-nav-caption">System</div>', unsafe_allow_html=True)
        memory_backend = st.session_state.get("memory_backend", "session")
        if st.session_state.get("backend_initialized", False):
            st.success("AI connected")
            st.caption(f"Memory backend: {memory_backend}")
        else:
            if st.session_state.get("backend_error"):
                st.warning("Fallback mode active")
                with st.expander("Initialization details"):
                    st.code(st.session_state.backend_error)
            else:
                st.info("Initializing services...")

        with st.expander("How to demo effectively"):
            st.markdown(
                """
                1. Upload a repository and complete analysis.
                2. Ask architecture + feature questions in Codebase Chat.
                3. Switch language and show voice-to-query flow.
                4. Open Learning Memory for quizzes/flashcards.
                5. Show Progress dashboard.
                """
            )

    return st.session_state.current_page
