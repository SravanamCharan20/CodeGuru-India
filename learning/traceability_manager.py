"""
Traceability Manager for maintaining mappings between learning artifacts and source code.

This module ensures every learning artifact (flashcard, quiz question, learning step)
is traceable to specific code snippets with file paths and line numbers.
"""

import logging
import os
from typing import List, Dict, Optional
from datetime import datetime
from models.intent_models import (
    CodeEvidence,
    TraceabilityLink,
    ArtifactTrace
)

logger = logging.getLogger(__name__)


class TraceabilityManager:
    """Maintains bidirectional mappings between learning artifacts and source code."""
    
    def __init__(self, session_manager=None):
        """
        Initialize with session manager for persistence.
        
        Args:
            session_manager: SessionManager instance for storing traceability data
        """
        if session_manager is None:
            from session_manager import SessionManager
            session_manager = SessionManager()
        self.session_manager = session_manager
        self._initialize_storage()
    
    def _initialize_storage(self):
        """Initialize traceability storage in session state."""
        data = self.session_manager.traceability_data
        if 'artifact_to_code' not in data:
            data['artifact_to_code'] = {}  # artifact_id -> [CodeEvidence, ...]
        if 'code_to_artifacts' not in data:
            data['code_to_artifacts'] = {}  # "file_path:line" -> [artifact_id, ...]
        if 'validation_status' not in data:
            data['validation_status'] = {}  # artifact_id -> {is_valid, last_validated, message}
        if 'artifact_types' not in data:
            data['artifact_types'] = {}  # artifact_id -> artifact_type
    
    def register_artifact(
        self,
        artifact_id: str,
        artifact_type: str,
        code_evidence: List[CodeEvidence]
    ) -> bool:
        """
        Register a new artifact with its code evidence.
        
        Args:
            artifact_id: Unique identifier for the artifact
            artifact_type: Type of artifact (flashcard, quiz_question, learning_step)
            code_evidence: List of CodeEvidence objects
            
        Returns:
            True if registration successful, False otherwise
        """
        try:
            if not code_evidence:
                logger.warning(f"Artifact {artifact_id} has no code evidence")
                return False
            
            # Verify all evidence exists
            for evidence in code_evidence:
                if not self.verify_evidence_exists(evidence):
                    logger.warning(f"Evidence does not exist: {evidence.file_path}:{evidence.line_start}")
                    return False
            
            # Store artifact-to-code mapping
            self.session_manager.traceability_data['artifact_to_code'][artifact_id] = [
                {
                    'file_path': e.file_path,
                    'line_start': e.line_start,
                    'line_end': e.line_end,
                    'code_snippet': e.code_snippet,
                    'context_description': e.context_description
                }
                for e in code_evidence
            ]
            self.session_manager.traceability_data.setdefault('artifact_types', {})[artifact_id] = artifact_type
            
            # Store code-to-artifact mappings
            for evidence in code_evidence:
                key = f"{evidence.file_path}:{evidence.line_start}"
                if key not in self.session_manager.traceability_data['code_to_artifacts']:
                    self.session_manager.traceability_data['code_to_artifacts'][key] = []
                self.session_manager.traceability_data['code_to_artifacts'][key].append(artifact_id)
            
            # Initialize validation status
            self.session_manager.traceability_data['validation_status'][artifact_id] = {
                'is_valid': True,
                'last_validated': datetime.now().isoformat(),
                'validation_message': 'Artifact registered successfully'
            }
            
            logger.info(f"Registered artifact {artifact_id} with {len(code_evidence)} evidence links")
            return True
        
        except Exception as e:
            logger.error(f"Failed to register artifact {artifact_id}: {e}")
            return False
    
    def get_artifact_trace(self, artifact_id: str) -> Optional[ArtifactTrace]:
        """
        Get traceability information for an artifact.
        
        Args:
            artifact_id: Artifact identifier
            
        Returns:
            ArtifactTrace object or None if not found
        """
        try:
            evidence_list = self.session_manager.traceability_data['artifact_to_code'].get(artifact_id)
            if not evidence_list:
                return None
            
            # Convert evidence dicts to TraceabilityLink objects
            links = []
            for i, evidence_dict in enumerate(evidence_list):
                evidence = CodeEvidence(
                    file_path=evidence_dict['file_path'],
                    line_start=evidence_dict['line_start'],
                    line_end=evidence_dict['line_end'],
                    code_snippet=evidence_dict['code_snippet'],
                    context_description=evidence_dict.get('context_description', '')
                )
                
                link = TraceabilityLink(
                    link_id=f"{artifact_id}_link_{i}",
                    artifact_id=artifact_id,
                    artifact_type=self.session_manager.traceability_data.get('artifact_types', {}).get(artifact_id, "unknown"),
                    code_evidence=evidence,
                    created_at=datetime.now(),
                    is_valid=True
                )
                links.append(link)
            
            # Get validation status
            validation = self.session_manager.traceability_data['validation_status'].get(artifact_id, {})
            
            return ArtifactTrace(
                artifact_id=artifact_id,
                artifact_type=self.session_manager.traceability_data.get('artifact_types', {}).get(artifact_id, "unknown"),
                links=links,
                validation_status="valid" if validation.get('is_valid', True) else "invalid",
                last_validated=datetime.fromisoformat(validation.get('last_validated', datetime.now().isoformat()))
            )
        
        except Exception as e:
            logger.error(f"Failed to get artifact trace for {artifact_id}: {e}")
            return None
    
    def get_artifacts_for_code(
        self,
        file_path: str,
        line_number: Optional[int] = None,
        line_end: Optional[int] = None
    ) -> List[str]:
        """
        Get artifacts that reference specific code.
        
        Args:
            file_path: Path to code file
            line_number: Optional specific line number
            line_end: Optional line range end
            
        Returns:
            List of artifact IDs
        """
        try:
            artifacts = set()
            
            if line_number is not None:
                # Support exact line and line-range lookups.
                range_end = line_end if line_end is not None else line_number
                for key, artifact_ids in self.session_manager.traceability_data['code_to_artifacts'].items():
                    if not key.startswith(f"{file_path}:"):
                        continue
                    try:
                        evidence_line = int(key.rsplit(":", 1)[1])
                    except (ValueError, IndexError):
                        continue
                    if line_number <= evidence_line <= range_end:
                        artifacts.update(artifact_ids)
            else:
                # Get all artifacts for file
                for key, artifact_ids in self.session_manager.traceability_data['code_to_artifacts'].items():
                    if key.startswith(f"{file_path}:"):
                        artifacts.update(artifact_ids)
            
            return list(artifacts)
        
        except Exception as e:
            logger.error(f"Failed to get artifacts for {file_path}: {e}")
            return []
    
    def validate_artifact(self, artifact_id: str, current_code: str) -> bool:
        """
        Validate that artifact's code evidence still exists.
        
        Args:
            artifact_id: Artifact identifier
            current_code: Current code content to validate against
            
        Returns:
            True if valid, False otherwise
        """
        try:
            evidence_list = self.session_manager.traceability_data['artifact_to_code'].get(artifact_id)
            if not evidence_list:
                return False
            
            # Check if code snippets still exist in current code
            all_valid = True
            for evidence_dict in evidence_list:
                snippet = evidence_dict['code_snippet']
                if snippet and snippet not in current_code:
                    all_valid = False
                    break
            
            # Update validation status
            self.session_manager.traceability_data['validation_status'][artifact_id] = {
                'is_valid': all_valid,
                'last_validated': datetime.now().isoformat(),
                'validation_message': 'Valid' if all_valid else 'Code has changed'
            }
            
            return all_valid
        
        except Exception as e:
            logger.error(f"Failed to validate artifact {artifact_id}: {e}")
            return False
    
    def mark_artifacts_outdated(self, file_path: str) -> List[str]:
        """
        Mark artifacts as outdated when code changes.
        
        Args:
            file_path: Path to changed file
            
        Returns:
            List of affected artifact IDs
        """
        try:
            affected_artifacts = self.get_artifacts_for_code(file_path)
            
            for artifact_id in affected_artifacts:
                self.session_manager.traceability_data['validation_status'][artifact_id] = {
                    'is_valid': False,
                    'last_validated': datetime.now().isoformat(),
                    'validation_message': f'Code in {file_path} has been modified'
                }
            
            logger.info(f"Marked {len(affected_artifacts)} artifacts as outdated for {file_path}")
            return affected_artifacts
        
        except Exception as e:
            logger.error(f"Failed to mark artifacts outdated for {file_path}: {e}")
            return []
    
    def get_code_snippet(self, evidence: CodeEvidence) -> str:
        """
        Retrieve code snippet for evidence.
        
        Args:
            evidence: CodeEvidence object
            
        Returns:
            Code snippet string
        """
        try:
            # If snippet is already in evidence, return it
            if evidence.code_snippet:
                return evidence.code_snippet
            
            # Otherwise, try to read from file
            if os.path.exists(evidence.file_path):
                with open(evidence.file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                    # Extract lines (1-indexed to 0-indexed)
                    start_idx = max(0, evidence.line_start - 1)
                    end_idx = min(len(lines), evidence.line_end)
                    
                    snippet = ''.join(lines[start_idx:end_idx])
                    return snippet
            
            return ""
        
        except Exception as e:
            logger.error(f"Failed to get code snippet: {e}")
            return ""
    
    def verify_evidence_exists(self, evidence: CodeEvidence) -> bool:
        """
        Verify that code evidence exists before creating artifact.
        
        Args:
            evidence: CodeEvidence to verify
            
        Returns:
            True if evidence exists, False otherwise
        """
        try:
            # Check if file exists
            if not os.path.exists(evidence.file_path):
                # Allow relative/non-local evidence if a snippet is already provided.
                # This supports generated artifacts that reference repo-relative paths.
                if evidence.code_snippet:
                    return True
                logger.warning(f"File does not exist: {evidence.file_path}")
                return False
            
            # Check if line numbers are valid
            if evidence.line_start < 1 or evidence.line_end < evidence.line_start:
                logger.warning(f"Invalid line numbers: {evidence.line_start}-{evidence.line_end}")
                return False
            
            # If snippet provided, verify it exists in file
            if evidence.code_snippet:
                with open(evidence.file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if evidence.code_snippet not in content:
                        logger.warning(f"Code snippet not found in {evidence.file_path}")
                        return False
            
            return True
        
        except Exception as e:
            logger.error(f"Failed to verify evidence: {e}")
            return False
