"""Unit tests for intent-driven chat learning generator."""

from generators.chat_learning_generator import ChatLearningGenerator


def _sample_messages():
    return [
        {
            "role": "user",
            "content": "How does authentication middleware validate JWT and attach user context?",
        },
        {
            "role": "assistant",
            "content": (
                "The request first hits middleware, verifies JWT signature and expiry, "
                "then loads user metadata and attaches it to request context."
            ),
        },
        {
            "role": "user",
            "content": "Why do we rotate refresh tokens, and where is replay prevention handled?",
        },
        {
            "role": "assistant",
            "content": (
                "Rotation limits token replay risk. Replay prevention is enforced in the refresh handler "
                "by invalidating old token ids after successful exchange."
            ),
        },
        {
            "role": "user",
            "content": "Compare middleware auth with controller-level checks in this codebase.",
        },
        {
            "role": "assistant",
            "content": (
                "Middleware provides coarse-grained gatekeeping early, while controller checks "
                "enforce fine-grained authorization per action."
            ),
        },
    ]


def test_flashcards_are_intent_driven_and_challenging():
    generator = ChatLearningGenerator()
    cards = generator.generate_flashcards(_sample_messages(), language="english", limit=9)

    assert len(cards) >= 3
    assert any("Scenario challenge" in card["front"] for card in cards)
    assert any("Misconception check" in card["front"] for card in cards)
    assert any(card.get("intent_type") for card in cards)
    assert all(card["difficulty"] in {"intermediate", "advanced"} for card in cards)


def test_quiz_generation_uses_intent_themes_not_raw_chat_echo():
    generator = ChatLearningGenerator()
    quiz = generator.generate_quiz(_sample_messages(), language="english", num_questions=4)
    questions = quiz["questions"]

    assert len(questions) >= 2
    for question in questions:
        assert "Scenario:" in question["question_text"]
        assert len(question["options"]) == 4
        assert question["correct_answer"] in question["options"]
        assert question.get("intent_type")
        assert question["difficulty"] in {"intermediate", "advanced"}


def test_generation_filters_generic_noise_and_keeps_real_concept():
    generator = ChatLearningGenerator()
    messages = [
        {"role": "user", "content": "tell me what is shimmer in this repo and why should we have to use that?"},
        {
            "role": "assistant",
            "content": (
                "Shimmer is a skeleton loading UI. It improves perceived performance by showing placeholder "
                "structure before data arrives."
            ),
            "metadata": {
                "code_references": [{"file": "src/components/Shimmer.jsx", "lines": "1-40"}]
            },
        },
    ]

    cards = generator.generate_flashcards(messages, language="english", limit=6)
    quiz = generator.generate_quiz(messages, language="english", num_questions=2)

    assert cards
    assert quiz["questions"]
    assert all("tell" not in card["front"].lower() for card in cards)
    assert any("shimmer" in card.get("concept", "").lower() for card in cards)
    for question in quiz["questions"]:
        assert "tell" not in question["question_text"].lower()
        assert "tell" not in question["correct_answer"].lower()
