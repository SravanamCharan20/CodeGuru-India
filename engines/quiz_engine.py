"""Quiz engine for generating and evaluating quizzes."""
from dataclasses import dataclass
from typing import List, Optional
from ai.langchain_orchestrator import LangChainOrchestrator
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class Question:
    """Represents a quiz question."""
    id: str
    type: str  # "multiple_choice", "code_completion", "debugging"
    question_text: str
    options: Optional[List[str]]
    correct_answer: str
    explanation: str


@dataclass
class Quiz:
    """Represents a complete quiz."""
    id: str
    topic: str
    questions: List[Question]
    time_limit_minutes: int


@dataclass
class EvaluationResult:
    """Result of answer evaluation."""
    is_correct: bool
    score: float
    feedback: str
    explanation: str


class QuizEngine:
    """Generates and evaluates quizzes based on code and topics."""
    
    def __init__(self, langchain_orchestrator: LangChainOrchestrator):
        """Initialize with LangChain orchestrator."""
        self.orchestrator = langchain_orchestrator
    
    def generate_quiz(
        self,
        topic: str,
        difficulty: str,
        num_questions: int,
        language: str = "english"
    ) -> Quiz:
        """
        Generate a quiz for a topic.
        
        Args:
            topic: Quiz topic
            difficulty: Difficulty level
            num_questions: Number of questions
            language: Output language
            
        Returns:
            Generated quiz
        """
        try:
            # Generate quiz using AI
            response = self.orchestrator.generate_with_chain(
                chain_type="quiz_generation",
                inputs={
                    "topic": topic,
                    "difficulty": difficulty,
                    "num_questions": num_questions,
                    "language": language
                }
            )
            
            # Try to parse JSON response
            try:
                questions_data = json.loads(response)
                questions = [
                    Question(
                        id=str(i),
                        type=q.get("type", "multiple_choice"),
                        question_text=q.get("question", ""),
                        options=q.get("options", []),
                        correct_answer=q.get("correct_answer", ""),
                        explanation=q.get("explanation", "")
                    )
                    for i, q in enumerate(questions_data)
                ]
            except json.JSONDecodeError:
                # Fallback to generated questions
                questions = self._generate_fallback_questions(topic, num_questions)
            
            return Quiz(
                id=f"{topic}_{difficulty}",
                topic=topic,
                questions=questions,
                time_limit_minutes=num_questions * 2  # 2 minutes per question
            )
        
        except Exception as e:
            logger.error(f"Quiz generation failed: {e}")
            return self._generate_fallback_quiz(topic, num_questions)
    
    def evaluate_answer(
        self,
        question: Question,
        user_answer: str
    ) -> EvaluationResult:
        """
        Evaluate user's answer to a question.
        
        Args:
            question: The question
            user_answer: User's answer
            
        Returns:
            Evaluation result
        """
        try:
            # Simple string comparison for multiple choice
            if question.type == "multiple_choice":
                is_correct = user_answer.strip().lower() == question.correct_answer.strip().lower()
                score = 1.0 if is_correct else 0.0
                
                if is_correct:
                    feedback = "✅ Correct! Well done!"
                else:
                    feedback = f"❌ Incorrect. The correct answer is: {question.correct_answer}"
                
                return EvaluationResult(
                    is_correct=is_correct,
                    score=score,
                    feedback=feedback,
                    explanation=question.explanation
                )
            
            # For code completion and debugging, use partial matching
            else:
                similarity = self._calculate_similarity(user_answer, question.correct_answer)
                is_correct = similarity > 0.7
                score = similarity
                
                if is_correct:
                    feedback = f"✅ Great job! Your answer is {int(similarity * 100)}% correct."
                else:
                    feedback = f"⚠️ Partially correct ({int(similarity * 100)}%). Review the explanation."
                
                return EvaluationResult(
                    is_correct=is_correct,
                    score=score,
                    feedback=feedback,
                    explanation=question.explanation
                )
        
        except Exception as e:
            logger.error(f"Answer evaluation failed: {e}")
            return EvaluationResult(
                is_correct=False,
                score=0.0,
                feedback="Error evaluating answer",
                explanation="Please try again"
            )
    
    def generate_explanation(
        self,
        question: Question,
        user_answer: str,
        language: str = "english"
    ) -> str:
        """
        Generate explanation for correct/incorrect answer.
        
        Args:
            question: The question
            user_answer: User's answer
            language: Output language
            
        Returns:
            Detailed explanation
        """
        try:
            prompt = f"""Explain why the answer to this question is correct or incorrect:

Question: {question.question_text}
User's Answer: {user_answer}
Correct Answer: {question.correct_answer}

Provide a clear, educational explanation."""
            
            return self.orchestrator.generate_completion(prompt)
        except Exception as e:
            logger.error(f"Explanation generation failed: {e}")
            return question.explanation
    
    def _generate_fallback_questions(self, topic: str, num_questions: int) -> List[Question]:
        """Generate fallback questions when AI fails."""
        questions = []
        
        # Generate simple questions based on topic
        if "react" in topic.lower():
            questions.append(Question(
                id="1",
                type="multiple_choice",
                question_text="What is the purpose of useState in React?",
                options=[
                    "To manage component state",
                    "To fetch data from APIs",
                    "To style components",
                    "To handle routing"
                ],
                correct_answer="To manage component state",
                explanation="useState is a React Hook that lets you add state to functional components."
            ))
        
        elif "javascript" in topic.lower():
            questions.append(Question(
                id="1",
                type="multiple_choice",
                question_text="What is the difference between let and var?",
                options=[
                    "let has block scope, var has function scope",
                    "let is faster than var",
                    "var is newer than let",
                    "There is no difference"
                ],
                correct_answer="let has block scope, var has function scope",
                explanation="let is block-scoped while var is function-scoped, making let safer to use."
            ))
        
        else:
            questions.append(Question(
                id="1",
                type="multiple_choice",
                question_text=f"What is a key concept in {topic}?",
                options=[
                    "Understanding the fundamentals",
                    "Ignoring best practices",
                    "Avoiding documentation",
                    "Random coding"
                ],
                correct_answer="Understanding the fundamentals",
                explanation=f"Understanding fundamentals is crucial for mastering {topic}."
            ))
        
        # Pad with more questions if needed
        while len(questions) < num_questions:
            questions.append(questions[0])  # Duplicate for now
        
        return questions[:num_questions]
    
    def _generate_fallback_quiz(self, topic: str, num_questions: int) -> Quiz:
        """Generate fallback quiz when AI fails."""
        return Quiz(
            id=f"{topic}_fallback",
            topic=topic,
            questions=self._generate_fallback_questions(topic, num_questions),
            time_limit_minutes=num_questions * 2
        )
    
    def _calculate_similarity(self, answer1: str, answer2: str) -> float:
        """Calculate simple similarity between two strings."""
        answer1 = answer1.lower().strip()
        answer2 = answer2.lower().strip()
        
        if answer1 == answer2:
            return 1.0
        
        # Simple word overlap
        words1 = set(answer1.split())
        words2 = set(answer2.split())
        
        if not words1 or not words2:
            return 0.0
        
        overlap = len(words1 & words2)
        total = len(words1 | words2)
        
        return overlap / total if total > 0 else 0.0
