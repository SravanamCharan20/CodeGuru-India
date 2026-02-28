"""Session management for CodeGuru India."""
import streamlit as st
import json
import os
from typing import Dict, Optional
from datetime import datetime


class SessionManager:
    """Manages user session state, preferences, and progress persistence."""
    
    def __init__(self):
        """Initialize session manager with Streamlit session state."""
        self._reset_for_new_pytest_case()
        self._ensure_session_initialized()

    def _reset_for_new_pytest_case(self):
        """
        Reset managed keys between pytest test cases when running in bare mode.

        Streamlit session state persists process-wide during tests, which can leak
        values across test cases. We detect per-test changes via PYTEST_CURRENT_TEST.
        """
        current_test = os.environ.get("PYTEST_CURRENT_TEST")
        if not current_test:
            return

        last_test = st.session_state.get("_codeguru_last_pytest_case")
        if last_test == current_test:
            return

        managed_keys = [
            "user_id",
            "language_preference",
            "current_learning_path",
            "uploaded_code",
            "uploaded_filename",
            "current_repository",
            "current_intent",
            "file_selection",
            "multi_file_analysis",
            "learning_artifacts",
            "traceability",
            "analysis_history",
            "local_storage",
            "progress_data",
            "progress_meta",
        ]
        for key in managed_keys:
            if key in st.session_state:
                del st.session_state[key]

        st.session_state["_codeguru_last_pytest_case"] = current_test
    
    def _ensure_session_initialized(self):
        """Ensure all required session state keys exist."""
        if "user_id" not in st.session_state:
            import uuid
            st.session_state.user_id = str(uuid.uuid4())
        
        if "language_preference" not in st.session_state:
            st.session_state.language_preference = "english"
        
        if "current_learning_path" not in st.session_state:
            st.session_state.current_learning_path = None
        
        if "uploaded_code" not in st.session_state:
            st.session_state.uploaded_code = None
        
        if "uploaded_filename" not in st.session_state:
            st.session_state.uploaded_filename = None
        
        # New fields for intent-driven analysis
        if "current_repository" not in st.session_state:
            st.session_state.current_repository = None
        
        if "current_intent" not in st.session_state:
            st.session_state.current_intent = None
        
        if "file_selection" not in st.session_state:
            st.session_state.file_selection = None
        
        if "multi_file_analysis" not in st.session_state:
            st.session_state.multi_file_analysis = None
        
        if "learning_artifacts" not in st.session_state:
            st.session_state.learning_artifacts = {
                'flashcards': [],
                'quizzes': [],
                'learning_paths': [],
                'concept_summary': {}
            }
        
        if "traceability" not in st.session_state:
            st.session_state.traceability = {
                'artifact_to_code': {},
                'code_to_artifacts': {},
                'validation_status': {}
            }
        
        if "analysis_history" not in st.session_state:
            st.session_state.analysis_history = []

        if "progress_data" not in st.session_state:
            st.session_state.progress_data = {}

        if "progress_meta" not in st.session_state:
            st.session_state.progress_meta = {
                "last_activity_type": None,
                "last_saved_at": None
            }
    
    def get_language_preference(self) -> str:
        """Get user's language preference."""
        return st.session_state.language_preference
    
    def set_language_preference(self, language: str) -> None:
        """Set user's language preference."""
        st.session_state.language_preference = language
        self._save_to_local_storage("language_preference", language)
    
    def get_current_learning_path(self) -> Optional[str]:
        """Get active learning path."""
        return st.session_state.current_learning_path
    
    def set_current_learning_path(self, path_id: str) -> None:
        """Set active learning path."""
        st.session_state.current_learning_path = path_id
    
    def save_progress(self, activity_type: str, data: Dict) -> None:
        """Save canonical learning progress payload to local storage."""
        now = datetime.now().isoformat()
        payload = self._normalize_progress_payload(data)

        st.session_state.progress_data = payload
        st.session_state.progress_meta = {
            "last_activity_type": activity_type,
            "last_saved_at": now
        }

        self._save_to_local_storage("progress_data", payload)
        self._save_to_local_storage("progress_meta", st.session_state.progress_meta)

        # Backward compatibility key for older code paths and persisted sessions.
        self._save_to_local_storage("progress", {
            "timestamp": now,
            "activity_type": activity_type,
            "data": payload
        })
    
    def load_progress(self) -> Dict:
        """Load canonical learning progress payload from session/local storage."""
        in_memory = st.session_state.get("progress_data")
        if isinstance(in_memory, dict) and in_memory:
            return in_memory

        persisted = self._load_from_local_storage("progress_data", None)
        if isinstance(persisted, dict):
            st.session_state.progress_data = persisted
            return persisted

        # Backward compatibility: migrate legacy wrapped payload.
        legacy = self._load_from_local_storage("progress", {})
        migrated = self._normalize_progress_payload(legacy)
        if migrated:
            st.session_state.progress_data = migrated
            self._save_to_local_storage("progress_data", migrated)
        return migrated
    
    def get_uploaded_code(self) -> Optional[str]:
        """Get currently uploaded code from session."""
        return st.session_state.uploaded_code
    
    def set_uploaded_code(self, code: str, filename: str) -> None:
        """Store uploaded code in session."""
        st.session_state.uploaded_code = code
        st.session_state.uploaded_filename = filename
    
    def _save_to_local_storage(self, key: str, value) -> None:
        """Save data to browser local storage via session state."""
        storage_key = f"codeguru_{key}"
        if "local_storage" not in st.session_state:
            st.session_state.local_storage = {}
        st.session_state.local_storage[storage_key] = value
    
    def _load_from_local_storage(self, key: str, default=None):
        """Load data from browser local storage via session state."""
        storage_key = f"codeguru_{key}"
        if "local_storage" not in st.session_state:
            st.session_state.local_storage = {}
        return st.session_state.local_storage.get(storage_key, default)

    def _normalize_progress_payload(self, data) -> Dict:
        """
        Normalize progress payload to a flat dictionary.

        Older versions wrapped payloads repeatedly as:
        {"timestamp": ..., "activity_type": ..., "data": {...}}
        This helper unwraps nested legacy format safely.
        """
        payload = data if isinstance(data, dict) else {}

        # Unwrap nested legacy wrappers.
        while (
            isinstance(payload, dict)
            and "data" in payload
            and "timestamp" in payload
            and "activity_type" in payload
        ):
            next_payload = payload.get("data")
            if isinstance(next_payload, dict):
                payload = next_payload
            else:
                return {}

        return payload if isinstance(payload, dict) else {}
    
    # ========================================================================
    # Intent-Driven Analysis Session Methods
    # ========================================================================
    
    def get_current_repository(self):
        """Get current repository information."""
        return st.session_state.current_repository
    
    def set_current_repository(self, repo_path: str, repo_analysis) -> None:
        """Set current repository."""
        st.session_state.current_repository = {
            'repo_path': repo_path,
            'repo_analysis': repo_analysis,
            'upload_timestamp': datetime.now().isoformat()
        }
        self._save_to_local_storage("current_repository", st.session_state.current_repository)
    
    def get_current_intent(self):
        """Get current user intent."""
        return st.session_state.current_intent
    
    def set_current_intent(self, intent) -> None:
        """Set current user intent."""
        st.session_state.current_intent = {
            'intent': intent,
            'interpretation_timestamp': datetime.now().isoformat(),
            'clarifications': []
        }
        self._save_to_local_storage("current_intent", st.session_state.current_intent)
    
    def get_file_selection(self):
        """Get current file selection."""
        return st.session_state.file_selection
    
    def set_file_selection(self, selection_result, manual_inclusions=None, manual_exclusions=None) -> None:
        """Set file selection result."""
        st.session_state.file_selection = {
            'selection_result': selection_result,
            'manual_inclusions': manual_inclusions or [],
            'manual_exclusions': manual_exclusions or []
        }
        self._save_to_local_storage("file_selection", st.session_state.file_selection)
    
    def get_multi_file_analysis(self):
        """Get multi-file analysis result."""
        return st.session_state.multi_file_analysis
    
    def set_multi_file_analysis(self, analysis) -> None:
        """Set multi-file analysis result."""
        st.session_state.multi_file_analysis = {
            'analysis': analysis,
            'analysis_timestamp': datetime.now().isoformat()
        }
        self._save_to_local_storage("multi_file_analysis", st.session_state.multi_file_analysis)
    
    def get_learning_artifacts(self):
        """Get generated learning artifacts."""
        return st.session_state.learning_artifacts
    
    def set_learning_artifacts(self, flashcards=None, quizzes=None, learning_paths=None, concept_summary=None) -> None:
        """Set learning artifacts."""
        if flashcards is not None:
            st.session_state.learning_artifacts['flashcards'] = flashcards
        if quizzes is not None:
            st.session_state.learning_artifacts['quizzes'] = quizzes
        if learning_paths is not None:
            st.session_state.learning_artifacts['learning_paths'] = learning_paths
        if concept_summary is not None:
            st.session_state.learning_artifacts['concept_summary'] = concept_summary
        
        self._save_to_local_storage("learning_artifacts", st.session_state.learning_artifacts)
    
    def get_traceability_data(self):
        """Get traceability data."""
        return st.session_state.traceability
    
    @property
    def traceability_data(self):
        """Property accessor for traceability data (used by TraceabilityManager)."""
        return st.session_state.traceability
    
    def add_to_analysis_history(self, intent, files_analyzed: list, artifacts_generated: int) -> None:
        """Add entry to analysis history."""
        history_entry = {
            'timestamp': datetime.now().isoformat(),
            'intent': intent,
            'files_analyzed': files_analyzed,
            'artifacts_generated': artifacts_generated
        }
        st.session_state.analysis_history.append(history_entry)
        self._save_to_local_storage("analysis_history", st.session_state.analysis_history)
    
    def get_analysis_history(self):
        """Get analysis history."""
        return st.session_state.analysis_history
    
    def clear_current_analysis(self) -> None:
        """Clear current analysis data (for starting new analysis)."""
        st.session_state.current_repository = None
        st.session_state.current_intent = None
        st.session_state.file_selection = None
        st.session_state.multi_file_analysis = None
        st.session_state.learning_artifacts = {
            'flashcards': [],
            'quizzes': [],
            'learning_paths': [],
            'concept_summary': {}
        }
        st.session_state.traceability = {
            'artifact_to_code': {},
            'code_to_artifacts': {},
            'validation_status': {}
        }
