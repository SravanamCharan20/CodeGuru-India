"""Repository analyzer for GitHub repositories."""
from dataclasses import dataclass
from typing import List, Dict, Optional
import os
import tempfile
import shutil
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class FileInfo:
    """Information about a file in the repository."""
    path: str
    name: str
    extension: str
    size_bytes: int
    lines: int


@dataclass
class RepoAnalysis:
    """Repository analysis result."""
    repo_url: str
    total_files: int
    total_lines: int
    total_size_bytes: int
    file_tree: Dict[str, List[FileInfo]]
    languages: Dict[str, int]  # Language -> line count
    main_files: List[FileInfo]
    summary: str


class RepoAnalyzer:
    """Analyzes GitHub repositories."""
    
    def __init__(self, code_analyzer=None):
        """
        Initialize repository analyzer.
        
        Args:
            code_analyzer: Optional CodeAnalyzer instance for file analysis
        """
        self.code_analyzer = code_analyzer
        self.supported_extensions = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.jsx': 'JavaScript',
            '.ts': 'TypeScript',
            '.tsx': 'TypeScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.go': 'Go',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.cs': 'C#',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.rs': 'Rust'
        }
    
    def analyze_repo(
        self,
        repo_url: str,
        max_size_mb: int = 100
    ) -> Optional[RepoAnalysis]:
        """
        Analyze a GitHub repository.
        
        Args:
            repo_url: GitHub repository URL
            max_size_mb: Maximum repository size in MB
            
        Returns:
            Repository analysis result or None if failed
        """
        try:
            # Validate URL
            if not self._validate_github_url(repo_url):
                logger.error(f"Invalid GitHub URL: {repo_url}")
                return None
            
            # Clone repository to temp directory
            temp_dir = self.clone_repo(repo_url)
            if not temp_dir:
                return None
            
            try:
                # Get file tree
                file_tree = self.get_file_tree(temp_dir)
                
                # Analyze files
                all_files = []
                for files in file_tree.values():
                    all_files.extend(files)
                
                # Calculate statistics
                total_files = len(all_files)
                total_lines = sum(f.lines for f in all_files)
                total_size_bytes = sum(f.size_bytes for f in all_files)
                
                # Check size limit
                total_size_mb = total_size_bytes / (1024 * 1024)
                if total_size_mb > max_size_mb:
                    logger.error(f"Repository too large: {total_size_mb:.2f}MB > {max_size_mb}MB")
                    return None
                
                # Count languages
                languages = self._count_languages(all_files)
                
                # Identify main files
                main_files = self._identify_main_files(all_files)
                
                # Generate summary
                summary = self._generate_summary(
                    repo_url, total_files, total_lines, 
                    total_size_mb, languages, main_files
                )
                
                return RepoAnalysis(
                    repo_url=repo_url,
                    total_files=total_files,
                    total_lines=total_lines,
                    total_size_bytes=total_size_bytes,
                    file_tree=file_tree,
                    languages=languages,
                    main_files=main_files,
                    summary=summary
                )
            
            finally:
                # Clean up temp directory
                if temp_dir and os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir, ignore_errors=True)
        
        except Exception as e:
            logger.error(f"Failed to analyze repository: {e}")
            return None
    
    def clone_repo(self, repo_url: str) -> Optional[str]:
        """
        Clone a GitHub repository to a temporary directory.
        
        Args:
            repo_url: GitHub repository URL
            
        Returns:
            Path to cloned repository or None if failed
        """
        try:
            # Try to import GitPython
            try:
                import git
            except ImportError:
                logger.warning("GitPython not installed, using mock clone")
                return self._mock_clone(repo_url)
            
            # Create temp directory
            temp_dir = tempfile.mkdtemp(prefix="codeguru_repo_")
            
            # Clone repository
            logger.info(f"Cloning repository: {repo_url}")
            git.Repo.clone_from(repo_url, temp_dir, depth=1)
            
            return temp_dir
        
        except Exception as e:
            logger.error(f"Failed to clone repository: {e}")
            return None
    
    def get_file_tree(self, repo_path: str) -> Dict[str, List[FileInfo]]:
        """
        Get file tree structure of repository.
        
        Args:
            repo_path: Path to repository
            
        Returns:
            Dictionary mapping directory paths to file lists
        """
        file_tree = {}
        
        try:
            repo_path_obj = Path(repo_path)
            
            # Walk through directory
            for root, dirs, files in os.walk(repo_path):
                # Skip hidden directories and common ignore patterns
                dirs[:] = [d for d in dirs if not d.startswith('.') 
                          and d not in ['node_modules', '__pycache__', 'venv', 'env', 'dist', 'build']]
                
                # Get relative path
                rel_root = os.path.relpath(root, repo_path)
                if rel_root == '.':
                    rel_root = 'root'
                
                file_infos = []
                for file in files:
                    # Skip hidden files
                    if file.startswith('.'):
                        continue
                    
                    file_path = os.path.join(root, file)
                    ext = os.path.splitext(file)[1].lower()
                    
                    # Only include supported code files
                    if ext in self.supported_extensions:
                        try:
                            size = os.path.getsize(file_path)
                            
                            # Count lines
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                lines = len(f.readlines())
                            
                            file_info = FileInfo(
                                path=os.path.relpath(file_path, repo_path),
                                name=file,
                                extension=ext,
                                size_bytes=size,
                                lines=lines
                            )
                            file_infos.append(file_info)
                        
                        except Exception as e:
                            logger.warning(f"Failed to process file {file_path}: {e}")
                            continue
                
                if file_infos:
                    file_tree[rel_root] = file_infos
            
            return file_tree
        
        except Exception as e:
            logger.error(f"Failed to get file tree: {e}")
            return {}
    
    def analyze_files(
        self,
        repo_path: str,
        file_infos: List[FileInfo]
    ) -> List[Dict]:
        """
        Analyze multiple files in repository.
        
        Args:
            repo_path: Path to repository
            file_infos: List of files to analyze
            
        Returns:
            List of analysis results
        """
        results = []
        
        if not self.code_analyzer:
            logger.warning("No code analyzer available")
            return results
        
        for file_info in file_infos[:10]:  # Limit to 10 files
            try:
                file_path = os.path.join(repo_path, file_info.path)
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    code = f.read()
                
                analysis = self.code_analyzer.analyze_file(
                    code=code,
                    filename=file_info.name,
                    language='english'
                )
                
                results.append({
                    'file': file_info.path,
                    'analysis': analysis
                })
            
            except Exception as e:
                logger.error(f"Failed to analyze file {file_info.path}: {e}")
                continue
        
        return results
    
    def _validate_github_url(self, url: str) -> bool:
        """Validate GitHub URL format."""
        return url.startswith('https://github.com/') and len(url.split('/')) >= 5
    
    def _count_languages(self, files: List[FileInfo]) -> Dict[str, int]:
        """Count lines of code by language."""
        languages = {}
        
        for file in files:
            lang = self.supported_extensions.get(file.extension, 'Other')
            languages[lang] = languages.get(lang, 0) + file.lines
        
        return dict(sorted(languages.items(), key=lambda x: x[1], reverse=True))
    
    def _identify_main_files(self, files: List[FileInfo]) -> List[FileInfo]:
        """Identify main/important files in repository."""
        main_files = []
        
        # Look for common entry point files
        important_names = [
            'main', 'index', 'app', 'server', 'client',
            '__init__', 'setup', 'config', 'settings'
        ]
        
        for file in files:
            name_without_ext = os.path.splitext(file.name)[0].lower()
            if name_without_ext in important_names:
                main_files.append(file)
        
        # Sort by size (larger files are often more important)
        main_files.sort(key=lambda f: f.lines, reverse=True)
        
        return main_files[:5]  # Return top 5
    
    def _generate_summary(
        self,
        repo_url: str,
        total_files: int,
        total_lines: int,
        total_size_mb: float,
        languages: Dict[str, int],
        main_files: List[FileInfo]
    ) -> str:
        """Generate repository summary."""
        summary_parts = [
            f"Repository: {repo_url}",
            f"Total Files: {total_files}",
            f"Total Lines: {total_lines:,}",
            f"Size: {total_size_mb:.2f} MB",
            "",
            "Languages:"
        ]
        
        for lang, lines in list(languages.items())[:5]:
            percentage = (lines / total_lines * 100) if total_lines > 0 else 0
            summary_parts.append(f"  - {lang}: {lines:,} lines ({percentage:.1f}%)")
        
        if main_files:
            summary_parts.append("")
            summary_parts.append("Main Files:")
            for file in main_files:
                summary_parts.append(f"  - {file.path} ({file.lines} lines)")
        
        return "\n".join(summary_parts)
    
    def _mock_clone(self, repo_url: str) -> Optional[str]:
        """Mock clone for when GitPython is not available."""
        logger.warning("Using mock repository data (GitPython not installed)")
        return None

