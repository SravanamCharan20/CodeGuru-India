# User Guide - Intent-Driven Repository Analysis

Welcome to CodeGuru India's Intent-Driven Repository Analysis! This guide will help you analyze code repositories and generate personalized learning materials.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Uploading a Repository](#uploading-a-repository)
3. [Describing Your Learning Goal](#describing-your-learning-goal)
4. [Understanding the Analysis](#understanding-the-analysis)
5. [Using Learning Materials](#using-learning-materials)
6. [Language Support](#language-support)
7. [Tips and Best Practices](#tips-and-best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Internet connection (for GitHub repositories)
- AWS credentials (optional, for AI-powered features)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/codeguru-india.git
cd codeguru-india

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

---

## Uploading a Repository

You have three options to upload a repository:

### Option 1: GitHub URL

1. Navigate to "Repository Analysis" in the sidebar
2. Select "GitHub URL" tab
3. Enter the repository URL (e.g., `https://github.com/username/repository`)
4. Click "Upload"

**Supported:** Public GitHub repositories

### Option 2: ZIP File

1. Select "ZIP File" tab
2. Click "Browse files" and select your ZIP file
3. Click "Upload"

**Maximum size:** 100MB

### Option 3: Local Folder

1. Select "Local Folder" tab
2. Enter the folder path
3. Click "Upload"

**Note:** Folder must contain supported code files

### Supported Languages

- Python (.py)
- JavaScript (.js)
- TypeScript (.ts)
- Java (.java)
- C++ (.cpp, .h)
- Go (.go)
- Ruby (.rb)

---

## Describing Your Learning Goal

After uploading, describe what you want to learn in natural language.

### Good Examples

✅ "I want to learn how authentication works in this project"
✅ "Help me understand the database schema and relationships"
✅ "Explain the API endpoints and how they handle requests"
✅ "I'm preparing for an interview, focus on design patterns"

### Tips for Better Results

- **Be specific**: Mention specific features or components
- **State your level**: "I'm a beginner" or "I'm experienced"
- **Mention technologies**: "Focus on React components" or "Explain the Flask routes"

### Language Selection

Choose your preferred language for learning materials:
- 🇬🇧 English
- 🇮🇳 हिंदी (Hindi)
- 🇮🇳 తెలుగు (Telugu)

**Note:** Code snippets remain in their original language; only explanations are translated.

### Suggested Goals

The system suggests learning goals based on your repository:
- Click any suggestion to use it
- Modify suggestions to fit your needs

### Clarification Questions

If your goal is unclear, the system will ask questions like:
- "Which authentication method are you interested in?"
- "Do you want to focus on frontend or backend?"

Answer these to refine your learning goal.

---

## Understanding the Analysis

### Analysis Steps

1. **Intent Interpretation**: System understands your goal
2. **File Selection**: Relevant files are identified
3. **Multi-File Analysis**: Code is analyzed for concepts
4. **Artifact Generation**: Learning materials are created

### What Gets Analyzed

- **Functions and Classes**: Core building blocks
- **Relationships**: How files interact
- **Data Flows**: How data moves through the system
- **Design Patterns**: Architectural patterns used
- **Key Concepts**: Important programming concepts

### Analysis Results

You'll see:
- Number of flashcards generated
- Number of quiz questions
- Number of learning steps
- Estimated study time

---

## Using Learning Materials

### Concept Summary

**What it shows:**
- Total concepts found
- Top 5 most important concepts
- Concepts organized by category

**How to use:**
- Get an overview of the codebase
- Identify key areas to focus on
- Understand the architecture

### Flashcards

**What they are:**
- Question-answer pairs for quick review
- Based on actual code in the repository
- Categorized by concept type

**How to use:**
1. Read the question
2. Try to answer mentally
3. Click "Show Answer" to check
4. Navigate with Previous/Next buttons
5. Click "View Code" to see the actual code

**Features:**
- Spaced repetition ready
- Difficulty levels (beginner, intermediate, advanced)
- Code evidence for every card

### Quizzes

**What they are:**
- Multiple choice questions
- Test your understanding
- Detailed explanations

**How to use:**
1. Read each question carefully
2. Select your answer
3. Click "Check Answer"
4. Read the explanation
5. View code evidence if needed

**Tips:**
- Take quizzes after studying flashcards
- Review explanations even for correct answers
- Use code evidence to deepen understanding

### Learning Path

**What it is:**
- Ordered sequence of learning steps
- From foundational to advanced concepts
- Based on code dependencies

**How to use:**
1. Follow steps in order
2. Study recommended files for each step
3. Complete prerequisites before moving forward
4. Mark steps as complete to track progress

**Features:**
- Estimated time for each step
- Concepts covered in each step
- Recommended files to study
- Prerequisites clearly marked

---

## Language Support

### Switching Languages

1. Go to Learning Materials dashboard
2. Click "🌐 Change Language"
3. Select your preferred language
4. Go back to Analysis step to regenerate

### What Gets Translated

✅ **Translated:**
- Flashcard questions and answers
- Quiz questions and explanations
- Learning path titles and descriptions
- Concept summaries

❌ **Not Translated:**
- Code snippets (remain in original language)
- File names and paths
- Variable and function names

### Culturally Relevant Analogies

When available, explanations include analogies from Indian culture:
- Chai stalls and street food
- Cricket and sports
- Indian railways
- Bollywood
- Festivals and traditions

---

## Tips and Best Practices

### For Best Results

1. **Start Broad, Then Narrow**
   - First: "Understand the overall architecture"
   - Then: "Learn how authentication works"

2. **Match Your Level**
   - Beginner: Focus on basic concepts
   - Intermediate: Explore patterns and relationships
   - Advanced: Deep dive into architecture

3. **Use Multiple Repositories**
   - Compare implementations across projects
   - Build analysis history
   - Track your learning progress

4. **Combine Learning Methods**
   - Start with Concept Summary (overview)
   - Study Flashcards (memorization)
   - Take Quizzes (testing)
   - Follow Learning Path (structured learning)

### Study Workflow

**Day 1:**
1. Upload repository
2. Describe learning goal
3. Review Concept Summary
4. Study first 5 flashcards

**Day 2:**
5. Review yesterday's flashcards
6. Study next 5 flashcards
7. Take first quiz

**Day 3:**
8. Review all flashcards
9. Follow Learning Path Step 1
10. Take second quiz

**Continue this pattern for best retention!**

---

## Troubleshooting

### Common Issues

**"No relevant files found"**
- Try a broader learning goal
- Check if repository contains supported languages
- Verify repository structure

**"Intent needs clarification"**
- Answer the clarification questions
- Be more specific in your goal
- Mention specific features or components

**"Repository too large"**
- Maximum size is 100MB
- Try analyzing specific folders
- Use a smaller repository

**"AI service unavailable"**
- Basic analysis will still work
- Try again later for AI-powered features
- Check your AWS credentials (if using)

### Getting Help

**Check the logs:**
- Look for error messages in the terminal
- Check Streamlit logs for details

**Verify setup:**
- Ensure all dependencies are installed
- Check Python version (3.8+)
- Verify repository structure

**Report issues:**
- Include error messages
- Describe steps to reproduce
- Mention repository type and size

---

## Advanced Features

### Session Persistence

Your analysis is saved automatically:
- Switch between repositories
- Resume where you left off
- Track progress across sessions

### Analysis History

View all your past analyses:
- See what you've learned
- Compare different repositories
- Track artifacts generated

### Code Traceability

Every learning artifact links to actual code:
- Click "View Code" to see the source
- Understand context of concepts
- Verify information accuracy

---

## Next Steps

1. **Try the Quick Start**: Follow [INTENT_DRIVEN_QUICKSTART.md](../INTENT_DRIVEN_QUICKSTART.md)
2. **Explore Examples**: Check sample repositories
3. **Read API Docs**: See [API_REFERENCE.md](API_REFERENCE.md) for developers
4. **Join Community**: Share your experience and get help

---

## Feedback

We'd love to hear from you!
- Report bugs
- Suggest features
- Share success stories
- Contribute improvements

Happy Learning! 🚀
