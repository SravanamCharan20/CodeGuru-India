# 🎓 CodeGuru India

An AI-powered code learning platform designed to help Indian developers learn faster through multi-language support, interactive learning features, and personalized guidance.

## ✨ Features

- 🔍 **Smart Code Analysis** - Upload files or GitHub repositories for instant analysis
- 🗣️ **Voice Queries** - Ask questions in English, Hindi, or Telugu
- 📚 **Interactive Learning** - Flashcards, quizzes, and structured learning paths
- 📊 **Progress Tracking** - Monitor your growth with detailed analytics
- 🎯 **Simple Analogies** - Complex concepts explained with culturally relevant examples
- 📈 **Visual Diagrams** - Auto-generated flowcharts, class diagrams, and architecture views

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
├── app.py                      # Main application entry point
├── config.py                   # Configuration management
├── session_manager.py          # Session state management
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── ui/                        # UI components
│   ├── sidebar.py             # Navigation sidebar
│   ├── code_upload.py         # Code upload interface
│   ├── explanation_view.py    # Code explanations view
│   ├── learning_path.py       # Learning paths interface
│   ├── quiz_view.py           # Quiz interface
│   ├── flashcard_view.py      # Flashcard interface
│   └── progress_dashboard.py  # Progress tracking dashboard
└── .kiro/
    └── specs/                 # Feature specifications
```

## 🎯 Current Status

### ✅ Completed (Phase 1 & 2)

**UI/UX Phase:**
- Project setup and configuration
- Session management
- Main application structure with routing
- Sidebar navigation with language selector
- Code upload interface (file, GitHub, voice)
- Code explanation view with tabs (Summary, Details, Diagrams, Issues)
- Learning paths with roadmap visualization
- Interactive quiz interface with multiple question types
- Flashcard system with flip animation
- Progress dashboard with metrics and charts

**Backend Integration Phase:**
- AWS Bedrock client with retry logic and error handling
- Prompt management system with multi-language support
- LangChain orchestrator for AI operations
- Code analyzer with AST parsing (Python) and regex (JavaScript/TypeScript)
- Real-time code analysis integration
- AI-powered code explanations and summaries
- Issue detection and pattern recognition
- Mock data fallback when AWS credentials not configured

### 🚧 Next Steps

Future enhancements will include:
- Voice processing with AWS Transcribe
- Diagram generation with Mermaid
- Repository analyzer for GitHub integration
- Quiz and flashcard generation with AI
- Progress persistence with local storage
- Learning path recommendations
- Framework-specific insights (React, Node.js, AWS)

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI/ML**: AWS Bedrock, LangChain
- **Language**: Python 3.9+
- **Testing**: Pytest, Hypothesis (Property-Based Testing)

## 📖 Usage

### Upload Code

1. Navigate to "Upload Code" from the sidebar
2. Choose upload method:
   - Upload a code file (.py, .js, .ts, etc.)
   - Enter a GitHub repository URL
   - Use voice input (coming soon)
3. Click "Analyze Code"

### View Explanations

- **Summary**: High-level overview with key concepts and analogies
- **Details**: In-depth explanations with code examples
- **Diagrams**: Visual representations (flowcharts, class diagrams)
- **Issues**: Detected bugs and suggestions

### Learning Paths

1. Select a learning path (DSA, Backend, Frontend, Full-Stack, AWS)
2. View your progress and roadmap
3. Start available topics
4. Complete quizzes to unlock advanced topics

### Take Quizzes

1. Choose a quiz topic
2. Answer multiple choice, code completion, or debugging questions
3. Get immediate feedback and explanations
4. Track your scores over time

### Review Flashcards

1. Filter by topic and difficulty
2. Flip cards to reveal answers
3. Rate difficulty (Easy, Medium, Hard)
4. Mark cards as reviewed or mastered

### Track Progress

- View key metrics (topics completed, quiz scores, streak)
- Monitor skill levels for different technologies
- Review weekly summaries
- Earn achievement badges

## 🌐 Language Support

CodeGuru India supports three languages:
- 🇬🇧 English
- 🇮🇳 हिंदी (Hindi)
- 🇮🇳 తెలుగు (Telugu)

Switch languages anytime from the sidebar.

## 🤝 Contributing

Contributions are welcome! Please read the contributing guidelines before submitting pull requests.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

Built with ❤️ for the Indian developer community.
