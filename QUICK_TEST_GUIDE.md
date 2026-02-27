# Quick Test Guide - CodeGuru India

## Run This First! 🚀

To verify everything is working correctly, run:

```bash
python test_complete_features.py
```

Expected output:
```
✅ ALL FEATURES WORKING!
Total: 5/5 tests passed
```

## What Gets Tested

### 1. Required Packages ✅
- streamlit
- boto3
- langchain
- hypothesis
- pytest
- GitPython
- python-dotenv
- audio-recorder-streamlit

### 2. Repository Upload Fix ✅
- File contents stored in session
- File selector dropdown
- Analyze button
- Repo view clears after analysis

### 3. Audio Recorder Integration ✅
- Package installed
- Voice processor initialized
- Multi-language support (English, Hindi, Telugu)
- Mock transcription working
- UI integration complete

### 4. Multi-Language Support ✅
- English translations
- Hindi translations (हिंदी)
- Telugu translations (తెలుగు)
- Voice languages configured

### 5. AWS Integration ✅
- Credentials configured
- Bedrock client initialized
- Transcribe client initialized

## Individual Tests

### Test Audio Recorder Only
```bash
python test_audio_recorder.py
```

### Test AI Features Only
```bash
python test_ai_working.py
```

### Test All Features (Older Version)
```bash
python test_all_features.py
```

## If Tests Fail

### Missing Package Error
```bash
pip install -r requirements.txt
```

### AWS Credentials Error
Check your `.env` file has:
```
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
BEDROCK_MODEL_ID=us.meta.llama3-2-3b-instruct-v1:0
```

### Audio Recorder Error
```bash
pip install audio-recorder-streamlit
```

## Start the App

Once all tests pass:
```bash
python -m streamlit run app.py
```

Open browser to: http://localhost:8501

## Quick Feature Test

### 1. Test Repository Analysis (2 minutes)
1. Go to "Upload Code" → "GitHub Repository"
2. Enter: `https://github.com/TheAlgorithms/Python`
3. Click "Analyze Code"
4. Select a file from dropdown
5. Click "🔍 Analyze [filename]"
6. Verify detailed analysis appears

### 2. Test Voice Query (1 minute)
1. Go to "Upload Code" → "Voice Query"
2. Upload a simple Python file first
3. Select language (English)
4. Click microphone button
5. Speak: "Explain this code"
6. Click "Transcribe Audio"
7. Click "Process Query"
8. Verify AI answer appears

### 3. Test File Upload (1 minute)
1. Go to "Upload Code" → "File Upload"
2. Upload a Python file
3. Click "Analyze Code"
4. Go to "Explanations" tab
5. Verify analysis appears

## Success Criteria

✅ All tests pass
✅ App starts without errors
✅ Repository analysis works
✅ Voice query works
✅ File upload works
✅ AI responses generated

## Need Help?

1. Check test output for specific errors
2. Review `.env` file configuration
3. Verify internet connection
4. Check AWS credentials and permissions
5. Try restarting the app

## Documentation

- `FEATURES_COMPLETE.md` - Complete feature documentation
- `AUDIO_RECORDER_GUIDE.md` - Audio recorder details
- `README.md` - Main project documentation
- `QUICKSTART.md` - Quick start guide
