"""Flashcard interface component."""
import streamlit as st


def render_flashcard_view():
    """Render flashcard interface."""
    st.title("🗂️ Interactive Flashcards")
    
    # Initialize flashcard state
    if "current_card" not in st.session_state:
        st.session_state.current_card = 0
    if "card_flipped" not in st.session_state:
        st.session_state.card_flipped = False
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        topic_filter = st.selectbox(
            "📚 Topic",
            ["All Topics", "React", "JavaScript", "Node.js", "AWS", "Data Structures"]
        )
    with col2:
        difficulty_filter = st.selectbox(
            "📊 Difficulty",
            ["All Levels", "Beginner", "Intermediate", "Advanced"]
        )
    
    st.divider()
    
    # Get mock flashcards
    flashcards = _get_mock_flashcards()
    
    if flashcards:
        current_idx = st.session_state.current_card
        total_cards = len(flashcards)
        
        # Card counter
        st.markdown(f"### Card {current_idx + 1} of {total_cards}")
        st.progress((current_idx + 1) / total_cards)
        
        st.divider()
        
        # Display flashcard
        card = flashcards[current_idx]
        _render_flashcard(card)
        
        st.divider()
        
        # Navigation and rating
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if current_idx > 0:
                if st.button("⬅️ Previous", use_container_width=True):
                    st.session_state.current_card -= 1
                    st.session_state.card_flipped = False
                    st.rerun()
        
        with col2:
            # Difficulty rating
            st.markdown("**Rate this card:**")
            rating = st.select_slider(
                "Difficulty",
                options=["Easy 😊", "Medium 😐", "Hard 😓"],
                label_visibility="collapsed"
            )
        
        with col3:
            if current_idx < total_cards - 1:
                if st.button("Next ➡️", use_container_width=True):
                    st.session_state.current_card += 1
                    st.session_state.card_flipped = False
                    st.rerun()
        
        st.divider()
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Mark Reviewed", use_container_width=True):
                st.success("Card marked as reviewed!")
        with col2:
            if st.button("🏆 Mark as Mastered", use_container_width=True):
                st.success("Card mastered! It will appear less frequently.")
    else:
        st.info("No flashcards available. Generate flashcards from code analysis!")


def _render_flashcard(card):
    """Render a single flashcard with flip functionality."""
    is_flipped = st.session_state.card_flipped
    
    # Card container with styling
    card_container = st.container()
    
    with card_container:
        if not is_flipped:
            # Front of card
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 60px 40px;
                    border-radius: 15px;
                    text-align: center;
                    min-height: 300px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                ">
                    <h2 style="color: white; font-size: 28px; margin: 0;">
                        {card['front']}
                    </h2>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            if st.button("🔄 Flip to Back", use_container_width=True, type="primary"):
                st.session_state.card_flipped = True
                st.rerun()
        
        else:
            # Back of card
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    padding: 40px;
                    border-radius: 15px;
                    min-height: 300px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                ">
                    <div style="color: white;">
                        <h3 style="margin-top: 0;">Answer:</h3>
                        <p style="font-size: 18px; line-height: 1.6;">
                            {card['back']}
                        </p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            if st.button("🔄 Flip to Front", use_container_width=True, type="primary"):
                st.session_state.card_flipped = False
                st.rerun()
        
        # Card metadata
        st.caption(f"📚 Topic: {card['topic']} | 📊 Difficulty: {card['difficulty']}")


def _get_mock_flashcards():
    """Get mock flashcards."""
    return [
        {
            "front": "What is a closure in JavaScript?",
            "back": "A closure is a function that has access to variables in its outer (enclosing) function's scope, even after the outer function has returned. It 'closes over' these variables.",
            "topic": "JavaScript",
            "difficulty": "Intermediate"
        },
        {
            "front": "What does useState return in React?",
            "back": "useState returns an array with two elements: [1] the current state value, and [2] a function to update that state. Example: const [count, setCount] = useState(0);",
            "topic": "React",
            "difficulty": "Beginner"
        },
        {
            "front": "What is the time complexity of binary search?",
            "back": "O(log n) - Binary search divides the search space in half with each iteration, making it very efficient for sorted arrays.",
            "topic": "Data Structures",
            "difficulty": "Intermediate"
        },
        {
            "front": "What is AWS Lambda?",
            "back": "AWS Lambda is a serverless compute service that runs code in response to events without requiring server management. You only pay for the compute time you consume.",
            "topic": "AWS",
            "difficulty": "Beginner"
        },
        {
            "front": "What is the difference between let and var?",
            "back": "let has block scope and cannot be redeclared in the same scope, while var has function scope and can be redeclared. let is the modern, preferred way to declare variables.",
            "topic": "JavaScript",
            "difficulty": "Beginner"
        }
    ]
