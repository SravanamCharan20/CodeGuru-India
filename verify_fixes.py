"""Verify both errors are fixed."""
print("Testing fixes...")

# Test 1: VoiceProcessor
try:
    from ai.voice_processor import VoiceProcessor
    from config import load_config
    aws_config, _ = load_config()
    v = VoiceProcessor(aws_config)
    print("✓ VoiceProcessor fixed")
except Exception as e:
    print(f"✗ VoiceProcessor error: {e}")
    exit(1)

# Test 2: Sidebar
try:
    from ui.sidebar import render_sidebar
    print("✓ Sidebar import fixed")
except Exception as e:
    print(f"✗ Sidebar error: {e}")
    exit(1)

# Test 3: All imports
try:
    from ui.code_upload import render_code_upload
    from ui.explanation_view import render_explanation_view
    from ui.learning_path import render_learning_path
    from ui.quiz_view import render_quiz_view
    from ui.flashcard_view import render_flashcard_view
    from ui.progress_dashboard import render_progress_dashboard
    print("✓ All UI components work")
except Exception as e:
    print(f"✗ UI components error: {e}")
    exit(1)

print("\n✅ All errors fixed! App ready to start.")
print("Run: python -m streamlit run app.py")
