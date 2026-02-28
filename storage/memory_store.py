"""Persistent memory store for analyses, chat, and generated learning artifacts."""

from __future__ import annotations

import json
import os
import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class MemoryStore:
    """SQLite-backed store for user analysis sessions and learning memory."""

    def __init__(self, db_path: str = "data/codeguru_memory.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _initialize(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS analysis_sessions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    source_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    source_ref TEXT,
                    language TEXT DEFAULT 'english',
                    summary TEXT DEFAULT '',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS chat_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    language TEXT DEFAULT 'english',
                    metadata_json TEXT DEFAULT '{}',
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES analysis_sessions(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS generated_artifacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    artifact_type TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES analysis_sessions(id) ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_analysis_sessions_user
                ON analysis_sessions(user_id, updated_at DESC);

                CREATE INDEX IF NOT EXISTS idx_chat_messages_session
                ON chat_messages(session_id, created_at ASC);

                CREATE INDEX IF NOT EXISTS idx_generated_artifacts_session
                ON generated_artifacts(session_id, artifact_type, updated_at DESC);
                """
            )

    def create_session(
        self,
        user_id: str,
        source_type: str,
        title: str,
        source_ref: Optional[str] = None,
        language: str = "english",
        summary: str = "",
    ) -> str:
        session_id = str(uuid.uuid4())
        now = _utc_now_iso()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO analysis_sessions (
                    id, user_id, source_type, title, source_ref, language, summary, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    user_id,
                    source_type,
                    title,
                    source_ref,
                    language,
                    summary,
                    now,
                    now,
                ),
            )
        return session_id

    def touch_session(self, session_id: str, summary: Optional[str] = None) -> None:
        now = _utc_now_iso()
        with self._connect() as conn:
            if summary is None:
                conn.execute(
                    "UPDATE analysis_sessions SET updated_at = ? WHERE id = ?",
                    (now, session_id),
                )
            else:
                conn.execute(
                    "UPDATE analysis_sessions SET summary = ?, updated_at = ? WHERE id = ?",
                    (summary, now, session_id),
                )

    def list_sessions(self, user_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, user_id, source_type, title, source_ref, language, summary, created_at, updated_at
                FROM analysis_sessions
                WHERE user_id = ?
                ORDER BY updated_at DESC
                LIMIT ?
                """,
                (user_id, limit),
            ).fetchall()
        return [dict(r) for r in rows]

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT id, user_id, source_type, title, source_ref, language, summary, created_at, updated_at
                FROM analysis_sessions
                WHERE id = ?
                """,
                (session_id,),
            ).fetchone()
        return dict(row) if row else None

    def save_chat_message(
        self,
        session_id: str,
        role: str,
        content: str,
        language: str = "english",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        now = _utc_now_iso()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO chat_messages (
                    session_id, role, content, language, metadata_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    role,
                    content,
                    language,
                    json.dumps(metadata or {}, ensure_ascii=False),
                    now,
                ),
            )
            conn.execute(
                "UPDATE analysis_sessions SET updated_at = ? WHERE id = ?",
                (now, session_id),
            )

    def get_chat_messages(self, session_id: str, limit: int = 200) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, session_id, role, content, language, metadata_json, created_at
                FROM chat_messages
                WHERE session_id = ?
                ORDER BY created_at ASC
                LIMIT ?
                """,
                (session_id, limit),
            ).fetchall()
        messages = []
        for row in rows:
            message = dict(row)
            try:
                message["metadata"] = json.loads(message.pop("metadata_json", "{}"))
            except json.JSONDecodeError:
                message["metadata"] = {}
            messages.append(message)
        return messages

    def save_artifact(
        self,
        session_id: str,
        artifact_type: str,
        payload: Any,
        replace: bool = True,
    ) -> None:
        now = _utc_now_iso()
        serialized = json.dumps(payload, ensure_ascii=False, default=str)
        with self._connect() as conn:
            if replace:
                existing = conn.execute(
                    """
                    SELECT id FROM generated_artifacts
                    WHERE session_id = ? AND artifact_type = ?
                    ORDER BY updated_at DESC
                    LIMIT 1
                    """,
                    (session_id, artifact_type),
                ).fetchone()
                if existing:
                    conn.execute(
                        """
                        UPDATE generated_artifacts
                        SET payload_json = ?, updated_at = ?
                        WHERE id = ?
                        """,
                        (serialized, now, existing["id"]),
                    )
                else:
                    conn.execute(
                        """
                        INSERT INTO generated_artifacts (
                            session_id, artifact_type, payload_json, created_at, updated_at
                        ) VALUES (?, ?, ?, ?, ?)
                        """,
                        (session_id, artifact_type, serialized, now, now),
                    )
            else:
                conn.execute(
                    """
                    INSERT INTO generated_artifacts (
                        session_id, artifact_type, payload_json, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (session_id, artifact_type, serialized, now, now),
                )
            conn.execute(
                "UPDATE analysis_sessions SET updated_at = ? WHERE id = ?",
                (now, session_id),
            )

    def get_artifact(self, session_id: str, artifact_type: str) -> Optional[Any]:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT payload_json
                FROM generated_artifacts
                WHERE session_id = ? AND artifact_type = ?
                ORDER BY updated_at DESC
                LIMIT 1
                """,
                (session_id, artifact_type),
            ).fetchone()
        if not row:
            return None
        try:
            return json.loads(row["payload_json"])
        except json.JSONDecodeError:
            return None

    def list_artifacts(self, session_id: str) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, session_id, artifact_type, payload_json, created_at, updated_at
                FROM generated_artifacts
                WHERE session_id = ?
                ORDER BY updated_at DESC
                """,
                (session_id,),
            ).fetchall()
        artifacts = []
        for row in rows:
            item = dict(row)
            try:
                item["payload"] = json.loads(item.pop("payload_json", "{}"))
            except json.JSONDecodeError:
                item["payload"] = None
            artifacts.append(item)
        return artifacts
