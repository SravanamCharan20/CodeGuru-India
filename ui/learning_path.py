"""Learning path view component."""
import streamlit as st


def render_learning_path():
    """Render learning path interface."""
    st.title("🛤️ Learning Paths")
    
    # Path selection
    st.markdown("### Choose Your Learning Journey")
    
    paths = {
        "DSA Fundamentals": {
            "icon": "🧮",
            "description": "Master Data Structures and Algorithms",
            "topics": 12,
            "hours": 40,
            "progress": 0.35
        },
        "Backend Development": {
            "icon": "⚙️",
            "description": "Build robust server-side applications",
            "topics": 15,
            "hours": 50,
            "progress": 0.20
        },
        "Frontend Development": {
            "icon": "🎨",
            "description": "Create beautiful user interfaces",
            "topics": 18,
            "hours": 45,
            "progress": 0.50
        },
        "Full-Stack Development": {
            "icon": "🚀",
            "description": "Complete web development mastery",
            "topics": 25,
            "hours": 80,
            "progress": 0.15
        },
        "AWS Services": {
            "icon": "☁️",
            "description": "Cloud computing with Amazon Web Services",
            "topics": 20,
            "hours": 60,
            "progress": 0.10
        }
    }
    
    selected_path = st.selectbox(
        "Select a Learning Path",
        options=list(paths.keys()),
        format_func=lambda x: f"{paths[x]['icon']} {x}"
    )
    
    # Display path details
    path_info = paths[selected_path]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📚 Topics", path_info["topics"])
    with col2:
        st.metric("⏱️ Est. Hours", path_info["hours"])
    with col3:
        st.metric("✅ Progress", f"{int(path_info['progress'] * 100)}%")
    
    st.progress(path_info["progress"], text=f"{int(path_info['progress'] * 100)}% Complete")
    
    st.divider()
    
    # Render roadmap
    _render_roadmap(selected_path)
    
    st.divider()
    
    # Milestone achievements
    _render_milestones()


def _render_roadmap(path_name: str):
    """Render learning roadmap visualization."""
    st.markdown("### 🗺️ Learning Roadmap")
    
    # Mock topics based on path
    if path_name == "DSA Fundamentals":
        topics = [
            {"name": "Arrays & Strings", "status": "completed", "prereq": []},
            {"name": "Linked Lists", "status": "completed", "prereq": ["Arrays & Strings"]},
            {"name": "Stacks & Queues", "status": "available", "prereq": ["Linked Lists"]},
            {"name": "Trees & Graphs", "status": "locked", "prereq": ["Stacks & Queues"]},
            {"name": "Dynamic Programming", "status": "locked", "prereq": ["Trees & Graphs"]},
        ]
    elif path_name == "Frontend Development":
        topics = [
            {"name": "HTML & CSS Basics", "status": "completed", "prereq": []},
            {"name": "JavaScript Fundamentals", "status": "completed", "prereq": ["HTML & CSS Basics"]},
            {"name": "React Basics", "status": "completed", "prereq": ["JavaScript Fundamentals"]},
            {"name": "State Management", "status": "available", "prereq": ["React Basics"]},
            {"name": "React Hooks", "status": "available", "prereq": ["React Basics"]},
            {"name": "Next.js", "status": "locked", "prereq": ["State Management", "React Hooks"]},
        ]
    else:
        topics = [
            {"name": "Introduction", "status": "completed", "prereq": []},
            {"name": "Core Concepts", "status": "available", "prereq": ["Introduction"]},
            {"name": "Advanced Topics", "status": "locked", "prereq": ["Core Concepts"]},
        ]
    
    # Display topics as cards
    for topic in topics:
        status_icons = {
            "completed": "✅",
            "available": "📖",
            "locked": "🔒"
        }
        
        status_colors = {
            "completed": "success",
            "available": "info",
            "locked": "secondary"
        }
        
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown(f"**{status_icons[topic['status']]} {topic['name']}**")
            if topic['prereq']:
                st.caption(f"Prerequisites: {', '.join(topic['prereq'])}")
        
        with col2:
            if topic['status'] == "available":
                if st.button("Start", key=f"start_{topic['name']}", use_container_width=True):
                    st.success(f"Starting {topic['name']}...")
            elif topic['status'] == "completed":
                st.button("Review", key=f"review_{topic['name']}", use_container_width=True)
            else:
                st.button("Locked", key=f"locked_{topic['name']}", disabled=True, use_container_width=True)
        
        st.divider()


def _render_milestones():
    """Render milestone achievements."""
    st.markdown("### 🏆 Milestone Achievements")
    
    milestones = [
        {"name": "First Steps", "description": "Complete your first topic", "achieved": True},
        {"name": "Quick Learner", "description": "Complete 5 topics", "achieved": True},
        {"name": "Dedicated Student", "description": "Complete 10 topics", "achieved": False},
        {"name": "Path Master", "description": "Complete entire learning path", "achieved": False},
    ]
    
    cols = st.columns(4)
    for i, milestone in enumerate(milestones):
        with cols[i]:
            if milestone["achieved"]:
                st.success(f"🏅 {milestone['name']}")
            else:
                st.info(f"⭕ {milestone['name']}")
            st.caption(milestone["description"])
