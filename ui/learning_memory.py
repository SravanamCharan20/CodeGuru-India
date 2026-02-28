"""Persistent learning memory page."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

import streamlit as st
from ui.design_system import section_header, spacing


def render_learning_memory(session_manager, memory_store, chat_learning_generator):
    """Render persistent memory of uploaded sessions, chat, and generated revision material."""
    section_header(
        "Learning Memory",
        "All uploaded code/repositories, your chat history, and generated revision material",
    )

    if not memory_store:
        st.info("Learning memory store is not available yet. Refresh the app and try again.")
        return

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("User session not initialized.")
        return

    sessions = memory_store.list_sessions(user_id=user_id, limit=100)
    if not sessions:
        st.info("No saved sessions yet. Upload code or a repository and start chatting to build memory.")
        return

    if "selected_memory_session_id" not in st.session_state:
        st.session_state.selected_memory_session_id = sessions[0]["id"]

    selected_id = st.session_state.selected_memory_session_id

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### Sessions")
        for item in sessions:
            label = _session_label(item)
            if st.button(label, key=f"memory_session_{item['id']}", use_container_width=True):
                st.session_state.selected_memory_session_id = item["id"]
                st.rerun()

    with col2:
        session = memory_store.get_session(selected_id)
        if not session:
            st.warning("Selected session not found.")
            return

        st.markdown(f"### {session['title']}")
        st.caption(
            f"Type: {session['source_type']} | Language: {session['language']} | Last Updated: {_fmt_dt(session['updated_at'])}"
        )
        if session.get("summary"):
            st.info(session["summary"])

        chat_messages = memory_store.get_chat_messages(selected_id, limit=500)

        actions_col1, actions_col2, actions_col3 = st.columns(3)
        with actions_col1:
            if st.button("Use For Chat", use_container_width=True):
                st.session_state.current_analysis_session_id = selected_id
                st.session_state.current_page = "Codebase Chat"
                st.rerun()
        with actions_col2:
            if st.button(
                "Generate Flashcards",
                use_container_width=True,
                disabled=(not chat_messages or not chat_learning_generator),
            ):
                cards = chat_learning_generator.generate_flashcards(
                    chat_messages,
                    language=st.session_state.get("selected_language", "english"),
                )
                memory_store.save_artifact(selected_id, "chat_flashcards", cards, replace=True)
                st.success(f"Generated {len(cards)} flashcards from chat history.")
                st.rerun()
        with actions_col3:
            if st.button(
                "Generate Quiz",
                use_container_width=True,
                disabled=(not chat_messages or not chat_learning_generator),
            ):
                quiz = chat_learning_generator.generate_quiz(
                    chat_messages,
                    language=st.session_state.get("selected_language", "english"),
                )
                memory_store.save_artifact(selected_id, "chat_quiz", quiz, replace=True)
                st.success(f"Generated {len(quiz.get('questions', []))} quiz questions from chat history.")
                st.rerun()

        spacing("sm")
        tabs = st.tabs(["Chat History", "Flashcards", "Quiz"])

        with tabs[0]:
            _render_chat_history(chat_messages)

        with tabs[1]:
            cards = memory_store.get_artifact(selected_id, "chat_flashcards") or []
            _render_flashcards(cards)

        with tabs[2]:
            quiz = memory_store.get_artifact(selected_id, "chat_quiz") or {}
            _render_quiz(quiz)


def _session_label(item: Dict[str, Any]) -> str:
    source = "Repo" if item["source_type"] == "repository" else "Code"
    timestamp = _fmt_dt(item["updated_at"])
    return f"{source} | {item['title']} | {timestamp}"


def _fmt_dt(value: str) -> str:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return value


def _render_chat_history(messages: List[Dict[str, Any]]) -> None:
    if not messages:
        st.info("No chat history saved for this session yet.")
        return

    for message in messages:
        role = message.get("role", "assistant")
        prefix = "You" if role == "user" else "Assistant"
        st.markdown(f"**{prefix}:** {message.get('content', '')}")
        st.caption(_fmt_dt(message.get("created_at", "")))
        st.divider()


def _render_flashcards(cards: List[Dict[str, Any]]) -> None:
    if not cards:
        st.info("No flashcards generated yet.")
        return

    st.caption(f"{len(cards)} flashcards")
    for index, card in enumerate(cards, start=1):
        with st.expander(f"Card {index}: {card.get('front', 'Question')}"):
            st.write(card.get("back", ""))


def _render_quiz(quiz: Dict[str, Any]) -> None:
    questions = quiz.get("questions", [])
    if not questions:
        st.info("No quiz generated yet.")
        return

    st.caption(f"{len(questions)} questions")
    for index, question in enumerate(questions, start=1):
        with st.expander(f"Q{index}: {question.get('question_text', 'Question')}"):
            options = question.get("options", [])
            for option in options:
                if option == question.get("correct_answer"):
                    st.write(f"- ✅ {option}")
                else:
                    st.write(f"- {option}")
            if question.get("explanation"):
                st.caption(question["explanation"])
