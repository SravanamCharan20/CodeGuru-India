"""Progress dashboard component."""

from __future__ import annotations

from datetime import datetime, timedelta

import pandas as pd
import streamlit as st
from ui.design_system import section_header, spacing


def render_progress_dashboard():
    """Render streamlined progress dashboard with real data only."""
    section_header("Learning Progress", "Real activity from your quizzes, paths, chat and analysis")

    progress_tracker = st.session_state.get("progress_tracker")
    if not progress_tracker:
        st.warning("Progress tracker is not initialized.")
        return

    stats = progress_tracker.get_statistics()
    progress_payload = progress_tracker.session_manager.load_progress() or {}
    activities = progress_payload.get("activities", [])

    _render_top_metrics(stats)
    spacing("md")

    if not activities:
        st.info("No progress yet. Complete a path step, ask codebase chat questions, or take a quiz.")
        return

    tab1, tab2, tab3 = st.tabs(["📈 Activity Trend", "🧾 Recent Activity", "🎯 Skill Growth"])
    with tab1:
        _render_activity_trend(activities)
    with tab2:
        _render_recent_activity(activities, progress_tracker)
    with tab3:
        _render_skills(stats.skill_levels)


def _render_top_metrics(stats) -> None:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Topics", str(stats.topics_completed))
    with col2:
        st.metric("Quizzes", str(stats.quizzes_taken))
    with col3:
        st.metric("Avg Quiz", f"{int(stats.average_quiz_score)}%")
    with col4:
        st.metric("Streak", f"{stats.current_streak} day(s)")
    with col5:
        hours = stats.total_time_minutes // 60
        minutes = stats.total_time_minutes % 60
        st.metric("Time", f"{hours}h {minutes}m")


def _render_activity_trend(activities) -> None:
    section_header("Trend (Last 30 Days)")

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=29)
    date_range = [start_date + timedelta(days=i) for i in range(30)]

    by_day_minutes = {day: 0 for day in date_range}
    by_day_topics = {day: 0 for day in date_range}
    by_day_quiz_scores = {day: [] for day in date_range}

    for activity in activities:
        try:
            day = datetime.fromisoformat(activity.get("timestamp", "")).date()
        except Exception:
            continue
        if day < start_date or day > end_date:
            continue

        by_day_minutes[day] += int(activity.get("minutes_spent", 0))
        if activity.get("type") == "topic_completed":
            by_day_topics[day] += 1
        if activity.get("type") == "quiz_taken":
            details = activity.get("details", {})
            score = details.get("score")
            if isinstance(score, (int, float)):
                by_day_quiz_scores[day].append(float(score))

    cumulative_topics = []
    total_topics = 0
    avg_quiz_scores = []
    for day in date_range:
        total_topics += by_day_topics[day]
        cumulative_topics.append(total_topics)
        scores = by_day_quiz_scores[day]
        avg_quiz_scores.append((sum(scores) / len(scores)) if scores else None)

    chart_df = pd.DataFrame(
        {
            "Date": pd.to_datetime(date_range),
            "Minutes": [by_day_minutes[day] for day in date_range],
            "Cumulative Topics": cumulative_topics,
            "Quiz Score": avg_quiz_scores,
        }
    )

    col1, col2 = st.columns(2)
    with col1:
        st.caption("Time spent (minutes per day)")
        st.bar_chart(chart_df.set_index("Date")["Minutes"], use_container_width=True)
    with col2:
        st.caption("Cumulative topics completed")
        st.line_chart(chart_df.set_index("Date")["Cumulative Topics"], use_container_width=True)

    quiz_series = chart_df["Quiz Score"].dropna()
    if not quiz_series.empty:
        st.caption("Daily average quiz score")
        st.line_chart(chart_df.set_index("Date")["Quiz Score"], use_container_width=True)
    else:
        st.caption("No quiz score trend yet.")


def _render_recent_activity(activities, progress_tracker) -> None:
    section_header("Recent Activity")

    recent = sorted(
        activities,
        key=lambda item: item.get("timestamp", ""),
        reverse=True,
    )[:12]

    if not recent:
        st.info("No recent activity.")
        return

    for item in recent:
        timestamp = item.get("timestamp", "")
        activity_type = item.get("type", "activity")
        minutes = item.get("minutes_spent", 0)
        details = item.get("details", {}) or {}
        topic = details.get("topic_name") or details.get("topic") or details.get("path") or "Learning activity"

        try:
            when = datetime.fromisoformat(timestamp).strftime("%Y-%m-%d %H:%M")
        except Exception:
            when = timestamp

        st.markdown(f"**{activity_type}** - {topic}")
        st.caption(f"{when} | {minutes} min")
        if activity_type == "quiz_taken":
            st.caption(f"Score: {details.get('score', 0)}")
        st.divider()

    summary = progress_tracker.get_weekly_summary()
    st.info(
        f"This week: {summary.activities_completed} activities, "
        f"{summary.time_spent_minutes} min, "
        f"{len(summary.topics_learned)} topics, "
        f"{len(summary.quiz_scores)} quizzes."
    )


def _render_skills(skill_levels) -> None:
    section_header("Skill Growth")
    if not skill_levels:
        st.info("No skill growth yet. Complete path steps and quizzes to build skill score.")
        return

    ordered = sorted(skill_levels.items(), key=lambda item: item[1], reverse=True)
    for skill, level in ordered:
        st.markdown(f"**{skill}** - {level}/100")
        st.progress(min(100, max(0, level)) / 100)
