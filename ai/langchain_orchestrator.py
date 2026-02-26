"""LangChain orchestration for LLM interactions."""
import json
import logging
from typing import Dict, Optional
from ai.bedrock_client import BedrockClient
from ai.prompt_templates import PromptManager

logger = logging.getLogger(__name__)


class LangChainOrchestrator:
    """Orchestrates LLM calls using LangChain and AWS Bedrock."""
    
    def __init__(self, bedrock_client: BedrockClient, prompt_manager: PromptManager):
        """Initialize with Bedrock client and prompt manager."""
        self.bedrock_client = bedrock_client
        self.prompt_manager = prompt_manager
    
    def generate_completion(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> str:
        """
        Generate completion from LLM.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated text
        """
        try:
            parameters = {
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            response = self.bedrock_client.invoke_model(
                prompt=prompt,
                parameters=parameters
            )
            
            return response
        
        except Exception as e:
            logger.error(f"Completion generation failed: {e}")
            return f"Error generating response: {str(e)}"
    
    def generate_with_chain(
        self,
        chain_type: str,
        inputs: Dict
    ) -> str:
        """
        Execute a LangChain chain with inputs.
        
        Args:
            chain_type: Type of chain to execute
            inputs: Input parameters for the chain
            
        Returns:
            Chain output
        """
        try:
            if chain_type == "code_explanation":
                prompt = self.prompt_manager.get_code_explanation_prompt(
                    code=inputs.get("code", ""),
                    language=inputs.get("language", "english"),
                    difficulty=inputs.get("difficulty", "intermediate")
                )
            
            elif chain_type == "analogy_generation":
                prompt = self.prompt_manager.get_analogy_generation_prompt(
                    concept=inputs.get("concept", ""),
                    language=inputs.get("language", "english")
                )
            
            elif chain_type == "debugging":
                prompt = self.prompt_manager.get_debugging_prompt(
                    code=inputs.get("code", ""),
                    language=inputs.get("language", "english")
                )
            
            elif chain_type == "summary":
                prompt = self.prompt_manager.get_summary_prompt(
                    code=inputs.get("code", ""),
                    language=inputs.get("language", "english")
                )
            
            elif chain_type == "quiz_generation":
                prompt = self.prompt_manager.get_quiz_generation_prompt(
                    topic=inputs.get("topic", ""),
                    difficulty=inputs.get("difficulty", "intermediate"),
                    num_questions=inputs.get("num_questions", 5),
                    language=inputs.get("language", "english")
                )
            
            elif chain_type == "flashcard_generation":
                prompt = self.prompt_manager.get_flashcard_generation_prompt(
                    code_concepts=inputs.get("concepts", []),
                    language=inputs.get("language", "english")
                )
            
            elif chain_type == "learning_path":
                prompt = self.prompt_manager.get_learning_path_prompt(
                    path_name=inputs.get("path_name", ""),
                    current_level=inputs.get("current_level", "beginner"),
                    language=inputs.get("language", "english")
                )
            
            elif chain_type == "framework_specific":
                prompt = self.prompt_manager.get_framework_specific_prompt(
                    code=inputs.get("code", ""),
                    framework=inputs.get("framework", ""),
                    language=inputs.get("language", "english")
                )
            
            else:
                return f"Unknown chain type: {chain_type}"
            
            return self.generate_completion(prompt)
        
        except Exception as e:
            logger.error(f"Chain execution failed: {e}")
            return f"Error executing chain: {str(e)}"
    
    def generate_structured_output(
        self,
        prompt: str,
        output_schema: Dict
    ) -> Dict:
        """
        Generate structured output matching schema.
        
        Args:
            prompt: Input prompt
            output_schema: Expected output schema
            
        Returns:
            Structured output as dictionary
        """
        try:
            # Add schema instructions to prompt
            schema_prompt = f"""{prompt}

IMPORTANT: Respond with valid JSON matching this schema:
{json.dumps(output_schema, indent=2)}

Ensure your response is valid JSON that can be parsed."""
            
            response = self.generate_completion(schema_prompt)
            
            # Try to extract JSON from response
            try:
                # Look for JSON in response
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                
                if start_idx != -1 and end_idx > start_idx:
                    json_str = response[start_idx:end_idx]
                    return json.loads(json_str)
                else:
                    # Try parsing entire response
                    return json.loads(response)
            
            except json.JSONDecodeError:
                logger.warning("Failed to parse JSON from response, returning raw text")
                return {"raw_response": response}
        
        except Exception as e:
            logger.error(f"Structured output generation failed: {e}")
            return {"error": str(e)}
    
    def explain_code(
        self,
        code: str,
        language: str = "english",
        difficulty: str = "intermediate"
    ) -> str:
        """
        Generate code explanation.
        
        Args:
            code: Code to explain
            language: Output language
            difficulty: Explanation difficulty level
            
        Returns:
            Code explanation
        """
        return self.generate_with_chain(
            chain_type="code_explanation",
            inputs={
                "code": code,
                "language": language,
                "difficulty": difficulty
            }
        )
    
    def debug_code(
        self,
        code: str,
        language: str = "english"
    ) -> str:
        """
        Analyze code for issues.
        
        Args:
            code: Code to debug
            language: Output language
            
        Returns:
            Debugging analysis
        """
        return self.generate_with_chain(
            chain_type="debugging",
            inputs={
                "code": code,
                "language": language
            }
        )
    
    def summarize_code(
        self,
        code: str,
        language: str = "english"
    ) -> str:
        """
        Generate code summary.
        
        Args:
            code: Code to summarize
            language: Output language
            
        Returns:
            Code summary
        """
        return self.generate_with_chain(
            chain_type="summary",
            inputs={
                "code": code,
                "language": language
            }
        )
    
    def generate_analogy(
        self,
        concept: str,
        language: str = "english"
    ) -> str:
        """
        Generate culturally relevant analogy.
        
        Args:
            concept: Programming concept
            language: Output language
            
        Returns:
            Analogy explanation
        """
        return self.generate_with_chain(
            chain_type="analogy_generation",
            inputs={
                "concept": concept,
                "language": language
            }
        )
