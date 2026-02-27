"""
End-to-End Integration Tests for Intent-Driven Repository Analysis.

Tests the complete workflow from repository upload to artifact generation.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, MagicMock

# Import components
from analyzers.repository_manager import RepositoryManager
from analyzers.intent_interpreter import IntentInterpreter
from analyzers.file_selector import FileSelector
from analyzers.multi_file_analyzer import MultiFileAnalyzer
from generators.learning_artifact_generator import LearningArtifactGenerator
from learning.traceability_manager import TraceabilityManager
from analyzers.intent_driven_orchestrator import IntentDrivenOrchestrator
from session_manager import SessionManager


class TestEndToEndFlow:
    """Test complete intent-driven analysis workflow."""
    
    @pytest.fixture
    def sample_repo_path(self):
        """Create a sample repository for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create sample Python files
            sample_code = """
def authenticate_user(username, password):
    '''Authenticate user with credentials.'''
    if not username or not password:
        return False
    # Authentication logic here
    return True

class UserManager:
    '''Manages user operations.'''
    
    def __init__(self):
        self.users = {}
    
    def add_user(self, username, email):
        '''Add a new user.'''
        self.users[username] = {'email': email}
        return True
"""
            
            # Write sample file
            sample_file = Path(tmpdir) / "auth.py"
            sample_file.write_text(sample_code)
            
            yield tmpdir
    
    @pytest.fixture
    def mock_components(self):
        """Create mock components for testing."""
        # Mock LangChain orchestrator
        mock_orchestrator = Mock()
        mock_orchestrator.generate_with_chain = Mock(return_value="Mocked AI response")
        
        # Mock repo analyzer
        mock_repo_analyzer = Mock()
        mock_repo_analyzer.analyze_repository = Mock(return_value={
            'languages': ['Python'],
            'file_count': 1,
            'total_lines': 20
        })
        
        # Mock code analyzer
        mock_code_analyzer = Mock()
        
        # Mock flashcard manager
        mock_flashcard_manager = Mock()
        
        # Mock quiz engine
        mock_quiz_engine = Mock()
        
        return {
            'orchestrator': mock_orchestrator,
            'repo_analyzer': mock_repo_analyzer,
            'code_analyzer': mock_code_analyzer,
            'flashcard_manager': mock_flashcard_manager,
            'quiz_engine': mock_quiz_engine
        }
    
    def test_complete_workflow_english(self, sample_repo_path, mock_components):
        """Test complete workflow with English language."""
        # Initialize components
        session_manager = SessionManager()
        
        repo_manager = RepositoryManager(
            repo_analyzer=mock_components['repo_analyzer'],
            max_size_mb=100
        )
        
        intent_interpreter = IntentInterpreter(
            langchain_orchestrator=mock_components['orchestrator']
        )
        
        file_selector = FileSelector(
            code_analyzer=mock_components['code_analyzer']
        )
        
        multi_file_analyzer = MultiFileAnalyzer(
            code_analyzer=mock_components['code_analyzer']
        )
        
        traceability_manager = TraceabilityManager()
        
        artifact_generator = LearningArtifactGenerator(
            flashcard_manager=mock_components['flashcard_manager'],
            quiz_engine=mock_components['quiz_engine'],
            langchain_orchestrator=mock_components['orchestrator']
        )
        
        orchestrator = IntentDrivenOrchestrator(
            repository_manager=repo_manager,
            intent_interpreter=intent_interpreter,
            file_selector=file_selector,
            multi_file_analyzer=multi_file_analyzer,
            learning_artifact_generator=artifact_generator,
            traceability_manager=traceability_manager,
            session_manager=session_manager
        )
        
        # Step 1: Upload repository
        result = repo_manager.upload_from_folder(sample_repo_path)
        assert result['success'] is True
        assert 'repo_path' in result
        
        # Store in session
        session_manager.set_current_repository(
            repo_path=result['repo_path'],
            repo_analysis=result.get('repo_analysis', {})
        )
        
        # Step 2: Analyze with intent
        user_input = "I want to learn how authentication works"
        
        result = orchestrator.analyze_repository_with_intent(
            repo_path=result['repo_path'],
            user_input=user_input,
            language="english"
        )
        
        # Verify results
        assert result['status'] in ['success', 'clarification_needed', 'no_files_found']
        
        if result['status'] == 'success':
            assert 'intent' in result
            assert 'flashcards' in result
            assert 'quiz' in result
            assert 'learning_path' in result
            assert 'concept_summary' in result
    
    def test_complete_workflow_hindi(self, sample_repo_path, mock_components):
        """Test complete workflow with Hindi language."""
        session_manager = SessionManager()
        
        repo_manager = RepositoryManager(
            repo_analyzer=mock_components['repo_analyzer'],
            max_size_mb=100
        )
        
        intent_interpreter = IntentInterpreter(
            langchain_orchestrator=mock_components['orchestrator']
        )
        
        file_selector = FileSelector(
            code_analyzer=mock_components['code_analyzer']
        )
        
        multi_file_analyzer = MultiFileAnalyzer(
            code_analyzer=mock_components['code_analyzer']
        )
        
        traceability_manager = TraceabilityManager()
        
        artifact_generator = LearningArtifactGenerator(
            flashcard_manager=mock_components['flashcard_manager'],
            quiz_engine=mock_components['quiz_engine'],
            langchain_orchestrator=mock_components['orchestrator']
        )
        
        orchestrator = IntentDrivenOrchestrator(
            repository_manager=repo_manager,
            intent_interpreter=intent_interpreter,
            file_selector=file_selector,
            multi_file_analyzer=multi_file_analyzer,
            learning_artifact_generator=artifact_generator,
            traceability_manager=traceability_manager,
            session_manager=session_manager
        )
        
        # Upload and analyze with Hindi
        result = repo_manager.upload_from_folder(sample_repo_path)
        session_manager.set_current_repository(
            repo_path=result['repo_path'],
            repo_analysis=result.get('repo_analysis', {})
        )
        
        result = orchestrator.analyze_repository_with_intent(
            repo_path=result['repo_path'],
            user_input="मैं प्रमाणीकरण के बारे में सीखना चाहता हूं",
            language="hindi"
        )
        
        assert result['status'] in ['success', 'clarification_needed', 'no_files_found']
    
    def test_session_persistence(self, sample_repo_path, mock_components):
        """Test session state persistence."""
        session_manager = SessionManager()
        
        # Set repository
        session_manager.set_current_repository(
            repo_path=sample_repo_path,
            repo_analysis={'languages': ['Python']}
        )
        
        # Verify retrieval
        repo_data = session_manager.get_current_repository()
        assert repo_data is not None
        assert repo_data['repo_path'] == sample_repo_path
        
        # Set intent
        from models.intent_models import UserIntent, IntentScope
        
        intent = UserIntent(
            primary_intent="learn_authentication",
            secondary_intents=[],
            scope=IntentScope(scope_type="full_repository"),
            audience_level="intermediate",
            technologies=["Python"],
            confidence_score=0.9
        )
        
        session_manager.set_current_intent(intent)
        
        # Verify retrieval
        intent_data = session_manager.get_current_intent()
        assert intent_data is not None
        assert intent_data['intent'].primary_intent == "learn_authentication"
    
    def test_traceability_throughout_workflow(self, sample_repo_path, mock_components):
        """Test that traceability is maintained throughout workflow."""
        traceability_manager = TraceabilityManager()
        
        # Register artifacts
        from models.intent_models import CodeEvidence
        
        evidence = CodeEvidence(
            file_path="auth.py",
            line_start=1,
            line_end=5,
            code_snippet="def authenticate_user():",
            context_description="Authentication function"
        )
        
        traceability_manager.register_artifact(
            artifact_id="flashcard_1",
            artifact_type="flashcard",
            code_evidence=[evidence]
        )
        
        # Verify traceability
        trace = traceability_manager.get_artifact_trace("flashcard_1")
        assert trace is not None
        assert len(trace.code_locations) > 0
        
        # Verify reverse lookup
        artifacts = traceability_manager.get_artifacts_for_code("auth.py", 1, 5)
        assert len(artifacts) > 0
        assert "flashcard_1" in artifacts
    
    def test_error_handling(self, mock_components):
        """Test error handling in workflow."""
        session_manager = SessionManager()
        
        repo_manager = RepositoryManager(
            repo_analyzer=mock_components['repo_analyzer'],
            max_size_mb=100
        )
        
        # Test invalid repository path
        result = repo_manager.upload_from_folder("/nonexistent/path")
        assert result['success'] is False
        assert 'error' in result
    
    def test_multi_language_artifact_generation(self, sample_repo_path, mock_components):
        """Test artifact generation in multiple languages."""
        from models.intent_models import MultiFileAnalysis, UserIntent, IntentScope
        
        artifact_generator = LearningArtifactGenerator(
            flashcard_manager=mock_components['flashcard_manager'],
            quiz_engine=mock_components['quiz_engine'],
            langchain_orchestrator=mock_components['orchestrator']
        )
        
        # Create sample analysis
        analysis = MultiFileAnalysis(
            file_analyses={},
            relationships=[],
            dependency_graph={},
            data_flows=[],
            execution_paths=[],
            cross_file_patterns=[],
            key_concepts=[
                {
                    'name': 'authenticate_user',
                    'category': 'functions',
                    'description': 'Authenticates user credentials',
                    'file': 'auth.py',
                    'line': 1,
                    'evidence': [{
                        'file_path': 'auth.py',
                        'line_start': 1,
                        'line_end': 5,
                        'context': 'Authentication function'
                    }]
                }
            ]
        )
        
        intent = UserIntent(
            primary_intent="learn_authentication",
            secondary_intents=[],
            scope=IntentScope(scope_type="full_repository"),
            audience_level="intermediate",
            technologies=["Python"],
            confidence_score=0.9
        )
        
        # Test English
        flashcards_en = artifact_generator.generate_flashcards(analysis, intent, "english")
        assert len(flashcards_en) > 0
        assert "What does" in flashcards_en[0].front or "function" in flashcards_en[0].front.lower()
        
        # Test Hindi
        flashcards_hi = artifact_generator.generate_flashcards(analysis, intent, "hindi")
        assert len(flashcards_hi) > 0
        
        # Test Telugu
        flashcards_te = artifact_generator.generate_flashcards(analysis, intent, "telugu")
        assert len(flashcards_te) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
