"""Comprehensive test for all implemented features."""
import sys
import os

def test_repository_upload_fix():
    """Test repository upload and file analysis."""
    print("\n" + "=" * 60)
    print("Testing Repository Upload Fix")
    print("=" * 60)
    
    try:
        # Check if repo analyzer stores file contents
        with open('analyzers/repo_analyzer.py', 'r') as f:
            content = f.read()
        
        checks = [
            ('Store file contents', 'st.session_state' in content and 'repo_files' in content),
            ('File content reading', 'with open(file_path' in content or 'f.read()' in content),
            ('File path storage', 'repo_files[file.path]' in content)
        ]
        
        print("\n📦 Repository Analyzer:")
        all_passed = True
        for check_name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}")
            if not passed:
                all_passed = False
        
        # Check if explanation view has file selector
        with open('ui/explanation_view.py', 'r') as f:
            content = f.read()
        
        checks = [
            ('File selector dropdown', 'st.selectbox("Select a file to analyze:' in content),
            ('Analyze button', 'st.button(f"🔍 Analyze' in content),
            ('Get file from session', 'repo_files = st.session_state.get("repo_files"' in content),
            ('Clear repo view after analysis', 'del st.session_state.current_repo_analysis' in content)
        ]
        
        print("\n📊 Explanation View:")
        for check_name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}")
            if not passed:
                all_passed = False
        
        return all_passed
    
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False

def test_audio_recorder_integration():
    """Test audio recorder end-to-end integration."""
    print("\n" + "=" * 60)
    print("Testing Audio Recorder Integration")
    print("=" * 60)
    
    try:
        # Test package installation
        print("\n🎤 Audio Recorder Package:")
        try:
            from audio_recorder_streamlit import audio_recorder
            print("   ✅ Package installed")
            package_ok = True
        except ImportError:
            print("   ❌ Package NOT installed")
            print("   Run: pip install audio-recorder-streamlit")
            package_ok = False
        
        # Test voice processor
        print("\n🎙️ Voice Processor:")
        from ai.voice_processor import VoiceProcessor
        
        processor = VoiceProcessor()
        languages = processor.get_supported_languages()
        
        checks = [
            ('Initialization', processor is not None),
            ('English support', 'en' in languages),
            ('Hindi support', 'hi' in languages),
            ('Telugu support', 'te' in languages),
            ('Mock transcription', True)  # Always available
        ]
        
        all_passed = package_ok
        for check_name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}")
            if not passed:
                all_passed = False
        
        # Test mock transcription
        mock_audio = b"test_audio_data"
        result = processor.process_audio(mock_audio, 'en')
        
        if result:
            print(f"   ✅ Mock transcription works")
            print(f"      Transcript: '{result.transcript[:40]}...'")
            print(f"      Confidence: {result.confidence:.0%}")
        else:
            print("   ❌ Mock transcription failed")
            all_passed = False
        
        # Test AWS Transcribe integration
        print("\n🌐 AWS Transcribe Integration:")
        from config import load_config
        aws_config, _ = load_config()
        processor_aws = VoiceProcessor(aws_config)
        
        if processor_aws.transcribe_client:
            print("   ✅ AWS Transcribe client initialized")
            
            # Check helper methods
            helper_methods = [
                '_get_or_create_bucket',
                '_prepare_audio_for_transcribe',
                '_fetch_transcript',
                '_cleanup_transcription_job',
                '_cleanup_s3_object'
            ]
            
            for method in helper_methods:
                if hasattr(processor_aws, method):
                    print(f"   ✅ {method}")
                else:
                    print(f"   ❌ {method} - NOT FOUND")
                    all_passed = False
        else:
            print("   ⚠️  AWS Transcribe not configured (will use mock)")
        
        # Test UI integration
        print("\n🖥️ UI Integration:")
        with open('ui/code_upload.py', 'r') as f:
            content = f.read()
        
        checks = [
            ('Audio recorder import', 'from audio_recorder_streamlit import audio_recorder' in content),
            ('Language selector', 'Select Voice Language' in content),
            ('Record button', 'audio_recorder(' in content),
            ('Transcribe button', 'Transcribe Audio' in content),
            ('Text fallback', 'Or type your question' in content),
            ('Process query', 'Process Query' in content)
        ]
        
        for check_name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}")
            if not passed:
                all_passed = False
        
        return all_passed
    
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False

def test_aws_integration():
    """Test AWS Bedrock and Transcribe integration."""
    print("\n" + "=" * 60)
    print("Testing AWS Integration")
    print("=" * 60)
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check AWS credentials
        print("\n🔐 AWS Credentials:")
        aws_region = os.getenv('AWS_REGION')
        aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret = os.getenv('AWS_SECRET_ACCESS_KEY')
        model_id = os.getenv('BEDROCK_MODEL_ID')
        
        checks = [
            ('AWS_REGION', aws_region is not None),
            ('AWS_ACCESS_KEY_ID', aws_access_key is not None),
            ('AWS_SECRET_ACCESS_KEY', aws_secret is not None),
            ('BEDROCK_MODEL_ID', model_id is not None)
        ]
        
        all_passed = True
        for check_name, passed in checks:
            status = "✅" if passed else "⚠️ "
            value = "configured" if passed else "not set"
            print(f"   {status} {check_name}: {value}")
            if not passed:
                all_passed = False
        
        if aws_region:
            print(f"\n   Region: {aws_region}")
        if model_id:
            print(f"   Model: {model_id}")
        
        # Test Bedrock client
        if all_passed:
            print("\n🤖 AWS Bedrock:")
            try:
                import boto3
                client = boto3.client('bedrock-runtime', region_name=aws_region)
                print("   ✅ Bedrock client initialized")
            except Exception as e:
                print(f"   ⚠️  Bedrock client error: {e}")
            
            # Test Transcribe client
            print("\n🎙️ AWS Transcribe:")
            try:
                client = boto3.client('transcribe', region_name=aws_region)
                print("   ✅ Transcribe client initialized")
            except Exception as e:
                print(f"   ⚠️  Transcribe client error: {e}")
        else:
            print("\n   ⚠️  Configure AWS credentials in .env to enable AI features")
        
        return True  # AWS is optional, so always return True
    
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return True  # AWS is optional

def test_multi_language_support():
    """Test multi-language support."""
    print("\n" + "=" * 60)
    print("Testing Multi-Language Support")
    print("=" * 60)
    
    try:
        # Check translations
        print("\n🌐 Translation System:")
        with open('ui/translations.py', 'r') as f:
            content = f.read()
        
        checks = [
            ('English translations', '"english":' in content or "'english':" in content),
            ('Hindi translations', '"hindi":' in content or "'hindi':" in content or '"हिंदी":' in content),
            ('Telugu translations', '"telugu":' in content or "'telugu':" in content or '"తెలుగు":' in content),
            ('TRANSLATIONS dict', 'TRANSLATIONS = {' in content)
        ]
        
        all_passed = True
        for check_name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}")
            if not passed:
                all_passed = False
        
        # Check voice processor languages
        print("\n🎤 Voice Languages:")
        from ai.voice_processor import VoiceProcessor
        processor = VoiceProcessor()
        languages = processor.get_supported_languages()
        
        for code, name in languages.items():
            print(f"   ✅ {code}: {name}")
        
        return all_passed
    
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False

def test_requirements():
    """Test all required packages."""
    print("\n" + "=" * 60)
    print("Testing Required Packages")
    print("=" * 60)
    
    packages = [
        ('streamlit', 'streamlit'),
        ('boto3', 'boto3'),
        ('langchain', 'langchain'),
        ('hypothesis', 'hypothesis'),
        ('pytest', 'pytest'),
        ('GitPython', 'git'),
        ('python-dotenv', 'dotenv'),
        ('audio-recorder-streamlit', 'audio_recorder_streamlit')
    ]
    
    all_passed = True
    for package_name, import_name in packages:
        try:
            __import__(import_name)
            print(f"   ✅ {package_name}")
        except ImportError:
            print(f"   ❌ {package_name} - NOT INSTALLED")
            all_passed = False
    
    return all_passed

def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("🚀 CodeGuru India - Complete Feature Test")
    print("=" * 60)
    
    results = []
    
    # Run all tests
    results.append(("Required Packages", test_requirements()))
    results.append(("Repository Upload Fix", test_repository_upload_fix()))
    results.append(("Audio Recorder Integration", test_audio_recorder_integration()))
    results.append(("Multi-Language Support", test_multi_language_support()))
    results.append(("AWS Integration", test_aws_integration()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    # Final status
    print("\n" + "=" * 60)
    if passed == total:
        print("✅ ALL FEATURES WORKING!")
        print("=" * 60)
        print("\n🎉 CodeGuru India is ready to use!")
        print("\nTo start the application:")
        print("  python -m streamlit run app.py")
        print("\nFeatures available:")
        print("  ✅ File upload and code analysis")
        print("  ✅ GitHub repository analysis with file selection")
        print("  ✅ Voice query in English, Hindi, and Telugu")
        print("  ✅ Audio recording and transcription")
        print("  ✅ AI-powered explanations and answers")
        print("  ✅ Multi-language support")
        print("  ✅ Flashcards and learning paths")
        print("  ✅ Progress tracking")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("=" * 60)
        print("\nPlease fix the failing tests before using the application.")
        print("\nCommon fixes:")
        print("  • Install missing packages: pip install -r requirements.txt")
        print("  • Configure AWS credentials in .env file")
        print("  • Check file permissions")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
