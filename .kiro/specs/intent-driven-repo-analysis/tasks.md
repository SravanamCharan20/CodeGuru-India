# Implementation Plan: Intent-Driven Repository Analysis System

## Overview

This implementation plan breaks down the Intent-Driven Repository Analysis System into incremental, testable tasks. The system transforms CodeGuru India from a single-file analyzer into an intelligent repository analysis platform that interprets user learning goals, selects relevant files, performs multi-file analysis, and generates personalized learning materials with complete code traceability.

The implementation follows a bottom-up approach: foundation components first (data models, core analyzers), then integration layers, then UI components, with testing integrated throughout.

## Tasks

- [x] 1. Set up project structure and core data models
  - Create directory structure for new components
  - Define all data model classes in `models/intent_models.py`
  - Implement UserIntent, IntentScope, FileSelection, SelectionResult, FileRelationship, DataFlow, ExecutionPath, MultiFileAnalysis, CodeEvidence, CodeFlashcard, CodeQuestion, LearningStep, LearningPath, TraceabilityLink, ArtifactTrace dataclasses
  - Set up type hints and validation
  - _Requirements: 1.7, 2.3, 3.7, 4.6, 5.7, 6.7, 7.6, 8.1, 8.2_

- [ ]* 1.1 Write property test for data model validation
  - **Property 1: Complete Intent Extraction**
  - **Validates: Requirements 1.1, 1.2, 1.3, 1.4, 1.7**

- [x] 2. Implement Intent Interpreter component
  - [x] 2.1 Create IntentInterpreter class in `analyzers/intent_interpreter.py`
    - Implement `interpret_intent()` method using LangChainOrchestrator
    - Extract primary_intent, secondary_intents, scope, audience_level, technologies
    - Calculate confidence_score based on clarity of user input
    - Support all intent categories: learn_specific_feature, interview_preparation, architecture_understanding, generate_learning_materials, focus_on_technology, backend_flow_analysis, frontend_flow_analysis
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.7_

  - [x] 2.2 Implement ambiguity detection and clarification
    - Implement `generate_clarification_questions()` method
    - Implement `refine_intent()` method to process user responses
    - Detect when confidence_score < 0.7 and trigger clarification
    - _Requirements: 1.6, 10.1, 10.4_

  - [x] 2.3 Implement intent suggestion generation
    - Implement `suggest_intents()` method based on repository context
    - Analyze repository languages, file structure, and common patterns
    - Generate 3-5 relevant intent suggestions
    - _Requirements: 10.2_


  - [ ]* 2.4 Write property tests for Intent Interpreter
    - **Property 1: Complete Intent Extraction**
    - **Property 2: Ambiguity Detection and Clarification**
    - **Property 24: Intent Suggestion Generation**
    - **Validates: Requirements 1.1-1.7, 10.1, 10.2, 10.4**

  - [ ]* 2.5 Write unit tests for Intent Interpreter
    - Test authentication goal interpretation
    - Test architecture understanding goal
    - Test ambiguous input handling
    - Test edge cases (empty input, very long input)
    - _Requirements: 1.1-1.7_

- [x] 3. Implement File Selector component
  - [x] 3.1 Create FileSelector class in `analyzers/file_selector.py`
    - Implement `select_files()` method
    - Implement `calculate_relevance_score()` using multi-factor algorithm
    - Score based on: file name matching (0-0.3), path matching (0-0.2), content analysis (0-0.3), file importance (0-0.2)
    - Filter out config files, build artifacts, dependency folders unless explicitly requested
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

  - [x] 3.2 Implement file prioritization and explanation
    - Implement `explain_selection()` method for each selected file
    - Prioritize files by relevance_score and file_role (entry_point, core_logic, utility, model, view, controller)
    - Implement `suggest_alternative_intents()` when no files match
    - _Requirements: 2.6, 2.7, 2.8_

  - [ ]* 3.3 Write property tests for File Selector
    - **Property 3: File Relevance Scoring Bounds**
    - **Property 4: Relevant File Selection**
    - **Property 5: File Exclusion Filtering**
    - **Property 6: Selection Explanation Completeness**
    - **Property 7: File Priority Ordering**
    - **Validates: Requirements 2.1-2.8**

  - [ ]* 3.4 Write unit tests for File Selector
    - Test relevance scoring with different file types
    - Test exclusion of node_modules, venv, dist folders
    - Test empty repository handling
    - Test no matching files scenario
    - _Requirements: 2.1-2.8_

- [ ] 4. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Implement Multi-File Analyzer component
  - [x] 5.1 Create MultiFileAnalyzer class in `analyzers/multi_file_analyzer.py`
    - Implement `analyze_files()` method using CodeAnalyzer for individual files
    - Extract functions, classes, imports from each file
    - Preserve file_path and line_number for traceability
    - Handle analysis errors gracefully (continue with remaining files)
    - _Requirements: 3.1, 3.4, 3.9, 15.3_

  - [x] 5.2 Implement relationship detection
    - Implement `detect_relationships()` method
    - Identify imports, calls, extends, implements, uses relationships
    - Build FileRelationship objects with source, target, type, details
    - _Requirements: 3.2, 3.3_

  - [x] 5.3 Implement dependency graph construction
    - Implement `build_dependency_graph()` method
    - Create directed graph from relationships
    - Validate graph structure (all nodes in analyzed_files)
    - _Requirements: 3.7_

  - [x] 5.4 Implement data flow and execution path analysis
    - Implement `identify_data_flows()` method
    - Implement `identify_execution_paths()` method based on intent
    - Track data movement between files with line numbers
    - Identify entry points and trace execution
    - _Requirements: 3.2, 3.3, 3.8_

  - [x] 5.5 Implement cross-file pattern detection and concept extraction
    - Implement `detect_cross_file_patterns()` method
    - Implement `extract_key_concepts()` method with categorization
    - Detect design patterns spanning multiple files
    - Categorize concepts: architecture, patterns, data_structures, algorithms, functions, classes
    - _Requirements: 3.5, 3.6, 4.1, 4.2, 4.3_

  - [ ]* 5.6 Write property tests for Multi-File Analyzer
    - **Property 8: Complete File Analysis**
    - **Property 9: Dependency Graph Validity**
    - **Property 10: Traceability Preservation**
    - **Property 11: Concept Categorization**
    - **Property 12: Concept Evidence Traceability**
    - **Property 31: Analysis Error Recovery**
    - **Validates: Requirements 3.1-3.9, 4.1-4.3, 15.3**

  - [ ]* 5.7 Write unit tests for Multi-File Analyzer
    - Test single file analysis
    - Test relationship detection between files
    - Test dependency graph with circular dependencies
    - Test syntax error recovery
    - Test data flow identification
    - _Requirements: 3.1-3.9_

- [x] 6. Implement Traceability Manager component
  - [x] 6.1 Create TraceabilityManager class in `learning/traceability_manager.py`
    - Implement `register_artifact()` method
    - Implement `get_artifact_trace()` method
    - Implement `get_artifacts_for_code()` method
    - Store artifact-to-code and code-to-artifact mappings
    - _Requirements: 8.1, 8.2_

  - [x] 6.2 Implement validation and code change detection
    - Implement `validate_artifact()` method
    - Implement `verify_evidence_exists()` method
    - Implement `mark_artifacts_outdated()` when code changes
    - Implement `get_code_snippet()` for evidence retrieval
    - _Requirements: 8.3, 8.4, 8.5, 8.7_

  - [ ]* 6.3 Write property tests for Traceability Manager
    - **Property 20: Universal Artifact Traceability**
    - **Property 21: Code Change Invalidation**
    - **Validates: Requirements 8.1-8.7**

  - [ ]* 6.4 Write unit tests for Traceability Manager
    - Test artifact registration
    - Test bidirectional lookup (artifact->code, code->artifact)
    - Test validation with modified code
    - Test code snippet retrieval
    - _Requirements: 8.1-8.7_

- [ ] 7. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 8. Implement Learning Artifact Generator component
  - [x] 8.1 Create LearningArtifactGenerator class in `generators/learning_artifact_generator.py`
    - Initialize with FlashcardManager, QuizEngine, LangChainOrchestrator
    - Implement `_extract_code_evidence()` helper method
    - Ensure all artifacts have code evidence before creation
    - _Requirements: 8.3, 8.4_

  - [x] 8.2 Implement flashcard generation
    - Implement `generate_flashcards()` method
    - Generate flashcards for functions, classes, patterns, data flows
    - Adjust difficulty based on audience_level
    - Create CodeFlashcard objects with code_evidence
    - Integrate with existing FlashcardManager for storage
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8_

  - [ ]* 8.3 Write property tests for flashcard generation
    - **Property 13: Comprehensive Flashcard Generation**
    - **Property 14: Flashcard Difficulty Alignment**
    - **Validates: Requirements 5.1-5.8**

  - [x] 8.4 Implement quiz generation
    - Implement `generate_quiz()` method
    - Generate questions about function behavior, code flow, patterns, architecture
    - Adjust difficulty based on audience_level
    - Create CodeQuestion objects with code_evidence and detailed explanations
    - Integrate with existing QuizEngine
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8_

  - [ ]* 8.5 Write property tests for quiz generation
    - **Property 15: Comprehensive Quiz Generation**
    - **Property 16: Quiz Difficulty Alignment**
    - **Property 17: Quiz Explanation Completeness**
    - **Validates: Requirements 6.1-6.8**

  - [x] 8.6 Implement learning path generation
    - Implement `generate_learning_path()` method
    - Order steps from foundational to advanced concepts
    - Order based on code dependencies (topological sort)
    - Include estimated_time_minutes, recommended_files, code_evidence for each step
    - Create LearningPath with ordered LearningStep objects
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7_

  - [ ]* 8.7 Write property tests for learning path generation
    - **Property 18: Learning Path Ordering**
    - **Property 19: Learning Step Completeness**
    - **Validates: Requirements 7.1-7.7**

  - [x] 8.8 Implement concept summary generation
    - Implement `generate_concept_summary()` method
    - Organize concepts by category with code references
    - Prioritize concepts based on intent relevance
    - Exclude generic concepts not demonstrated in code
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

  - [x] 8.9 Implement parser/serializer detection and round-trip properties
    - Detect parser implementations (parse/decode/deserialize patterns)
    - Detect pretty printers (print/format/encode patterns)
    - Generate quiz questions about round-trip properties
    - Generate flashcards about parser-printer relationships
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5, 13.6, 13.7_

  - [ ]* 8.10 Write property tests for parser detection
    - **Property 27: Parser Detection and Round-Trip Properties**
    - **Property 28: Parser-Printer Relationship Detection**
    - **Validates: Requirements 13.1-13.7**

  - [x] 8.11 Implement fallback artifact generation
    - Implement `generate_basic_flashcards()` fallback method
    - Implement `generate_basic_quiz()` fallback method
    - Use when AI service fails
    - Generate simple artifacts from code structure
    - _Requirements: 15.4_

  - [ ]* 8.12 Write property test for graceful degradation
    - **Property 32: Graceful Artifact Generation Degradation**
    - **Validates: Requirements 15.4**

  - [ ]* 8.13 Write unit tests for Learning Artifact Generator
    - Test flashcard generation from functions
    - Test quiz generation from data flows
    - Test learning path ordering with dependencies
    - Test concept summary categorization
    - Test parser detection
    - Test fallback generation
    - _Requirements: 4.1-4.6, 5.1-5.8, 6.1-6.8, 7.1-7.7, 13.1-13.7, 15.4_

- [x] 9. Implement multi-language support
  - [x] 9.1 Add language parameter to all artifact generation methods
    - Update `generate_flashcards()` to accept language parameter
    - Update `generate_quiz()` to accept language parameter
    - Update `generate_learning_path()` to accept language parameter
    - Update `generate_concept_summary()` to accept language parameter
    - _Requirements: 11.1_

  - [x] 9.2 Implement language-specific prompts for LangChain
    - Create prompt templates for English, Hindi, Telugu
    - Ensure code snippets remain in original language
    - Implement language switching and regeneration
    - _Requirements: 11.2, 11.3, 11.4, 11.5, 11.6_

  - [ ]* 9.3 Write property tests for multi-language support
    - **Property 25: Language Consistency**
    - **Property 26: Language Switching Regeneration**
    - **Validates: Requirements 11.1-11.6**

  - [ ]* 9.4 Write unit tests for multi-language support
    - Test flashcard generation in Hindi
    - Test quiz generation in Telugu
    - Test code snippet preservation across languages
    - Test language switching
    - _Requirements: 11.1-11.6_

- [ ] 10. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 11. Implement Repository Manager component
  - [x] 11.1 Create RepositoryManager class in `analyzers/repository_manager.py`
    - Initialize with RepoAnalyzer and max_size_mb limit
    - Implement `validate_repository()` method
    - Implement `get_supported_languages()` method
    - _Requirements: 9.7_

  - [x] 11.2 Implement GitHub upload
    - Implement `upload_from_github()` method
    - Validate GitHub URL format
    - Clone repository using RepoAnalyzer
    - Handle authentication errors, network errors
    - _Requirements: 9.1, 15.1_

  - [x] 11.3 Implement ZIP and folder upload
    - Implement `upload_from_zip()` method
    - Implement `upload_from_folder()` method
    - Validate file size limits
    - Extract and validate contents
    - _Requirements: 9.2, 9.3, 9.5_

  - [x] 11.4 Implement repository validation
    - Check for supported code files (.py, .js, .ts, .java, .cpp, .go, .rb)
    - Display repository structure to user
    - Store repository temporarily for analysis
    - _Requirements: 9.4, 9.6, 9.8_

  - [ ]* 11.5 Write property tests for Repository Manager
    - **Property 22: Repository Validation**
    - **Property 23: Repository Storage**
    - **Validates: Requirements 9.1-9.8, 15.1**

  - [ ]* 11.6 Write unit tests for Repository Manager
    - Test GitHub URL validation
    - Test ZIP file validation
    - Test size limit enforcement
    - Test supported language detection
    - Test empty repository handling
    - _Requirements: 9.1-9.8_

- [x] 12. Implement Session Manager extensions
  - [x] 12.1 Extend session state schema
    - Add current_repository field
    - Add current_intent field
    - Add file_selection field
    - Add multi_file_analysis field
    - Add learning_artifacts field
    - Add traceability field
    - Add analysis_history field
    - _Requirements: 14.1, 14.2, 14.3, 14.4_

  - [x] 12.2 Implement session persistence methods
    - Implement save methods for all new fields
    - Implement load methods for all new fields
    - Implement progress tracking for learning paths
    - Implement flashcard review schedule persistence
    - Implement quiz score persistence
    - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5_

  - [x] 12.3 Implement multi-analysis support
    - Store multiple repository analyses in analysis_history
    - Allow switching between analyses
    - Provide dashboard showing progress across repositories
    - _Requirements: 14.6, 14.7_

  - [ ]* 12.4 Write property tests for Session Manager
    - **Property 29: Session State Round-Trip**
    - **Property 30: Multi-Analysis Coexistence**
    - **Validates: Requirements 14.1-14.7**

  - [ ]* 12.5 Write unit tests for Session Manager
    - Test session save and load
    - Test progress tracking
    - Test multi-analysis storage
    - Test session restoration after browser refresh
    - _Requirements: 14.1-14.7_

- [x] 13. Implement error handling and validation
  - [x] 13.1 Create error handling utilities in `utils/error_handling.py`
    - Define error message templates
    - Implement `validate_repository_upload()` function
    - Implement `display_error()` function for user-friendly messages
    - Implement retry logic with exponential backoff for AI services
    - _Requirements: 15.1, 15.2, 15.5, 15.6_

  - [x] 13.2 Add error handling to all components
    - Add try-catch blocks with graceful degradation
    - Log errors with context (no sensitive data)
    - Provide specific error messages and suggestions
    - Handle AI service unavailability
    - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5, 15.6, 15.7_

  - [ ]* 13.3 Write property test for input validation
    - **Property 33: Input Validation Feedback**
    - **Validates: Requirements 15.5**

  - [ ]* 13.4 Write unit tests for error handling
    - Test invalid GitHub URL handling
    - Test repository size limit enforcement
    - Test no code files error
    - Test AI service unavailable handling
    - Test file analysis error recovery
    - _Requirements: 15.1-15.7_

- [ ] 14. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 15. Implement UI components
  - [x] 15.1 Create Intent Input component in `ui/intent_input.py`
    - Text area for natural language intent
    - Display suggested intents based on repository
    - Show clarification dialog when needed
    - Display interpreted intent for confirmation
    - Allow intent refinement
    - _Requirements: 10.1, 10.2, 10.3, 10.5, 10.6, 12.2_

  - [x] 15.2 Create File Selection View in `ui/file_selection_view.py`
    - Display selected files with relevance scores
    - Show selection reasons for each file
    - Allow manual file inclusion/exclusion
    - Visualize file importance with color coding
    - _Requirements: 2.6, 10.5, 12.3_

  - [x] 15.3 Create Multi-File Analysis View in `ui/multi_file_analysis_view.py`
    - Display dependency graph visualization using networkx/graphviz
    - Show data flow diagrams
    - Display execution paths
    - Show cross-file patterns
    - _Requirements: 12.6_

  - [x] 15.4 Create Code Evidence Viewer in `ui/code_evidence_viewer.py`
    - Display code snippets with syntax highlighting
    - Show file path and line numbers
    - Provide "Jump to File" functionality
    - Show related artifacts for code
    - _Requirements: 8.5, 12.5_

  - [x] 15.5 Create Learning Artifacts Dashboard in `ui/learning_artifacts_dashboard.py`
    - Unified view of flashcards, quizzes, learning paths
    - Navigation between sections (concept summary, flashcards, quizzes, learning path)
    - Filter by concept category
    - Show traceability status
    - Progress tracking display
    - Provide concise mode toggle
    - _Requirements: 12.1, 12.4, 12.5, 12.7, 14.7_

  - [x] 15.6 Create Repository Upload Screen in `ui/repository_upload.py`
    - GitHub URL input with upload button
    - ZIP file upload with file chooser
    - Folder selection with browse button
    - Display supported languages and size limit
    - Show upload progress
    - Display repository structure after upload
    - _Requirements: 9.1, 9.2, 9.3, 9.6, 12.1_

  - [x] 15.7 Integrate UI components into main Streamlit app
    - Update `app.py` to include new workflow
    - Add navigation between upload, intent, selection, analysis, results
    - Implement responsive design for different screen sizes
    - Add visual feedback and progress indicators
    - _Requirements: 12.1-12.7_

  - [ ]* 15.8 Write integration tests for UI components
    - Test complete user flow from upload to artifact viewing
    - Test intent clarification dialog
    - Test file selection modification
    - Test code evidence viewer
    - Test session persistence across page refreshes
    - _Requirements: 9.1-9.8, 10.1-10.6, 12.1-12.7, 14.1-14.7_

- [x] 16. Integration and end-to-end testing
  - [x] 16.1 Create end-to-end test suite in `tests/integration/test_end_to_end_flow.py`
    - Test complete flow: upload → intent → selection → analysis → artifacts
    - Test with sample repositories in different languages
    - Test with different intent types
    - Verify traceability throughout the flow
    - _Requirements: All requirements_

  - [x] 16.2 Test AI integration
    - Test LangChainOrchestrator integration with all components
    - Test retry logic and error handling
    - Test fallback generation when AI fails
    - _Requirements: 15.4, 15.6_

  - [x] 16.3 Test session persistence
    - Test save and restore across browser sessions
    - Test multi-analysis storage and retrieval
    - Test progress tracking persistence
    - _Requirements: 14.1-14.7_

  - [ ]* 16.4 Run all property tests with CI configuration
    - Execute all 33 property tests with 100 iterations each
    - Verify all properties pass
    - Generate coverage report
    - _Requirements: All requirements_

- [ ] 17. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 18. Documentation and deployment preparation
  - [x] 18.1 Create API documentation
    - Document all public methods and classes
    - Add docstrings with examples
    - Create API reference guide
    - _Requirements: All requirements_

  - [x] 18.2 Create user guide
    - Write step-by-step usage instructions
    - Add screenshots of UI components
    - Document supported languages and features
    - Create troubleshooting section
    - _Requirements: All requirements_

  - [x] 18.3 Update README and configuration
    - Update README with new features
    - Add installation instructions for new dependencies
    - Update requirements.txt
    - Configure CI/CD pipeline for automated testing
    - _Requirements: All requirements_

## Notes

- Tasks marked with `*` are optional testing tasks and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation throughout implementation
- Property tests validate universal correctness properties across all inputs
- Unit tests validate specific examples, edge cases, and error conditions
- The implementation uses Python as specified in the design document
- All components integrate with existing CodeGuru India infrastructure (CodeAnalyzer, RepoAnalyzer, FlashcardManager, QuizEngine, LangChainOrchestrator, SessionManager)
- Error handling and graceful degradation are built into each component
- Complete code traceability is maintained throughout the system
