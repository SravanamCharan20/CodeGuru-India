"""Progress dashboard component."""
import streamlit as st
from ui.design_system import section_header, spacing, metric_card


def render_progress_dashboard():
    """Render progress tracking dashboard."""
    section_header("Your Learning Progress", "Track your journey, celebrate your achievements")
    
    # Get progress tracker
    progress_tracker = st.session_state.get("progress_tracker", None)
    
    if progress_tracker:
        stats = progress_tracker.get_statistics()
        _render_real_dashboard(stats, progress_tracker)
    else:
        _render_mock_dashboard()


def _render_real_dashboard(stats, progress_tracker):
    """Render dashboard with real data."""
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_card(
            str(stats.topics_completed),
            "Topics Completed",
            "+3 this week" if stats.topics_completed > 0 else None
        )
    
    with col2:
        metric_card(
            f"{int(stats.average_quiz_score)}%",
            "Avg Quiz Score",
            "+5%" if stats.average_quiz_score > 0 else None
        )
    
    with col3:
        metric_card(
            f"{stats.current_streak}",
            "Day Streak",
            "+1 day" if stats.current_streak > 0 else None
        )
    
    with col4:
        metric_card(
            f"{stats.total_time_minutes // 60}h",
            "Time Spent",
            f"+{stats.total_time_minutes % 60}m"
        )
    
    spacing("lg")
    _render_progress_charts()
    spacing("lg")
    _render_skill_levels(stats.skill_levels)
    spacing("lg")
    _render_weekly_summary(progress_tracker)
    spacing("lg")
    _render_achievements()


def _render_mock_dashboard():
    """Render dashboard with mock data."""
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_card("24", "Topics Completed", "+3 this week")
    with col2:
        metric_card("78%", "Avg Quiz Score", "+5%")
    with col3:
        metric_card("12", "Day Streak", "+1 day")
    with col4:
        metric_card("45h", "Time Spent", "+8h")
    
    spacing("lg")
    _render_progress_charts()
    spacing("lg")
    _render_skill_levels({})
    spacing("lg")
    _render_weekly_summary(None)
    spacing("lg")
    _render_achievements()


def _render_progress_charts():
    """Render progress charts."""
    section_header("Progress Over Time")
    
    import pandas as pd
    import numpy as np
    
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    topics_completed = np.cumsum(np.random.randint(0, 3, 30))
    quiz_scores = np.random.randint(60, 95, 30)
    
    chart_data = pd.DataFrame({
        'Date': dates,
        'Topics Completed': topics_completed,
        'Quiz Score': quiz_scores
    })
    
    tab1, tab2 = st.tabs(["📚 Topics Progress", "📝 Quiz Performance"])
    
    with tab1:
        st.line_chart(chart_data.set_index('Date')['Topics Completed'], use_container_width=True)
        st.caption("📊 Cumulative topics completed over the last 30 days")
    
    with tab2:
        st.line_chart(chart_data.set_index('Date')['Quiz Score'], use_container_width=True)
        st.caption("📊 Quiz scores over the last 30 days")


def _render_skill_levels(skill_levels: dict = None):
    """Render skill level progress bars."""
    section_header("🎯 Skill Levels", "Your expertise across technologies")
    
    if skill_levels and len(skill_levels) > 0:
        skills = skill_levels
    else:
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
            st.markdown(f"""
            <div style="
                background: white;
                border-radius: 12px;
                padding: 1.2rem;
                margin-bottom: 1rem;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                border: 1px solid #e2e8f0;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-weight: 600; color: #2d3748;">{skill}</span>
                    <span style="
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        font-weight: 700;
                    ">{level}/100</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(level / 100)
            st.caption(_get_skill_label(level))
            spacing("sm")


def _get_skill_label(level):
    """Get skill level label."""
    if level < 30:
        return "🌱 Beginner - Keep practicing!"
    elif level < 60:
        return "📚 Learning - You're making progress!"
    elif level < 80:
        return "💪 Proficient - Great work!"
    else:
        return "🏆 Expert - Outstanding!"


def _render_weekly_summary(progress_tracker=None):
    """Render weekly summary."""
    section_header("📅 This Week's Summary", "Your recent achievements")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
            border-radius: 12px;
            padding: 1.5rem;
            border-left: 4px solid #10b981;
        ">
            <h4 style="color: #065f46; margin-bottom: 1rem;">✅ Activities Completed</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if progress_tracker:
            summary = progress_tracker.get_weekly_summary()
            if summary.topics_learned:
                for topic in summary.topics_learned[:5]:
                    st.markdown(f"• Completed **{topic}** topic")
            else:
                st.info("No activities this week yet. Start learning!")
        else:
            activities = [
                "• Completed **React Hooks** topic",
                "• Scored **85%** on JavaScript quiz",
                "• Reviewed **15 flashcards**",
                "• Started **Node.js APIs** learning path"
            ]
            for activity in activities:
                st.markdown(activity)
    
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border-radius: 12px;
            padding: 1.5rem;
            border-left: 4px solid #3b82f6;
        ">
            <h4 style="color: #1e40af; margin-bottom: 1rem;">📊 Learning Stats</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if progress_tracker:
            summary = progress_tracker.get_weekly_summary()
            st.markdown(f"⏱️ **{summary.time_spent_minutes // 60}h {summary.time_spent_minutes % 60}m** learning time")
            st.markdown(f"📚 **{len(summary.topics_learned)} topics** completed")
            st.markdown(f"📝 **{len(summary.quiz_scores)} quizzes** taken")
            if summary.quiz_scores:
                avg_score = sum(summary.quiz_scores) / len(summary.quiz_scores)
                st.markdown(f"🎯 **{int(avg_score)}%** average score")
        else:
            st.markdown("⏱️ **8 hours** of learning time")
            st.markdown("📚 **3 topics** completed")
            st.markdown("📝 **2 quizzes** taken")
            st.markdown("🗂️ **15 flashcards** reviewed")


def _render_achievements():
    """Render achievement badges."""
    section_header("🏆 Achievement Badges", "Celebrate your milestones")
    
    achievements = [
        {"name": "First Steps", "icon": "🎯", "earned": True, "date": "Jan 15, 2024", "desc": "Complete your first topic"},
        {"name": "Quick Learner", "icon": "⚡", "earned": True, "date": "Jan 22, 2024", "desc": "Complete 5 topics"},
        {"name": "Code Master", "icon": "👨‍💻", "earned": True, "date": "Feb 5, 2024", "desc": "Analyze 10 code files"},
        {"name": "Quiz Champion", "icon": "🏅", "earned": True, "date": "Feb 12, 2024", "desc": "Score 90%+ on 5 quizzes"},
        {"name": "Streak Keeper", "icon": "🔥", "earned": True, "date": "Feb 18, 2024", "desc": "Maintain 7-day streak"},
        {"name": "Path Completer", "icon": "🛤️", "earned": False, "date": "", "desc": "Complete a learning path"},
        {"name": "Perfect Score", "icon": "💯", "earned": False, "date": "", "desc": "Score 100% on a quiz"},
        {"name": "Dedication Award", "icon": "⭐", "earned": False, "date": "", "desc": "Learn for 50 hours"},
    ]
    
    cols = st.columns(4)
    
    for i, achievement in enumerate(achievements):
        with cols[i % 4]:
            if achievement["earned"]:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
                    border-radius: 12px;
                    padding: 1.5rem;
                    text-align: center;
                    border: 2px solid #f59e0b;
                    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.2);
                ">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">{achievement['icon']}</div>
                    <div style="font-weight: 600; color: #92400e; margin-bottom: 0.3rem;">{achievement['name']}</div>
                    <div style="font-size: 0.8rem; color: #b45309; margin-bottom: 0.5rem;">{achievement['desc']}</div>
                    <div style="font-size: 0.75rem; color: #d97706;">✓ {achievement['date']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="
                    background: #f7fafc;
                    border-radius: 12px;
                    padding: 1.5rem;
                    text-align: center;
                    border: 2px dashed #cbd5e0;
                    opacity: 0.6;
                ">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem; filter: grayscale(100%);">{achievement['icon']}</div>
                    <div style="font-weight: 600; color: #718096; margin-bottom: 0.3rem;">{achievement['name']}</div>
                    <div style="font-size: 0.8rem; color: #a0aec0;">{achievement['desc']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            spacing("sm")
