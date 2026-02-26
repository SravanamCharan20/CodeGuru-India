"""Progress dashboard component."""
import streamlit as st


def render_progress_dashboard():
    """Render progress tracking dashboard."""
    st.title("📊 Your Learning Progress")
    
    # Key metrics
    st.markdown("### 📈 Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Topics Completed",
            "24",
            delta="+3 this week",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            "Avg Quiz Score",
            "78%",
            delta="+5%",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            "Learning Streak",
            "12 days",
            delta="+1",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            "Time Spent",
            "45 hrs",
            delta="+8 hrs",
            delta_color="normal"
        )
    
    st.divider()
    
    # Progress visualizations
    _render_progress_charts()
    
    st.divider()
    
    # Skill levels
    _render_skill_levels()
    
    st.divider()
    
    # Weekly summary
    _render_weekly_summary()
    
    st.divider()
    
    # Achievement badges
    _render_achievements()


def _render_progress_charts():
    """Render progress charts."""
    st.markdown("### 📉 Progress Over Time")
    
    # Mock chart data
    import pandas as pd
    import numpy as np
    
    # Generate mock data
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    topics_completed = np.cumsum(np.random.randint(0, 3, 30))
    quiz_scores = np.random.randint(60, 95, 30)
    
    chart_data = pd.DataFrame({
        'Date': dates,
        'Topics Completed': topics_completed,
        'Quiz Score': quiz_scores
    })
    
    tab1, tab2 = st.tabs(["Topics Progress", "Quiz Performance"])
    
    with tab1:
        st.line_chart(chart_data.set_index('Date')['Topics Completed'])
        st.caption("📚 Cumulative topics completed over the last 30 days")
    
    with tab2:
        st.line_chart(chart_data.set_index('Date')['Quiz Score'])
        st.caption("📝 Quiz scores over the last 30 days")


def _render_skill_levels():
    """Render skill level progress bars."""
    st.markdown("### 🎯 Skill Levels")
    
    skills = {
        "React": 75,
        "JavaScript": 85,
        "Node.js": 60,
        "AWS Services": 45,
        "Data Structures": 70,
        "Python": 80
    }
    
    col1, col2 = st.columns(2)
    
    for i, (skill, level) in enumerate(skills.items()):
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"**{skill}**")
            st.progress(level / 100, text=f"Level {level}/100")
            st.caption(_get_skill_label(level))


def _get_skill_label(level):
    """Get skill level label."""
    if level < 30:
        return "🌱 Beginner"
    elif level < 60:
        return "📚 Learning"
    elif level < 80:
        return "💪 Proficient"
    else:
        return "🏆 Expert"


def _render_weekly_summary():
    """Render weekly summary."""
    st.markdown("### 📅 This Week's Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Activities Completed")
        activities = [
            "✅ Completed 'React Hooks' topic",
            "✅ Scored 85% on JavaScript quiz",
            "✅ Reviewed 15 flashcards",
            "✅ Started 'Node.js APIs' learning path"
        ]
        for activity in activities:
            st.markdown(activity)
    
    with col2:
        st.markdown("#### Learning Stats")
        st.info("⏱️ **8 hours** of learning time")
        st.info("📚 **3 topics** completed")
        st.info("📝 **2 quizzes** taken")
        st.info("🗂️ **15 flashcards** reviewed")


def _render_achievements():
    """Render achievement badges."""
    st.markdown("### 🏆 Achievement Badges")
    
    achievements = [
        {"name": "First Steps", "icon": "🎯", "earned": True, "date": "Jan 15, 2024"},
        {"name": "Quick Learner", "icon": "⚡", "earned": True, "date": "Jan 22, 2024"},
        {"name": "Code Master", "icon": "👨‍💻", "earned": True, "date": "Feb 5, 2024"},
        {"name": "Quiz Champion", "icon": "🏅", "earned": True, "date": "Feb 12, 2024"},
        {"name": "Streak Keeper", "icon": "🔥", "earned": True, "date": "Feb 18, 2024"},
        {"name": "Path Completer", "icon": "🛤️", "earned": False, "date": ""},
        {"name": "Perfect Score", "icon": "💯", "earned": False, "date": ""},
        {"name": "Dedication Award", "icon": "⭐", "earned": False, "date": ""},
    ]
    
    cols = st.columns(4)
    
    for i, achievement in enumerate(achievements):
        with cols[i % 4]:
            if achievement["earned"]:
                st.success(f"{achievement['icon']} **{achievement['name']}**")
                st.caption(f"Earned: {achievement['date']}")
            else:
                st.info(f"⭕ **{achievement['name']}**")
                st.caption("Not yet earned")
