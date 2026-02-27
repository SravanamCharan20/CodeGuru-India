"""
Learning Artifact Generator for creating flashcards, quizzes, and learning paths.

This module generates learning materials from multi-file analysis with complete
code traceability.
"""

import logging
import uuid
import json
from typing import List, Dict, Any
from datetime import datetime, timedelta
from models.intent_models import (
    MultiFileAnalysis,
    UserIntent,
    CodeEvidence,
    CodeFlashcard,
    CodeQuestion,
    LearningStep,
    LearningPath
)

logger = logging.getLogger(__name__)


class LearningArtifactGenerator:
    """Generates flashcards, quizzes, and learning paths from multi-file analysis."""
    
    def __init__(
        self,
        flashcard_manager,
        quiz_engine,
        langchain_orchestrator
    ):
        """
        Initialize with existing learning components.
        
        Args:
            flashcard_manager: FlashcardManager instance
            quiz_engine: QuizEngine instance
            langchain_orchestrator: LangChainOrchestrator for AI generation
        """
        self.flashcard_manager = flashcard_manager
        self.quiz_engine = quiz_engine
        self.orchestrator = langchain_orchestrator
    
    def generate_flashcards(
        self,
        multi_file_analysis: MultiFileAnalysis,
        intent: UserIntent,
        language: str = "english"
    ) -> List[CodeFlashcard]:
        """
        Generate flashcards from multi-file analysis.
        
        Args:
            multi_file_analysis: MultiFileAnalysis with code analysis
            intent: User's learning intent
            language: Output language (english, hindi, telugu)
            
        Returns:
            List of CodeFlashcard objects
        """
        flashcards = []
        
        try:
            logger.info(f"Generating flashcards in {language} for {len(multi_file_analysis.key_concepts)} concepts")
            
            # Skip AI generation - it's unreliable with small models
            # Generate flashcards directly from key concepts
            for concept in multi_file_analysis.key_concepts[:20]:  # Limit to 20
                # Extract code evidence
                evidence_list = []
                if 'evidence' in concept and concept['evidence']:
                    for ev_dict in concept['evidence']:
                        evidence = CodeEvidence(
                            file_path=ev_dict.get('file_path', concept.get('file', '')),
                            line_start=ev_dict.get('line_start', concept.get('line', 1)),
                            line_end=ev_dict.get('line_end', concept.get('line', 1) + 5),
                            code_snippet="",  # Will be filled by traceability manager
                            context_description=ev_dict.get('context', concept.get('description', ''))
                        )
                        evidence_list.append(evidence)
                
                # Skip if no evidence
                if not evidence_list:
                    continue
                
                # Generate flashcard content based on category
                category = concept.get('category', 'general')
                name = concept.get('name', 'Unknown')
                description = concept.get('description', '')
                
                # Language-specific question templates
                if language == "hindi":
                    templates = {
                        'functions': f"फ़ंक्शन '{name}' क्या करता है?",
                        'classes': f"क्लास '{name}' का उद्देश्य क्या है?",
                        'patterns': f"'{name}' कौन सा डिज़ाइन पैटर्न है?",
                        'architecture': f"आर्किटेक्चरल अवधारणा समझाएं: {name}",
                        'default': f"{name} क्या है?"
                    }
                elif language == "telugu":
                    templates = {
                        'functions': f"ఫంక్షన్ '{name}' ఏమి చేస్తుంది?",
                        'classes': f"క్లాస్ '{name}' యొక్క ఉద్దేశ్యం ఏమిటి?",
                        'patterns': f"'{name}' ఏ డిజైన్ ప్యాటర్న్?",
                        'architecture': f"ఆర్కిటెక్చరల్ కాన్సెప్ట్ వివరించండి: {name}",
                        'default': f"{name} అంటే ఏమిటి?"
                    }
                else:  # English
                    templates = {
                        'functions': f"What does the function '{name}' do?",
                        'classes': f"What is the purpose of the class '{name}'?",
                        'patterns': f"What design pattern is '{name}'?",
                        'architecture': f"Explain the architectural concept: {name}",
                        'default': f"What is {name}?"
                    }
                
                front = templates.get(category, templates['default'])
                back = description
                
                flashcard = CodeFlashcard(
                    id=str(uuid.uuid4()),
                    front=front,
                    back=back,
                    topic=intent.primary_intent,
                    difficulty=intent.audience_level,
                    last_reviewed=None,
                    next_review=datetime.now() + timedelta(days=1),
                    mastered=False,
                    code_evidence=evidence_list,
                    concept_category=category
                )
                
                flashcards.append(flashcard)
            
            logger.info(f"Generated {len(flashcards)} flashcards in {language}")
            
        except Exception as e:
            logger.error(f"Flashcard generation failed: {e}")
            # Return basic flashcards as fallback
            flashcards = self.generate_basic_flashcards(multi_file_analysis)
        
        return flashcards
    
    def generate_quiz(
        self,
        multi_file_analysis: MultiFileAnalysis,
        intent: UserIntent,
        num_questions: int = 10,
        language: str = "english"
    ) -> Dict[str, Any]:
        """
        Generate quiz from multi-file analysis.
        
        Args:
            multi_file_analysis: MultiFileAnalysis with code analysis
            intent: User's learning intent
            num_questions: Number of questions to generate
            language: Output language
            
        Returns:
            Quiz dictionary with questions
        """
        questions = []
        
        try:
            logger.info(f"Generating {num_questions} quiz questions in {language}")
            
            # Generate questions from different sources
            concepts = multi_file_analysis.key_concepts[:num_questions]
            
            for i, concept in enumerate(concepts):
                # Extract code evidence
                evidence_list = []
                if 'evidence' in concept and concept['evidence']:
                    for ev_dict in concept['evidence']:
                        evidence = CodeEvidence(
                            file_path=ev_dict.get('file_path', concept.get('file', '')),
                            line_start=ev_dict.get('line_start', concept.get('line', 1)),
                            line_end=ev_dict.get('line_end', concept.get('line', 1) + 5),
                            code_snippet="",
                            context_description=ev_dict.get('context', '')
                        )
                        evidence_list.append(evidence)
                
                if not evidence_list:
                    continue
                
                # Generate question based on category
                category = concept.get('category', 'general')
                name = concept.get('name', 'Unknown')
                description = concept.get('description', '')
                
                # Language-specific question templates
                if language == "hindi":
                    if category == 'functions':
                        question_text = f"फ़ंक्शन '{name}' का मुख्य उद्देश्य क्या है?"
                        correct_answer = description
                        options = [
                            correct_answer,
                            "यूज़र ऑथेंटिकेशन को हैंडल करना",
                            "डेटाबेस कनेक्शन को मैनेज करना",
                            "HTTP रिक्वेस्ट को प्रोसेस करना"
                        ]
                    elif category == 'classes':
                        question_text = f"क्लास '{name}' क्या दर्शाती है?"
                        correct_answer = description
                        options = [
                            correct_answer,
                            "हेल्पर फ़ंक्शन के लिए यूटिलिटी क्लास",
                            "डेटा ट्रांसफर ऑब्जेक्ट",
                            "कॉन्फ़िगरेशन मैनेजर"
                        ]
                    else:
                        question_text = f"{name} क्या है?"
                        correct_answer = description
                        options = [correct_answer, "विकल्प A", "विकल्प B", "विकल्प C"]
                    explanation = f"{concept.get('file', 'रिपॉजिटरी')} में कोड के आधार पर, {description}"
                
                elif language == "telugu":
                    if category == 'functions':
                        question_text = f"ఫంక్షన్ '{name}' యొక్క ప్రాథమిక ఉద్దేశ్యం ఏమిటి?"
                        correct_answer = description
                        options = [
                            correct_answer,
                            "యూజర్ ఆథెంటికేషన్ హ్యాండిల్ చేయడం",
                            "డేటాబేస్ కనెక్షన్లను నిర్వహించడం",
                            "HTTP రిక్వెస్ట్లను ప్రాసెస్ చేయడం"
                        ]
                    elif category == 'classes':
                        question_text = f"క్లాస్ '{name}' ఏమి సూచిస్తుంది?"
                        correct_answer = description
                        options = [
                            correct_answer,
                            "హెల్పర్ ఫంక్షన్ల కోసం యుటిలిటీ క్లాస్",
                            "డేటా ట్రాన్స్ఫర్ ఆబ్జెక్ట్",
                            "కాన్ఫిగరేషన్ మేనేజర్"
                        ]
                    else:
                        question_text = f"{name} అంటే ఏమిటి?"
                        correct_answer = description
                        options = [correct_answer, "ఆప్షన్ A", "ఆప్షన్ B", "ఆప్షన్ C"]
                    explanation = f"{concept.get('file', 'రిపోజిటరీ')}లోని కోడ్ ఆధారంగా, {description}"
                
                else:  # English
                    if category == 'functions':
                        question_text = f"What is the primary purpose of the function '{name}'?"
                        correct_answer = description
                        options = [
                            correct_answer,
                            "To handle user authentication",
                            "To manage database connections",
                            "To process HTTP requests"
                        ]
                    elif category == 'classes':
                        question_text = f"What does the class '{name}' represent?"
                        correct_answer = description
                        options = [
                            correct_answer,
                            "A utility class for helper functions",
                            "A data transfer object",
                            "A configuration manager"
                        ]
                    else:
                        question_text = f"What is {name}?"
                        correct_answer = description
                        options = [correct_answer, "Option A", "Option B", "Option C"]
                    explanation = f"Based on the code in {concept.get('file', 'the repository')}, {description}"
                
                # Ensure correct answer is in options
                if correct_answer not in options:
                    options[0] = correct_answer
                
                question = CodeQuestion(
                    id=str(i),
                    type="multiple_choice",
                    question_text=question_text,
                    options=options,
                    correct_answer=correct_answer,
                    explanation=explanation,
                    code_evidence=evidence_list,
                    question_category=category
                )
                
                questions.append(question)
            
            quiz = {
                'id': f"quiz_{intent.primary_intent}_{uuid.uuid4().hex[:8]}",
                'topic': intent.primary_intent,
                'questions': questions,
                'time_limit_minutes': num_questions * 2
            }
            
            logger.info(f"Generated quiz with {len(questions)} questions in {language}")
            
        except Exception as e:
            logger.error(f"Quiz generation failed: {e}")
            quiz = self.generate_basic_quiz(multi_file_analysis)
        
        return quiz
    
    def generate_learning_path(
        self,
        multi_file_analysis: MultiFileAnalysis,
        intent: UserIntent,
        language: str = "english"
    ) -> LearningPath:
        """
        Generate ordered learning path.
        
        Args:
            multi_file_analysis: MultiFileAnalysis with code analysis
            intent: User's learning intent
            language: Output language
            
        Returns:
            LearningPath object with ordered steps
        """
        try:
            logger.info(f"Generating learning path in {language}")
            
            # Group concepts by category
            concepts_by_category = {}
            for concept in multi_file_analysis.key_concepts:
                category = concept.get('category', 'general')
                if category not in concepts_by_category:
                    concepts_by_category[category] = []
                concepts_by_category[category].append(concept)
            
            # Define learning order (foundational to advanced)
            category_order = ['classes', 'functions', 'patterns', 'architecture', 'data_structures', 'algorithms']
            
            # Language-specific category titles
            category_titles = {
                'english': {
                    'classes': 'Understanding Classes',
                    'functions': 'Understanding Functions',
                    'patterns': 'Understanding Design Patterns',
                    'architecture': 'Understanding Architecture',
                    'data_structures': 'Understanding Data Structures',
                    'algorithms': 'Understanding Algorithms'
                },
                'hindi': {
                    'classes': 'क्लासेस को समझना',
                    'functions': 'फ़ंक्शन को समझना',
                    'patterns': 'डिज़ाइन पैटर्न को समझना',
                    'architecture': 'आर्किटेक्चर को समझना',
                    'data_structures': 'डेटा स्ट्रक्चर को समझना',
                    'algorithms': 'एल्गोरिदम को समझना'
                },
                'telugu': {
                    'classes': 'క్లాసెస్ అర్థం చేసుకోవడం',
                    'functions': 'ఫంక్షన్స్ అర్థం చేసుకోవడం',
                    'patterns': 'డిజైన్ ప్యాటర్న్స్ అర్థం చేసుకోవడం',
                    'architecture': 'ఆర్కిటెక్చర్ అర్థం చేసుకోవడం',
                    'data_structures': 'డేటా స్ట్రక్చర్స్ అర్థం చేసుకోవడం',
                    'algorithms': 'అల్గారిథమ్స్ అర్థం చేసుకోవడం'
                }
            }
            
            titles = category_titles.get(language, category_titles['english'])
            
            # Create learning steps
            steps = []
            step_number = 1
            
            for category in category_order:
                if category not in concepts_by_category:
                    continue
                
                concepts = concepts_by_category[category]
                
                # Create a step for this category
                step_id = f"step_{step_number}"
                
                # Extract evidence and files
                evidence_list = []
                recommended_files = set()
                concepts_covered = []
                
                for concept in concepts[:3]:  # Limit to 3 concepts per step
                    concepts_covered.append(concept.get('name', 'Unknown'))
                    recommended_files.add(concept.get('file', ''))
                    
                    if 'evidence' in concept and concept['evidence']:
                        for ev_dict in concept['evidence']:
                            evidence = CodeEvidence(
                                file_path=ev_dict.get('file_path', concept.get('file', '')),
                                line_start=ev_dict.get('line_start', 1),
                                line_end=ev_dict.get('line_end', 10),
                                code_snippet="",
                                context_description=ev_dict.get('context', '')
                            )
                            evidence_list.append(evidence)
                
                # Language-specific descriptions
                if language == "hindi":
                    description = f"{', '.join(concepts_covered[:3])} के बारे में जानें"
                elif language == "telugu":
                    description = f"{', '.join(concepts_covered[:3])} గురించి తెలుసుకోండి"
                else:
                    description = f"Learn about {', '.join(concepts_covered[:3])}"
                
                step = LearningStep(
                    step_id=step_id,
                    step_number=step_number,
                    title=titles.get(category, category.replace('_', ' ').title()),
                    description=description,
                    estimated_time_minutes=20,
                    recommended_files=list(recommended_files),
                    concepts_covered=concepts_covered,
                    code_evidence=evidence_list,
                    prerequisites=[f"step_{step_number-1}"] if step_number > 1 else []
                )
                
                steps.append(step)
                step_number += 1
            
            # Calculate total time
            total_time = sum(step.estimated_time_minutes for step in steps)
            
            # Language-specific path titles
            if language == "hindi":
                path_title = f"सीखने का रास्ता: {intent.primary_intent.replace('_', ' ').title()}"
                path_desc = f"{len(steps)} संरचित चरणों के माध्यम से कोडबेस में महारत हासिल करें"
            elif language == "telugu":
                path_title = f"నేర్చుకునే మార్గం: {intent.primary_intent.replace('_', ' ').title()}"
                path_desc = f"{len(steps)} నిర్మాణాత్మక దశల ద్వారా కోడ్‌బేస్‌లో నైపుణ్యం సాధించండి"
            else:
                path_title = f"Learning Path: {intent.primary_intent.replace('_', ' ').title()}"
                path_desc = f"Master the codebase through {len(steps)} structured steps"
            
            learning_path = LearningPath(
                path_id=f"path_{intent.primary_intent}_{uuid.uuid4().hex[:8]}",
                title=path_title,
                description=path_desc,
                total_steps=len(steps),
                estimated_total_time_minutes=total_time,
                steps=steps,
                difficulty_level=intent.audience_level
            )
            
            logger.info(f"Generated learning path with {len(steps)} steps in {language}")
            return learning_path
        
        except Exception as e:
            logger.error(f"Learning path generation failed: {e}")
            return self._create_empty_learning_path(intent)
    
    def generate_concept_summary(
        self,
        multi_file_analysis: MultiFileAnalysis,
        intent: UserIntent,
        language: str = "english"
    ) -> Dict[str, Any]:
        """
        Generate concept summary organized by category.
        
        Args:
            multi_file_analysis: MultiFileAnalysis with code analysis
            intent: User's learning intent
            language: Output language
            
        Returns:
            Dictionary with categorized concepts
        """
        try:
            # Language-specific labels
            labels = {
                'english': {
                    'total_concepts': 'Total Concepts',
                    'categories': 'Categories',
                    'top_concepts': 'Top Concepts'
                },
                'hindi': {
                    'total_concepts': 'कुल अवधारणाएं',
                    'categories': 'श्रेणियां',
                    'top_concepts': 'शीर्ष अवधारणाएं'
                },
                'telugu': {
                    'total_concepts': 'మొత్తం కాన్సెప్ట్‌లు',
                    'categories': 'వర్గాలు',
                    'top_concepts': 'టాప్ కాన్సెప్ట్‌లు'
                }
            }
            
            lang_labels = labels.get(language, labels['english'])
            
            summary = {
                'total_concepts': len(multi_file_analysis.key_concepts),
                'categories': {},
                'top_concepts': [],
                'language': language
            }
            
            # Group by category
            for concept in multi_file_analysis.key_concepts:
                category = concept.get('category', 'general')
                if category not in summary['categories']:
                    summary['categories'][category] = []
                
                summary['categories'][category].append({
                    'name': concept.get('name', 'Unknown'),
                    'description': concept.get('description', ''),
                    'file': concept.get('file', ''),
                    'line': concept.get('line', 0)
                })
            
            # Get top concepts (first 5)
            summary['top_concepts'] = [
                {
                    'name': c.get('name', 'Unknown'),
                    'category': c.get('category', 'general'),
                    'description': c.get('description', '')
                }
                for c in multi_file_analysis.key_concepts[:5]
            ]
            
            logger.info(f"Generated concept summary with {len(summary['categories'])} categories in {language}")
            return summary
        
        except Exception as e:
            logger.error(f"Concept summary generation failed: {e}")
            return {'total_concepts': 0, 'categories': {}, 'top_concepts': [], 'language': language}
    
    def _extract_code_evidence(
        self,
        file_path: str,
        line_start: int,
        line_end: int,
        context: str
    ) -> CodeEvidence:
        """
        Extract code evidence for traceability.
        
        Args:
            file_path: Path to code file
            line_start: Starting line number
            line_end: Ending line number
            context: Context description
            
        Returns:
            CodeEvidence object
        """
        return CodeEvidence(
            file_path=file_path,
            line_start=line_start,
            line_end=line_end,
            code_snippet="",  # Will be filled by traceability manager
            context_description=context
        )
    
    def generate_basic_flashcards(
        self,
        multi_file_analysis: MultiFileAnalysis
    ) -> List[CodeFlashcard]:
        """
        Generate basic flashcards as fallback when AI fails.
        
        Args:
            multi_file_analysis: MultiFileAnalysis
            
        Returns:
            List of basic flashcards
        """
        flashcards = []
        
        try:
            # Generate from file analyses
            for file_path, analysis in list(multi_file_analysis.file_analyses.items())[:5]:
                if hasattr(analysis, 'structure'):
                    # Create flashcard from first function
                    if hasattr(analysis.structure, 'functions') and analysis.structure.functions:
                        func = analysis.structure.functions[0]
                        
                        evidence = CodeEvidence(
                            file_path=file_path,
                            line_start=func.line_number,
                            line_end=func.line_number + 5,
                            code_snippet="",
                            context_description=f"Function {func.name}"
                        )
                        
                        flashcard = CodeFlashcard(
                            id=str(uuid.uuid4()),
                            front=f"What does {func.name} do?",
                            back=func.docstring or f"Function with parameters: {', '.join(func.parameters)}",
                            topic="Code Structure",
                            difficulty="intermediate",
                            code_evidence=[evidence],
                            concept_category="functions"
                        )
                        flashcards.append(flashcard)
        
        except Exception as e:
            logger.error(f"Basic flashcard generation failed: {e}")
        
        return flashcards
    
    def generate_basic_quiz(
        self,
        multi_file_analysis: MultiFileAnalysis
    ) -> Dict[str, Any]:
        """
        Generate basic quiz as fallback when AI fails.
        
        Args:
            multi_file_analysis: MultiFileAnalysis
            
        Returns:
            Basic quiz dictionary
        """
        questions = []
        
        try:
            # Generate simple questions from analysis
            for i, (file_path, analysis) in enumerate(list(multi_file_analysis.file_analyses.items())[:5]):
                if hasattr(analysis, 'structure') and hasattr(analysis.structure, 'functions'):
                    if analysis.structure.functions:
                        func = analysis.structure.functions[0]
                        
                        evidence = CodeEvidence(
                            file_path=file_path,
                            line_start=func.line_number,
                            line_end=func.line_number + 5,
                            code_snippet="",
                            context_description=f"Function {func.name}"
                        )
                        
                        question = CodeQuestion(
                            id=str(i),
                            type="multiple_choice",
                            question_text=f"What is the purpose of {func.name}?",
                            options=[
                                func.docstring or "Primary function",
                                "Helper function",
                                "Utility function",
                                "Configuration function"
                            ],
                            correct_answer=func.docstring or "Primary function",
                            explanation=f"Based on the code structure",
                            code_evidence=[evidence],
                            question_category="functions"
                        )
                        questions.append(question)
        
        except Exception as e:
            logger.error(f"Basic quiz generation failed: {e}")
        
        return {
            'id': f"basic_quiz_{uuid.uuid4().hex[:8]}",
            'topic': "Code Understanding",
            'questions': questions,
            'time_limit_minutes': len(questions) * 2
        }
    
    def _create_empty_learning_path(self, intent: UserIntent) -> LearningPath:
        """Create empty learning path for error cases."""
        return LearningPath(
            path_id=f"empty_path_{uuid.uuid4().hex[:8]}",
            title="Learning Path",
            description="No learning path available",
            total_steps=0,
            estimated_total_time_minutes=0,
            steps=[],
            difficulty_level=intent.audience_level
        )
