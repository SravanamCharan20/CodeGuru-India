"""
Intent-Driven Analysis Orchestrator.

This module coordinates all components of the intent-driven repository analysis system.
"""

import logging
from typing import Dict, Any, Optional
from models.intent_models import UserIntent, SelectionResult, MultiFileAnalysis

logger = logging.getLogger(__name__)


class IntentDrivenOrchestrator:
    """Orchestrates the complete intent-driven analysis workflow."""
    
    def __init__(
        self,
        repository_manager,
        intent_interpreter,
        file_selector,
        multi_file_analyzer,
        learning_artifact_generator,
        traceability_manager,
        session_manager
    ):
        """
        Initialize orchestrator with all required components.
        
        Args:
            repository_manager: RepositoryManager instance
            intent_interpreter: IntentInterpreter instance
            file_selector: FileSelector instance
            multi_file_analyzer: MultiFileAnalyzer instance
            learning_artifact_generator: LearningArtifactGenerator instance
            traceability_manager: TraceabilityManager instance
            session_manager: SessionManager instance
        """
        self.repo_manager = repository_manager
        self.intent_interpreter = intent_interpreter
        self.file_selector = file_selector
        self.multi_file_analyzer = multi_file_analyzer
        self.artifact_generator = learning_artifact_generator
        self.traceability_manager = traceability_manager
        self.session_manager = session_manager
    
    def analyze_repository_with_intent(
        self,
        repo_path: str,
        user_input: str,
        language: str = "english"
    ) -> Dict[str, Any]:
        """
        Complete workflow: interpret intent → select files → analyze → generate artifacts.
        
        Args:
            repo_path: Path to repository
            user_input: User's natural language learning goal
            language: Output language for artifacts
            
        Returns:
            Dictionary with all analysis results and artifacts
        """
        try:
            logger.info("Starting intent-driven analysis workflow")
            
            # Step 1: Get repository analysis
            repo_analysis = self.session_manager.get_current_repository()
            if not repo_analysis or repo_analysis.get('repo_path') != repo_path:
                logger.error("Repository not found in session")
                return {'error': 'Repository not loaded'}
            
            repo_context = repo_analysis.get('repo_analysis')
            
            # Step 2: Interpret user intent
            logger.info("Interpreting user intent")
            intent = self.intent_interpreter.interpret_intent(user_input, repo_context)
            self.session_manager.set_current_intent(intent)
            
            # Check if clarification needed
            if intent.confidence_score < 0.7:
                questions = self.intent_interpreter.generate_clarification_questions(intent)
                return {
                    'status': 'clarification_needed',
                    'intent': intent,
                    'questions': questions
                }
            
            # Step 3: Select relevant files
            logger.info("Selecting relevant files")
            selection_result = self.file_selector.select_files(intent, repo_context)
            self.session_manager.set_file_selection(selection_result)
            
            if not selection_result.selected_files:
                # No files matched - suggest alternatives
                suggestions = self.file_selector.suggest_alternative_intents(repo_context)
                return {
                    'status': 'no_files_found',
                    'intent': intent,
                    'suggestions': suggestions
                }
            
            # Step 4: Analyze selected files
            logger.info(f"Analyzing {len(selection_result.selected_files)} files")
            multi_file_analysis = self.multi_file_analyzer.analyze_files(
                selection_result.selected_files,
                repo_path,
                intent
            )
            self.session_manager.set_multi_file_analysis(multi_file_analysis)
            
            # Step 5: Generate learning artifacts
            logger.info("Generating learning artifacts")
            
            flashcards = self.artifact_generator.generate_flashcards(
                multi_file_analysis,
                intent,
                language
            )
            
            quiz = self.artifact_generator.generate_quiz(
                multi_file_analysis,
                intent,
                num_questions=10,
                language=language
            )
            
            learning_path = self.artifact_generator.generate_learning_path(
                multi_file_analysis,
                intent,
                language
            )
            
            concept_summary = self.artifact_generator.generate_concept_summary(
                multi_file_analysis,
                intent,
                language
            )
            
            # Step 6: Register artifacts with traceability
            logger.info("Registering artifacts for traceability")
            for flashcard in flashcards:
                self.traceability_manager.register_artifact(
                    flashcard.id,
                    'flashcard',
                    flashcard.code_evidence
                )
            
            for question in quiz.get('questions', []):
                self.traceability_manager.register_artifact(
                    question.id,
                    'quiz_question',
                    question.code_evidence
                )
            
            for step in learning_path.steps:
                self.traceability_manager.register_artifact(
                    step.step_id,
                    'learning_step',
                    step.code_evidence
                )
            
            # Step 7: Save artifacts to session
            self.session_manager.set_learning_artifacts(
                flashcards=flashcards,
                quizzes=[quiz],
                learning_paths=[learning_path],
                concept_summary=concept_summary
            )
            
            # Step 8: Add to analysis history
            self.session_manager.add_to_analysis_history(
                intent=intent.primary_intent,
                files_analyzed=[f.file_info.path for f in selection_result.selected_files],
                artifacts_generated=len(flashcards) + len(quiz.get('questions', [])) + len(learning_path.steps)
            )
            
            logger.info("Intent-driven analysis complete")
            
            return {
                'status': 'success',
                'intent': intent,
                'selection_result': selection_result,
                'multi_file_analysis': multi_file_analysis,
                'flashcards': flashcards,
                'quiz': quiz,
                'learning_path': learning_path,
                'concept_summary': concept_summary
            }
        
        except Exception as e:
            logger.error(f"Intent-driven analysis failed: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def refine_intent_and_reanalyze(
        self,
        clarification_responses: Dict[str, str],
        language: str = "english"
    ) -> Dict[str, Any]:
        """
        Refine intent based on clarifications and re-run analysis.
        
        Args:
            clarification_responses: User's answers to clarification questions
            language: Output language
            
        Returns:
            Analysis results
        """
        try:
            # Get current intent
            intent_data = self.session_manager.get_current_intent()
            if not intent_data:
                return {'error': 'No intent to refine'}
            
            current_intent = intent_data['intent']
            
            # Refine intent
            refined_intent = self.intent_interpreter.refine_intent(
                current_intent,
                clarification_responses
            )
            
            # Get repository info
            repo_data = self.session_manager.get_current_repository()
            if not repo_data:
                return {'error': 'No repository loaded'}
            
            # Re-run analysis with refined intent
            return self.analyze_repository_with_intent(
                repo_data['repo_path'],
                refined_intent.primary_intent,
                language
            )
        
        except Exception as e:
            logger.error(f"Intent refinement failed: {e}")
            return {'error': str(e)}
