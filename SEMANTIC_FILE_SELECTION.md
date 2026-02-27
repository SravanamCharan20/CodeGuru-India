# Semantic AI-Powered File Selection

## Problem
The previous keyword-based file selection was too rigid and failed to find relevant files even when they existed. For example, searching for "routing" wouldn't find `App.js` or `index.js` files that actually contain routing logic.

## Solution
Implemented a truly semantic, AI-driven file selection system that:

1. **Analyzes repository structure contextually** - Not just keyword matching
2. **Understands semantic relationships** - Knows that `App.js` often contains routing, `index.js` is an entry point, etc.
3. **Considers file locations** - Understands that files in `src/`, `components/`, `pages/` are important
4. **Thinks like a developer** - Knows common patterns and conventions

## How It Works

### 1. AI Semantic Analysis (Primary Method)
```python
def _ai_semantic_file_selection(files, intent, repo_context):
    # Sends file list to AI with user's learning goal
    # AI analyzes paths, names, locations semantically
    # Returns 10-20 most relevant files
```

**AI Prompt Strategy**:
- Provides user's learning goal in plain language
- Shows all file paths and names
- Asks AI to think semantically and contextually
- Examples:
  - "routing" → Look for route, router, navigation, App, index, pages
  - "authentication" → Look for auth, login, user, session, token
  - "state management" → Look for store, redux, context, state

**AI Response**:
- Returns JSON array of file paths
- Ranked by relevance
- Typically 10-20 files

### 2. Keyword-Based Fallback
If AI fails or is unavailable, falls back to enhanced keyword matching with multiple fallback levels.

## Key Improvements

### Before (Keyword-Based)
```
User: "learn routing"
System: Looks for files with "routing" in name
Result: ❌ No files found (even though App.js has routing)
```

### After (Semantic AI)
```
User: "learn routing"
AI: Analyzes semantically
  - App.js → Main entry, likely has routing setup
  - index.js → Entry point, routing configuration
  - pages/ → Route components
  - components/Header.js → Navigation links
Result: ✅ 15 relevant files found
```

## Examples

### Example 1: Routing
**User Goal**: "i want to learn how the routing works in this app"

**AI Analysis**:
- Identifies `App.js` as main entry point (routing setup)
- Finds `index.js` files (route definitions)
- Locates `pages/` or `routes/` directories
- Includes navigation components
- Finds route configuration files

**Selected Files**:
- `src/App.js` - Main routing setup
- `src/index.js` - Entry point
- `src/components/Header.js` - Navigation
- `src/pages/Home.js` - Route component
- `src/routes/index.js` - Route definitions

### Example 2: Authentication
**User Goal**: "learn authentication"

**AI Analysis**:
- Looks for auth, login, user files
- Finds session/token management
- Identifies middleware/guards
- Locates user models

**Selected Files**:
- `src/auth/login.js`
- `src/middleware/auth.js`
- `src/models/User.js`
- `src/utils/token.js`

## Technical Details

### File Selection Flow
```
1. Get all files from repository
2. Filter out excluded files (node_modules, build, etc.)
3. Try AI semantic selection
   ├─ Success → Use AI-selected files
   └─ Failure → Fall back to keyword-based
4. Return selected files with relevance scores
```

### AI Integration
- Uses `LangChainOrchestrator.generate_completion()`
- Temperature: 0.3 (focused, deterministic)
- Max tokens: 500
- Response format: JSON array of file paths

### Error Handling
- Graceful fallback to keyword-based if AI fails
- Multiple parsing strategies for AI response
- Comprehensive logging for debugging

## Benefits

1. **More Accurate** - Finds files that keyword matching misses
2. **Context-Aware** - Understands repository structure and conventions
3. **Flexible** - Works with any repository structure
4. **Intelligent** - Learns from repository patterns
5. **Reliable** - Has fallback mechanisms

## Testing

Test with Namaste-React repository:
```
Repository: https://github.com/SravanamCharan20/Namaste-React
Intent: "i want to learn how the routing works in this app"
Expected: Should find App.js, routing components, navigation files
```

## Configuration

No configuration needed - works out of the box with any repository.

## Performance

- AI call: ~2-3 seconds
- Fallback: <1 second
- Total: ~3-4 seconds for file selection

## Future Enhancements

1. Cache AI selections for similar intents
2. Learn from user feedback
3. Support for multi-language repositories
4. File content analysis (not just paths)
