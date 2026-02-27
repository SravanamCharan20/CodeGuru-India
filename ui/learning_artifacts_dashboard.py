"""
Learning Artifacts Dashboard UI Component.

Displays generated flashcards, quizzes, learning paths, and concept summaries.
"""

import streamlit as st
import logging

logger = logging.getLogger(__name__)


def render_learning_artifacts_dashboard(session_manager):
    """
    Render learning artifacts dashboard.
    
    Args:
        session_manager: SessionManager instance
    """
    st.header("📚 Learning Materials")
    
    # Get artifacts from session
    artifacts = session_manager.get_learning_artifacts()
    
    if not artifacts or not any([
        artifacts.get('flashcards'),
        artifacts.get('quizzes'),
        artifacts.get('learning_paths'),
        artifacts.get('concept_summary')
    ]):
        st.info("No learning materials generated yet. Complete the analysis first.")
        return
    
    # Language display and switching
    current_language = artifacts.get('concept_summary', {}).get('language', 'english')
    
    col1, col2 = st.columns([3, 1])
    with col1:
        language_names = {'english': 'English', 'hindi': 'हिंदी', 'telugu': 'తెలుగు'}
        st.write(f"**Current Language**: {language_names.get(current_language, 'English')}")
    with col2:
        if st.button("🌐 Change Language"):
            st.session_state['show_language_selector'] = True
    
    # Language switching dialog
    if st.session_state.get('show_language_selector', False):
        with st.expander("🌐 Select Language", expanded=True):
            st.info("Note: Changing language will regenerate all learning materials. This may take a moment.")
            new_language = st.selectbox(
                "Choose language",
                ["english", "hindi", "telugu"],
                format_func=lambda x: {"english": "English", "hindi": "हिंदी", "telugu": "తెలుగు"}[x],
                index=["english", "hindi", "telugu"].index(current_language)
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✓ Apply", type="primary"):
                    if new_language != current_language:
                        st.session_state['selected_language'] = new_language
                        st.session_state['regenerate_artifacts'] = True
                        st.info(f"Language changed to {new_language}. Please go back to the Analyze step to regenerate materials.")
                    st.session_state['show_language_selector'] = False
                    st.rerun()
            with col2:
                if st.button("✗ Cancel"):
                    st.session_state['show_language_selector'] = False
                    st.rerun()
    
    st.divider()
    
    # Create tabs for different artifact types
    tabs = st.tabs(["📝 Concept Summary", "🎴 Flashcards", "❓ Quizzes", "🗺️ Learning Path"])
    
    # Tab 1: Concept Summary
    with tabs[0]:
        _render_concept_summary(artifacts.get('concept_summary', {}))
    
    # Tab 2: Flashcards
    with tabs[1]:
        _render_flashcards(artifacts.get('flashcards', []))
    
    # Tab 3: Quizzes
    with tabs[2]:
        _render_quizzes(artifacts.get('quizzes', []))
    
    # Tab 4: Learning Path
    with tabs[3]:
        _render_learning_path(artifacts.get('learning_paths', []))


def _render_concept_summary(concept_summary):
    """Render concept summary section."""
    if not concept_summary:
        st.info("No concept summary available")
        return
    
    st.subheader("Key Concepts")
    
    total = concept_summary.get('total_concepts', 0)
    st.metric("Total Concepts", total)
    
    # Show top concepts
    top_concepts = concept_summary.get('top_concepts', [])
    if top_concepts:
        st.write("**Top Concepts:**")
        for concept in top_concepts:
            with st.expander(f"🔹 {concept.get('name', 'Unknown')}", expanded=False):
                st.write(f"**Category**: {concept.get('category', 'general').title()}")
                st.write(f"**Description**: {concept.get('description', 'No description')}")
    
    # Show by category
    categories = concept_summary.get('categories', {})
    if categories:
        st.divider()
        st.write("**By Category:**")
        for category, concepts in categories.items():
            with st.expander(f"📂 {category.title()} ({len(concepts)})", expanded=False):
                for concept in concepts[:5]:  # Show first 5
                    st.write(f"- **{concept.get('name')}**: {concept.get('description', 'No description')[:100]}...")


def _render_flashcards(flashcards):
    """Render flashcards section."""
    if not flashcards:
        st.info("No flashcards generated")
        return
    
    st.write(f"**Total Flashcards**: {len(flashcards)}")
    
    # Flashcard navigation
    if 'current_flashcard_index' not in st.session_state:
        st.session_state.current_flashcard_index = 0
    
    if flashcards:
        current_idx = st.session_state.current_flashcard_index
        flashcard = flashcards[current_idx]
        
        # Display flashcard
        st.write(f"**Card {current_idx + 1} of {len(flashcards)}**")
        st.write(f"**Category**: {flashcard.concept_category.title()}")
        st.write(f"**Difficulty**: {flashcard.difficulty.title()}")
        
        # Card content
        with st.container():
            st.markdown(f"### Question")
            st.info(flashcard.front)
            
            if st.button("Show Answer", key=f"show_answer_{current_idx}"):
                st.session_state[f'show_answer_{current_idx}'] = True
            
            if st.session_state.get(f'show_answer_{current_idx}', False):
                st.markdown(f"### Answer")
                st.success(flashcard.back)
                
                # Show code evidence
                if flashcard.code_evidence:
                    with st.expander("📄 View Code", expanded=False):
                        for evidence in flashcard.code_evidence:
                            st.code(evidence.code_snippet or "Code snippet not available", language="python")
                            st.caption(f"From: {evidence.file_path} (lines {evidence.line_start}-{evidence.line_end})")
        
        # Navigation
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⬅️ Previous", disabled=current_idx == 0):
                st.session_state.current_flashcard_index -= 1
                st.rerun()
        with col2:
            st.write(f"{current_idx + 1} / {len(flashcards)}")
        with col3:
            if st.button("Next ➡️", disabled=current_idx >= len(flashcards) - 1):
                st.session_state.current_flashcard_index += 1
                st.rerun()


def _render_quizzes(quizzes):
    """Render quizzes section."""
    if not quizzes:
        st.info("No quizzes generated")
        return
    
    st.write(f"**Total Quizzes**: {len(quizzes)}")
    
    # Select quiz
    if len(quizzes) > 1:
        quiz_idx = st.selectbox("Select Quiz", range(len(quizzes)), format_func=lambda x: f"Quiz {x+1}")
    else:
        quiz_idx = 0
    
    quiz = quizzes[quiz_idx]
    questions = quiz.get('questions', [])
    
    if not questions:
        st.info("No questions in this quiz")
        return
    
    st.write(f"**Questions**: {len(questions)}")
    st.write(f"**Time Limit**: {quiz.get('time_limit_minutes', 0)} minutes")
    
    # Display questions
    for i, question in enumerate(questions):
        with st.expander(f"Question {i+1}: {question.question_text[:50]}...", expanded=False):
            st.write(f"**{question.question_text}**")
            
            # Show options
            if question.options:
                selected = st.radio(
                    "Select your answer:",
                    question.options,
                    key=f"quiz_{quiz_idx}_q_{i}"
                )
                
                if st.button("Check Answer", key=f"check_{quiz_idx}_{i}"):
                    if selected == question.correct_answer:
                        st.success("✅ Correct!")
                    else:
                        st.error(f"❌ Incorrect. Correct answer: {question.correct_answer}")
                    
                    st.info(f"**Explanation**: {question.explanation}")
                    
                    # Show code evidence
                    if question.code_evidence:
                        with st.expander("📄 View Code", expanded=False):
                            for evidence in question.code_evidence:
                                st.code(evidence.code_snippet or "Code snippet not available", language="python")
                                st.caption(f"From: {evidence.file_path}")


def _render_learning_path(learning_paths):
    """Render learning path section."""
    if not learning_paths:
        st.info("No learning paths generated")
        return
    
    # Select path
    if len(learning_paths) > 1:
        path_idx = st.selectbox("Select Learning Path", range(len(learning_paths)), 
                               format_func=lambda x: learning_paths[x].title)
    else:
        path_idx = 0
    
    path = learning_paths[path_idx]
    
    st.subheader(path.title)
    st.write(path.description)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Steps", path.total_steps)
    with col2:
        st.metric("Estimated Time", f"{path.estimated_total_time_minutes} min")
    with col3:
        st.metric("Difficulty", path.difficulty_level.title())
    
    st.divider()
    
    # Display steps
    for step in path.steps:
        status_icon = "✅" if st.session_state.get(f'step_{step.step_id}_completed', False) else "⭕"
        
        with st.expander(f"{status_icon} Step {step.step_number}: {step.title}", expanded=False):
            st.write(step.description)
            st.write(f"**Estimated Time**: {step.estimated_time_minutes} minutes")
            
            if step.concepts_covered:
                st.write(f"**Concepts**: {', '.join(step.concepts_covered)}")
            
            if step.recommended_files:
                st.write("**Recommended Files**:")
                for file in step.recommended_files:
                    st.write(f"  - `{file}`")
            
            if step.prerequisites:
                st.write(f"**Prerequisites**: Steps {', '.join([p.split('_')[1] for p in step.prerequisites])}")
            
            if st.button(f"Mark as Complete", key=f"complete_{step.step_id}"):
                st.session_state[f'step_{step.step_id}_completed'] = True
                st.success("Step marked as complete!")
                st.rerun()
