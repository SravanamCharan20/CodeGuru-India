"""Generate challenging flashcards and quizzes from chat intent themes."""

from __future__ import annotations

from dataclasses import dataclass, field
import random
import re
import uuid
from typing import Any, Dict, List, Sequence, Tuple


@dataclass
class IntentTheme:
    """Intent cluster extracted from user chat questions."""

    key: str
    intent_type: str
    objective: str
    representative_question: str
    keywords: List[str] = field(default_factory=list)
    answer_points: List[str] = field(default_factory=list)
    support_count: int = 0


class ChatLearningGenerator:
    """Creates intent-driven, challenge-oriented learning material from chat exchanges."""

    STOP_WORDS = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "if",
        "then",
        "to",
        "for",
        "of",
        "in",
        "on",
        "at",
        "with",
        "from",
        "by",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "do",
        "does",
        "did",
        "can",
        "could",
        "should",
        "would",
        "will",
        "this",
        "that",
        "these",
        "those",
        "it",
        "its",
        "how",
        "what",
        "why",
        "where",
        "when",
        "which",
        "who",
        "whom",
        "about",
        "into",
        "through",
        "across",
        "code",
        "codebase",
        "project",
        "repo",
        "repository",
        "please",
        "explain",
        "understand",
        "learn",
        "show",
        "tell",
    }

    INTENT_PATTERNS = {
        "security": [
            r"\bauth\b",
            r"\bauthentication\b",
            r"\bauthorization\b",
            r"\btoken\b",
            r"\bpermission\b",
            r"\bjwt\b",
            r"\bsecure\b",
        ],
        "flow": [
            r"\bflow\b",
            r"\brequest\b",
            r"\bpath\b",
            r"\bpipeline\b",
            r"\bend[- ]to[- ]end\b",
            r"\bsequence\b",
        ],
        "architecture": [
            r"\barchitecture\b",
            r"\bdesign\b",
            r"\bmodule\b",
            r"\blayer\b",
            r"\bpattern\b",
            r"\bcomponent\b",
        ],
        "debugging": [
            r"\bbug\b",
            r"\berror\b",
            r"\bfix\b",
            r"\bissue\b",
            r"\bfail\b",
            r"\bcrash\b",
            r"\bdebug\b",
        ],
        "performance": [
            r"\bperformance\b",
            r"\bcache\b",
            r"\boptimi",
            r"\blatency\b",
            r"\bslow\b",
            r"\bfast\b",
        ],
        "comparison": [
            r"\bcompare\b",
            r"\bdifference\b",
            r"\bvs\b",
            r"\btrade[- ]?off\b",
            r"\bbetter\b",
        ],
    }

    def __init__(self, orchestrator=None):
        self.orchestrator = orchestrator

    def generate_flashcards(
        self,
        chat_messages: List[Dict[str, Any]],
        language: str = "english",
        limit: int = 12,
    ) -> List[Dict[str, Any]]:
        """Generate challenge-oriented flashcards from extracted user intent themes."""
        pairs = self._extract_qa_pairs(chat_messages)
        themes = self._extract_intent_themes(pairs)
        cards: List[Dict[str, Any]] = []

        if not themes:
            return cards

        for theme in themes:
            cards.append(
                {
                    "id": str(uuid.uuid4()),
                    "front": self._front_recall(theme, language),
                    "back": self._back_core(theme),
                    "topic": self._topic_from_theme(theme),
                    "difficulty": self._difficulty(theme),
                    "language": language,
                    "intent_type": theme.intent_type,
                }
            )
            if len(cards) >= limit:
                break

            cards.append(
                {
                    "id": str(uuid.uuid4()),
                    "front": self._front_apply(theme, language),
                    "back": self._back_application(theme),
                    "topic": self._topic_from_theme(theme),
                    "difficulty": "advanced",
                    "language": language,
                    "intent_type": theme.intent_type,
                }
            )
            if len(cards) >= limit:
                break

            cards.append(
                {
                    "id": str(uuid.uuid4()),
                    "front": self._front_misconception(theme, language),
                    "back": self._back_misconception(theme),
                    "topic": self._topic_from_theme(theme),
                    "difficulty": "advanced",
                    "language": language,
                    "intent_type": theme.intent_type,
                }
            )
            if len(cards) >= limit:
                break

        return cards[:limit]

    def generate_quiz(
        self,
        chat_messages: List[Dict[str, Any]],
        language: str = "english",
        num_questions: int = 6,
    ) -> Dict[str, Any]:
        """Generate challenging MCQs from user intent themes."""
        pairs = self._extract_qa_pairs(chat_messages)
        themes = self._extract_intent_themes(pairs)
        questions: List[Dict[str, Any]] = []

        for index, theme in enumerate(themes[:num_questions], start=1):
            correct = self._build_correct_option(theme)
            distractors = self._build_distractors(theme, correct)
            options = [correct] + distractors[:3]

            rnd = random.Random(theme.key)
            rnd.shuffle(options)

            questions.append(
                {
                    "id": str(index),
                    "type": "multiple_choice",
                    "question_text": self._quiz_prompt(theme, language),
                    "options": options,
                    "correct_answer": correct,
                    "explanation": self._quiz_explanation(theme),
                    "language": language,
                    "intent_type": theme.intent_type,
                    "difficulty": self._difficulty(theme),
                }
            )

        return {
            "id": f"chat_quiz_{uuid.uuid4().hex[:8]}",
            "topic": "Intent-Driven Chat Revision",
            "questions": questions,
            "time_limit_minutes": max(1, len(questions) * 2),
            "language": language,
        }

    def _extract_qa_pairs(self, chat_messages: Sequence[Dict[str, Any]]) -> List[Tuple[str, str]]:
        pairs: List[Tuple[str, str]] = []
        pending_question = ""

        for message in chat_messages:
            role = message.get("role")
            content = self._clean_text(message.get("content", ""), 4000)
            if not content:
                continue

            if role == "user":
                pending_question = content
                continue

            if role == "assistant" and pending_question:
                pairs.append((pending_question, content))
                pending_question = ""

        return pairs

    def _extract_intent_themes(self, pairs: Sequence[Tuple[str, str]]) -> List[IntentTheme]:
        themes: Dict[str, IntentTheme] = {}

        for question, answer in pairs:
            intent_type = self._classify_intent(question)
            keywords = self._extract_keywords(question)
            key = self._theme_key(intent_type, keywords, question)
            point = self._summarize_answer(answer)

            if key not in themes:
                themes[key] = IntentTheme(
                    key=key,
                    intent_type=intent_type,
                    objective=self._build_objective(intent_type, keywords),
                    representative_question=question,
                    keywords=keywords[:6],
                    answer_points=[],
                    support_count=0,
                )

            theme = themes[key]
            theme.support_count += 1
            if point:
                theme.answer_points.append(point)

            # Merge keywords to enrich theme signals.
            merged = theme.keywords + [kw for kw in keywords if kw not in theme.keywords]
            theme.keywords = merged[:8]

        ordered = sorted(
            themes.values(),
            key=lambda t: (t.support_count * 2 + len(t.keywords)),
            reverse=True,
        )
        return ordered

    def _classify_intent(self, question: str) -> str:
        q = question.lower()
        for intent_type, patterns in self.INTENT_PATTERNS.items():
            if any(re.search(pattern, q) for pattern in patterns):
                return intent_type
        return "explanation"

    def _extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        tokens = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", text.lower())
        words = [tok for tok in tokens if tok not in self.STOP_WORDS and len(tok) >= 3]

        ordered: List[str] = []
        seen = set()
        for word in words:
            if word not in seen:
                ordered.append(word)
                seen.add(word)
            if len(ordered) >= max_keywords:
                break
        return ordered

    def _theme_key(self, intent_type: str, keywords: List[str], question: str) -> str:
        if keywords:
            return f"{intent_type}:{'|'.join(keywords[:3])}"
        fallback = re.sub(r"[^a-z0-9]+", "_", question.lower()).strip("_")
        return f"{intent_type}:{fallback[:30] or 'general'}"

    def _build_objective(self, intent_type: str, keywords: List[str]) -> str:
        focus = " ".join(keywords[:3]) if keywords else "the relevant code behavior"
        templates = {
            "security": f"Master security behavior around {focus}",
            "flow": f"Trace end-to-end flow for {focus}",
            "architecture": f"Explain architectural responsibility for {focus}",
            "debugging": f"Diagnose failure causes around {focus}",
            "performance": f"Reason about performance impact of {focus}",
            "comparison": f"Evaluate trade-offs in {focus}",
            "explanation": f"Explain implementation details of {focus}",
        }
        return templates.get(intent_type, templates["explanation"])

    def _summarize_answer(self, answer: str) -> str:
        # Keep first 1-2 high-signal sentences.
        sentences = re.split(r"(?<=[.!?])\s+", answer.strip())
        compact = " ".join(s.strip() for s in sentences[:2] if s.strip())
        return self._clean_text(compact, 220)

    def _difficulty(self, theme: IntentTheme) -> str:
        if theme.support_count >= 2 or theme.intent_type in {"architecture", "performance", "comparison"}:
            return "advanced"
        if theme.intent_type in {"flow", "security", "debugging"}:
            return "intermediate"
        return "intermediate"

    def _topic_from_theme(self, theme: IntentTheme) -> str:
        if theme.keywords:
            return f"{theme.intent_type.title()}: {', '.join(theme.keywords[:2])}"
        return theme.intent_type.title()

    def _front_recall(self, theme: IntentTheme, language: str) -> str:
        if language == "hindi":
            return f"गहराई से समझाएं: {theme.objective} को इस कोडबेस में कैसे लागू किया गया है?"
        if language == "telugu":
            return f"లోతుగా వివరించండి: {theme.objective} ఈ కోడ్‌బేస్‌లో ఎలా అమలు అయింది?"
        return f"Deep explain: how is '{theme.objective}' implemented in this codebase?"

    def _front_apply(self, theme: IntentTheme, language: str) -> str:
        key = theme.keywords[0] if theme.keywords else "this module"
        if language == "hindi":
            return f"परिदृश्य: अगर {key} बदलता है, तो कौन सा flow पहले प्रभावित होगा और क्यों?"
        if language == "telugu":
            return f"సినారియో: {key} మారితే ముందుగా ఏ flow ప్రభావితం అవుతుంది? ఎందుకు?"
        return f"Scenario challenge: if '{key}' changes, which flow breaks first and why?"

    def _front_misconception(self, theme: IntentTheme, language: str) -> str:
        if language == "hindi":
            return f"गलतफहमी जांच: क्या {theme.objective.lower()} सिर्फ एक layer की जिम्मेदारी है?"
        if language == "telugu":
            return f"మిస్‌కాన్సెప్షన్ చెక్: {theme.objective.lower()} ఒకే layer బాధ్యతేనా?"
        return f"Misconception check: is '{theme.objective.lower()}' handled by only one layer?"

    def _back_core(self, theme: IntentTheme) -> str:
        summary = "; ".join(theme.answer_points[:2]) or "Derived from your prior chat explanation."
        keywords = ", ".join(theme.keywords[:5]) if theme.keywords else "core behavior"
        return (
            f"Core idea: {summary}\n\n"
            f"Intent focus: {theme.objective}\n"
            f"Key terms to revisit: {keywords}\n"
            f"Challenge prompt: explain this without using generic words like 'it works'."
        )

    def _back_application(self, theme: IntentTheme) -> str:
        summary = theme.answer_points[0] if theme.answer_points else "Use the chat explanation to map dependencies."
        primary = theme.keywords[0] if theme.keywords else "the entry point"
        secondary = theme.keywords[1] if len(theme.keywords) > 1 else "dependent modules"
        return (
            f"Likely impact path: changes in {primary} propagate to {secondary} and then to downstream handlers.\n\n"
            f"Reasoning anchor from chat: {summary}\n"
            f"Verification checklist: trace call chain, validate contracts, retest integration boundaries."
        )

    def _back_misconception(self, theme: IntentTheme) -> str:
        return (
            "False.\n\n"
            f"{theme.objective} usually spans multiple layers (entry, orchestration, validation, and side effects). "
            "Use cross-file references from chat explanations to verify each step."
        )

    def _build_correct_option(self, theme: IntentTheme) -> str:
        summary = theme.answer_points[0] if theme.answer_points else theme.objective
        return self._clean_text(
            f"Trace dependency boundaries and execution order first; {summary}",
            180,
        )

    def _build_distractors(self, theme: IntentTheme, correct: str) -> List[str]:
        key = theme.keywords[0] if theme.keywords else "this feature"
        distractors = [
            f"Only UI rendering matters for {key}; backend flow can be ignored.",
            f"{key} behavior is configured entirely by environment variables, not code paths.",
            f"Treat every module as independent; cross-file dependencies do not affect outcomes.",
            f"Focus only on syntax-level details of {key}; runtime flow is not relevant.",
        ]

        unique: List[str] = []
        for option in distractors:
            trimmed = self._clean_text(option, 180)
            if trimmed != correct and trimmed not in unique:
                unique.append(trimmed)
        return unique

    def _quiz_prompt(self, theme: IntentTheme, language: str) -> str:
        base = theme.objective
        if language == "hindi":
            return f"Scenario: {base} के लिए सबसे सही reasoning क्या है?"
        if language == "telugu":
            return f"Scenario: {base} కోసం సరైన reasoning ఏది?"
        return f"Scenario: for '{base}', what is the best reasoning path?"

    def _quiz_explanation(self, theme: IntentTheme) -> str:
        source = theme.answer_points[0] if theme.answer_points else "your previous assistant response"
        return (
            f"This checks intent-level understanding ({theme.intent_type}). "
            f"Correct reasoning comes from: {source}"
        )

    def _clean_text(self, text: str, max_len: int) -> str:
        sanitized = re.sub(r"\s+", " ", text or "").strip()
        if len(sanitized) <= max_len:
            return sanitized
        return sanitized[: max_len - 3].rstrip() + "..."
