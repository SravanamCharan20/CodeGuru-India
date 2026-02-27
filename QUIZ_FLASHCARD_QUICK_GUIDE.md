# Code-Based Quiz & Flashcard - Quick Guide

## What Changed?

Quizzes and flashcards are now generated from YOUR uploaded code, not random generic content.

## How to Use

### Step 1: Upload Code
```
1. Go to "Upload Code" tab
2. Upload a code file (Python, JavaScript, etc.)
3. Click "Analyze Code" button
```

### Step 2: View Quiz
```
1. Go to "Quizzes" tab
2. Click "Start Quiz" button
3. Answer questions about YOUR code
```

### Step 3: View Flashcards
```
1. Go to "Flashcards" tab
2. Review flashcards about YOUR code
3. Mark cards as reviewed or mastered
```

## What You'll See

### Before Uploading Code:
- **Quizzes tab**: "Upload and analyze code first to generate quizzes"
- **Flashcards tab**: "Upload and analyze code first to generate flashcards"

### After Uploading Code:
- **Quizzes tab**: Quiz with 5 questions about your functions, classes, and patterns
- **Flashcards tab**: Flashcards about your functions, classes, and patterns

## Example

If you upload this code:
```python
def calculate_discount(price, percentage):
    '''Calculate discounted price'''
    return price * (1 - percentage/100)

class ShoppingCart:
    '''Manages shopping cart'''
    def add_item(self, item):
        pass
```

You'll get:
- **Quiz Question**: "What does the function 'calculate_discount' do?"
- **Flashcard**: Front: "What does 'calculate_discount' do?" / Back: "Calculate discounted price. Parameters: price, percentage"

## Run Tests

```bash
python test_code_based_quiz_flashcards.py
```

Expected: ✅ ALL TESTS PASSED SUCCESSFULLY!

## Start App

```bash
python -m streamlit run app.py
```

Then navigate to http://localhost:8501

---

**Status**: ✅ WORKING
**Language Support**: English, Hindi, Telugu
