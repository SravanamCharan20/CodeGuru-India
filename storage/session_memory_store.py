"""Session-based in-memory store for analyses, chat, and generated artifacts."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

import streamlit as st


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class SessionMemoryStore:
    """Session-state backed memory store (no external database)."""

    def __init__(self):
        self._ensure_store()

    def _ensure_store(self) -> None:
        if "memory_sessions" not in st.session_state:
            st.session_state.memory_sessions = {}
        if "memory_chat_messages" not in st.session_state:
            st.session_state.memory_chat_messages = {}
        if "memory_artifacts" not in st.session_state:
            st.session_state.memory_artifacts = {}
        if "memory_chat_counter" not in st.session_state:
            st.session_state.memory_chat_counter = 0
        if "memory_artifact_counter" not in st.session_state:
            st.session_state.memory_artifact_counter = 0

    def create_session(
        self,
        user_id: str,
        source_type: str,
        title: str,
        source_ref: Optional[str] = None,
        language: str = "english",
        summary: str = "",
    ) -> str:
        self._ensure_store()
        session_id = str(uuid.uuid4())
        now = _utc_now_iso()
        st.session_state.memory_sessions[session_id] = {
            "id": session_id,
            "user_id": user_id,
            "source_type": source_type,
            "title": title,
            "source_ref": source_ref,
            "language": language,
            "summary": summary,
            "created_at": now,
            "updated_at": now,
        }
        st.session_state.memory_chat_messages.setdefault(session_id, [])
        st.session_state.memory_artifacts.setdefault(session_id, {})
        return session_id

    def touch_session(self, session_id: str, summary: Optional[str] = None) -> None:
        self._ensure_store()
        session = st.session_state.memory_sessions.get(session_id)
        if not session:
            return
        session["updated_at"] = _utc_now_iso()
        if summary is not None:
            session["summary"] = summary

    def list_sessions(self, user_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        self._ensure_store()
        rows = [
            session
            for session in st.session_state.memory_sessions.values()
            if session.get("user_id") == user_id
        ]
        rows.sort(key=lambda item: item.get("updated_at", ""), reverse=True)
        return rows[:limit]

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        self._ensure_store()
        session = st.session_state.memory_sessions.get(session_id)
        return dict(session) if session else None

    def save_chat_message(
        self,
        session_id: str,
        role: str,
        content: str,
        language: str = "english",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._ensure_store()
        if session_id not in st.session_state.memory_sessions:
            return
        st.session_state.memory_chat_counter += 1
        message = {
            "id": st.session_state.memory_chat_counter,
            "session_id": session_id,
            "role": role,
            "content": content,
            "language": language,
            "metadata": metadata or {},
            "created_at": _utc_now_iso(),
        }
        st.session_state.memory_chat_messages.setdefault(session_id, []).append(message)
        self.touch_session(session_id)

    def get_chat_messages(self, session_id: str, limit: int = 200) -> List[Dict[str, Any]]:
        self._ensure_store()
        messages = st.session_state.memory_chat_messages.get(session_id, [])
        return [dict(item) for item in messages[:limit]]

    def save_artifact(
        self,
        session_id: str,
        artifact_type: str,
        payload: Any,
        replace: bool = True,
    ) -> None:
        self._ensure_store()
        if session_id not in st.session_state.memory_sessions:
            return

        artifact_bucket = st.session_state.memory_artifacts.setdefault(session_id, {})
        now = _utc_now_iso()

        if replace:
            existing = artifact_bucket.get(artifact_type)
            if existing:
                existing["payload"] = payload
                existing["updated_at"] = now
            else:
                st.session_state.memory_artifact_counter += 1
                artifact_bucket[artifact_type] = {
                    "id": st.session_state.memory_artifact_counter,
                    "session_id": session_id,
                    "artifact_type": artifact_type,
                    "payload": payload,
                    "created_at": now,
                    "updated_at": now,
                }
        else:
            st.session_state.memory_artifact_counter += 1
            key = f"{artifact_type}:{st.session_state.memory_artifact_counter}"
            artifact_bucket[key] = {
                "id": st.session_state.memory_artifact_counter,
                "session_id": session_id,
                "artifact_type": artifact_type,
                "payload": payload,
                "created_at": now,
                "updated_at": now,
            }

        self.touch_session(session_id)

    def get_artifact(self, session_id: str, artifact_type: str) -> Optional[Any]:
        self._ensure_store()
        artifact_bucket = st.session_state.memory_artifacts.get(session_id, {})
        artifact = artifact_bucket.get(artifact_type)
        if artifact:
            return artifact.get("payload")

        # Fallback for non-replace entries.
        candidates = [
            value
            for value in artifact_bucket.values()
            if value.get("artifact_type") == artifact_type
        ]
        if not candidates:
            return None
        candidates.sort(key=lambda item: item.get("updated_at", ""), reverse=True)
        return candidates[0].get("payload")

    def list_artifacts(self, session_id: str) -> List[Dict[str, Any]]:
        self._ensure_store()
        artifact_bucket = st.session_state.memory_artifacts.get(session_id, {})
        rows = []
        for item in artifact_bucket.values():
            rows.append(
                {
                    "id": item.get("id"),
                    "session_id": item.get("session_id"),
                    "artifact_type": item.get("artifact_type"),
                    "payload": item.get("payload"),
                    "created_at": item.get("created_at"),
                    "updated_at": item.get("updated_at"),
                }
            )
        rows.sort(key=lambda obj: obj.get("updated_at", ""), reverse=True)
        return rows
