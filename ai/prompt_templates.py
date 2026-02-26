"""Prompt templates for different AI tasks."""
from typing import Dict


class PromptManager:
    """Manages prompt templates for different tasks and languages."""
    
    def __init__(self):
        """Initialize prompt manager with templates."""
        self.language_instructions = {
            "english": "Respond in English.",
            "hindi": "Respond in Hindi (हिंदी में जवाब दें).",
            "telugu": "Respond in Telugu (తెలుగులో సమాధానం ఇవ్వండి)."
        }
    
    def get_code_explanation_prompt(
        self, 
        code: str, 
        language: str, 
        difficulty: str = "intermediate"
    ) -> str:
        """Get prompt for code explanation."""
        lang_instruction = self.language_instructions.get(language, self.language_instructions["english"])
        
        difficulty_context = {
            "beginner": "Explain in very simple terms, as if teaching someone new to programming.",
            "intermediate": "Provide a balanced explanation with technical details and examples.",
            "advanced": "Give an in-depth technical explanation with advanced concepts."
        }
        
        context = difficulty_context.get(difficulty.lower(), difficulty_context["intermediate"])
        
        return f"""You are CodeGuru India, an AI assistant helping Indian developers learn code.

{lang_instruction}

Analyze and explain the following code:

```
{code}
```

{context}

Provide:
1. A clear summary of what the code does
2. Key concepts and patterns used
3. At least one culturally relevant analogy (like chai stalls, cricket, Indian railways, etc.)
4. Code examples if helpful
5. Any potential issues or improvements

Make it engaging and easy to understand!"""
    
    def get_analogy_generation_prompt(self, concept: str, language: str) -> str:
        """Get prompt for analogy generation with cultural context."""
        lang_instruction = self.language_instructions.get(language, self.language_instructions["english"])
        
        return f"""You are CodeGuru India, creating relatable analogies for Indian developers.

{lang_instruction}

Create a simple, culturally relevant analogy to explain this programming concept: {concept}

Use examples from Indian daily life such as:
- Chai stalls and street food
- Cricket and sports
- Indian railways and transportation
- Bollywood and entertainment
- Indian festivals and traditions
- Local markets and shopping

Make it memorable and easy to understand!"""
    
    def get_quiz_generation_prompt(
        self,
        topic: str,
        difficulty: str,
        num_questions: int,
        language: str
    ) -> str:
        """Get prompt for quiz generation."""
        lang_instruction = self.language_instructions.get(language, self.language_instructions["english"])
        
        return f"""You are CodeGuru India, creating educational quizzes for developers.

{lang_instruction}

Generate {num_questions} quiz questions about: {topic}
Difficulty level: {difficulty}

For each question, provide:
1. Question text
2. Question type (multiple_choice, code_completion, or debugging)
3. Options (for multiple choice)
4. Correct answer
5. Detailed explanation

Make questions practical and relevant to real-world coding scenarios.
Include examples from popular Indian tech stacks (React, Node.js, AWS, MongoDB).

Format as JSON array."""
    
    def get_debugging_prompt(self, code: str, language: str) -> str:
        """Get prompt for debugging assistance."""
        lang_instruction = self.language_instructions.get(language, self.language_instructions["english"])
        
        return f"""You are CodeGuru India, helping developers debug their code.

{lang_instruction}

Analyze this code for potential issues:

```
{code}
```

Identify:
1. Critical errors (syntax errors, runtime errors, security issues)
2. Warnings (potential bugs, anti-patterns, performance issues)
3. Suggestions (code improvements, best practices)

For each issue, provide:
- Severity level (critical, warning, suggestion)
- Line number (if applicable)
- Clear description
- Specific fix suggestion
- Why it matters

Be thorough but friendly in your explanations!"""
    
    def get_summary_prompt(self, code: str, language: str) -> str:
        """Get prompt for code summarization."""
        lang_instruction = self.language_instructions.get(language, self.language_instructions["english"])
        
        return f"""You are CodeGuru India, summarizing code for developers.

{lang_instruction}

Provide a concise summary of this code:

```
{code}
```

Include:
1. Main purpose and functionality (2-3 sentences)
2. Key functions and classes
3. Technologies/frameworks used
4. Overall architecture pattern (if applicable)

Keep it brief but informative!"""
    
    def get_flashcard_generation_prompt(
        self,
        code_concepts: list,
        language: str
    ) -> str:
        """Get prompt for flashcard generation."""
        lang_instruction = self.language_instructions.get(language, self.language_instructions["english"])
        
        concepts_text = "\n".join([f"- {concept}" for concept in code_concepts])
        
        return f"""You are CodeGuru India, creating learning flashcards.

{lang_instruction}

Create flashcards for these programming concepts:
{concepts_text}

For each flashcard, provide:
1. Front: A clear question or concept name
2. Back: A concise, memorable answer or explanation
3. Topic category
4. Difficulty level (beginner, intermediate, advanced)

Make them perfect for quick review and spaced repetition learning!

Format as JSON array."""
    
    def get_learning_path_prompt(
        self,
        path_name: str,
        current_level: str,
        language: str
    ) -> str:
        """Get prompt for learning path recommendations."""
        lang_instruction = self.language_instructions.get(language, self.language_instructions["english"])
        
        return f"""You are CodeGuru India, guiding developers through learning paths.

{lang_instruction}

Learning Path: {path_name}
Current Level: {current_level}

Recommend the next topic to learn, considering:
1. Prerequisites already completed
2. Logical progression
3. Practical relevance for Indian tech industry
4. Popular tech stacks (MERN, AWS, etc.)

Provide:
- Next topic name
- Why it's important
- What they'll learn
- Estimated time to complete
- Resources or tips"""
    
    def get_framework_specific_prompt(
        self,
        code: str,
        framework: str,
        language: str
    ) -> str:
        """Get framework-specific insights prompt."""
        lang_instruction = self.language_instructions.get(language, self.language_instructions["english"])
        
        framework_contexts = {
            "react": "Focus on React best practices, hooks, component patterns, and performance optimization.",
            "nodejs": "Focus on Node.js patterns, async/await, error handling, and API design.",
            "express": "Focus on Express middleware, routing, error handling, and security.",
            "mongodb": "Focus on MongoDB schema design, queries, indexing, and performance.",
            "aws": "Focus on AWS services, serverless patterns, security, and cost optimization."
        }
        
        context = framework_contexts.get(framework.lower(), "Focus on best practices and common patterns.")
        
        return f"""You are CodeGuru India, providing framework-specific insights.

{lang_instruction}

Analyze this {framework} code:

```
{code}
```

{context}

Provide:
1. Framework-specific best practices
2. Common patterns used
3. Potential improvements
4. Security considerations
5. Performance tips
6. Relevance to Indian tech industry (e-commerce, fintech, etc.)

Include practical examples!"""
