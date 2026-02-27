"""Quiz interface component."""
import streamlit as st
from ui.design_system import section_header, spacing, info_box
import random
import time


def render_quiz_view():
    """Render quiz interface."""
    st.markdown("# Interactive Quizzes")
    
    # Check if code analysis exists
    if "current_analysis" not in st.session_state or st.session_state.current_analysis is None:
        section_header("No Code Analyzed Yet", "Upload and analyze code first to generate quizzes")
        
        from ui.design_system import info_box
        info_box("📝 Quizzes are generated from your uploaded code to help you understand YOUR codebase better!", "info")
        
        spacing("md")
        
        if st.button("📤 Go to Upload Code", type="primary", use_container_width=True):
            st.session_state.current_page = "Upload Code"
            st.rerun()
        
        return
    
    # Initialize quiz state
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
    if "quiz_start_time" not in st.session_state:
        st.session_state.quiz_start_time = None
    
    if not st.session_state.quiz_started:
        _render_quiz_selection()
    else:
        _render_quiz_questions()


def _render_quiz_selection():
    """Render quiz topic selection."""
    section_header("Quiz About Your Code", "Test your understanding of the uploaded codebase")
    
    # Get code analysis
    code_analysis = st.session_state.get("current_analysis")
    
    if not code_analysis:
        st.warning("No code analysis found. Please upload and analyze code first.")
        return
    
    spacing("md")
    
    # Display quiz info
    with st.container():
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        
        with col1:
            st.markdown(f"**Your Uploaded Code**")
            st.caption(f"Functions: {len(code_analysis.structure.functions)}, Classes: {len(code_analysis.structure.classes)}")
        with col2:
            st.caption("🟡 Intermediate")
        with col3:
            st.caption("📝 5 Questions")
        with col4:
            if st.button("Start Quiz", key="start_code_quiz", use_container_width=True, type="primary"):
                # Generate quiz from code analysis
                quiz_engine = st.session_state.get("quiz_engine")
                language = st.session_state.session_manager.get_language_preference()
                
                if quiz_engine:
                    quiz = quiz_engine.generate_quiz_from_code(
                        code_analysis=code_analysis,
                        language=language,
                        num_questions=5
                    )
                    
                    st.session_state.quiz_started = True
                    st.session_state.current_topic = "Your Uploaded Code"
                    st.session_state.current_quiz = quiz
                    st.session_state.current_question = 0
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_start_time = time.time()
                    st.session_state.quiz_score = 0
                    st.rerun()
                else:
                    st.error("Quiz engine not available")
        
        st.divider()


def _render_quiz_questions():
    """Render quiz questions and navigation."""
    topic = st.session_state.current_topic
    quiz = st.session_state.current_quiz
    questions = quiz.questions
    current_q = st.session_state.current_question
    total_q = len(questions)
    
    # Check if quiz is complete
    if current_q >= total_q:
        _show_quiz_results()
        return
    
    # Header with progress
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"### 📝 {topic}")
    with col2:
        elapsed = int((time.time() - st.session_state.quiz_start_time) / 60) if st.session_state.quiz_start_time else 0
        st.metric("⏱️ Time", f"{elapsed} min")
    with col3:
        st.metric("Score", f"{st.session_state.quiz_score}/{current_q}")
    
    st.progress((current_q + 1) / total_q, text=f"Question {current_q + 1} of {total_q}")
    
    st.divider()
    
    # Display current question
    question = questions[current_q]
    
    st.markdown(f"### Question {current_q + 1}")
    st.markdown(f"**{question.question_text}**")
    
    spacing("md")
    
    # Render based on question type
    if question.type == "multiple_choice":
        # Shuffle options if not already done
        if f"shuffled_options_{current_q}" not in st.session_state:
            options = question.options.copy()
            random.shuffle(options)
            st.session_state[f"shuffled_options_{current_q}"] = options
        
        options = st.session_state[f"shuffled_options_{current_q}"]
        
        # Show options as radio buttons
        answer = st.radio(
            "Select your answer:",
            options,
            key=f"q_{current_q}",
            label_visibility="collapsed"
        )
        
        st.session_state.quiz_answers[current_q] = answer
    
    st.divider()
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if current_q > 0:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()
    
    with col2:
        # Show explanation if answer is selected
        if current_q in st.session_state.quiz_answers:
            if st.button("💡 Show Explanation", use_container_width=True):
                user_answer = st.session_state.quiz_answers[current_q]
                correct_answer = question.correct_answer
                
                if user_answer == correct_answer:
                    st.success("✅ Correct!")
                    if current_q not in st.session_state.get("scored_questions", set()):
                        st.session_state.quiz_score += 1
                        if "scored_questions" not in st.session_state:
                            st.session_state.scored_questions = set()
                        st.session_state.scored_questions.add(current_q)
                else:
                    st.error(f"❌ Incorrect. The correct answer is: **{correct_answer}**")
                
                st.info(f"**Explanation:** {question.explanation}")
    
    with col3:
        if current_q < total_q - 1:
            if st.button("Next ➡️", use_container_width=True, type="primary"):
                st.session_state.current_question += 1
                st.rerun()
        else:
            if st.button("✅ Finish Quiz", use_container_width=True, type="primary"):
                st.session_state.current_question = total_q
                st.rerun()


def _show_quiz_results():
    """Show quiz results summary."""
    st.balloons()
    
    st.markdown("### 🎉 Quiz Complete!")
    
    # Calculate results
    quiz = st.session_state.current_quiz
    questions = quiz.questions
    total_questions = len(questions)
    
    # Calculate score
    correct_answers = 0
    for i, question in enumerate(questions):
        user_answer = st.session_state.quiz_answers.get(i, "")
        if user_answer == question.correct_answer:
            correct_answers += 1
    
    score_percentage = int((correct_answers / total_questions) * 100) if total_questions > 0 else 0
    
    # Calculate time taken
    time_taken = int((time.time() - st.session_state.quiz_start_time) / 60) if st.session_state.quiz_start_time else 0
    
    spacing("md")
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Score", f"{score_percentage}%", delta=f"{correct_answers}/{total_questions}")
    with col2:
        st.metric("Time Taken", f"{time_taken} min")
    with col3:
        performance = "Excellent!" if score_percentage >= 80 else "Good!" if score_percentage >= 60 else "Keep practicing!"
        st.metric("Performance", performance)
    
    st.divider()
    
    # Performance analysis
    st.markdown("### 📊 Performance Analysis")
    
    if score_percentage >= 80:
        st.success("✅ Excellent work! You have a strong understanding of this topic.")
    elif score_percentage >= 60:
        st.info("👍 Good job! Review the questions you missed to improve further.")
    else:
        st.warning("📚 Keep practicing! Review the explanations and try again.")
    
    spacing("md")
    
    # Show detailed results
    with st.expander("📋 View Detailed Results", expanded=False):
        for i, question in enumerate(questions):
            user_answer = st.session_state.quiz_answers.get(i, "No answer")
            correct_answer = question.correct_answer
            is_correct = user_answer == correct_answer
            
            if is_correct:
                st.success(f"**Q{i+1}:** {question.question_text}")
                st.write(f"Your answer: {user_answer} ✅")
            else:
                st.error(f"**Q{i+1}:** {question.question_text}")
                st.write(f"Your answer: {user_answer} ❌")
                st.write(f"Correct answer: {correct_answer}")
            
            st.caption(f"Explanation: {question.explanation}")
            st.divider()
    
    spacing("lg")
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Take Another Quiz", use_container_width=True, type="primary"):
            st.session_state.quiz_started = False
            st.session_state.current_question = 0
            st.session_state.quiz_answers = {}
            st.session_state.quiz_start_time = None
            st.session_state.quiz_score = 0
            if "scored_questions" in st.session_state:
                del st.session_state.scored_questions
            # Clear shuffled options
            keys_to_delete = [key for key in st.session_state.keys() if key.startswith("shuffled_options_")]
            for key in keys_to_delete:
                del st.session_state[key]
            st.rerun()
    
    with col2:
        if st.button("📚 Practice with Flashcards", use_container_width=True):
            st.session_state.current_page = "Flashcards"
            st.rerun()
