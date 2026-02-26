"""Quiz interface component."""
import streamlit as st
from ui.design_system import section_header, spacing, info_box


def render_quiz_view():
    """Render quiz interface."""
    st.markdown("# Interactive Quizzes")
    
    # Initialize quiz state
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
    
    if not st.session_state.quiz_started:
        _render_quiz_selection()
    else:
        _render_quiz_questions()


def _render_quiz_selection():
    """Render quiz topic selection."""
    section_header("Choose a Quiz Topic")
    
    quiz_topics = {
        "React Basics": {"questions": 10, "difficulty": "Beginner", "time": 15},
        "JavaScript Arrays": {"questions": 8, "difficulty": "Intermediate", "time": 12},
        "Node.js APIs": {"questions": 12, "difficulty": "Advanced", "time": 20},
        "AWS Lambda": {"questions": 10, "difficulty": "Intermediate", "time": 15},
        "Data Structures": {"questions": 15, "difficulty": "Advanced", "time": 25},
    }
    
    for topic, info in quiz_topics.items():
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.markdown(f"**{topic}**")
            with col2:
                st.caption(f"{info['difficulty']}")
            with col3:
                st.caption(f"{info['questions']} Questions")
            with col4:
                if st.button("Start", key=f"start_{topic}", use_container_width=True):
                    # Generate quiz using QuizEngine
                    if "quiz_engine" in st.session_state:
                        with st.spinner("Generating quiz..."):
                            try:
                                language = st.session_state.session_manager.get_language_preference()
                                quiz = st.session_state.quiz_engine.generate_quiz(
                                    topic=topic,
                                    difficulty=info['difficulty'],
                                    num_questions=info['questions'],
                                    language=language
                                )
                                st.session_state.current_quiz = quiz
                                st.session_state.quiz_started = True
                                st.session_state.current_question = 0
                                st.session_state.quiz_answers = {}
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error generating quiz: {str(e)}")
                    else:
                        # Fallback to mock quiz
                        st.session_state.quiz_started = True
                        st.session_state.current_topic = topic
                        st.session_state.total_questions = info['questions']
                        st.session_state.quiz_time_limit = info['time']
                        st.rerun()
            
            st.divider()


def _render_quiz_questions():
    """Render quiz questions and navigation."""
    topic = st.session_state.current_topic
    current_q = st.session_state.current_question
    total_q = st.session_state.total_questions
    
    # Header with progress
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### 📝 {topic}")
    with col2:
        st.metric("⏱️ Time", f"{st.session_state.quiz_time_limit} min")
    
    st.progress((current_q + 1) / total_q, text=f"Question {current_q + 1} of {total_q}")
    
    st.divider()
    
    # Mock questions
    questions = _get_mock_questions(topic)
    
    if current_q < len(questions):
        question = questions[current_q]
        
        st.markdown(f"### Question {current_q + 1}")
        st.markdown(question["text"])
        
        # Render based on question type
        if question["type"] == "multiple_choice":
            answer = st.radio(
                "Select your answer:",
                question["options"],
                key=f"q_{current_q}"
            )
            st.session_state.quiz_answers[current_q] = answer
        
        elif question["type"] == "code_completion":
            st.code(question["code"], language="python")
            answer = st.text_area(
                "Complete the code:",
                key=f"q_{current_q}",
                height=100
            )
            st.session_state.quiz_answers[current_q] = answer
        
        elif question["type"] == "debugging":
            st.code(question["buggy_code"], language="python")
            answer = st.text_area(
                "What's wrong with this code?",
                key=f"q_{current_q}",
                height=100
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
            if current_q < total_q - 1:
                if st.button("Next ➡️", use_container_width=True):
                    st.session_state.current_question += 1
                    st.rerun()
        
        with col3:
            if current_q == total_q - 1:
                if st.button("✅ Submit Quiz", type="primary", use_container_width=True):
                    _show_quiz_results()
    else:
        _show_quiz_results()


def _get_mock_questions(topic: str):
    """Get mock questions for a topic."""
    return [
        {
            "type": "multiple_choice",
            "text": "What is the purpose of useState in React?",
            "options": [
                "To manage component state",
                "To fetch data from APIs",
                "To style components",
                "To handle routing"
            ],
            "correct": "To manage component state"
        },
        {
            "type": "code_completion",
            "text": "Complete the function to reverse an array:",
            "code": "def reverse_array(arr):\n    # Your code here\n    return ___",
            "correct": "arr[::-1]"
        },
        {
            "type": "debugging",
            "text": "Find the bug in this code:",
            "buggy_code": "for i in range(10):\n    if i = 5:\n        print('Found 5')",
            "correct": "Use == instead of = for comparison"
        }
    ]


def _show_quiz_results():
    """Show quiz results summary."""
    st.balloons()
    
    st.markdown("### 🎉 Quiz Complete!")
    
    # Mock results
    score = 75
    time_taken = 12
    correct_answers = 6
    total_questions = st.session_state.total_questions
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Score", f"{score}%", delta="+15%")
    with col2:
        st.metric("Time Taken", f"{time_taken} min")
    with col3:
        st.metric("Correct", f"{correct_answers}/{total_questions}")
    
    st.divider()
    
    st.markdown("### 📊 Performance Analysis")
    st.success("✅ Great job! You're improving steadily.")
    st.info("💡 Tip: Review topics on array methods and async/await patterns.")
    
    if st.button("🔄 Take Another Quiz", use_container_width=True):
        st.session_state.quiz_started = False
        st.session_state.current_question = 0
        st.session_state.quiz_answers = {}
        st.rerun()
