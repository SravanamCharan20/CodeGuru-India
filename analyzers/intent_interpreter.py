"""
Intent Interpreter for parsing natural language learning goals.

This module interprets user's natural language input to extract structured
learning goals including primary intent, scope, audience level, and technologies.
"""

import logging
import json
from typing import List, Dict, Optional
from models.intent_models import UserIntent, IntentScope

logger = logging.getLogger(__name__)


class IntentInterpreter:
    """Parses natural language user input to extract structured learning goals."""
    
    # Supported intent categories
    INTENT_CATEGORIES = [
        "learn_specific_feature",
        "interview_preparation",
        "architecture_understanding",
        "generate_learning_materials",
        "focus_on_technology",
        "backend_flow_analysis",
        "frontend_flow_analysis"
    ]
    
    # Confidence threshold for ambiguity detection
    CONFIDENCE_THRESHOLD = 0.7
    
    def __init__(self, langchain_orchestrator):
        """
        Initialize with AI orchestrator for NLP.
        
        Args:
            langchain_orchestrator: LangChainOrchestrator instance for AI-powered analysis
        """
        self.orchestrator = langchain_orchestrator
    
    def interpret_intent(self, user_input: str, repo_context) -> UserIntent:
        """
        Parse user input and extract structured intent.
        
        Args:
            user_input: Natural language learning goal statement
            repo_context: RepoAnalysis object with repository information
            
        Returns:
            UserIntent object with extracted information
        """
        try:
            # Build context about repository
            repo_info = self._build_repo_context(repo_context)
            
            # Create prompt for intent extraction
            prompt = self._create_intent_extraction_prompt(user_input, repo_info)
            
            # Get structured output from AI
            output_schema = {
                "primary_intent": "string",
                "secondary_intents": ["string"],
                "scope_type": "string",
                "target_paths": ["string"],
                "exclude_paths": ["string"],
                "audience_level": "string",
                "technologies": ["string"],
                "confidence": "float"
            }
            
            response = self.orchestrator.generate_structured_output(
                prompt=prompt,
                output_schema=output_schema
            )
            
            # Parse response into UserIntent
            intent = self._parse_intent_response(response, user_input)
            
            logger.info(f"Interpreted intent: {intent.primary_intent} (confidence: {intent.confidence_score})")
            return intent
        
        except Exception as e:
            logger.error(f"Intent interpretation failed: {e}")
            # Return default intent
            return self._create_default_intent(user_input)
    
    def generate_clarification_questions(self, intent: UserIntent) -> List[str]:
        """
        Generate questions when intent is ambiguous.
        
        Args:
            intent: UserIntent with low confidence score
            
        Returns:
            List of clarification questions
        """
        questions = []
        
        # Check what's missing or unclear
        if not intent.primary_intent or intent.primary_intent == "unknown":
            questions.append(
                "What is your main learning goal? (e.g., understand a specific feature, "
                "prepare for interviews, learn the architecture)"
            )
        
        if intent.scope and intent.scope.scope_type == "unknown":
            questions.append(
                "Do you want to analyze the entire repository or focus on specific "
                "folders/files/technologies?"
            )
        
        if not intent.technologies:
            questions.append(
                "Are there specific technologies or frameworks you want to focus on?"
            )
        
        if intent.audience_level == "unknown":
            questions.append(
                "What is your experience level? (beginner, intermediate, advanced)"
            )
        
        # If no specific questions, ask general clarification
        if not questions:
            questions.append(
                "Could you provide more details about what you want to learn from this repository?"
            )
        
        return questions
    
    def refine_intent(
        self,
        intent: UserIntent,
        user_responses: Dict[str, str]
    ) -> UserIntent:
        """
        Refine intent based on user's clarification responses.
        
        Args:
            intent: Original UserIntent
            user_responses: Dictionary mapping questions to answers
            
        Returns:
            Refined UserIntent with higher confidence
        """
        try:
            # Combine original input with clarifications
            combined_input = f"""
Original goal: {intent.primary_intent if intent.primary_intent != 'unknown' else 'Not specified'}

Additional clarifications:
{json.dumps(user_responses, indent=2)}
"""
            
            # Re-interpret with additional context
            # Note: We need repo_context here, but for refinement we can use the existing scope
            prompt = f"""Analyze this refined learning goal and extract structured intent:

{combined_input}

Previous interpretation:
- Primary intent: {intent.primary_intent}
- Scope: {intent.scope.scope_type if intent.scope else 'unknown'}
- Audience level: {intent.audience_level}
- Technologies: {', '.join(intent.technologies) if intent.technologies else 'none'}

Based on the clarifications, provide an updated interpretation with higher confidence.

Extract:
1. Primary intent (one of: {', '.join(self.INTENT_CATEGORIES)})
2. Secondary intents
3. Scope (entire_repo, specific_folders, specific_files, technology)
4. Target paths (if specific folders/files)
5. Audience level (beginner, intermediate, advanced)
6. Technologies mentioned
7. Confidence score (0.0-1.0)

Respond in JSON format."""
            
            output_schema = {
                "primary_intent": "string",
                "secondary_intents": ["string"],
                "scope_type": "string",
                "target_paths": ["string"],
                "exclude_paths": ["string"],
                "audience_level": "string",
                "technologies": ["string"],
                "confidence": "float"
            }
            
            response = self.orchestrator.generate_structured_output(
                prompt=prompt,
                output_schema=output_schema
            )
            
            # Parse refined intent
            refined_intent = self._parse_intent_response(response, combined_input)
            
            # Ensure confidence increased
            if refined_intent.confidence_score <= intent.confidence_score:
                refined_intent.confidence_score = min(intent.confidence_score + 0.2, 1.0)
            
            logger.info(f"Refined intent confidence: {intent.confidence_score} -> {refined_intent.confidence_score}")
            return refined_intent
        
        except Exception as e:
            logger.error(f"Intent refinement failed: {e}")
            # Return original intent with slightly higher confidence
            intent.confidence_score = min(intent.confidence_score + 0.1, 1.0)
            return intent
    
    def suggest_intents(self, repo_context) -> List[str]:
        """
        Suggest possible intents based on repository content.
        
        Args:
            repo_context: RepoAnalysis object
            
        Returns:
            List of suggested intent descriptions
        """
        suggestions = []
        
        try:
            repo_info = self._build_repo_context(repo_context)
            
            prompt = f"""Based on this repository structure, suggest 3-5 learning goals a user might have:

Repository Information:
{repo_info}

Provide specific, actionable learning goals that match the repository's content.
For example:
- "Learn how the authentication system works"
- "Understand the React component architecture"
- "Study the database models and relationships"

Respond with a JSON array of suggestion strings."""
            
            response = self.orchestrator.generate_structured_output(
                prompt=prompt,
                output_schema={"suggestions": ["string"]}
            )
            
            if "suggestions" in response:
                suggestions = response["suggestions"][:5]  # Limit to 5
            
        except Exception as e:
            logger.error(f"Intent suggestion failed: {e}")
            # Provide generic suggestions
            suggestions = [
                "Understand the overall architecture",
                "Learn the main features and functionality",
                "Study the code structure and patterns",
                "Prepare for technical interviews"
            ]
        
        return suggestions
    
    # ========================================================================
    # Private Helper Methods
    # ========================================================================
    
    def _build_repo_context(self, repo_context) -> str:
        """Build string representation of repository context."""
        if not repo_context:
            return "No repository context available"
        
        context_parts = []
        
        # Add languages
        if hasattr(repo_context, 'languages') and repo_context.languages:
            langs = ', '.join([f"{lang}: {pct}%" for lang, pct in repo_context.languages.items()])
            context_parts.append(f"Languages: {langs}")
        
        # Add file count
        if hasattr(repo_context, 'total_files'):
            context_parts.append(f"Total files: {repo_context.total_files}")
        
        # Add main files
        if hasattr(repo_context, 'main_files') and repo_context.main_files:
            main_files = ', '.join([f.name for f in repo_context.main_files[:10]])
            context_parts.append(f"Main files: {main_files}")
        
        # Add frameworks detected
        if hasattr(repo_context, 'frameworks') and repo_context.frameworks:
            frameworks = ', '.join(repo_context.frameworks)
            context_parts.append(f"Frameworks: {frameworks}")
        
        return '\n'.join(context_parts) if context_parts else "Repository structure available"
    
    def _create_intent_extraction_prompt(self, user_input: str, repo_info: str) -> str:
        """Create prompt for intent extraction."""
        return f"""Analyze this user's learning goal and extract structured intent:

User Input: "{user_input}"

Repository Context:
{repo_info}

Extract:
1. Primary intent - Choose ONE from: {', '.join(self.INTENT_CATEGORIES)}
2. Secondary intents - Additional goals (if any)
3. Scope type - One of: entire_repo, specific_folders, specific_files, technology
4. Target paths - Specific paths if mentioned (e.g., ["src/auth", "models/"])
5. Exclude paths - Paths to exclude if mentioned
6. Audience level - One of: beginner, intermediate, advanced
7. Technologies - Specific technologies/frameworks mentioned (e.g., ["React", "JWT", "PostgreSQL"])
8. Confidence - How confident you are in this interpretation (0.0-1.0)

Guidelines:
- If user mentions "authentication", "auth", "login" -> likely learn_specific_feature + technologies: ["authentication"]
- If user mentions "interview", "prepare" -> likely interview_preparation
- If user mentions "architecture", "design", "structure" -> likely architecture_understanding
- If user mentions "flashcards", "quiz", "study" -> likely generate_learning_materials
- If user mentions specific tech (React, Django, etc.) -> focus_on_technology
- If user mentions "backend", "API", "database" -> backend_flow_analysis
- If user mentions "frontend", "UI", "components" -> frontend_flow_analysis
- Default audience level is "intermediate" unless specified
- Default scope is "entire_repo" unless specific paths mentioned

Respond in JSON format matching the schema."""
    
    def _parse_intent_response(self, response: Dict, original_input: str) -> UserIntent:
        """Parse AI response into UserIntent object."""
        try:
            # Extract fields with defaults
            primary_intent = response.get("primary_intent", "generate_learning_materials")
            
            # Validate primary intent
            if primary_intent not in self.INTENT_CATEGORIES:
                primary_intent = "generate_learning_materials"
            
            secondary_intents = response.get("secondary_intents", [])
            if not isinstance(secondary_intents, list):
                secondary_intents = []
            
            scope_type = response.get("scope_type", "entire_repo")
            target_paths = response.get("target_paths", [])
            exclude_paths = response.get("exclude_paths", [])
            
            scope = IntentScope(
                scope_type=scope_type,
                target_paths=target_paths if isinstance(target_paths, list) else [],
                exclude_paths=exclude_paths if isinstance(exclude_paths, list) else []
            )
            
            audience_level = response.get("audience_level", "intermediate")
            if audience_level not in ["beginner", "intermediate", "advanced"]:
                audience_level = "intermediate"
            
            technologies = response.get("technologies", [])
            if not isinstance(technologies, list):
                technologies = []
            
            confidence = response.get("confidence", 0.5)
            if not isinstance(confidence, (int, float)):
                confidence = 0.5
            confidence = max(0.0, min(1.0, float(confidence)))
            
            return UserIntent(
                primary_intent=primary_intent,
                secondary_intents=secondary_intents,
                scope=scope,
                audience_level=audience_level,
                technologies=technologies,
                confidence_score=confidence
            )
        
        except Exception as e:
            logger.error(f"Failed to parse intent response: {e}")
            return self._create_default_intent(original_input)
    
    def _create_default_intent(self, user_input: str) -> UserIntent:
        """Create default intent when parsing fails."""
        return UserIntent(
            primary_intent="generate_learning_materials",
            secondary_intents=[],
            scope=IntentScope(scope_type="entire_repo", target_paths=[], exclude_paths=[]),
            audience_level="intermediate",
            technologies=[],
            confidence_score=0.3
        )
