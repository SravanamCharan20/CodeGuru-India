"""Progress dashboard component."""
import streamlit as st


def render_progress_dashboard():
    """Render progress tracking dashboard."""
    st.title("📊 Your Learning Progress")
    
    # Get progress tracker
    progress_tracker = st.session_state.get("progress_tracker", None)
    
    if progress_tracker:
        # Get real statistics
        stats = progress_tracker.get_statistics()
        
        # Key metrics
        st.markdown("### 📈 Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Topics Completed",
                stats.topics_completed,
                delta="+3 this week" if stats.topics_completed > 0 else None,
                delta_color="normal"
            )
        
        with col2:
            st.metric(
                "Avg Quiz Score",
                f"{int(stats.average_quiz_score)}%",
                delta="+5%" if stats.average_quiz_score > 0 else None,
                delta_color="normal"
            )
        
        with col3:
            st.metric(
                "Learning Streak",
                f"{stats.current_streak} days",
                delta="+1" if stats.current_streak > 0 else None,
                delta_color="normal"
            )
        
        with col4:
            st.metric(
                "Time Spent",
                f"{stats.total_time_minutes // 60} hrs",
                delta=f"+{stats.total_time_minutes % 60} min",
                delta_color="normal"
            )
        
        st.divider()
        
        # Progress visualizations
        _render_progress_charts()
        
        st.divider()
        
        # Skill levels
        _render_skill_levels(stats.skill_levels)
        
        st.divider()
        
        # Weekly summary
        _render_weekly_summary(progress_tracker)
        
        st.divider()
        
        # Achievement badges
        _render_achievements()
    else:
        # Fallback to mock data
        _render_mock_dashboard()


def _render_mock_dashboard():
    """Render dashboard with mock data."""
    st.markdown("### 📈 Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Topics Completed", "24", delta="+3 this week", delta_color="normal")
    with col2:
        st.metric("Avg Quiz Score", "78%", delta="+5%", delta_color="normal")
    with col3:
        st.metric("Learning Streak", "12 days", delta="+1", delta_color="normal")
    with col4:
        st.metric("Time Spent", "45 hrs", delta="+8 hrs", delta_color="normal")
    
    st.divider()
    _render_progress_charts()
    st.divider()
    _render_skill_levels({})
    st.divider()
    _render_weekly_summary(None)
    st.divider()
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


def _render_skill_levels(skill_levels: dict = None):
    """Render skill level progress bars."""
    st.markdown("### 🎯 Skill Levels")
    
    if skill_levels and len(skill_levels) > 0:
        # Use real skill levels
        skills = skill_levels
    else:
        # Use mock data
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


def _render_weekly_summary(progress_tracker=None):
    """Render weekly summary."""
    st.markdown("### 📅 This Week's Summary")
    
    if progress_tracker:
        # Get real weekly summary
        summary = progress_tracker.get_weekly_summary()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Activities Completed")
            if summary.topics_learned:
                for topic in summary.topics_learned[:5]:  # Show first 5
                    st.markdown(f"✅ Completed '{topic}' topic")
            else:
                st.info("No activities this week yet. Start learning!")
        
        with col2:
            st.markdown("#### Learning Stats")
            st.info(f"⏱️ **{summary.time_spent_minutes // 60} hours {summary.time_spent_minutes % 60} min** of learning time")
            st.info(f"📚 **{len(summary.topics_learned)} topics** completed")
            st.info(f"📝 **{len(summary.quiz_scores)} quizzes** taken")
            if summary.quiz_scores:
                avg_score = sum(summary.quiz_scores) / len(summary.quiz_scores)
                st.info(f"🎯 **{int(avg_score)}% average** quiz score")
    else:
        # Mock data
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
