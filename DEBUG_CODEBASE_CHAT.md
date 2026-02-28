# Debug Guide: Codebase Chat Not Responding

## Issue Fixed

The chat was getting stuck because:
1. Repository wasn't being indexed automatically
2. No error messages were shown
3. No progress indicators during processing

## Fixes Applied

### 1. Auto-Indexing
Now when you open Codebase Chat, it will:
- Check if codebase is indexed
- If not, automatically index it
- Show progress: "Indexing codebase..."
- Display success message when done

### 2. Better Error Handling
- Shows detailed error messages
- Logs all steps for debugging
- Provides helpful suggestions

### 3. Progress Indicators
- "🤔 Analyzing your question..."
- "🔍 Searching codebase..."
- "✍️ Generating explanation..."

### 4. Fallback Behavior
- If no relevant code found, returns top chunks anyway
- If keyword search fails, uses all chunks
- Always tries to give an answer

## How to Test

### Step 1: Check Logs
Run the app and watch the terminal for logs:
```bash
streamlit run app.py
```

Look for:
```
INFO:analyzers.semantic_code_search:Indexing repository: /path/to/repo
INFO:analyzers.semantic_code_search:Indexed 150 code chunks from 25 files
INFO:analyzers.multi_intent_analyzer:Analyzing query: how is routing implemented
INFO:analyzers.semantic_code_search:Searching for intent: routing implementation
INFO:analyzers.semantic_code_search:Found 15 relevant chunks
INFO:analyzers.rag_explainer:Generating explanation...
```

### Step 2: Try Simple Query
1. Upload a repository
2. Go to Codebase Chat
3. Wait for "Codebase indexed!" message
4. Ask: "what is this codebase about?"
5. Should get response in 5-10 seconds

### Step 3: Check Indexed Status
In Codebase Chat, expand "📦 Current Codebase"
- Should show: "Indexed: X code chunks"
- If X = 0, indexing failed

## Common Issues & Solutions

### Issue 1: "No codebase loaded"
**Solution**: Upload repository first in "Upload Code" page

### Issue 2: Stuck on "Analyzing your question..."
**Possible causes**:
- AI model not responding
- Check terminal for errors
- Check AWS Bedrock credentials

**Solution**:
```bash
# Check .env file
cat .env | grep AWS

# Should see:
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=...
```

### Issue 3: "No relevant code found"
**Possible causes**:
- Indexing failed
- No code chunks created

**Solution**:
1. Check terminal logs for indexing errors
2. Try re-uploading repository
3. Check if repository has code files

### Issue 4: Empty response
**Possible causes**:
- AI model returned empty response
- Explanation generation failed

**Solution**:
1. Check terminal for errors
2. Try simpler question
3. Check AI model status

## Debug Commands

### Check if semantic search is working:
```python
# In Python console
from analyzers.semantic_code_search import SemanticCodeSearch
search = SemanticCodeSearch(orchestrator)
print(f"Chunks: {len(search.code_chunks)}")
print(f"Summaries: {len(search.file_summaries)}")
```

### Test intent analyzer:
```python
from analyzers.multi_intent_analyzer import MultiIntentAnalyzer
analyzer = MultiIntentAnalyzer(orchestrator)
intents = analyzer.analyze_query("how is routing implemented")
print(f"Found {len(intents)} intents")
for intent in intents:
    print(f"- {intent.intent_text}")
```

### Test RAG explainer:
```python
from analyzers.rag_explainer import RAGExplainer
explainer = RAGExplainer(orchestrator)
# Test with dummy data
result = explainer.generate_detailed_explanation(
    "test query",
    [],  # empty chunks
    None,
    use_web_search=False
)
print(result['explanation'])
```

## Enable Debug Mode

Add this to the top of `ui/codebase_chat.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

This will show ALL logs including:
- Every function call
- Every AI request
- Every search result
- Every error

## What to Check in Terminal

### Good Output:
```
INFO:analyzers.semantic_code_search:Indexing repository: /path
INFO:analyzers.semantic_code_search:Indexed 150 code chunks from 25 files
INFO:analyzers.multi_intent_analyzer:Analyzing query: how is routing implemented
INFO:analyzers.multi_intent_analyzer:Found 1 intents
INFO:analyzers.semantic_code_search:Searching for: routing implementation
INFO:analyzers.semantic_code_search:Total indexed chunks: 150
INFO:analyzers.semantic_code_search:Extracted keywords: ['routing', 'implementation']
INFO:analyzers.semantic_code_search:Filtered to 12 chunks with keyword matches
INFO:analyzers.semantic_code_search:Returning 12 candidates
INFO:analyzers.rag_explainer:Generating detailed explanation for: routing implementation
INFO:analyzers.rag_explainer:Explanation generated: 1234 chars
```

### Bad Output (Errors):
```
ERROR:analyzers.semantic_code_search:Repository indexing failed: ...
ERROR:analyzers.multi_intent_analyzer:Intent analysis failed: ...
ERROR:analyzers.rag_explainer:Explanation generation failed: ...
```

## Quick Fix Checklist

- [ ] Repository uploaded successfully
- [ ] Codebase Chat shows "Indexed: X chunks" (X > 0)
- [ ] AWS credentials configured in .env
- [ ] Terminal shows no ERROR messages
- [ ] Query appears in chat history
- [ ] Progress indicators show up
- [ ] Response appears within 10 seconds

## If Still Not Working

1. **Restart Streamlit**:
   ```bash
   # Stop with Ctrl+C
   streamlit run app.py
   ```

2. **Clear Cache**:
   ```bash
   rm -rf .streamlit/cache
   streamlit run app.py
   ```

3. **Check Python Version**:
   ```bash
   python --version
   # Should be 3.8+
   ```

4. **Reinstall Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Test AI Connection**:
   ```python
   from ai.langchain_orchestrator import LangChainOrchestrator
   from ai.bedrock_client import BedrockClient
   from config import load_config
   
   aws_config, _ = load_config()
   client = BedrockClient(aws_config)
   orchestrator = LangChainOrchestrator(client, None)
   
   response = orchestrator.generate_completion("Hello", max_tokens=10)
   print(response)
   # Should print AI response
   ```

## Contact for Help

If none of this works, provide:
1. Terminal output (last 50 lines)
2. Error messages
3. Steps you tried
4. Repository size/type

---

**Most Common Fix**: Just reload the page and wait for "Codebase indexed!" message before asking questions!
