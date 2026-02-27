"""
Data models for Intent-Driven Repository Analysis System.
"""

from .intent_models import (
    UserIntent,
    IntentScope,
    FileSelection,
    SelectionResult,
    FileRelationship,
    DataFlow,
    ExecutionPath,
    MultiFileAnalysis,
    CodeEvidence,
    CodeFlashcard,
    CodeQuestion,
    LearningStep,
    LearningPath,
    TraceabilityLink,
    ArtifactTrace,
    UploadResult
)

__all__ = [
    'UserIntent',
    'IntentScope',
    'FileSelection',
    'SelectionResult',
    'FileRelationship',
    'DataFlow',
    'ExecutionPath',
    'MultiFileAnalysis',
    'CodeEvidence',
    'CodeFlashcard',
    'CodeQuestion',
    'LearningStep',
    'LearningPath',
    'TraceabilityLink',
    'ArtifactTrace',
    'UploadResult'
]
