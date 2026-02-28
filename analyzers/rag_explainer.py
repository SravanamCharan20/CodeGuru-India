"""
RAG-Enhanced Code Explainer.

Uses Retrieval-Augmented Generation to provide detailed explanations
with external knowledge when needed.
"""

import logging
import re
from typing import List, Dict, Any, Optional
from analyzers.semantic_code_search import CodeChunk

logger = logging.getLogger(__name__)


class RAGExplainer:
    """Generates detailed explanations using RAG approach."""

    FEATURE_OVERVIEW_PATTERNS = (
        "key feature",
        "main feature",
        "major feature",
        "what features",
        "core features",
        "feature set",
        "what this app does",
        "what this codebase does",
        "overall functionality",
        "capabilities",
        "high level overview",
    )
    NOISE_FILE_HINTS = (
        ".env",
        "config",
        "settings",
        "package.json",
        "tsconfig",
        "webpack",
        "vite",
        "babel",
        "eslint",
        "prettier",
        "jest",
        "test",
        "__tests__",
        ".spec.",
        ".test.",
    )
    FEATURE_RULES = (
        {
            "id": "routing",
            "signals": ("createbrowserrouter", "browserrouter", "routerprovider", "<route", "path:", "useparams"),
            "path_hints": ("router", "route"),
            "weight": 3.2,
            "label": {
                "english": "Routing and Navigation",
                "hindi": "रूटिंग और नेविगेशन",
                "telugu": "రూటింగ్ మరియు నావిగేషన్",
            },
            "why": {
                "english": "Handles multi-page navigation and deep links without full page reload.",
                "hindi": "यह बिना पूरा पेज रीलोड किए नेविगेशन और डीप-लिंकिंग को संभालता है।",
                "telugu": "పేజీని పూర్తిగా రీలోడ్ చేయకుండా నావిగేషన్ మరియు డీప్-లింకింగ్‌ను నిర్వహిస్తుంది.",
            },
        },
        {
            "id": "data_fetching",
            "signals": ("fetch(", "axios", "usequery", "swr", "graphql", "apollo"),
            "path_hints": ("api", "service", "query"),
            "weight": 2.7,
            "label": {
                "english": "Data Fetching Layer",
                "hindi": "डेटा फ़ेचिंग लेयर",
                "telugu": "డేటా ఫెచింగ్ లేయర్",
            },
            "why": {
                "english": "Connects UI to APIs and keeps runtime data updated.",
                "hindi": "यह UI को APIs से जोड़कर रनटाइम डेटा अपडेट रखता है।",
                "telugu": "ఇది UIని APIsతో కలిపి రన్‌టైమ్ డేటాను తాజాగా ఉంచుతుంది.",
            },
        },
        {
            "id": "state_management",
            "signals": ("redux", "configurestore", "createslice", "context", "usecontext", "usestate", "usereducer", "zustand"),
            "path_hints": ("store", "state", "slice"),
            "weight": 2.6,
            "label": {
                "english": "State Management",
                "hindi": "स्टेट मैनेजमेंट",
                "telugu": "స్టేట్ మేనేజ్‌మెంట్",
            },
            "why": {
                "english": "Maintains shared app state and predictable UI behavior.",
                "hindi": "यह साझा ऐप स्टेट को मैनेज करके UI व्यवहार को स्थिर रखता है।",
                "telugu": "ఇది షేర్డ్ యాప్ స్టేట్‌ను నిర్వహించి UI ప్రవర్తనను స్థిరంగా ఉంచుతుంది.",
            },
        },
        {
            "id": "lazy_loading",
            "signals": ("lazy(", "suspense", "dynamic import", "import("),
            "path_hints": ("lazy",),
            "weight": 2.4,
            "label": {
                "english": "Lazy Loading / Code Splitting",
                "hindi": "लेज़ी लोडिंग / कोड स्प्लिटिंग",
                "telugu": "లేజీ లోడింగ్ / కోడ్ స్ప్లిటింగ్",
            },
            "why": {
                "english": "Reduces initial bundle size and speeds up first load.",
                "hindi": "यह शुरुआती बंडल आकार घटाकर शुरुआती लोड तेज करता है।",
                "telugu": "ఇది ప్రారంభ బండిల్ సైజును తగ్గించి మొదటి లోడ్‌ను వేగవంతం చేస్తుంది.",
            },
        },
        {
            "id": "loading_ui",
            "signals": ("shimmer", "skeleton", "loading", "placeholder"),
            "path_hints": ("shimmer", "skeleton", "loader"),
            "weight": 2.2,
            "label": {
                "english": "Loading Experience (Shimmer/Skeleton)",
                "hindi": "लोडिंग अनुभव (शिमर/स्केलेटन)",
                "telugu": "లోడింగ్ అనుభవం (షిమ్మర్/స్కెలెటన్)",
            },
            "why": {
                "english": "Improves perceived performance while data is loading.",
                "hindi": "डेटा लोड होते समय यूज़र को बेहतर अनुभव देता है।",
                "telugu": "డేటా లోడ్ అవుతున్నప్పుడు యూజర్ అనుభవాన్ని మెరుగుపరుస్తుంది.",
            },
        },
        {
            "id": "auth_security",
            "signals": ("auth", "authentication", "authorize", "jwt", "token", "login", "protectedroute"),
            "path_hints": ("auth", "login", "security"),
            "weight": 2.5,
            "label": {
                "english": "Authentication / Access Control",
                "hindi": "ऑथेंटिकेशन / एक्सेस कंट्रोल",
                "telugu": "ఆథెంటికేషన్ / యాక్సెస్ కంట్రోల్",
            },
            "why": {
                "english": "Protects user actions and secures restricted flows.",
                "hindi": "यह सीमित फीचर्स को सुरक्षित रखता है और एक्सेस नियंत्रित करता है।",
                "telugu": "ఇది పరిమిత ఫ్లోలను రక్షించి యాక్సెస్‌ను నియంత్రిస్తుంది.",
            },
        },
        {
            "id": "api_backend",
            "signals": ("router.get", "router.post", "app.get", "app.post", "express", "fastapi", "flask", "@get(", "@post("),
            "path_hints": ("controller", "routes", "api"),
            "weight": 2.5,
            "label": {
                "english": "API / Backend Endpoints",
                "hindi": "API / बैकएंड एंडपॉइंट्स",
                "telugu": "API / బ్యాక్‌ఎండ్ ఎండ్‌పాయింట్స్",
            },
            "why": {
                "english": "Implements server-side business operations and request handling.",
                "hindi": "यह सर्वर-साइड बिज़नेस लॉजिक और रिक्वेस्ट हैंडलिंग लागू करता है।",
                "telugu": "ఇది సర్వర్-సైడ్ బిజినెస్ లాజిక్ మరియు రిక్వెస్ట్ హ్యాండ్లింగ్‌ను అమలు చేస్తుంది.",
            },
        },
        {
            "id": "db_layer",
            "signals": ("prisma", "mongoose", "sequelize", "sqlalchemy", "postgres", "mysql", "sqlite", "mongodb"),
            "path_hints": ("db", "database", "model", "schema"),
            "weight": 2.4,
            "label": {
                "english": "Database Integration",
                "hindi": "डेटाबेस इंटीग्रेशन",
                "telugu": "డేటాబేస్ ఇంటిగ్రేషన్",
            },
            "why": {
                "english": "Stores persistent data and powers core business records.",
                "hindi": "यह डेटा को स्थायी रूप से स्टोर करके मुख्य रिकॉर्ड्स संभालता है।",
                "telugu": "ఇది శాశ్వత డేటాను నిల్వచేసి ప్రధాన రికార్డులను నిర్వహిస్తుంది.",
            },
        },
        {
            "id": "search_filter",
            "signals": ("search", "filter", "debounce", "sort(", "query"),
            "path_hints": ("search", "filter"),
            "weight": 2.1,
            "label": {
                "english": "Search / Filter Experience",
                "hindi": "सर्च / फ़िल्टर अनुभव",
                "telugu": "సెర్చ్ / ఫిల్టర్ అనుభవం",
            },
            "why": {
                "english": "Helps users find relevant content faster.",
                "hindi": "यह यूज़र्स को तेज़ी से सही कंटेंट खोजने में मदद करता है।",
                "telugu": "ఇది యూజర్లకు అవసరమైన కంటెంట్‌ను వేగంగా కనుగొనడంలో సహాయపడుతుంది.",
            },
        },
    )
    
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

            is_feature_overview = self._is_feature_overview_intent(intent)
            scoped_chunks = relevant_chunks
            if is_feature_overview:
                scoped_chunks = self._filter_overview_chunks(relevant_chunks)
                if not scoped_chunks:
                    scoped_chunks = relevant_chunks

            # Step 1: Analyze code chunks
            grounded_snippets = self._build_grounded_snippets(scoped_chunks)
            observed_facts = self._extract_observed_facts(intent, grounded_snippets)

            if is_feature_overview:
                code_analysis = {
                    "total_chunks": len(scoped_chunks),
                    "files_involved": list({chunk.file_path for chunk in scoped_chunks}),
                    "code_summary": "",
                    "key_patterns": [],
                    "technologies": [],
                }
            else:
                code_analysis = self._analyze_code_chunks(scoped_chunks)

            # Step 2: Get external knowledge if needed
            external_knowledge = ""
            if use_web_search and self.web_search_available and not is_feature_overview:
                external_knowledge = self._fetch_external_knowledge(intent, code_analysis)

            # Step 3: Generate comprehensive explanation
            if is_feature_overview:
                explanation = self._generate_feature_overview_from_snippets(
                    grounded_snippets,
                    output_language=output_language,
                )
                if not explanation:
                    explanation = self._generate_explanation(
                        intent,
                        code_analysis,
                        external_knowledge,
                        repo_context,
                        grounded_snippets,
                        observed_facts,
                        output_language=output_language,
                    )
            else:
                explanation = self._generate_explanation(
                    intent,
                    code_analysis,
                    external_knowledge,
                    repo_context,
                    grounded_snippets,
                    observed_facts,
                    output_language=output_language,
                )

            explanation = self._strip_code_blocks(explanation)
            explanation = self._apply_fact_corrections(
                explanation,
                intent,
                grounded_snippets,
            )
            explanation = self._remove_unsupported_code_entities(
                explanation,
                grounded_snippets,
                intent,
                output_language,
            )
            evidence_section = self._format_evidence_section(
                grounded_snippets,
                output_language,
                compact=is_feature_overview,
            )
            if evidence_section:
                explanation = f"{explanation.strip()}\n\n{evidence_section}".strip()
            
            return {
                'intent': intent,
                'explanation': explanation,
                'code_references': [
                    {
                        'file': chunk.file_path,
                        'lines': f"{chunk.start_line}-{chunk.end_line}",
                        'content': chunk.content[:500]  # Preview
                    }
                    for chunk in scoped_chunks[:5]
                ],
                'external_sources': external_knowledge != "",
                'confidence': 'high' if len(scoped_chunks) > 3 else 'medium'
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
        grounded_snippets: List[Dict[str, Any]],
        observed_facts: List[str],
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

            context_parts.append(f"\nFiles Involved: {len(code_analysis['files_involved'])}")
            for file in code_analysis['files_involved'][:8]:
                context_parts.append(f"  - {file}")

            if observed_facts:
                context_parts.append("\nObserved Facts from Retrieved Code:")
                for fact in observed_facts:
                    context_parts.append(f"- {fact}")

            if grounded_snippets:
                context_parts.append("\nRetrieved Code Evidence:")
                for idx, snippet in enumerate(grounded_snippets[:6], start=1):
                    context_parts.append(
                        f"[Snippet {idx}] {snippet['file_path']}:{snippet['start_line']}-{snippet['end_line']}\n"
                        f"{snippet['snippet']}"
                    )
            
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
            prompt = f"""You are an expert code explainer. Provide a detailed and accurate explanation.

User Question: "{intent}"

Context:
{context}

Strict grounding rules (must follow):
1. Use ONLY the retrieved code evidence and observed facts above.
2. Do NOT invent any files, APIs, routes, components, or code.
3. If the evidence is insufficient, explicitly say: "Not found in retrieved snippets."
4. Do NOT generate new code examples. If mentioning code, quote exact tokens/snippets from evidence.
5. Prefer file-path and line references over hypothetical examples.
6. Wrap every code entity (file path, route path, function/class/component/hook/API name) in backticks.

Provide an explanation that:
1. Directly answers the user's question
2. Explains HOW it's implemented in this codebase
3. Explains WHY this approach is used
4. Explains relevant concepts/patterns grounded in evidence
5. Mentions alternatives only as brief comparison without writing alternative code
6. Add one concise culturally relevant Indian analogy (chai stall/cricket/railways/etc.) only if it helps understanding

Output language requirement:
- Write the explanation in {language_name}
- Keep code/file names unchanged in original form

Be clear and educational. Use markdown formatting.

Explanation:"""
            
            explanation = self.orchestrator.generate_completion(prompt, max_tokens=1500)
            
            return explanation.strip()
        
        except Exception as e:
            logger.error(f"Explanation generation failed: {e}")
            return f"I found relevant code but encountered an error generating the explanation: {str(e)}"

    def _build_grounded_snippets(self, chunks: List[CodeChunk], max_snippets: int = 6) -> List[Dict[str, Any]]:
        """Build sanitized evidence snippets from retrieved chunks."""
        snippets: List[Dict[str, Any]] = []

        for chunk in chunks[: max_snippets * 2]:
            content = (chunk.content or "").strip()
            if not content:
                continue

            normalized = re.sub(r"\n{3,}", "\n\n", content)
            preview = normalized[:900]
            snippets.append(
                {
                    "file_path": chunk.file_path,
                    "start_line": chunk.start_line,
                    "end_line": chunk.end_line,
                    "snippet": preview,
                }
            )
            if len(snippets) >= max_snippets:
                break

        return snippets

    def _extract_observed_facts(
        self,
        intent: str,
        grounded_snippets: List[Dict[str, Any]],
    ) -> List[str]:
        """Extract deterministic facts directly from retrieved snippets."""
        joined = "\n".join(item.get("snippet", "") for item in grounded_snippets)
        joined_lower = joined.lower()
        facts: List[str] = []

        if not joined:
            return facts

        if "createbrowserrouter" in joined_lower:
            facts.append("Detected `createBrowserRouter` usage from `react-router-dom`.")
        if re.search(r"\bbrowserrouter\b", joined_lower):
            facts.append("Detected `BrowserRouter` component usage.")
        if "routerprovider" in joined_lower:
            facts.append("Detected `RouterProvider` usage.")
        if "routes" in joined_lower and "route" in joined_lower:
            facts.append("Detected route definitions using `Routes` / `Route`.")
        if "lazy(" in joined_lower or "lazy(()" in joined_lower:
            facts.append("Detected lazy loading via `lazy()`.")
        if "suspense" in joined_lower:
            facts.append("Detected `Suspense` fallback handling.")
        if "/:" in joined:
            facts.append("Detected dynamic route parameter(s) (e.g., `:id`).")

        intent_lower = intent.lower()
        is_routing_query = any(token in intent_lower for token in ("route", "routing", "router"))
        if is_routing_query and not facts:
            facts.append("Routing implementation details are not explicit in retrieved snippets.")

        return facts

    def _strip_code_blocks(self, text: str) -> str:
        """Remove model-generated fenced code blocks to prevent synthetic examples."""
        if not text:
            return text
        return re.sub(r"```[\s\S]*?```", "", text).strip()

    def _apply_fact_corrections(
        self,
        explanation: str,
        intent: str,
        grounded_snippets: List[Dict[str, Any]],
    ) -> str:
        """
        Apply small deterministic corrections for known hallucination patterns.
        """
        if not explanation:
            return explanation

        intent_lower = intent.lower()
        is_routing_query = any(token in intent_lower for token in ("route", "routing", "router"))
        if not is_routing_query:
            return explanation

        source = "\n".join(item.get("snippet", "") for item in grounded_snippets)
        source_lower = source.lower()
        has_create = "createbrowserrouter" in source_lower
        has_browser = re.search(r"\bbrowserrouter\b", source_lower) is not None

        corrected = explanation
        if has_create and not has_browser:
            corrected = re.sub(r"\bBrowserRouter\b", "createBrowserRouter", corrected)
        elif has_browser and not has_create:
            corrected = re.sub(r"\bcreateBrowserRouter\b", "BrowserRouter", corrected)

        return corrected

    def _remove_unsupported_code_entities(
        self,
        explanation: str,
        grounded_snippets: List[Dict[str, Any]],
        intent: str,
        output_language: str,
    ) -> str:
        """Remove answer lines that reference code entities not found in retrieved evidence."""
        if not explanation:
            return explanation

        supported_tokens, supported_paths, supported_basenames = self._extract_supported_entities(grounded_snippets)
        supported_tokens.update(self._extract_query_entities(intent))
        supported_tokens.update({
            "react", "react-router-dom", "javascript", "typescript", "python",
            "node", "api", "http", "css", "html",
        })

        removed_any = False
        cleaned_lines: List[str] = []

        for line in explanation.splitlines():
            if self._line_has_unsupported_backtick_token(line, supported_tokens):
                removed_any = True
                continue
            if self._line_has_unsupported_path(line, supported_paths, supported_basenames):
                removed_any = True
                continue
            cleaned_lines.append(line)

        cleaned = "\n".join(cleaned_lines).strip()
        if not cleaned:
            cleaned = self._not_found_message(output_language)

        if removed_any:
            cleaned = f"{cleaned}\n\n{self._unsupported_filtered_note(output_language)}".strip()

        return cleaned

    def _extract_supported_entities(
        self,
        grounded_snippets: List[Dict[str, Any]],
    ) -> tuple[set[str], set[str], set[str]]:
        """Build supported entity sets from retrieved snippets."""
        tokens: set[str] = set()
        paths: set[str] = set()
        basenames: set[str] = set()

        identifier_pattern = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]{2,}\b")
        file_pattern = re.compile(r"[A-Za-z0-9_./-]+\.(?:py|js|jsx|ts|tsx|java|go|rb|php|cs|json|yaml|yml|toml)")

        for snippet in grounded_snippets:
            file_path = (snippet.get("file_path") or "").strip()
            if file_path:
                paths.add(file_path)
                basenames.add(file_path.split("/")[-1])
                tokens.add(file_path)
                tokens.add(file_path.split("/")[-1])

            snippet_text = snippet.get("snippet") or ""
            for identifier in identifier_pattern.findall(snippet_text):
                if self._looks_like_code_entity(identifier):
                    tokens.add(identifier)
            for path in file_pattern.findall(snippet_text):
                normalized = path.strip("`'\" ")
                if normalized:
                    paths.add(normalized)
                    basenames.add(normalized.split("/")[-1])
                    tokens.add(normalized)
                    tokens.add(normalized.split("/")[-1])
            for route_path in self._extract_route_examples(snippet_text):
                tokens.add(route_path)

        lowered_tokens = {token.lower() for token in tokens}
        lowered_paths = {path.lower() for path in paths}
        lowered_basenames = {name.lower() for name in basenames}
        return lowered_tokens, lowered_paths, lowered_basenames

    def _extract_query_entities(self, intent: str) -> set[str]:
        """Extract code-like tokens from user query for safe mention."""
        entities: set[str] = set()
        if not intent:
            return entities

        for token in re.findall(r"[A-Za-z_][A-Za-z0-9_./:-]{2,}", intent):
            normalized = token.strip("`'\".,:;()[]{}")
            if self._looks_like_code_entity(normalized):
                entities.add(normalized.lower())
        return entities

    def _line_has_unsupported_backtick_token(self, line: str, supported_tokens: set[str]) -> bool:
        """Check if line has unsupported backtick-wrapped code entities."""
        for token in re.findall(r"`([^`]+)`", line):
            normalized = token.strip("`'\".,:;()[]{}").lower()
            if not normalized:
                continue
            if not self._looks_like_code_entity(normalized):
                continue
            if normalized not in supported_tokens:
                return True
        return False

    def _line_has_unsupported_path(
        self,
        line: str,
        supported_paths: set[str],
        supported_basenames: set[str],
    ) -> bool:
        """Check for plain-text file path mentions not present in evidence."""
        file_pattern = re.compile(r"[A-Za-z0-9_./-]+\.(?:py|js|jsx|ts|tsx|java|go|rb|php|cs|json|yaml|yml|toml)")
        for path in file_pattern.findall(line):
            normalized = path.strip("`'\".,:;()[]{}").lower()
            if not normalized:
                continue
            basename = normalized.split("/")[-1]
            if normalized not in supported_paths and basename not in supported_basenames:
                return True
        return False

    def _looks_like_code_entity(self, token: str) -> bool:
        """Heuristic to detect code-like tokens/symbols."""
        if not token:
            return False

        if "/" in token or "." in token or "_" in token or ":" in token:
            return True
        if any(char.isupper() for char in token[1:]):
            return True
        if token.startswith("use") and len(token) > 4:
            return True
        if re.match(r"^[a-z]+[A-Z][A-Za-z0-9]*$", token):
            return True
        return False

    def _not_found_message(self, output_language: str) -> str:
        """Localized fallback when all unsupported lines are removed."""
        if output_language == "hindi":
            return "रिट्रीव किए गए स्निपेट्स में इस प्रश्न का ठोस प्रमाण नहीं मिला।"
        if output_language == "telugu":
            return "రిట్రీవ్ చేసిన స్నిప్పెట్లలో ఈ ప్రశ్నకు సరిపడే స్పష్టమైన ఆధారాలు కనిపించలేదు."
        return "I could not verify this answer from the retrieved snippets."

    def _unsupported_filtered_note(self, output_language: str) -> str:
        """Localized note for filtered unsupported claims."""
        if output_language == "hindi":
            return "_नोट: जिन कोड entities का प्रमाण स्निपेट्स में नहीं मिला, उन्हें उत्तर से हटाया गया है।_"
        if output_language == "telugu":
            return "_గమనిక: రిట్రీవ్ చేసిన స్నిప్పెట్లలో ఆధారం లేని కోడ్ entities ను సమాధానం నుండి తొలగించాం._"
        return "_Note: Unsupported code entities not present in retrieved snippets were removed._"

    def _format_evidence_section(
        self,
        grounded_snippets: List[Dict[str, Any]],
        output_language: str,
        compact: bool = False,
    ) -> str:
        """Append an explicit evidence section from actual retrieved snippets."""
        if not grounded_snippets:
            return ""

        if output_language == "hindi":
            header = "### रिपॉजिटरी से प्रमाण (Retrieved Snippets)"
            note = "नीचे दिए गए snippets सीधे रिपॉजिटरी से लिए गए हैं:"
        elif output_language == "telugu":
            header = "### రిపోజిటరీ ఆధారాలు (Retrieved Snippets)"
            note = "క్రింద snippets నేరుగా రిపోజిటరీ నుంచి తీసుకున్నవి:"
        else:
            header = "### Evidence From Repository (Retrieved Snippets)"
            note = "The snippets below are directly taken from retrieved repository chunks:"

        lines = [header, note]
        for idx, snippet in enumerate(grounded_snippets[:4], start=1):
            lines.append(
                f"- Snippet {idx}: `{snippet['file_path']}` (lines {snippet['start_line']}-{snippet['end_line']})"
            )
            if not compact:
                lines.append("```")
                lines.append(snippet["snippet"].strip())
                lines.append("```")

        return "\n".join(lines)

    def _is_feature_overview_intent(self, intent: str) -> bool:
        """Return True for broad feature-overview questions."""
        query = (intent or "").strip().lower()
        if not query:
            return False
        if any(pattern in query for pattern in self.FEATURE_OVERVIEW_PATTERNS):
            return True
        return "feature" in query and ("what" in query or "which" in query)

    def _is_noise_file(self, file_path: str) -> bool:
        """Detect tooling/config files that should not dominate feature summaries."""
        path_lower = (file_path or "").lower()
        return any(token in path_lower for token in self.NOISE_FILE_HINTS)

    def _filter_overview_chunks(self, chunks: List[CodeChunk]) -> List[CodeChunk]:
        """Drop chunks from obvious noise files for feature-overview prompts."""
        filtered = [chunk for chunk in chunks if not self._is_noise_file(chunk.file_path)]
        return filtered or chunks

    def _generate_feature_overview_from_snippets(
        self,
        grounded_snippets: List[Dict[str, Any]],
        output_language: str,
    ) -> str:
        """Generate deterministic, evidence-grounded feature summary."""
        if not grounded_snippets:
            return ""

        language = output_language if output_language in {"english", "hindi", "telugu"} else "english"
        lexicon = self._feature_overview_lexicon(language)
        features = self._collect_feature_candidates(grounded_snippets)

        if not features:
            return lexicon["not_found"]

        lines = [lexicon["title"], lexicon["intro"]]
        for idx, feature in enumerate(features[:6], start=1):
            label = feature["label"].get(language, feature["label"]["english"])
            why_text = feature["why"].get(language, feature["why"]["english"])
            signals = ", ".join(feature["signals"][:3]) if feature["signals"] else lexicon["signal_generic"]
            evidence = ", ".join(
                f"`{item['file']}` (lines {item['start']}-{item['end']})"
                for item in feature["evidence"][:2]
            )
            lines.append(f"{idx}. **{label}**")
            lines.append(f"- {lexicon['implementation']}: {lexicon['signal_phrase'].format(signals=signals)}")
            lines.append(f"- {lexicon['why']}: {why_text}")
            if feature.get("route_examples"):
                sample_paths = ", ".join(f"`{path}`" for path in feature["route_examples"][:3])
                lines.append(f"- {lexicon['routes']}: {sample_paths}")
            lines.append(f"- {lexicon['evidence']}: {evidence}")

        return "\n".join(lines).strip()

    def _collect_feature_candidates(self, grounded_snippets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract feature candidates from snippet content and paths."""
        collected: Dict[str, Dict[str, Any]] = {}

        for snippet in grounded_snippets:
            file_path = snippet.get("file_path", "")
            if self._is_noise_file(file_path):
                continue

            snippet_text = snippet.get("snippet", "")
            content_lower = snippet_text.lower()
            path_lower = file_path.lower()

            for rule in self.FEATURE_RULES:
                signal_hits = [signal for signal in rule["signals"] if signal in content_lower]
                if any(path_hint in path_lower for path_hint in rule["path_hints"]):
                    signal_hits.append("path_match")

                if not signal_hits:
                    continue

                entry = collected.setdefault(
                    rule["id"],
                    {
                        "id": rule["id"],
                        "label": rule["label"],
                        "why": rule["why"],
                        "signals": [],
                        "evidence": [],
                        "route_examples": [],
                        "score": 0.0,
                    },
                )
                entry["score"] += rule["weight"] + (0.2 * len(signal_hits))

                for signal in signal_hits:
                    if signal == "path_match":
                        continue
                    if signal not in entry["signals"]:
                        entry["signals"].append(signal)

                evidence_item = {
                    "file": file_path,
                    "start": snippet.get("start_line", 1),
                    "end": snippet.get("end_line", 1),
                }
                if evidence_item not in entry["evidence"]:
                    entry["evidence"].append(evidence_item)

                if rule["id"] == "routing":
                    route_paths = self._extract_route_examples(snippet_text)
                    for route_path in route_paths:
                        if route_path not in entry["route_examples"]:
                            entry["route_examples"].append(route_path)

        ranked = sorted(collected.values(), key=lambda item: item["score"], reverse=True)
        return ranked

    def _extract_route_examples(self, snippet_text: str) -> List[str]:
        """Extract route path strings from snippet text."""
        if not snippet_text:
            return []

        matches = []
        patterns = (
            r"path\s*:\s*[\"']([^\"']+)[\"']",
            r"<Route[^>]*path=[\"']([^\"']+)[\"']",
        )
        for pattern in patterns:
            for value in re.findall(pattern, snippet_text, flags=re.IGNORECASE):
                path = value.strip()
                if path and path not in matches:
                    matches.append(path)
        return matches[:5]

    def _feature_overview_lexicon(self, language: str) -> Dict[str, str]:
        """Localized copy for deterministic feature-overview responses."""
        if language == "hindi":
            return {
                "title": "### कोडबेस की मुख्य सुविधाएँ",
                "intro": "नीचे दी गई सुविधाएँ सीधे रिट्रीव किए गए कोड स्निपेट्स से निकाली गई हैं:",
                "implementation": "कैसे लागू किया गया",
                "why": "यह क्यों महत्वपूर्ण है",
                "routes": "रूट उदाहरण",
                "evidence": "प्रमाण",
                "signal_phrase": "कोड संकेत: {signals}",
                "signal_generic": "संबंधित कोड पैटर्न मिले",
                "not_found": "रिट्रीव किए गए स्निपेट्स में स्पष्ट फीचर संकेत नहीं मिले।",
            }
        if language == "telugu":
            return {
                "title": "### ఈ కోడ్‌బేస్‌లోని ముఖ్యమైన ఫీచర్లు",
                "intro": "క్రింది ఫీచర్లు రిట్రీవ్ చేసిన కోడ్ స్నిప్పెట్ల ఆధారంగా గుర్తించబడ్డాయి:",
                "implementation": "ఎలా అమలు చేశారు",
                "why": "ఇది ఎందుకు ముఖ్యము",
                "routes": "రూట్ ఉదాహరణలు",
                "evidence": "ఆధారాలు",
                "signal_phrase": "కోడ్ సంకేతాలు: {signals}",
                "signal_generic": "సంబంధిత కోడ్ నమూనాలు గుర్తించబడ్డాయి",
                "not_found": "రిట్రీవ్ చేసిన స్నిప్పెట్లలో స్పష్టమైన ఫీచర్ సంకేతాలు కనిపించలేదు.",
            }
        return {
            "title": "### Key Features In This Codebase",
            "intro": "The features below are inferred directly from retrieved code snippets:",
            "implementation": "How implemented",
            "why": "Why it matters",
            "routes": "Route examples",
            "evidence": "Evidence",
            "signal_phrase": "Detected code signals: {signals}",
            "signal_generic": "Relevant implementation patterns detected",
            "not_found": "I could not detect clear feature signals in the retrieved snippets.",
        }
