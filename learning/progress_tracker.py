"""Progress tracker for monitoring user learning progress."""
from dataclasses import dataclass
from typing import Dict, List
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
    
    def __init__(self, session_manager: SessionManager):
        """Initialize with session manager."""
        self.session_manager = session_manager
        self._ensure_progress_structure()
    
    def _ensure_progress_structure(self):
        """Ensure progress data structure exists in session."""
        progress = self.session_manager.load_progress()
        
        if not progress:
            progress = {
                "topics_completed": [],
                "quizzes": [],
                "activities": [],
                "skill_levels": {},
                "streak_data": {
                    "current_streak": 0,
                    "last_activity_date": None,
                    "longest_streak": 0
                }
            }
            self.session_manager.save_progress("init", progress)
    
    def record_activity(self, activity_type: str, details: Dict) -> None:
        """
        Record a learning activity.
        
        Args:
            activity_type: Type of activity (topic_completed, quiz_taken, etc.)
            details: Activity details
        """
        try:
            progress = self.session_manager.load_progress()
            
            # Add activity to log
            activity = {
                "type": activity_type,
                "timestamp": datetime.now().isoformat(),
                "details": details
            }
            
            if "activities" not in progress:
                progress["activities"] = []
            progress["activities"].append(activity)
            
            # Update specific counters
            if activity_type == "topic_completed":
                if "topics_completed" not in progress:
                    progress["topics_completed"] = []
                progress["topics_completed"].append(details.get("topic_id", ""))
                
                # Update skill level
                skill = details.get("skill", "general")
                if "skill_levels" not in progress:
                    progress["skill_levels"] = {}
                progress["skill_levels"][skill] = progress["skill_levels"].get(skill, 0) + 5
            
            elif activity_type == "quiz_taken":
                if "quizzes" not in progress:
                    progress["quizzes"] = []
                progress["quizzes"].append({
                    "topic": details.get("topic", ""),
                    "score": details.get("score", 0),
                    "timestamp": datetime.now().isoformat()
                })
                
                # Update skill level based on score
                skill = details.get("skill", "general")
                score = details.get("score", 0)
                if "skill_levels" not in progress:
                    progress["skill_levels"] = {}
                progress["skill_levels"][skill] = min(
                    progress["skill_levels"].get(skill, 0) + int(score / 10),
                    100
                )
            
            # Update streak
            self._update_streak(progress)
            
            # Save progress
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
            progress = self.session_manager.load_progress()
            
            topics_completed = len(progress.get("topics_completed", []))
            quizzes = progress.get("quizzes", [])
            quizzes_taken = len(quizzes)
            
            # Calculate average quiz score
            if quizzes:
                total_score = sum(q.get("score", 0) for q in quizzes)
                average_score = total_score / len(quizzes)
            else:
                average_score = 0.0
            
            # Calculate total time (estimate based on activities)
            activities = progress.get("activities", [])
            total_time = len(activities) * 15  # Assume 15 min per activity
            
            # Get current streak
            streak_data = progress.get("streak_data", {})
            current_streak = streak_data.get("current_streak", 0)
            
            # Get skill levels
            skill_levels = progress.get("skill_levels", {})
            
            return ProgressStats(
                topics_completed=topics_completed,
                quizzes_taken=quizzes_taken,
                average_quiz_score=average_score,
                total_time_minutes=total_time,
                current_streak=current_streak,
                skill_levels=skill_levels
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
            progress = self.session_manager.load_progress()
            return progress.get("skill_levels", {})
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
            progress = self.session_manager.load_progress()
            streak_data = progress.get("streak_data", {})
            return streak_data.get("current_streak", 0)
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
            progress = self.session_manager.load_progress()
            activities = progress.get("activities", [])
            
            # Filter activities from last 7 days
            week_ago = datetime.now() - timedelta(days=7)
            recent_activities = []
            
            for activity in activities:
                try:
                    activity_date = datetime.fromisoformat(activity.get("timestamp", ""))
                    if activity_date >= week_ago:
                        recent_activities.append(activity)
                except:
                    continue
            
            # Extract topics learned
            topics_learned = []
            quiz_scores = []
            
            for activity in recent_activities:
                if activity.get("type") == "topic_completed":
                    topic = activity.get("details", {}).get("topic_name", "Unknown")
                    topics_learned.append(topic)
                elif activity.get("type") == "quiz_taken":
                    score = activity.get("details", {}).get("score", 0)
                    quiz_scores.append(score)
            
            return WeeklySummary(
                activities_completed=len(recent_activities),
                time_spent_minutes=len(recent_activities) * 15,
                topics_learned=topics_learned,
                quiz_scores=quiz_scores
            )
        
        except Exception as e:
            logger.error(f"Failed to get weekly summary: {e}")
            return WeeklySummary(0, 0, [], [])
    
    def _update_streak(self, progress: Dict) -> None:
        """Update learning streak based on activity."""
        try:
            streak_data = progress.get("streak_data", {
                "current_streak": 0,
                "last_activity_date": None,
                "longest_streak": 0
            })
            
            today = datetime.now().date()
            last_date_str = streak_data.get("last_activity_date")
            
            if last_date_str:
                last_date = datetime.fromisoformat(last_date_str).date()
                days_diff = (today - last_date).days
                
                if days_diff == 0:
                    # Same day, no change
                    pass
                elif days_diff == 1:
                    # Consecutive day, increment streak
                    streak_data["current_streak"] += 1
                else:
                    # Streak broken, reset
                    streak_data["current_streak"] = 1
            else:
                # First activity
                streak_data["current_streak"] = 1
            
            # Update last activity date
            streak_data["last_activity_date"] = today.isoformat()
            
            # Update longest streak
            if streak_data["current_streak"] > streak_data.get("longest_streak", 0):
                streak_data["longest_streak"] = streak_data["current_streak"]
            
            progress["streak_data"] = streak_data
        
        except Exception as e:
            logger.error(f"Failed to update streak: {e}")
