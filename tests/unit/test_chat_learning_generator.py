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
