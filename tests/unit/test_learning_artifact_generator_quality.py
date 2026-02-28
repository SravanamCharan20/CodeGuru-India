"""Quality tests for repository learning artifact generation."""

from unittest.mock import Mock

from generators.learning_artifact_generator import LearningArtifactGenerator
from models.intent_models import MultiFileAnalysis, UserIntent, IntentScope


def _sample_analysis() -> MultiFileAnalysis:
    return MultiFileAnalysis(
        analyzed_files=["src/components/Shimmer.jsx", "src/pages/Home.jsx"],
        file_analyses={},
        relationships=[],
        dependency_graph={},
        data_flows=[],
        execution_paths=[],
        cross_file_patterns=[],
        key_concepts=[
            {
                "name": "Shimmer",
                "category": "functions",
                "description": "Renders a skeleton placeholder while API data is loading.",
                "file": "src/components/Shimmer.jsx",
                "line": 4,
                "evidence": [
                    {
                        "file_path": "src/components/Shimmer.jsx",
                        "line_start": 4,
                        "line_end": 28,
                        "context": "Shimmer component rendering logic",
                    }
                ],
            },
            {
                "name": "fetchHomeFeed",
                "category": "functions",
                "description": "Fetches restaurant cards and toggles loading state.",
                "file": "src/pages/Home.jsx",
                "line": 16,
                "evidence": [
                    {
                        "file_path": "src/pages/Home.jsx",
                        "line_start": 16,
                        "line_end": 45,
                        "context": "Home page data fetch logic",
                    }
                ],
            },
            {
                "name": "UI Data Flow",
                "category": "architecture",
                "description": "Data flows from fetch call to state update and then conditional UI rendering.",
                "file": "src/pages/Home.jsx",
                "line": 10,
                "evidence": [
                    {
                        "file_path": "src/pages/Home.jsx",
                        "line_start": 10,
                        "line_end": 60,
                        "context": "Flow from loading state to rendered list",
                    }
                ],
            },
        ],
    )


def _sample_intent() -> UserIntent:
    return UserIntent(
        primary_intent="understand_loading_and_render_flow",
        secondary_intents=["debug slow ui"],
        scope=IntentScope(scope_type="entire_repo"),
        audience_level="intermediate",
        technologies=["react"],
        confidence_score=0.95,
    )


def test_flashcards_are_scenario_or_reasoning_driven_and_grounded():
    generator = LearningArtifactGenerator(
        flashcard_manager=Mock(),
        quiz_engine=Mock(),
        langchain_orchestrator=Mock(),
    )

    flashcards = generator.generate_flashcards(_sample_analysis(), _sample_intent(), language="english")

    assert flashcards
    assert any("Scenario challenge" in card.front for card in flashcards)
    assert any("Reasoning check" in card.front for card in flashcards)
    assert any(card.difficulty == "advanced" for card in flashcards)
    assert all(card.code_evidence for card in flashcards)


def test_quiz_is_challenging_and_not_option_duplicate():
    generator = LearningArtifactGenerator(
        flashcard_manager=Mock(),
        quiz_engine=Mock(),
        langchain_orchestrator=Mock(),
    )

    quiz = generator.generate_quiz(
        _sample_analysis(),
        _sample_intent(),
        num_questions=6,
        language="english",
    )

    questions = quiz["questions"]
    assert len(questions) == 6

    for question in questions:
        assert len(question.options) == 4
        assert len(set(question.options)) == 4
        assert question.correct_answer in question.options
        assert question.question_category in {"responsibility", "impact", "reasoning", "debug"}


def test_learning_path_is_goal_focused_and_grounded_in_repo_concepts():
    generator = LearningArtifactGenerator(
        flashcard_manager=Mock(),
        quiz_engine=Mock(),
        langchain_orchestrator=Mock(),
    )

    learning_path = generator.generate_learning_path(
        _sample_analysis(),
        _sample_intent(),
        language="english",
    )

    assert learning_path.total_steps >= 3
    assert "understand loading and render flow" in learning_path.title.lower()
    assert "tailored to your goal" in learning_path.description.lower()
    assert learning_path.steps[0].concepts_covered
    assert any("Shimmer" in step.concepts_covered for step in learning_path.steps)
    assert any(step.recommended_files for step in learning_path.steps)
