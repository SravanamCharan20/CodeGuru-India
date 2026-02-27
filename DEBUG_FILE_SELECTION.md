# Debug File Selection - What to Check

## Run the App and Check Logs

When you run the app and try to analyze with "i want to learn how the routing works in this app", check the console logs for these messages:

### 1. File Scanning
```
INFO: Selecting files for intent: learn_specific_feature
INFO: Total files scanned: X
```
**If X = 0**: Repository upload failed or file tree extraction broken

### 2. File Filtering
```
INFO: Files after filtering: Y (excluded: Z)
```
**If Y = 0**: All files were excluded (check EXCLUDE_PATTERNS)

### 3. AI Availability
```
INFO: AI orchestrator available - using AI-powered semantic file selection
```
**OR**
```
WARNING: AI orchestrator not available - using keyword-based file selection
```

### 4. AI Selection Process
```
INFO: Starting AI semantic file selection with N files
INFO: Prepared M files for AI analysis
INFO: Sample files: ['src/App.js', ...]
INFO: Calling AI for semantic file selection...
INFO: AI response received: X characters
INFO: AI response preview: ...
```

### 5. AI Response Parsing
```
INFO: ✓ Successfully parsed N file paths from AI
INFO: Selected paths: ['src/App.js', ...]
```
**OR**
```
ERROR: ✗ Could not find JSON array in AI response
ERROR: Full response: ...
```

### 6. File Matching
```
INFO: Matching N AI-selected paths with actual files...
INFO:   ✓ Matched: src/App.js
```

### 7. Final Result
```
INFO: FINAL RESULT: Selected N files out of M
```

## Common Issues and Solutions

### Issue 1: No Files Scanned (Total files scanned: 0)
**Cause**: Repository upload or file tree extraction failed
**Solution**: Check `analyzers/repository_manager.py` - file tree building

### Issue 2: All Files Filtered Out
**Cause**: EXCLUDE_PATTERNS too aggressive
**Solution**: Check file paths against EXCLUDE_PATTERNS in `file_selector.py`

### Issue 3: AI Not Available
**Cause**: `orchestrator` is None
**Solution**: Check initialization in `app.py` - ensure LangChainOrchestrator is passed to FileSelector

### Issue 4: AI Returns Bad JSON
**Cause**: Meta Llama 3.2 3B returns text instead of JSON
**Example Bad Response**:
```
Based on the analysis, the relevant files are:
- src/App.js
- src/index.js
```

**Solution**: Already handled with multiple parsing strategies, but if still failing, check AI response in logs

### Issue 5: AI Paths Don't Match Files
**Cause**: AI returns paths that don't exist in file list
**Solution**: Check path format consistency (with/without leading slash, etc.)

## What to Send Me

Run the app and send me the console output showing:
1. Total files scanned
2. Files after filtering
3. Whether AI is being used
4. AI response (if available)
5. Final result

This will tell me exactly where the problem is!

## Quick Test

Run this in your terminal while the app is running:
```bash
# Check if logs show the issue
tail -f logs/app.log | grep -E "(Total files|AI response|FINAL RESULT)"
```

Or just look at the Streamlit console output when you click "Analyze".
