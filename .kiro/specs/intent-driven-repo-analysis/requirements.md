# Requirements Document

## Introduction

The Intent-Driven Repository Analysis System transforms CodeGuru India from a single-file analyzer into an intelligent repository analysis platform. The system interprets user learning goals, selects relevant code files based on intent, performs multi-file analysis, and generates personalized learning materials (flashcards, quizzes, learning paths) that directly reference the analyzed code. This ensures all learning artifacts are grounded in actual repository code rather than generic theory.

## Glossary

- **Intent_Interpreter**: Component that parses user input to extract learning goals and analysis scope
- **File_Selector**: Component that identifies relevant files based on interpreted intent
- **Multi_File_Analyzer**: Component that analyzes multiple code files and their relationships
- **Learning_Artifact_Generator**: Component that creates flashcards, quizzes, and learning paths from analysis
- **Traceability_Manager**: Component that maintains mappings between learning artifacts and source code
- **Repository**: A collection of code files uploaded by the user
- **User_Intent**: The learning or analysis goal stated by the user
- **Learning_Artifact**: Generated educational content (flashcard, quiz question, or learning path step)
- **Code_Evidence**: Specific code snippets or file references that support a learning artifact
- **Relevance_Score**: Numeric measure of how relevant a file is to the user's intent

## Requirements

### Requirement 1: User Intent Interpretation

**User Story:** As a learner, I want to state my learning goal in natural language, so that the system understands what I want to learn from the repository.

#### Acceptance Criteria

1. WHEN a user provides a learning goal statement, THE Intent_Interpreter SHALL extract the primary intent from the statement
2. WHEN a user provides a learning goal statement, THE Intent_Interpreter SHALL extract any secondary intents from the statement
3. WHEN a user provides a learning goal statement, THE Intent_Interpreter SHALL determine the analysis scope (specific folders, technologies, or entire repository)
4. WHEN a user provides a learning goal statement, THE Intent_Interpreter SHALL identify the target audience level (beginner, intermediate, advanced)
5. THE Intent_Interpreter SHALL support the following intent categories: "learn specific feature", "interview preparation", "architecture understanding", "generate learning materials", "focus on specific technology", "backend flow analysis", "frontend flow analysis"
6. WHEN the user's intent is ambiguous, THE Intent_Interpreter SHALL identify missing information and prompt the user for clarification
7. THE Intent_Interpreter SHALL store the interpreted intent in a structured format with fields for primary_intent, secondary_intents, scope, and audience_level

### Requirement 2: Intent-Driven File Selection

**User Story:** As a learner, I want the system to analyze only files relevant to my learning goal, so that I don't waste time on unrelated code.

#### Acceptance Criteria

1. WHEN the Intent_Interpreter has extracted user intent, THE File_Selector SHALL identify files relevant to the primary intent
2. WHEN the Intent_Interpreter has extracted user intent, THE File_Selector SHALL identify files relevant to any secondary intents
3. THE File_Selector SHALL calculate a Relevance_Score for each file in the Repository based on the user intent
4. THE File_Selector SHALL exclude configuration files, build artifacts, and dependency folders unless explicitly requested by the user
5. WHEN a file has a Relevance_Score below the threshold, THE File_Selector SHALL exclude it from analysis
6. THE File_Selector SHALL provide an explanation for why each selected file is relevant to the user's intent
7. WHEN no files match the user's intent, THE File_Selector SHALL inform the user and suggest alternative intents
8. THE File_Selector SHALL prioritize files based on Relevance_Score and file importance (entry points, core logic)

### Requirement 3: Multi-File Code Analysis

**User Story:** As a learner, I want the system to analyze how multiple files work together, so that I understand the complete flow and relationships in the codebase.

#### Acceptance Criteria

1. WHEN files are selected by the File_Selector, THE Multi_File_Analyzer SHALL extract core logic from each selected file
2. WHEN files are selected by the File_Selector, THE Multi_File_Analyzer SHALL identify data flow between files
3. WHEN files are selected by the File_Selector, THE Multi_File_Analyzer SHALL identify control flow between files
4. THE Multi_File_Analyzer SHALL identify important functions and classes in each file
5. THE Multi_File_Analyzer SHALL detect design patterns used across multiple files
6. THE Multi_File_Analyzer SHALL identify hidden behaviors that emerge from file interactions
7. THE Multi_File_Analyzer SHALL create a dependency graph showing relationships between analyzed files
8. THE Multi_File_Analyzer SHALL identify entry points and execution paths relevant to the user's intent
9. WHEN analyzing files, THE Multi_File_Analyzer SHALL preserve file context including file paths and line numbers for traceability

### Requirement 4: Concept Summary Generation

**User Story:** As a learner, I want a summary of key concepts found in the code, so that I understand the main ideas before diving into details.

#### Acceptance Criteria

1. WHEN the Multi_File_Analyzer completes analysis, THE Learning_Artifact_Generator SHALL extract key concepts from the analyzed code
2. THE Learning_Artifact_Generator SHALL organize concepts by category (architecture, patterns, data structures, algorithms)
3. THE Learning_Artifact_Generator SHALL provide concise explanations for each concept tied to specific code examples
4. THE Learning_Artifact_Generator SHALL prioritize concepts based on relevance to the user's intent
5. THE Learning_Artifact_Generator SHALL exclude generic programming concepts unless they are specifically implemented in the code
6. FOR ALL concepts in the summary, THE Traceability_Manager SHALL maintain references to the source files and line numbers

### Requirement 5: Flashcard Generation from Code

**User Story:** As a learner, I want flashcards generated from the actual code, so that I can memorize key concepts through spaced repetition.

#### Acceptance Criteria

1. WHEN the Multi_File_Analyzer completes analysis, THE Learning_Artifact_Generator SHALL generate flashcards based on analyzed code
2. THE Learning_Artifact_Generator SHALL adjust flashcard difficulty based on the user's audience level
3. THE Learning_Artifact_Generator SHALL create flashcards for important functions with questions about their purpose and parameters
4. THE Learning_Artifact_Generator SHALL create flashcards for classes with questions about their responsibilities and methods
5. THE Learning_Artifact_Generator SHALL create flashcards for design patterns with questions about their implementation
6. THE Learning_Artifact_Generator SHALL create flashcards for data flow with questions about how data moves between components
7. FOR ALL flashcards, THE Traceability_Manager SHALL store references to the specific code snippets that support the flashcard content
8. WHEN displaying a flashcard, THE System SHALL provide a link to view the relevant code snippet

### Requirement 6: Quiz Generation from Code

**User Story:** As a learner, I want quizzes generated from the actual code, so that I can test my understanding of the repository.

#### Acceptance Criteria

1. WHEN the Multi_File_Analyzer completes analysis, THE Learning_Artifact_Generator SHALL generate quiz questions based on analyzed code
2. THE Learning_Artifact_Generator SHALL adjust quiz difficulty based on the user's audience level
3. THE Learning_Artifact_Generator SHALL create multiple-choice questions about function behavior
4. THE Learning_Artifact_Generator SHALL create questions about code flow and execution paths
5. THE Learning_Artifact_Generator SHALL create questions about design patterns and architectural decisions
6. THE Learning_Artifact_Generator SHALL provide detailed explanations for each answer that reference specific code
7. FOR ALL quiz questions, THE Traceability_Manager SHALL store references to the code that validates the correct answer
8. WHEN displaying quiz results, THE System SHALL show the relevant code snippets that explain the correct answer

### Requirement 7: Learning Path Generation

**User Story:** As a learner, I want an ordered learning path, so that I can master the codebase concepts in a logical sequence.

#### Acceptance Criteria

1. WHEN the Multi_File_Analyzer completes analysis, THE Learning_Artifact_Generator SHALL generate a learning path with ordered steps
2. THE Learning_Artifact_Generator SHALL order learning steps from foundational concepts to advanced concepts
3. THE Learning_Artifact_Generator SHALL order learning steps based on code dependencies (learn dependencies before dependents)
4. THE Learning_Artifact_Generator SHALL include estimated time for each learning step
5. THE Learning_Artifact_Generator SHALL include recommended files to study for each learning step
6. FOR ALL learning path steps, THE Traceability_Manager SHALL maintain references to relevant code files
7. WHEN a user completes a learning step, THE System SHALL track progress and recommend the next step

### Requirement 8: Consistency and Traceability

**User Story:** As a learner, I want every quiz and flashcard to reference actual code, so that I know the learning materials are accurate and grounded in reality.

#### Acceptance Criteria

1. THE Traceability_Manager SHALL maintain a mapping between each Learning_Artifact and its Code_Evidence
2. THE Traceability_Manager SHALL store file paths, line numbers, and code snippets for each Code_Evidence reference
3. WHEN generating a Learning_Artifact, THE Learning_Artifact_Generator SHALL verify that Code_Evidence exists before creating the artifact
4. THE System SHALL reject any Learning_Artifact that lacks Code_Evidence
5. WHEN displaying a Learning_Artifact, THE System SHALL provide a "View Code" option that shows the relevant code snippet
6. THE System SHALL exclude generic programming theory that is not demonstrated in the analyzed code
7. WHEN code is updated, THE Traceability_Manager SHALL mark affected Learning_Artifacts as potentially outdated

### Requirement 9: Repository Upload and Processing

**User Story:** As a learner, I want to upload a repository easily, so that I can start learning from it quickly.

#### Acceptance Criteria

1. THE System SHALL accept repository uploads via GitHub URL
2. THE System SHALL accept repository uploads via ZIP file
3. THE System SHALL accept repository uploads via folder selection
4. WHEN a repository is uploaded, THE System SHALL validate that it contains code files
5. WHEN a repository exceeds the size limit, THE System SHALL inform the user and reject the upload
6. WHEN a repository is uploaded, THE System SHALL display the repository structure to the user
7. THE System SHALL support repositories in Python, JavaScript, TypeScript, Java, C++, Go, and Ruby
8. WHEN a repository is uploaded, THE System SHALL store it temporarily for analysis

### Requirement 10: Intent Clarification Dialog

**User Story:** As a learner, I want the system to ask clarifying questions when my intent is unclear, so that the analysis is accurate.

#### Acceptance Criteria

1. WHEN the Intent_Interpreter detects ambiguous intent, THE System SHALL present clarifying questions to the user
2. THE System SHALL provide suggested intent options based on repository content
3. WHEN the user selects a suggested intent, THE System SHALL proceed with file selection
4. WHEN the user provides additional context, THE Intent_Interpreter SHALL re-analyze the intent
5. THE System SHALL allow users to refine their intent after seeing initial file selections
6. THE System SHALL display the interpreted intent to the user for confirmation before analysis

### Requirement 11: Multi-Language Support

**User Story:** As a learner in India, I want learning materials in my preferred language, so that I can learn more effectively.

#### Acceptance Criteria

1. THE System SHALL support generating learning artifacts in English, Hindi, and Telugu
2. WHEN a user selects a language, THE Learning_Artifact_Generator SHALL generate all flashcards in that language
3. WHEN a user selects a language, THE Learning_Artifact_Generator SHALL generate all quiz questions in that language
4. WHEN a user selects a language, THE Learning_Artifact_Generator SHALL generate the learning path in that language
5. THE System SHALL preserve code snippets in their original language regardless of the selected output language
6. THE System SHALL allow users to switch languages and regenerate learning artifacts

### Requirement 12: Analysis Results Presentation

**User Story:** As a learner, I want to see clear analysis results with section separation, so that I can easily navigate the information.

#### Acceptance Criteria

1. WHEN analysis completes, THE System SHALL display results in clearly separated sections
2. THE System SHALL display the interpreted intent at the top of the results
3. THE System SHALL display the list of selected files with relevance explanations
4. THE System SHALL display the concept summary before detailed learning artifacts
5. THE System SHALL provide navigation between sections (concept summary, flashcards, quizzes, learning path)
6. THE System SHALL display file relationships as a visual dependency graph
7. THE System SHALL provide a "concise mode" that shows only key information without verbose explanations

### Requirement 13: Parser and Serializer Handling

**User Story:** As a developer analyzing a codebase with parsers, I want the system to identify and test parser round-trip properties, so that I can verify parser correctness.

#### Acceptance Criteria

1. WHEN the Multi_File_Analyzer detects a parser implementation, THE System SHALL identify it as a parser
2. WHEN the Multi_File_Analyzer detects a parser implementation, THE System SHALL identify the grammar being parsed
3. WHEN a parser is detected, THE Learning_Artifact_Generator SHALL create a flashcard about the parser's purpose
4. WHEN a parser is detected, THE Learning_Artifact_Generator SHALL create a quiz question about round-trip properties (parse → print → parse)
5. WHEN a pretty printer is detected alongside a parser, THE System SHALL create learning artifacts about their relationship
6. THE System SHALL identify serializers and deserializers as inverse operations
7. WHEN a serializer is detected, THE Learning_Artifact_Generator SHALL create quiz questions about round-trip properties (serialize → deserialize)

### Requirement 14: Progress Tracking and Session Management

**User Story:** As a learner, I want my progress saved across sessions, so that I can continue learning where I left off.

#### Acceptance Criteria

1. THE System SHALL save the user's current repository analysis to session state
2. THE System SHALL save the user's progress through the learning path
3. THE System SHALL save which flashcards have been reviewed and their review schedule
4. THE System SHALL save quiz scores and completed quizzes
5. WHEN a user returns to the application, THE System SHALL restore their previous session
6. THE System SHALL allow users to start a new analysis while preserving previous analyses
7. THE System SHALL provide a dashboard showing progress across all analyzed repositories

### Requirement 15: Error Handling and Feedback

**User Story:** As a learner, I want clear error messages when something goes wrong, so that I know how to fix the issue.

#### Acceptance Criteria

1. WHEN repository upload fails, THE System SHALL display a specific error message explaining the failure reason
2. WHEN file selection finds no relevant files, THE System SHALL suggest alternative intents or broader scope
3. WHEN code analysis fails for a file, THE System SHALL log the error and continue analyzing other files
4. WHEN learning artifact generation fails, THE System SHALL display a fallback message and generate basic artifacts
5. THE System SHALL validate user input before processing and provide immediate feedback for invalid input
6. WHEN the AI service is unavailable, THE System SHALL inform the user and suggest trying again later
7. THE System SHALL log all errors with sufficient context for debugging without exposing sensitive information to users
