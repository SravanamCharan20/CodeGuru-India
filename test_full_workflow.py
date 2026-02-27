"""
Test the complete workflow from analysis to artifact display.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import logging
from dataclasses import dataclass
from typing import List, Dict

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Import components
from analyzers.multi_file_analyzer import MultiFileAnalyzer
from analyzers.code_analyzer import CodeAnalyzer
from generators.learning_artifact_generator import LearningArtifactGenerator
from models.intent_models import UserIntent, IntentScope, FileSelection

# Mock components
@dataclass
class FileInfo:
    path: str
    name: str
    extension: str

class MockOrchestrator:
    def summarize_code(self, code, language):
        return "Mock summary"
    
    def identify_patterns(self, code):
        return []

class MockFlashcardManager:
    pass

class MockQuizEngine:
    pass

def test_full_workflow():
    """Test the complete workflow."""
    print("\n" + "="*80)
    print("FULL WORKFLOW TEST")
    print("="*80)
    
    try:
        # Step 1: Create mock file selections
        file_selections = [
            FileSelection(
                file_info=FileInfo("test.js", "test.js", ".js"),
                relevance_score=0.9,
                selection_reason="Test file",
                priority=1,
                file_role="core_logic"
            )
        ]
        
        # Create test JavaScript file
        test_code = """
function Router() {
    return <div>Router component</div>;
}

class App {
    constructor() {
        this.router = new Router();
    }
    
    render() {
        return this.router;
    }
}

export default App;
"""
        
        # Write test file
        os.makedirs("test_repo", exist_ok=True)
        with open("test_repo/test.js", "w") as f:
            f.write(test_code)
        
        print("✓ Created test repository")
        
        # Step 2: Initialize components
        orchestrator = MockOrchestrator()
        code_analyzer = CodeAnalyzer(orchestrator)
        multi_file_analyzer = MultiFileAnalyzer(code_analyzer, orchestrator)
        
        print("✓ Initialized analyzers")
        
        # Step 3: Create intent
        intent = UserIntent(
            primary_intent="learn_specific_feature",
            secondary_intents=[],
            scope=IntentScope(scope_type="entire_repo", target_paths=[], exclude_paths=[]),
            audience_level="intermediate",
            technologies=["javascript"],
            confidence_score=0.9
        )
        
        print("✓ Created intent")
        
        # Step 4: Analyze files
        analysis = multi_file_analyzer.analyze_files(
            file_selections,
            "test_repo",
            intent
        )
        
        print(f"✓ Analyzed files")
        print(f"  - Analyzed files: {len(analysis.analyzed_files)}")
        print(f"  - Key concepts: {len(analysis.key_concepts)}")
        
        if analysis.key_concepts:
            print(f"\n  Concepts extracted:")
            for concept in analysis.key_concepts[:5]:
                print(f"    - {concept['name']} ({concept['category']}): {concept['description'][:50]}...")
        
        # Step 5: Generate artifacts
        artifact_generator = LearningArtifactGenerator(
            MockFlashcardManager(),
            MockQuizEngine(),
            orchestrator
        )
        
        flashcards = artifact_generator.generate_flashcards(analysis, intent, "english")
        quiz = artifact_generator.generate_quiz(analysis, intent, num_questions=5, language="english")
        learning_path = artifact_generator.generate_learning_path(analysis, intent, "english")
        concept_summary = artifact_generator.generate_concept_summary(analysis, intent, "english")
        
        print(f"\n✓ Generated artifacts:")
        print(f"  - Flashcards: {len(flashcards)}")
        print(f"  - Quiz questions: {len(quiz.get('questions', []))}")
        print(f"  - Learning steps: {learning_path.total_steps}")
        print(f"  - Concept summary: {concept_summary['total_concepts']} concepts")
        
        # Show sample flashcard
        if flashcards:
            print(f"\n  Sample flashcard:")
            print(f"    Q: {flashcards[0].front}")
            print(f"    A: {flashcards[0].back[:100]}...")
        
        # Show sample quiz question
        if quiz.get('questions'):
            q = quiz['questions'][0]
            print(f"\n  Sample quiz question:")
            print(f"    Q: {q.question_text}")
            print(f"    A: {q.correct_answer[:100]}...")
        
        # Cleanup
        import shutil
        shutil.rmtree("test_repo")
        
        # Verify all artifacts were generated
        success = (
            len(flashcards) > 0 and
            len(quiz.get('questions', [])) > 0 and
            learning_path.total_steps > 0 and
            concept_summary['total_concepts'] > 0
        )
        
        if success:
            print("\n✅ FULL WORKFLOW TEST PASSED!")
            print("All artifacts generated successfully.")
            return True
        else:
            print("\n❌ FULL WORKFLOW TEST FAILED!")
            print("Some artifacts were not generated.")
            return False
    
    except Exception as e:
        print(f"\n❌ TEST FAILED WITH EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_full_workflow()
    sys.exit(0 if success else 1)
