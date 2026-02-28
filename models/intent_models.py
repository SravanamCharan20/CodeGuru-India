"""
Core data models for Intent-Driven Repository Analysis System.

This module defines all data structures used throughout the system for
intent interpretation, file selection, multi-file analysis, learning
artifact generation, and traceability management.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime


# ============================================================================
# Intent Models
# ============================================================================

@dataclass
class IntentScope:
    """Defines the scope of analysis."""
    scope_type: str  # "entire_repo", "specific_folders", "specific_files", "technology"
    target_paths: List[str] = field(default_factory=list)
    exclude_paths: List[str] = field(default_factory=list)


@dataclass
class UserIntent:
    """Structured representation of user's learning goal."""
    primary_intent: str  # Main learning goal
    secondary_intents: List[str] = field(default_factory=list)
    scope: Optional[IntentScope] = None
    audience_level: str = "intermediate"  # beginner, intermediate, advanced
    technologies: List[str] = field(default_factory=list)
    confidence_score: float = 0.0  # 0.0-1.0, how confident the interpretation is


# ============================================================================
# File Selection Models
# ============================================================================

@dataclass
class FileSelection:
    """Represents a selected file with relevance information."""
    file_info: Any  # FileInfo from RepoAnalyzer
    relevance_score: float  # 0.0-1.0
    selection_reason: str
    priority: int  # 1 (highest) to N (lowest)
    file_role: str  # "entry_point", "core_logic", "utility", "model", "view", "controller"


@dataclass
class SelectionResult:
    """Result of file selection process."""
    selected_files: List[FileSelection] = field(default_factory=list)
    excluded_count: int = 0
    total_scanned: int = 0
    selection_summary: str = ""


# ============================================================================
# Analysis Models
# ============================================================================

@dataclass
class FileRelationship:
    """Represents a relationship between two files."""
    source_file: str
    target_file: str
    relationship_type: str  # "imports", "calls", "extends", "implements", "uses"
    details: str = ""


@dataclass
class DataFlow:
    """Represents data flow between components."""
    flow_id: str
    start_file: str
    start_line: int
    end_file: str
    end_line: int
    data_description: str
    flow_path: List[str] = field(default_factory=list)  # Files in the flow path


@dataclass
class ExecutionPath:
    """Represents an execution path through the codebase."""
    path_id: str
    entry_point: str
    steps: List[Dict[str, Any]] = field(default_factory=list)  # Each step: {file, function, line, description}
    path_description: str = ""


@dataclass
class MultiFileAnalysis:
    """Complete multi-file analysis result."""
    analyzed_files: List[str] = field(default_factory=list)
    file_analyses: Dict[str, Any] = field(default_factory=dict)  # file_path -> CodeAnalysis
    relationships: List[FileRelationship] = field(default_factory=list)
    dependency_graph: Dict[str, List[str]] = field(default_factory=dict)  # file -> dependencies
    data_flows: List[DataFlow] = field(default_factory=list)
    execution_paths: List[ExecutionPath] = field(default_factory=list)
    cross_file_patterns: List[Any] = field(default_factory=list)  # List[Pattern]
    key_concepts: List[Dict[str, Any]] = field(default_factory=list)  # Extracted concepts with file references
    analysis_summary: str = ""


# ============================================================================
# Learning Artifact Models
# ============================================================================

@dataclass
class CodeEvidence:
    """Evidence from code supporting a learning artifact."""
    file_path: str
    line_start: int
    line_end: int
    code_snippet: str
    context_description: str = ""


@dataclass
class CodeFlashcard:
    """Flashcard with code evidence."""
    id: str
    front: str
    back: str
    topic: str
    difficulty: str  # beginner, intermediate, advanced
    last_reviewed: Optional[datetime] = None
    next_review: Optional[datetime] = None
    mastered: bool = False
    code_evidence: List[CodeEvidence] = field(default_factory=list)
    concept_category: str = ""  # "function", "class", "pattern", "data_flow", "architecture"


@dataclass
class CodeQuestion:
    """Quiz question with code evidence."""
    id: str
    type: str  # "multiple_choice", "true_false", "short_answer"
    question_text: str
    options: List[str] = field(default_factory=list)
    correct_answer: str = ""
    explanation: str = ""
    code_evidence: List[CodeEvidence] = field(default_factory=list)
    question_category: str = ""  # "behavior", "flow", "pattern", "architecture"


@dataclass
class LearningStep:
    """A step in a learning path."""
    step_id: str
    step_number: int
    title: str
    description: str
    estimated_time_minutes: int
    recommended_files: List[str] = field(default_factory=list)
    concepts_covered: List[str] = field(default_factory=list)
    code_evidence: List[CodeEvidence] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)  # IDs of prerequisite steps


@dataclass
class LearningPath:
    """Complete learning path."""
    path_id: str
    title: str
    description: str
    total_steps: int
    estimated_total_time_minutes: int
    steps: List[LearningStep] = field(default_factory=list)
    difficulty_level: str = "intermediate"  # beginner, intermediate, advanced


# ============================================================================
# Traceability Models
# ============================================================================

@dataclass
class TraceabilityLink:
    """Link between artifact and code."""
    link_id: str
    artifact_id: str
    artifact_type: str  # "flashcard", "quiz_question", "learning_step"
    code_evidence: CodeEvidence
    created_at: datetime = field(default_factory=datetime.now)
    is_valid: bool = True  # False if code has changed


@dataclass
class ArtifactTrace:
    """Complete traceability information for an artifact."""
    artifact_id: str
    artifact_type: str
    links: List[TraceabilityLink] = field(default_factory=list)
    validation_status: str = "valid"  # "valid", "outdated", "invalid"
    last_validated: datetime = field(default_factory=datetime.now)

    @property
    def code_locations(self) -> List[TraceabilityLink]:
        """
        Backward-compatible alias used by older tests/callers.

        Returns:
            List of traceability links for this artifact.
        """
        return self.links


# ============================================================================
# Repository Management Models
# ============================================================================

@dataclass
class UploadResult:
    """Result of repository upload."""
    success: bool
    repo_path: str = ""
    repo_analysis: Optional[Any] = None  # RepoAnalysis
    error_message: Optional[str] = None
    validation_warnings: List[str] = field(default_factory=list)

    def __getitem__(self, key: str):
        """
        Backward-compatible dict-like access.
        """
        if key == "success":
            return self.success
        if key == "repo_path":
            return self.repo_path
        if key == "repo_analysis":
            return self.repo_analysis
        if key in {"error", "error_message"}:
            return self.error_message
        if key == "validation_warnings":
            return self.validation_warnings
        raise KeyError(key)

    def get(self, key: str, default=None):
        """
        Backward-compatible dict-like get().
        """
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key: str) -> bool:
        return key in {
            "success",
            "repo_path",
            "repo_analysis",
            "error",
            "error_message",
            "validation_warnings",
        }
