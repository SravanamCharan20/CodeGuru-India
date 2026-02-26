"""Learning path view component."""
import streamlit as st
from ui.design_system import section_header, spacing, info_box


def render_learning_path():
    """Render learning path interface."""
    st.markdown("# Learning Paths")
    
    # Get path manager and progress tracker
    path_manager = st.session_state.get("path_manager")
    progress_tracker = st.session_state.get("progress_tracker")
    
    if not path_manager:
        info_box("Learning path manager not initialized. Please restart the app.", "warning")
        return
    
    # Path selection
    section_header("Choose Your Learning Journey")
    
    # Get available paths from manager
    available_paths = path_manager.get_available_paths()
    
    path_options = {path.name: path for path in available_paths}
    
    selected_path_name = st.selectbox(
        "Select a Learning Path",
        options=list(path_options.keys())
    )
    
    selected_path = path_options[selected_path_name]
    
    # Get or initialize progress for this path
    if "learning_progress" not in st.session_state:
        st.session_state.learning_progress = {}
    
    path_progress = st.session_state.learning_progress.get(selected_path.id, {})
    
    # Calculate progress
    completed_topics = sum(1 for topic_id in path_progress.values() if topic_id)
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
    
    # Get progress for this path
    if "learning_progress" not in st.session_state:
        st.session_state.learning_progress = {}
    
    path_progress = st.session_state.learning_progress.get(learning_path.id, {})
    
    # Display topics from the learning path
    for topic in learning_path.topics:
        # Determine status based on progress
        is_completed = path_progress.get(topic.id, False)
        
        # Check if prerequisites are met
        prereqs_met = True
        if topic.prerequisites:
            for prereq_id in topic.prerequisites:
                if not path_progress.get(prereq_id, False):
                    prereqs_met = False
                    break
        
        # Determine status
        if is_completed:
            status = "completed"
            status_icon = "✅"
        elif prereqs_met:
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
                # Get prerequisite names
                prereq_names = []
                for prereq_id in topic.prerequisites:
                    for t in learning_path.topics:
                        if t.id == prereq_id:
                            prereq_names.append(t.name)
                            break
                if prereq_names:
                    st.caption(f"Prerequisites: {', '.join(prereq_names)}")
        
        with col2:
            if status == "available":
                if st.button("Start", key=f"start_{topic.id}", use_container_width=True):
                    # Mark topic as completed (simplified - in real app would track actual completion)
                    if learning_path.id not in st.session_state.learning_progress:
                        st.session_state.learning_progress[learning_path.id] = {}
                    st.session_state.learning_progress[learning_path.id][topic.id] = True
                    
                    # Record activity
                    if progress_tracker:
                        progress_tracker.record_activity("topic_started", {
                            "path": learning_path.name,
                            "topic": topic.name
                        })
                    
                    st.success(f"Starting {topic.name}...")
                    st.info("💡 Complete quizzes and flashcards to mark this topic as complete!")
                    st.rerun()
            
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
