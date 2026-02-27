"""
AI Integration Tests.

Tests LangChain orchestrator integration with all components.
"""

import pytest
from unittest.mock import Mock, patch
from ai.langchain_orchestrator import LangChainOrchestrator
from ai.prompt_templates import PromptManager


class TestAIIntegration:
    """Test AI service integration."""
    
    @pytest.fixture
    def mock_bedrock_client(self):
        """Create mock Bedrock client."""
        mock_client = Mock()
        mock_client.invoke_model = Mock(return_value="Mocked AI response")
        return mock_client
    
    @pytest.fixture
    def orchestrator(self, mock_bedrock_client):
        """Create orchestrator with mock client."""
        prompt_manager = PromptManager()
        return LangChainOrchestrator(mock_bedrock_client, prompt_manager)
    
    def test_code_explanation_generation(self, orchestrator):
        """Test code explanation generation."""
        code = "def hello(): return 'world'"
        
        result = orchestrator.explain_code(code, language="english")
        assert result is not None
        assert isinstance(result, str)
    
    def test_multi_language_support(self, orchestrator):
        """Test multi-language prompt generation."""
        code = "def test(): pass"
        
        # Test English
        result_en = orchestrator.explain_code(code, language="english")
        assert result_en is not None
        
        # Test Hindi
        result_hi = orchestrator.explain_code(code, language="hindi")
        assert result_hi is not None
        
        # Test Telugu
        result_te = orchestrator.explain_code(code, language="telugu")
        assert result_te is not None
    
    def test_retry_logic_on_failure(self, mock_bedrock_client):
        """Test retry logic when AI service fails."""
        # Simulate failure then success
        mock_bedrock_client.invoke_model = Mock(
            side_effect=[Exception("Service unavailable"), "Success"]
        )
        
        prompt_manager = PromptManager()
        orchestrator = LangChainOrchestrator(mock_bedrock_client, prompt_manager)
        
        # Should handle error gracefully
        result = orchestrator.generate_completion("test prompt")
        assert result is not None
    
    def test_fallback_generation_when_ai_fails(self):
        """Test fallback artifact generation when AI fails."""
        from generators.learning_artifact_generator import LearningArtifactGenerator
        from models.intent_models import MultiFileAnalysis
        
        # Create generator with failing orchestrator
        mock_orchestrator = Mock()
        mock_orchestrator.generate_with_chain = Mock(side_effect=Exception("AI failed"))
        
        generator = LearningArtifactGenerator(
            flashcard_manager=Mock(),
            quiz_engine=Mock(),
            langchain_orchestrator=mock_orchestrator
        )
        
        # Create sample analysis
        analysis = MultiFileAnalysis(
            file_analyses={},
            relationships=[],
            dependency_graph={},
            data_flows=[],
            execution_paths=[],
            cross_file_patterns=[],
            key_concepts=[]
        )
        
        # Should use fallback generation
        flashcards = generator.generate_basic_flashcards(analysis)
        assert isinstance(flashcards, list)
    
    def test_prompt_template_generation(self):
        """Test prompt template generation for different tasks."""
        prompt_manager = PromptManager()
        
        # Test flashcard prompt
        flashcard_prompt = prompt_manager.get_flashcard_generation_prompt(
            code_concepts=["function", "class"],
            language="english",
            difficulty="intermediate"
        )
        assert "flashcard" in flashcard_prompt.lower()
        assert "english" in flashcard_prompt.lower()
        
        # Test quiz prompt
        quiz_prompt = prompt_manager.get_quiz_generation_prompt(
            topic="authentication",
            difficulty="intermediate",
            num_questions=5,
            language="hindi"
        )
        assert "quiz" in quiz_prompt.lower() or "प्रश्न" in quiz_prompt.lower()
        
        # Test learning path prompt
        path_prompt = prompt_manager.get_learning_path_prompt(
            path_name="Authentication",
            current_level="beginner",
            language="telugu"
        )
        assert "learning" in path_prompt.lower() or "నేర్చుకునే" in path_prompt.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
