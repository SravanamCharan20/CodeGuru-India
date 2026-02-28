"""Generate flashcards and quizzes from chat history."""

from __future__ import annotations

import re
import uuid
from typing import Any, Dict, List, Tuple


class ChatLearningGenerator:
    """Creates revision material from user-assistant chat exchanges."""

    def __init__(self, orchestrator=None):
        self.orchestrator = orchestrator

    def generate_flashcards(
        self,
        chat_messages: List[Dict[str, Any]],
        language: str = "english",
        limit: int = 12,
    ) -> List[Dict[str, Any]]:
        pairs = self._extract_qa_pairs(chat_messages)[:limit]
        cards = []
        for user_q, assistant_a in pairs:
            cards.append(
                {
                    "id": str(uuid.uuid4()),
                    "front": self._clean_text(user_q, 220),
                    "back": self._clean_text(assistant_a, 420),
                    "topic": "Codebase Chat",
                    "difficulty": "intermediate",
                    "language": language,
                }
            )
        return cards

    def generate_quiz(
        self,
        chat_messages: List[Dict[str, Any]],
        language: str = "english",
        num_questions: int = 6,
    ) -> Dict[str, Any]:
        pairs = self._extract_qa_pairs(chat_messages)
        questions = []

        for index, (user_q, assistant_a) in enumerate(pairs[:num_questions], start=1):
            correct = self._clean_text(assistant_a, 170)
            options = self._build_options(correct)
            questions.append(
                {
                    "id": str(index),
                    "type": "multiple_choice",
                    "question_text": f"Best answer for: {self._clean_text(user_q, 140)}",
                    "options": options,
                    "correct_answer": correct,
                    "explanation": "Derived from your codebase chat explanation.",
                    "language": language,
                }
            )

        return {
            "id": f"chat_quiz_{uuid.uuid4().hex[:8]}",
            "topic": "Codebase Chat Revision",
            "questions": questions,
            "time_limit_minutes": max(1, len(questions) * 2),
            "language": language,
        }

    def _extract_qa_pairs(self, chat_messages: List[Dict[str, Any]]) -> List[Tuple[str, str]]:
        pairs: List[Tuple[str, str]] = []
        pending_question = None

        for message in chat_messages:
            role = message.get("role")
            content = message.get("content", "").strip()
            if not content:
                continue

            if role == "user":
                pending_question = content
                continue

            if role == "assistant" and pending_question:
                pairs.append((pending_question, content))
                pending_question = None

        return pairs

    def _clean_text(self, text: str, max_len: int) -> str:
        sanitized = re.sub(r"\s+", " ", text or "").strip()
        if len(sanitized) <= max_len:
            return sanitized
        return sanitized[: max_len - 3].rstrip() + "..."

    def _build_options(self, correct_answer: str) -> List[str]:
        distractors = [
            "This behavior is controlled by a separate config not shown here.",
            "It is handled entirely in frontend styling logic.",
            "It relies only on environment variables and no code path.",
        ]
        options = [correct_answer] + distractors
        return options
