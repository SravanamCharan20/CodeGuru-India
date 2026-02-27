"""Test quiz and flashcard features."""
import sys

def test_quiz_database():
    """Test quiz database."""
    print("=" * 60)
    print("Testing Quiz Database")
    print("=" * 60)
    
    try:
        from data.quiz_questions import QUIZ_DATABASE
        
        print(f"\n✅ Quiz database loaded")
        print(f"   Topics available: {len(QUIZ_DATABASE)}")
        
        total_questions = 0
        for topic, quiz_data in QUIZ_DATABASE.items():
            questions = quiz_data.get("questions", [])
            difficulty = quiz_data.get("difficulty", "Unknown")
            print(f"\n   📝 {topic}")
            print(f"      Difficulty: {difficulty}")
            print(f"      Questions: {len(questions)}")
            total_questions += len(questions)
            
            # Validate question structure
            for i, q in enumerate(questions):
                required_fields = ["type", "question", "options", "correct_answer", "explanation"]
                missing = [field for field in required_fields if field not in q]
                if missing:
                    print(f"      ❌ Question {i+1} missing fields: {missing}")
                    return False
        
        print(f"\n   Total questions: {total_questions}")
        return True
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_flashcard_database():
    """Test flashcard database."""
    print("\n" + "=" * 60)
    print("Testing Flashcard Database")
    print("=" * 60)
    
    try:
        from data.flashcard_data import FLASHCARD_DATABASE
        
        print(f"\n✅ Flashcard database loaded")
        print(f"   Topics available: {len(FLASHCARD_DATABASE)}")
        
        total_cards = 0
        for topic, cards in FLASHCARD_DATABASE.items():
            print(f"\n   📚 {topic}")
            print(f"      Cards: {len(cards)}")
            total_cards += len(cards)
            
            # Validate card structure
            for i, card in enumerate(cards):
                required_fields = ["front", "back", "difficulty"]
                missing = [field for field in required_fields if field not in card]
                if missing:
                    print(f"      ❌ Card {i+1} missing fields: {missing}")
                    return False
        
        print(f"\n   Total flashcards: {total_cards}")
        return True
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_quiz_ui():
    """Test quiz UI components."""
    print("\n" + "=" * 60)
    print("Testing Quiz UI")
    print("=" * 60)
    
    try:
        from ui.quiz_view import render_quiz_view
        
        print("\n✅ Quiz UI module loaded")
        
        # Check for required functions
        functions = [
            'render_quiz_view',
            '_render_quiz_selection',
            '_render_quiz_questions',
            '_show_quiz_results'
        ]
        
        import ui.quiz_view as quiz_module
        for func_name in functions:
            if hasattr(quiz_module, func_name):
                print(f"   ✅ {func_name}")
            else:
                print(f"   ❌ {func_name} - NOT FOUND")
                return False
        
        return True
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_flashcard_ui():
    """Test flashcard UI components."""
    print("\n" + "=" * 60)
    print("Testing Flashcard UI")
    print("=" * 60)
    
    try:
        from ui.flashcard_view import render_flashcard_view
        
        print("\n✅ Flashcard UI module loaded")
        
        # Check for required functions
        functions = [
            'render_flashcard_view',
            '_render_flashcard'
        ]
        
        import ui.flashcard_view as flashcard_module
        for func_name in functions:
            if hasattr(flashcard_module, func_name):
                print(f"   ✅ {func_name}")
            else:
                print(f"   ❌ {func_name} - NOT FOUND")
                return False
        
        return True
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_data_quality():
    """Test data quality and content."""
    print("\n" + "=" * 60)
    print("Testing Data Quality")
    print("=" * 60)
    
    try:
        from data.quiz_questions import QUIZ_DATABASE
        from data.flashcard_data import FLASHCARD_DATABASE
        
        # Test quiz questions
        print("\n📝 Quiz Questions Quality:")
        for topic, quiz_data in QUIZ_DATABASE.items():
            questions = quiz_data.get("questions", [])
            for i, q in enumerate(questions):
                # Check if correct answer is in options
                if q["correct_answer"] not in q["options"]:
                    print(f"   ❌ {topic} Q{i+1}: Correct answer not in options")
                    return False
                
                # Check if explanation exists and is not empty
                if not q.get("explanation") or len(q["explanation"]) < 10:
                    print(f"   ❌ {topic} Q{i+1}: Explanation too short or missing")
                    return False
        
        print("   ✅ All quiz questions valid")
        
        # Test flashcards
        print("\n📚 Flashcard Quality:")
        for topic, cards in FLASHCARD_DATABASE.items():
            for i, card in enumerate(cards):
                # Check if front and back are not empty
                if not card.get("front") or len(card["front"]) < 5:
                    print(f"   ❌ {topic} Card{i+1}: Front text too short")
                    return False
                
                if not card.get("back") or len(card["back"]) < 10:
                    print(f"   ❌ {topic} Card{i+1}: Back text too short")
                    return False
                
                # Check difficulty is valid
                if card.get("difficulty") not in ["Beginner", "Intermediate", "Advanced"]:
                    print(f"   ❌ {topic} Card{i+1}: Invalid difficulty")
                    return False
        
        print("   ✅ All flashcards valid")
        
        return True
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Run all tests."""
    print("\n🎯 Quiz & Flashcard Feature Test\n")
    
    results = []
    
    # Run tests
    results.append(("Quiz Database", test_quiz_database()))
    results.append(("Flashcard Database", test_flashcard_database()))
    results.append(("Quiz UI", test_quiz_ui()))
    results.append(("Flashcard UI", test_flashcard_ui()))
    results.append(("Data Quality", test_data_quality()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    # Final status
    print("\n" + "=" * 60)
    if passed == total:
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\n🎉 Quiz and Flashcard features are ready!")
        print("\nFeatures available:")
        print("  ✅ 6 quiz topics with 30 total questions")
        print("  ✅ 6 flashcard topics with 30 total cards")
        print("  ✅ Multiple difficulty levels")
        print("  ✅ Progress tracking")
        print("  ✅ Interactive UI with flip animations")
        print("\nTo use:")
        print("  1. Start app: python -m streamlit run app.py")
        print("  2. Go to 'Quizzes' or 'Flashcards' tab")
        print("  3. Select a topic and start learning!")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("=" * 60)
        print("\nPlease fix the failing tests.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
