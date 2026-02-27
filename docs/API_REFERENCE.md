# API Reference - Intent-Driven Repository Analysis

Complete API documentation for all components of the Intent-Driven Repository Analysis System.

## Table of Contents

1. [Core Components](#core-components)
2. [Data Models](#data-models)
3. [Analyzers](#analyzers)
4. [Generators](#generators)
5. [UI Components](#ui-components)
6. [Utilities](#utilities)

---

## Core Components

### IntentDrivenOrchestrator

Main orchestrator that coordinates the complete workflow.

```python
from analyzers.intent_driven_orchestrator import IntentDrivenOrchestrator

orchestrator = IntentDrivenOrchestrator(
    repository_manager=repo_manager,
    intent_interpreter=intent_interpreter,
    file_selector=file_selector,
    multi_file_analyzer=multi_file_analyzer,
    learning_artifact_generator=artifact_generator,
    traceability_manager=traceability_manager,
    session_manager=session_manager
)
```

#### Methods

**analyze_repository_with_intent(repo_path, user_input, language="english")**

Complete workflow from intent interpretation to artifact generation.

- **Parameters:**
  - `repo_path` (str): Path to repository
  - `user_input` (str): User's natural language learning goal
  - `language` (str): Output language (english, hindi, telugu)

- **Returns:** Dictionary with status and results
  - `status`: 'success', 'clarification_needed', 'no_files_found', or 'error'
  - `intent`: UserIntent object
  - `flashcards`: List of CodeFlashcard objects
  - `quiz`: Quiz dictionary
  - `learning_path`: LearningPath object
  - `concept_summary`: Dictionary with categorized concepts

**Example:**
```python
result = orchestrator.analyze_repository_with_intent(
    repo_path="/path/to/repo",
    user_input="I want to learn how authentication works",
    language="english"
)

if result['status'] == 'success':
    flashcards = result['flashcards']
    quiz = result['quiz']
```

---

## Data Models

### UserIntent

Represents user's learning intent.

```python
from models.intent_models import UserIntent, IntentScope

intent = UserIntent(
    primary_intent="learn_authentication",
    secondary_intents=["security", "best_practices"],
    scope=IntentScope(scope_type="full_repository"),
    audience_level="intermediate",
    technologies=["Python", "Flask"],
    confidence_score=0.85
)
```

**Attributes:**
- `primary_intent` (str): Main learning goal
- `secondary_intents` (List[str]): Additional goals
- `scope` (IntentScope): Analysis scope
- `audience_level` (str): beginner, intermediate, or advanced
- `technologies` (List[str]): Relevant technologies
- `confidence_score` (float): 0.0 to 1.0

### CodeFlashcard

Flashcard with code evidence.

```python
from models.intent_models import CodeFlashcard, CodeEvidence

flashcard = CodeFlashcard(
    id="unique_id",
    front="What does authenticate_user() do?",
    back="Verifies user credentials",
    topic="Authentication",
    difficulty="intermediate",
    code_evidence=[evidence],
    concept_category="functions"
)
```

### LearningPath

Structured learning path with ordered steps.

```python
from models.intent_models import LearningPath, LearningStep

path = LearningPath(
    path_id="path_123",
    title="Learning Path: Authentication",
    description="Master authentication concepts",
    total_steps=5,
    estimated_total_time_minutes=100,
    steps=[step1, step2, ...],
    difficulty_level="intermediate"
)
```

---

## Analyzers

### IntentInterpreter

Interprets natural language learning goals.

```python
from analyzers.intent_interpreter import IntentInterpreter

interpreter = IntentInterpreter(langchain_orchestrator=orchestrator)
```

**Methods:**

**interpret_intent(user_input, repo_context)**

Interprets user's learning goal.

```python
intent = interpreter.interpret_intent(
    user_input="I want to learn authentication",
    repo_context={'languages': ['Python'], 'file_count': 50}
)
```

**generate_clarification_questions(intent)**

Generates questions when intent is ambiguous.

```python
questions = interpreter.generate_clarification_questions(intent)
# Returns: ["Which authentication method?", "Frontend or backend?"]
```

**suggest_intents(repo_context)**

Suggests learning goals based on repository.

```python
suggestions = interpreter.suggest_intents(repo_context)
# Returns: ["Learn authentication flow", "Understand database schema", ...]
```

### FileSelector

Selects relevant files based on intent.

```python
from analyzers.file_selector import FileSelector

selector = FileSelector(code_analyzer=code_analyzer)
```

**Methods:**

**select_files(intent, repo_context)**

Selects files relevant to learning goal.

```python
selection_result = selector.select_files(intent, repo_context)
# Returns SelectionResult with selected_files and explanations
```

**calculate_relevance_score(file_info, intent)**

Calculates relevance score (0.0 to 1.0) for a file.

```python
score = selector.calculate_relevance_score(file_info, intent)
# Returns: 0.85
```

### MultiFileAnalyzer

Analyzes multiple files and their relationships.

```python
from analyzers.multi_file_analyzer import MultiFileAnalyzer

analyzer = MultiFileAnalyzer(code_analyzer=code_analyzer)
```

**Methods:**

**analyze_files(selected_files, repo_path, intent)**

Analyzes selected files and extracts concepts.

```python
analysis = analyzer.analyze_files(selected_files, repo_path, intent)
# Returns MultiFileAnalysis with relationships, concepts, etc.
```

**detect_relationships(file_analyses)**

Detects relationships between files.

```python
relationships = analyzer.detect_relationships(file_analyses)
# Returns: [FileRelationship(source='a.py', target='b.py', type='imports')]
```

---

## Generators

### LearningArtifactGenerator

Generates flashcards, quizzes, and learning paths.

```python
from generators.learning_artifact_generator import LearningArtifactGenerator

generator = LearningArtifactGenerator(
    flashcard_manager=flashcard_manager,
    quiz_engine=quiz_engine,
    langchain_orchestrator=orchestrator
)
```

**Methods:**

**generate_flashcards(multi_file_analysis, intent, language="english")**

Generates flashcards from analysis.

```python
flashcards = generator.generate_flashcards(
    multi_file_analysis=analysis,
    intent=intent,
    language="hindi"
)
```

**generate_quiz(multi_file_analysis, intent, num_questions=10, language="english")**

Generates quiz questions.

```python
quiz = generator.generate_quiz(
    multi_file_analysis=analysis,
    intent=intent,
    num_questions=10,
    language="telugu"
)
```

**generate_learning_path(multi_file_analysis, intent, language="english")**

Generates ordered learning path.

```python
path = generator.generate_learning_path(
    multi_file_analysis=analysis,
    intent=intent,
    language="english"
)
```

**generate_concept_summary(multi_file_analysis, intent, language="english")**

Generates categorized concept summary.

```python
summary = generator.generate_concept_summary(
    multi_file_analysis=analysis,
    intent=intent,
    language="english"
)
```

---

## UI Components

### Repository Upload

```python
from ui.repository_upload import render_repository_upload

render_repository_upload(repository_manager, session_manager)
```

### Intent Input

```python
from ui.intent_input import render_intent_input

render_intent_input(intent_interpreter, session_manager, on_intent_confirmed=callback)
```

### Learning Artifacts Dashboard

```python
from ui.learning_artifacts_dashboard import render_learning_artifacts_dashboard

render_learning_artifacts_dashboard(session_manager)
```

---

## Utilities

### Error Handling

```python
from utils.error_handling import (
    display_error,
    validate_repository_upload,
    retry_with_exponential_backoff
)

# Display user-friendly error
error_msg = display_error('invalid_github_url')

# Validate upload
result = validate_repository_upload('github', url, max_size_mb=100)

# Retry with backoff
@retry_with_exponential_backoff(max_retries=3)
def call_ai_service():
    # Your code here
    pass
```

### Traceability Manager

```python
from learning.traceability_manager import TraceabilityManager

manager = TraceabilityManager()

# Register artifact
manager.register_artifact(
    artifact_id="flashcard_1",
    artifact_type="flashcard",
    code_evidence=[evidence]
)

# Get trace
trace = manager.get_artifact_trace("flashcard_1")

# Reverse lookup
artifacts = manager.get_artifacts_for_code("auth.py", 1, 10)
```

---

## Language Support

All artifact generation methods support three languages:

- **english**: English
- **hindi**: हिंदी (Hindi)
- **telugu**: తెలుగు (Telugu)

**Example:**
```python
# Generate in Hindi
flashcards = generator.generate_flashcards(analysis, intent, language="hindi")

# Generate in Telugu
quiz = generator.generate_quiz(analysis, intent, language="telugu")
```

**Note:** Code snippets remain in their original programming language; only explanations are translated.

---

## Error Handling

All components include comprehensive error handling:

```python
try:
    result = orchestrator.analyze_repository_with_intent(...)
    if result['status'] == 'error':
        print(f"Error: {result['error']}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

Common error statuses:
- `clarification_needed`: Intent needs more details
- `no_files_found`: No relevant files matched
- `error`: Analysis failed

---

## Best Practices

1. **Always check result status** before accessing data
2. **Handle clarification requests** by prompting user for more details
3. **Use appropriate language** for your target audience
4. **Validate inputs** before passing to components
5. **Store session state** for persistence across page refreshes
6. **Register artifacts** with traceability manager for code linking

---

## Examples

### Complete Workflow Example

```python
# Initialize components
orchestrator = IntentDrivenOrchestrator(...)

# Upload repository
repo_result = repo_manager.upload_from_github("https://github.com/user/repo")
session_manager.set_current_repository(
    repo_path=repo_result['repo_path'],
    repo_analysis=repo_result['repo_analysis']
)

# Analyze with intent
result = orchestrator.analyze_repository_with_intent(
    repo_path=repo_result['repo_path'],
    user_input="I want to learn authentication",
    language="english"
)

# Handle results
if result['status'] == 'success':
    flashcards = result['flashcards']
    quiz = result['quiz']
    learning_path = result['learning_path']
    
    # Use artifacts
    for flashcard in flashcards:
        print(f"Q: {flashcard.front}")
        print(f"A: {flashcard.back}")
elif result['status'] == 'clarification_needed':
    questions = result['questions']
    # Prompt user for answers
```

---

For more examples, see the [User Guide](USER_GUIDE.md) and [Integration Tests](../tests/integration/).
