"""Test code-based quiz and flashcard generation."""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from analyzers.code_analyzer import CodeAnalyzer, CodeAnalysis, CodeStructure, Function, Class, Pattern
from engines.quiz_engine import QuizEngine
from learning.flashcard_manager import FlashcardManager
from session_manager import SessionManager
from ai.langchain_orchestrator import LangChainOrchestrator
from config import load_config


def test_quiz_generation_from_code():
    """Test quiz generation from code analysis."""
    print("\n" + "="*60)
    print("TEST 1: Quiz Generation from Code Analysis")
    print("="*60)
    
    # Create mock code analysis
    code_analysis = CodeAnalysis(
        summary="Sample Python code with functions and classes",
        structure=CodeStructure(
            functions=[
                Function(
                    name="calculate_total",
                    parameters=["items", "tax_rate"],
                    line_number=10,
                    docstring="Calculates total price with tax"
                ),
                Function(
                    name="validate_email",
                    parameters=["email"],
                    line_number=20,
                    docstring="Validates email format"
                ),
                Function(
                    name="process_payment",
                    parameters=["amount", "method"],
                    line_number=30,
                    docstring="Processes payment transaction"
                )
            ],
            classes=[
                Class(
                    name="UserManager",
                    methods=["create_user", "update_user", "delete_user"],
                    line_number=50,
                    docstring="Manages user operations"
                ),
                Class(
                    name="OrderProcessor",
                    methods=["create_order", "cancel_order", "get_status"],
                    line_number=80,
                    docstring="Handles order processing"
                )
            ],
            imports=["flask", "sqlalchemy", "datetime"],
            main_logic="Main execution logic detected"
        ),
        patterns=[
            Pattern(
                name="Object-Oriented Design",
                description="Uses classes and objects for modularity",
                location="Throughout file"
            ),
            Pattern(
                name="Error Handling",
                description="Implements try-except error handling",
                location="Error handling blocks"
            )
        ],
        issues=[],
        complexity_score=45
    )
    
    # Initialize quiz engine
    from ai.bedrock_client import BedrockClient
    from ai.prompt_templates import PromptManager
    
    aws_config, app_config = load_config()
    bedrock_client = BedrockClient(aws_config)
    prompt_manager = PromptManager()
    orchestrator = LangChainOrchestrator(bedrock_client, prompt_manager)
    quiz_engine = QuizEngine(orchestrator)
    
    # Generate quiz
    print("\n📝 Generating quiz from code analysis...")
    quiz = quiz_engine.generate_quiz_from_code(
        code_analysis=code_analysis,
        language="english",
        num_questions=5
    )
    
    # Verify quiz
    print(f"\n✅ Quiz Generated Successfully!")
    print(f"   Topic: {quiz.topic}")
    print(f"   Questions: {len(quiz.questions)}")
    print(f"   Time Limit: {quiz.time_limit_minutes} minutes")
    
    # Display questions
    print("\n📋 Generated Questions:")
    for i, question in enumerate(quiz.questions, 1):
        print(f"\n   Q{i}: {question.question_text}")
        print(f"   Type: {question.type}")
        if question.options:
            print(f"   Options: {len(question.options)}")
        print(f"   Correct Answer: {question.correct_answer}")
        print(f"   Explanation: {question.explanation[:80]}...")
    
    # Verify questions are about the code
    assert quiz.topic == "Your Uploaded Code", "Quiz topic should be 'Your Uploaded Code'"
    assert len(quiz.questions) == 5, "Should generate 5 questions"
    
    # Check that questions reference actual code elements
    question_texts = [q.question_text for q in quiz.questions]
    has_function_question = any("calculate_total" in q or "validate_email" in q or "process_payment" in q for q in question_texts)
    has_class_question = any("UserManager" in q or "OrderProcessor" in q for q in question_texts)
    
    print(f"\n✅ Questions reference actual functions: {has_function_question}")
    print(f"✅ Questions reference actual classes: {has_class_question}")
    
    return True


def test_flashcard_generation_from_code():
    """Test flashcard generation from code analysis."""
    print("\n" + "="*60)
    print("TEST 2: Flashcard Generation from Code Analysis")
    print("="*60)
    
    # Create mock code analysis
    code_analysis = CodeAnalysis(
        summary="Sample Python code with functions and classes",
        structure=CodeStructure(
            functions=[
                Function(
                    name="authenticate_user",
                    parameters=["username", "password"],
                    line_number=15,
                    docstring="Authenticates user credentials"
                ),
                Function(
                    name="generate_token",
                    parameters=["user_id"],
                    line_number=25,
                    docstring="Generates JWT token for user"
                )
            ],
            classes=[
                Class(
                    name="DatabaseConnection",
                    methods=["connect", "disconnect", "execute_query"],
                    line_number=40,
                    docstring="Manages database connections"
                )
            ],
            imports=["jwt", "bcrypt", "psycopg2"],
            main_logic=""
        ),
        patterns=[
            Pattern(
                name="Authentication Pattern",
                description="Implements JWT-based authentication",
                location="Auth module"
            )
        ],
        issues=[],
        complexity_score=30
    )
    
    # Initialize flashcard manager
    session_manager = SessionManager()
    flashcard_manager = FlashcardManager(session_manager)
    
    # Generate flashcards
    print("\n🎴 Generating flashcards from code analysis...")
    flashcards = flashcard_manager.generate_flashcards(
        code_analysis=code_analysis,
        language="english"
    )
    
    # Verify flashcards
    print(f"\n✅ Flashcards Generated Successfully!")
    print(f"   Total Flashcards: {len(flashcards)}")
    
    # Display flashcards
    print("\n📋 Generated Flashcards:")
    for i, card in enumerate(flashcards, 1):
        print(f"\n   Card {i}:")
        print(f"   Front: {card.front}")
        print(f"   Back: {card.back[:80]}...")
        print(f"   Topic: {card.topic}")
        print(f"   Difficulty: {card.difficulty}")
    
    # Verify flashcards are about the code
    assert len(flashcards) > 0, "Should generate at least one flashcard"
    
    # Check that flashcards reference actual code elements
    card_fronts = [card.front for card in flashcards]
    has_function_card = any("authenticate_user" in front or "generate_token" in front for front in card_fronts)
    has_class_card = any("DatabaseConnection" in front for front in card_fronts)
    has_pattern_card = any("Authentication Pattern" in front for front in card_fronts)
    
    print(f"\n✅ Flashcards reference actual functions: {has_function_card}")
    print(f"✅ Flashcards reference actual classes: {has_class_card}")
    print(f"✅ Flashcards reference actual patterns: {has_pattern_card}")
    
    return True


def test_integration():
    """Test full integration flow."""
    print("\n" + "="*60)
    print("TEST 3: Full Integration Flow")
    print("="*60)
    
    # Sample code to analyze
    sample_code = """
def fibonacci(n):
    '''Calculate fibonacci number at position n.'''
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

class Calculator:
    '''Simple calculator class.'''
    
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b
"""
    
    print("\n📄 Sample Code:")
    print(sample_code)
    
    # Initialize components
    from ai.bedrock_client import BedrockClient
    from ai.prompt_templates import PromptManager
    
    aws_config, app_config = load_config()
    bedrock_client = BedrockClient(aws_config)
    prompt_manager = PromptManager()
    orchestrator = LangChainOrchestrator(bedrock_client, prompt_manager)
    code_analyzer = CodeAnalyzer(orchestrator)
    quiz_engine = QuizEngine(orchestrator)
    session_manager = SessionManager()
    flashcard_manager = FlashcardManager(session_manager)
    
    # Step 1: Analyze code
    print("\n🔍 Step 1: Analyzing code...")
    analysis = code_analyzer.analyze_file(
        code=sample_code,
        filename="test.py",
        language="english"
    )
    
    print(f"✅ Analysis complete!")
    print(f"   Functions found: {len(analysis.structure.functions)}")
    print(f"   Classes found: {len(analysis.structure.classes)}")
    print(f"   Patterns found: {len(analysis.patterns)}")
    
    # Step 2: Generate quiz
    print("\n📝 Step 2: Generating quiz...")
    quiz = quiz_engine.generate_quiz_from_code(
        code_analysis=analysis,
        language="english",
        num_questions=3
    )
    
    print(f"✅ Quiz generated with {len(quiz.questions)} questions")
    
    # Step 3: Generate flashcards
    print("\n🎴 Step 3: Generating flashcards...")
    flashcards = flashcard_manager.generate_flashcards(
        code_analysis=analysis,
        language="english"
    )
    
    print(f"✅ Generated {len(flashcards)} flashcards")
    
    # Verify integration
    assert len(quiz.questions) > 0, "Quiz should have questions"
    assert len(flashcards) > 0, "Should have flashcards"
    
    print("\n" + "="*60)
    print("✅ ALL INTEGRATION TESTS PASSED!")
    print("="*60)
    
    return True


if __name__ == "__main__":
    try:
        print("\n🚀 Starting Code-Based Quiz & Flashcard Tests...")
        
        # Run tests
        test_quiz_generation_from_code()
        test_flashcard_generation_from_code()
        test_integration()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED SUCCESSFULLY!")
        print("="*60)
        print("\n📌 Summary:")
        print("   ✓ Quiz generation from code analysis works")
        print("   ✓ Flashcard generation from code analysis works")
        print("   ✓ Full integration flow works end-to-end")
        print("\n💡 Next Steps:")
        print("   1. Run the app: python -m streamlit run app.py")
        print("   2. Upload a code file")
        print("   3. Click 'Analyze Code'")
        print("   4. Go to 'Quizzes' tab to see code-based quiz")
        print("   5. Go to 'Flashcards' tab to see code-based flashcards")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
