"""Code upload interface component."""
import streamlit as st
from config import load_config


def render_code_upload():
    """Render code upload interface."""
    st.title("📤 Upload Code for Analysis")
    
    _, app_config = load_config()
    session_manager = st.session_state.session_manager
    
    # Create tabs for different upload methods
    tab1, tab2, tab3 = st.tabs(["📁 File Upload", "🔗 GitHub Repository", "🎤 Voice Query"])
    
    with tab1:
        st.markdown("### Upload a Code File")
        st.caption(f"Supported formats: {', '.join(app_config.supported_extensions)}")
        st.caption(f"Max file size: {app_config.max_file_size_mb}MB")
        
        uploaded_file = st.file_uploader(
            "Choose a code file",
            type=[ext.replace(".", "") for ext in app_config.supported_extensions],
            help="Upload a code file to analyze"
        )
        
        if uploaded_file is not None:
            # Read file content
            file_content = uploaded_file.read().decode("utf-8")
            file_size_mb = len(file_content) / (1024 * 1024)
            
            # Display file info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("File Name", uploaded_file.name)
            with col2:
                st.metric("File Size", f"{file_size_mb:.2f} MB")
            with col3:
                st.metric("Lines", len(file_content.split('\n')))
            
            # Store in session
            session_manager.set_uploaded_code(file_content, uploaded_file.name)
            
            # Show code preview
            with st.expander("📄 Preview Code", expanded=False):
                st.code(file_content, language=_detect_language(uploaded_file.name))
    
    with tab2:
        st.markdown("### Analyze GitHub Repository")
        st.caption(f"Max repository size: {app_config.max_repo_size_mb}MB")
        
        repo_url = st.text_input(
            "GitHub Repository URL",
            placeholder="https://github.com/username/repository",
            help="Enter a public GitHub repository URL"
        )
        
        if repo_url:
            if repo_url.startswith("https://github.com/"):
                st.success(f"✅ Valid GitHub URL: {repo_url}")
            else:
                st.error("❌ Please enter a valid GitHub URL")
    
    with tab3:
        st.markdown("### Ask Questions with Voice")
        st.caption("Speak in English, Hindi, or Telugu")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("🎤 Start Recording", use_container_width=True):
                st.info("🎙️ Voice recording will be available soon!")
        with col2:
            st.text_input("Or type your question here", placeholder="What does this function do?")
    
    # Analysis options
    st.divider()
    st.markdown("### ⚙️ Analysis Options")
    
    col1, col2 = st.columns(2)
    with col1:
        enable_debugging = st.checkbox("🐛 Enable Debugging Analysis", value=True)
        generate_diagrams = st.checkbox("📊 Generate Diagrams", value=True)
    
    with col2:
        difficulty_level = st.select_slider(
            "Explanation Difficulty",
            options=["Beginner", "Intermediate", "Advanced"],
            value="Intermediate"
        )
        generate_flashcards = st.checkbox("🗂️ Generate Flashcards", value=True)
    
    # Analyze button
    st.divider()
    if st.button("🚀 Analyze Code", type="primary", use_container_width=True):
        if session_manager.get_uploaded_code() or repo_url:
            with st.spinner("🔍 Analyzing your code..."):
                # Get the analyzer from session state
                if "code_analyzer" in st.session_state:
                    code = session_manager.get_uploaded_code()
                    filename = st.session_state.get("uploaded_filename", "code.py")
                    language = session_manager.get_language_preference()
                    
                    try:
                        # Perform actual analysis
                        analysis = st.session_state.code_analyzer.analyze_file(
                            code=code,
                            filename=filename,
                            language=language
                        )
                        
                        # Store analysis in session
                        st.session_state.current_analysis = analysis
                        
                        # Generate flashcards if requested
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
        else:
            st.warning("⚠️ Please upload a file or enter a repository URL first.")


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
