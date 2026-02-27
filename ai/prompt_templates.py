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
        language: str,
        code_context: str = ""
    ) -> str:
        """Get prompt for quiz generation."""
        lang_instruction = self.language_instructions.get(language, self.language_instructions["english"])
        
        code_section = ""
        if code_context:
            code_section = f"\nBase questions on this code context:\n```\n{code_context}\n```\n"
        
        return f"""You are CodeGuru India, creating educational quizzes for developers.

{lang_instruction}

Generate {num_questions} quiz questions about: {topic}
Difficulty level: {difficulty}
{code_section}

For each question, provide:
1. Question text (in {language})
2. Question type (multiple_choice, code_completion, or debugging)
3. Options (for multiple choice) - 4 options
4. Correct answer
5. Detailed explanation (why the answer is correct and others are wrong)

IMPORTANT:
- Keep all code snippets in their original programming language
- Questions must be grounded in the actual code provided
- Make questions practical and relevant to real-world coding scenarios
- Include culturally relevant examples when helpful

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
        language: str,
        difficulty: str = "intermediate"
    ) -> str:
        """Get prompt for flashcard generation."""
        lang_instruction = self.language_instructions.get(language, self.language_instructions["english"])
        
        concepts_text = "\n".join([f"- {concept}" for concept in code_concepts])
        
        difficulty_note = {
            "beginner": "Use simple language and basic examples.",
            "intermediate": "Include technical details with clear explanations.",
            "advanced": "Use advanced terminology and in-depth concepts."
        }.get(difficulty.lower(), "")
        
        return f"""You are CodeGuru India, creating learning flashcards.

{lang_instruction}

Create flashcards for these programming concepts:
{concepts_text}

Difficulty level: {difficulty}
{difficulty_note}

For each flashcard, provide:
1. Front: A clear question or concept name
2. Back: A concise, memorable answer or explanation (2-3 sentences max)
3. Include culturally relevant analogies when helpful
4. Keep code snippets in original language

Make them perfect for quick review and spaced repetition learning!

Format as JSON array."""
    
    def get_learning_path_prompt(
        self,
        path_name: str,
        current_level: str,
        language: str,
        concepts: list = None
    ) -> str:
        """Get prompt for learning path recommendations."""
        lang_instruction = self.language_instructions.get(language, self.language_instructions["english"])
        
        concepts_section = ""
        if concepts:
            concepts_section = f"\nConcepts to cover:\n" + "\n".join([f"- {c}" for c in concepts])
        
        return f"""You are CodeGuru India, guiding developers through learning paths.

{lang_instruction}

Learning Path: {path_name}
Current Level: {current_level}
{concepts_section}

Create a structured learning path with ordered steps, considering:
1. Prerequisites and logical progression (foundational to advanced)
2. Dependencies between concepts
3. Practical relevance for Indian tech industry
4. Estimated time for each step

For each step, provide:
- Step title (in {language})
- Description of what will be learned
- Estimated time in minutes
- Concepts covered
- Prerequisites (previous step IDs)

IMPORTANT:
- Keep code examples in original programming language
- Order steps from basic to advanced
- Each step should build on previous ones

Format as JSON array of steps."""
    
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
    
    def get_concept_summary_prompt(
        self,
        concepts: list,
        language: str,
        intent: str = ""
    ) -> str:
        """Get prompt for concept summary generation."""
        lang_instruction = self.language_instructions.get(language, self.language_instructions["english"])
        
        concepts_text = "\n".join([f"- {c.get('name', 'Unknown')}: {c.get('description', '')}" for c in concepts])
        
        intent_section = ""
        if intent:
            intent_section = f"\nUser's learning goal: {intent}\nPrioritize concepts most relevant to this goal."
        
        return f"""You are CodeGuru India, summarizing code concepts for developers.

{lang_instruction}

Organize and summarize these programming concepts:
{concepts_text}
{intent_section}

Provide:
1. Categorized summary (group by: architecture, patterns, data_structures, algorithms, functions, classes)
2. Top 5 most important concepts with brief explanations
3. How concepts relate to each other
4. Practical applications in real projects

IMPORTANT:
- Keep code references in original programming language
- Focus only on concepts demonstrated in the actual code
- Exclude generic concepts not shown in the code
- Use culturally relevant analogies when helpful

Format as structured JSON."""
