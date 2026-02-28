"""
Semantic Code Search using AI embeddings and similarity matching.

This module provides intelligent code search capabilities to find relevant files
based on user intent, not just keyword matching.
"""

import logging
import os
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
import json

logger = logging.getLogger(__name__)


@dataclass
class CodeChunk:
    """Represents a chunk of code with metadata."""
    file_path: str
    content: str
    start_line: int
    end_line: int
    language: str
    chunk_type: str  # 'class', 'function', 'module', 'block'
    name: str
    relevance_score: float = 0.0


class SemanticCodeSearch:
    """Semantic search engine for code repositories."""
    
    def __init__(self, langchain_orchestrator):
        """
        Initialize semantic search engine.
        
        Args:
            langchain_orchestrator: LangChainOrchestrator for AI operations
        """
        self.orchestrator = langchain_orchestrator
        self.code_chunks = []
        self.file_summaries = {}

    def clear_index(self) -> None:
        """Clear indexed chunks and summaries."""
        self.code_chunks = []
        self.file_summaries = {}
    
    def index_repository(self, repo_path: str, repo_analysis) -> None:
        """
        Index entire repository for semantic search.
        
        Args:
            repo_path: Path to repository
            repo_analysis: RepoAnalysis object
        """
        try:
            logger.info(f"Indexing repository: {repo_path}")
            
            self.code_chunks = []
            self.file_summaries = {}
            
            # Get all code files
            all_files = []
            for files in repo_analysis.file_tree.values():
                all_files.extend(files)
            
            # Process each file
            for file_info in all_files:
                try:
                    file_path = os.path.join(repo_path, file_info.path)
                    
                    if not os.path.isfile(file_path):
                        continue
                    
                    # Read file content
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Chunk the file
                    chunks = self._chunk_file(file_info.path, content, file_info.extension)
                    self.code_chunks.extend(chunks)
                    
                    # Generate file summary
                    summary = self._generate_file_summary(file_info.path, content)
                    self.file_summaries[file_info.path] = summary
                
                except Exception as e:
                    logger.warning(f"Failed to index file {file_info.path}: {e}")
                    continue
            
            logger.info(f"Indexed {len(self.code_chunks)} code chunks from {len(self.file_summaries)} files")
        
        except Exception as e:
            logger.error(f"Repository indexing failed: {e}")
    
    def search_by_intent(
        self,
        user_intent: str,
        top_k: int = 20
    ) -> List[CodeChunk]:
        """
        Search for relevant code chunks based on user intent.
        
        Args:
            user_intent: User's natural language query
            top_k: Number of top results to return
            
        Returns:
            List of relevant code chunks with scores
        """
        try:
            logger.info(f"Searching for intent: {user_intent}")
            logger.info(f"Total indexed chunks: {len(self.code_chunks)}")
            
            if not self.code_chunks:
                logger.warning("No code chunks indexed")
                return []
            
            # Use AI to score relevance
            relevant_chunks = self._score_chunks_with_ai(user_intent, self.code_chunks, top_k)
            
            logger.info(f"Found {len(relevant_chunks)} relevant chunks")
            
            # If no chunks found, return top chunks anyway
            if not relevant_chunks and self.code_chunks:
                logger.warning("No relevant chunks found, returning top chunks")
                relevant_chunks = self.code_chunks[:min(top_k, len(self.code_chunks))]
                for chunk in relevant_chunks:
                    chunk.relevance_score = 0.5
            
            return relevant_chunks
        
        except Exception as e:
            logger.error(f"Semantic search failed: {e}", exc_info=True)
            return []
    
    def get_relevant_files(
        self,
        user_intent: str,
        top_k: int = 10
    ) -> List[Tuple[str, float, str]]:
        """
        Get relevant files based on intent.
        
        Args:
            user_intent: User's natural language query
            top_k: Number of files to return
            
        Returns:
            List of (file_path, relevance_score, summary) tuples
        """
        try:
            # Score files based on summaries
            file_scores = []
            
            for file_path, summary in self.file_summaries.items():
                score = self._calculate_relevance(user_intent, summary)
                file_scores.append((file_path, score, summary))
            
            # Sort by score
            file_scores.sort(key=lambda x: x[1], reverse=True)
            
            return file_scores[:top_k]
        
        except Exception as e:
            logger.error(f"File relevance calculation failed: {e}")
            return []
    
    def _chunk_file(
        self,
        file_path: str,
        content: str,
        extension: str
    ) -> List[CodeChunk]:
        """
        Split file into semantic chunks.
        
        Args:
            file_path: Path to file
            content: File content
            extension: File extension
            
        Returns:
            List of code chunks
        """
        chunks = []
        
        # Simple line-based chunking (can be enhanced with AST parsing)
        lines = content.split('\n')
        chunk_size = 50  # lines per chunk
        
        for i in range(0, len(lines), chunk_size):
            chunk_lines = lines[i:i + chunk_size]
            chunk_content = '\n'.join(chunk_lines)
            
            if chunk_content.strip():
                chunk = CodeChunk(
                    file_path=file_path,
                    content=chunk_content,
                    start_line=i + 1,
                    end_line=min(i + chunk_size, len(lines)),
                    language=self._get_language(extension),
                    chunk_type='block',
                    name=f"{file_path}:{i+1}-{min(i+chunk_size, len(lines))}"
                )
                chunks.append(chunk)
        
        return chunks
    
    def _generate_file_summary(self, file_path: str, content: str) -> str:
        """
        Generate AI summary of file.
        
        Args:
            file_path: Path to file
            content: File content
            
        Returns:
            Summary string
        """
        try:
            # Truncate content if too long
            max_chars = 3000
            truncated_content = content[:max_chars]
            
            prompt = f"""Analyze this code file and provide a brief summary (2-3 sentences) of what it does:

File: {file_path}

Code:
```
{truncated_content}
```

Summary:"""
            
            summary = self.orchestrator.generate_completion(prompt, max_tokens=150)
            return summary.strip()
        
        except Exception as e:
            logger.warning(f"Failed to generate summary for {file_path}: {e}")
            return f"Code file: {file_path}"
    
    def _score_chunks_with_ai(
        self,
        intent: str,
        chunks: List[CodeChunk],
        top_k: int
    ) -> List[CodeChunk]:
        """
        Score chunks using AI for relevance.
        
        Args:
            intent: User intent
            chunks: List of code chunks
            top_k: Number to return
            
        Returns:
            Top k relevant chunks
        """
        try:
            logger.info(f"Scoring {len(chunks)} chunks for intent: {intent}")
            
            # For efficiency, first filter with keyword matching
            keywords = self._extract_keywords(intent)
            logger.info(f"Extracted keywords: {keywords}")
            
            filtered_chunks = []
            
            for chunk in chunks:
                score = 0.0
                content_lower = chunk.content.lower()
                
                for keyword in keywords:
                    if keyword.lower() in content_lower:
                        score += 1.0
                
                # Include chunks with any keyword match or top chunks
                if score > 0:
                    chunk.relevance_score = score
                    filtered_chunks.append(chunk)
            
            logger.info(f"Filtered to {len(filtered_chunks)} chunks with keyword matches")
            
            # If no matches, use all chunks
            if not filtered_chunks:
                logger.warning("No keyword matches, using all chunks")
                filtered_chunks = chunks
                for chunk in filtered_chunks:
                    chunk.relevance_score = 0.1
            
            # Sort by initial score
            filtered_chunks.sort(key=lambda x: x.relevance_score, reverse=True)
            
            # Take top candidates
            candidates = filtered_chunks[:min(top_k, len(filtered_chunks))]
            
            logger.info(f"Returning {len(candidates)} candidates")
            return candidates
        
        except Exception as e:
            logger.error(f"AI scoring failed: {e}", exc_info=True)
            # Fallback to first chunks
            logger.warning("Falling back to first chunks")
            return chunks[:top_k] if chunks else []
    
    def _calculate_relevance(self, intent: str, content: str) -> float:
        """
        Calculate relevance score between intent and content.
        
        Args:
            intent: User intent
            content: Code content
            
        Returns:
            Relevance score (0-1)
        """
        try:
            # Simple keyword-based scoring (can be enhanced with embeddings)
            keywords = self._extract_keywords(intent)
            content_lower = content.lower()
            
            matches = sum(1 for kw in keywords if kw.lower() in content_lower)
            score = min(matches / max(len(keywords), 1), 1.0)
            
            return score
        
        except Exception as e:
            logger.warning(f"Relevance calculation failed: {e}")
            return 0.0
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract keywords from text.
        
        Args:
            text: Input text
            
        Returns:
            List of keywords
        """
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might', 'must', 'can', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who', 'when', 'where', 'why', 'how'}
        
        words = text.lower().split()
        keywords = [w.strip('.,!?;:()[]{}') for w in words if w.lower() not in stop_words and len(w) > 2]
        
        return keywords
    
    def _get_language(self, extension: str) -> str:
        """Get language from file extension."""
        lang_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rb': 'ruby'
        }
        return lang_map.get(extension, 'text')
