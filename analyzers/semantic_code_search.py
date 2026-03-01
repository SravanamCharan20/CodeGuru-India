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
    LOW_SIGNAL_KEYWORDS = {
        "system",
        "implementation",
        "implement",
        "implemented",
        "use",
        "used",
        "using",
        "explain",
        "about",
        "overview",
        "details",
        "detail",
        "code",
        "codebase",
        "repo",
        "repository",
        "project",
        "application",
        "app",
        "feature",
        "features",
        "file",
        "files",
        "module",
        "modules",
        "functionality",
        "purpose",
        "works",
        "working",
    }
    
    def __init__(self, langchain_orchestrator):
        """
        Initialize semantic search engine.
        
        Args:
            langchain_orchestrator: LangChainOrchestrator for AI operations
        """
        self.orchestrator = langchain_orchestrator
        self.code_chunks = []
        self.file_summaries = {}
        self.rerank_cache: Dict[Tuple[str, Tuple[str, ...]], Dict[int, int]] = {}

    def clear_index(self) -> None:
        """Clear indexed chunks and summaries."""
        self.code_chunks = []
        self.file_summaries = {}
        self.rerank_cache = {}
    
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

            query_mode = self._classify_query_mode(user_intent)
            strict_mode = self._is_strict_mode(query_mode)
            
            # Use AI to score relevance
            relevant_chunks = self._score_chunks_with_ai(user_intent, self.code_chunks, top_k)
            
            logger.info(f"Found {len(relevant_chunks)} relevant chunks")
            
            # If no chunks found, return top chunks only for non-strict broad modes.
            if not relevant_chunks and self.code_chunks:
                if strict_mode:
                    logger.warning("No grounded chunks found for strict query mode")
                    return []
                logger.warning("No relevant chunks found, returning top chunks")
                relevant_chunks = self.code_chunks[:min(top_k, len(self.code_chunks))]
                for chunk in relevant_chunks:
                    chunk.relevance_score = 0.5
            
            return relevant_chunks
        
        except Exception as e:
            logger.error(f"Semantic search failed: {e}", exc_info=True)
            return []

    def assess_grounding(self, user_intent: str, chunks: List[CodeChunk]) -> Dict[str, Any]:
        """
        Assess whether retrieved chunks are strongly grounded for the query.

        Returns:
            Dict with grounding flags and diagnostics.
        """
        query_mode = self._classify_query_mode(user_intent)
        strict_mode = self._is_strict_mode(query_mode)
        keywords = self._extract_keywords(user_intent)
        anchor_terms = self._extract_anchor_terms(keywords, user_intent)

        if not chunks:
            return {
                "is_grounded": False,
                "query_mode": query_mode,
                "top_score": 0.0,
                "anchor_terms": anchor_terms,
                "anchor_coverage": 0,
                "reason": "no_chunks",
            }

        top_score = max(float(chunk.relevance_score or 0.0) for chunk in chunks)
        anchor_coverage = 0
        if anchor_terms:
            expanded = self._expand_query_keywords(anchor_terms)
            coverage = set()
            for chunk in chunks:
                content_lower = chunk.content.lower()
                path_lower = chunk.file_path.lower()
                for term in expanded:
                    if term and (term in content_lower or term in path_lower):
                        coverage.add(term)
            anchor_coverage = len(coverage)

        min_score = 1.2 if strict_mode else 0.6
        has_min_score = top_score >= min_score
        has_anchor = (anchor_coverage >= 1) if (strict_mode and anchor_terms) else True
        is_grounded = bool(has_min_score and has_anchor)

        reason = "ok"
        if not has_min_score:
            reason = "low_score"
        elif not has_anchor:
            reason = "missing_anchor"

        return {
            "is_grounded": is_grounded,
            "query_mode": query_mode,
            "top_score": top_score,
            "anchor_terms": anchor_terms,
            "anchor_coverage": anchor_coverage,
            "reason": reason,
        }
    
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
            anchor_terms = self._extract_anchor_terms(keywords, intent)
            logger.info(f"Extracted keywords: {keywords}")
            logger.info(f"Anchor terms: {anchor_terms}")
            strict_mode = self._is_strict_mode(query_mode)

            scored_chunks = []
            for chunk in chunks:
                score = self._compute_chunk_score(
                    chunk=chunk,
                    keywords=keywords,
                    anchor_terms=anchor_terms,
                    strict_mode=strict_mode,
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

            if strict_mode and anchor_terms:
                scored_chunks = [
                    chunk for chunk in scored_chunks
                    if self._anchor_hits_for_chunk(chunk, anchor_terms) > 0
                ]

            if not scored_chunks:
                if query_is_overview or query_is_comparison or query_is_config:
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

                logger.warning("No grounded matches for strict query mode")
                return []

            scored_chunks.sort(key=lambda x: x.relevance_score, reverse=True)
            if self._should_use_llm_rerank(query_mode, len(scored_chunks)):
                scored_chunks = self._apply_llm_rerank(
                    intent=intent,
                    scored_chunks=scored_chunks,
                    top_k=top_k,
                )

            if strict_mode and scored_chunks[0].relevance_score < 1.2:
                logger.warning(
                    "Top relevance score %.2f is below strict threshold; returning no match",
                    scored_chunks[0].relevance_score,
                )
                return []

            top_score = scored_chunks[0].relevance_score
            min_kept_score = max(0.9 if strict_mode else 0.35, top_score * (0.32 if strict_mode else 0.22))
            scored_chunks = [chunk for chunk in scored_chunks if chunk.relevance_score >= min_kept_score]

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
        anchor_terms: List[str],
        strict_mode: bool,
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

        anchor_hits_path, anchor_hits_content = self._anchor_hit_counts(
            path_lower=path_lower,
            content_lower=content_lower,
            anchor_terms=anchor_terms,
        )
        score += anchor_hits_content * 2.0
        score += anchor_hits_path * 1.3
        if strict_mode and anchor_terms and (anchor_hits_path + anchor_hits_content == 0):
            score -= 1.8

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

    def _is_strict_mode(self, query_mode: str) -> bool:
        """Modes where precision is preferred over broad fallback."""
        return query_mode in {"specific", "location"}

    def _extract_anchor_terms(self, keywords: List[str], intent: str) -> List[str]:
        """Extract high-signal anchor terms from query keywords and explicit entities."""
        anchors: List[str] = []
        seen = set()

        def add_term(term: str) -> None:
            normalized = term.strip().lower().strip("`'\".,:;()[]{}")
            if not normalized or len(normalized) <= 2:
                return
            if normalized in self.LOW_SIGNAL_KEYWORDS:
                return
            if normalized in seen:
                return
            seen.add(normalized)
            anchors.append(normalized)

        for keyword in keywords:
            add_term(keyword)

        for token in re.findall(r"`([^`]+)`", intent or ""):
            add_term(token)

        for token in re.findall(r'"([^"]+)"|\'([^\']+)\'', intent or ""):
            for candidate in token:
                if candidate:
                    add_term(candidate)

        for route in re.findall(r"/[A-Za-z0-9_:/-]+", intent or ""):
            add_term(route)
            for part in re.split(r"[/:-]", route):
                add_term(part)

        for token in re.findall(r"[A-Za-z_][A-Za-z0-9_./:-]{2,}", intent or ""):
            lowered = token.lower()
            is_code_like = (
                "/" in token
                or "." in token
                or "_" in token
                or ":" in token
                or any(char.isupper() for char in token[1:])
            )
            if is_code_like and lowered not in self.LOW_SIGNAL_KEYWORDS:
                add_term(lowered)

        return anchors[:10]

    def _anchor_hit_counts(
        self,
        path_lower: str,
        content_lower: str,
        anchor_terms: List[str],
    ) -> Tuple[int, int]:
        """Count anchor matches in path/content for scoring."""
        if not anchor_terms:
            return (0, 0)

        expanded = self._expand_query_keywords(anchor_terms)
        path_hits = 0
        content_hits = 0

        for term in expanded:
            if not term:
                continue
            if term in path_lower:
                path_hits += 1
            if term in content_lower:
                content_hits += 1

        return (path_hits, content_hits)

    def _anchor_hits_for_chunk(self, chunk: CodeChunk, anchor_terms: List[str]) -> int:
        """Return total anchor hits for a chunk."""
        path_hits, content_hits = self._anchor_hit_counts(
            path_lower=chunk.file_path.lower(),
            content_lower=chunk.content.lower(),
            anchor_terms=anchor_terms,
        )
        return path_hits + content_hits

    def _should_use_llm_rerank(self, query_mode: str, candidate_count: int) -> bool:
        """Decide whether to run lightweight LLM reranking."""
        if candidate_count < 2:
            return False
        if not self.orchestrator or not hasattr(self.orchestrator, "generate_completion"):
            return False
        return query_mode in {"specific", "location", "debug", "comparison"}

    def _apply_llm_rerank(
        self,
        intent: str,
        scored_chunks: List[CodeChunk],
        top_k: int,
    ) -> List[CodeChunk]:
        """Apply LLM-based direct-answer reranking on top candidates."""
        if not scored_chunks:
            return scored_chunks

        candidate_limit = min(len(scored_chunks), max(6, top_k * 2))
        candidates = scored_chunks[:candidate_limit]
        candidate_signature = tuple(
            f"{chunk.file_path}:{chunk.start_line}:{chunk.end_line}"
            for chunk in candidates
        )
        cache_key = (intent.strip().lower(), candidate_signature)
        ranking = self.rerank_cache.get(cache_key)

        if ranking is None:
            prompt = self._build_rerank_prompt(intent, candidates)
            try:
                try:
                    response = self.orchestrator.generate_completion(
                        prompt,
                        max_tokens=320,
                        temperature=0.0,
                    )
                except TypeError:
                    response = self.orchestrator.generate_completion(
                        prompt,
                        max_tokens=320,
                    )
                ranking = self._parse_rerank_response(str(response or ""), len(candidates))
            except Exception as exc:
                logger.warning(f"LLM reranking failed, using deterministic ranking: {exc}")
                ranking = {}
            self.rerank_cache[cache_key] = ranking

        if not ranking:
            return scored_chunks

        for index, chunk in enumerate(candidates, start=1):
            llm_score = ranking.get(index)
            if llm_score is None:
                continue
            llm_norm = max(0.0, min(1.0, llm_score / 100.0))
            # Keep deterministic relevance as primary signal; use reranker as adjustment.
            chunk.relevance_score = max(
                0.0,
                float(chunk.relevance_score) + ((llm_norm - 0.5) * 1.6),
            )

        scored_chunks.sort(key=lambda item: item.relevance_score, reverse=True)
        return scored_chunks

    def _build_rerank_prompt(self, intent: str, candidates: List[CodeChunk]) -> str:
        """Build compact prompt for direct-answer snippet reranking."""
        lines = [
            "Rank repository snippets for direct answer relevance.",
            f'User question: "{intent}"',
            "",
            "Rules:",
            "- Higher score if snippet directly answers the question.",
            "- Prefer explicit entity/route/function matches.",
            "- Penalize generic setup/config snippets.",
            "- Do not infer beyond snippet text.",
            "- Output ONLY lines in format: ID|SCORE|REASON",
            "- SCORE must be an integer between 0 and 100.",
            "",
            "Candidates:",
        ]

        for idx, chunk in enumerate(candidates, start=1):
            excerpt = re.sub(r"\s+", " ", chunk.content or "").strip()[:220]
            lines.append(
                f"{idx}|{chunk.file_path}:{chunk.start_line}-{chunk.end_line}|{excerpt}"
            )

        return "\n".join(lines)

    def _parse_rerank_response(self, response: str, max_id: int) -> Dict[int, int]:
        """Parse reranker output lines into {candidate_id: score}."""
        if not response:
            return {}
        if response.lower().startswith("error generating response"):
            return {}

        ranking: Dict[int, int] = {}
        line_pattern = re.compile(r"^\s*(\d+)\s*\|\s*(-?\d{1,3})\b")

        for line in response.splitlines():
            match = line_pattern.match(line.strip())
            if not match:
                continue
            candidate_id = int(match.group(1))
            if candidate_id < 1 or candidate_id > max_id:
                continue
            score = int(match.group(2))
            ranking[candidate_id] = max(0, min(100, score))

        return ranking

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
