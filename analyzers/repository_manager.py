"""
Repository Manager for handling repository uploads and validation.

This module manages repository uploads via GitHub URL, ZIP file, or folder selection,
validates repository contents, and integrates with RepoAnalyzer.
"""

import logging
import os
import zipfile
import tempfile
import shutil
from typing import List, Tuple, Optional
from models.intent_models import UploadResult

logger = logging.getLogger(__name__)


class RepositoryManager:
    """Handles repository upload, validation, and storage."""
    
    # Supported programming language extensions
    SUPPORTED_EXTENSIONS = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.jsx': 'JavaScript',
        '.ts': 'TypeScript',
        '.tsx': 'TypeScript',
        '.java': 'Java',
        '.cpp': 'C++',
        '.cc': 'C++',
        '.cxx': 'C++',
        '.go': 'Go',
        '.rb': 'Ruby'
    }
    
    def __init__(self, repo_analyzer, max_size_mb: int = 100):
        """
        Initialize with repo analyzer and size limit.
        
        Args:
            repo_analyzer: RepoAnalyzer instance
            max_size_mb: Maximum repository size in megabytes
        """
        self.repo_analyzer = repo_analyzer
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.max_size_mb = max_size_mb
    
    def upload_from_github(self, github_url: str) -> UploadResult:
        """
        Upload repository from GitHub URL.
        
        Args:
            github_url: GitHub repository URL
            
        Returns:
            UploadResult with success status and analysis
        """
        try:
            logger.info(f"Uploading from GitHub: {github_url}")
            
            # Validate URL format
            if not self._validate_github_url(github_url):
                return UploadResult(
                    success=False,
                    error_message="Invalid GitHub URL format. Expected: https://github.com/user/repo"
                )
            
            # Clone repository using RepoAnalyzer
            repo_path = self.repo_analyzer.clone_repo(github_url)
            
            if not repo_path:
                return UploadResult(
                    success=False,
                    error_message="Failed to clone repository. Check URL and network connection."
                )
            
            # Validate repository
            is_valid, warnings = self.validate_repository(repo_path)
            
            if not is_valid:
                return UploadResult(
                    success=False,
                    repo_path=repo_path,
                    error_message="Repository validation failed: " + "; ".join(warnings)
                )
            
            # Analyze repository
            repo_analysis = self.repo_analyzer.analyze_repo(github_url)
            
            logger.info(f"Successfully uploaded from GitHub: {repo_path}")
            
            return UploadResult(
                success=True,
                repo_path=repo_path,
                repo_analysis=repo_analysis,
                validation_warnings=warnings
            )
        
        except Exception as e:
            logger.error(f"GitHub upload failed: {e}")
            return UploadResult(
                success=False,
                error_message=f"Upload failed: {str(e)}"
            )
    
    def upload_from_zip(self, zip_file) -> UploadResult:
        """
        Upload repository from ZIP file.
        
        Args:
            zip_file: File-like object or path to ZIP file
            
        Returns:
            UploadResult with success status and analysis
        """
        try:
            logger.info("Uploading from ZIP file")
            
            # Create temporary directory for extraction
            temp_dir = tempfile.mkdtemp(prefix="repo_upload_")
            
            # Extract ZIP file
            if hasattr(zip_file, 'read'):
                # File-like object (from Streamlit upload)
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
            else:
                # File path
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
            
            # Check size
            total_size = self._get_directory_size(temp_dir)
            if total_size > self.max_size_bytes:
                shutil.rmtree(temp_dir)
                return UploadResult(
                    success=False,
                    error_message=f"Repository too large: {total_size / (1024*1024):.1f}MB exceeds {self.max_size_mb}MB limit"
                )
            
            # Validate repository
            is_valid, warnings = self.validate_repository(temp_dir)
            
            if not is_valid:
                shutil.rmtree(temp_dir)
                return UploadResult(
                    success=False,
                    error_message="Repository validation failed: " + "; ".join(warnings)
                )
            
            # Analyze repository
            repo_analysis = self.repo_analyzer.analyze_repo(temp_dir)
            
            logger.info(f"Successfully uploaded from ZIP: {temp_dir}")
            
            return UploadResult(
                success=True,
                repo_path=temp_dir,
                repo_analysis=repo_analysis,
                validation_warnings=warnings
            )
        
        except zipfile.BadZipFile:
            return UploadResult(
                success=False,
                error_message="Invalid or corrupted ZIP file"
            )
        except Exception as e:
            logger.error(f"ZIP upload failed: {e}")
            return UploadResult(
                success=False,
                error_message=f"Upload failed: {str(e)}"
            )
    
    def upload_from_folder(self, folder_path: str) -> UploadResult:
        """
        Upload repository from local folder.
        
        Args:
            folder_path: Path to local folder
            
        Returns:
            UploadResult with success status and analysis
        """
        try:
            logger.info(f"Uploading from folder: {folder_path}")
            
            # Check if folder exists
            if not os.path.exists(folder_path):
                return UploadResult(
                    success=False,
                    error_message=f"Folder does not exist: {folder_path}"
                )
            
            if not os.path.isdir(folder_path):
                return UploadResult(
                    success=False,
                    error_message=f"Path is not a directory: {folder_path}"
                )
            
            # Check size
            total_size = self._get_directory_size(folder_path)
            if total_size > self.max_size_bytes:
                return UploadResult(
                    success=False,
                    error_message=f"Repository too large: {total_size / (1024*1024):.1f}MB exceeds {self.max_size_mb}MB limit"
                )
            
            # Validate repository
            is_valid, warnings = self.validate_repository(folder_path)
            
            if not is_valid:
                return UploadResult(
                    success=False,
                    error_message="Repository validation failed: " + "; ".join(warnings)
                )
            
            # Analyze repository
            repo_analysis = self.repo_analyzer.analyze_repo(folder_path)
            
            logger.info(f"Successfully uploaded from folder: {folder_path}")
            
            return UploadResult(
                success=True,
                repo_path=folder_path,
                repo_analysis=repo_analysis,
                validation_warnings=warnings
            )
        
        except Exception as e:
            logger.error(f"Folder upload failed: {e}")
            return UploadResult(
                success=False,
                error_message=f"Upload failed: {str(e)}"
            )
    
    def validate_repository(self, repo_path: str) -> Tuple[bool, List[str]]:
        """
        Validate repository contains code files.
        
        Args:
            repo_path: Path to repository
            
        Returns:
            Tuple of (is_valid, list_of_warnings)
        """
        warnings = []
        
        try:
            # Check if path exists
            if not os.path.exists(repo_path):
                return False, ["Repository path does not exist"]
            
            # Find code files
            code_files = []
            for root, dirs, files in os.walk(repo_path):
                # Skip common excluded directories
                dirs[:] = [d for d in dirs if d not in {
                    'node_modules', 'venv', 'env', '.git', '__pycache__',
                    'dist', 'build', '.idea', '.vscode'
                }]
                
                for file in files:
                    ext = os.path.splitext(file)[1]
                    if ext in self.SUPPORTED_EXTENSIONS:
                        code_files.append(os.path.join(root, file))
            
            # Check if any code files found
            if not code_files:
                return False, [
                    f"No supported code files found. Supported languages: {', '.join(set(self.SUPPORTED_EXTENSIONS.values()))}"
                ]
            
            # Add informational warnings
            if len(code_files) < 3:
                warnings.append(f"Only {len(code_files)} code files found. Analysis may be limited.")
            
            logger.info(f"Validated repository: {len(code_files)} code files found")
            return True, warnings
        
        except Exception as e:
            logger.error(f"Repository validation failed: {e}")
            return False, [f"Validation error: {str(e)}"]
    
    def get_supported_languages(self) -> List[str]:
        """
        Get list of supported programming languages.
        
        Returns:
            List of language names
        """
        return sorted(set(self.SUPPORTED_EXTENSIONS.values()))
    
    # ========================================================================
    # Private Helper Methods
    # ========================================================================
    
    def _validate_github_url(self, url: str) -> bool:
        """Validate GitHub URL format."""
        if not url:
            return False
        
        # Basic GitHub URL validation
        url_lower = url.lower()
        if 'github.com' not in url_lower:
            return False
        
        # Check for basic structure
        parts = url.split('/')
        if len(parts) < 5:  # https://github.com/user/repo
            return False
        
        return True
    
    def _get_directory_size(self, path: str) -> int:
        """Calculate total size of directory in bytes."""
        total_size = 0
        
        for root, dirs, files in os.walk(path):
            # Skip common large directories
            dirs[:] = [d for d in dirs if d not in {
                'node_modules', 'venv', 'env', '.git', '__pycache__',
                'dist', 'build'
            }]
            
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    total_size += os.path.getsize(file_path)
                except OSError:
                    continue
        
        return total_size
