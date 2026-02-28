"""
Learning Artifact Generator for creating flashcards, quizzes, and learning paths.

This module generates learning materials from multi-file analysis with complete
code traceability.
"""

import logging
import uuid
import random
import re
from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import datetime, timedelta
from models.intent_models import (
    MultiFileAnalysis,
    UserIntent,
    CodeEvidence,
    CodeFlashcard,
    CodeQuestion,
    LearningStep,
    LearningPath
)

logger = logging.getLogger(__name__)


@dataclass
class ConceptSeed:
    """Scored concept used to build high-quality learning artifacts."""

    name: str
    category: str
    description: str
    file_path: str
    line: int
    evidence: List[CodeEvidence]
    score: float = 0.0


class LearningArtifactGenerator:
    """Generates flashcards, quizzes, and learning paths from multi-file analysis."""
    
    def __init__(
        self,
        flashcard_manager,
        quiz_engine,
        langchain_orchestrator
    ):
        """
        Initialize with existing learning components.
        
        Args:
            flashcard_manager: FlashcardManager instance
            quiz_engine: QuizEngine instance
            langchain_orchestrator: LangChainOrchestrator for AI generation
        """
        self.flashcard_manager = flashcard_manager
        self.quiz_engine = quiz_engine
        self.orchestrator = langchain_orchestrator
    
    def generate_flashcards(
        self,
        multi_file_analysis: MultiFileAnalysis,
        intent: UserIntent,
        language: str = "english"
    ) -> List[CodeFlashcard]:
        """
        Generate flashcards from multi-file analysis.
        
        Args:
            multi_file_analysis: MultiFileAnalysis with code analysis
            intent: User's learning intent
            language: Output language (english, hindi, telugu)
            
        Returns:
            List of CodeFlashcard objects
        """
        flashcards = []

        try:
            concept_pool = self._build_concept_pool(multi_file_analysis, intent, max_items=10)
            logger.info(
                "Generating flashcards in %s using %s prioritized concepts",
                language,
                len(concept_pool),
            )

            if not concept_pool:
                return self.generate_basic_flashcards(multi_file_analysis)

            seen_fronts = set()
            for index, seed in enumerate(concept_pool):
                # Every concept gets at least recall + impact cards.
                styles = ["responsibility", "impact"]
                # High-value concepts also get reasoning card.
                if seed.score >= 5.5 or seed.category in {"architecture", "patterns"} or index < 3:
                    styles.append("reasoning")

                for style in styles:
                    front = self._flashcard_front(seed, style, language)
                    front_key = front.lower()
                    if front_key in seen_fronts:
                        continue
                    seen_fronts.add(front_key)

                    card = CodeFlashcard(
                        id=str(uuid.uuid4()),
                        front=front,
                        back=self._flashcard_back(seed, style),
                        topic=self._humanize_intent(intent.primary_intent),
                        difficulty=self._difficulty_from_seed(seed, style, intent.audience_level),
                        last_reviewed=None,
                        next_review=datetime.now() + timedelta(days=1),
                        mastered=False,
                        code_evidence=seed.evidence,
                        concept_category=seed.category,
                    )
                    flashcards.append(card)

                    if len(flashcards) >= 20:
                        break

                if len(flashcards) >= 20:
                    break

            logger.info("Generated %s flashcards in %s", len(flashcards), language)

        except Exception as e:
            logger.error(f"Flashcard generation failed: {e}")
            flashcards = self.generate_basic_flashcards(multi_file_analysis)

        return flashcards
    
    def generate_quiz(
        self,
        multi_file_analysis: MultiFileAnalysis,
        intent: UserIntent,
        num_questions: int = 10,
        language: str = "english"
    ) -> Dict[str, Any]:
        """
        Generate quiz from multi-file analysis.
        
        Args:
            multi_file_analysis: MultiFileAnalysis with code analysis
            intent: User's learning intent
            num_questions: Number of questions to generate
            language: Output language
            
        Returns:
            Quiz dictionary with questions
        """
        questions = []

        try:
            logger.info(f"Generating {num_questions} quiz questions in {language}")
            concept_pool = self._build_concept_pool(
                multi_file_analysis,
                intent,
                max_items=max(8, num_questions),
            )

            if not concept_pool:
                return self.generate_basic_quiz(multi_file_analysis)

            styles = ["responsibility", "impact", "reasoning", "debug"]
            for i in range(num_questions):
                seed = concept_pool[i % len(concept_pool)]
                style = styles[i % len(styles)]

                question_text = self._quiz_question_text(seed, style, language)
                correct_answer = self._quiz_correct_answer(seed, style, language)
                distractors = self._quiz_distractors(
                    seed,
                    style,
                    language,
                    concept_pool,
                    correct_answer,
                )
                options = self._unique_texts([correct_answer] + distractors)[:4]
                if len(options) < 4:
                    options = self._fill_options(seed, options, language)
                options = options[:4]

                rng = random.Random(f"{seed.name}:{style}:{i}")
                rng.shuffle(options)

                question = CodeQuestion(
                    id=str(i),
                    type="multiple_choice",
                    question_text=question_text,
                    options=options,
                    correct_answer=correct_answer,
                    explanation=self._quiz_explanation(seed, style, language),
                    code_evidence=seed.evidence,
                    question_category=style,
                )
                questions.append(question)

            quiz = {
                'id': f"quiz_{intent.primary_intent}_{uuid.uuid4().hex[:8]}",
                'topic': self._humanize_intent(intent.primary_intent),
                'questions': questions,
                'time_limit_minutes': max(5, len(questions) * 2),
            }

            logger.info(f"Generated quiz with {len(questions)} questions in {language}")

        except Exception as e:
            logger.error(f"Quiz generation failed: {e}")
            quiz = self.generate_basic_quiz(multi_file_analysis)

        return quiz

    def _build_concept_pool(
        self,
        multi_file_analysis: MultiFileAnalysis,
        intent: UserIntent,
        max_items: int = 10,
    ) -> List[ConceptSeed]:
        """Build prioritized concept pool from analysis + intent."""
        intent_keywords = self._intent_keywords(intent)
        by_name: Dict[str, ConceptSeed] = {}

        for raw in multi_file_analysis.key_concepts:
            if not isinstance(raw, dict):
                continue

            name = str(raw.get("name", "")).strip()
            if not name or name.lower() in {"unknown", "none"}:
                continue

            category = str(raw.get("category", "general")).lower()
            description = str(raw.get("description", "")).strip()
            file_path = str(raw.get("file", "")).strip()
            line = int(raw.get("line", 1) or 1)
            evidence = self._extract_concept_evidence(raw)
            if not evidence and file_path:
                evidence = [
                    CodeEvidence(
                        file_path=file_path,
                        line_start=max(1, line),
                        line_end=max(1, line + 5),
                        code_snippet="",
                        context_description=description or f"Concept {name}",
                    )
                ]
            if not evidence:
                continue

            score = self._score_concept(raw, intent_keywords, len(evidence))
            normalized_name = re.sub(r"[^a-z0-9_]+", "_", name.lower()).strip("_")
            if not normalized_name:
                continue

            candidate = ConceptSeed(
                name=name,
                category=category,
                description=description or f"{name} contributes to repository behavior.",
                file_path=file_path or evidence[0].file_path,
                line=line,
                evidence=evidence,
                score=score,
            )

            existing = by_name.get(normalized_name)
            if not existing or candidate.score > existing.score:
                by_name[normalized_name] = candidate

        ordered = sorted(by_name.values(), key=lambda item: item.score, reverse=True)
        return ordered[:max_items]

    def _extract_concept_evidence(self, concept: Dict[str, Any]) -> List[CodeEvidence]:
        evidence: List[CodeEvidence] = []
        evidence_items = concept.get("evidence", [])
        if isinstance(evidence_items, list):
            for ev in evidence_items:
                if not isinstance(ev, dict):
                    continue
                file_path = ev.get("file_path", concept.get("file", ""))
                line_start = int(ev.get("line_start", concept.get("line", 1)) or 1)
                line_end = int(ev.get("line_end", line_start + 5) or (line_start + 5))
                evidence.append(
                    CodeEvidence(
                        file_path=file_path,
                        line_start=max(1, line_start),
                        line_end=max(line_start, line_end),
                        code_snippet="",
                        context_description=str(ev.get("context", concept.get("description", ""))),
                    )
                )
        return evidence

    def _score_concept(self, concept: Dict[str, Any], intent_keywords: set[str], evidence_count: int) -> float:
        category = str(concept.get("category", "general")).lower()
        name = str(concept.get("name", "")).lower()
        description = str(concept.get("description", "")).lower()

        category_weight = {
            "architecture": 3.0,
            "patterns": 2.6,
            "classes": 2.2,
            "functions": 2.0,
            "data_flow": 2.8,
            "algorithms": 2.4,
            "general": 1.5,
        }.get(category, 1.4)

        relevance_hits = 0
        for keyword in intent_keywords:
            if keyword in name or keyword in description:
                relevance_hits += 1

        description_bonus = 0.7 if len(description) >= 30 else 0.3
        evidence_bonus = min(1.6, evidence_count * 0.4)
        relevance_bonus = min(2.4, relevance_hits * 0.8)

        return category_weight + description_bonus + evidence_bonus + relevance_bonus

    def _intent_keywords(self, intent: UserIntent) -> set[str]:
        tokens = []
        tokens.extend(re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", intent.primary_intent.lower()))
        for secondary in intent.secondary_intents:
            tokens.extend(re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", secondary.lower()))
        for tech in intent.technologies:
            tokens.extend(re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", tech.lower()))
        stop = {
            "learn",
            "understand",
            "about",
            "how",
            "what",
            "why",
            "code",
            "codebase",
            "repo",
            "repository",
            "and",
            "the",
        }
        return {tok for tok in tokens if len(tok) >= 3 and tok not in stop}

    def _flashcard_front(self, seed: ConceptSeed, style: str, language: str) -> str:
        if style == "responsibility":
            if language == "hindi":
                if seed.category == "functions":
                    return f"फ़ंक्शन '{seed.name}' का मुख्य उद्देश्य क्या है?"
                if seed.category == "classes":
                    return f"क्लास '{seed.name}' की मुख्य जिम्मेदारी क्या है?"
            elif language == "telugu":
                if seed.category == "functions":
                    return f"ఫంక్షన్ '{seed.name}' యొక్క ప్రధాన ఉద్దేశ్యం ఏమిటి?"
                if seed.category == "classes":
                    return f"క్లాస్ '{seed.name}' యొక్క ప్రధాన బాధ్యత ఏమిటి?"
            else:
                if seed.category == "functions":
                    return f"What does the function '{seed.name}' do in this repository?"
                if seed.category == "classes":
                    return f"What is the primary responsibility of class '{seed.name}'?"

        if language == "hindi":
            if style == "impact":
                return f"Scenario challenge: '{seed.name}' में बदलाव से सबसे पहले कौन सा behavior प्रभावित होगा?"
            if style == "reasoning":
                return f"Reasoning check: इस repo में '{seed.name}' को इसी तरीके से क्यों implement किया गया है?"
            return f"कोर समझ: '{seed.name}' की मुख्य जिम्मेदारी क्या है?"

        if language == "telugu":
            if style == "impact":
                return f"Scenario challenge: '{seed.name}' మార్చితే ముందుగా ఏ behavior ప్రభావితం అవుతుంది?"
            if style == "reasoning":
                return f"Reasoning check: ఈ repoలో '{seed.name}' ని ఈ విధంగా ఎందుకు అమలు చేశారు?"
            return f"మూల అవగాహన: '{seed.name}' యొక్క ప్రధాన బాధ్యత ఏమిటి?"

        if style == "impact":
            return f"Scenario challenge: if '{seed.name}' changes, which behavior breaks first?"
        if style == "reasoning":
            return f"Reasoning check: why is '{seed.name}' implemented this way in this repository?"
        return f"Core understanding: what is the primary responsibility of '{seed.name}'?"

    def _flashcard_back(self, seed: ConceptSeed, style: str) -> str:
        anchor = f"{seed.file_path}:{seed.evidence[0].line_start}" if seed.evidence else seed.file_path
        if style == "impact":
            return (
                f"Most likely first impact: behavior dependent on '{seed.name}' contracts in {seed.file_path}.\n\n"
                f"Why: {seed.description}\n"
                "Check: trace callers -> validate assumptions -> run integration path tests."
            )
        if style == "reasoning":
            return (
                f"Design rationale: {seed.description}\n\n"
                f"This concept is anchored at {anchor} and should be understood with dependency context."
            )
        return (
            f"Primary responsibility: {seed.description}\n\n"
            f"Code anchor: {anchor}\n"
            "Self-check: explain inputs, outputs, and downstream effects."
        )

    def _quiz_question_text(self, seed: ConceptSeed, style: str, language: str) -> str:
        if language == "hindi":
            prompts = {
                "responsibility": f"'{seed.name}' का सबसे सटीक technical उद्देश्य क्या है?",
                "impact": f"अगर '{seed.name}' टूट जाए, तो impact analysis का पहला सही कदम क्या होगा?",
                "reasoning": f"'{seed.name}' के implementation के पीछे सही reasoning कौन सी है?",
                "debug": f"'{seed.name}' से जुड़ी bug debug करने के लिए सबसे पहले कहाँ देखना चाहिए?",
            }
            return prompts.get(style, prompts["responsibility"])

        if language == "telugu":
            prompts = {
                "responsibility": f"'{seed.name}' యొక్క అత్యంత ఖచ్చితమైన technical ఉద్దేశ్యం ఏమిటి?",
                "impact": f"'{seed.name}' fail అయితే impact analysisలో సరైన first step ఏది?",
                "reasoning": f"'{seed.name}' implementation వెనుక సరైన reasoning ఏది?",
                "debug": f"'{seed.name}' సంబంధిత bug debug చేయాలంటే ముందుగా ఎక్కడ చూడాలి?",
            }
            return prompts.get(style, prompts["responsibility"])

        prompts = {
            "responsibility": f"What is the most accurate technical purpose of '{seed.name}' in this repository?",
            "impact": f"If '{seed.name}' fails, what is the most reliable first step in impact analysis?",
            "reasoning": f"Which reasoning best justifies the current implementation of '{seed.name}'?",
            "debug": f"Where should you inspect first when debugging a bug around '{seed.name}'?",
        }
        return prompts.get(style, prompts["responsibility"])

    def _quiz_correct_answer(self, seed: ConceptSeed, style: str, language: str) -> str:
        if style == "impact":
            if language == "hindi":
                return f"'{seed.name}' की dependency chain और callers trace करें, क्योंकि {seed.description}"
            if language == "telugu":
                return f"'{seed.name}' dependency chain మరియు callers trace చేయాలి, ఎందుకంటే {seed.description}"
            return f"Trace '{seed.name}' dependencies and callers first, because {seed.description}"

        if style == "debug":
            if language == "hindi":
                return f"'{seed.file_path}' में '{seed.name}' के code path से debug शुरू करें; वहीं primary contract define है।"
            if language == "telugu":
                return f"'{seed.file_path}' లో '{seed.name}' code path నుండి debug ప్రారంభించాలి; అక్కడే primary contract ఉంటుంది."
            return f"Start from '{seed.name}' code path in {seed.file_path}; its contract is the root signal."

        if style == "reasoning":
            if language == "hindi":
                return f"इस design का उद्देश्य है: {seed.description}"
            if language == "telugu":
                return f"ఈ design యొక్క ఉద్దేశ్యం: {seed.description}"
            return f"The design intent is: {seed.description}"

        if language == "hindi":
            return f"'{seed.name}' का मुख्य कार्य: {seed.description}"
        if language == "telugu":
            return f"'{seed.name}' ప్రధాన బాధ్యత: {seed.description}"
        return f"The primary responsibility of '{seed.name}' is: {seed.description}"

    def _quiz_distractors(
        self,
        seed: ConceptSeed,
        style: str,
        language: str,
        concept_pool: List[ConceptSeed],
        correct_answer: str,
    ) -> List[str]:
        distractors: List[str] = []

        # Plausible but wrong alternatives from other concepts.
        for other in concept_pool:
            if other.name == seed.name:
                continue
            if language == "hindi":
                distractors.append(f"'{seed.name}' का काम '{other.name}' जैसा है: {other.description}")
            elif language == "telugu":
                distractors.append(f"'{seed.name}' పని '{other.name}' లాంటిదే: {other.description}")
            else:
                distractors.append(f"'{seed.name}' has the same role as '{other.name}': {other.description}")
            if len(distractors) >= 2:
                break

        if language == "hindi":
            distractors.extend(
                [
                    f"'{seed.name}' सिर्फ naming convention है, runtime behavior पर असर नहीं डालता।",
                    f"'{seed.name}' को समझने के लिए dependency flow देखने की जरूरत नहीं है।",
                    f"'{seed.name}' केवल test files में उपयोग होता है, production flow में नहीं।",
                ]
            )
        elif language == "telugu":
            distractors.extend(
                [
                    f"'{seed.name}' కేవలం naming convention మాత్రమే; runtime behavior‌పై ప్రభావం లేదు.",
                    f"'{seed.name}' అర్థం చేసుకోవడానికి dependency flow అవసరం లేదు.",
                    f"'{seed.name}' test filesలో మాత్రమే ఉంటుంది; production flowలో లేదు.",
                ]
            )
        else:
            distractors.extend(
                [
                    f"'{seed.name}' is only a naming convention and does not affect runtime behavior.",
                    f"Understanding '{seed.name}' does not require checking dependency flow.",
                    f"'{seed.name}' is used only in tests and never in production execution paths.",
                ]
            )

        unique = self._unique_texts([item for item in distractors if item != correct_answer])
        return unique

    def _quiz_explanation(self, seed: ConceptSeed, style: str, language: str) -> str:
        anchor = f"{seed.file_path}:{seed.evidence[0].line_start}" if seed.evidence else seed.file_path
        if language == "hindi":
            return f"यह प्रश्न '{seed.name}' ({style}) समझने के लिए है। कोड एंकर: {anchor}. विवरण: {seed.description}"
        if language == "telugu":
            return f"ఈ ప్రశ్న '{seed.name}' ({style}) అవగాహన కోసం. కోడ్ యాంకర్: {anchor}. వివరణ: {seed.description}"
        return f"This tests '{seed.name}' ({style}) understanding. Code anchor: {anchor}. Context: {seed.description}"

    def _fill_options(self, seed: ConceptSeed, existing: List[str], language: str) -> List[str]:
        options = list(existing)
        if language == "hindi":
            fillers = [
                f"'{seed.name}' को debug करने के लिए code path छोड़कर सिर्फ UI text देखना चाहिए।",
                f"'{seed.name}' बदलने पर downstream modules पर कोई असर नहीं पड़ता।",
            ]
        elif language == "telugu":
            fillers = [
                f"'{seed.name}' debug చేయడానికి code path కాకుండా UI text మాత్రమే చూడాలి.",
                f"'{seed.name}' మార్చినా downstream modulesపై ప్రభావం ఉండదు.",
            ]
        else:
            fillers = [
                f"Debug '{seed.name}' by looking only at UI text, not code execution paths.",
                f"Changing '{seed.name}' never impacts downstream modules.",
            ]

        for item in fillers:
            if item not in options:
                options.append(item)
            if len(options) >= 4:
                break
        return options

    def _difficulty_from_seed(self, seed: ConceptSeed, style: str, default_level: str) -> str:
        if style in {"impact", "reasoning"}:
            return "advanced"
        if seed.score >= 6.0:
            return "advanced"
        if seed.score >= 4.3:
            return "intermediate"
        return default_level or "intermediate"

    def _humanize_intent(self, intent_text: str) -> str:
        return (intent_text or "Learning Goal").replace("_", " ").strip().title()

    def _unique_texts(self, values: List[str]) -> List[str]:
        unique: List[str] = []
        seen = set()
        for value in values:
            normalized = re.sub(r"\s+", " ", (value or "").strip())
            if not normalized:
                continue
            key = normalized.lower()
            if key in seen:
                continue
            seen.add(key)
            unique.append(normalized)
        return unique

    def _phase_titles(self, language: str) -> List[str]:
        if language == "hindi":
            return [
                "चरण 1: लक्ष्य और संरचना समझना",
                "चरण 2: मुख्य execution flow ट्रेस करना",
                "चरण 3: क्रिटिकल components में गहराई",
                "चरण 4: Debug और verification अभ्यास",
            ]
        if language == "telugu":
            return [
                "దశ 1: లక్ష్యం మరియు నిర్మాణం అర్థం చేసుకోవడం",
                "దశ 2: ప్రధాన execution flow ట్రేస్ చేయడం",
                "దశ 3: క్రిటికల్ components లో లోతుగా వెళ్లడం",
                "దశ 4: Debug మరియు verification ప్రాక్టీస్",
            ]
        return [
            "Step 1: Understand Goal and Structure",
            "Step 2: Trace Primary Execution Flow",
            "Step 3: Deep Dive Critical Components",
            "Step 4: Debug and Verify Behavior",
        ]

    def _phase_descriptions(self, language: str) -> List[str]:
        if language == "hindi":
            return [
                "लक्ष्य: {goal}. पहले इन अवधारणाओं को समझें: {concepts}.",
                "अब end-to-end flow ट्रेस करें और देखें कि {concepts} कैसे जुड़ते हैं।",
                "इन core हिस्सों में deep-dive करें: {concepts}. contracts और side-effects पर ध्यान दें।",
                "इन concepts पर debugging drills करें: {concepts}. बदलाव के impact को validate करें।",
            ]
        if language == "telugu":
            return [
                "లక్ష్యం: {goal}. ముందుగా ఈ concepts అర్థం చేసుకోండి: {concepts}.",
                "ఇప్పుడు end-to-end flow ట్రేస్ చేసి {concepts} ఎలా కలుస్తాయో చూడండి.",
                "ఈ core భాగాల్లో deep-dive చేయండి: {concepts}. contracts మరియు side-effects పై దృష్టి పెట్టండి.",
                "ఈ concepts పై debugging drills చేయండి: {concepts}. మార్పుల impact validate చేయండి.",
            ]
        return [
            "Goal: {goal}. Start with these concepts: {concepts}.",
            "Now trace end-to-end flow and map how {concepts} connect.",
            "Deep dive into these core parts: {concepts}. Focus on contracts and side-effects.",
            "Run debugging drills on {concepts} and validate impact of changes.",
        ]
    
    def generate_learning_path(
        self,
        multi_file_analysis: MultiFileAnalysis,
        intent: UserIntent,
        language: str = "english"
    ) -> LearningPath:
        """
        Generate ordered learning path.
        
        Args:
            multi_file_analysis: MultiFileAnalysis with code analysis
            intent: User's learning intent
            language: Output language
            
        Returns:
            LearningPath object with ordered steps
        """
        try:
            logger.info(f"Generating learning path in {language}")
            concept_pool = self._build_concept_pool(multi_file_analysis, intent, max_items=10)
            if not concept_pool:
                return self._create_empty_learning_path(intent)

            path_goal = self._humanize_intent(intent.primary_intent)
            steps: List[LearningStep] = []

            architecture = [c for c in concept_pool if c.category in {"architecture", "patterns"}]
            runtime = [c for c in concept_pool if c.category in {"functions", "classes"}]
            remaining = [c for c in concept_pool if c not in architecture and c not in runtime]

            phase_groups = []
            phase_groups.append(architecture[:2] or concept_pool[:2])
            phase_groups.append(runtime[:3] or concept_pool[2:5] or concept_pool[:2])
            phase_groups.append((runtime[3:5] + remaining[:2])[:3] or concept_pool[1:4] or concept_pool[:2])
            phase_groups.append((remaining[2:4] + concept_pool[:2])[:2] or concept_pool[:2])

            phase_titles = self._phase_titles(language)
            phase_desc_templates = self._phase_descriptions(language)

            for index, concepts in enumerate(phase_groups, start=1):
                if not concepts:
                    continue

                concepts_covered = [seed.name for seed in concepts]
                recommended_files = self._unique_texts([seed.file_path for seed in concepts if seed.file_path])
                evidence = []
                for seed in concepts:
                    evidence.extend(seed.evidence[:1])

                step_id = f"step_{index}"
                title = phase_titles[min(index - 1, len(phase_titles) - 1)]
                desc_template = phase_desc_templates[min(index - 1, len(phase_desc_templates) - 1)]
                description = desc_template.format(
                    goal=path_goal,
                    concepts=", ".join(concepts_covered[:3]),
                )
                estimated = 15 if index == 1 else 20
                if index == 3:
                    estimated = 25

                steps.append(
                    LearningStep(
                        step_id=step_id,
                        step_number=index,
                        title=title,
                        description=description,
                        estimated_time_minutes=estimated,
                        recommended_files=recommended_files,
                        concepts_covered=concepts_covered,
                        code_evidence=evidence,
                        prerequisites=[f"step_{index-1}"] if index > 1 else [],
                    )
                )

            total_time = sum(step.estimated_time_minutes for step in steps)

            if language == "hindi":
                path_title = f"उद्देश्य-केंद्रित सीखने का मार्ग: {path_goal}"
                path_desc = (
                    f"यह मार्ग आपके लक्ष्य '{path_goal}' के लिए बनाया गया है और "
                    "इसी रिपॉजिटरी के वास्तविक कोड प्रवाह पर आधारित है।"
                )
            elif language == "telugu":
                path_title = f"లక్ష్య-ఆధారిత లెర్నింగ్ పాత్: {path_goal}"
                path_desc = (
                    f"ఈ పాత్ మీ లక్ష్యం '{path_goal}' కోసం రూపొందించబడింది మరియు "
                    "ఈ repository లోని నిజమైన code flow పై ఆధారపడి ఉంటుంది."
                )
            else:
                path_title = f"Goal-Focused Learning Path: {path_goal}"
                path_desc = (
                    f"This path is tailored to your goal '{path_goal}' and grounded in "
                    "the actual implementation flow of this repository."
                )

            learning_path = LearningPath(
                path_id=f"path_{intent.primary_intent}_{uuid.uuid4().hex[:8]}",
                title=path_title,
                description=path_desc,
                total_steps=len(steps),
                estimated_total_time_minutes=total_time,
                steps=steps,
                difficulty_level=intent.audience_level,
            )

            logger.info(f"Generated learning path with {len(steps)} steps in {language}")
            return learning_path

        except Exception as e:
            logger.error(f"Learning path generation failed: {e}")
            return self._create_empty_learning_path(intent)
    
    def generate_concept_summary(
        self,
        multi_file_analysis: MultiFileAnalysis,
        intent: UserIntent,
        language: str = "english"
    ) -> Dict[str, Any]:
        """
        Generate concept summary organized by category.
        
        Args:
            multi_file_analysis: MultiFileAnalysis with code analysis
            intent: User's learning intent
            language: Output language
            
        Returns:
            Dictionary with categorized concepts
        """
        try:
            concept_pool = self._build_concept_pool(multi_file_analysis, intent, max_items=12)
            summary = {
                'total_concepts': len(multi_file_analysis.key_concepts),
                'categories': {},
                'top_concepts': [],
                'language': language,
                'summary': "",
                'learning_focus': [self._humanize_intent(intent.primary_intent)],
            }

            for concept in multi_file_analysis.key_concepts:
                category = concept.get('category', 'general')
                summary['categories'].setdefault(category, []).append({
                    'name': concept.get('name', 'Unknown'),
                    'description': concept.get('description', ''),
                    'file': concept.get('file', ''),
                    'line': concept.get('line', 0),
                })

            summary['top_concepts'] = [
                {
                    'name': seed.name,
                    'category': seed.category,
                    'description': seed.description,
                    'file': seed.file_path,
                    'score': round(seed.score, 2),
                }
                for seed in concept_pool[:5]
            ]

            top_names = ", ".join(seed.name for seed in concept_pool[:3]) if concept_pool else "core modules"
            total_files = len(multi_file_analysis.analyzed_files)
            if language == "hindi":
                summary['summary'] = (
                    f"{total_files} files में विश्लेषण पूरा हुआ। फोकस concepts: {top_names}."
                )
            elif language == "telugu":
                summary['summary'] = (
                    f"{total_files} files విశ్లేషించబడ్డాయి. ఫోకస్ concepts: {top_names}."
                )
            else:
                summary['summary'] = (
                    f"Analysis covered {total_files} files. Primary learning focus: {top_names}."
                )

            logger.info(f"Generated concept summary with {len(summary['categories'])} categories in {language}")
            return summary

        except Exception as e:
            logger.error(f"Concept summary generation failed: {e}")
            return {'total_concepts': 0, 'categories': {}, 'top_concepts': [], 'language': language, 'summary': ''}
    
    def _extract_code_evidence(
        self,
        file_path: str,
        line_start: int,
        line_end: int,
        context: str
    ) -> CodeEvidence:
        """
        Extract code evidence for traceability.
        
        Args:
            file_path: Path to code file
            line_start: Starting line number
            line_end: Ending line number
            context: Context description
            
        Returns:
            CodeEvidence object
        """
        return CodeEvidence(
            file_path=file_path,
            line_start=line_start,
            line_end=line_end,
            code_snippet="",  # Will be filled by traceability manager
            context_description=context
        )
    
    def generate_basic_flashcards(
        self,
        multi_file_analysis: MultiFileAnalysis
    ) -> List[CodeFlashcard]:
        """
        Generate basic flashcards as fallback when AI fails.
        
        Args:
            multi_file_analysis: MultiFileAnalysis
            
        Returns:
            List of basic flashcards
        """
        flashcards = []
        
        try:
            # Generate from file analyses
            for file_path, analysis in list(multi_file_analysis.file_analyses.items())[:5]:
                if hasattr(analysis, 'structure'):
                    # Create flashcard from first function
                    if hasattr(analysis.structure, 'functions') and analysis.structure.functions:
                        func = analysis.structure.functions[0]
                        
                        evidence = CodeEvidence(
                            file_path=file_path,
                            line_start=func.line_number,
                            line_end=func.line_number + 5,
                            code_snippet="",
                            context_description=f"Function {func.name}"
                        )
                        
                        flashcard = CodeFlashcard(
                            id=str(uuid.uuid4()),
                            front=f"What does {func.name} do?",
                            back=func.docstring or f"Function with parameters: {', '.join(func.parameters)}",
                            topic="Code Structure",
                            difficulty="intermediate",
                            code_evidence=[evidence],
                            concept_category="functions"
                        )
                        flashcards.append(flashcard)
        
        except Exception as e:
            logger.error(f"Basic flashcard generation failed: {e}")
        
        return flashcards
    
    def generate_basic_quiz(
        self,
        multi_file_analysis: MultiFileAnalysis
    ) -> Dict[str, Any]:
        """
        Generate basic quiz as fallback when AI fails.
        
        Args:
            multi_file_analysis: MultiFileAnalysis
            
        Returns:
            Basic quiz dictionary
        """
        questions = []
        
        try:
            # Generate simple questions from analysis
            for i, (file_path, analysis) in enumerate(list(multi_file_analysis.file_analyses.items())[:5]):
                if hasattr(analysis, 'structure') and hasattr(analysis.structure, 'functions'):
                    if analysis.structure.functions:
                        func = analysis.structure.functions[0]
                        
                        evidence = CodeEvidence(
                            file_path=file_path,
                            line_start=func.line_number,
                            line_end=func.line_number + 5,
                            code_snippet="",
                            context_description=f"Function {func.name}"
                        )
                        
                        question = CodeQuestion(
                            id=str(i),
                            type="multiple_choice",
                            question_text=f"What is the purpose of {func.name}?",
                            options=[
                                func.docstring or "Primary function",
                                "Helper function",
                                "Utility function",
                                "Configuration function"
                            ],
                            correct_answer=func.docstring or "Primary function",
                            explanation=f"Based on the code structure",
                            code_evidence=[evidence],
                            question_category="functions"
                        )
                        questions.append(question)
        
        except Exception as e:
            logger.error(f"Basic quiz generation failed: {e}")
        
        return {
            'id': f"basic_quiz_{uuid.uuid4().hex[:8]}",
            'topic': "Code Understanding",
            'questions': questions,
            'time_limit_minutes': len(questions) * 2
        }
    
    def _create_empty_learning_path(self, intent: UserIntent) -> LearningPath:
        """Create empty learning path for error cases."""
        return LearningPath(
            path_id=f"empty_path_{uuid.uuid4().hex[:8]}",
            title="Learning Path",
            description="No learning path available",
            total_steps=0,
            estimated_total_time_minutes=0,
            steps=[],
            difficulty_level=intent.audience_level
        )
