"""Traceability manager path resolution tests."""

import tempfile
from pathlib import Path

from learning.traceability_manager import TraceabilityManager
from models.intent_models import CodeEvidence
from session_manager import SessionManager


def test_register_artifact_resolves_repo_relative_paths():
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)
        target_file = repo_path / "frontend" / "src" / "App.jsx"
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(
            "function App() {\n  return <div>Hello</div>;\n}\nexport default App;\n",
            encoding="utf-8",
        )

        sm = SessionManager()
        sm.set_current_repository(str(repo_path), {"repo_url": "local"})
        tm = TraceabilityManager(sm)

        evidence = CodeEvidence(
            file_path="frontend/src/App.jsx",
            line_start=1,
            line_end=2,
            code_snippet="",
            context_description="App component",
        )

        ok = tm.register_artifact("artifact_app", "flashcard", [evidence])
        assert ok is True

        trace = tm.get_artifact_trace("artifact_app")
        assert trace is not None
        assert len(trace.links) == 1
        assert trace.links[0].code_evidence.file_path.endswith("frontend/src/App.jsx")
        assert "function App()" in trace.links[0].code_evidence.code_snippet


def test_register_artifact_without_evidence_is_graceful():
    sm = SessionManager()
    tm = TraceabilityManager(sm)

    ok = tm.register_artifact("artifact_empty", "learning_step", [])
    assert ok is True

    trace = tm.get_artifact_trace("artifact_empty")
    assert trace is None

    status = sm.traceability_data["validation_status"]["artifact_empty"]
    assert status["is_valid"] is False
