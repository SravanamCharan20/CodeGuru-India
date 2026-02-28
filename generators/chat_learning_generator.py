"""Generate challenging flashcards and quizzes from chat intent themes."""

from __future__ import annotations

from dataclasses import dataclass, field
import random
import re
import uuid
from typing import Any, Dict, List, Sequence


@dataclass
class ChatExchange:
    """A paired user question and assistant response."""

    question: str
    answer: str
    question_metadata: Dict[str, Any] = field(default_factory=dict)
    answer_metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IntentTheme:
    """Intent cluster extracted from user chat questions."""

    key: str
    concept: str
    intent_type: str
    objective: str
    representative_question: str
    keywords: List[str] = field(default_factory=list)
    answer_points: List[str] = field(default_factory=list)
    code_references: List[str] = field(default_factory=list)
    intent_counts: Dict[str, int] = field(default_factory=dict)
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
        "give",
        "have",
        "need",
        "want",
        "use",
    }

    GENERIC_CONCEPTS = {
        "what",
        "why",
        "how",
        "tell",
        "code",
        "codebase",
        "repo",
        "repository",
        "project",
        "question",
        "answer",
        "feature",
        "thing",
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
            r"\brouting\b",
        ],
        "architecture": [
            r"\barchitecture\b",
            r"\bdesign\b",
            r"\bmodule\b",
            r"\blayer\b",
            r"\bpattern\b",
            r"\bcomponent\b",
            r"\bstructure\b",
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
        exchanges = self._extract_qa_pairs(chat_messages)
        themes = self._extract_intent_themes(exchanges)
        cards: List[Dict[str, Any]] = []
        seen_fronts = set()

        if not themes:
            return cards

        card_builders = [
            ("core", self._front_recall, self._back_core),
            ("reasoning", self._front_reasoning, self._back_reasoning),
            ("application", self._front_apply, self._back_application),
            ("misconception", self._front_misconception, self._back_misconception),
        ]

        for theme in themes:
            for challenge_type, front_builder, back_builder in card_builders:
                front = self._clean_text(front_builder(theme, language), 240)
                front_key = front.lower()
                if front_key in seen_fronts:
                    continue

                seen_fronts.add(front_key)
                cards.append(
                    {
                        "id": str(uuid.uuid4()),
                        "front": front,
                        "back": self._clean_text(back_builder(theme), 900),
                        "topic": self._topic_from_theme(theme),
                        "difficulty": self._difficulty(theme, challenge_type),
                        "language": language,
                        "intent_type": theme.intent_type,
                        "concept": theme.concept,
                        "objective": theme.objective,
                        "challenge_type": challenge_type,
                    }
                )

                if len(cards) >= limit:
                    return cards[:limit]

        return cards[:limit]

    def generate_quiz(
        self,
        chat_messages: List[Dict[str, Any]],
        language: str = "english",
        num_questions: int = 6,
    ) -> Dict[str, Any]:
        """Generate challenging MCQs from user intent themes."""
        exchanges = self._extract_qa_pairs(chat_messages)
        themes = self._extract_intent_themes(exchanges)
        questions: List[Dict[str, Any]] = []

        for index, theme in enumerate(themes[:num_questions], start=1):
            correct = self._build_correct_option(theme)
            distractors = self._build_distractors(theme, correct, index)
            options = self._ensure_unique_options([correct] + distractors)[:4]
            if len(options) < 4:
                options += self._fill_quiz_options(theme, options, target=4)
            options = options[:4]

            rnd = random.Random(f"{theme.key}:{index}")
            rnd.shuffle(options)

            questions.append(
                {
                    "id": str(index),
                    "type": "multiple_choice",
                    "question_text": self._quiz_prompt(theme, language, index),
                    "options": options,
                    "correct_answer": correct,
                    "explanation": self._quiz_explanation(theme),
                    "language": language,
                    "intent_type": theme.intent_type,
                    "difficulty": self._difficulty(theme, "reasoning"),
                    "concept": theme.concept,
                    "objective": theme.objective,
                }
            )

        return {
            "id": f"chat_quiz_{uuid.uuid4().hex[:8]}",
            "topic": "Intent-Driven Chat Revision",
            "questions": questions,
            "time_limit_minutes": max(2, len(questions) * 2),
            "language": language,
        }

    def _extract_qa_pairs(self, chat_messages: Sequence[Dict[str, Any]]) -> List[ChatExchange]:
        pairs: List[ChatExchange] = []
        pending_question = ""
        pending_metadata: Dict[str, Any] = {}

        for message in chat_messages:
            role = message.get("role")
            content = self._clean_text(message.get("content", ""), 7000)
            metadata = message.get("metadata", {}) if isinstance(message.get("metadata"), dict) else {}
            if not content:
                continue

            if role == "user":
                pending_question = content
                pending_metadata = metadata
                continue

            if role == "assistant" and pending_question:
                pairs.append(
                    ChatExchange(
                        question=pending_question,
                        answer=content,
                        question_metadata=pending_metadata,
                        answer_metadata=metadata,
                    )
                )
                pending_question = ""
                pending_metadata = {}

        return pairs

    def _extract_intent_themes(self, pairs: Sequence[ChatExchange]) -> List[IntentTheme]:
        themes: Dict[str, IntentTheme] = {}

        for pair in pairs:
            intent_type = self._classify_intent(pair.question)
            question_keywords = self._extract_keywords(pair.question, max_keywords=10)
            answer_keywords = self._extract_keywords(pair.answer, max_keywords=8)
            ref_keywords, formatted_refs = self._extract_reference_signals(pair.answer_metadata)

            concept = self._derive_concept(pair.question, question_keywords, ref_keywords)
            if not concept:
                concept = self._derive_concept(pair.answer, answer_keywords, ref_keywords)
            if not concept or self._is_generic_concept(concept):
                continue

            key = self._theme_key(concept)
            point = self._summarize_answer(pair.answer)

            if key not in themes:
                themes[key] = IntentTheme(
                    key=key,
                    concept=concept,
                    intent_type=intent_type,
                    objective="",
                    representative_question=pair.question,
                    keywords=[],
                    answer_points=[],
                    code_references=[],
                    intent_counts={},
                    support_count=0,
                )

            theme = themes[key]
            theme.support_count += 1
            theme.intent_counts[intent_type] = theme.intent_counts.get(intent_type, 0) + 1
            theme.intent_type = self._dominant_intent(theme.intent_counts)

            theme.keywords = self._merge_unique(
                theme.keywords,
                question_keywords + answer_keywords + ref_keywords,
                limit=12,
            )

            if point:
                theme.answer_points = self._merge_unique(theme.answer_points, [point], limit=4)

            if formatted_refs:
                theme.code_references = self._merge_unique(theme.code_references, formatted_refs, limit=4)

            theme.objective = self._build_objective(theme)

        # Fallback: keep at least one theme when chat has a valid QA pair.
        if not themes and pairs:
            last_pair = pairs[-1]
            fallback_keywords = self._extract_keywords(last_pair.question)
            fallback_concept = self._derive_concept(last_pair.question, fallback_keywords, [])
            if fallback_concept:
                fallback = IntentTheme(
                    key=self._theme_key(fallback_concept),
                    concept=fallback_concept,
                    intent_type=self._classify_intent(last_pair.question),
                    objective=f"Explain how {fallback_concept} works in this repository.",
                    representative_question=last_pair.question,
                    keywords=fallback_keywords[:8],
                    answer_points=[self._summarize_answer(last_pair.answer)],
                    code_references=[],
                    intent_counts={self._classify_intent(last_pair.question): 1},
                    support_count=1,
                )
                themes[fallback.key] = fallback

        ordered = sorted(
            themes.values(),
            key=self._theme_score,
            reverse=True,
        )
        return ordered

    def _classify_intent(self, question: str) -> str:
        q = question.lower().strip()
        if re.match(r"^why\b", q):
            return "why"
        if re.match(r"^how\b", q):
            return "how"
        if re.match(r"^what\b", q):
            return "what"

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

    def _extract_reference_signals(self, metadata: Dict[str, Any]) -> tuple[List[str], List[str]]:
        refs = metadata.get("code_references") if isinstance(metadata, dict) else []
        if not isinstance(refs, list):
            return [], []

        keywords: List[str] = []
        formatted_refs: List[str] = []

        for ref in refs[:6]:
            if not isinstance(ref, dict):
                continue

            file_path = ref.get("file", "")
            lines = ref.get("lines", "")
            if file_path:
                formatted = f"{file_path}:{lines}" if lines else file_path
                formatted_refs.append(formatted)

                basename = file_path.split("/")[-1]
                stem = basename.split(".")[0]
                stem_parts = re.split(r"[_\W]+", stem.lower())
                for part in stem_parts:
                    if part and part not in self.STOP_WORDS and len(part) >= 3:
                        keywords.append(part)

        return self._merge_unique([], keywords, limit=8), self._merge_unique([], formatted_refs, limit=4)

    def _derive_concept(self, text: str, keywords: List[str], ref_keywords: List[str]) -> str:
        quoted = re.findall(r"['\"]([a-zA-Z_][a-zA-Z0-9_\-\s]{1,80})['\"]", text)
        for candidate in quoted:
            concept = self._normalize_concept(candidate)
            if concept:
                return concept

        patterns = [
            r"(?:what is|what's|how does|how do|why do we use|why should we use|why use|explain|describe)\s+([a-zA-Z_][a-zA-Z0-9_\-\s]{2,100})",
            r"(?:about|for)\s+([a-zA-Z_][a-zA-Z0-9_\-\s]{2,80})",
        ]
        lowered = text.lower()
        for pattern in patterns:
            match = re.search(pattern, lowered)
            if not match:
                continue
            concept = self._normalize_concept(match.group(1))
            if concept:
                return concept

        for source in (keywords, ref_keywords):
            for token in source:
                concept = self._normalize_concept(token)
                if concept:
                    return concept

        return ""

    def _normalize_concept(self, concept: str) -> str:
        clean = (concept or "").lower().strip()
        if not clean:
            return ""

        clean = re.sub(r"\s+", " ", clean)
        for splitter in [" in this repo", " in the repo", " in repo", " and why", " and how", " and what"]:
            if splitter in clean:
                clean = clean.split(splitter, 1)[0].strip()

        clean = re.sub(r"[^a-z0-9_\-\s]", " ", clean)
        tokens = [tok for tok in clean.split() if tok and tok not in self.STOP_WORDS and tok not in self.GENERIC_CONCEPTS]
        if not tokens:
            return ""

        compact = " ".join(tokens[:3])
        if self._is_generic_concept(compact):
            return ""
        return compact

    def _is_generic_concept(self, concept: str) -> bool:
        lowered = concept.lower().strip()
        if not lowered:
            return True
        if lowered in self.GENERIC_CONCEPTS:
            return True
        if len(lowered) <= 2:
            return True
        return all(token in self.STOP_WORDS or token in self.GENERIC_CONCEPTS for token in lowered.split())

    def _theme_key(self, concept: str) -> str:
        normalized = re.sub(r"[^a-z0-9]+", "_", concept.lower()).strip("_")
        return normalized[:50] or "general_concept"

    def _build_objective(self, theme: IntentTheme) -> str:
        concept = theme.concept
        dominant = theme.intent_type

        if dominant == "why":
            return f"Explain why '{concept}' is used and what trade-offs it solves."
        if dominant == "how":
            return f"Trace how '{concept}' works end-to-end across the codebase."
        if dominant == "comparison":
            return f"Compare alternatives around '{concept}' and justify the chosen implementation."
        if dominant == "debugging":
            return f"Diagnose failure points and debugging strategy for '{concept}'."
        if dominant == "performance":
            return f"Reason about performance impact of '{concept}' and optimization boundaries."
        if dominant == "security":
            return f"Understand security responsibilities and validation flow in '{concept}'."
        if dominant == "flow":
            return f"Map request/data flow involving '{concept}' from entry to side-effects."
        if dominant == "architecture":
            return f"Explain architectural role and dependencies of '{concept}'."
        return f"Build a precise mental model of '{concept}' in this repository."

    def _summarize_answer(self, answer: str) -> str:
        # Keep first 1-2 high-signal sentences.
        sentences = re.split(r"(?<=[.!?])\s+", answer.strip())
        compact = " ".join(s.strip() for s in sentences if s.strip() and len(s.strip()) > 15)
        compact = compact if compact else answer.strip()
        return self._clean_text(compact, 220)

    def _difficulty(self, theme: IntentTheme, challenge_type: str = "core") -> str:
        advanced_intents = {"architecture", "performance", "comparison", "debugging", "security"}
        if challenge_type in {"reasoning", "application"}:
            return "advanced"
        if theme.support_count >= 2:
            return "advanced"
        if theme.intent_type in advanced_intents:
            return "advanced"
        return "intermediate"

    def _topic_from_theme(self, theme: IntentTheme) -> str:
        return f"{theme.concept.title()} ({theme.intent_type})"

    def _front_recall(self, theme: IntentTheme, language: str) -> str:
        if language == "hindi":
            return f"कोर समझ: इस repo में '{theme.concept}' की जिम्मेदारी क्या है?"
        if language == "telugu":
            return f"ప్రధాన అర్థం: ఈ repoలో '{theme.concept}' బాధ్యత ఏమిటి?"
        return f"Core understanding: what responsibility does '{theme.concept}' have in this repository?"

    def _front_reasoning(self, theme: IntentTheme, language: str) -> str:
        if language == "hindi":
            return f"रीज़निंग चेक: '{theme.concept}' को ऐसे design करने की मुख्य वजह क्या है?"
        if language == "telugu":
            return f"రీజనింగ్ చెక్: '{theme.concept}' ఇలా design చేయడానికి ప్రధాన కారణం ఏమిటి?"
        return f"Reasoning check: why is '{theme.concept}' implemented this way in this codebase?"

    def _front_apply(self, theme: IntentTheme, language: str) -> str:
        if language == "hindi":
            return f"Scenario challenge: अगर '{theme.concept}' बदलें, तो कौन सा behavior पहले टूटेगा और क्यों?"
        if language == "telugu":
            return f"Scenario challenge: '{theme.concept}' మార్చితే ముందుగా ఏ behavior break అవుతుంది? ఎందుకు?"
        return f"Scenario challenge: if '{theme.concept}' changes, what breaks first and why?"

    def _front_misconception(self, theme: IntentTheme, language: str) -> str:
        if language == "hindi":
            return f"Misconception check: क्या '{theme.concept}' सिर्फ एक file तक सीमित है?"
        if language == "telugu":
            return f"Misconception check: '{theme.concept}' ఒకే file లో మాత్రమే పరిమితమైందా?"
        return f"Misconception check: is '{theme.concept}' isolated to a single file?"

    def _back_core(self, theme: IntentTheme) -> str:
        summary = "; ".join(theme.answer_points[:2]) or "Based on your chat discussion."
        refs = ", ".join(theme.code_references[:3]) if theme.code_references else "Use referenced files from the chat response."
        return (
            f"Core idea: {summary}\n\n"
            f"Learning objective: {theme.objective}\n"
            f"Code anchors: {refs}\n"
            "Self-check: explain this in your own words without generic filler."
        )

    def _back_reasoning(self, theme: IntentTheme) -> str:
        primary = theme.answer_points[0] if theme.answer_points else "Use dependency direction and contracts as reasoning anchors."
        return (
            f"Best reasoning path: {primary}\n\n"
            f"Why this matters: '{theme.concept}' often coordinates behavior across modules, not just one line of code.\n"
            "Verification: follow call path, validate assumptions, and confirm side-effects."
        )

    def _back_application(self, theme: IntentTheme) -> str:
        key_terms = ", ".join(theme.keywords[:4]) if theme.keywords else theme.concept
        return (
            f"Likely impact area: start from '{theme.concept}', then trace adjacent modules linked to {key_terms}.\n\n"
            "Execution checklist: identify entry point -> inspect contracts -> run affected flow-level tests."
        )

    def _back_misconception(self, theme: IntentTheme) -> str:
        refs = ", ".join(theme.code_references[:2]) if theme.code_references else "cross-file chat references"
        return (
            "No. In most codebases this concept is cross-cutting.\n\n"
            f"For '{theme.concept}', verify upstream and downstream dependencies using: {refs}."
        )

    def _build_correct_option(self, theme: IntentTheme) -> str:
        summary = theme.answer_points[0] if theme.answer_points else theme.objective
        text = f"Start from '{theme.concept}' responsibilities and dependency flow; {summary}"
        return self._clean_text(text, 180)

    def _build_distractors(self, theme: IntentTheme, correct: str, seed_index: int) -> List[str]:
        concept = theme.concept
        base = [
            f"'{concept}' is only naming/style and has no runtime effect.",
            f"'{concept}' works in a single isolated file, so cross-file flow is irrelevant.",
            f"'{concept}' is only for tests/build scripts and not production behavior.",
            f"'{concept}' removes the need for validation, contracts, and error handling.",
        ]

        if theme.intent_type in {"performance", "flow"}:
            base.append(f"Performance and request path around '{concept}' can be inferred without reading call order.")
        if theme.intent_type in {"security", "debugging"}:
            base.append(f"Debugging '{concept}' should start from UI labels, not execution traces.")

        unique: List[str] = []
        for option in base:
            trimmed = self._clean_text(option, 180)
            if trimmed != correct and trimmed not in unique:
                unique.append(trimmed)

        rnd = random.Random(f"{theme.key}:{seed_index}:distractors")
        rnd.shuffle(unique)
        return unique

    def _fill_quiz_options(self, theme: IntentTheme, options: List[str], target: int) -> List[str]:
        fill = [
            f"Treat '{theme.concept}' as documentation-only and skip runtime validation.",
            f"Analyze '{theme.concept}' by syntax alone; no need to inspect flow or dependencies.",
            f"Assume '{theme.concept}' has no integration boundaries with other modules.",
        ]
        additions: List[str] = []
        for value in fill:
            trimmed = self._clean_text(value, 180)
            if trimmed not in options and trimmed not in additions:
                additions.append(trimmed)
            if len(options) + len(additions) >= target:
                break
        return additions

    def _quiz_prompt(self, theme: IntentTheme, language: str, question_index: int) -> str:
        variant = question_index % 3
        if language == "hindi":
            prompts = [
                f"Scenario: '{theme.concept}' की role समझाने के लिए सबसे सही reasoning कौन सी है?",
                f"Scenario: अगर '{theme.concept}' में change हो, तो impact analysis का सही पहला कदम क्या होगा?",
                f"Scenario: '{theme.concept}' के बारे में कौन सा कथन सबसे तकनीकी रूप से सही है?",
            ]
            return prompts[variant]

        if language == "telugu":
            prompts = [
                f"Scenario: '{theme.concept}' పాత్రను అర్థం చేసుకోవడానికి సరైన reasoning ఏది?",
                f"Scenario: '{theme.concept}' మారితే impact analysis లో సరైన first step ఏది?",
                f"Scenario: '{theme.concept}' గురించి ఏ statement technical గా సరైనది?",
            ]
            return prompts[variant]

        prompts = [
            f"Scenario: which reasoning best explains the role of '{theme.concept}' in this repository?",
            f"Scenario: if '{theme.concept}' changes, what is the most reliable first step for impact analysis?",
            f"Scenario: which statement about '{theme.concept}' is technically correct for this codebase?",
        ]
        return prompts[variant]

    def _quiz_explanation(self, theme: IntentTheme) -> str:
        source = theme.answer_points[0] if theme.answer_points else "the validated assistant explanation from your chat"
        refs = ", ".join(theme.code_references[:2]) if theme.code_references else "chat code references"
        return (
            f"This question tests concept-level reasoning for '{theme.concept}' ({theme.intent_type}). "
            f"Use this anchor: {source}. Verify against: {refs}."
        )

    def _theme_score(self, theme: IntentTheme) -> float:
        return (
            theme.support_count * 3.0
            + len(theme.intent_counts) * 2.0
            + len(theme.code_references) * 1.5
            + len(theme.answer_points)
            + len(theme.keywords) * 0.2
        )

    def _dominant_intent(self, counts: Dict[str, int]) -> str:
        if not counts:
            return "explanation"
        return max(counts, key=lambda key: counts[key])

    def _merge_unique(self, base: List[str], additions: Sequence[str], limit: int) -> List[str]:
        merged = list(base)
        seen = {item.lower() for item in merged if isinstance(item, str)}
        for item in additions:
            if not isinstance(item, str):
                continue
            clean = item.strip()
            if not clean:
                continue
            lowered = clean.lower()
            if lowered in seen:
                continue
            merged.append(clean)
            seen.add(lowered)
            if len(merged) >= limit:
                break
        return merged

    def _ensure_unique_options(self, options: Sequence[str]) -> List[str]:
        unique: List[str] = []
        seen = set()
        for option in options:
            clean = self._clean_text(option, 180)
            key = clean.lower()
            if not clean or key in seen:
                continue
            unique.append(clean)
            seen.add(key)
        return unique

    def _clean_text(self, text: str, max_len: int) -> str:
        sanitized = re.sub(r"\s+", " ", text or "").strip()
        if len(sanitized) <= max_len:
            return sanitized
        return sanitized[: max_len - 3].rstrip() + "..."
