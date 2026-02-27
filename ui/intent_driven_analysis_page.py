"""
Intent-Driven Repository Analysis Page.

Main page that orchestrates the complete workflow.
"""

import streamlit as st
import logging
from ui.repository_upload import render_repository_upload
from ui.intent_input import render_intent_input
from ui.learning_artifacts_dashboard import render_learning_artifacts_dashboard

logger = logging.getLogger(__name__)


def render_intent_driven_analysis_page(orchestrator, repository_manager, intent_interpreter, session_manager):
    """
    Render the complete intent-driven analysis workflow.
    
    Args:
        orchestrator: IntentDrivenOrchestrator instance
        repository_manager: RepositoryManager instance
        intent_interpreter: IntentInterpreter instance
        session_manager: SessionManager instance
    """
    st.title("🧠 Intent-Driven Repository Analysis")
    st.write("Analyze code repositories based on your learning goals")
    
    # Initialize workflow state
    if 'workflow_step' not in st.session_state:
        st.session_state.workflow_step = 'upload'
    
    # Progress indicator
    steps = ['Upload', 'Intent', 'Analyze', 'Learn']
    current_step_idx = steps.index(st.session_state.workflow_step.title()) if st.session_state.workflow_step.title() in steps else 0
    
    cols = st.columns(len(steps))
    for i, step in enumerate(steps):
        with cols[i]:
            if i < current_step_idx:
                st.success(f"✅ {step}")
            elif i == current_step_idx:
                st.info(f"▶️ {step}")
            else:
                st.write(f"⭕ {step}")
    
    st.divider()
    
    # Workflow steps
    if st.session_state.workflow_step == 'upload':
        _render_upload_step(repository_manager, session_manager)
    
    elif st.session_state.workflow_step == 'intent':
        _render_intent_step(intent_interpreter, session_manager)
    
    elif st.session_state.workflow_step == 'analyze':
        _render_analyze_step(orchestrator, session_manager)
    
    elif st.session_state.workflow_step == 'learn':
        _render_learn_step(session_manager)


def _render_upload_step(repository_manager, session_manager):
    """Render repository upload step."""
    render_repository_upload(repository_manager, session_manager)
    
    # Check if repository is loaded
    if session_manager.get_current_repository():
        st.divider()
        if st.button("Continue to Intent →", type="primary"):
            st.session_state.workflow_step = 'intent'
            st.rerun()


def _render_intent_step(intent_interpreter, session_manager):
    """Render intent input step."""
    # Back button
    if st.button("← Back to Upload"):
        st.session_state.workflow_step = 'upload'
        st.rerun()
    
    st.divider()
    
    def on_intent_confirmed():
        st.session_state.workflow_step = 'analyze'
    
    render_intent_input(intent_interpreter, session_manager, on_intent_confirmed)


def _render_analyze_step(orchestrator, session_manager):
    """Render analysis step."""
    # Back button
    if st.button("← Back to Intent"):
        st.session_state.workflow_step = 'intent'
        st.rerun()
    
    st.divider()
    
    st.header("🔍 Analyze Repository")
    
    # Get current state
    repo_data = session_manager.get_current_repository()
    intent_data = session_manager.get_current_intent()
    
    if not repo_data or not intent_data:
        st.error("Missing repository or intent data. Please go back and complete previous steps.")
        return
    
    intent = intent_data['intent']
    
    # Show what will be analyzed
    st.write("**Your Learning Goal:**", intent.primary_intent.replace('_', ' ').title())
    st.write("**Audience Level:**", intent.audience_level.title())
    if intent.technologies:
        st.write("**Technologies:**", ", ".join(intent.technologies))
    
    st.divider()
    
    # Check if analysis is already complete
    artifacts = session_manager.get_learning_artifacts()
    analysis_complete = (
        artifacts and 
        (len(artifacts.get('flashcards', [])) > 0 or 
         len(artifacts.get('quizzes', [])) > 0 or 
         len(artifacts.get('learning_paths', [])) > 0)
    )
    
    if analysis_complete:
        # Show results
        st.success("✅ Analysis complete!")
        
        flashcards = artifacts.get('flashcards', [])
        quizzes = artifacts.get('quizzes', [])
        learning_paths = artifacts.get('learning_paths', [])
        
        st.write("**Generated:**")
        st.write(f"- {len(flashcards)} flashcards")
        st.write(f"- {len(quizzes[0].get('questions', [])) if quizzes else 0} quiz questions")
        st.write(f"- {learning_paths[0].total_steps if learning_paths and hasattr(learning_paths[0], 'total_steps') else 0} learning steps")
        
        st.divider()
        
        # This button is OUTSIDE the analysis block, so it persists
        if st.button("View Learning Materials →", type="primary", key="view_materials_btn"):
            st.session_state.workflow_step = 'learn'
            st.rerun()
        
        # Option to re-run analysis
        if st.button("🔄 Re-run Analysis"):
            session_manager.clear_current_analysis()
            st.rerun()
    
    else:
        # Language selection (use from session if available)
        default_language = st.session_state.get('selected_language', 'english')
        language = st.selectbox(
            "🌐 Output Language",
            ["english", "hindi", "telugu"],
            format_func=lambda x: {"english": "English", "hindi": "हिंदी", "telugu": "తెలుగు"}[x],
            index=["english", "hindi", "telugu"].index(default_language),
            help="Language for learning materials (flashcards, quizzes, learning paths)"
        )
        
        # Start analysis button
        if st.button("🚀 Start Analysis", type="primary"):
            with st.spinner("Analyzing repository... This may take a minute."):
                try:
                    # Run complete analysis
                    result = orchestrator.analyze_repository_with_intent(
                        repo_path=repo_data['repo_path'],
                        user_input=intent.primary_intent,
                        language=language
                    )
                    
                    if result.get('status') == 'success':
                        st.success("✅ Analysis complete!")
                        st.balloons()
                        
                        # Show summary
                        flashcards = result.get('flashcards', [])
                        quiz = result.get('quiz', {})
                        learning_path = result.get('learning_path')
                        
                        logger.info(f"Analysis result - Flashcards: {len(flashcards)}, Quiz questions: {len(quiz.get('questions', []))}, Learning path steps: {learning_path.total_steps if learning_path and hasattr(learning_path, 'total_steps') else 0}")
                        
                        st.write("**Generated:**")
                        st.write(f"- {len(flashcards)} flashcards")
                        st.write(f"- {len(quiz.get('questions', []))} quiz questions")
                        st.write(f"- {learning_path.total_steps if learning_path and hasattr(learning_path, 'total_steps') else 0} learning steps")
                        
                        st.info("✨ Analysis saved! Click the button above to view your learning materials.")
                        
                        # Force rerun to show the "View Learning Materials" button
                        st.rerun()
                    
                    elif result.get('status') == 'clarification_needed':
                        st.warning("Your intent needs clarification. Please go back and provide more details.")
                    
                    elif result.get('status') == 'no_files_found':
                        st.error("No relevant files found for your learning goal.")
                        suggestions = result.get('suggestions', [])
                        if suggestions:
                            st.write("**Try these instead:**")
                            for suggestion in suggestions:
                                st.write(f"- {suggestion}")
                    
                    else:
                        st.error(f"Analysis failed: {result.get('error', 'Unknown error')}")
                
                except Exception as e:
                    logger.error(f"Analysis failed: {e}")
                    st.error(f"Analysis failed: {str(e)}")


def _render_learn_step(session_manager):
    """Render learning materials step."""
    # Back button
    if st.button("← Back to Analysis"):
        st.session_state.workflow_step = 'analyze'
        st.rerun()
    
    st.divider()
    
    # Render learning artifacts dashboard
    render_learning_artifacts_dashboard(session_manager)
    
    st.divider()
    
    # Option to start new analysis
    if st.button("🔄 Start New Analysis"):
        session_manager.clear_current_analysis()
        st.session_state.workflow_step = 'upload'
        st.rerun()
