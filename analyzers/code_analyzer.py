"""Code analyzer for parsing and analyzing code files."""
import ast
import re
from dataclasses import dataclass
from typing import List, Optional
from ai.langchain_orchestrator import LangChainOrchestrator
import logging

logger = logging.getLogger(__name__)


@dataclass
class Function:
    """Represents a function in code."""
    name: str
    parameters: List[str]
    line_number: int
    docstring: Optional[str] = None


@dataclass
class Class:
    """Represents a class in code."""
    name: str
    methods: List[str]
    line_number: int
    docstring: Optional[str] = None


@dataclass
class CodeStructure:
    """Represents the structure of code."""
    functions: List[Function]
    classes: List[Class]
    imports: List[str]
    main_logic: str


@dataclass
class Pattern:
    """Represents a design pattern or algorithm."""
    name: str
    description: str
    location: str


@dataclass
class Issue:
    """Represents a code issue."""
    severity: str  # "critical", "warning", "suggestion"
    line_number: int
    description: str
    suggestion: str


@dataclass
class CodeAnalysis:
    """Complete code analysis result."""
    summary: str
    structure: CodeStructure
    patterns: List[Pattern]
    issues: List[Issue]
    complexity_score: int


class CodeAnalyzer:
    """Analyzes code files and extracts structure and metadata."""
    
    def __init__(self, langchain_orchestrator: LangChainOrchestrator):
        """Initialize with LangChain orchestrator."""
        self.orchestrator = langchain_orchestrator
    
    def analyze_file(
        self,
        code: str,
        filename: str,
        language: str = "english"
    ) -> CodeAnalysis:
        """
        Analyze a single code file.
        
        Args:
            code: Source code content
            filename: Name of the file
            language: Output language for explanations
            
        Returns:
            Complete code analysis
        """
        try:
            if not code:
                return CodeAnalysis(
                    summary="No code provided",
                    structure=CodeStructure([], [], [], ""),
                    patterns=[],
                    issues=[],
                    complexity_score=0
                )
            
            # Extract structure
            file_extension = filename.split('.')[-1] if '.' in filename else ''
            structure = self.extract_structure(code, file_extension)
            
            # Generate summary using AI
            summary = self.orchestrator.summarize_code(code, language)
            
            # Identify patterns using AI
            patterns = self.identify_patterns(code)
            
            # Detect issues
            issues = self.detect_issues(code, language)
            
            # Calculate complexity (simple heuristic)
            complexity_score = self._calculate_complexity(code)
            
            return CodeAnalysis(
                summary=summary,
                structure=structure,
                patterns=patterns,
                issues=issues,
                complexity_score=complexity_score
            )
        
        except Exception as e:
            logger.error(f"Code analysis failed: {e}")
            # Return minimal analysis
            return CodeAnalysis(
                summary=f"Analysis failed: {str(e)}",
                structure=CodeStructure([], [], [], ""),
                patterns=[],
                issues=[],
                complexity_score=0
            )
    
    def extract_structure(
        self,
        code: str,
        file_extension: str
    ) -> CodeStructure:
        """
        Extract functions, classes, and imports from code.
        
        Args:
            code: Source code
            file_extension: File extension (py, js, etc.)
            
        Returns:
            Code structure
        """
        if file_extension == 'py':
            return self._extract_python_structure(code)
        elif file_extension in ['js', 'jsx', 'ts', 'tsx']:
            return self._extract_javascript_structure(code)
        else:
            return self._extract_generic_structure(code)
    
    def _extract_python_structure(self, code: str) -> CodeStructure:
        """Extract structure from Python code using AST."""
        functions = []
        classes = []
        imports = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(Function(
                        name=node.name,
                        parameters=[arg.arg for arg in node.args.args],
                        line_number=node.lineno,
                        docstring=ast.get_docstring(node)
                    ))
                
                elif isinstance(node, ast.ClassDef):
                    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    classes.append(Class(
                        name=node.name,
                        methods=methods,
                        line_number=node.lineno,
                        docstring=ast.get_docstring(node)
                    ))
                
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        imports.extend([alias.name for alias in node.names])
                    else:
                        imports.append(node.module or "")
        
        except SyntaxError as e:
            logger.warning(f"Python syntax error: {e}")
        
        main_logic = "Main execution logic detected" if "__main__" in code else ""
        
        return CodeStructure(
            functions=functions,
            classes=classes,
            imports=imports,
            main_logic=main_logic
        )
    
    def _extract_javascript_structure(self, code: str) -> CodeStructure:
        """Extract structure from JavaScript/TypeScript code using regex."""
        functions = []
        classes = []
        imports = []
        
        # Extract function declarations
        func_pattern = r'(?:function|const|let|var)\s+(\w+)\s*(?:=\s*)?(?:\([^)]*\)|async\s*\([^)]*\))'
        for match in re.finditer(func_pattern, code):
            line_num = code[:match.start()].count('\n') + 1
            functions.append(Function(
                name=match.group(1),
                parameters=[],
                line_number=line_num
            ))
        
        # Extract class declarations
        class_pattern = r'class\s+(\w+)'
        for match in re.finditer(class_pattern, code):
            line_num = code[:match.start()].count('\n') + 1
            classes.append(Class(
                name=match.group(1),
                methods=[],
                line_number=line_num
            ))
        
        # Extract imports
        import_pattern = r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]'
        imports = [match.group(1) for match in re.finditer(import_pattern, code)]
        
        return CodeStructure(
            functions=functions,
            classes=classes,
            imports=imports,
            main_logic=""
        )
    
    def _extract_generic_structure(self, code: str) -> CodeStructure:
        """Extract basic structure from any code."""
        # Simple line-based analysis
        lines = code.split('\n')
        
        return CodeStructure(
            functions=[],
            classes=[],
            imports=[],
            main_logic=f"{len(lines)} lines of code"
        )
    
    def identify_patterns(self, code: str) -> List[Pattern]:
        """
        Identify design patterns and algorithms.
        
        Args:
            code: Source code
            
        Returns:
            List of identified patterns
        """
        patterns = []
        
        if not code:
            return patterns
        
        # Simple pattern detection
        if "class" in code.lower() and "def __init__" in code:
            patterns.append(Pattern(
                name="Object-Oriented Design",
                description="Uses classes and objects",
                location="Throughout file"
            ))
        
        if "async" in code or "await" in code:
            patterns.append(Pattern(
                name="Asynchronous Programming",
                description="Uses async/await patterns",
                location="Async functions"
            ))
        
        if "try:" in code and "except" in code:
            patterns.append(Pattern(
                name="Error Handling",
                description="Implements try-except error handling",
                location="Error handling blocks"
            ))
        
        return patterns
    
    def detect_issues(self, code: str, language: str) -> List[Issue]:
        """
        Detect potential bugs and anti-patterns.
        
        Args:
            code: Source code
            language: Output language
            
        Returns:
            List of issues
        """
        issues = []
        
        if not code:
            return issues
        
        # Simple static checks
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            if "TODO" in line or "FIXME" in line:
                issues.append(Issue(
                    severity="suggestion",
                    line_number=i,
                    description="TODO or FIXME comment found",
                    suggestion="Complete the pending task"
                ))
        
        return issues
    
    def _calculate_complexity(self, code: str) -> int:
        """Calculate code complexity score (simplified)."""
        lines = code.split('\n')
        non_empty_lines = [l for l in lines if l.strip()]
        
        # Simple heuristic based on lines and control structures
        complexity = len(non_empty_lines)
        complexity += code.count('if ') * 2
        complexity += code.count('for ') * 2
        complexity += code.count('while ') * 2
        complexity += code.count('class ') * 5
        
        return min(complexity, 100)  # Cap at 100
