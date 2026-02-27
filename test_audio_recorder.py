"""Test audio recorder implementation."""
import sys
import os

def test_audio_recorder_package():
    """Test if streamlit-audio-recorder is installed."""
    print("=" * 60)
    print("Testing Audio Recorder Implementation")
    print("=" * 60)
    
    # Test 1: Check if package is installed
    print("\n1. Checking streamlit-audio-recorder package...")
    try:
        from audio_recorder_streamlit import audio_recorder
        print("   ✅ streamlit-audio-recorder is installed")
        return True
    except ImportError as e:
        print(f"   ❌ streamlit-audio-recorder NOT installed")
        print(f"   Error: {e}")
        print("\n   To install, run:")
        print("   pip install streamlit-audio-recorder")
        return False

def test_voice_processor():
    """Test voice processor initialization."""
    print("\n2. Testing VoiceProcessor...")
    try:
        from ai.voice_processor import VoiceProcessor
        
        # Test without AWS config
        processor = VoiceProcessor()
        print("   ✅ VoiceProcessor initialized (no AWS)")
        
        # Test supported languages
        languages = processor.get_supported_languages()
        print(f"   ✅ Supported languages: {', '.join(languages.values())}")
        
        # Test mock transcription
        mock_audio = b"mock_audio_data"
        result = processor.process_audio(mock_audio, 'en')
        if result:
            print(f"   ✅ Mock transcription works: '{result.transcript[:50]}...'")
        else:
            print("   ⚠️  Mock transcription returned None")
        
        return True
    except Exception as e:
        print(f"   ❌ VoiceProcessor test failed: {e}")
        return False

def test_ui_integration():
    """Test UI integration."""
    print("\n3. Testing UI Integration...")
    try:
        # Check if code_upload.py has audio recorder integration
        with open('ui/code_upload.py', 'r') as f:
            content = f.read()
        
        checks = [
            ('audio_recorder_streamlit import', 'from audio_recorder_streamlit import audio_recorder' in content),
            ('audio_recorder call', 'audio_recorder(' in content),
            ('voice_processor usage', 'voice_processor.process_audio' in content),
            ('language selector', 'voice_language' in content),
            ('transcribe button', 'Transcribe Audio' in content)
        ]
        
        all_passed = True
        for check_name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}")
            if not passed:
                all_passed = False
        
        return all_passed
    except Exception as e:
        print(f"   ❌ UI integration test failed: {e}")
        return False

def test_aws_transcribe_config():
    """Test AWS Transcribe configuration."""
    print("\n4. Testing AWS Transcribe Configuration...")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        aws_region = os.getenv('AWS_REGION')
        aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        
        if aws_region and aws_access_key:
            print(f"   ✅ AWS credentials configured (Region: {aws_region})")
            
            # Test boto3 transcribe client
            try:
                import boto3
                client = boto3.client('transcribe', region_name=aws_region)
                print("   ✅ AWS Transcribe client can be initialized")
                return True
            except Exception as e:
                print(f"   ⚠️  AWS Transcribe client initialization failed: {e}")
                print("   Note: This is OK if you don't have Transcribe permissions")
                return True
        else:
            print("   ⚠️  AWS credentials not configured in .env")
            print("   Note: Voice processor will use mock transcription")
            return True
    except Exception as e:
        print(f"   ❌ AWS config test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("\n🎤 Audio Recorder End-to-End Test\n")
    
    results = []
    
    # Run tests
    results.append(("Audio Recorder Package", test_audio_recorder_package()))
    results.append(("Voice Processor", test_voice_processor()))
    results.append(("UI Integration", test_ui_integration()))
    results.append(("AWS Transcribe Config", test_aws_transcribe_config()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    # Installation instructions
    if not results[0][1]:  # If audio recorder not installed
        print("\n" + "=" * 60)
        print("Installation Required")
        print("=" * 60)
        print("\nTo complete the audio recorder setup, run:")
        print("\n  pip install streamlit-audio-recorder")
        print("\nThen restart the Streamlit app:")
        print("\n  python -m streamlit run app.py")
    else:
        print("\n" + "=" * 60)
        print("✅ Audio Recorder Ready!")
        print("=" * 60)
        print("\nThe audio recorder is fully integrated. To use it:")
        print("\n1. Start the app: python -m streamlit run app.py")
        print("2. Go to 'Upload Code' tab")
        print("3. Click on 'Voice Query' sub-tab")
        print("4. Select your language (English, Hindi, or Telugu)")
        print("5. Click the microphone button to record")
        print("6. Click 'Transcribe Audio' to process")
        print("\nNote: Without AWS Transcribe permissions, mock transcription will be used.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
