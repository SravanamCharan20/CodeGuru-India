# 🚀 Quick Start Guide - CodeGuru India

## Running the Application

### Step 1: Ensure Dependencies are Installed

```bash
pip install -r requirements.txt
```

### Step 2: Start the Application

```bash
python -m streamlit run app.py
```

Or simply:

```bash
streamlit run app.py
```

### Step 3: Access the Application

Open your browser and go to:
- **Local:** http://localhost:8501
- **Network:** http://192.168.0.103:8501

## Testing the Code Analysis Feature

### Option 1: Use the Provided Test File

1. Click on "Upload Code" in the sidebar
2. Upload the `test_sample.py` file from the project root
3. Click "🚀 Analyze Code"
4. View results in the "Explanations" tab

### Option 2: Create Your Own Test File

Create a simple Python file:

```python
def hello_world():
    """A simple greeting function."""
    print("Hello, CodeGuru India!")

if __name__ == "__main__":
    hello_world()
```

Upload it and see the analysis!

## Features to Try

### 1. Code Upload & Analysis
- Upload Python, JavaScript, TypeScript, or other supported files
- See structure extraction (functions, classes)
- View AI-generated summaries
- Check detected issues and patterns

### 2. Language Switching
- Use the language selector in the sidebar
- Switch between English, हिंदी, and తెలుగు
- See how the UI updates instantly

### 3. Learning Paths
- Navigate to "Learning Paths"
- Explore different paths (DSA, Backend, Frontend, etc.)
- See the roadmap visualization
- Check milestone achievements

### 4. Interactive Quizzes
- Go to "Quizzes"
- Select a quiz topic
- Answer questions
- Get immediate feedback

### 5. Flashcards
- Navigate to "Flashcards"
- Flip cards to reveal answers
- Rate difficulty
- Mark cards as mastered

### 6. Progress Dashboard
- Check "Progress" in the sidebar
- View your learning metrics
- See skill level progress
- Review achievement badges

## Running Without AWS Credentials

The app works perfectly without AWS credentials! It will:
- ✅ Extract code structure (functions, classes, imports)
- ✅ Detect patterns and issues
- ✅ Show all UI features
- ✅ Use mock AI responses for demonstration

You'll see a message: "⚠️ AI services not configured. Add AWS credentials to .env file for full functionality."

## Enabling Full AI Features (Optional)

### Step 1: Create .env File

```bash
cp .env.example .env
```

### Step 2: Add Your AWS Credentials

Edit `.env` and add:

```
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
BEDROCK_MODEL_ID=anthropic.claude-v2
MAX_TOKENS=2000
TEMPERATURE=0.7
```

### Step 3: Restart the Application

```bash
# Stop the current process (Ctrl+C)
# Then restart
python -m streamlit run app.py
```

You should now see: "✅ AI services initialized and ready!"

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'boto3'"

**Solution:**
```bash
pip install boto3 python-dotenv
```

### Issue: "Port 8501 is not available"

**Solution:**
```bash
# Kill any process using port 8501
lsof -ti:8501 | xargs kill -9

# Or use a different port
streamlit run app.py --server.port 8502
```

### Issue: App shows "AI services not configured"

**Solution:**
This is normal! The app works without AWS credentials. To enable full AI:
1. Create `.env` file with AWS credentials
2. Restart the app
3. You should see "✅ AI services initialized and ready!"

### Issue: Code analysis shows mock data

**Solution:**
- Without AWS credentials: This is expected behavior
- With AWS credentials: Check your credentials are correct in `.env`

## What to Expect

### Without AWS Credentials:
- ✅ Full UI functionality
- ✅ Code structure extraction
- ✅ Pattern detection
- ✅ Issue detection (basic)
- ⚠️ Mock AI responses

### With AWS Credentials:
- ✅ Everything above, plus:
- ✅ Real AI-generated explanations
- ✅ Culturally relevant analogies
- ✅ Detailed code insights
- ✅ Advanced debugging suggestions

## Next Steps

1. **Explore the UI** - Navigate through all pages
2. **Upload Code** - Try analyzing different code files
3. **Switch Languages** - Test the multi-language support
4. **Check Learning Paths** - Explore the structured curriculum
5. **Take Quizzes** - Test your knowledge
6. **Review Flashcards** - Reinforce learning
7. **Track Progress** - Monitor your growth

## Need Help?

- Check `README.md` for detailed documentation
- Review `IMPLEMENTATION_SUMMARY.md` for technical details
- Look at `test_sample.py` for a sample code file

## Enjoy Learning with CodeGuru India! 🎓
