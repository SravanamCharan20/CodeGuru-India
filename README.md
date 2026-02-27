# 🎓 CodeGuru India

An AI-powered code learning platform designed to help Indian developers learn faster through multi-language support, interactive learning features, and personalized guidance.

## ✨ Features

### Core Features
- 🔍 **Smart Code Analysis** - Upload files or GitHub repositories for instant analysis
- 🗣️ **Voice Queries** - Ask questions in English, Hindi, or Telugu
- 📚 **Interactive Learning** - Flashcards, quizzes, and structured learning paths
- 📊 **Progress Tracking** - Monitor your growth with detailed analytics
- 🎯 **Simple Analogies** - Complex concepts explained with culturally relevant examples
- 📈 **Visual Diagrams** - Auto-generated flowcharts, class diagrams, and architecture views

### 🧠 Intent-Driven Repository Analysis (NEW!)
- 🎯 **Natural Language Goals** - Describe what you want to learn in plain language
- 🤖 **AI-Powered Intent Understanding** - System interprets your learning goals automatically
- 📁 **Smart File Selection** - Automatically identifies relevant files based on your intent
- 🔗 **Multi-File Analysis** - Analyzes relationships, data flows, and patterns across files
- 📝 **Code-Grounded Learning** - Every flashcard and quiz links directly to actual code
- 🗺️ **Personalized Learning Paths** - Ordered steps from foundational to advanced concepts
- 🌐 **Multi-Language Support** - Generate materials in English, Hindi, or Telugu
- 🔍 **Complete Traceability** - Track every concept back to its source code

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip package manager
- AWS Account (optional - for AI features)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd codeguru-india
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (optional for AI features):
```bash
cp .env.example .env
# Edit .env with your AWS credentials
```

4. Run the application:
```bash
streamlit run app.py
```

5. Open your browser and navigate to `http://localhost:8501`

### Running Without AWS Credentials

The app works perfectly without AWS credentials! It will:
- Use mock AI responses for demonstrations
- Still perform code structure analysis
- Show all UI features and interactions
- Display helpful messages about enabling AI features

To enable full AI capabilities, add your AWS Bedrock credentials to the `.env` file.

## 📁 Project Structure

```
codeguru-india/
├── app.py                           # Main application entry point
├── config.py                        # Configuration management
├── session_manager.py               # Session state management
├── requirements.txt                 # Python dependencies
├── .streamlit/
│   └── config.toml                 # Streamlit configuration
├── analyzers/                       # Analysis components
│   ├── intent_interpreter.py       # Natural language intent understanding
│   ├── file_selector.py            # Intent-driven file selection
│   ├── multi_file_analyzer.py      # Multi-file code analysis
│   ├── repository_manager.py       # Repository upload and validation
│   └── intent_driven_orchestrator.py # Workflow orchestration
├── generators/                      # Learning artifact generators
│   └── learning_artifact_generator.py # Flashcards, quizzes, paths
├── learning/                        # Learning components
│   └── traceability_manager.py     # Code-artifact traceability
├── models/                          # Data models
│   └── intent_models.py            # Intent and artifact models
├── ui/                             # UI components
│   ├── sidebar.py                  # Navigation sidebar
│   ├── repository_upload.py        # Repository upload interface
│   ├── intent_input.py             # Learning goal input
│   ├── learning_artifacts_dashboard.py # Learning materials view
│   └── intent_driven_analysis_page.py  # Main analysis workflow
├── utils/                          # Utilities
│   └── error_handling.py           # Error handling and validation
├── tests/                          # Test suite
│   └── integration/                # Integration tests
├── docs/                           # Documentation
│   ├── API_REFERENCE.md            # API documentation
│   └── USER_GUIDE.md               # User guide
└── .kiro/
    └── specs/                      # Feature specifications
```

## 🎯 Current Status

### ✅ Completed Features

**Phase 1 & 2: Core Platform**
- Project setup and configuration
- Session management with persistence
- Main application structure with routing
- Sidebar navigation with language selector
- Code upload interface (file, GitHub, voice)
- Code explanation view with tabs
- Interactive quiz and flashcard interfaces
- Progress dashboard with metrics

**Phase 3: Intent-Driven Analysis (NEW!)**
- ✅ Natural language intent interpretation
- ✅ AI-powered intent understanding with clarification
- ✅ Intent-driven file selection with relevance scoring
- ✅ Multi-file analysis with relationship detection
- ✅ Dependency graph construction
- ✅ Data flow and execution path analysis
- ✅ Cross-file pattern detection
- ✅ Code-grounded flashcard generation
- ✅ Code-grounded quiz generation
- ✅ Personalized learning path generation
- ✅ Concept summary with categorization
- ✅ Complete code traceability system
- ✅ Multi-language support (English, Hindi, Telugu)
- ✅ Repository upload (GitHub, ZIP, folder)
- ✅ Session persistence across analyses
- ✅ Error handling and validation
- ✅ Integration test suite
- ✅ Comprehensive documentation

### 🚧 Future Enhancements

- Voice processing with AWS Transcribe
- Diagram generation with Mermaid
- Parser/serializer detection and round-trip properties
- Property-based testing for all components
- Advanced framework-specific insights
- Collaborative learning features

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI/ML**: AWS Bedrock, LangChain
- **Language**: Python 3.9+
- **Testing**: Pytest, Hypothesis (Property-Based Testing)

## 📖 Usage

### Quick Start: Intent-Driven Analysis

1. **Upload Repository**
   - Navigate to "Repository Analysis" in sidebar
   - Choose: GitHub URL, ZIP file, or local folder
   - Supported: Python, JavaScript, TypeScript, Java, C++, Go, Ruby

2. **Describe Your Learning Goal**
   - Use natural language: "I want to learn how authentication works"
   - Select your language: English, Hindi, or Telugu
   - System interprets your intent automatically

3. **Review Analysis**
   - System selects relevant files
   - Analyzes code relationships and patterns
   - Generates personalized learning materials

4. **Learn with Generated Materials**
   - **Concept Summary**: Overview of key concepts
   - **Flashcards**: Question-answer pairs with code evidence
   - **Quizzes**: Multiple choice questions with explanations
   - **Learning Path**: Ordered steps from basic to advanced

### Traditional Code Analysis

1. **Upload Code**
   - Navigate to "Upload Code" from sidebar
   - Upload file, GitHub URL, or use voice input
   - Click "Analyze Code"

2. **View Explanations**
   - Summary, details, diagrams, and issues
   - AI-powered insights and suggestions

3. **Learning Paths**
   - Follow structured learning roadmaps
   - Complete quizzes to unlock topics

4. **Track Progress**
   - Monitor metrics and achievements
   - Review weekly summaries

## 🌐 Language Support

CodeGuru India supports three languages:
- 🇬🇧 English
- 🇮🇳 हिंदी (Hindi)
- 🇮🇳 తెలుగు (Telugu)

Switch languages anytime from the sidebar. All learning materials (flashcards, quizzes, learning paths) can be generated in your preferred language while keeping code snippets in their original language.

## 📚 Documentation

- **[User Guide](docs/USER_GUIDE.md)** - Complete guide for using the platform
- **[API Reference](docs/API_REFERENCE.md)** - API documentation for developers
- **[Quick Start](INTENT_DRIVEN_QUICKSTART.md)** - Get started with intent-driven analysis
- **[Implementation Status](INTENT_DRIVEN_IMPLEMENTATION_STATUS.md)** - Feature completion status

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run integration tests
pytest tests/integration/

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/integration/test_end_to_end_flow.py
```

Test coverage includes:
- End-to-end workflow tests
- AI integration tests
- Session persistence tests
- Multi-language support tests
- Error handling tests

## 🤝 Contributing

Contributions are welcome! Please read the contributing guidelines before submitting pull requests.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

Built with ❤️ for the Indian developer community.
