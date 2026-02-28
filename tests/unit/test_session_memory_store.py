"""Unit tests for session-based memory store."""

from storage.session_memory_store import SessionMemoryStore


def test_session_memory_store_session_chat_and_artifacts():
    store = SessionMemoryStore()

    session_id = store.create_session(
        user_id="user_1",
        source_type="repository",
        title="demo-repo",
        source_ref="/tmp/demo",
        language="english",
        summary="initial summary",
    )

    session = store.get_session(session_id)
    assert session is not None
    assert session["title"] == "demo-repo"

    store.save_chat_message(session_id, role="user", content="How auth works?", language="english")
    store.save_chat_message(session_id, role="assistant", content="Auth flow explanation", language="english")

    messages = store.get_chat_messages(session_id)
    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"

    store.save_artifact(session_id, "chat_quiz", {"questions": [1, 2]}, replace=True)
    artifact = store.get_artifact(session_id, "chat_quiz")
    assert artifact == {"questions": [1, 2]}

    artifacts = store.list_artifacts(session_id)
    assert len(artifacts) >= 1
