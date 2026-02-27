"""
Session Persistence Tests.

Tests session state management and persistence.
"""

import pytest
from session_manager import SessionManager
from models.intent_models import UserIntent, IntentScope


class TestSessionPersistence:
    """Test session state persistence."""
    
    @pytest.fixture
    def session_manager(self):
        """Create session manager instance."""
        return SessionManager()
    
    def test_repository_storage_and_retrieval(self, session_manager):
        """Test storing and retrieving repository data."""
        # Store repository
        session_manager.set_current_repository(
            repo_path="/test/repo",
            repo_analysis={'languages': ['Python'], 'file_count': 10}
        )
        
        # Retrieve repository
        repo_data = session_manager.get_current_repository()
        assert repo_data is not None
        assert repo_data['repo_path'] == "/test/repo"
        assert repo_data['repo_analysis']['languages'] == ['Python']
    
    def test_intent_storage_and_retrieval(self, session_manager):
        """Test storing and retrieving intent data."""
        # Create intent
        intent = UserIntent(
            primary_intent="learn_authentication",
            secondary_intents=["security", "best_practices"],
            scope=IntentScope(scope_type="full_repository"),
            audience_level="intermediate",
            technologies=["Python", "Flask"],
            confidence_score=0.85
        )
        
        # Store intent
        session_manager.set_current_intent(intent)
        
        # Retrieve intent
        intent_data = session_manager.get_current_intent()
        assert intent_data is not None
        assert intent_data['intent'].primary_intent == "learn_authentication"
        assert intent_data['intent'].confidence_score == 0.85
    
    def test_learning_artifacts_storage(self, session_manager):
        """Test storing learning artifacts."""
        from models.intent_models import CodeFlashcard, CodeEvidence
        
        # Create sample flashcard
        flashcard = CodeFlashcard(
            id="test_1",
            front="What is authentication?",
            back="Process of verifying user identity",
            topic="Security",
            difficulty="beginner",
            code_evidence=[
                CodeEvidence(
                    file_path="auth.py",
                    line_start=1,
                    line_end=5,
                    code_snippet="def authenticate():",
                    context_description="Auth function"
                )
            ],
            concept_category="functions"
        )
        
        # Store artifacts
        session_manager.set_learning_artifacts(
            flashcards=[flashcard],
            quizzes=[],
            learning_paths=[],
            concept_summary={}
        )
        
        # Retrieve artifacts
        artifacts = session_manager.get_learning_artifacts()
        assert artifacts is not None
        assert len(artifacts['flashcards']) == 1
        assert artifacts['flashcards'][0].id == "test_1"
    
    def test_analysis_history(self, session_manager):
        """Test analysis history tracking."""
        # Add to history
        session_manager.add_to_analysis_history(
            intent="learn_authentication",
            files_analyzed=["auth.py", "user.py"],
            artifacts_generated=15
        )
        
        session_manager.add_to_analysis_history(
            intent="understand_architecture",
            files_analyzed=["main.py", "config.py"],
            artifacts_generated=20
        )
        
        # Retrieve history
        history = session_manager.get_analysis_history()
        assert len(history) == 2
        assert history[0]['intent'] == "learn_authentication"
        assert history[1]['intent'] == "understand_architecture"
    
    def test_multi_analysis_coexistence(self, session_manager):
        """Test multiple analyses can coexist."""
        # First analysis
        session_manager.set_current_repository(
            repo_path="/repo1",
            repo_analysis={'languages': ['Python']}
        )
        
        intent1 = UserIntent(
            primary_intent="learn_auth",
            secondary_intents=[],
            scope=IntentScope(scope_type="full_repository"),
            audience_level="beginner",
            technologies=["Python"],
            confidence_score=0.8
        )
        session_manager.set_current_intent(intent1)
        
        session_manager.add_to_analysis_history(
            intent="learn_auth",
            files_analyzed=["auth.py"],
            artifacts_generated=10
        )
        
        # Second analysis
        session_manager.set_current_repository(
            repo_path="/repo2",
            repo_analysis={'languages': ['JavaScript']}
        )
        
        intent2 = UserIntent(
            primary_intent="learn_react",
            secondary_intents=[],
            scope=IntentScope(scope_type="full_repository"),
            audience_level="intermediate",
            technologies=["JavaScript", "React"],
            confidence_score=0.9
        )
        session_manager.set_current_intent(intent2)
        
        session_manager.add_to_analysis_history(
            intent="learn_react",
            files_analyzed=["App.js"],
            artifacts_generated=15
        )
        
        # Verify both exist in history
        history = session_manager.get_analysis_history()
        assert len(history) == 2
    
    def test_session_clear(self, session_manager):
        """Test clearing session data."""
        # Add data
        session_manager.set_current_repository(
            repo_path="/test",
            repo_analysis={}
        )
        
        # Clear
        session_manager.clear_current_analysis()
        
        # Verify cleared
        repo_data = session_manager.get_current_repository()
        # Should be None or empty after clear
        assert repo_data is None or not repo_data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
