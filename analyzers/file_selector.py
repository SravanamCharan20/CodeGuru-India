"""
File Selector for identifying relevant files based on user intent.

This module calculates relevance scores for files and selects those most
relevant to the user's learning goals.
"""

import logging
import os
import re
from typing import List, Set
from models.intent_models import UserIntent, FileSelection, SelectionResult

logger = logging.getLogger(__name__)


class FileSelector:
    """Identifies and ranks files relevant to user's intent."""
    
    # Files and folders to exclude by default
    EXCLUDE_PATTERNS = {
        # Dependency folders
        'node_modules', 'venv', 'env', '.env', 'virtualenv',
        '__pycache__', '.pytest_cache', '.mypy_cache',
        'vendor', 'packages', 'bower_components',
        
        # Build artifacts
        'dist', 'build', 'out', 'target', 'bin', 'obj',
        '.next', '.nuxt', '.output',
        
        # Config and meta
        '.git', '.svn', '.hg',
        '.idea', '.vscode', '.vs',
        
        # Compiled/generated
        '*.pyc', '*.pyo', '*.class', '*.o', '*.so', '*.dll',
        '*.min.js', '*.min.css',
        
        # Logs and temp
        'logs', 'tmp', 'temp', 'cache',
        '*.log', '*.tmp'
    }
    
    # Configuration file extensions
    CONFIG_EXTENSIONS = {
        '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg',
        '.conf', '.config', '.xml', '.properties'
    }
    
    # Relevance score threshold
    RELEVANCE_THRESHOLD = 0.3
    
    def __init__(self, langchain_orchestrator):
        """
        Initialize with AI orchestrator for semantic analysis.
        
        Args:
            langchain_orchestrator: LangChainOrchestrator for AI-powered analysis
        """
        self.orchestrator = langchain_orchestrator
    
    def select_files(
        self,
        intent: UserIntent,
        repo_analysis
    ) -> SelectionResult:
        """
        Select files relevant to user intent.
        
        Args:
            intent: UserIntent with learning goals
            repo_analysis: RepoAnalysis object with repository information
            
        Returns:
            SelectionResult with selected files and metadata
        """
        try:
            logger.info(f"Selecting files for intent: {intent.primary_intent}")
            
            # Get all files from repository
            all_files = self._get_all_files(repo_analysis)
            total_scanned = len(all_files)
            
            # Filter out excluded files
            filtered_files = self._filter_excluded_files(all_files, intent)
            excluded_count = total_scanned - len(filtered_files)
            
            # Calculate relevance scores
            scored_files = []
            for file_info in filtered_files:
                score = self.calculate_relevance_score(file_info, intent, repo_analysis)
                
                if score >= self.RELEVANCE_THRESHOLD:
                    # Determine file role
                    role = self._determine_file_role(file_info, repo_analysis)
                    
                    # Generate selection reason
                    reason = self._generate_selection_reason(file_info, intent, score, role)
                    
                    selection = FileSelection(
                        file_info=file_info,
                        relevance_score=score,
                        selection_reason=reason,
                        priority=0,  # Will be set during prioritization
                        file_role=role
                    )
                    scored_files.append(selection)
            
            # Prioritize files
            prioritized_files = self._prioritize_files(scored_files)
            
            # Generate summary
            summary = self._generate_selection_summary(
                prioritized_files,
                excluded_count,
                total_scanned,
                intent
            )
            
            logger.info(f"Selected {len(prioritized_files)} files out of {total_scanned}")
            
            return SelectionResult(
                selected_files=prioritized_files,
                excluded_count=excluded_count,
                total_scanned=total_scanned,
                selection_summary=summary
            )
        
        except Exception as e:
            logger.error(f"File selection failed: {e}")
            return SelectionResult(
                selected_files=[],
                excluded_count=0,
                total_scanned=0,
                selection_summary=f"File selection failed: {str(e)}"
            )
    
    def calculate_relevance_score(
        self,
        file_info,
        intent: UserIntent,
        repo_context
    ) -> float:
        """
        Calculate how relevant a file is to the intent.
        
        Scoring algorithm:
        - File name matching (0-0.3)
        - Path matching (0-0.2)
        - Content analysis (0-0.3)
        - File importance (0-0.2)
        
        Args:
            file_info: FileInfo object
            intent: UserIntent
            repo_context: RepoAnalysis
            
        Returns:
            Relevance score between 0.0 and 1.0
        """
        score = 0.0
        
        try:
            # 1. File name matching (0-0.3)
            name_score = self._calculate_name_score(file_info, intent)
            score += name_score * 0.3
            
            # 2. Path matching (0-0.2)
            path_score = self._calculate_path_score(file_info, intent)
            score += path_score * 0.2
            
            # 3. Content analysis (0-0.3) - simplified for now
            content_score = self._calculate_content_score(file_info, intent)
            score += content_score * 0.3
            
            # 4. File importance (0-0.2)
            importance_score = self._calculate_importance_score(file_info, repo_context)
            score += importance_score * 0.2
            
            # Ensure score is in valid range
            score = max(0.0, min(1.0, score))
            
        except Exception as e:
            logger.warning(f"Error calculating relevance for {file_info.name}: {e}")
            score = 0.0
        
        return score
    
    def explain_selection(self, file_selection: FileSelection, intent: UserIntent) -> str:
        """
        Generate human-readable explanation for why file was selected.
        
        Args:
            file_selection: FileSelection object
            intent: UserIntent
            
        Returns:
            Explanation string
        """
        return file_selection.selection_reason
    
    def suggest_alternative_intents(self, repo_analysis) -> List[str]:
        """
        Suggest alternative intents when no files match.
        
        Args:
            repo_analysis: RepoAnalysis object
            
        Returns:
            List of suggested intent descriptions
        """
        suggestions = []
        
        try:
            # Analyze repository structure
            if hasattr(repo_analysis, 'languages') and repo_analysis.languages:
                main_lang = max(repo_analysis.languages.items(), key=lambda x: x[1])[0]
                suggestions.append(f"Learn {main_lang} programming patterns in this repository")
            
            if hasattr(repo_analysis, 'frameworks') and repo_analysis.frameworks:
                for framework in repo_analysis.frameworks[:2]:
                    suggestions.append(f"Understand how {framework} is used")
            
            # Generic suggestions
            suggestions.extend([
                "Study the overall code structure and organization",
                "Learn the main features and functionality",
                "Understand the architecture and design patterns"
            ])
        
        except Exception as e:
            logger.error(f"Failed to suggest alternatives: {e}")
            suggestions = [
                "Try broadening your search to the entire repository",
                "Focus on a specific technology or framework",
                "Look for specific features or functionality"
            ]
        
        return suggestions[:5]  # Return top 5
    
    # ========================================================================
    # Private Helper Methods
    # ========================================================================
    
    def _get_all_files(self, repo_analysis) -> List:
        """Extract all files from repository analysis."""
        files = []
        
        if hasattr(repo_analysis, 'file_tree') and repo_analysis.file_tree:
            files = self._extract_files_from_tree(repo_analysis.file_tree)
        elif hasattr(repo_analysis, 'files') and repo_analysis.files:
            files = repo_analysis.files
        
        return files
    
    def _extract_files_from_tree(self, tree, current_path="") -> List:
        """Recursively extract files from file tree."""
        files = []
        
        if isinstance(tree, dict):
            for name, subtree in tree.items():
                path = os.path.join(current_path, name) if current_path else name
                
                if isinstance(subtree, dict):
                    # It's a directory
                    files.extend(self._extract_files_from_tree(subtree, path))
                else:
                    # It's a file - create a simple file info object
                    files.append(type('FileInfo', (), {
                        'name': name,
                        'path': path,
                        'extension': os.path.splitext(name)[1],
                        'size_bytes': 0,
                        'lines': 0
                    })())
        
        return files
    
    def _filter_excluded_files(self, files: List, intent: UserIntent) -> List:
        """Filter out configuration files, build artifacts, and dependencies."""
        filtered = []
        
        for file_info in files:
            # Check if explicitly requested
            if intent.scope and intent.scope.scope_type == "specific_files":
                if file_info.path in intent.scope.target_paths:
                    filtered.append(file_info)
                    continue
            
            # Check exclude patterns
            if self._should_exclude(file_info, intent):
                continue
            
            filtered.append(file_info)
        
        return filtered
    
    def _should_exclude(self, file_info, intent: UserIntent) -> bool:
        """Check if file should be excluded."""
        path = file_info.path
        name = file_info.name
        
        # Check explicit exclusions
        if intent.scope and path in intent.scope.exclude_paths:
            return True
        
        # Check if in excluded folder
        path_parts = path.split(os.sep)
        for part in path_parts:
            if part in self.EXCLUDE_PATTERNS:
                return True
        
        # Check file extension for config files (unless explicitly requested)
        ext = os.path.splitext(name)[1]
        if ext in self.CONFIG_EXTENSIONS:
            # Only exclude if not specifically looking for config
            if "config" not in intent.primary_intent.lower():
                return True
        
        return False
    
    def _calculate_name_score(self, file_info, intent: UserIntent) -> float:
        """Calculate score based on file name matching."""
        score = 0.0
        name_lower = file_info.name.lower()
        
        # Check technologies
        for tech in intent.technologies:
            if tech.lower() in name_lower:
                score += 0.5
        
        # Check intent keywords
        intent_keywords = self._extract_keywords_from_intent(intent)
        for keyword in intent_keywords:
            if keyword in name_lower:
                score += 0.3
        
        return min(score, 1.0)
    
    def _calculate_path_score(self, file_info, intent: UserIntent) -> float:
        """Calculate score based on path matching."""
        score = 0.0
        path_lower = file_info.path.lower()
        
        # Check if in target paths
        if intent.scope and intent.scope.target_paths:
            for target in intent.scope.target_paths:
                if target.lower() in path_lower:
                    score += 0.8
        
        # Check for relevant path components
        intent_keywords = self._extract_keywords_from_intent(intent)
        for keyword in intent_keywords:
            if keyword in path_lower:
                score += 0.2
        
        return min(score, 1.0)
    
    def _calculate_content_score(self, file_info, intent: UserIntent) -> float:
        """Calculate score based on file content (simplified)."""
        # For now, use file extension as proxy for content
        score = 0.0
        ext = file_info.extension if hasattr(file_info, 'extension') else ""
        
        # Check if extension matches technologies
        for tech in intent.technologies:
            tech_lower = tech.lower()
            if tech_lower in ['python', 'py'] and ext == '.py':
                score += 0.5
            elif tech_lower in ['javascript', 'js'] and ext in ['.js', '.jsx']:
                score += 0.5
            elif tech_lower in ['typescript', 'ts'] and ext in ['.ts', '.tsx']:
                score += 0.5
            elif tech_lower == 'java' and ext == '.java':
                score += 0.5
        
        # Boost for common important files
        if file_info.name in ['main.py', 'app.py', 'index.js', 'main.js', 'App.jsx']:
            score += 0.3
        
        return min(score, 1.0)
    
    def _calculate_importance_score(self, file_info, repo_context) -> float:
        """Calculate file importance score."""
        score = 0.0
        
        # Check if it's a main file
        if hasattr(repo_context, 'main_files') and repo_context.main_files:
            main_file_names = [f.name for f in repo_context.main_files]
            if file_info.name in main_file_names:
                score += 0.7
        
        # Boost for entry point patterns
        entry_patterns = ['main', 'app', 'index', 'server', 'client']
        name_lower = file_info.name.lower()
        for pattern in entry_patterns:
            if pattern in name_lower:
                score += 0.3
                break
        
        return min(score, 1.0)
    
    def _determine_file_role(self, file_info, repo_context) -> str:
        """Determine the role of a file."""
        name_lower = file_info.name.lower()
        path_lower = file_info.path.lower()
        
        # Entry points
        if any(pattern in name_lower for pattern in ['main', 'app', 'index', 'server']):
            return "entry_point"
        
        # Models
        if 'model' in path_lower or 'models' in path_lower:
            return "model"
        
        # Views/UI
        if any(term in path_lower for term in ['view', 'views', 'ui', 'component', 'components']):
            return "view"
        
        # Controllers
        if any(term in path_lower for term in ['controller', 'controllers', 'handler', 'handlers']):
            return "controller"
        
        # Utilities
        if any(term in path_lower for term in ['util', 'utils', 'helper', 'helpers', 'lib']):
            return "utility"
        
        # Default to core logic
        return "core_logic"
    
    def _generate_selection_reason(
        self,
        file_info,
        intent: UserIntent,
        score: float,
        role: str
    ) -> str:
        """Generate explanation for why file was selected."""
        reasons = []
        
        # Role-based reason
        role_descriptions = {
            "entry_point": "Entry point for the application",
            "core_logic": "Contains core business logic",
            "model": "Defines data models and structures",
            "view": "Handles UI and presentation",
            "controller": "Manages request handling and flow",
            "utility": "Provides utility functions and helpers"
        }
        reasons.append(role_descriptions.get(role, "Contains relevant code"))
        
        # Technology match
        for tech in intent.technologies:
            if tech.lower() in file_info.name.lower() or tech.lower() in file_info.path.lower():
                reasons.append(f"Related to {tech}")
                break
        
        # Intent match
        intent_keywords = self._extract_keywords_from_intent(intent)
        for keyword in intent_keywords:
            if keyword in file_info.name.lower():
                reasons.append(f"Matches '{keyword}' from your goal")
                break
        
        return "; ".join(reasons)
    
    def _prioritize_files(self, files: List[FileSelection]) -> List[FileSelection]:
        """Prioritize files by relevance and role."""
        # Sort by relevance score (descending) and role importance
        role_priority = {
            "entry_point": 1,
            "core_logic": 2,
            "controller": 3,
            "model": 4,
            "view": 5,
            "utility": 6
        }
        
        sorted_files = sorted(
            files,
            key=lambda f: (-f.relevance_score, role_priority.get(f.file_role, 99))
        )
        
        # Assign priority numbers
        for i, file_sel in enumerate(sorted_files, 1):
            file_sel.priority = i
        
        return sorted_files
    
    def _generate_selection_summary(
        self,
        selected_files: List[FileSelection],
        excluded_count: int,
        total_scanned: int,
        intent: UserIntent
    ) -> str:
        """Generate summary of file selection."""
        if not selected_files:
            return f"No files matched your intent '{intent.primary_intent}'. " \
                   f"Scanned {total_scanned} files, excluded {excluded_count}. " \
                   f"Try broadening your search or focusing on different aspects."
        
        summary_parts = [
            f"Selected {len(selected_files)} files out of {total_scanned} scanned",
            f"({excluded_count} excluded as config/build artifacts)"
        ]
        
        # Add role breakdown
        role_counts = {}
        for f in selected_files:
            role_counts[f.file_role] = role_counts.get(f.file_role, 0) + 1
        
        if role_counts:
            role_summary = ", ".join([f"{count} {role}" for role, count in role_counts.items()])
            summary_parts.append(f"Includes: {role_summary}")
        
        return ". ".join(summary_parts)
    
    def _extract_keywords_from_intent(self, intent: UserIntent) -> Set[str]:
        """Extract keywords from intent for matching."""
        keywords = set()
        
        # Extract from primary intent
        if intent.primary_intent:
            # Convert snake_case to words
            words = intent.primary_intent.replace('_', ' ').split()
            keywords.update(w.lower() for w in words)
        
        # Extract from technologies
        keywords.update(t.lower() for t in intent.technologies)
        
        # Extract from secondary intents
        for secondary in intent.secondary_intents:
            words = secondary.replace('_', ' ').split()
            keywords.update(w.lower() for w in words)
        
        return keywords
