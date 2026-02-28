"""
Unified Code Analysis Interface.

Consolidates single file upload and repository analysis into one streamlined workflow.
"""

import streamlit as st
import logging
from dataclasses import asdict, is_dataclass
from typing import Optional
from ui.design_system import section_header, spacing, info_box
from ui.learning_artifacts_dashboard import render_learning_artifacts_dashboard

logger = logging.getLogger(__name__)


def _to_serializable(value):
    """Best-effort conversion for dataclasses/objects to JSON-safe structures."""
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, dict):
        return {k: _to_serializable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_to_serializable(v) for v in value]
    if hasattr(value, "__dict__"):
        return _to_serializable(vars(value))
    return value


def _ensure_memory_session(source_type: str, title: str, source_ref: str, summary: str = "") -> Optional[str]:
    """Create or reuse persistent memory session for current analysis source."""
    memory_store = st.session_state.get("memory_store")
    if not memory_store:
        return None

    existing_id = st.session_state.get("current_analysis_session_id")
    if existing_id:
        existing = memory_store.get_session(existing_id)
        if existing and existing.get("source_ref") == source_ref:
            if summary:
                memory_store.touch_session(existing_id, summary=summary[:1000])
            else:
                memory_store.touch_session(existing_id)
            return existing_id

    user_id = st.session_state.get("user_id", "anonymous")
    language = st.session_state.get("selected_language", "english")
    session_id = memory_store.create_session(
        user_id=user_id,
        source_type=source_type,
        title=title,
        source_ref=source_ref,
        language=language,
        summary=summary[:1000] if summary else "",
    )
    st.session_state.current_analysis_session_id = session_id
    return session_id


def render_unified_code_analysis(
    orchestrator,
    repository_manager,
    intent_interpreter,
    session_manager,
    code_analyzer,
    flashcard_manager
):
    """
    Render unified code analysis interface.
    
    Args:
        orchestrator: IntentDrivenOrchestrator instance
        repository_manager: RepositoryManager instance
        intent_interpreter: IntentInterpreter instance
        session_manager: SessionManager instance
        code_analyzer: CodeAnalyzer instance
        flashcard_manager: FlashcardManager instance
    """
    section_header(
        "Code Analysis",
        "Upload code and analyze with AI-powered insights"
    )
    
    # Initialize workflow state
    if 'analysis_mode' not in st.session_state:
        st.session_state.analysis_mode = None
    if 'workflow_step' not in st.session_state:
        st.session_state.workflow_step = 'upload'
    
    # Step 1: Upload
    if st.session_state.workflow_step == 'upload':
        _render_upload_step(
            repository_manager,
            session_manager,
            code_analyzer
        )
    
    # Step 2: Intent (only for deep mode)
    elif st.session_state.workflow_step == 'intent':
        _render_intent_step(
            intent_interpreter,
            session_manager
        )
    
    # Step 3: Analysis
    elif st.session_state.workflow_step == 'analyze':
        _render_analysis_step(
            orchestrator,
            session_manager,
            code_analyzer,
            flashcard_manager
        )
    
    # Step 4: Results
    elif st.session_state.workflow_step == 'results':
        _render_results_step(session_manager)


def _render_upload_step(repository_manager, session_manager, code_analyzer):
    """Render unified upload interface."""
    
    # Upload method tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 Single File",
        "🔗 GitHub URL",
        "📦 ZIP/Folder",
        "🎤 Voice Query"
    ])
    
    # Tab 1: Single File Upload
    with tab1:
        spacing("md")
        _render_single_file_upload(session_manager, code_analyzer)
    
    # Tab 2: GitHub URL
    with tab2:
        spacing("md")
        _render_github_upload(repository_manager, session_manager)
    
    # Tab 3: ZIP/Folder Upload
    with tab3:
        spacing("md")
        _render_zip_folder_upload(repository_manager, session_manager)
    
    # Tab 4: Voice Query
    with tab4:
        spacing("md")
        _render_voice_query(session_manager)
    
    # Show uploaded content summary
    _show_upload_summary(session_manager)


def _render_single_file_upload(session_manager, code_analyzer):
    """Render single file upload interface."""
    st.markdown("### Quick Analysis")
    st.caption("Upload a single code file for fast analysis")
    
    uploaded_file = st.file_uploader(
        "Choose a code file",
        type=['py', 'js', 'jsx', 'ts', 'tsx', 'java', 'cpp', 'c', 'go', 'rb'],
        help="Supported: Python, JavaScript, TypeScript, Java, C++, C, Go, Ruby"
    )
    
    if uploaded_file:
        # Store file in session using existing method
        file_content = uploaded_file.read().decode('utf-8')
        session_manager.set_uploaded_code(file_content, uploaded_file.name)
        
        st.success(f"✅ Uploaded: {uploaded_file.name}")
        
        # Analysis mode selection
        st.markdown("### Analysis Mode")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("⚡ Quick Analysis", use_container_width=True, type="primary"):
                st.session_state.analysis_mode = 'quick'
                st.session_state.workflow_step = 'analyze'
                st.rerun()
        
        with col2:
            if st.button("🧠 Deep Analysis", use_container_width=True):
                st.session_state.analysis_mode = 'deep'
                st.session_state.workflow_step = 'intent'
                st.rerun()
        
        st.caption("Quick: Fast code explanation | Deep: Intent-driven with learning artifacts")


def _render_github_upload(repository_manager, session_manager):
    """Render GitHub repository upload interface."""
    st.markdown("### GitHub Repository")
    st.caption("Analyze an entire repository from GitHub")
    
    github_url = st.text_input(
        "Repository URL",
        placeholder="https://github.com/username/repository",
        help="Enter the full GitHub repository URL"
    )
    
    if st.button("Upload Repository", type="primary"):
        if not github_url:
            st.error("Please enter a GitHub URL")
        else:
            with st.spinner("Cloning repository..."):
                result = repository_manager.upload_from_github(github_url)
                
                if result.success:
                    session_manager.set_current_repository(result.repo_path, result.repo_analysis)
                    _ensure_memory_session(
                        source_type="repository",
                        title=(result.repo_analysis.repo_url.rstrip("/").split("/")[-1]
                               if result.repo_analysis and getattr(result.repo_analysis, "repo_url", None)
                               else "repository"),
                        source_ref=result.repo_path,
                        summary=getattr(result.repo_analysis, "summary", ""),
                    )
                    st.success(f"✅ Repository uploaded successfully!")
                    st.session_state.analysis_mode = 'deep'
                    st.session_state.workflow_step = 'intent'
                    st.rerun()
                else:
                    st.error(f"❌ Upload failed: {result.error_message}")


def _render_zip_folder_upload(repository_manager, session_manager):
    """Render ZIP file and folder upload interface."""
    st.markdown("### ZIP File or Folder")
    st.caption("Upload a compressed repository or select a local folder")
    
    # ZIP file upload
    st.markdown("#### Upload ZIP File")
    zip_file = st.file_uploader(
        "Choose a ZIP file",
        type=['zip'],
        help="Upload a ZIP file containing your code repository"
    )
    
    if zip_file:
        if st.button("Process ZIP File", type="primary"):
            with st.spinner("Extracting and analyzing..."):
                result = repository_manager.upload_from_zip(zip_file)
                
                if result.success:
                    session_manager.set_current_repository(result.repo_path, result.repo_analysis)
                    _ensure_memory_session(
                        source_type="repository",
                        title=(result.repo_analysis.repo_url.rstrip("/").split("/")[-1]
                               if result.repo_analysis and getattr(result.repo_analysis, "repo_url", None)
                               else "repository_zip"),
                        source_ref=result.repo_path,
                        summary=getattr(result.repo_analysis, "summary", ""),
                    )
                    st.success("✅ ZIP file processed successfully!")
                    st.session_state.analysis_mode = 'deep'
                    st.session_state.workflow_step = 'intent'
                    st.rerun()
                else:
                    st.error(f"❌ Processing failed: {result.error_message}")
    
    spacing("lg")
    
    # Folder selection
    st.markdown("#### Select Local Folder")
    folder_path = st.text_input(
        "Folder Path",
        placeholder="/path/to/your/code/folder",
        help="Enter the full path to your local code folder"
    )
    
    if folder_path and st.button("Analyze Folder", type="primary"):
        with st.spinner("Analyzing folder..."):
            result = repository_manager.upload_from_folder(folder_path)
            
            if result.success:
                session_manager.set_current_repository(result.repo_path, result.repo_analysis)
                _ensure_memory_session(
                    source_type="repository",
                    title=(result.repo_analysis.repo_url.rstrip("/").split("/")[-1]
                           if result.repo_analysis and getattr(result.repo_analysis, "repo_url", None)
                           else "repository_folder"),
                    source_ref=result.repo_path,
                    summary=getattr(result.repo_analysis, "summary", ""),
                )
                st.success("✅ Folder analyzed successfully!")
                st.session_state.analysis_mode = 'deep'
                st.session_state.workflow_step = 'intent'
                st.rerun()
            else:
                st.error(f"❌ Analysis failed: {result.error_message}")


def _render_voice_query(session_manager):
    """Render voice query interface."""
    st.markdown("### Voice Query")
    st.caption("Ask questions about code using your voice")
    
    # Initialize voice query state
    if "voice_query" not in st.session_state:
        st.session_state.voice_query = ""
    if "voice_transcript" not in st.session_state:
        st.session_state.voice_transcript = ""
    
    # Voice processor
    voice_processor = st.session_state.get("voice_processor")
    
    if voice_processor:
        languages = voice_processor.get_supported_languages()
        
        # Language selector for voice
        voice_lang = st.selectbox(
            "Select Voice Language",
            options=list(languages.keys()),
            format_func=lambda x: languages[x],
            key="voice_language"
        )
        
        info_box(f"Speak in {languages[voice_lang]} to ask questions about your code", "info")
        
        spacing("sm")
        
        # Audio recorder component
        st.markdown("**Record your question:**")
        
        try:
            # Try to use streamlit-audio-recorder if available
            from audio_recorder_streamlit import audio_recorder
            
            audio_bytes = audio_recorder(
                text="Click to record",
                recording_color="#0066CC",
                neutral_color="#E5E5E5",
                icon_size="2x"
            )
            
            if audio_bytes:
                st.success("✓ Audio recorded!")
                
                # Process audio
                if st.button("🔄 Transcribe Audio", type="primary"):
                    with st.spinner("🎙️ Transcribing..."):
                        result = voice_processor.process_audio(audio_bytes, voice_lang)
                        
                        if result:
                            st.session_state.voice_transcript = result.transcript
                            st.session_state.voice_query = result.transcript
                            
                            st.success(f"✓ Transcribed ({result.confidence:.0%} confidence)")
                            st.info(f"**Transcript:** {result.transcript}")
                        else:
                            st.error("Failed to transcribe audio")
        
        except ImportError:
            st.warning("⚠️ Audio recorder not available. Install with: pip install streamlit-audio-recorder")
            st.info("💡 Use the text box below instead")
    
    else:
        st.warning("⚠️ Voice processor not initialized")
    
    spacing("md")
    
    # Text input as fallback
    st.markdown("**Or type your question:**")
    voice_query = st.text_area(
        "Type your question",
        value=st.session_state.voice_transcript,
        placeholder="What does this function do?\nExplain the authentication logic\nHow does this code work?",
        height=120,
        key="voice_query_input",
        label_visibility="collapsed"
    )
    
    if voice_query:
        st.session_state.voice_query = voice_query
    
    # Process voice query button
    if st.session_state.voice_query:
        if st.button("🚀 Process Query", type="primary", use_container_width=True):
            st.info("Voice query processing will be integrated with code analysis in the next update")
            st.caption("For now, please use the file upload tabs to analyze code")


def _show_upload_summary(session_manager):
    """Show summary of uploaded content."""
    # Check for uploaded file
    uploaded_code = session_manager.get_uploaded_code()
    uploaded_filename = st.session_state.get('uploaded_filename')
    
    # Check for uploaded repository
    current_repo = session_manager.get_current_repository()
    
    if uploaded_code or current_repo:
        spacing("lg")
        st.divider()
        st.markdown("### 📊 Upload Summary")
        
        if uploaded_code and uploaded_filename:
            st.info(f"**File**: {uploaded_filename}")
        
        if current_repo:
            repo_analysis = current_repo.get('repo_analysis')
            if repo_analysis:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Files", repo_analysis.total_files)
                with col2:
                    st.metric("Lines", f"{repo_analysis.total_lines:,}")
                with col3:
                    languages = ", ".join(repo_analysis.languages.keys())
                    st.metric("Languages", len(repo_analysis.languages))
                
                with st.expander("Repository Details"):
                    st.write(f"**URL**: {repo_analysis.repo_url}")
                    st.write(f"**Size**: {repo_analysis.total_size_bytes / 1024:.1f} KB")
                    st.write(f"**Languages**: {languages}")


def _render_intent_step(intent_interpreter, session_manager):
    """Render intent input step."""
    st.markdown("## 🎯 Define Your Learning Goal")
    st.caption("Tell us what you want to learn from this code")
    
    # Back button
    if st.button("← Back to Upload"):
        st.session_state.workflow_step = 'upload'
        st.rerun()
    
    spacing("md")
    
    # Intent input
    user_input = st.text_area(
        "What do you want to learn?",
        placeholder="Examples:\n- Understand the authentication flow\n- Learn how the payment system works\n- Prepare for interview questions about this codebase\n- Focus on the backend API architecture",
        height=150,
        help="Describe your learning goal in natural language"
    )
    
    # Quick intent templates
    st.markdown("#### Quick Templates")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔐 Authentication Flow", use_container_width=True):
            user_input = "Understand the authentication and authorization flow"
    
    with col2:
        if st.button("🏗️ Architecture", use_container_width=True):
            user_input = "Learn the overall system architecture and design patterns"
    
    with col3:
        if st.button("💼 Interview Prep", use_container_width=True):
            user_input = "Prepare for technical interview questions about this codebase"
    
    spacing("md")
    
    # Continue button
    if st.button("Continue to Analysis →", type="primary", disabled=not user_input):
        if user_input:
            # Interpret intent
            with st.spinner("Interpreting your learning goal..."):
                repo_context = session_manager.get_current_repository()
                if repo_context:
                    repo_analysis = repo_context.get('repo_analysis')
                    intent = intent_interpreter.interpret_intent(user_input, repo_analysis)
                    session_manager.set_current_intent(intent)
                    
                    # Check if clarification needed
                    if hasattr(intent, 'needs_clarification') and intent.needs_clarification:
                        st.warning("Your goal needs clarification")
                        if hasattr(intent, 'clarification_questions'):
                            for question in intent.clarification_questions:
                                st.write(f"- {question}")
                    else:
                        st.session_state.workflow_step = 'analyze'
                        st.rerun()
                else:
                    st.error("No repository found. Please upload code first.")


def _render_analysis_step(orchestrator, session_manager, code_analyzer, flashcard_manager):
    """Render analysis step."""
    st.markdown("## 🔍 Analyzing Code")
    
    analysis_mode = st.session_state.analysis_mode
    
    if analysis_mode == 'quick':
        _run_quick_analysis(session_manager, code_analyzer, flashcard_manager)
    elif analysis_mode == 'deep':
        _run_deep_analysis(orchestrator, session_manager)
    else:
        st.error("Invalid analysis mode")


def _run_quick_analysis(session_manager, code_analyzer, flashcard_manager):
    """Run quick single-file analysis."""
    code = session_manager.get_uploaded_code()
    filename = st.session_state.get('uploaded_filename', 'code.py')
    
    if not code:
        st.error("No file found. Please upload a file first.")
        return
    
    with st.spinner("Analyzing code..."):
        try:
            analysis_session_id = _ensure_memory_session(
                source_type="code",
                title=filename,
                source_ref=filename,
                summary=f"Quick analysis for {filename}",
            )

            # Analyze file
            analysis = code_analyzer.analyze_file(code, filename)
            
            # Generate flashcards
            flashcards = flashcard_manager.generate_flashcards(
                analysis,
                language=st.session_state.get("selected_language", "english"),
            )
            flashcards_serialized = _to_serializable(flashcards)
            
            # Store results in session state
            st.session_state.current_analysis = {
                'mode': 'quick',
                'analysis': analysis,
                'flashcards': flashcards_serialized,
                'filename': filename
            }

            memory_store = st.session_state.get("memory_store")
            if memory_store and analysis_session_id:
                memory_store.touch_session(
                    analysis_session_id,
                    summary=f"Quick analysis complete for {filename}",
                )
                memory_store.save_artifact(
                    analysis_session_id,
                    "quick_analysis",
                    {
                        "filename": filename,
                        "analysis": _to_serializable(analysis),
                    },
                    replace=True,
                )
                memory_store.save_artifact(
                    analysis_session_id,
                    "quick_flashcards",
                    flashcards_serialized,
                    replace=True,
                )
            
            st.success("✅ Analysis complete!")
            st.session_state.workflow_step = 'results'
            st.rerun()
        
        except Exception as e:
            logger.error(f"Quick analysis failed: {e}")
            st.error(f"Analysis failed: {str(e)}")


def _run_deep_analysis(orchestrator, session_manager):
    """Run deep intent-driven analysis."""
    repo_context = session_manager.get_current_repository()
    intent_data = session_manager.get_current_intent()
    
    if not repo_context or not intent_data:
        st.error("Missing repository or intent. Please start over.")
        return
    
    with st.spinner("Running deep analysis..."):
        try:
            repo_path = repo_context.get('repo_path')
            repo_analysis = repo_context.get('repo_analysis')
            intent = intent_data.get('intent')
            user_input = intent.original_input if hasattr(intent, 'original_input') else "Analyze this repository"
            analysis_session_id = _ensure_memory_session(
                source_type="repository",
                title=(getattr(repo_analysis, "repo_url", repo_path).rstrip("/").split("/")[-1]
                       if repo_analysis
                       else "repository"),
                source_ref=repo_path,
                summary=getattr(repo_analysis, "summary", ""),
            )
            
            # Index repository for semantic search
            if 'semantic_search' in st.session_state:
                with st.spinner("Indexing codebase for intelligent search..."):
                    st.session_state.semantic_search.index_repository(repo_path, repo_analysis)
                    st.success("✓ Codebase indexed - you can now use Codebase Chat!")
            
            # Run complete workflow
            result = orchestrator.analyze_repository_with_intent(
                repo_path,
                user_input
            )
            
            if 'error' in result:
                st.error(f"Analysis failed: {result['error']}")
            else:
                # Store results in session state
                st.session_state.current_analysis = {
                    'mode': 'deep',
                    'result': result
                }

                memory_store = st.session_state.get("memory_store")
                if memory_store and analysis_session_id and result.get("status") == "success":
                    memory_store.touch_session(
                        analysis_session_id,
                        summary=result.get("concept_summary", {}).get("summary", "Deep analysis completed"),
                    )
                    memory_store.save_artifact(
                        analysis_session_id,
                        "deep_analysis",
                        _to_serializable(result),
                        replace=True,
                    )
                
                st.success("✅ Deep analysis complete!")
                st.session_state.workflow_step = 'results'
                st.rerun()
        
        except Exception as e:
            logger.error(f"Deep analysis failed: {e}")
            st.error(f"Analysis failed: {str(e)}")


def _render_results_step(session_manager):
    """Render analysis results."""
    analysis = st.session_state.get('current_analysis')
    
    if not analysis:
        st.error("No analysis results found")
        return
    
    mode = analysis.get('mode')
    
    # Header with restart button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("## 📊 Analysis Results")
    with col2:
        if st.button("🔄 New Analysis", use_container_width=True):
            st.session_state.workflow_step = 'upload'
            st.session_state.analysis_mode = None
            st.session_state.current_analysis = None
            st.session_state.current_analysis_session_id = None
            st.session_state.loaded_chat_session_id = None
            st.rerun()
    
    spacing("md")
    
    if mode == 'quick':
        _render_quick_results(analysis)
    elif mode == 'deep':
        _render_deep_results(analysis, session_manager)


def _render_quick_results(analysis):
    """Render quick analysis results."""
    analysis_data = analysis.get('analysis', {})
    if not isinstance(analysis_data, dict):
        analysis_data = _to_serializable(analysis_data)
    flashcards = analysis.get('flashcards', [])
    filename = analysis.get('filename', 'code file')
    
    # Tabs for different views
    tab1, tab2 = st.tabs(["📝 Explanation", "🎴 Flashcards"])
    
    with tab1:
        st.markdown(f"### Code Explanation: {filename}")
        
        if 'explanation' in analysis_data:
            st.markdown(analysis_data['explanation'])
        elif 'summary' in analysis_data:
            st.markdown(analysis_data['summary'])
        else:
            st.info("No explanation available")
        
        spacing("md")
        
        if 'structure' in analysis_data:
            with st.expander("📊 Code Structure"):
                structure = analysis_data['structure']
                
                if isinstance(structure, dict):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        classes = structure.get('classes', [])
                        st.metric("Classes", len(classes))
                        if classes:
                            st.write("**Classes:**")
                            for cls in classes[:5]:
                                st.write(f"- {cls}")
                    
                    with col2:
                        functions = structure.get('functions', [])
                        st.metric("Functions", len(functions))
                        if functions:
                            st.write("**Functions:**")
                            for func in functions[:5]:
                                st.write(f"- {func}")
                    
                    with col3:
                        imports = structure.get('imports', [])
                        st.metric("Imports", len(imports))
                        if imports:
                            st.write("**Imports:**")
                            for imp in imports[:5]:
                                st.write(f"- {imp}")
                else:
                    st.json(structure)
        
        if 'concepts' in analysis_data:
            with st.expander("💡 Key Concepts"):
                concepts = analysis_data['concepts']
                if isinstance(concepts, list):
                    for concept in concepts:
                        st.write(f"- {concept}")
                else:
                    st.write(concepts)
    
    with tab2:
        st.markdown("### Flashcards")
        
        if flashcards and len(flashcards) > 0:
            st.info(f"Generated {len(flashcards)} flashcards for review")
            
            for i, card in enumerate(flashcards, 1):
                with st.expander(f"Card {i}: {card.get('front', 'Question')}"):
                    st.markdown(f"**Question:** {card.get('front', 'N/A')}")
                    st.markdown(f"**Answer:** {card.get('back', 'N/A')}")
                    
                    if 'code_evidence' in card:
                        st.code(card['code_evidence'], language='python')
        else:
            st.info("No flashcards generated. Flashcards are created for more complex code.")
            st.caption("Try uploading a larger file or use Deep Analysis mode for comprehensive learning materials.")


def _render_deep_results(analysis, session_manager):
    """Render deep analysis results."""
    result = analysis.get('result', {})
    
    # Check result status
    status = result.get('status', 'unknown')
    
    if status == 'error':
        st.error(f"Analysis failed: {result.get('error', 'Unknown error')}")
        return
    
    elif status == 'clarification_needed':
        st.warning("Your learning goal needs clarification")
        questions = result.get('questions', [])
        for question in questions:
            st.write(f"- {question}")
        st.info("Please go back and refine your learning goal")
        return
    
    elif status == 'no_files_found':
        st.warning("No relevant files found for your learning goal")
        suggestions = result.get('suggestions', [])
        if suggestions:
            st.write("**Suggestions:**")
            for suggestion in suggestions:
                st.write(f"- {suggestion}")
        return
    
    elif status == 'success':
        # Show summary
        intent = result.get('intent')
        selection_result = result.get('selection_result')
        
        if intent and selection_result:
            st.success("✅ Analysis complete!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Files Analyzed", len(selection_result.selected_files))
            with col2:
                flashcards = result.get('flashcards', [])
                st.metric("Flashcards", len(flashcards))
            with col3:
                quiz = result.get('quiz', {})
                questions = quiz.get('questions', [])
                st.metric("Quiz Questions", len(questions))
            
            spacing("md")
        
        # Use existing dashboard to display artifacts
        render_learning_artifacts_dashboard(session_manager)
    
    else:
        st.error(f"Unknown analysis status: {status}")
