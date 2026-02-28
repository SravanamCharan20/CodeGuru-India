"""
Multi-File Analyzer for analyzing multiple code files and their relationships.

This module analyzes multiple files together to understand relationships,
data flow, control flow, and system behavior across the codebase.
"""

import logging
import os
import re
import uuid
from typing import List, Dict, Any, Set
from collections import defaultdict
from models.intent_models import (
    FileSelection,
    FileRelationship,
    DataFlow,
    ExecutionPath,
    MultiFileAnalysis,
    UserIntent
)

logger = logging.getLogger(__name__)


class MultiFileAnalyzer:
    """Analyzes multiple files together to understand relationships and system behavior."""
    
    def __init__(self, code_analyzer, langchain_orchestrator=None):
        """
        Initialize with code analyzer and AI orchestrator.
        
        Args:
            code_analyzer: CodeAnalyzer instance for individual file analysis
            langchain_orchestrator: LangChainOrchestrator for AI-powered analysis
        """
        self.code_analyzer = code_analyzer
        self.orchestrator = langchain_orchestrator
    
    def analyze_files(
        self,
        file_selections: List[FileSelection],
        repo_path: str,
        intent: UserIntent
    ) -> MultiFileAnalysis:
        """
        Analyze multiple files and their relationships.
        
        Args:
            file_selections: List of selected files to analyze
            repo_path: Path to repository root
            intent: User's learning intent
            
        Returns:
            MultiFileAnalysis with complete analysis results
        """
        try:
            logger.info(f"Analyzing {len(file_selections)} files")
            
            # Step 1: Analyze individual files
            file_analyses = {}
            analyzed_files = []
            
            for selection in file_selections:
                try:
                    file_path = os.path.join(repo_path, selection.file_info.path)
                    
                    # Skip if it's a directory
                    if os.path.isdir(file_path):
                        logger.warning(f"Skipping directory: {file_path}")
                        continue
                    
                    # Skip if file doesn't exist
                    if not os.path.isfile(file_path):
                        logger.warning(f"File not found: {file_path}")
                        continue
                    
                    # Read file content
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code = f.read()
                    
                    # Analyze using CodeAnalyzer
                    analysis = self.code_analyzer.analyze_file(
                        code=code,
                        filename=selection.file_info.name,
                        language="english"
                    )
                    
                    file_analyses[selection.file_info.path] = analysis
                    analyzed_files.append(selection.file_info.path)
                    
                    logger.info(f"Analyzed {selection.file_info.path}")
                
                except Exception as e:
                    logger.warning(f"Failed to analyze {selection.file_info.path}: {e}")
                    # Continue with remaining files (graceful degradation)
                    continue
            
            if not file_analyses:
                logger.error("No files were successfully analyzed")
                return self._create_empty_analysis()
            
            # Step 2: Detect relationships between files
            relationships = self.detect_relationships(file_analyses)
            
            # Step 3: Build dependency graph
            dependency_graph = self.build_dependency_graph(relationships)
            
            # Step 4: Identify data flows
            data_flows = self.identify_data_flows(file_analyses, relationships)
            
            # Step 5: Identify execution paths
            execution_paths = self.identify_execution_paths(
                file_analyses,
                dependency_graph,
                intent
            )
            
            # Step 6: Detect cross-file patterns
            cross_file_patterns = self.detect_cross_file_patterns(file_analyses)
            
            # Step 7: Extract key concepts
            key_concepts = self.extract_key_concepts(
                MultiFileAnalysis(
                    analyzed_files=analyzed_files,
                    file_analyses=file_analyses,
                    relationships=relationships,
                    dependency_graph=dependency_graph,
                    data_flows=data_flows,
                    execution_paths=execution_paths,
                    cross_file_patterns=cross_file_patterns
                ),
                intent
            )
            
            # Step 8: Generate summary
            summary = self._generate_analysis_summary(
                analyzed_files,
                relationships,
                key_concepts,
                intent
            )
            
            logger.info(f"Multi-file analysis complete: {len(analyzed_files)} files, "
                       f"{len(relationships)} relationships, {len(key_concepts)} concepts")
            
            return MultiFileAnalysis(
                analyzed_files=analyzed_files,
                file_analyses=file_analyses,
                relationships=relationships,
                dependency_graph=dependency_graph,
                data_flows=data_flows,
                execution_paths=execution_paths,
                cross_file_patterns=cross_file_patterns,
                key_concepts=key_concepts,
                analysis_summary=summary
            )
        
        except Exception as e:
            logger.error(f"Multi-file analysis failed: {e}")
            return self._create_empty_analysis()
    
    def detect_relationships(
        self,
        file_analyses: Dict[str, Any]
    ) -> List[FileRelationship]:
        """
        Detect relationships between analyzed files.
        
        Args:
            file_analyses: Dictionary mapping file paths to CodeAnalysis objects
            
        Returns:
            List of FileRelationship objects
        """
        relationships = []
        
        try:
            # Build import map
            import_map = {}
            for file_path, analysis in file_analyses.items():
                if hasattr(analysis, 'structure') and hasattr(analysis.structure, 'imports'):
                    import_map[file_path] = analysis.structure.imports
            
            # Detect import relationships
            for source_file, imports in import_map.items():
                for import_stmt in imports:
                    # Try to match import to actual files
                    target_file = self._resolve_import(import_stmt, file_analyses.keys())
                    
                    if target_file:
                        relationships.append(FileRelationship(
                            source_file=source_file,
                            target_file=target_file,
                            relationship_type="imports",
                            details=f"Imports: {import_stmt}"
                        ))
            
            # Detect function call relationships (simplified)
            for source_file, analysis in file_analyses.items():
                if hasattr(analysis, 'structure'):
                    # Look for function calls to other files
                    for target_file in file_analyses.keys():
                        if source_file != target_file:
                            if self._has_cross_file_calls(analysis, target_file):
                                relationships.append(FileRelationship(
                                    source_file=source_file,
                                    target_file=target_file,
                                    relationship_type="calls",
                                    details="Contains function calls to this file"
                                ))
            
            logger.info(f"Detected {len(relationships)} relationships")
        
        except Exception as e:
            logger.error(f"Relationship detection failed: {e}")
        
        return relationships
    
    def build_dependency_graph(
        self,
        relationships: List[FileRelationship]
    ) -> Dict[str, List[str]]:
        """
        Build dependency graph from relationships.
        
        Args:
            relationships: List of FileRelationship objects
            
        Returns:
            Dictionary mapping files to their dependencies
        """
        graph = defaultdict(list)
        
        try:
            for rel in relationships:
                if rel.relationship_type in ["imports", "uses", "calls"]:
                    graph[rel.source_file].append(rel.target_file)
            
            # Convert to regular dict
            graph = dict(graph)
            
            logger.info(f"Built dependency graph with {len(graph)} nodes")
        
        except Exception as e:
            logger.error(f"Dependency graph construction failed: {e}")
        
        return graph
    
    def identify_data_flows(
        self,
        file_analyses: Dict[str, Any],
        relationships: List[FileRelationship]
    ) -> List[DataFlow]:
        """
        Identify how data flows between files.
        
        Args:
            file_analyses: Dictionary of file analyses
            relationships: List of relationships
            
        Returns:
            List of DataFlow objects
        """
        data_flows = []
        
        try:
            # Identify data flows based on imports and function calls
            for rel in relationships:
                if rel.relationship_type in ["imports", "calls"]:
                    flow_id = str(uuid.uuid4())[:8]
                    
                    # Get line numbers from analyses
                    source_analysis = file_analyses.get(rel.source_file)
                    target_analysis = file_analyses.get(rel.target_file)
                    
                    start_line = 1
                    end_line = 1
                    
                    if source_analysis and hasattr(source_analysis, 'structure'):
                        # Try to find import line
                        if hasattr(source_analysis.structure, 'imports'):
                            start_line = 1  # Imports typically at top
                    
                    data_flows.append(DataFlow(
                        flow_id=flow_id,
                        start_file=rel.source_file,
                        start_line=start_line,
                        end_file=rel.target_file,
                        end_line=end_line,
                        data_description=f"Data flows via {rel.relationship_type}",
                        flow_path=[rel.source_file, rel.target_file]
                    ))
            
            logger.info(f"Identified {len(data_flows)} data flows")
        
        except Exception as e:
            logger.error(f"Data flow identification failed: {e}")
        
        return data_flows
    
    def identify_execution_paths(
        self,
        file_analyses: Dict[str, Any],
        dependency_graph: Dict[str, List[str]],
        intent: UserIntent
    ) -> List[ExecutionPath]:
        """
        Identify execution paths relevant to user intent.
        
        Args:
            file_analyses: Dictionary of file analyses
            dependency_graph: Dependency graph
            intent: User intent
            
        Returns:
            List of ExecutionPath objects
        """
        execution_paths = []
        
        try:
            # Find entry points
            entry_points = self._find_entry_points(file_analyses)
            
            # Trace execution from each entry point
            for entry_file in entry_points:
                path_id = str(uuid.uuid4())[:8]
                
                # Build execution steps
                steps = []
                visited = set()
                
                self._trace_execution(
                    entry_file,
                    file_analyses,
                    dependency_graph,
                    steps,
                    visited,
                    max_depth=5
                )
                
                if steps:
                    execution_paths.append(ExecutionPath(
                        path_id=path_id,
                        entry_point=entry_file,
                        steps=steps,
                        path_description=f"Execution starting from {os.path.basename(entry_file)}"
                    ))
            
            logger.info(f"Identified {len(execution_paths)} execution paths")
        
        except Exception as e:
            logger.error(f"Execution path identification failed: {e}")
        
        return execution_paths
    
    def detect_cross_file_patterns(
        self,
        file_analyses: Dict[str, Any]
    ) -> List[Any]:
        """
        Detect design patterns spanning multiple files.
        
        Args:
            file_analyses: Dictionary of file analyses
            
        Returns:
            List of Pattern objects
        """
        patterns = []
        
        try:
            # Collect all patterns from individual files
            all_patterns = []
            for file_path, analysis in file_analyses.items():
                if hasattr(analysis, 'patterns'):
                    for pattern in analysis.patterns:
                        all_patterns.append((file_path, pattern))
            
            # Look for patterns that appear across multiple files
            pattern_files = defaultdict(list)
            for file_path, pattern in all_patterns:
                pattern_files[pattern.name].append(file_path)
            
            # Identify cross-file patterns
            for pattern_name, files in pattern_files.items():
                if len(files) > 1:
                    # This pattern appears in multiple files
                    # Create a cross-file pattern object
                    from analyzers.code_analyzer import Pattern
                    patterns.append(Pattern(
                        name=pattern_name,
                        description=f"Pattern used across {len(files)} files",
                        location=", ".join([os.path.basename(f) for f in files[:3]])
                    ))
            
            logger.info(f"Detected {len(patterns)} cross-file patterns")
        
        except Exception as e:
            logger.error(f"Cross-file pattern detection failed: {e}")
        
        return patterns
    
    def extract_key_concepts(
        self,
        multi_file_analysis: MultiFileAnalysis,
        intent: UserIntent
    ) -> List[Dict[str, Any]]:
        """
        Extract key concepts with file references.
        
        Args:
            multi_file_analysis: MultiFileAnalysis object
            intent: User intent
            
        Returns:
            List of concept dictionaries with categorization
        """
        concepts = []
        
        try:
            # Extract concepts from each file
            for file_path, analysis in multi_file_analysis.file_analyses.items():
                if hasattr(analysis, 'structure'):
                    structure = analysis.structure
                    
                    # Extract function concepts
                    for func in structure.functions[:5]:  # Limit to top 5
                        concepts.append({
                            'name': func.name,
                            'category': 'functions',
                            'description': func.docstring or f"Function with {len(func.parameters)} parameters",
                            'file': file_path,
                            'line': func.line_number,
                            'evidence': [{
                                'file_path': file_path,
                                'line_start': func.line_number,
                                'line_end': func.line_number + 5,
                                'context': f"Function {func.name}"
                            }]
                        })
                    
                    # Extract class concepts
                    for cls in structure.classes[:5]:  # Limit to top 5
                        concepts.append({
                            'name': cls.name,
                            'category': 'classes',
                            'description': cls.docstring or f"Class with {len(cls.methods)} methods",
                            'file': file_path,
                            'line': cls.line_number,
                            'evidence': [{
                                'file_path': file_path,
                                'line_start': cls.line_number,
                                'line_end': cls.line_number + 10,
                                'context': f"Class {cls.name}"
                            }]
                        })
            
            # Extract pattern concepts
            for pattern in multi_file_analysis.cross_file_patterns:
                concepts.append({
                    'name': pattern.name,
                    'category': 'patterns',
                    'description': pattern.description,
                    'file': pattern.location,
                    'line': 0,
                    'evidence': []
                })
            
            # Extract architecture concepts from relationships
            if len(multi_file_analysis.relationships) > 0:
                concepts.append({
                    'name': 'Module Dependencies',
                    'category': 'architecture',
                    'description': f"System has {len(multi_file_analysis.relationships)} inter-module dependencies",
                    'file': 'multiple',
                    'line': 0,
                    'evidence': []
                })
            
            logger.info(f"Extracted {len(concepts)} key concepts")
        
        except Exception as e:
            logger.error(f"Concept extraction failed: {e}")
        
        return concepts
    
    # ========================================================================
    # Private Helper Methods
    # ========================================================================
    
    def _resolve_import(self, import_stmt: str, available_files: List[str]) -> str:
        """Try to resolve an import statement to an actual file."""
        # Simplified import resolution
        import_parts = import_stmt.replace('from ', '').replace('import ', '').split()[0]
        import_parts = import_parts.replace('.', os.sep)
        
        # Try to match with available files
        for file_path in available_files:
            if import_parts in file_path:
                return file_path
        
        return None
    
    def _has_cross_file_calls(self, analysis: Any, target_file: str) -> bool:
        """Check if analysis contains calls to target file (simplified)."""
        # This is a simplified check - in reality would need more sophisticated analysis
        target_name = os.path.splitext(os.path.basename(target_file))[0]
        
        if hasattr(analysis, 'structure') and hasattr(analysis.structure, 'main_logic'):
            return target_name in analysis.structure.main_logic
        
        return False
    
    def _find_entry_points(self, file_analyses: Dict[str, Any]) -> List[str]:
        """Find entry point files (main, app, index, etc.)."""
        entry_points = []
        
        entry_patterns = ['main', 'app', 'index', 'server', '__main__']
        
        for file_path in file_analyses.keys():
            filename = os.path.basename(file_path).lower()
            
            for pattern in entry_patterns:
                if pattern in filename:
                    entry_points.append(file_path)
                    break
        
        # If no entry points found, use first file
        if not entry_points and file_analyses:
            entry_points.append(list(file_analyses.keys())[0])
        
        return entry_points
    
    def _trace_execution(
        self,
        current_file: str,
        file_analyses: Dict[str, Any],
        dependency_graph: Dict[str, List[str]],
        steps: List[Dict[str, Any]],
        visited: Set[str],
        max_depth: int,
        current_depth: int = 0
    ):
        """Recursively trace execution path."""
        if current_depth >= max_depth or current_file in visited:
            return
        
        visited.add(current_file)
        
        # Add current file as step
        analysis = file_analyses.get(current_file)
        if analysis and hasattr(analysis, 'structure'):
            # Get main function or first function
            main_func = None
            if hasattr(analysis.structure, 'functions') and analysis.structure.functions:
                main_func = analysis.structure.functions[0]
            
            steps.append({
                'file': current_file,
                'function': main_func.name if main_func else 'module',
                'line': main_func.line_number if main_func else 1,
                'description': f"Executes in {os.path.basename(current_file)}"
            })
        
        # Follow dependencies
        if current_file in dependency_graph:
            for dep_file in dependency_graph[current_file][:2]:  # Limit branching
                self._trace_execution(
                    dep_file,
                    file_analyses,
                    dependency_graph,
                    steps,
                    visited,
                    max_depth,
                    current_depth + 1
                )
    
    def _generate_analysis_summary(
        self,
        analyzed_files: List[str],
        relationships: List[FileRelationship],
        key_concepts: List[Dict[str, Any]],
        intent: UserIntent
    ) -> str:
        """Generate summary of multi-file analysis."""
        summary_parts = [
            f"Analyzed {len(analyzed_files)} files for {intent.primary_intent}",
            f"Found {len(relationships)} inter-file relationships",
            f"Extracted {len(key_concepts)} key concepts"
        ]
        
        # Add concept breakdown
        concept_categories = defaultdict(int)
        for concept in key_concepts:
            concept_categories[concept['category']] += 1
        
        if concept_categories:
            category_summary = ", ".join([
                f"{count} {cat}" for cat, count in concept_categories.items()
            ])
            summary_parts.append(f"Concepts: {category_summary}")
        
        return ". ".join(summary_parts)
    
    def _create_empty_analysis(self) -> MultiFileAnalysis:
        """Create empty analysis result for error cases."""
        return MultiFileAnalysis(
            analyzed_files=[],
            file_analyses={},
            relationships=[],
            dependency_graph={},
            data_flows=[],
            execution_paths=[],
            cross_file_patterns=[],
            key_concepts=[],
            analysis_summary="Analysis failed or no files to analyze"
        )
