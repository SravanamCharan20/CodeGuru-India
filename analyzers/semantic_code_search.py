"""
Semantic Code Search using AI embeddings and similarity matching.

This module provides intelligent code search capabilities to find relevant files
based on user intent, not just keyword matching.
"""

import logging
import os
import re
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

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

    OVERVIEW_PATTERNS = (
        "key feature",
        "main feature",
        "major feature",
        "what are the features",
        "key features are",
        "feature of this codebase",
        "what this codebase does",
        "what does this app do",
        "overall functionality",
        "high level",
        "overview",
        "capabilities",
    )
    CONFIG_PATTERNS = (
        "config",
        "configuration",
        "environment",
        "env",
        "build",
        "webpack",
        "vite",
        "tsconfig",
        "package json",
        "deployment",
    )
    LOCATION_PATTERNS = (
        "which file",
        "where is",
        "where are",
        "where does",
        "defined in",
        "implemented in",
        "located",
        "location",
    )
    COMPARISON_PATTERNS = (
        "compare",
        "difference",
        "different",
        "vs",
        "versus",
        "better than",
        "contrast",
    )
    DEBUG_PATTERNS = (
        "error",
        "bug",
        "issue",
        "not working",
        "failing",
        "fails",
        "fix",
        "exception",
        "traceback",
        "crash",
    )
    NOISE_FILE_HINTS = (
        "config",
        "settings",
        "constant",
        "types",
        "schema",
        ".env",
        "package.json",
        "tsconfig",
        "webpack",
        "vite",
        "babel",
        "eslint",
        "prettier",
    )
    FEATURE_FILE_HINTS = (
        "router",
        "route",
        "page",
        "component",
        "screen",
        "view",
        "layout",
        "service",
        "api",
        "controller",
        "store",
        "state",
        "hook",
    )
    
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
            query_mode = self._classify_query_mode(intent)
            query_is_config = query_mode == "config"
            query_is_overview = query_mode == "overview"
            query_is_location = query_mode == "location"
            query_is_comparison = query_mode == "comparison"
            query_is_debug = query_mode == "debug"
            logger.info(f"Detected query mode: {query_mode}")

            keywords = self._extract_keywords(intent)
            logger.info(f"Extracted keywords: {keywords}")

            scored_chunks = []
            for chunk in chunks:
                score = self._compute_chunk_score(
                    chunk=chunk,
                    keywords=keywords,
                    query_is_config=query_is_config,
                    query_is_overview=query_is_overview,
                    query_is_location=query_is_location,
                    query_is_comparison=query_is_comparison,
                    query_is_debug=query_is_debug,
                )
                if score <= 0:
                    continue
                chunk.relevance_score = score
                scored_chunks.append(chunk)

            if not scored_chunks:
                logger.warning("No high-confidence matches found, using heuristic fallback")
                fallback = self._fallback_chunks(
                    chunks=chunks,
                    top_k=top_k,
                    query_is_config=query_is_config,
                    query_is_overview=query_is_overview,
                    query_is_location=query_is_location,
                    query_is_comparison=query_is_comparison,
                    query_is_debug=query_is_debug,
                )
                for rank, chunk in enumerate(fallback, start=1):
                    chunk.relevance_score = max(0.1, 1.0 - rank * 0.01)
                return fallback

            scored_chunks.sort(key=lambda x: x.relevance_score, reverse=True)
            per_file_limit = 1 if (query_is_overview or query_is_comparison) else 2
            candidates = self._select_diverse_chunks(scored_chunks, top_k=top_k, per_file_limit=per_file_limit)
            logger.info(f"Returning {len(candidates)} candidates")
            return candidates
        
        except Exception as e:
            logger.error(f"AI scoring failed: {e}", exc_info=True)
            # Fallback to first chunks
            logger.warning("Falling back to first chunks")
            return chunks[:top_k] if chunks else []

    def _compute_chunk_score(
        self,
        chunk: CodeChunk,
        keywords: List[str],
        query_is_config: bool,
        query_is_overview: bool,
        query_is_location: bool,
        query_is_comparison: bool,
        query_is_debug: bool,
    ) -> float:
        """Compute weighted relevance score for a chunk."""
        content_lower = chunk.content.lower()
        path_lower = chunk.file_path.lower()

        score = 0.0
        keyword_hits = 0
        for keyword in keywords:
            if keyword in content_lower:
                keyword_hits += 1
            if keyword in path_lower:
                score += 0.8

        score += keyword_hits * 1.6

        # Prefer central app files when query is broad/overview.
        feature_signal = self._feature_signal_score(content_lower, path_lower)
        if query_is_overview:
            score += feature_signal
            score += self._entry_file_score(path_lower)
            # Penalize chunks that are broad but lack user-facing feature signals.
            if feature_signal < 0.8:
                score -= 0.7
        else:
            score += self._entry_file_score(path_lower) * 0.4

        if query_is_location:
            score += self._location_signal_score(content_lower, path_lower, keywords)
        if query_is_comparison:
            score += feature_signal * 0.6
            if keyword_hits >= 2:
                score += 0.8
        if query_is_debug:
            score += self._debug_signal_score(content_lower, path_lower)

        if not query_is_config:
            score -= self._noise_penalty(path_lower, content_lower)
            if query_is_overview and any(token in path_lower for token in self.NOISE_FILE_HINTS):
                score -= 0.8
        else:
            # For config questions, noise files become relevant.
            if any(token in path_lower for token in self.NOISE_FILE_HINTS):
                score += 1.4

        if query_is_overview and "path" in content_lower:
            score += 0.6
        if query_is_overview and ("fetch(" in content_lower or "axios" in content_lower):
            score += 0.6
        if query_is_overview and ("usestate" in content_lower or "redux" in content_lower or "context" in content_lower):
            score += 0.5

        return max(0.0, score)

    def _classify_query_mode(self, intent: str) -> str:
        """Classify query into retrieval mode."""
        query = intent.lower()
        if any(pattern in query for pattern in self.CONFIG_PATTERNS):
            return "config"
        if any(pattern in query for pattern in self.LOCATION_PATTERNS):
            return "location"
        if any(pattern in query for pattern in self.COMPARISON_PATTERNS):
            return "comparison"
        if any(pattern in query for pattern in self.DEBUG_PATTERNS):
            return "debug"
        if any(pattern in query for pattern in self.OVERVIEW_PATTERNS):
            return "overview"
        if "feature" in query and ("what" in query or "which" in query):
            return "overview"
        return "specific"

    def _feature_signal_score(self, content_lower: str, path_lower: str) -> float:
        """Extra score for user-facing behavior and architecture signals."""
        score = 0.0
        if any(token in path_lower for token in self.FEATURE_FILE_HINTS):
            score += 1.2
        if any(token in path_lower for token in ("/pages/", "\\pages\\", "/components/", "\\components\\")):
            score += 1.0
        if any(token in content_lower for token in ("createbrowserrouter", "browserrouter", "<route", "path:", "routerprovider")):
            score += 1.3
        if any(token in content_lower for token in ("lazy(", "suspense", "errorelement")):
            score += 0.8
        if any(token in content_lower for token in ("cart", "menu", "restaurant", "search", "filter", "shimmer")):
            score += 0.9
        return score

    def _entry_file_score(self, path_lower: str) -> float:
        """Boost probable entry points and main UI files."""
        score = 0.0
        entry_names = ("app.", "main.", "index.", "router.", "routes.", "layout.")
        if any(name in os.path.basename(path_lower) for name in entry_names):
            score += 1.0
        if path_lower.endswith((".jsx", ".tsx", ".js", ".ts")):
            score += 0.2
        return score

    def _location_signal_score(self, content_lower: str, path_lower: str, keywords: List[str]) -> float:
        """Boost symbols likely to answer 'where is X implemented' queries."""
        score = 0.0
        expanded_keywords = self._expand_query_keywords(keywords)
        if any(keyword in path_lower for keyword in expanded_keywords):
            score += 1.6
        if any(token in content_lower for token in ("export default", "export const", "export function", "class ", "function ")):
            score += 0.6
        if any(keyword in content_lower for keyword in expanded_keywords):
            score += 0.5
        if any(token in path_lower for token in ("component", "page", "route", "router", "service", "controller", "hook")):
            score += 0.5
        return score

    def _expand_query_keywords(self, keywords: List[str]) -> List[str]:
        """Expand query keywords with light stemming and domain synonyms."""
        expanded = set(keywords)
        synonyms = {
            "routing": {"route", "router"},
            "routes": {"route", "router"},
            "authentication": {"auth", "login", "token"},
            "authorization": {"auth", "role", "permission"},
            "state": {"store", "context", "redux"},
            "loading": {"shimmer", "skeleton", "loader"},
        }
        for keyword in list(expanded):
            if keyword.endswith("ing") and len(keyword) > 5:
                expanded.add(keyword[:-3])
            if keyword.endswith("ed") and len(keyword) > 4:
                expanded.add(keyword[:-2])
            for alias in synonyms.get(keyword, set()):
                expanded.add(alias)
        return list(expanded)

    def _debug_signal_score(self, content_lower: str, path_lower: str) -> float:
        """Boost error-handling and fallback logic for debugging questions."""
        score = 0.0
        if any(token in content_lower for token in ("try:", "except", "try {", "catch", "throw", "raise")):
            score += 1.0
        if any(token in content_lower for token in ("error", "exception", "fallback", "retry", "timeout", "status", "traceback")):
            score += 0.9
        if any(token in path_lower for token in ("error", "exception", "debug", "log", "handler")):
            score += 0.8
        return score

    def _noise_penalty(self, path_lower: str, content_lower: str) -> float:
        """Penalty for boilerplate/config/test files when not explicitly asked."""
        penalty = 0.0
        if any(token in path_lower for token in self.NOISE_FILE_HINTS):
            penalty += 1.4
        if any(token in path_lower for token in ("test", "__tests__", ".spec.", ".test.")):
            penalty += 1.0
        if "eslint" in content_lower or "prettier" in content_lower:
            penalty += 0.6
        return penalty

    def _select_diverse_chunks(self, chunks: List[CodeChunk], top_k: int, per_file_limit: int = 2) -> List[CodeChunk]:
        """Select top chunks while maintaining file diversity."""
        selected: List[CodeChunk] = []
        file_counts: Dict[str, int] = {}

        for chunk in chunks:
            current = file_counts.get(chunk.file_path, 0)
            if current >= per_file_limit:
                continue
            selected.append(chunk)
            file_counts[chunk.file_path] = current + 1
            if len(selected) >= top_k:
                break

        if len(selected) < top_k:
            for chunk in chunks:
                if chunk in selected:
                    continue
                selected.append(chunk)
                if len(selected) >= top_k:
                    break

        return selected

    def _fallback_chunks(
        self,
        chunks: List[CodeChunk],
        top_k: int,
        query_is_config: bool,
        query_is_overview: bool,
        query_is_location: bool,
        query_is_comparison: bool,
        query_is_debug: bool,
    ) -> List[CodeChunk]:
        """Fallback ranking when keyword matching is weak."""
        rescored = []
        for chunk in chunks:
            content_lower = chunk.content.lower()
            path_lower = chunk.file_path.lower()

            score = self._entry_file_score(path_lower)
            if query_is_overview:
                score += self._feature_signal_score(content_lower, path_lower)
            if query_is_location:
                score += self._location_signal_score(content_lower, path_lower, [])
            if query_is_debug:
                score += self._debug_signal_score(content_lower, path_lower)
            if not query_is_config:
                score -= self._noise_penalty(path_lower, content_lower)
            rescored.append((score, chunk))

        rescored.sort(key=lambda item: item[0], reverse=True)
        ordered = [chunk for _, chunk in rescored if _ > -2.0]
        if not ordered:
            ordered = [item[1] for item in rescored]
        per_file_limit = 1 if (query_is_overview or query_is_comparison) else 2
        return self._select_diverse_chunks(ordered, top_k=top_k, per_file_limit=per_file_limit)
    
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
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'should', 'could', 'may', 'might', 'must', 'can', 'i', 'you', 'he',
            'she', 'it', 'we', 'they', 'what', 'which', 'who', 'when', 'where',
            'why', 'how', 'this', 'that', 'these', 'those', 'code', 'codebase',
            'repo', 'repository', 'app', 'key', 'feature', 'features', 'file',
            'files', 'implemented', 'implementation', 'explain'
        }

        tokens = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", text.lower())
        keywords: List[str] = []
        seen = set()

        for token in tokens:
            normalized = token.rstrip("s") if token.endswith("s") and len(token) > 4 else token
            if normalized in stop_words or len(normalized) <= 2:
                continue
            if normalized in seen:
                continue
            seen.add(normalized)
            keywords.append(normalized)

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
