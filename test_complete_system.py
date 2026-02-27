"""
Complete system test to verify all fixes work.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import logging
from dataclasses import dataclass
from typing import List, Dict

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Import the actual classes
from analyzers.file_selector import FileSelector
from analyzers.intent_interpreter import IntentInterpreter
from models.intent_models import UserIntent, IntentScope

# Mock FileInfo class
@dataclass
class FileInfo:
    path: str
    name: str
    extension: str
    size_bytes: int = 1000
    lines: int = 100

# Mock RepoAnalysis class
@dataclass
class RepoAnalysis:
    repo_url: str
    total_files: int
    total_lines: int
    total_size_bytes: int
    file_tree: Dict[str, List[FileInfo]]
    languages: Dict[str, int]
    main_files: List[FileInfo]
    summary: str

def create_mock_repo_analysis():
    """Create mock repository analysis for Namaste-React."""
    files = [
        FileInfo("src/App.js", "App.js", ".js", 2000, 150),
        FileInfo("src/index.js", "index.js", ".js", 500, 50),
        FileInfo("src/components/Header.js", "Header.js", ".js", 1500, 100),
        FileInfo("src/components/Body.js", "Body.js", ".js", 2000, 120),
        FileInfo("src/components/About.js", "About.js", ".js", 1000, 80),
        FileInfo("src/components/Contact.js", "Contact.js", ".js", 1000, 80),
        FileInfo("src/components/RestaurantCard.js", "RestaurantCard.js", ".js", 1500, 100),
        FileInfo("src/components/RestaurantMenu.js", "RestaurantMenu.js", ".js", 1800, 110),
        FileInfo("src/components/Error.js", "Error.js", ".js", 800, 60),
        FileInfo("src/utils/constants.js", "constants.js", ".js", 500, 40),
        FileInfo("package.json", "package.json", ".json", 1000, 50),
        FileInfo("README.md", "README.md", ".md", 2000, 100),
    ]
    
    # Create file_tree structure (dict mapping directories to file lists)
    file_tree = {
        'root': [files[10], files[11]],  # package.json, README.md
        'src': [files[0], files[1], files[9]],  # App.js, index.js, constants.js
        'src/components': files[2:9],  # All component files
    }
    
    return RepoAnalysis(
        repo_url="https://github.com/SravanamCharan20/Namaste-React",
        total_files=len(files),
        total_lines=sum(f.lines for f in files),
        total_size_bytes=sum(f.size_bytes for f in files),
        file_tree=file_tree,
        languages={"JavaScript": 1000},
        main_files=[files[0], files[1]],
        summary="Mock Namaste-React repository"
    )

def test_file_extraction():
    """Test 1: File extraction from file_tree."""
    print("\n" + "="*80)
    print("TEST 1: FILE EXTRACTION")
    print("="*80)
    
    repo_analysis = create_mock_repo_analysis()
    file_selector = FileSelector(langchain_orchestrator=None)
    
    # Test _get_all_files
    all_files = file_selector._get_all_files(repo_analysis)
    
    print(f"✓ Extracted {len(all_files)} files from file_tree")
    print(f"  Expected: 12 files")
    print(f"  Result: {'PASS' if len(all_files) == 12 else 'FAIL'}")
    
    if len(all_files) > 0:
        print(f"\n  Sample files:")
        for f in all_files[:5]:
            print(f"    - {f.path}")
    
    return len(all_files) == 12

def test_intent_interpretation():
    """Test 2: Intent interpretation."""
    print("\n" + "="*80)
    print("TEST 2: INTENT INTERPRETATION")
    print("="*80)
    
    intent_interpreter = IntentInterpreter(langchain_orchestrator=None)
    user_input = "i want to learn how the routing works in this app"
    
    intent = intent_interpreter.interpret_intent(user_input, None)
    
    print(f"✓ User input: {user_input}")
    print(f"✓ Primary intent: {intent.primary_intent}")
    print(f"✓ Confidence: {intent.confidence_score}")
    print(f"✓ AI keywords: {getattr(intent, 'ai_keywords', [])}")
    
    success = intent.primary_intent == "learn_specific_feature" and intent.confidence_score >= 0.7
    print(f"\n  Result: {'PASS' if success else 'FAIL'}")
    
    return success

def test_smart_file_selection():
    """Test 3: Smart rule-based file selection."""
    print("\n" + "="*80)
    print("TEST 3: SMART FILE SELECTION")
    print("="*80)
    
    repo_analysis = create_mock_repo_analysis()
    file_selector = FileSelector(langchain_orchestrator=None)
    intent_interpreter = IntentInterpreter(langchain_orchestrator=None)
    
    # Create intent
    user_input = "i want to learn how the routing works in this app"
    intent = intent_interpreter.interpret_intent(user_input, repo_analysis)
    
    # Select files
    result = file_selector.select_files(intent, repo_analysis)
    
    print(f"✓ Total files scanned: {result.total_scanned}")
    print(f"✓ Files excluded: {result.excluded_count}")
    print(f"✓ Files selected: {len(result.selected_files)}")
    
    if result.selected_files:
        print(f"\n  Selected files:")
        for selection in result.selected_files[:10]:
            print(f"    - {selection.file_info.path} (score: {selection.relevance_score:.2f})")
            print(f"      Reason: {selection.selection_reason}")
    
    success = len(result.selected_files) > 0
    print(f"\n  Result: {'PASS' if success else 'FAIL'}")
    
    return success

def test_important_files_selected():
    """Test 4: Verify important files are selected."""
    print("\n" + "="*80)
    print("TEST 4: IMPORTANT FILES SELECTED")
    print("="*80)
    
    repo_analysis = create_mock_repo_analysis()
    file_selector = FileSelector(langchain_orchestrator=None)
    intent_interpreter = IntentInterpreter(langchain_orchestrator=None)
    
    user_input = "i want to learn how the routing works in this app"
    intent = intent_interpreter.interpret_intent(user_input, repo_analysis)
    result = file_selector.select_files(intent, repo_analysis)
    
    # Check if important files are selected
    selected_paths = [s.file_info.path for s in result.selected_files]
    
    important_files = ['src/App.js', 'src/index.js']
    found_important = [f for f in important_files if f in selected_paths]
    
    print(f"✓ Important files to find: {important_files}")
    print(f"✓ Found: {found_important}")
    
    success = len(found_important) >= 1  # At least one important file
    print(f"\n  Result: {'PASS' if success else 'FAIL'}")
    
    return success

def test_fallback_mechanism():
    """Test 5: Fallback mechanism when no matches."""
    print("\n" + "="*80)
    print("TEST 5: FALLBACK MECHANISM")
    print("="*80)
    
    repo_analysis = create_mock_repo_analysis()
    file_selector = FileSelector(langchain_orchestrator=None)
    
    # Create intent with keywords that won't match
    intent = UserIntent(
        primary_intent="learn_specific_feature",
        secondary_intents=[],
        scope=IntentScope(scope_type="entire_repo", target_paths=[], exclude_paths=[]),
        audience_level="intermediate",
        technologies=[],
        confidence_score=0.9
    )
    intent.ai_keywords = ["nonexistent", "fake", "notreal"]  # Keywords that won't match
    
    result = file_selector.select_files(intent, repo_analysis)
    
    print(f"✓ Using keywords that won't match: {intent.ai_keywords}")
    print(f"✓ Files selected by fallback: {len(result.selected_files)}")
    
    if result.selected_files:
        print(f"\n  Fallback selected:")
        for selection in result.selected_files[:5]:
            print(f"    - {selection.file_info.path}")
    
    success = len(result.selected_files) > 0  # Fallback should still select files
    print(f"\n  Result: {'PASS' if success else 'FAIL'}")
    
    return success

def run_all_tests():
    """Run all tests and report results."""
    print("\n" + "="*80)
    print("RUNNING COMPLETE SYSTEM TESTS")
    print("="*80)
    
    tests = [
        ("File Extraction", test_file_extraction),
        ("Intent Interpretation", test_intent_interpretation),
        ("Smart File Selection", test_smart_file_selection),
        ("Important Files Selected", test_important_files_selected),
        ("Fallback Mechanism", test_fallback_mechanism),
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
        print("\n🎉 ALL TESTS PASSED! System is working correctly.")
        return True
    else:
        print(f"\n⚠️  {total_tests - total_passed} test(s) failed. Review the output above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
