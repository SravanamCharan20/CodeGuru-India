# Requirements Document: CodeGuru India

## Introduction

CodeGuru India is an AI-powered code learning platform designed to help Indian developers learn faster through multi-language support, interactive learning features, and personalized guidance. The system provides code explanations using simple analogies, supports voice queries with regional accent handling, and offers structured learning paths from DSA fundamentals to full-stack development.

## Glossary

- **System**: The CodeGuru India application
- **User**: A developer using the platform to learn or understand code
- **Code_Analyzer**: Component that processes and analyzes uploaded code or repositories
- **Explanation_Engine**: Component that generates code explanations using AI
- **Voice_Processor**: Component that handles voice input and regional accent recognition
- **Learning_Path**: A structured sequence of topics from beginner to advanced
- **Flashcard**: An interactive learning card with a question/concept on one side and answer/explanation on the other
- **Quiz**: An assessment tool to test user understanding
- **Progress_Tracker**: Component that monitors and displays user learning progress
- **Diagram_Generator**: Component that creates visual representations of code concepts
- **LLM**: Large Language Model (AWS Bedrock)
- **UI**: User Interface built with Streamlit

## Requirements

### Requirement 1: Multi-Language Interface Support

**User Story:** As a developer in India, I want to interact with the system in my preferred language (English, Hindi, or Telugu), so that I can learn more effectively in a language I'm comfortable with.

#### Acceptance Criteria

1. THE System SHALL support English, Hindi, and Telugu as interface languages
2. WHEN a user selects a language preference, THE System SHALL persist that preference across sessions
3. WHEN displaying code explanations, THE System SHALL render text in the user's selected language
4. THE System SHALL maintain consistent terminology across all supported languages
5. WHEN switching languages, THE System SHALL update all UI elements within 500ms

### Requirement 2: Voice Query Processing

**User Story:** As a developer, I want to ask questions about code using voice input, so that I can get explanations hands-free while coding.

#### Acceptance Criteria

1. WHEN a user activates voice input, THE Voice_Processor SHALL capture audio and convert it to text
2. THE Voice_Processor SHALL recognize and accurately process Indian English, Hindi, and Telugu accents
3. WHEN voice input is received, THE System SHALL provide visual feedback indicating processing status
4. IF voice input is unclear or cannot be processed, THEN THE System SHALL prompt the user to repeat or type the query
5. WHEN voice transcription completes, THE System SHALL display the transcribed text for user confirmation
6. THE Voice_Processor SHALL process voice queries within 3 seconds of audio completion

### Requirement 3: Code Upload and Repository Analysis

**User Story:** As a developer, I want to upload code files or connect repositories, so that I can get comprehensive analysis and explanations of existing codebases.

#### Acceptance Criteria

1. THE System SHALL accept code file uploads in formats: .py, .js, .jsx, .ts, .tsx, .java, .cpp, .c, .go, .rb
2. WHEN a user uploads a code file, THE Code_Analyzer SHALL parse and validate the file within 2 seconds
3. THE System SHALL accept GitHub repository URLs for analysis
4. WHEN a repository URL is provided, THE Code_Analyzer SHALL clone and analyze the repository structure
5. IF a file or repository cannot be processed, THEN THE System SHALL display a descriptive error message
6. THE System SHALL support files up to 10MB in size
7. THE System SHALL support repositories up to 100MB in total size

### Requirement 4: AI-Powered Code Summarization

**User Story:** As a developer, I want automatic summaries of uploaded code, so that I can quickly understand what the code does without reading every line.

#### Acceptance Criteria

1. WHEN code is uploaded, THE Code_Analyzer SHALL generate a high-level summary within 5 seconds
2. THE Explanation_Engine SHALL identify and list the main functions, classes, and modules in the code
3. THE Explanation_Engine SHALL describe the overall purpose and functionality of the code
4. THE Explanation_Engine SHALL highlight key algorithms and design patterns used
5. WHEN analyzing repositories, THE Code_Analyzer SHALL generate a project structure overview
6. THE System SHALL present summaries in the user's selected language

### Requirement 5: Code Debugging Assistance

**User Story:** As a developer, I want AI-powered debugging suggestions, so that I can identify and fix issues in my code more efficiently.

#### Acceptance Criteria

1. WHEN a user requests debugging help, THE Code_Analyzer SHALL scan the code for common errors and anti-patterns
2. THE Explanation_Engine SHALL provide specific suggestions for fixing identified issues
3. THE System SHALL highlight problematic code sections with line numbers
4. THE Explanation_Engine SHALL explain why each issue is problematic
5. THE System SHALL prioritize issues by severity (critical, warning, suggestion)
6. WHEN no issues are found, THE System SHALL confirm the code appears correct

### Requirement 6: Simple Analogy-Based Explanations

**User Story:** As a developer learning new concepts, I want code explanations using simple, relatable analogies, so that I can understand complex concepts more easily.

#### Acceptance Criteria

1. WHEN explaining code concepts, THE Explanation_Engine SHALL include at least one real-world analogy
2. THE Explanation_Engine SHALL use culturally relevant analogies appropriate for Indian developers
3. THE Explanation_Engine SHALL break down complex concepts into simpler components
4. THE Explanation_Engine SHALL provide examples alongside analogies
5. WHEN a user requests simpler explanations, THE System SHALL regenerate explanations at a more basic level

### Requirement 7: Interactive Flashcards

**User Story:** As a developer, I want to review concepts using flashcards, so that I can reinforce my learning through spaced repetition.

#### Acceptance Criteria

1. THE System SHALL generate flashcards based on analyzed code concepts
2. WHEN a user views a flashcard, THE UI SHALL display the question/concept first
3. WHEN a user flips a flashcard, THE UI SHALL reveal the answer/explanation with animation
4. THE System SHALL organize flashcards by topic and difficulty level
5. THE Progress_Tracker SHALL track which flashcards have been reviewed
6. THE System SHALL support user-created custom flashcards
7. WHEN a user marks a flashcard as "mastered", THE System SHALL reduce its review frequency

### Requirement 8: Interactive Quizzes

**User Story:** As a developer, I want to test my understanding through quizzes, so that I can assess my knowledge and identify gaps.

#### Acceptance Criteria

1. THE System SHALL generate quizzes based on analyzed code and learning topics
2. THE System SHALL support multiple question types: multiple choice, code completion, and debugging challenges
3. WHEN a user submits a quiz answer, THE System SHALL provide immediate feedback
4. THE System SHALL explain correct answers and why incorrect answers are wrong
5. THE Progress_Tracker SHALL record quiz scores and track improvement over time
6. THE System SHALL recommend topics for review based on quiz performance
7. WHEN a quiz is completed, THE System SHALL display a summary with score and time taken

### Requirement 9: Structured Learning Paths

**User Story:** As a developer, I want guided learning paths from DSA to full-stack development, so that I can follow a structured curriculum tailored to my goals.

#### Acceptance Criteria

1. THE System SHALL provide predefined learning paths: DSA Fundamentals, Backend Development, Frontend Development, Full-Stack Development, AWS Services
2. WHEN a user selects a learning path, THE System SHALL display a roadmap with milestones
3. THE System SHALL track progress through each learning path
4. THE System SHALL unlock advanced topics only after prerequisite topics are completed
5. WHEN a user completes a milestone, THE System SHALL provide a certificate or achievement badge
6. THE System SHALL recommend the next topic based on current progress and performance
7. THE System SHALL allow users to customize learning paths by adding or removing topics

### Requirement 10: Visual Diagram Generation

**User Story:** As a visual learner, I want automatic generation of diagrams for code concepts, so that I can understand architecture and flow more intuitively.

#### Acceptance Criteria

1. WHEN analyzing code, THE Diagram_Generator SHALL create flowcharts for function logic
2. THE Diagram_Generator SHALL create class diagrams for object-oriented code
3. THE Diagram_Generator SHALL create architecture diagrams for multi-file projects
4. THE Diagram_Generator SHALL create sequence diagrams for API interactions
5. THE System SHALL render diagrams using Mermaid format
6. WHEN a user clicks on a diagram element, THE System SHALL highlight the corresponding code section
7. THE System SHALL allow users to download diagrams as PNG or SVG files

### Requirement 11: Personalized Progress Tracking

**User Story:** As a developer, I want to track my learning progress over time, so that I can see my improvement and stay motivated.

#### Acceptance Criteria

1. THE Progress_Tracker SHALL display a dashboard with learning statistics
2. THE Progress_Tracker SHALL track metrics: topics completed, quiz scores, time spent learning, streak days
3. THE Progress_Tracker SHALL visualize progress using charts and graphs
4. THE Progress_Tracker SHALL show skill level progression for each technology
5. WHEN a user achieves a milestone, THE System SHALL display a congratulatory message
6. THE Progress_Tracker SHALL compare current performance with past performance
7. THE System SHALL provide weekly learning summaries via the UI

### Requirement 12: Popular Indian Tech Stack Support

**User Story:** As an Indian developer, I want specialized support for technologies commonly used in India, so that I can learn the most relevant skills for the job market.

#### Acceptance Criteria

1. THE System SHALL provide enhanced explanations for React, Node.js, Express, MongoDB, AWS Lambda, AWS S3, AWS DynamoDB
2. THE System SHALL include learning paths specifically for MERN stack and AWS services
3. THE System SHALL recognize and explain Indian tech industry best practices
4. THE System SHALL provide examples relevant to Indian e-commerce and fintech applications
5. WHEN analyzing code using these technologies, THE Explanation_Engine SHALL provide framework-specific insights

### Requirement 13: Session Management

**User Story:** As a user, I want my learning progress and preferences saved automatically, so that I can continue where I left off in future sessions.

#### Acceptance Criteria

1. THE System SHALL persist user preferences in browser local storage
2. THE System SHALL save learning progress after each completed activity
3. WHEN a user returns to the application, THE System SHALL restore their previous session state
4. THE System SHALL maintain session data for at least 30 days
5. IF session data is corrupted or unavailable, THEN THE System SHALL start a fresh session without errors

## Non-Functional Requirements

### Performance Requirements

**NFR-1: Response Time**
- THE System SHALL respond to user interactions within 500ms for UI updates
- THE System SHALL generate code summaries within 5 seconds for files up to 1000 lines
- THE System SHALL process voice queries within 3 seconds of audio completion
- THE LLM SHALL return explanations within 10 seconds for standard queries

**NFR-2: Scalability**
- THE System SHALL support concurrent usage by up to 100 users without performance degradation
- THE System SHALL handle file uploads up to 10MB without timeout
- THE System SHALL process repositories up to 50MB within 30 seconds

**NFR-3: Availability**
- THE System SHALL maintain 99% uptime during business hours (9 AM - 9 PM IST)
- THE System SHALL gracefully handle AWS Bedrock API failures with user-friendly error messages

### Security Requirements

**NFR-4: Data Privacy**
- THE System SHALL NOT store uploaded code permanently on servers
- THE System SHALL process code in-memory and discard after session ends
- THE System SHALL NOT transmit user code to third-party services except AWS Bedrock
- THE System SHALL sanitize all user inputs to prevent code injection attacks

**NFR-5: Authentication**
- WHERE user authentication is implemented, THE System SHALL use secure token-based authentication
- THE System SHALL enforce HTTPS for all communications
- THE System SHALL validate all file uploads for malicious content before processing

### Usability Requirements

**NFR-6: User Experience**
- THE UI SHALL be responsive and work on desktop browsers (Chrome, Firefox, Safari, Edge)
- THE UI SHALL provide clear visual feedback for all user actions
- THE UI SHALL display loading indicators for operations taking longer than 1 second
- THE System SHALL provide helpful error messages with suggested actions

**NFR-7: Accessibility**
- THE UI SHALL support keyboard navigation for all interactive elements
- THE UI SHALL provide sufficient color contrast for readability (WCAG AA compliance)
- THE UI SHALL support screen reader compatibility for text content

### Maintainability Requirements

**NFR-8: Code Quality**
- THE System SHALL be implemented with modular, reusable components
- THE System SHALL include comprehensive error handling for all external API calls
- THE System SHALL log errors and warnings for debugging purposes
- THE System SHALL follow Python PEP 8 style guidelines for backend code

**NFR-9: Technology Stack**
- THE System SHALL use AWS Bedrock for LLM capabilities
- THE System SHALL use Streamlit for UI implementation
- THE System SHALL use LangChain for LLM orchestration and chaining
- THE System SHALL use Python 3.9 or higher as the primary programming language
- No external database dependencies (use Streamlit session state only)
