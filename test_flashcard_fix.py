"""Test flashcard generation and saving."""
import sys
from pathlib import Path
import json

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from analyzers.code_analyzer import CodeAnalyzer, CodeAnalysis, CodeStructure, Function, Class, Pattern
from learning.flashcard_manager import FlashcardManager
from session_manager import SessionManager
from ai.langchain_orchestrator import LangChainOrchestrator
from ai.bedrock_client import BedrockClient
from ai.prompt_templates import PromptManager
from config import load_config


def test_flashcard_generation_and_saving():
    """Test that flashcards are generated and saved correctly."""
    print("\n" + "="*60)
    print("TEST: Flashcard Generation and Saving")
    print("="*60)
    
    # Create mock code analysis
    code_analysis = CodeAnalysis(
        summary="Test code",
        structure=CodeStructure(
            functions=[
                Function(
                    name="test_function",
                    parameters=["arg1", "arg2"],
                    line_number=10,
                    docstring="Test function docstring"
                )
            ],
            classes=[
                Class(
                    name="TestClass",
                    methods=["method1", "method2"],
                    line_number=20,
                    docstring="Test class docstring"
                )
            ],
            imports=["os", "sys"],
            main_logic=""
        ),
        patterns=[
            Pattern(
                name="Test Pattern",
                description="Test pattern description",
                location="Test location"
            )
        ],
        issues=[],
        complexity_score=10
    )
    
    # Initialize session manager and flashcard manager
    session_manager = SessionManager()
    flashcard_manager = FlashcardManager(session_manager)
    
    print("\n📝 Step 1: Generating flashcards...")
    flashcards = flashcard_manager.generate_flashcards(
        code_analysis=code_analysis,
        language="english"
    )
    
    print(f"✅ Generated {len(flashcards)} flashcards")
    for i, card in enumerate(flashcards, 1):
        print(f"   Card {i}: {card.front}")
    
    print("\n💾 Step 2: Checking if flashcards were saved...")
    progress = session_manager.load_progress()
    saved_flashcards = progress.get("flashcards", {}).get("cards", [])
    
    print(f"✅ Found {len(saved_flashcards)} flashcards in session")
    
    if len(saved_flashcards) == 0:
        print("❌ ERROR: Flashcards were not saved!")
        print("\n🔍 Debug Info:")
        print(f"   Progress file location: {session_manager.progress_file}")
        print(f"   Progress data: {json.dumps(progress, indent=2)}")
        return False
    
    print("\n✅ Flashcards saved successfully!")
    
    # Verify flashcard data structure
    print("\n🔍 Step 3: Verifying flashcard data structure...")
    for i, card_dict in enumerate(saved_flashcards, 1):
        print(f"\n   Card {i}:")
        print(f"      ID: {card_dict.get('id', 'MISSING')}")
        print(f"      Front: {card_dict.get('front', 'MISSING')}")
        print(f"      Back: {card_dict.get('back', 'MISSING')[:50]}...")
        print(f"      Topic: {card_dict.get('topic', 'MISSING')}")
        print(f"      Difficulty: {card_dict.get('difficulty', 'MISSING')}")
    
    print("\n" + "="*60)
    print("✅ TEST PASSED!")
    print("="*60)
    
    return True


if __name__ == "__main__":
    try:
        print("\n🚀 Starting Flashcard Fix Test...")
        
        success = test_flashcard_generation_and_saving()
        
        if success:
            print("\n✅ Flashcards are working correctly!")
            print("\n💡 If flashcards still don't show in the app:")
            print("   1. Make sure 'Generate Flashcards' checkbox is enabled")
            print("   2. Click 'Analyze Code' button")
            print("   3. Wait for success message")
            print("   4. Go to Flashcards tab")
        else:
            print("\n❌ Flashcard generation/saving failed!")
            sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
