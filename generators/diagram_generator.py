"""Diagram generator for creating visual representations of code."""
import re
from typing import List
from analyzers.code_analyzer import Class, Function, CodeStructure
import logging

logger = logging.getLogger(__name__)


class DiagramGenerator:
    """Creates visual diagrams from code using Mermaid syntax."""
    
    def generate_flowchart(self, function_code: str, function_name: str = "function") -> str:
        """
        Generate Mermaid flowchart for function logic.
        
        Args:
            function_code: Source code of the function
            function_name: Name of the function
            
        Returns:
            Mermaid flowchart syntax
        """
        try:
            lines = function_code.strip().split('\n')
            
            # Start flowchart
            mermaid = f"graph TD\n"
            mermaid += f"    Start([Start: {function_name}])\n"
            
            node_id = 1
            prev_node = "Start"
            
            for line in lines:
                stripped = line.strip()
                
                if not stripped or stripped.startswith('#') or stripped.startswith('"""'):
                    continue
                
                # Detect control structures
                if stripped.startswith('if '):
                    condition = stripped[3:].rstrip(':')
                    mermaid += f"    {prev_node} --> Decision{node_id}{{{{if {condition}?}}}}\n"
                    prev_node = f"Decision{node_id}"
                    node_id += 1
                
                elif stripped.startswith('for ') or stripped.startswith('while '):
                    loop_type = "for" if stripped.startswith('for') else "while"
                    condition = stripped.split(':', 1)[0]
                    mermaid += f"    {prev_node} --> Loop{node_id}[/{loop_type} {condition}/]\n"
                    prev_node = f"Loop{node_id}"
                    node_id += 1
                
                elif stripped.startswith('return '):
                    return_val = stripped[7:]
                    mermaid += f"    {prev_node} --> Return{node_id}[Return: {return_val}]\n"
                    mermaid += f"    Return{node_id} --> End([End])\n"
                    prev_node = f"Return{node_id}"
                    node_id += 1
                
                elif '=' in stripped and not stripped.startswith('def '):
                    var_name = stripped.split('=')[0].strip()
                    mermaid += f"    {prev_node} --> Process{node_id}[{var_name} assignment]\n"
                    prev_node = f"Process{node_id}"
                    node_id += 1
            
            # Add end if not already added
            if "End" not in mermaid:
                mermaid += f"    {prev_node} --> End([End])\n"
            
            return mermaid
        
        except Exception as e:
            logger.error(f"Flowchart generation failed: {e}")
            return self._get_simple_flowchart(function_name)
    
    def generate_class_diagram(self, classes: List[Class]) -> str:
        """
        Generate Mermaid class diagram.
        
        Args:
            classes: List of Class objects
            
        Returns:
            Mermaid class diagram syntax
        """
        try:
            if not classes:
                return "classDiagram\n    class NoClasses{\n        +No classes found\n    }"
            
            mermaid = "classDiagram\n"
            
            for cls in classes:
                mermaid += f"    class {cls.name}{{\n"
                
                # Add methods
                for method in cls.methods[:10]:  # Limit to 10 methods
                    mermaid += f"        +{method}()\n"
                
                mermaid += "    }\n"
            
            # Add simple relationships if multiple classes
            if len(classes) > 1:
                for i in range(len(classes) - 1):
                    mermaid += f"    {classes[i].name} --> {classes[i+1].name}\n"
            
            return mermaid
        
        except Exception as e:
            logger.error(f"Class diagram generation failed: {e}")
            return "classDiagram\n    class Error{\n        +Diagram generation failed\n    }"
    
    def generate_architecture_diagram(self, structure: CodeStructure, project_name: str = "Project") -> str:
        """
        Generate architecture diagram for project.
        
        Args:
            structure: Code structure
            project_name: Name of the project
            
        Returns:
            Mermaid architecture diagram syntax
        """
        try:
            mermaid = "graph TB\n"
            mermaid += f"    Main[{project_name}]\n"
            
            # Add classes
            if structure.classes:
                mermaid += "    subgraph Classes\n"
                for cls in structure.classes[:5]:  # Limit to 5
                    mermaid += f"        {cls.name}[{cls.name}]\n"
                mermaid += "    end\n"
                mermaid += "    Main --> Classes\n"
            
            # Add functions
            if structure.functions:
                mermaid += "    subgraph Functions\n"
                for func in structure.functions[:5]:  # Limit to 5
                    mermaid += f"        {func.name}[{func.name}()]\n"
                mermaid += "    end\n"
                mermaid += "    Main --> Functions\n"
            
            # Add imports
            if structure.imports:
                mermaid += "    subgraph Dependencies\n"
                for imp in structure.imports[:5]:  # Limit to 5
                    safe_name = imp.replace('.', '_').replace('-', '_')
                    mermaid += f"        {safe_name}[{imp}]\n"
                mermaid += "    end\n"
                mermaid += "    Main --> Dependencies\n"
            
            return mermaid
        
        except Exception as e:
            logger.error(f"Architecture diagram generation failed: {e}")
            return "graph TB\n    Main[Project]\n    Main --> Error[Diagram generation failed]"
    
    def generate_sequence_diagram(self, api_code: str) -> str:
        """
        Generate sequence diagram for API interactions.
        
        Args:
            api_code: API-related code
            
        Returns:
            Mermaid sequence diagram syntax
        """
        try:
            mermaid = "sequenceDiagram\n"
            mermaid += "    participant Client\n"
            mermaid += "    participant API\n"
            mermaid += "    participant Database\n\n"
            
            # Detect API patterns
            if "get" in api_code.lower() or "fetch" in api_code.lower():
                mermaid += "    Client->>API: GET Request\n"
                mermaid += "    API->>Database: Query Data\n"
                mermaid += "    Database-->>API: Return Data\n"
                mermaid += "    API-->>Client: Response\n"
            
            elif "post" in api_code.lower() or "create" in api_code.lower():
                mermaid += "    Client->>API: POST Request\n"
                mermaid += "    API->>Database: Insert Data\n"
                mermaid += "    Database-->>API: Confirmation\n"
                mermaid += "    API-->>Client: Success Response\n"
            
            elif "put" in api_code.lower() or "update" in api_code.lower():
                mermaid += "    Client->>API: PUT Request\n"
                mermaid += "    API->>Database: Update Data\n"
                mermaid += "    Database-->>API: Confirmation\n"
                mermaid += "    API-->>Client: Success Response\n"
            
            elif "delete" in api_code.lower():
                mermaid += "    Client->>API: DELETE Request\n"
                mermaid += "    API->>Database: Delete Data\n"
                mermaid += "    Database-->>API: Confirmation\n"
                mermaid += "    API-->>Client: Success Response\n"
            
            else:
                mermaid += "    Client->>API: Request\n"
                mermaid += "    API->>Database: Process\n"
                mermaid += "    Database-->>API: Result\n"
                mermaid += "    API-->>Client: Response\n"
            
            return mermaid
        
        except Exception as e:
            logger.error(f"Sequence diagram generation failed: {e}")
            return "sequenceDiagram\n    Client->>API: Request\n    API-->>Client: Response"
    
    def _get_simple_flowchart(self, function_name: str) -> str:
        """Generate a simple fallback flowchart."""
        return f"""graph TD
    Start([Start: {function_name}])
    Start --> Process[Execute function logic]
    Process --> End([End])
"""
