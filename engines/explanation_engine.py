"""Explanation engine for generating code explanations with analogies."""
from dataclasses import dataclass
from typing import List
from ai.langchain_orchestrator import LangChainOrchestrator
import logging

logger = logging.getLogger(__name__)


@dataclass
class CodeExample:
    """Represents a code example."""
    description: str
    code: str
    output: str


@dataclass
class Explanation:
    """Complete code explanation."""
    summary: str
    detailed_explanation: str
    analogies: List[str]
    examples: List[CodeExample]
    key_concepts: List[str]


class ExplanationEngine:
    """Generates code explanations with analogies using LLM."""
    
    def __init__(self, langchain_orchestrator: LangChainOrchestrator):
        """Initialize with LangChain orchestrator."""
        self.orchestrator = langchain_orchestrator
    
    def explain_code(
        self,
        code: str,
        context: str = "",
        language: str = "english",
        difficulty: str = "intermediate"
    ) -> Explanation:
        """
        Generate explanation for code snippet.
        
        Args:
            code: Code to explain
            context: Additional context
            language: Output language
            difficulty: Explanation difficulty level
            
        Returns:
            Complete explanation
        """
        try:
            # Generate main explanation
            explanation_text = self.orchestrator.explain_code(
                code=code,
                language=language,
                difficulty=difficulty
            )
            
            # Extract key concepts (simplified)
            key_concepts = self._extract_key_concepts(code)
            
            # Generate analogy
            if key_concepts:
                analogy = self.generate_analogy(key_concepts[0], language)
            else:
                analogy = "No specific analogy generated"
            
            # Create examples (simplified)
            examples = self._generate_examples(code)
            
            return Explanation(
                summary=explanation_text[:200] + "..." if len(explanation_text) > 200 else explanation_text,
                detailed_explanation=explanation_text,
                analogies=[analogy],
                examples=examples,
                key_concepts=key_concepts
            )
        
        except Exception as e:
            logger.error(f"Explanation generation failed: {e}")
            return self._get_fallback_explanation(code)
    
    def generate_analogy(self, concept: str, language: str = "english") -> str:
        """
        Generate culturally relevant analogy for concept.
        
        Args:
            concept: Programming concept
            language: Output language
            
        Returns:
            Analogy explanation
        """
        try:
            return self.orchestrator.generate_analogy(concept, language)
        except Exception as e:
            logger.error(f"Analogy generation failed: {e}")
            return f"Think of {concept} like organizing items in a chai stall - everything has its place!"
    
    def simplify_explanation(
        self,
        explanation: str,
        language: str = "english"
    ) -> str:
        """
        Simplify existing explanation to more basic level.
        
        Args:
            explanation: Original explanation
            language: Output language
            
        Returns:
            Simplified explanation
        """
        try:
            prompt = f"""Simplify this explanation for a beginner:

{explanation}

Make it very simple and easy to understand, using everyday language."""
            
            return self.orchestrator.generate_completion(prompt)
        except Exception as e:
            logger.error(f"Simplification failed: {e}")
            return "Simplified version: " + explanation[:100] + "..."
    
    def explain_with_examples(
        self,
        code: str,
        language: str = "english"
    ) -> Explanation:
        """
        Generate explanation with code examples.
        
        Args:
            code: Code to explain
            language: Output language
            
        Returns:
            Explanation with examples
        """
        return self.explain_code(code, "", language, "intermediate")
    
    def _extract_key_concepts(self, code: str) -> List[str]:
        """Extract key programming concepts from code."""
        concepts = []
        
        # Simple keyword-based extraction
        if "class " in code:
            concepts.append("Object-Oriented Programming")
        if "def " in code or "function " in code:
            concepts.append("Functions")
        if "async " in code or "await " in code:
            concepts.append("Asynchronous Programming")
        if "try:" in code or "except" in code:
            concepts.append("Error Handling")
        if "import " in code:
            concepts.append("Modules and Imports")
        if "for " in code or "while " in code:
            concepts.append("Loops")
        if "if " in code:
            concepts.append("Conditional Logic")
        
        return concepts[:5]  # Limit to 5 concepts
    
    def _generate_examples(self, code: str) -> List[CodeExample]:
        """Generate simple code examples."""
        examples = []
        
        # Add a basic example
        if "def " in code:
            examples.append(CodeExample(
                description="Basic function usage",
                code="# Call the function\nresult = function_name(arg1, arg2)",
                output="# Returns the computed result"
            ))
        
        return examples
    
    def _get_fallback_explanation(self, code: str) -> Explanation:
        """Generate fallback explanation when AI fails."""
        return Explanation(
            summary="This code performs specific operations. Enable AWS Bedrock for detailed AI analysis.",
            detailed_explanation=f"Code analysis:\n\n{code[:200]}...\n\nConfigure AWS credentials for full AI-powered explanations.",
            analogies=["Think of code like a recipe - each line is a step to achieve the final result!"],
            examples=[],
            key_concepts=self._extract_key_concepts(code)
        )
