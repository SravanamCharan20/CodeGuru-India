"""Learning path view component."""
import streamlit as st


def render_learning_path():
    """Render learning path interface."""
    st.title("🛤️ Learning Paths")
    
    # Get path manager and progress tracker
    path_manager = st.session_state.get("path_manager")
    progress_tracker = st.session_state.get("progress_tracker")
    
    if not path_manager:
        st.warning("⚠️ Learning path manager not initialized. Please restart the app.")
        return
    
    # Path selection
    st.markdown("### Choose Your Learning Journey")
    
    # Get available paths from manager
    available_paths = path_manager.get_available_paths()
    
    # Create path options
    path_options = {path.name: path for path in available_paths}
    
    selected_path_name = st.selectbox(
        "Select a Learning Path",
        options=list(path_options.keys()),
        format_func=lambda x: f"{path_options[x].icon} {x}"
    )
    
    selected_path = path_options[selected_path_name]
    
    # Calculate progress
    completed_topics = sum(1 for topic in selected_path.topics if topic.completed)
    total_topics = len(selected_path.topics)
    progress = completed_topics / total_topics if total_topics > 0 else 0
    
    # Display path details
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📚 Topics", total_topics)
    with col2:
        st.metric("⏱️ Est. Hours", selected_path.estimated_hours)
    with col3:
        st.metric("✅ Progress", f"{int(progress * 100)}%")
    
    st.progress(progress, text=f"{int(progress * 100)}% Complete")
    
    st.divider()
    
    # Render roadmap
    _render_roadmap(selected_path, path_manager, progress_tracker)
    
    st.divider()
    
    # Milestone achievements
    _render_milestones(progress)


def _render_roadmap(learning_path, path_manager, progress_tracker):
    """Render learning roadmap visualization."""
    st.markdown("### 🗺️ Learning Roadmap")
    
    # Display topics from the learning path
    for topic in learning_path.topics:
        # Determine status
        if topic.completed:
            status = "completed"
            status_icon = "✅"
        elif topic.unlocked:
            status = "available"
            status_icon = "📖"
        else:
            status = "locked"
            status_icon = "🔒"
        
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown(f"**{status_icon} {topic.name}**")
            st.caption(topic.description)
            if topic.prerequisites:
                st.caption(f"Prerequisites: {', '.join(topic.prerequisites)}")
        
        with col2:
            if status == "available":
                if st.button("Start", key=f"start_{topic.id}", use_container_width=True):
                    # Mark topic as started
                    if progress_tracker:
                        progress_tracker.record_activity("topic_started", {
                            "path": learning_path.name,
                            "topic": topic.name
                        })
                    
                    st.success(f"Starting {topic.name}...")
                    st.info("💡 Complete quizzes and flashcards to mark this topic as complete!")
            
            elif status == "completed":
                if st.button("Review", key=f"review_{topic.id}", use_container_width=True):
                    st.info(f"Reviewing {topic.name}...")
            
            else:
                st.button("Locked", key=f"locked_{topic.id}", disabled=True, use_container_width=True)
        
        st.divider()


def _render_milestones(progress):
    """Render milestone achievements."""
    st.markdown("### 🏆 Milestone Achievements")
    
    # Calculate milestones based on progress
    milestones = [
        {"name": "First Steps", "description": "Complete your first topic", "threshold": 0.05},
        {"name": "Quick Learner", "description": "Complete 25% of topics", "threshold": 0.25},
        {"name": "Dedicated Student", "description": "Complete 50% of topics", "threshold": 0.50},
        {"name": "Path Master", "description": "Complete entire learning path", "threshold": 1.0},
    ]
    
    cols = st.columns(4)
    for i, milestone in enumerate(milestones):
        with cols[i]:
            achieved = progress >= milestone["threshold"]
            if achieved:
                st.success(f"🏅 {milestone['name']}")
            else:
                st.info(f"⭕ {milestone['name']}")
            st.caption(milestone["description"])
