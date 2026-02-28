"""
Unified Code Analyzer.

Consolidates single-file and multi-file analysis capabilities with intelligent mode selection.
"""

import logging
from typing import Dict, Any, Optional, List
from models.intent_models import UserIntent

logger = logging.getLogger(__name__)


class UnifiedAnalyzer:
    """Unified analyzer that handles both quick and deep analysis modes."""
    
    def __init__(
        self,
        code_analyzer,
        repository_manager,
        intent_interpreter,
        file_selector,
        multi_file_analyzer,
        learning_artifact_generator,
        session_manager
    ):
        """
        Initialize unified analyzer with all components.
        
        Args:
            code_analyzer: CodeAnalyzer for single file analysis
            repository_manager: RepositoryManager for repo handling
            intent_interpreter: IntentInterpreter for goal parsing
            file_selector: FileSelector for relevant file identification
            multi_file_analyzer: MultiFileAnalyzer for multi-file analysis
            learning_artifact_generator: Generator for learning materials
            session_manager: SessionManager for state management
        """
        self.code_analyzer = code_analyzer
        self.repo_manager = repository_manager
        self.intent_interpreter = intent_interpreter
        self.file_selector = file_selector
        self.multi_file_analyzer = multi_file_analyzer
        self.artifact_generator = learning_artifact_generator
        self.session_manager = session_manager
    
    def analyze(
        self,
        mode: str,
        content: Any,
        user_intent: Optional[str] = None,
        language: str = "english"
    ) -> Dict[str, Any]:
        """
        Unified analysis entry point.
        
        Args:
            mode: 'quick' for single file, 'deep' for multi-file with intent
            content: File content (str) or repository path (str)
            user_intent: Optional learning goal for deep mode
            language: Output language for artifacts
            
        Returns:
            Analysis results dictionary
        """
        try:
            if mode == 'quick':
                return self._quick_analysis(content)
            elif mode == 'deep':
                if not user_intent:
                    return {'error': 'Deep mode requires user intent'}
                return self._deep_analysis(content, user_intent, language)
            else:
                return {'error': f'Invalid mode: {mode}'}
        
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return {'error': str(e)}
    
    def _quick_analysis(self, file_content: str) -> Dict[str, Any]:
        """
        Quick single-file analysis.
        
        Args:
            file_content: Code content as string
            
        Returns:
            Analysis results with explanation and structure
        """
        try:
            logger.info("Running quick analysis")
            
            # Analyze file
            analysis = self.code_analyzer.analyze_file(file_content)
            
            # Generate basic explanation
            explanation = self._generate_quick_explanation(analysis)
            
            return {
                'mode': 'quick',
                'analysis': analysis,
                'explanation': explanation,
                'success': True
            }
        
        except Exception as e:
            logger.error(f"Quick analysis failed: {e}")
            return {'error': str(e), 'success': False}
    
    def _deep_analysis(
        self,
        repo_path: str,
        user_intent: str,
        language: str
    ) -> Dict[str, Any]:
        """
        Deep intent-driven multi-file analysis.
        
        Args:
            repo_path: Path to repository
            user_intent: User's learning goal
            language: Output language
            
        Returns:
            Comprehensive analysis with learning artifacts
        """
        try:
            logger.info("Running deep analysis")
            
            # Get repository context
            repo_analysis = self.session_manager.get_current_repository()
            if not repo_analysis:
                return {'error': 'Repository not found', 'success': False}
            
            repo_context = repo_analysis.get('repo_analysis')
            
            # Step 1: Interpret intent
            logger.info("Interpreting user intent")
            intent = self.intent_interpreter.interpret_intent(user_intent, repo_context)
            
            # Check for clarification needs
            if intent.needs_clarification:
                return {
                    'needs_clarification': True,
                    'questions': intent.clarification_questions,
                    'success': False
                }
            
            # Step 2: Select relevant files
            logger.info("Selecting relevant files")
            selection_result = self.file_selector.select_files(intent, repo_context)
            
            if not selection_result.selected_files:
                return {
                    'error': 'No relevant files found',
                    'success': False
                }
            
            # Step 3: Analyze selected files
            logger.info(f"Analyzing {len(selection_result.selected_files)} files")
            multi_file_analysis = self.multi_file_analyzer.analyze_files(
                selection_result.selected_files,
                repo_path,
                intent
            )
            
            # Step 4: Generate learning artifacts
            logger.info("Generating learning artifacts")
            artifacts = self.artifact_generator.generate_artifacts(
                multi_file_analysis,
                intent,
                language
            )
            
            return {
                'mode': 'deep',
                'intent': intent,
                'selection': selection_result,
                'analysis': multi_file_analysis,
                'artifacts': artifacts,
                'success': True
            }
        
        except Exception as e:
            logger.error(f"Deep analysis failed: {e}")
            return {'error': str(e), 'success': False}
    
    def _generate_quick_explanation(self, analysis: Dict[str, Any]) -> str:
        """
        Generate quick explanation from analysis.
        
        Args:
            analysis: Code analysis results
            
        Returns:
            Human-readable explanation
        """
        explanation_parts = []
        
        # Overview
        if 'summary' in analysis:
            explanation_parts.append(f"## Overview\n{analysis['summary']}")
        
        # Structure
        if 'structure' in analysis:
            structure = analysis['structure']
            explanation_parts.append("\n## Code Structure")
            
            if 'classes' in structure:
                explanation_parts.append(f"- **Classes**: {len(structure['classes'])}")
            
            if 'functions' in structure:
                explanation_parts.append(f"- **Functions**: {len(structure['functions'])}")
            
            if 'imports' in structure:
                explanation_parts.append(f"- **Imports**: {len(structure['imports'])}")
        
        # Key concepts
        if 'concepts' in analysis:
            explanation_parts.append("\n## Key Concepts")
            for concept in analysis['concepts'][:5]:
                explanation_parts.append(f"- {concept}")
        
        return "\n".join(explanation_parts)
    
    def get_analysis_recommendations(
        self,
        content_type: str,
        content_size: int
    ) -> Dict[str, Any]:
        """
        Recommend analysis mode based on content.
        
        Args:
            content_type: 'file' or 'repository'
            content_size: Size in bytes or file count
            
        Returns:
            Recommendations dictionary
        """
        recommendations = {
            'suggested_mode': None,
            'reason': None,
            'alternatives': []
        }
        
        if content_type == 'file':
            if content_size < 1000:  # Small file
                recommendations['suggested_mode'] = 'quick'
                recommendations['reason'] = 'Small file - quick analysis is sufficient'
            else:
                recommendations['suggested_mode'] = 'quick'
                recommendations['reason'] = 'Single file - quick analysis recommended'
                recommendations['alternatives'].append({
                    'mode': 'deep',
                    'reason': 'Use deep mode if you want comprehensive learning artifacts'
                })
        
        elif content_type == 'repository':
            if content_size <= 5:  # Few files
                recommendations['suggested_mode'] = 'quick'
                recommendations['reason'] = 'Small repository - quick analysis may be sufficient'
                recommendations['alternatives'].append({
                    'mode': 'deep',
                    'reason': 'Use deep mode for relationship analysis'
                })
            else:
                recommendations['suggested_mode'] = 'deep'
                recommendations['reason'] = 'Large repository - deep analysis recommended for comprehensive understanding'
        
        return recommendations
