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
            logger.info(f"Interpreting intent from user input: {user_input}")
            
            # Use hybrid approach: rule-based + AI enhancement
            # 1. Start with rule-based parsing (fast, reliable)
            intent = self._parse_intent_rule_based(user_input, repo_context)
            
            # 2. Enhance with AI-based keyword extraction (context-aware)
            if self.orchestrator and repo_context:
                try:
                    ai_keywords = self._extract_keywords_with_ai(user_input, repo_context)
                    # Store AI-extracted keywords in intent for file selector to use
                    if not hasattr(intent, 'ai_keywords'):
                        intent.ai_keywords = ai_keywords
                    logger.info(f"AI extracted {len(ai_keywords)} additional keywords: {ai_keywords[:10]}")
                except Exception as e:
                    logger.warning(f"AI keyword extraction failed, using rule-based only: {e}")
                    intent.ai_keywords = []
            else:
                intent.ai_keywords = []
            
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
            # Combine all responses into one string
            combined_input = " ".join(user_responses.values())
            
            # Re-parse with combined input
            refined_intent = self._parse_intent_rule_based(combined_input, None)
            
            # Merge with original intent (keep non-empty values from original)
            if intent.technologies and not refined_intent.technologies:
                refined_intent.technologies = intent.technologies
            
            if intent.scope and intent.scope.target_paths and not refined_intent.scope.target_paths:
                refined_intent.scope.target_paths = intent.scope.target_paths
            
            # Increase confidence
            refined_intent.confidence_score = min(refined_intent.confidence_score + 0.2, 1.0)
            
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
            # Provide generic but useful suggestions
            suggestions = [
                "Learn how the authentication system works",
                "Understand the overall architecture and design patterns",
                "Study the database models and relationships",
                "Learn the API endpoints and request handling",
                "Understand the frontend components and state management",
                "Prepare for technical interviews on this codebase"
            ]
            
            # Customize based on repo context if available
            if repo_context:
                if hasattr(repo_context, 'frameworks') and repo_context.frameworks:
                    for framework in repo_context.frameworks[:2]:
                        suggestions.insert(0, f"Learn how {framework} is used in this project")
        
        except Exception as e:
            logger.error(f"Intent suggestion failed: {e}")
            suggestions = [
                "Understand the overall architecture",
                "Learn the main features and functionality",
                "Study the code structure and patterns"
            ]
        
        return suggestions[:5]  # Limit to 5
    
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
        intent = UserIntent(
            primary_intent="generate_learning_materials",
            secondary_intents=[],
            scope=IntentScope(scope_type="entire_repo", target_paths=[], exclude_paths=[]),
            audience_level="intermediate",
            technologies=[],
            confidence_score=0.3
        )
        intent.ai_keywords = []
        return intent
    
    def _extract_keywords_with_ai(self, user_input: str, repo_context) -> List[str]:
        """
        Use AI to extract relevant keywords based on user input and repository context.
        
        Args:
            user_input: User's learning goal
            repo_context: Repository analysis with file structure
            
        Returns:
            List of relevant keywords for file matching
        """
        try:
            # Build repository context summary
            repo_info = self._build_repo_context(repo_context)
            
            # Create prompt for AI keyword extraction
            prompt = f"""Analyze this user's learning goal and the repository structure to extract relevant keywords for file matching.

User's Learning Goal: "{user_input}"

Repository Context:
{repo_info}

Task: Extract 10-15 specific keywords that would help identify relevant files in this repository.

Guidelines:
- Focus on technical terms, file names, folder names, and concepts mentioned
- Include variations (e.g., "route" → "router", "routing", "routes")
- Consider the repository's actual structure and technologies
- Be specific to what the user wants to learn
- Include both exact matches and related terms

Example for "learn authentication":
- Keywords: auth, authentication, login, user, password, session, token, jwt, signin, signup

Example for "learn routing":
- Keywords: route, router, routing, navigation, navigate, link, path, page, component

Now extract keywords for: "{user_input}"

Respond with ONLY a comma-separated list of keywords, nothing else.
Example response: route, router, routing, navigation, link, path, page, app"""
            
            # Get AI response
            response = self.orchestrator.generate_completion(prompt, max_tokens=200, temperature=0.3)
            
            # Parse keywords from response
            keywords = []
            # Clean up response - remove any extra text
            response = response.strip()
            
            # Try to extract just the keyword list
            lines = response.split('\n')
            for line in lines:
                line = line.strip()
                # Skip empty lines and lines that look like explanations
                if not line or line.startswith('#') or line.startswith('-') or len(line) > 200:
                    continue
                # This line likely contains keywords
                if ',' in line:
                    # Split by comma and clean
                    parts = [p.strip().lower() for p in line.split(',')]
                    keywords.extend([p for p in parts if p and len(p) > 1 and len(p) < 30])
                    break
            
            # Fallback: if no keywords extracted, try splitting the whole response
            if not keywords:
                words = response.lower().replace(',', ' ').replace('.', ' ').split()
                keywords = [w.strip() for w in words if len(w) > 2 and len(w) < 20][:15]
            
            logger.info(f"AI extracted keywords: {keywords}")
            return keywords[:15]  # Limit to 15 keywords
        
        except Exception as e:
            logger.error(f"AI keyword extraction failed: {e}")
            return []
    
    def _parse_intent_rule_based(self, user_input: str, repo_context) -> UserIntent:
        """
        Parse intent using rule-based approach (no AI needed).
        
        Args:
            user_input: User's learning goal
            repo_context: Repository context
            
        Returns:
            UserIntent object
        """
        user_input_lower = user_input.lower()
        
        # Detect primary intent based on keywords
        primary_intent = "generate_learning_materials"  # default
        confidence = 0.7
        
        if any(word in user_input_lower for word in ["authentication", "auth", "login", "signup", "register", "password"]):
            primary_intent = "learn_specific_feature"
            confidence = 0.9
        elif any(word in user_input_lower for word in ["routing", "route", "router", "navigation"]):
            primary_intent = "learn_specific_feature"
            confidence = 0.9
        elif any(word in user_input_lower for word in ["interview", "prepare", "preparation"]):
            primary_intent = "interview_preparation"
            confidence = 0.9
        elif any(word in user_input_lower for word in ["architecture", "design", "structure", "pattern"]):
            primary_intent = "architecture_understanding"
            confidence = 0.9
        elif any(word in user_input_lower for word in ["backend", "api", "database", "server"]):
            primary_intent = "backend_flow_analysis"
            confidence = 0.8
        elif any(word in user_input_lower for word in ["frontend", "ui", "component", "react", "vue"]):
            primary_intent = "frontend_flow_analysis"
            confidence = 0.8
        elif any(word in user_input_lower for word in ["flashcard", "quiz", "study", "learn", "understand"]):
            primary_intent = "generate_learning_materials"
            confidence = 0.8
        
        # Detect technologies
        technologies = []
        tech_keywords = {
            "react": "React",
            "vue": "Vue",
            "angular": "Angular",
            "node": "Node.js",
            "express": "Express",
            "django": "Django",
            "flask": "Flask",
            "fastapi": "FastAPI",
            "spring": "Spring",
            "jwt": "JWT",
            "oauth": "OAuth",
            "postgres": "PostgreSQL",
            "mysql": "MySQL",
            "mongodb": "MongoDB",
            "redis": "Redis",
            "docker": "Docker",
            "kubernetes": "Kubernetes",
            "aws": "AWS",
            "azure": "Azure",
            "gcp": "Google Cloud"
        }
        
        for keyword, tech_name in tech_keywords.items():
            if keyword in user_input_lower:
                technologies.append(tech_name)
        
        # Detect audience level
        audience_level = "intermediate"  # default
        if any(word in user_input_lower for word in ["beginner", "new", "basic", "simple"]):
            audience_level = "beginner"
        elif any(word in user_input_lower for word in ["advanced", "expert", "deep", "detailed"]):
            audience_level = "advanced"
        
        # Detect scope
        scope_type = "entire_repo"
        target_paths = []
        
        # Look for specific paths or folders mentioned
        if "src/" in user_input_lower or "source/" in user_input_lower:
            scope_type = "specific_folders"
            target_paths.append("src")
        if "models/" in user_input_lower or "model/" in user_input_lower:
            scope_type = "specific_folders"
            target_paths.append("models")
        if "controllers/" in user_input_lower or "controller/" in user_input_lower:
            scope_type = "specific_folders"
            target_paths.append("controllers")
        if "views/" in user_input_lower or "view/" in user_input_lower:
            scope_type = "specific_folders"
            target_paths.append("views")
        if "components/" in user_input_lower or "component/" in user_input_lower:
            scope_type = "specific_folders"
            target_paths.append("components")
        
        # If technologies detected, might be technology-focused
        if technologies and not target_paths:
            scope_type = "technology"
        
        scope = IntentScope(
            scope_type=scope_type,
            target_paths=target_paths,
            exclude_paths=[]
        )
        
        return UserIntent(
            primary_intent=primary_intent,
            secondary_intents=[],
            scope=scope,
            audience_level=audience_level,
            technologies=technologies,
            confidence_score=confidence
        )
