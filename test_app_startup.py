"""
Test app startup and initialization.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported."""
    print("\n" + "="*80)
    print("TEST: MODULE IMPORTS")
    print("="*80)
    
    try:
        # Core modules
        from session_manager import SessionManager
        print("✓ SessionManager imported")
        
        from config import load_config
        print("✓ Config imported")
        
        from ai.bedrock_client import BedrockClient
        print("✓ BedrockClient imported")
        
        from ai.langchain_orchestrator import LangChainOrchestrator
        print("✓ LangChainOrchestrator imported")
        
        # Analyzers
        from analyzers.intent_interpreter import IntentInterpreter
        print("✓ IntentInterpreter imported")
        
        from analyzers.file_selector import FileSelector
        print("✓ FileSelector imported")
        
        from analyzers.multi_file_analyzer import MultiFileAnalyzer
        print("✓ MultiFileAnalyzer imported")
        
        from analyzers.intent_driven_orchestrator import IntentDrivenOrchestrator
        print("✓ IntentDrivenOrchestrator imported")
        
        # Generators
        from generators.learning_artifact_generator import LearningArtifactGenerator
        print("✓ LearningArtifactGenerator imported")
        
        # UI components
        from ui.intent_driven_analysis_page import render_intent_driven_analysis_page
        print("✓ Intent-driven analysis page imported")
        
        from ui.learning_artifacts_dashboard import render_learning_artifacts_dashboard
        print("✓ Learning artifacts dashboard imported")
        
        print("\n✅ All imports successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_session_manager():
    """Test SessionManager initialization."""
    print("\n" + "="*80)
    print("TEST: SESSION MANAGER")
    print("="*80)
    
    try:
        from session_manager import SessionManager
        
        # Mock streamlit session state
        class MockSessionState:
            def __init__(self):
                self.data = {}
            
            def __contains__(self, key):
                return key in self.data
            
            def __getitem__(self, key):
                return self.data[key]
            
            def __setitem__(self, key, value):
                self.data[key] = value
            
            def get(self, key, default=None):
                return self.data.get(key, default)
        
        # Replace st.session_state with mock
        import streamlit as st
        original_session_state = st.session_state
        st.session_state = MockSessionState()
        
        # Initialize session manager
        session_manager = SessionManager()
        print("✓ SessionManager initialized")
        
        # Test methods
        session_manager.set_language_preference("english")
        print("✓ set_language_preference works")
        
        lang = session_manager.get_language_preference()
        print(f"✓ get_language_preference works: {lang}")
        
        artifacts = session_manager.get_learning_artifacts()
        print(f"✓ get_learning_artifacts works: {len(artifacts)} keys")
        
        # Restore original session state
        st.session_state = original_session_state
        
        print("\n✅ SessionManager working correctly!")
        return True
        
    except Exception as e:
        print(f"\n❌ SessionManager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_artifact_generation():
    """Test learning artifact generation."""
    print("\n" + "="*80)
    print("TEST: ARTIFACT GENERATION")
    print("="*80)
    
    try:
        from generators.learning_artifact_generator import LearningArtifactGenerator
        from models.intent_models import UserIntent, IntentScope, MultiFileAnalysis
        
        # Create mock components
        class MockFlashcardManager:
            pass
        
        class MockQuizEngine:
            pass
        
        class MockOrchestrator:
            pass
        
        # Initialize generator
        generator = LearningArtifactGenerator(
            MockFlashcardManager(),
            MockQuizEngine(),
            MockOrchestrator()
        )
        print("✓ LearningArtifactGenerator initialized")
        
        # Create mock intent
        intent = UserIntent(
            primary_intent="learn_specific_feature",
            secondary_intents=[],
            scope=IntentScope(scope_type="entire_repo", target_paths=[], exclude_paths=[]),
            audience_level="intermediate",
            technologies=["javascript"],
            confidence_score=0.9
        )
        print("✓ Mock intent created")
        
        # Create mock analysis with key concepts
        analysis = MultiFileAnalysis(
            analyzed_files=['src/App.js', 'src/Router.js'],
            file_analyses={},
            key_concepts=[
                {
                    'name': 'App',
                    'category': 'classes',
                    'description': 'Main application component',
                    'file': 'src/App.js',
                    'line': 10,
                    'evidence': [
                        {
                            'file_path': 'src/App.js',
                            'line_start': 10,
                            'line_end': 15,
                            'context': 'Main component'
                        }
                    ]
                },
                {
                    'name': 'Router',
                    'category': 'functions',
                    'description': 'Handles routing logic',
                    'file': 'src/Router.js',
                    'line': 5,
                    'evidence': [
                        {
                            'file_path': 'src/Router.js',
                            'line_start': 5,
                            'line_end': 10,
                            'context': 'Routing function'
                        }
                    ]
                }
            ]
        )
        print("✓ Mock analysis created")
        
        # Test flashcard generation
        flashcards = generator.generate_flashcards(analysis, intent, "english")
        print(f"✓ Generated {len(flashcards)} flashcards")
        
        if flashcards:
            print(f"  Sample: {flashcards[0].front[:50]}...")
        
        # Test quiz generation
        quiz = generator.generate_quiz(analysis, intent, num_questions=5, language="english")
        print(f"✓ Generated quiz with {len(quiz.get('questions', []))} questions")
        
        # Test learning path generation
        learning_path = generator.generate_learning_path(analysis, intent, "english")
        print(f"✓ Generated learning path with {learning_path.total_steps} steps")
        
        # Test concept summary
        summary = generator.generate_concept_summary(analysis, intent, "english")
        print(f"✓ Generated concept summary with {summary['total_concepts']} concepts")
        
        print("\n✅ Artifact generation working correctly!")
        return True
        
    except Exception as e:
        print(f"\n❌ Artifact generation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all startup tests."""
    print("\n" + "="*80)
    print("APP STARTUP TESTS")
    print("="*80)
    
    tests = [
        ("Module Imports", test_imports),
        ("Session Manager", test_session_manager),
        ("Artifact Generation", test_artifact_generation),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n✗ TEST FAILED WITH EXCEPTION: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    
    print(f"\nTotal: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n🎉 ALL TESTS PASSED! App can start successfully.")
        return True
    else:
        print(f"\n⚠️  {total_tests - total_passed} test(s) failed.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
