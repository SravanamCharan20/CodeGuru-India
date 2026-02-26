"""Code upload interface component."""
import streamlit as st
from config import load_config
from ui.design_system import section_header, spacing, info_box


def render_code_upload():
    """Render code upload interface."""
    from ui.design_system import section_header, spacing
    
    # Header - minimal
    section_header("Upload Code for Analysis", "Upload files, analyze GitHub repositories, or ask questions with voice")
    
    _, app_config = load_config()
    session_manager = st.session_state.session_manager
    
    # Create tabs for different upload methods
    tab1, tab2, tab3 = st.tabs(["File Upload", "GitHub Repository", "Voice Query"])
    
    with tab1:
        spacing("md")
        
        st.markdown("""
        <div style="
            background: #F9F9F9;
            border-radius: 6px;
            padding: 16px;
            margin-bottom: 16px;
            border: 1px solid #E5E5E5;
        ">
            <p style="color: #1A1A1A; font-weight: 500; margin-bottom: 8px; font-size: 15px;">
                Supported Formats
            </p>
            <p style="color: #666666; font-size: 13px; margin-bottom: 12px;">
                Python, JavaScript, TypeScript, Java, C++, C, Go, Ruby
            </p>
            <p style="color: #1A1A1A; font-weight: 500; margin-bottom: 8px; font-size: 15px;">
                Max File Size
            </p>
            <p style="color: #666666; font-size: 13px; margin: 0;">
                {max_size} MB
            </p>
        </div>
        """.format(max_size=app_config.max_file_size_mb), unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose a code file",
            type=[ext.replace(".", "") for ext in app_config.supported_extensions],
            help="Drag and drop or click to upload",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            # Read file content
            file_content = uploaded_file.read().decode("utf-8")
            file_size_mb = len(file_content) / (1024 * 1024)
            lines_count = len(file_content.split('\n'))
            
            spacing("md")
            
            # Display file info - minimal metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("File Name", uploaded_file.name[:20] + "..." if len(uploaded_file.name) > 20 else uploaded_file.name)
            with col2:
                st.metric("File Size", f"{file_size_mb:.2f} MB")
            with col3:
                st.metric("Lines of Code", f"{lines_count:,}")
            
            # Store in session
            session_manager.set_uploaded_code(file_content, uploaded_file.name)
            
            spacing("md")
            
            # Show code preview
            with st.expander("Preview Code", expanded=False):
                st.code(file_content, language=_detect_language(uploaded_file.name), line_numbers=True)
    
    with tab2:
        spacing("md")
        
        info_box("Analyze entire repositories with automatic file detection and language breakdown", "info")
        
        repo_url = st.text_input(
            "GitHub Repository URL",
            placeholder="https://github.com/username/repository",
            help="Enter a public GitHub repository URL",
            label_visibility="collapsed"
        )
        
        if repo_url:
            if repo_url.startswith("https://github.com/"):
                info_box("Valid GitHub URL detected", "success")
            else:
                info_box("Please enter a valid GitHub URL (must start with https://github.com/)", "error")
    
    with tab3:
        spacing("md")
        
        # Initialize voice query state
        if "voice_query" not in st.session_state:
            st.session_state.voice_query = ""
        
        # Voice processor
        voice_processor = st.session_state.get("voice_processor")
        
        if voice_processor:
            languages = voice_processor.get_supported_languages()
            info_box(f"Multi-Language Voice Support: {', '.join(languages.values())}", "info")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if st.button("🎤 Start Recording", use_container_width=True, type="secondary"):
                st.info("🎙️ Voice recording requires audio input. Use the text box for now!")
        
        with col2:
            voice_query = st.text_area(
                "Type your question",
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
                with st.spinner("🔍 Processing your query..."):
                    query = st.session_state.voice_query
                    code = session_manager.get_uploaded_code()
                    
                    if code and "explanation_engine" in st.session_state:
                        try:
                            language = session_manager.get_language_preference()
                            explanation = st.session_state.explanation_engine.explain_code(
                                code=code,
                                language=language,
                                difficulty="intermediate"
                            )
                            
                            st.session_state.voice_query_result = {
                                "query": query,
                                "explanation": explanation
                            }
                            
                            info_box("Query processed successfully!", "success")
                            
                            with st.expander("Answer", expanded=True):
                                st.markdown(f"**Your Question:** {query}")
                                st.divider()
                                st.markdown(explanation.detailed_explanation if hasattr(explanation, 'detailed_explanation') else str(explanation))
                        
                        except Exception as e:
                            info_box(f"Failed to process query: {str(e)}", "error")
                    
                    elif not code:
                        info_box("Please upload code first to ask questions about it!", "warning")
                    else:
                        info_box("Explanation engine not available. Configure AWS credentials for AI-powered answers.", "info")
    
    # Analysis options
    spacing("lg")
    section_header("Analysis Options")
    
    col1, col2 = st.columns(2)
    with col1:
        enable_debugging = st.checkbox("Enable Debugging Analysis", value=True)
        generate_diagrams = st.checkbox("Generate Diagrams", value=True)
    
    with col2:
        difficulty_level = st.select_slider(
            "Explanation Difficulty",
            options=["Beginner", "Intermediate", "Advanced"],
            value="Intermediate"
        )
        generate_flashcards = st.checkbox("Generate Flashcards", value=True)
    
    # Analyze button
    spacing("lg")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Analyze Code", type="primary", use_container_width=True):
            _handle_analysis(session_manager, repo_url, app_config, generate_flashcards)


def _handle_analysis(session_manager, repo_url, app_config, generate_flashcards):
    """Handle code analysis."""
    if session_manager.get_uploaded_code():
        with st.spinner("🔍 Analyzing your code..."):
            if "code_analyzer" in st.session_state:
                code = session_manager.get_uploaded_code()
                filename = st.session_state.get("uploaded_filename", "code.py")
                language = session_manager.get_language_preference()
                
                try:
                    analysis = st.session_state.code_analyzer.analyze_file(
                        code=code,
                        filename=filename,
                        language=language
                    )
                    
                    st.session_state.current_analysis = analysis
                    
                    if generate_flashcards and "flashcard_manager" in st.session_state:
                        flashcards = st.session_state.flashcard_manager.generate_flashcards(
                            code_analysis=analysis,
                            language=language
                        )
                        if flashcards:
                            st.success(f"✅ Analysis complete! Generated {len(flashcards)} flashcards.")
                        else:
                            st.success("✅ Analysis complete! View results in the Explanations tab.")
                    else:
                        st.success("✅ Analysis complete! View results in the Explanations tab.")
                    
                except Exception as e:
                    st.error(f"❌ Analysis failed: {str(e)}")
                    st.info("💡 Showing mock data instead. Configure AWS credentials for real analysis.")
            else:
                st.info("💡 Showing mock data. Configure AWS credentials for real AI analysis.")
            
            st.session_state.current_page = "Explanations"
            st.rerun()
    
    elif repo_url and repo_url.startswith("https://github.com/"):
        with st.spinner("🔍 Cloning and analyzing repository..."):
            if "repo_analyzer" in st.session_state:
                try:
                    repo_analysis = st.session_state.repo_analyzer.analyze_repo(
                        repo_url=repo_url,
                        max_size_mb=app_config.max_repo_size_mb
                    )
                    
                    if repo_analysis:
                        st.session_state.current_repo_analysis = repo_analysis
                        st.success("✅ Repository analysis complete!")
                        st.session_state.current_page = "Explanations"
                        st.rerun()
                    else:
                        st.error("❌ Failed to analyze repository. Please check the URL and try again.")
                
                except Exception as e:
                    st.error(f"❌ Repository analysis failed: {str(e)}")
            else:
                st.error("❌ Repository analyzer not initialized.")
    
    else:
        st.warning("⚠️ Please upload a file or enter a valid GitHub repository URL first.")


def _detect_language(filename: str) -> str:
    """Detect programming language from filename."""
    ext_map = {
        ".py": "python",
        ".js": "javascript",
        ".jsx": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".java": "java",
        ".cpp": "cpp",
        ".c": "c",
        ".go": "go",
        ".rb": "ruby"
    }
    
    for ext, lang in ext_map.items():
        if filename.endswith(ext):
            return lang
    
    return "text"
