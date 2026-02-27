"""
Intent Input UI Component.

Provides interface for entering learning goals and handling intent clarification.
"""

import streamlit as st
import logging

logger = logging.getLogger(__name__)


def render_intent_input(intent_interpreter, session_manager, on_intent_confirmed=None):
    """
    Render intent input interface.
    
    Args:
        intent_interpreter: IntentInterpreter instance
        session_manager: SessionManager instance
        on_intent_confirmed: Callback function when intent is confirmed
    """
    st.header("🎯 What do you want to learn?")
    
    # Check if repository is loaded
    current_repo = session_manager.get_current_repository()
    if not current_repo:
        st.warning("⚠️ Please upload a repository first")
        return
    
    repo_analysis = current_repo.get('repo_analysis')
    
    # Language selection
    col1, col2 = st.columns([3, 1])
    with col2:
        language = st.selectbox(
            "🌐 Language",
            options=["english", "hindi", "telugu"],
            format_func=lambda x: {"english": "English", "hindi": "हिंदी", "telugu": "తెలుగు"}[x],
            key="learning_language",
            help="Select the language for learning materials"
        )
        # Store language in session
        if 'selected_language' not in st.session_state or st.session_state.get('selected_language') != language:
            st.session_state['selected_language'] = language
    
    # Show suggested intents
    if repo_analysis:
        with st.expander("💡 Suggested Learning Goals", expanded=False):
            suggestions = intent_interpreter.suggest_intents(repo_analysis)
            for i, suggestion in enumerate(suggestions):
                if st.button(suggestion, key=f"suggestion_{i}"):
                    st.session_state['user_input'] = suggestion
                    st.rerun()
    
    # Main input area
    user_input = st.text_area(
        "Describe your learning goal",
        value=st.session_state.get('user_input', ''),
        placeholder="Example: I want to learn how authentication works in this project",
        help="Describe what you want to learn from this repository in natural language",
        height=100
    )
    
    # Analyze button
    col1, col2 = st.columns([1, 4])
    with col1:
        analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)
    with col2:
        if st.button("🔄 Clear", use_container_width=True):
            st.session_state['user_input'] = ''
            session_manager.set_current_intent(None)
            st.rerun()
    
    if analyze_button and user_input:
        with st.spinner("Interpreting your learning goal..."):
            # Interpret intent
            intent = intent_interpreter.interpret_intent(user_input, repo_analysis)
            session_manager.set_current_intent(intent)
            
            # Check if clarification needed
            if intent.confidence_score < 0.7:
                st.session_state['needs_clarification'] = True
                st.session_state['clarification_questions'] = intent_interpreter.generate_clarification_questions(intent)
                st.rerun()
            else:
                st.session_state['needs_clarification'] = False
                st.session_state['intent_confirmed'] = True
                st.rerun()
    
    # Show interpreted intent
    current_intent_data = session_manager.get_current_intent()
    if current_intent_data and current_intent_data.get('intent'):
        intent = current_intent_data['intent']
        
        st.divider()
        st.subheader("📋 Interpreted Intent")
        
        # Display intent details
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Primary Goal", intent.primary_intent.replace('_', ' ').title())
            st.metric("Audience Level", intent.audience_level.title())
        with col2:
            confidence_color = "🟢" if intent.confidence_score >= 0.7 else "🟡" if intent.confidence_score >= 0.5 else "🔴"
            st.metric("Confidence", f"{confidence_color} {intent.confidence_score:.0%}")
            if intent.technologies:
                st.write("**Technologies**:", ", ".join(intent.technologies))
        
        # Show scope
        if intent.scope:
            with st.expander("🎯 Analysis Scope", expanded=False):
                st.write(f"**Type**: {intent.scope.scope_type.replace('_', ' ').title()}")
                if intent.scope.target_paths:
                    st.write("**Target Paths**:", ", ".join(intent.scope.target_paths))
        
        # Handle clarification if needed
        if st.session_state.get('needs_clarification', False):
            _render_clarification_dialog(
                intent_interpreter,
                intent,
                st.session_state.get('clarification_questions', []),
                session_manager
            )
        else:
            # Confirmation
            st.success("✅ Intent understood!")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("✓ Confirm and Continue", type="primary", use_container_width=True):
                    st.session_state['intent_confirmed'] = True
                    if on_intent_confirmed:
                        on_intent_confirmed()
                    st.rerun()
            with col2:
                if st.button("✏️ Refine Intent", use_container_width=True):
                    st.session_state['user_input'] = user_input
                    session_manager.set_current_intent(None)
                    st.rerun()


def _render_clarification_dialog(intent_interpreter, intent, questions, session_manager):
    """Render clarification questions dialog."""
    st.warning("🤔 Your intent needs clarification")
    
    st.write("Please answer these questions to help us understand better:")
    
    responses = {}
    for i, question in enumerate(questions):
        response = st.text_input(
            question,
            key=f"clarification_{i}",
            placeholder="Your answer..."
        )
        if response:
            responses[question] = response
    
    if st.button("Submit Clarifications", type="primary"):
        if responses:
            with st.spinner("Refining intent..."):
                # Refine intent
                refined_intent = intent_interpreter.refine_intent(intent, responses)
                session_manager.set_current_intent(refined_intent)
                
                st.session_state['needs_clarification'] = False
                st.session_state['intent_confirmed'] = True
                st.rerun()
        else:
            st.error("Please provide at least one answer")
