"""
RAG-Enhanced Code Explainer.

Uses Retrieval-Augmented Generation to provide detailed explanations
with external knowledge when needed.
"""

import logging
from typing import List, Dict, Any, Optional
from analyzers.semantic_code_search import CodeChunk

logger = logging.getLogger(__name__)


class RAGExplainer:
    """Generates detailed explanations using RAG approach."""
    
    def __init__(self, langchain_orchestrator, web_search_available=False):
        """
        Initialize RAG explainer.
        
        Args:
            langchain_orchestrator: LangChainOrchestrator for AI operations
            web_search_available: Whether web search is available
        """
        self.orchestrator = langchain_orchestrator
        self.web_search_available = web_search_available
    
    def generate_detailed_explanation(
        self,
        intent: str,
        relevant_chunks: List[CodeChunk],
        repo_context: Any,
        use_web_search: bool = True,
        output_language: str = "english",
    ) -> Dict[str, Any]:
        """
        Generate detailed ChatGPT-style explanation for intent.
        
        Args:
            intent: User's intent/question
            relevant_chunks: Relevant code chunks
            repo_context: Repository context
            use_web_search: Whether to use web search for external knowledge
            output_language: Response language (english, hindi, telugu)
            
        Returns:
            Dictionary with explanation and metadata
        """
        try:
            logger.info(f"Generating detailed explanation for: {intent}")
            
            # Step 1: Analyze code chunks
            code_analysis = self._analyze_code_chunks(relevant_chunks)
            
            # Step 2: Get external knowledge if needed
            external_knowledge = ""
            if use_web_search and self.web_search_available:
                external_knowledge = self._fetch_external_knowledge(intent, code_analysis)
            
            # Step 3: Generate comprehensive explanation
            explanation = self._generate_explanation(
                intent,
                code_analysis,
                external_knowledge,
                repo_context,
                output_language=output_language,
            )
            
            return {
                'intent': intent,
                'explanation': explanation,
                'code_references': [
                    {
                        'file': chunk.file_path,
                        'lines': f"{chunk.start_line}-{chunk.end_line}",
                        'content': chunk.content[:500]  # Preview
                    }
                    for chunk in relevant_chunks[:5]
                ],
                'external_sources': external_knowledge != "",
                'confidence': 'high' if len(relevant_chunks) > 3 else 'medium'
            }
        
        except Exception as e:
            logger.error(f"Explanation generation failed: {e}")
            return {
                'intent': intent,
                'explanation': f"I encountered an error while analyzing the code: {str(e)}",
                'code_references': [],
                'external_sources': False,
                'confidence': 'low'
            }
    
    def _analyze_code_chunks(self, chunks: List[CodeChunk]) -> Dict[str, Any]:
        """
        Analyze code chunks to extract patterns and structure.
        
        Args:
            chunks: List of code chunks
            
        Returns:
            Analysis dictionary
        """
        analysis = {
            'total_chunks': len(chunks),
            'files_involved': list(set(chunk.file_path for chunk in chunks)),
            'code_summary': "",
            'key_patterns': [],
            'technologies': []
        }
        
        if not chunks:
            return analysis
        
        # Combine code for analysis
        combined_code = "\n\n".join([
            f"# File: {chunk.file_path} (lines {chunk.start_line}-{chunk.end_line})\n{chunk.content}"
            for chunk in chunks[:10]  # Limit to top 10
        ])
        
        try:
            # Generate code summary
            prompt = f"""Analyze this code and provide:
1. A brief summary of what it does
2. Key patterns or techniques used
3. Technologies/frameworks identified

Code:
```
{combined_code[:4000]}
```

Analysis:"""
            
            response = self.orchestrator.generate_completion(prompt, max_tokens=300)
            analysis['code_summary'] = response.strip()
        
        except Exception as e:
            logger.warning(f"Code analysis failed: {e}")
        
        return analysis
    
    def _fetch_external_knowledge(
        self,
        intent: str,
        code_analysis: Dict[str, Any]
    ) -> str:
        """
        Fetch external knowledge using web search.
        
        Args:
            intent: User intent
            code_analysis: Code analysis results
            
        Returns:
            External knowledge text
        """
        try:
            # Extract concepts that might need external explanation
            concepts = self._extract_concepts_needing_explanation(intent, code_analysis)
            
            if not concepts:
                return ""
            
            # Search for each concept
            knowledge_pieces = []
            
            for concept in concepts[:3]:  # Limit to 3 concepts
                try:
                    # Use web search (placeholder - integrate with actual search)
                    search_query = f"{concept} programming concept explanation"
                    
                    # Simulated search result
                    knowledge = f"[External Knowledge about {concept}]: This is a programming concept..."
                    knowledge_pieces.append(knowledge)
                
                except Exception as e:
                    logger.warning(f"Failed to fetch knowledge for {concept}: {e}")
            
            return "\n\n".join(knowledge_pieces)
        
        except Exception as e:
            logger.warning(f"External knowledge fetch failed: {e}")
            return ""
    
    def _extract_concepts_needing_explanation(
        self,
        intent: str,
        code_analysis: Dict[str, Any]
    ) -> List[str]:
        """
        Extract concepts that might benefit from external explanation.
        
        Args:
            intent: User intent
            code_analysis: Code analysis
            
        Returns:
            List of concepts
        """
        concepts = []
        
        # Technical terms that often need explanation
        technical_terms = [
            'routing', 'middleware', 'authentication', 'authorization',
            'dependency injection', 'state management', 'redux', 'context',
            'hooks', 'lifecycle', 'async', 'promise', 'callback',
            'rest api', 'graphql', 'websocket', 'ssr', 'csr',
            'orm', 'database', 'migration', 'transaction'
        ]
        
        intent_lower = intent.lower()
        
        for term in technical_terms:
            if term in intent_lower:
                concepts.append(term)
        
        return concepts[:3]  # Limit to 3
    
    def _generate_explanation(
        self,
        intent: str,
        code_analysis: Dict[str, Any],
        external_knowledge: str,
        repo_context: Any,
        output_language: str = "english",
    ) -> str:
        """
        Generate comprehensive explanation.
        
        Args:
            intent: User intent
            code_analysis: Code analysis results
            external_knowledge: External knowledge text
            repo_context: Repository context
            
        Returns:
            Detailed explanation
        """
        try:
            # Build context
            context_parts = []
            
            # Repository info
            if repo_context:
                context_parts.append(f"Repository: {repo_context.repo_url}")
                context_parts.append(f"Languages: {', '.join(repo_context.languages.keys())}")
            
            # Code analysis
            if code_analysis.get('code_summary'):
                context_parts.append(f"\nCode Analysis:\n{code_analysis['code_summary']}")
            
            context_parts.append(f"\nFiles Involved: {len(code_analysis['files_involved'])}")
            for file in code_analysis['files_involved'][:5]:
                context_parts.append(f"  - {file}")
            
            # External knowledge
            if external_knowledge:
                context_parts.append(f"\nRelevant Concepts:\n{external_knowledge}")
            
            context = "\n".join(context_parts)

            language_name = {
                "english": "English",
                "hindi": "Hindi",
                "telugu": "Telugu",
            }.get(output_language, "English")
            
            # Generate explanation
            prompt = f"""You are an expert code explainer. Provide a detailed, comprehensive explanation like ChatGPT/Claude would.

User Question: "{intent}"

Context:
{context}

Provide a detailed explanation that:
1. Directly answers the user's question
2. Explains HOW it's implemented in this codebase
3. Explains WHY this approach is used
4. Provides code examples from the codebase
5. Explains any relevant concepts or patterns
6. Mentions best practices or alternatives if relevant
7. Add one concise culturally relevant Indian analogy (chai stall/cricket/railways/etc.) when it helps understanding

Output language requirement:
- Write the explanation in {language_name}
- Keep code/file names unchanged in original form

Be thorough, clear, and educational. Use markdown formatting.

Explanation:"""
            
            explanation = self.orchestrator.generate_completion(prompt, max_tokens=1500)
            
            return explanation.strip()
        
        except Exception as e:
            logger.error(f"Explanation generation failed: {e}")
            return f"I found relevant code but encountered an error generating the explanation: {str(e)}"
