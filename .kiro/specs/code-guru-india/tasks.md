# Implementation Plan: CodeGuru India

## Overview

This implementation plan follows a UI-first approach, building out the Streamlit interface components before integrating backend functionality. This allows for rapid visual feedback and iterative refinement of the user experience. The system is built using Python 3.9+, Streamlit for UI, AWS Bedrock for LLM capabilities, and LangChain for orchestration.

## Tasks

- [x] 1. Project setup and configuration
  - Create project directory structure (app.py, config.py, ui/, analyzers/, engines/, ai/, learning/, generators/)
  - Set up requirements.txt with dependencies (streamlit, boto3, langchain, hypothesis, pytest)
  - Create .streamlit/config.toml for theme and server configuration
  - Create config.py with AWSConfig and AppConfig dataclasses
  - Set up environment variable loading for AWS credentials
  - _Requirements: NFR-9_

- [ ] 2. Core session management (minimal backend)
  - [x] 2.1 Implement SessionManager class in session_manager.py
    - Implement get/set methods for language preference, learning path, uploaded code
    - Implement save_progress() and load_progress() with localStorage integration
    - _Requirements: 13.1, 13.2, 13.3_
  
  - [ ]* 2.2 Write property test for session persistence
    - **Property 40: Preference Persistence**
    - **Validates: Requirements 13.1**
  
  - [ ]* 2.3 Write property test for session state round-trip
    - **Property 42: Session State Round-Trip**
    - **Validates: Requirements 13.3**

- [ ] 3. Main application structure and navigation UI
  - [x] 3.1 Create app.py with main entry point
    - Implement setup_page_config() with page title, icon, and layout
    - Implement initialize_session_state() to set default values
    - Implement basic routing structure
    - _Requirements: 1.1, 1.2_
  
  - [x] 3.2 Build sidebar navigation UI in ui/sidebar.py
    - Create language selector dropdown (English, हिंदी, తెలుగు)
    - Create navigation radio buttons with icons (Home, Upload Code, Learning Paths, Quizzes, Flashcards, Progress)
    - Add user progress indicator
    - Wire language selector to SessionManager
    - _Requirements: 1.1, 1.2, 1.5_
  
  - [ ] 3.3 Write property test for language preference persistence
    - **Property 1: Language Preference Persistence**
    - **Validates: Requirements 1.2**
  
  - [ ] 3.4 Write property test for language switch performance
    - **Property 3: Language Switch Performance**
    - **Validates: Requirements 1.5**

- [ ] 4. Code upload interface UI (no analysis yet)
  - [x] 4.1 Create ui/code_upload.py with upload interface
    - Add file uploader component with supported extensions (.py, .js, .jsx, .ts, .tsx, .java, .cpp, .c, .go, .rb)
    - Add GitHub repository URL text input
    - Add voice input button (placeholder for now)
    - Add analysis options: debugging checkbox, difficulty slider
    - Add "Analyze Code" button (shows placeholder message)
    - Store uploaded file content in session state
    - _Requirements: 3.1, 3.6_
  
  - [x] 4.2 Add file validation UI feedback
    - Display file size validation messages
    - Show supported format messages
    - Display loading spinner during upload
    - _Requirements: 3.5, 3.6_

- [ ] 5. Code explanation view UI (with mock data)
  - [x] 5.1 Create ui/explanation_view.py with tabbed interface
    - Create tabs: Summary, Details, Diagrams, Issues
    - Build Summary tab with mock data (summary text, key concepts, analogies)
    - Build Details tab with mock detailed explanation and code examples
    - Build Diagrams tab with diagram type selector and Mermaid placeholder
    - Build Issues tab with mock issues (critical, warning, suggestion)
    - _Requirements: 4.1, 4.2, 4.3, 5.1, 5.5_
  
  - [x] 5.2 Add diagram download buttons
    - Add PNG and SVG download buttons (placeholder functionality)
    - _Requirements: 10.7_

- [ ] 6. Learning path view UI (with mock data)
  - [x] 6.1 Create ui/learning_path.py with path selection
    - Add learning path selector dropdown (DSA, Backend, Frontend, Full-Stack, AWS)
    - Display progress bar for selected path
    - _Requirements: 9.1, 9.2, 9.3_
  
  - [x] 6.2 Build learning roadmap visualization
    - Create topic cards with status icons (✅ completed, 🔒 locked, 📖 available)
    - Display topic name, description, and "Start" button
    - Show prerequisite relationships visually
    - _Requirements: 9.2, 9.4_
  
  - [x] 6.3 Add milestone achievement display
    - Show certificate/badge placeholder when milestone reached
    - _Requirements: 9.5_

- [ ] 7. Quiz interface UI (with mock data)
  - [x] 7.1 Create ui/quiz_view.py with quiz display
    - Add quiz progress bar
    - Display question counter (Question X of Y)
    - Show question text
    - _Requirements: 8.1, 8.7_
  
  - [x] 7.2 Build answer input components
    - Create multiple choice radio buttons
    - Create code completion text area
    - Create debugging challenge display with code and text area
    - _Requirements: 8.2_
  
  - [x] 7.3 Add quiz navigation and feedback
    - Add Previous/Submit/Next buttons
    - Display timer in sidebar
    - Show immediate feedback on answer submission (mock)
    - Display quiz summary at completion (score, time, correct answers)
    - _Requirements: 8.3, 8.4, 8.7_

- [ ] 8. Flashcard interface UI (with mock data)
  - [x] 8.1 Create ui/flashcard_view.py with flashcard display
    - Add topic and difficulty filter dropdowns
    - Display flashcard counter (Card X of Y)
    - _Requirements: 7.4_
  
  - [x] 8.2 Build flashcard flip interaction
    - Show front of card with "Flip to Back" button
    - Show back of card with "Flip to Front" button
    - Use session state for flip animation
    - _Requirements: 7.2, 7.3_
  
  - [x] 8.3 Add flashcard navigation and rating
    - Add Previous/Next buttons
    - Add difficulty rating slider (Easy, Medium, Hard)
    - Add "Mark Reviewed" button
    - Add "Mark as Mastered" button
    - _Requirements: 7.5, 7.7_

- [ ] 9. Progress dashboard UI (with mock data)
  - [x] 9.1 Create ui/progress_dashboard.py with metrics display
    - Display key metrics in columns: Topics Completed, Avg Quiz Score, Learning Streak, Time Spent
    - Show delta indicators for weekly changes
    - _Requirements: 11.1, 11.2_
  
  - [x] 9.2 Build progress visualizations
    - Add line chart for progress over time
    - Add skill level progress bars for each technology
    - _Requirements: 11.3, 11.4_
  
  - [x] 9.3 Add weekly summary section
    - Display activities completed, time spent, topics learned
    - _Requirements: 11.7_
  
  - [x] 9.4 Add achievement badges display
    - Show achievement icons in grid layout
    - _Requirements: 11.5_

- [x] 10. Checkpoint - UI components complete
  - Verify all UI pages render correctly
  - Test navigation between pages
  - Verify mock data displays properly
  - Ensure all tests pass, ask the user if questions arise

- [ ] 11. AWS Bedrock client setup
  - [x] 11.1 Create ai/bedrock_client.py with BedrockClient class
    - Implement __init__ with AWS configuration
    - Implement invoke_model() method with error handling
    - Implement invoke_model_with_streaming() method
    - Add retry logic with exponential backoff
    - _Requirements: NFR-1, NFR-3_
  
  - [ ]* 11.2 Write unit tests for Bedrock client
    - Test successful invocation with mocked responses
    - Test error handling and retry logic
    - Test streaming responses
    - _Requirements: NFR-3_

- [ ] 12. Prompt management system
  - [x] 12.1 Create ai/prompt_templates.py with PromptManager class
    - Implement get_code_explanation_prompt() with language support
    - Implement get_analogy_generation_prompt() with cultural context
    - Implement get_quiz_generation_prompt()
    - Implement get_debugging_prompt()
    - Implement get_summary_prompt()
    - _Requirements: 4.1, 5.1, 6.1, 8.1_
  
  - [ ]* 12.2 Write unit tests for prompt templates
    - Test prompt generation for each language
    - Test parameter substitution
    - Verify cultural context in analogies
    - _Requirements: 1.3, 6.2_

- [ ] 13. LangChain orchestration layer
  - [x] 13.1 Create ai/langchain_orchestrator.py with LangChainOrchestrator class
    - Implement generate_completion() method
    - Implement generate_with_chain() for different chain types
    - Implement generate_structured_output() with schema validation
    - Add error handling and logging
    - _Requirements: NFR-1, NFR-3_
  
  - [ ]* 13.2 Write unit tests for LangChain orchestrator
    - Test completion generation with mocked LLM
    - Test chain execution
    - Test structured output parsing
    - Test error handling
    - _Requirements: NFR-3_

- [ ] 14. Code analyzer implementation
  - [x] 14.1 Create analyzers/code_analyzer.py with CodeAnalyzer class
    - Implement analyze_file() method
    - Implement extract_structure() using AST parsing
    - Implement identify_patterns() using LangChain
    - Implement detect_issues() for common errors
    - Define CodeAnalysis, CodeStructure, and Issue dataclasses
    - _Requirements: 3.2, 4.1, 4.2, 4.3, 4.4, 5.1, 5.2, 5.3, 5.4_
  
  - [ ]* 14.2 Write property test for file format support
    - **Property 7: File Format Support**
    - **Validates: Requirements 3.1**
  
  - [ ]* 14.3 Write property test for code parsing performance
    - **Property 8: Code Parsing Performance**
    - **Validates: Requirements 3.2**
  
  - [ ]* 14.4 Write property test for structure extraction
    - **Property 12: Structure Extraction Completeness**
    - **Validates: Requirements 4.2**
  
  - [ ]* 14.5 Write property test for issue detection
    - **Property 14: Issue Detection Completeness**
    - **Validates: Requirements 5.1, 5.2, 5.3, 5.4**

- [ ] 15. Repository analyzer implementation
  - [ ] 15.1 Create analyzers/repo_analyzer.py with RepoAnalyzer class
    - Implement analyze_repo() method
    - Implement clone_repo() using GitPython
    - Implement get_file_tree() for directory structure
    - Implement analyze_files() to process all code files
    - Define RepoAnalysis dataclass
    - _Requirements: 3.3, 3.4, 3.7, 4.5_
  
  - [ ]* 15.2 Write property test for repository analysis
    - **Property 9: Repository Analysis Completeness**
    - **Validates: Requirements 3.3, 3.4**
  
  - [ ]* 15.3 Write unit tests for repository analyzer
    - Test cloning with mocked Git operations
    - Test file tree generation
    - Test error handling for invalid URLs
    - _Requirements: 3.5_

- [ ] 16. Explanation engine implementation
  - [ ] 16.1 Create engines/explanation_engine.py with ExplanationEngine class
    - Implement explain_code() method with difficulty levels
    - Implement generate_analogy() with cultural relevance
    - Implement simplify_explanation() for adaptive difficulty
    - Implement explain_with_examples()
    - Define Explanation and CodeExample dataclasses
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_
  
  - [ ]* 16.2 Write property test for analogy inclusion
    - **Property 16: Analogy Inclusion**
    - **Validates: Requirements 6.1**
  
  - [ ]* 16.3 Write property test for example completeness
    - **Property 17: Example Completeness**
    - **Validates: Requirements 6.4**
  
  - [ ]* 16.4 Write property test for explanation simplification
    - **Property 18: Explanation Simplification**
    - **Validates: Requirements 6.5**

- [ ] 17. Integrate code analysis with upload UI
  - [x] 17.1 Wire CodeAnalyzer to code upload interface
    - Replace placeholder with actual analyze_file() call
    - Display real analysis results in explanation view
    - Handle loading states and errors
    - _Requirements: 3.2, 4.1_
  
  - [ ]* 17.2 Write integration test for code upload flow
    - Test file upload → analysis → display pipeline
    - Test error handling for invalid files
    - _Requirements: 3.1, 3.2, 3.5_

- [ ] 18. Diagram generator implementation
  - [ ] 18.1 Create generators/diagram_generator.py with DiagramGenerator class
    - Implement generate_flowchart() for function logic
    - Implement generate_class_diagram() for OOP code
    - Implement generate_architecture_diagram() for projects
    - Implement generate_sequence_diagram() for APIs
    - All methods return valid Mermaid syntax
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_
  
  - [ ]* 18.2 Write property test for Mermaid format compliance
    - **Property 33: Mermaid Format Compliance**
    - **Validates: Requirements 10.5**
  
  - [ ]* 18.3 Write unit tests for diagram generation
    - Test flowchart generation with sample functions
    - Test class diagram generation with sample classes
    - Verify Mermaid syntax validity
    - _Requirements: 10.1, 10.2, 10.3, 10.4_

- [ ] 19. Integrate diagrams with explanation view
  - [ ] 19.1 Wire DiagramGenerator to explanation view
    - Replace placeholder diagrams with real generated diagrams
    - Implement diagram type selection logic
    - Add diagram download functionality (PNG/SVG)
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.7_
  
  - [ ]* 19.2 Write property test for diagram generation completeness
    - **Property 32: Diagram Generation Completeness**
    - **Validates: Requirements 10.1, 10.2, 10.3, 10.4**

- [ ] 20. Voice processor implementation
  - [ ] 20.1 Create ai/voice_processor.py with VoiceProcessor class
    - Implement process_audio() method using AWS Transcribe
    - Implement detect_language() for language detection
    - Implement handle_accent() for regional accent support
    - Define VoiceResult dataclass
    - _Requirements: 2.1, 2.2, 2.5, 2.6_
  
  - [ ]* 20.2 Write property test for voice transcription completeness
    - **Property 4: Voice Transcription Completeness**
    - **Validates: Requirements 2.1, 2.5**
  
  - [ ]* 20.3 Write property test for voice processing performance
    - **Property 5: Voice Processing Performance**
    - **Validates: Requirements 2.6**
  
  - [ ]* 20.4 Write unit tests for voice processor
    - Test audio processing with mocked AWS Transcribe
    - Test language detection
    - Test error handling for unclear audio
    - _Requirements: 2.4_

- [ ] 21. Integrate voice input with upload UI
  - [ ] 21.1 Wire VoiceProcessor to code upload interface
    - Replace voice button placeholder with audio recording
    - Display transcription for user confirmation
    - Process voice query through ExplanationEngine
    - Add visual feedback during processing
    - _Requirements: 2.1, 2.3, 2.5, 2.6_
  
  - [ ]* 21.2 Write integration test for voice query flow
    - Test audio → transcription → explanation pipeline
    - Test error handling for unclear audio
    - _Requirements: 2.1, 2.4, 2.5_

- [ ] 22. Learning path manager implementation
  - [ ] 22.1 Create learning/path_manager.py with LearningPathManager class
    - Define predefined learning paths (DSA, Backend, Frontend, Full-Stack, AWS)
    - Implement get_available_paths()
    - Implement get_path_details()
    - Implement get_next_topic() with recommendation logic
    - Implement check_prerequisites()
    - Implement unlock_topic()
    - Define LearningPath and Topic dataclasses
    - _Requirements: 9.1, 9.2, 9.4, 9.6_
  
  - [ ]* 22.2 Write property test for prerequisite enforcement
    - **Property 29: Prerequisite Enforcement**
    - **Validates: Requirements 9.4**
  
  - [ ]* 22.3 Write property test for topic recommendation
    - **Property 31: Topic Recommendation**
    - **Validates: Requirements 9.6**
  
  - [ ]* 22.4 Write unit tests for learning path manager
    - Test path retrieval
    - Test prerequisite checking logic
    - Test topic unlocking
    - _Requirements: 9.1, 9.2, 9.4_

- [ ] 23. Progress tracker implementation
  - [ ] 23.1 Create learning/progress_tracker.py with ProgressTracker class
    - Implement record_activity() for all activity types
    - Implement get_statistics() for dashboard metrics
    - Implement get_skill_levels() for technology tracking
    - Implement calculate_streak() for daily streak
    - Implement get_weekly_summary()
    - Define ProgressStats and WeeklySummary dataclasses
    - _Requirements: 11.2, 11.3, 11.4, 11.6, 11.7_
  
  - [ ]* 23.2 Write property test for metrics tracking
    - **Property 35: Metrics Tracking**
    - **Validates: Requirements 11.2**
  
  - [ ]* 23.3 Write property test for skill level tracking
    - **Property 36: Skill Level Tracking**
    - **Validates: Requirements 11.4**
  
  - [ ]* 23.4 Write property test for progress persistence
    - **Property 41: Progress Persistence**
    - **Validates: Requirements 13.2**

- [ ] 24. Integrate learning paths with UI
  - [ ] 24.1 Wire LearningPathManager to learning path UI
    - Replace mock data with real learning paths
    - Implement topic unlocking logic
    - Display real progress tracking
    - Show milestone achievements
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_
  
  - [ ]* 24.2 Write property test for learning path roadmap
    - **Property 27: Learning Path Roadmap**
    - **Validates: Requirements 9.2**
  
  - [ ]* 24.3 Write integration test for learning path flow
    - Test path selection → topic completion → progress tracking
    - Test prerequisite enforcement
    - _Requirements: 9.2, 9.3, 9.4_

- [ ] 25. Quiz engine implementation
  - [ ] 25.1 Create engines/quiz_engine.py with QuizEngine class
    - Implement generate_quiz() with multiple question types
    - Implement evaluate_answer() for all question types
    - Implement generate_explanation() for feedback
    - Define Quiz, Question, and EvaluationResult dataclasses
    - _Requirements: 8.1, 8.2, 8.3, 8.4_
  
  - [ ]* 25.2 Write property test for quiz generation
    - **Property 23: Quiz Generation**
    - **Validates: Requirements 8.1**
  
  - [ ]* 25.3 Write property test for quiz feedback completeness
    - **Property 24: Quiz Feedback Completeness**
    - **Validates: Requirements 8.3, 8.4**
  
  - [ ]* 25.4 Write unit tests for quiz engine
    - Test quiz generation for different topics
    - Test answer evaluation for each question type
    - Test explanation generation
    - _Requirements: 8.1, 8.2, 8.3, 8.4_

- [ ] 26. Integrate quizzes with UI
  - [ ] 26.1 Wire QuizEngine to quiz UI
    - Replace mock quiz data with real generated quizzes
    - Implement answer evaluation and feedback display
    - Track quiz scores in ProgressTracker
    - Display quiz summary with real data
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.7_
  
  - [ ]* 26.2 Write property test for quiz score persistence
    - **Property 25: Quiz Score Persistence**
    - **Validates: Requirements 8.5**
  
  - [ ]* 26.3 Write integration test for quiz flow
    - Test quiz generation → answer submission → evaluation → score tracking
    - _Requirements: 8.1, 8.3, 8.5_

- [ ] 27. Flashcard manager implementation
  - [ ] 27.1 Create learning/flashcard_manager.py with FlashcardManager class
    - Implement generate_flashcards() from code analysis
    - Implement create_custom_flashcard()
    - Implement get_flashcards_for_review() with spaced repetition
    - Implement mark_reviewed() with scheduling logic
    - Implement mark_mastered()
    - Define Flashcard dataclass
    - _Requirements: 7.1, 7.4, 7.5, 7.6, 7.7_
  
  - [ ]* 27.2 Write property test for flashcard generation
    - **Property 19: Flashcard Generation**
    - **Validates: Requirements 7.1**
  
  - [ ]* 27.3 Write property test for flashcard organization
    - **Property 20: Flashcard Organization**
    - **Validates: Requirements 7.4**
  
  - [ ]* 27.4 Write property test for mastered flashcard scheduling
    - **Property 22: Mastered Flashcard Scheduling**
    - **Validates: Requirements 7.7**

- [ ] 28. Integrate flashcards with UI
  - [ ] 28.1 Wire FlashcardManager to flashcard UI
    - Replace mock flashcard data with real generated flashcards
    - Implement review tracking and scheduling
    - Implement mastered marking logic
    - Generate flashcards from code analysis
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7_
  
  - [ ]* 28.2 Write property test for flashcard review tracking
    - **Property 21: Flashcard Review Tracking**
    - **Validates: Requirements 7.5**
  
  - [ ]* 28.3 Write integration test for flashcard flow
    - Test flashcard generation → review → scheduling → mastering
    - _Requirements: 7.1, 7.5, 7.7_

- [ ] 29. Integrate progress tracking with dashboard UI
  - [ ] 29.1 Wire ProgressTracker to progress dashboard UI
    - Replace mock metrics with real tracked data
    - Display real progress charts
    - Show real skill levels
    - Display real weekly summaries
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.6, 11.7_
  
  - [ ]* 29.2 Write property test for weekly summary generation
    - **Property 38: Weekly Summary Generation**
    - **Validates: Requirements 11.7**
  
  - [ ]* 29.3 Write integration test for progress tracking
    - Test activity recording → metrics update → dashboard display
    - _Requirements: 11.2, 11.3_

- [ ] 30. Multi-language support implementation
  - [ ] 30.1 Create language translation system
    - Create translation dictionaries for UI text (English, Hindi, Telugu)
    - Implement language switching logic in all UI components
    - Update all prompt templates to support multiple languages
    - _Requirements: 1.1, 1.3, 1.4_
  
  - [ ]* 30.2 Write property test for consistent language rendering
    - **Property 2: Consistent Language Rendering**
    - **Validates: Requirements 1.3, 4.6**
  
  - [ ]* 30.3 Write unit tests for language support
    - Test translation for all UI elements
    - Test prompt generation in each language
    - _Requirements: 1.3, 1.4_

- [ ] 31. Tech stack specialization
  - [ ] 31.1 Add framework-specific insights to ExplanationEngine
    - Implement detection for React, Node.js, Express, MongoDB, AWS services
    - Add framework-specific prompt templates
    - Include Indian tech industry best practices
    - Add relevant examples for e-commerce and fintech
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_
  
  - [ ]* 31.2 Write property test for framework-specific insights
    - **Property 39: Framework-Specific Insights**
    - **Validates: Requirements 12.1, 12.5**

- [ ] 32. Error handling and resilience
  - [ ] 32.1 Implement comprehensive error handling
    - Add input validation for all file uploads
    - Add error handling for AWS Bedrock failures with fallback messages
    - Add error handling for GitHub API failures
    - Add graceful degradation for diagram generation failures
    - Add user-friendly error messages in all languages
    - _Requirements: NFR-3, NFR-4, NFR-6_
  
  - [ ]* 32.2 Write property test for graceful error recovery
    - **Property 44: Graceful Error Recovery**
    - **Validates: Requirements 13.5**
  
  - [ ]* 32.3 Write unit tests for error handling
    - Test file validation errors
    - Test API failure scenarios
    - Test corrupted session data handling
    - _Requirements: NFR-3, NFR-6_

- [ ] 33. Performance optimization
  - [ ] 33.1 Implement caching for LLM responses
    - Cache code analysis results in session state
    - Cache explanation results for repeated queries
    - Implement response time monitoring
    - _Requirements: NFR-1_
  
  - [ ]* 33.2 Write property test for summary generation performance
    - **Property 11: Summary Generation Performance**
    - **Validates: Requirements 4.1**

- [ ] 34. Security hardening
  - [ ] 34.1 Implement security measures
    - Add input sanitization for all user inputs
    - Implement file upload validation for malicious content
    - Ensure code is processed in-memory only (no persistent storage)
    - Add HTTPS enforcement configuration
    - _Requirements: NFR-4, NFR-5_
  
  - [ ]* 34.2 Write unit tests for security measures
    - Test input sanitization
    - Test file validation
    - Test that code is not persisted
    - _Requirements: NFR-4, NFR-5_

- [ ] 35. Final integration and testing
  - [ ] 35.1 End-to-end integration testing
    - Test complete code upload → analysis → explanation flow
    - Test complete learning path → quiz → progress tracking flow
    - Test complete flashcard generation → review → mastering flow
    - Test voice query → explanation flow
    - Test repository analysis flow
    - _Requirements: All_
  
  - [ ] 35.2 Run all property tests
    - Execute all 44 property tests with 100+ iterations each
    - Verify all properties hold
    - _Requirements: All_
  
  - [ ] 35.3 Performance testing
    - Test with files up to 10MB
    - Test with repositories up to 100MB
    - Verify response times meet requirements
    - _Requirements: NFR-1, NFR-2_

- [ ] 36. Deployment preparation
  - [ ] 36.1 Create deployment configuration
    - Create requirements.txt with all dependencies
    - Create .streamlit/config.toml with production settings
    - Create environment variable template
    - Write deployment documentation
    - _Requirements: NFR-8, NFR-9_
  
  - [ ] 36.2 Create Docker configuration (optional)
    - Create Dockerfile for containerized deployment
    - Create docker-compose.yml for local testing
    - _Requirements: NFR-8_

- [ ] 37. Final checkpoint - Complete system verification
  - Verify all UI components work correctly
  - Verify all backend integrations function properly
  - Verify all tests pass (unit, property, integration)
  - Verify multi-language support works across all features
  - Verify error handling works for all edge cases
  - Ensure all tests pass, ask the user if questions arise

## Notes

- Tasks marked with `*` are optional testing tasks and can be skipped for faster MVP
- UI-first approach allows for rapid visual feedback and iterative refinement
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at key milestones
- Property tests validate universal correctness properties with 100+ iterations
- Unit tests validate specific examples, edge cases, and error conditions
- Integration tests validate end-to-end user flows
- All code should follow Python PEP 8 style guidelines
- Mock AWS Bedrock calls in tests to avoid API costs during development
