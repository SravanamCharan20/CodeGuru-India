"""
Repository Upload UI Component.

Provides interface for uploading repositories via GitHub URL, ZIP file, or folder selection.
"""

import streamlit as st
import logging

logger = logging.getLogger(__name__)


def render_repository_upload(repository_manager, session_manager):
    """
    Render repository upload interface.
    
    Args:
        repository_manager: RepositoryManager instance
        session_manager: SessionManager instance
    """
    st.header("📦 Upload Repository")
    
    # Show supported languages
    supported_langs = repository_manager.get_supported_languages()
    st.info(f"**Supported Languages**: {', '.join(supported_langs)}")
    st.caption(f"**Maximum Size**: {repository_manager.max_size_mb}MB")
    
    # Create tabs for different upload methods
    tab1, tab2, tab3 = st.tabs(["GitHub URL", "ZIP File", "Local Folder"])
    
    # Tab 1: GitHub URL
    with tab1:
        st.subheader("Upload from GitHub")
        github_url = st.text_input(
            "GitHub Repository URL",
            placeholder="https://github.com/username/repository",
            help="Enter the full GitHub repository URL"
        )
        
        if st.button("Upload from GitHub", key="github_upload"):
            if not github_url:
                st.error("Please enter a GitHub URL")
            else:
                with st.spinner("Cloning repository..."):
                    result = repository_manager.upload_from_github(github_url)
                    _handle_upload_result(result, session_manager)
    
    # Tab 2: ZIP File
    with tab2:
        st.subheader("Upload ZIP File")
        uploaded_file = st.file_uploader(
            "Choose a ZIP file",
            type=['zip'],
            help="Upload a ZIP file containing your code repository"
        )
        
        if uploaded_file is not None:
            if st.button("Upload ZIP", key="zip_upload"):
                with st.spinner("Extracting and validating..."):
                    result = repository_manager.upload_from_zip(uploaded_file)
                    _handle_upload_result(result, session_manager)
    
    # Tab 3: Local Folder
    with tab3:
        st.subheader("Upload Local Folder")
        folder_path = st.text_input(
            "Folder Path",
            placeholder="/path/to/your/repository",
            help="Enter the full path to your local repository folder"
        )
        
        if st.button("Upload Folder", key="folder_upload"):
            if not folder_path:
                st.error("Please enter a folder path")
            else:
                with st.spinner("Validating repository..."):
                    result = repository_manager.upload_from_folder(folder_path)
                    _handle_upload_result(result, session_manager)
    
    # Show current repository if loaded
    current_repo = session_manager.get_current_repository()
    if current_repo:
        st.divider()
        st.success("✅ Repository Loaded")
        
        with st.expander("Repository Details", expanded=False):
            st.write(f"**Path**: `{current_repo['repo_path']}`")
            st.write(f"**Uploaded**: {current_repo['upload_timestamp']}")
            
            repo_analysis = current_repo.get('repo_analysis')
            if repo_analysis:
                if hasattr(repo_analysis, 'total_files'):
                    st.write(f"**Total Files**: {repo_analysis.total_files}")
                if hasattr(repo_analysis, 'languages'):
                    st.write("**Languages**:")
                    for lang, pct in repo_analysis.languages.items():
                        st.write(f"  - {lang}: {pct}%")


def _handle_upload_result(result, session_manager):
    """Handle upload result and display appropriate messages."""
    if result.success:
        # Save to session
        session_manager.set_current_repository(
            result.repo_path,
            result.repo_analysis
        )
        
        st.success("✅ Repository uploaded successfully!")
        
        # Show warnings if any
        if result.validation_warnings:
            with st.expander("⚠️ Warnings", expanded=False):
                for warning in result.validation_warnings:
                    st.warning(warning)
        
        # Show repository info
        if result.repo_analysis:
            st.write("**Repository Summary**:")
            if hasattr(result.repo_analysis, 'total_files'):
                st.write(f"- Files: {result.repo_analysis.total_files}")
            if hasattr(result.repo_analysis, 'languages'):
                langs = ', '.join([f"{k} ({v}%)" for k, v in result.repo_analysis.languages.items()])
                st.write(f"- Languages: {langs}")
        
        st.info("👉 Proceed to the next step to analyze your repository")
    
    else:
        st.error(f"❌ Upload failed: {result.error_message}")
        
        # Provide helpful suggestions
        if "Invalid GitHub URL" in result.error_message:
            st.info("💡 Make sure the URL is in format: https://github.com/username/repository")
        elif "too large" in result.error_message:
            st.info("💡 Try uploading a smaller repository or specific folders")
        elif "No supported code files" in result.error_message:
            st.info(f"💡 Supported languages: {', '.join(repository_manager.get_supported_languages())}")
