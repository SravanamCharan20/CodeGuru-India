"""Flashcard interface component."""
import streamlit as st
from ui.design_system import section_header, spacing, info_box
import random


def render_flashcard_view():
    """Render flashcard interface."""
    st.markdown("# Interactive Flashcards")
    
    # Check if flashcards exist from code analysis
    progress = st.session_state.session_manager.load_progress()
    
    # Handle both data structures (with and without wrapper)
    if isinstance(progress, dict) and "data" in progress:
        flashcard_data = progress["data"].get("flashcards", {})
    else:
        flashcard_data = progress.get("flashcards", {}) if isinstance(progress, dict) else {}
    
    cards_data = flashcard_data.get("cards", [])
    
    # Debug info (can be removed later)
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Flashcard view - Found {len(cards_data)} flashcards in session")
    
    if not cards_data:
        section_header("No Flashcards Generated Yet", "Upload and analyze code first to generate flashcards")
        
        info_box("🎴 Flashcards are generated from your uploaded code to help you learn YOUR codebase better!", "info")
        
        spacing("md")
        
        # Show debug info if code analysis exists
        if "current_analysis" in st.session_state and st.session_state.current_analysis:
            st.warning("⚠️ Code analysis found but no flashcards. This might be a bug.")
            st.info("💡 Try clicking 'Analyze Code' again with 'Generate Flashcards' checkbox enabled.")
        
        if st.button("📤 Go to Upload Code", type="primary", use_container_width=True):
            st.session_state.current_page = "Upload Code"
            st.rerun()
        
        return
    
    # Initialize flashcard state
    if "current_card" not in st.session_state:
        st.session_state.current_card = 0
    if "card_flipped" not in st.session_state:
        st.session_state.card_flipped = False
    if "flashcard_topic" not in st.session_state:
        st.session_state.flashcard_topic = "All Topics"
    if "reviewed_cards" not in st.session_state:
        st.session_state.reviewed_cards = set()
    if "mastered_cards" not in st.session_state:
        st.session_state.mastered_cards = set()
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        # Get unique topics from flashcards
        topics = ["All Topics"] + list(set([card.get("topic", "General") for card in cards_data]))
        topic_filter = st.selectbox(
            "Topic",
            topics,
            index=topics.index(st.session_state.flashcard_topic) if st.session_state.flashcard_topic in topics else 0,
            key="topic_selector"
        )
        
        if topic_filter != st.session_state.flashcard_topic:
            st.session_state.flashcard_topic = topic_filter
            st.session_state.current_card = 0
            st.session_state.card_flipped = False
    
    with col2:
        difficulty_filter = st.selectbox(
            "Difficulty",
            ["All Levels", "beginner", "intermediate", "advanced"]
        )
    
    st.divider()
    
    # Get flashcards based on filters
    flashcards = cards_data
    
    # Filter by topic
    if topic_filter != "All Topics":
        flashcards = [card for card in flashcards if card.get("topic") == topic_filter]
    
    # Filter by difficulty
    if difficulty_filter != "All Levels":
        flashcards = [card for card in flashcards if card.get("difficulty") == difficulty_filter]
    
    # Shuffle flashcards if not already done for this session
    if "shuffled_flashcards" not in st.session_state or st.session_state.get("last_topic") != topic_filter:
        random.shuffle(flashcards)
        st.session_state.shuffled_flashcards = flashcards
        st.session_state.last_topic = topic_filter
    else:
        flashcards = st.session_state.shuffled_flashcards
    
    if flashcards:
        current_idx = st.session_state.current_card
        
        # Ensure current_card is within bounds
        if current_idx >= len(flashcards):
            st.session_state.current_card = 0
            current_idx = 0
        
        total_cards = len(flashcards)
        
        # Card counter and stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Card", f"{current_idx + 1} of {total_cards}")
        with col2:
            st.metric("Reviewed", len(st.session_state.reviewed_cards))
        with col3:
            st.metric("Mastered", len(st.session_state.mastered_cards))
        
        st.progress((current_idx + 1) / total_cards)
        
        st.divider()
        
        # Display flashcard
        card = flashcards[current_idx]
        card_id = f"{topic_filter}_{current_idx}"
        _render_flashcard(card, card_id)
        
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
            st.markdown("**How difficult was this card?**")
            rating = st.select_slider(
                "Difficulty",
                options=["Easy 😊", "Medium 😐", "Hard 😓"],
                label_visibility="collapsed",
                key=f"rating_{card_id}"
            )
        
        with col3:
            if current_idx < total_cards - 1:
                if st.button("Next ➡️", use_container_width=True, type="primary"):
                    st.session_state.current_card += 1
                    st.session_state.card_flipped = False
                    st.rerun()
            else:
                if st.button("🔄 Restart", use_container_width=True, type="primary"):
                    st.session_state.current_card = 0
                    st.session_state.card_flipped = False
                    st.rerun()
        
        st.divider()
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Mark Reviewed", use_container_width=True):
                st.session_state.reviewed_cards.add(card_id)
                st.success("Card marked as reviewed!")
                progress_tracker = st.session_state.get("progress_tracker")
                if progress_tracker:
                    progress_tracker.record_activity(
                        "flashcard_reviewed",
                        {
                            "topic": card.get("topic", "flashcards"),
                            "skill": card.get("topic", "flashcards").lower().replace(" ", "_"),
                            "minutes_spent": 2,
                        },
                    )
                
                # Auto-advance to next card
                if current_idx < total_cards - 1:
                    st.session_state.current_card += 1
                    st.session_state.card_flipped = False
                    st.rerun()
        
        with col2:
            if st.button("🏆 Mark as Mastered", use_container_width=True):
                st.session_state.mastered_cards.add(card_id)
                st.session_state.reviewed_cards.add(card_id)
                st.success("Card mastered! Great job!")
                progress_tracker = st.session_state.get("progress_tracker")
                if progress_tracker:
                    progress_tracker.record_activity(
                        "flashcard_mastered",
                        {
                            "topic": card.get("topic", "flashcards"),
                            "skill": card.get("topic", "flashcards").lower().replace(" ", "_"),
                            "minutes_spent": 3,
                        },
                    )
                
                # Auto-advance to next card
                if current_idx < total_cards - 1:
                    st.session_state.current_card += 1
                    st.session_state.card_flipped = False
                    st.rerun()
        
        spacing("md")
        
        # Progress summary
        if len(st.session_state.reviewed_cards) > 0:
            review_percentage = int((len(st.session_state.reviewed_cards) / total_cards) * 100)
            mastery_percentage = int((len(st.session_state.mastered_cards) / total_cards) * 100)
            
            with st.expander("📊 Your Progress", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Review Progress", f"{review_percentage}%")
                    st.progress(review_percentage / 100)
                with col2:
                    st.metric("Mastery Progress", f"{mastery_percentage}%")
                    st.progress(mastery_percentage / 100)
    
    else:
        st.info("No flashcards available for the selected filters. Try a different topic or difficulty level!")
        
        # Show button to navigate to quizzes
        if st.button("📝 Take a Quiz Instead", type="primary"):
            st.session_state.current_page = "Quizzes"
            st.rerun()


def _render_flashcard(card, card_id):
    """Render a single flashcard with flip functionality."""
    is_flipped = st.session_state.card_flipped
    
    # Get card data
    front = card.get('front', '')
    back = card.get('back', '')
    difficulty = card.get('difficulty', 'Intermediate')
    
    # Check if card is reviewed or mastered
    is_reviewed = card_id in st.session_state.reviewed_cards
    is_mastered = card_id in st.session_state.mastered_cards
    
    # Status badges
    status_html = ""
    if is_mastered:
        status_html = '<span style="background: #10b981; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600;">🏆 MASTERED</span>'
    elif is_reviewed:
        status_html = '<span style="background: #3b82f6; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600;">✅ REVIEWED</span>'
    
    # Card container with styling
    if not is_flipped:
        # Front of card
        gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        st.markdown(
            f"""
            <div style="
                background: {gradient};
                padding: 60px 40px;
                border-radius: 15px;
                text-align: center;
                min-height: 300px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                position: relative;
            ">
                <div style="position: absolute; top: 20px; right: 20px;">
                    {status_html}
                </div>
                <h2 style="color: white; font-size: 28px; margin: 0; line-height: 1.4;">
                    {front}
                </h2>
                <p style="color: rgba(255,255,255,0.8); margin-top: 20px; font-size: 14px;">
                    Click below to see the answer
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        spacing("sm")
        
        if st.button("🔄 Flip to See Answer", use_container_width=True, type="primary"):
            st.session_state.card_flipped = True
            st.rerun()
    
    else:
        # Back of card
        gradient = "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
        st.markdown(
            f"""
            <div style="
                background: {gradient};
                padding: 40px;
                border-radius: 15px;
                min-height: 300px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                position: relative;
            ">
                <div style="position: absolute; top: 20px; right: 20px;">
                    {status_html}
                </div>
                <div style="color: white;">
                    <h3 style="margin-top: 0; font-size: 20px;">Answer:</h3>
                    <p style="font-size: 16px; line-height: 1.8; margin-top: 20px;">
                        {back}
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        spacing("sm")
        
        if st.button("🔄 Flip to Question", use_container_width=True, type="primary"):
            st.session_state.card_flipped = False
            st.rerun()
    
    # Card metadata
    difficulty_color = {
        "Beginner": "🟢",
        "Intermediate": "🟡",
        "Advanced": "🔴"
    }.get(difficulty, "⚪")
    
    st.caption(f"{difficulty_color} Difficulty: {difficulty}")
