"""Session management for CodeGuru India."""
import streamlit as st
import json
from typing import Dict, Optional
from datetime import datetime


class SessionManager:
    """Manages user session state, preferences, and progress persistence."""
    
    def __init__(self):
        """Initialize session manager with Streamlit session state."""
        self._ensure_session_initialized()
    
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
        """Save learning progress to local storage."""
        progress_data = {
            "timestamp": datetime.now().isoformat(),
            "activity_type": activity_type,
            "data": data
        }
        self._save_to_local_storage("progress", progress_data)
    
    def load_progress(self) -> Dict:
        """Load learning progress from local storage."""
        return self._load_from_local_storage("progress", {})
    
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
