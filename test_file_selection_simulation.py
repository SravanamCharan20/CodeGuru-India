"""
Simulation script to test the file selection process.
This will help us understand what's happening and identify the error.
"""

import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Simulate repository structure (Namaste-React)
SIMULATED_REPO_FILES = [
    {"name": "App.js", "path": "src/App.js", "extension": ".js"},
    {"name": "index.js", "path": "src/index.js", "extension": ".js"},
    {"name": "Header.js", "path": "src/components/Header.js", "extension": ".js"},
    {"name": "Body.js", "path": "src/components/Body.js", "extension": ".js"},
    {"name": "About.js", "path": "src/components/About.js", "extension": ".js"},
    {"name": "Contact.js", "path": "src/components/Contact.js", "extension": ".js"},
    {"name": "RestaurantCard.js", "path": "src/components/RestaurantCard.js", "extension": ".js"},
    {"name": "RestaurantMenu.js", "path": "src/components/RestaurantMenu.js", "extension": ".js"},
    {"name": "Error.js", "path": "src/components/Error.js", "extension": ".js"},
    {"name": "package.json", "path": "package.json", "extension": ".json"},
    {"name": "README.md", "path": "README.md", "extension": ".md"},
]

# Simulate user intent
USER_INPUT = "i want to learn how the routing works in this app"

def simulate_intent_interpretation():
    """Simulate intent interpretation."""
    print("\n" + "="*80)
    print("STEP 1: INTENT INTERPRETATION")
    print("="*80)
    
    user_input_lower = USER_INPUT.lower()
    
    # Rule-based detection
    primary_intent = "learn_specific_feature"
    confidence = 0.9
    technologies = []
    
    if "react" in user_input_lower:
        technologies.append("React")
    
    print(f"User Input: {USER_INPUT}")
    print(f"Primary Intent: {primary_intent}")
    print(f"Confidence: {confidence}")
    print(f"Technologies: {technologies}")
    
    # AI keyword extraction simulation
    print("\n--- AI Keyword Extraction ---")
    ai_keywords = ["route", "router", "routing", "navigation", "navigate", "link", "path", "page", "component", "app"]
    print(f"AI Keywords: {ai_keywords}")
    
    return {
        "primary_intent": primary_intent,
        "confidence": confidence,
        "technologies": technologies,
        "ai_keywords": ai_keywords
    }

def simulate_keyword_based_selection(intent):
    """Simulate keyword-based file selection."""
    print("\n" + "="*80)
    print("STEP 2A: KEYWORD-BASED FILE SELECTION (Fallback)")
    print("="*80)
    
    keywords = set(intent["ai_keywords"])
    keywords.update(["learn", "specific", "feature"])
    
    print(f"Keywords to match: {keywords}")
    print("\nScanning files...")
    
    scored_files = []
    for file_info in SIMULATED_REPO_FILES:
        name_lower = file_info["name"].lower()
        path_lower = file_info["path"].lower()
        
        score = 0.0
        matches = []
        
        # Check name matching
        for keyword in keywords:
            if keyword in name_lower:
                score += 0.3
                matches.append(f"name:{keyword}")
        
        # Check path matching
        for keyword in keywords:
            if keyword in path_lower:
                score += 0.2
                matches.append(f"path:{keyword}")
        
        # Boost for important files
        if file_info["name"] in ["App.js", "index.js"]:
            score += 0.3
            matches.append("important_file")
        
        if score > 0:
            print(f"  {file_info['path']}: score={score:.2f}, matches={matches}")
            scored_files.append((file_info, score))
    
    # Apply threshold
    THRESHOLD = 0.15
    selected = [f for f, s in scored_files if s >= THRESHOLD]
    
    print(f"\nThreshold: {THRESHOLD}")
    print(f"Files above threshold: {len(selected)}")
    print(f"Selected files: {[f['path'] for f in selected]}")
    
    return selected

def simulate_ai_semantic_selection(intent):
    """Simulate AI semantic file selection."""
    print("\n" + "="*80)
    print("STEP 2B: AI SEMANTIC FILE SELECTION (Primary)")
    print("="*80)
    
    # Build file list
    file_list = [{"path": f["path"], "name": f["name"], "extension": f["extension"]} 
                 for f in SIMULATED_REPO_FILES]
    
    print(f"Sending {len(file_list)} files to AI...")
    print(f"User Goal: {intent['primary_intent'].replace('_', ' ')}")
    
    # Simulate AI prompt
    prompt = f"""You are analyzing a code repository to help a user learn about: "learn specific feature"

User's Learning Goal: "learn specific feature"
Audience Level: intermediate
Technologies: {', '.join(intent['technologies']) if intent['technologies'] else 'Not specified'}

Repository Files (showing {len(file_list)} files):
{json.dumps(file_list, indent=2)}

Task: Analyze the file paths and names to identify which files are MOST RELEVANT to the user's learning goal.

Think semantically and contextually:
- For "routing": Look for files with route, router, navigation, App, index, pages, etc.
- For "authentication": Look for files with auth, login, user, session, token, etc.
- Consider file locations (src/, components/, pages/, routes/, etc.)
- Consider common patterns (App.js is often the main entry point, index files are important)

Select 10-20 files that would best help the user understand the topic.

Respond with ONLY a JSON array of file paths, nothing else:
["path/to/file1.js", "path/to/file2.js", ...]"""
    
    print("\n--- AI Prompt (truncated) ---")
    print(prompt[:500] + "...")
    
    # Simulate AI response (what Meta Llama 3.2 3B might return)
    print("\n--- Simulating AI Response ---")
    
    # Scenario 1: Good response
    ai_response_good = """["src/App.js", "src/index.js", "src/components/Header.js", "src/components/About.js", "src/components/Contact.js"]"""
    
    # Scenario 2: Response with extra text (common with small models)
    ai_response_with_text = """Based on the user's learning goal, here are the relevant files:
["src/App.js", "src/index.js", "src/components/Header.js"]
These files contain the routing logic."""
    
    # Scenario 3: Response without JSON
    ai_response_no_json = """The most relevant files for learning routing are:
- src/App.js (main routing setup)
- src/index.js (entry point)
- src/components/Header.js (navigation)"""
    
    # Test with different scenarios
    scenarios = [
        ("Good JSON", ai_response_good),
        ("JSON with extra text", ai_response_with_text),
        ("No JSON", ai_response_no_json)
    ]
    
    for scenario_name, response in scenarios:
        print(f"\n--- Scenario: {scenario_name} ---")
        print(f"AI Response: {response}")
        
        # Try to parse
        try:
            response_clean = response.strip()
            
            # Remove markdown
            if '```' in response_clean:
                response_clean = response_clean.split('```')[1]
                if response_clean.startswith('json'):
                    response_clean = response_clean[4:]
                response_clean = response_clean.strip()
            
            # Find JSON array
            start_idx = response_clean.find('[')
            end_idx = response_clean.rfind(']') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_clean[start_idx:end_idx]
                selected_paths = json.loads(json_str)
                print(f"✓ Successfully parsed: {selected_paths}")
                
                # Match with actual files
                path_to_file = {f["path"]: f for f in SIMULATED_REPO_FILES}
                matched = [path for path in selected_paths if path in path_to_file]
                print(f"✓ Matched {len(matched)}/{len(selected_paths)} files")
                
                if scenario_name == "Good JSON":
                    return matched
            else:
                print(f"✗ No JSON array found")
        
        except Exception as e:
            print(f"✗ Parsing failed: {e}")
    
    return []

def simulate_complete_flow():
    """Simulate the complete file selection flow."""
    print("\n" + "="*80)
    print("COMPLETE FILE SELECTION SIMULATION")
    print("="*80)
    print(f"Repository: Namaste-React (simulated)")
    print(f"Total files: {len(SIMULATED_REPO_FILES)}")
    print(f"User input: {USER_INPUT}")
    
    # Step 1: Intent interpretation
    intent = simulate_intent_interpretation()
    
    # Step 2: AI semantic selection (primary)
    ai_selected = simulate_ai_semantic_selection(intent)
    
    if ai_selected:
        print("\n" + "="*80)
        print("RESULT: AI SEMANTIC SELECTION SUCCESS")
        print("="*80)
        print(f"Selected {len(ai_selected)} files:")
        for path in ai_selected:
            print(f"  - {path}")
        return ai_selected
    else:
        print("\n" + "="*80)
        print("RESULT: AI FAILED, USING KEYWORD FALLBACK")
        print("="*80)
        
        # Step 2b: Keyword-based fallback
        keyword_selected = simulate_keyword_based_selection(intent)
        
        if keyword_selected:
            print(f"\nSelected {len(keyword_selected)} files:")
            for file_info in keyword_selected:
                print(f"  - {file_info['path']}")
            return keyword_selected
        else:
            print("\n" + "="*80)
            print("RESULT: NO FILES FOUND")
            print("="*80)
            print("This is the error you're seeing!")
            print("\nPossible reasons:")
            print("1. AI response not in expected format")
            print("2. Keyword matching too strict")
            print("3. Threshold too high")
            print("4. No files match the criteria")
            return []

def analyze_problem():
    """Analyze what's going wrong."""
    print("\n" + "="*80)
    print("PROBLEM ANALYSIS")
    print("="*80)
    
    print("\nLet's check what happens with the actual user input:")
    print(f"User: '{USER_INPUT}'")
    
    # Check keyword extraction
    print("\n1. Keyword Extraction:")
    keywords = ["route", "router", "routing", "navigation", "link", "path", "page", "component", "app"]
    print(f"   AI Keywords: {keywords}")
    
    # Check file matching
    print("\n2. File Matching:")
    for file_info in SIMULATED_REPO_FILES:
        name_lower = file_info["name"].lower()
        path_lower = file_info["path"].lower()
        
        matches = []
        for keyword in keywords:
            if keyword in name_lower or keyword in path_lower:
                matches.append(keyword)
        
        if matches:
            print(f"   {file_info['path']}: matches {matches}")
        else:
            print(f"   {file_info['path']}: NO MATCH")
    
    print("\n3. The Problem:")
    print("   - Files like 'App.js', 'Header.js' don't contain routing keywords")
    print("   - But they DO contain routing logic!")
    print("   - Keyword matching fails because filenames don't match")
    
    print("\n4. The Solution:")
    print("   - AI should analyze file PURPOSE, not just names")
    print("   - AI should know App.js typically has routing")
    print("   - AI should understand semantic relationships")
    
    print("\n5. Current Issue:")
    print("   - AI might not be returning proper JSON")
    print("   - OR AI is not being called at all")
    print("   - OR AI response parsing is failing")

if __name__ == "__main__":
    # Run simulation
    result = simulate_complete_flow()
    
    # Analyze
    analyze_problem()
    
    print("\n" + "="*80)
    print("SIMULATION COMPLETE")
    print("="*80)
    
    if result:
        print(f"✓ SUCCESS: Found {len(result)} files")
    else:
        print("✗ FAILURE: No files found (this is your error)")
