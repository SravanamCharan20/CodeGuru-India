"""Progress tracker for monitoring user learning progress."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List
from datetime import datetime, timedelta
from session_manager import SessionManager
import logging

logger = logging.getLogger(__name__)


@dataclass
class ProgressStats:
    """Overall learning statistics."""

    topics_completed: int
    quizzes_taken: int
    average_quiz_score: float
    total_time_minutes: int
    current_streak: int
    skill_levels: Dict[str, int]


@dataclass
class WeeklySummary:
    """Summary of past week's activities."""

    activities_completed: int
    time_spent_minutes: int
    topics_learned: List[str]
    quiz_scores: List[float]


class ProgressTracker:
    """Tracks and visualizes user learning progress."""

    DEFAULT_ACTIVITY_MINUTES = {
        "topic_completed": 20,
        "quiz_taken": 12,
        "flashcard_reviewed": 2,
        "flashcard_mastered": 3,
        "analysis_completed": 10,
        "chat_query": 4,
    }

    def __init__(self, session_manager: SessionManager):
        """Initialize with session manager."""
        self.session_manager = session_manager
        self._ensure_progress_structure()

    def _ensure_progress_structure(self):
        """Ensure progress data structure exists in session."""
        progress = self.session_manager.load_progress() or {}

        changed = False
        if "topics_completed" not in progress:
            progress["topics_completed"] = []
            changed = True
        if "quizzes" not in progress:
            progress["quizzes"] = []
            changed = True
        if "activities" not in progress:
            progress["activities"] = []
            changed = True
        if "skill_levels" not in progress:
            progress["skill_levels"] = {}
            changed = True
        if "totals" not in progress:
            progress["totals"] = {"minutes_spent": 0}
            changed = True
        if "streak_data" not in progress:
            progress["streak_data"] = {
                "current_streak": 0,
                "last_activity_date": None,
                "longest_streak": 0,
            }
            changed = True

        if changed:
            self.session_manager.save_progress("init", progress)

    def record_activity(self, activity_type: str, details: Dict[str, Any]) -> None:
        """
        Record a learning activity.

        Args:
            activity_type: Type of activity (topic_completed, quiz_taken, etc.)
            details: Activity details
        """
        try:
            details = details or {}
            progress = self.session_manager.load_progress() or {}
            self._bootstrap_progress(progress)

            minutes_spent = self._resolve_minutes_spent(activity_type, details)

            activity = {
                "type": activity_type,
                "timestamp": datetime.now().isoformat(),
                "minutes_spent": minutes_spent,
                "details": details,
            }
            progress["activities"].append(activity)
            progress["totals"]["minutes_spent"] = progress["totals"].get("minutes_spent", 0) + minutes_spent

            if activity_type == "topic_completed":
                topic_id = (
                    details.get("topic_id")
                    or details.get("topic")
                    or details.get("topic_name")
                    or ""
                )
                if topic_id and topic_id not in progress["topics_completed"]:
                    progress["topics_completed"].append(topic_id)

                skill = details.get("skill", "general")
                self._increase_skill(progress, skill, 8)

            elif activity_type == "quiz_taken":
                score = self._safe_float(details.get("score", 0.0))
                progress["quizzes"].append(
                    {
                        "topic": details.get("topic", ""),
                        "score": score,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

                skill = details.get("skill", "general")
                gain = max(2, int(score / 10))
                self._increase_skill(progress, skill, gain)

            elif activity_type in {"flashcard_reviewed", "flashcard_mastered"}:
                skill = details.get("skill", "general")
                self._increase_skill(progress, skill, 2 if activity_type == "flashcard_mastered" else 1)

            elif activity_type in {"analysis_completed", "chat_query"}:
                skill = details.get("skill", "codebase")
                self._increase_skill(progress, skill, 1)

            self._update_streak(progress)
            self.session_manager.save_progress(activity_type, progress)

        except Exception as e:
            logger.error(f"Failed to record activity: {e}")

    def get_statistics(self) -> ProgressStats:
        """
        Get overall learning statistics.

        Returns:
            Progress statistics
        """
        try:
            progress = self.session_manager.load_progress() or {}
            self._bootstrap_progress(progress)

            topics_completed = len(set(progress.get("topics_completed", [])))
            quizzes = progress.get("quizzes", [])
            quizzes_taken = len(quizzes)

            if quizzes:
                total_score = sum(self._safe_float(q.get("score", 0)) for q in quizzes)
                average_score = total_score / len(quizzes)
            else:
                average_score = 0.0

            total_time = int(progress.get("totals", {}).get("minutes_spent", 0))
            if total_time <= 0:
                total_time = sum(
                    int(activity.get("minutes_spent", 0))
                    for activity in progress.get("activities", [])
                )

            streak_data = progress.get("streak_data", {})
            current_streak = int(streak_data.get("current_streak", 0))

            skill_levels = {
                key: min(100, int(value))
                for key, value in progress.get("skill_levels", {}).items()
            }

            return ProgressStats(
                topics_completed=topics_completed,
                quizzes_taken=quizzes_taken,
                average_quiz_score=average_score,
                total_time_minutes=max(0, total_time),
                current_streak=max(0, current_streak),
                skill_levels=skill_levels,
            )

        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            return ProgressStats(0, 0, 0.0, 0, 0, {})

    def get_skill_levels(self) -> Dict[str, int]:
        """
        Get skill level for each technology.

        Returns:
            Dictionary of skill levels (0-100)
        """
        try:
            progress = self.session_manager.load_progress() or {}
            levels = progress.get("skill_levels", {})
            return {key: min(100, int(value)) for key, value in levels.items()}
        except Exception as e:
            logger.error(f"Failed to get skill levels: {e}")
            return {}

    def calculate_streak(self) -> int:
        """
        Calculate current learning streak in days.

        Returns:
            Current streak count
        """
        try:
            progress = self.session_manager.load_progress() or {}
            streak_data = progress.get("streak_data", {})
            return int(streak_data.get("current_streak", 0))
        except Exception as e:
            logger.error(f"Failed to calculate streak: {e}")
            return 0

    def get_weekly_summary(self) -> WeeklySummary:
        """
        Get summary of past week's activities.

        Returns:
            Weekly summary
        """
        try:
            progress = self.session_manager.load_progress() or {}
            activities = progress.get("activities", [])
            week_ago = datetime.now() - timedelta(days=7)
            recent_activities = []

            for activity in activities:
                try:
                    activity_date = datetime.fromisoformat(activity.get("timestamp", ""))
                    if activity_date >= week_ago:
                        recent_activities.append(activity)
                except Exception:
                    continue

            topics_seen = set()
            topics_learned = []
            quiz_scores = []
            time_spent = 0

            for activity in recent_activities:
                activity_type = activity.get("type")
                details = activity.get("details", {})
                time_spent += int(activity.get("minutes_spent", 0))

                if activity_type == "topic_completed":
                    topic = details.get("topic_name") or details.get("topic") or "Unknown Topic"
                    if topic not in topics_seen:
                        topics_seen.add(topic)
                        topics_learned.append(topic)
                elif activity_type == "quiz_taken":
                    quiz_scores.append(self._safe_float(details.get("score", 0)))

            return WeeklySummary(
                activities_completed=len(recent_activities),
                time_spent_minutes=max(0, time_spent),
                topics_learned=topics_learned,
                quiz_scores=quiz_scores,
            )

        except Exception as e:
            logger.error(f"Failed to get weekly summary: {e}")
            return WeeklySummary(0, 0, [], [])

    def _update_streak(self, progress: Dict[str, Any]) -> None:
        """Update learning streak based on activity."""
        try:
            streak_data = progress.get(
                "streak_data",
                {
                    "current_streak": 0,
                    "last_activity_date": None,
                    "longest_streak": 0,
                },
            )

            today = datetime.now().date()
            last_date_str = streak_data.get("last_activity_date")

            if last_date_str:
                last_date = datetime.fromisoformat(last_date_str).date()
                days_diff = (today - last_date).days

                if days_diff == 0:
                    pass
                elif days_diff == 1:
                    streak_data["current_streak"] = int(streak_data.get("current_streak", 0)) + 1
                else:
                    streak_data["current_streak"] = 1
            else:
                streak_data["current_streak"] = 1

            streak_data["last_activity_date"] = today.isoformat()
            if int(streak_data.get("current_streak", 0)) > int(streak_data.get("longest_streak", 0)):
                streak_data["longest_streak"] = int(streak_data["current_streak"])

            progress["streak_data"] = streak_data

        except Exception as e:
            logger.error(f"Failed to update streak: {e}")

    def _bootstrap_progress(self, progress: Dict[str, Any]) -> None:
        progress.setdefault("topics_completed", [])
        progress.setdefault("quizzes", [])
        progress.setdefault("activities", [])
        progress.setdefault("skill_levels", {})
        progress.setdefault("totals", {"minutes_spent": 0})
        progress.setdefault(
            "streak_data",
            {
                "current_streak": 0,
                "last_activity_date": None,
                "longest_streak": 0,
            },
        )

    def _increase_skill(self, progress: Dict[str, Any], skill: str, delta: int) -> None:
        if not skill:
            skill = "general"
        current = int(progress["skill_levels"].get(skill, 0))
        progress["skill_levels"][skill] = min(100, current + max(0, int(delta)))

    def _resolve_minutes_spent(self, activity_type: str, details: Dict[str, Any]) -> int:
        explicit = details.get("minutes_spent")
        if explicit is not None:
            try:
                return max(1, int(explicit))
            except Exception:
                pass
        return self.DEFAULT_ACTIVITY_MINUTES.get(activity_type, 5)

    def _safe_float(self, value: Any) -> float:
        try:
            return float(value)
        except Exception:
            return 0.0
