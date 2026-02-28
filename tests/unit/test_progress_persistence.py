"""Tests for progress persistence and tracker stats integrity."""

from session_manager import SessionManager
from learning.progress_tracker import ProgressTracker


def test_save_progress_keeps_flat_payload():
    manager = SessionManager()

    payload = {
        "topics_completed": ["topic_1"],
        "quizzes": [],
        "activities": [],
        "skill_levels": {},
        "streak_data": {"current_streak": 0, "last_activity_date": None, "longest_streak": 0},
    }
    manager.save_progress("topic_completed", payload)

    loaded = manager.load_progress()
    assert isinstance(loaded, dict)
    assert "data" not in loaded
    assert loaded.get("topics_completed") == ["topic_1"]


def test_progress_tracker_stats_use_recorded_activities():
    manager = SessionManager()
    tracker = ProgressTracker(manager)

    tracker.record_activity(
        "topic_completed",
        {
            "topic_id": "auth_topic",
            "topic_name": "Authentication Flow",
            "skill": "backend",
        },
    )
    tracker.record_activity(
        "quiz_taken",
        {
            "topic": "Authentication",
            "score": 80,
            "skill": "backend",
        },
    )

    stats = tracker.get_statistics()
    assert stats.topics_completed == 1
    assert stats.quizzes_taken == 1
    assert stats.average_quiz_score == 80
    assert stats.total_time_minutes >= 30
    assert stats.skill_levels.get("backend", 0) >= 13
