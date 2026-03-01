"""
Codebase Chat Interface.

Provides ChatGPT-like interface for asking questions about the codebase.
"""

import streamlit as st
import logging
import time
import html
from typing import List, Dict, Any
from ui.design_system import section_header, spacing
from utils.performance_metrics import record_metric

logger = logging.getLogger(__name__)

CHAT_LANGUAGE_LABELS = {
    "english": "English",
    "hindi": "हिंदी (Hindi)",
    "telugu": "తెలుగు (Telugu)",
}
CHAT_TO_VOICE_LANGUAGE = {
    "english": "en",
    "hindi": "hi",
    "telugu": "te",
}
FEATURE_OVERVIEW_PATTERNS = (
    "key feature",
    "main feature",
    "major feature",
    "what features",
    "overall functionality",
    "what this app does",
    "what this codebase does",
    "capabilities",
    "overview",
)
LOCATION_PATTERNS = (
    "which file",
    "where is",
    "where are",
    "where does",
    "defined in",
    "implemented in",
    "located",
)
COMPARISON_PATTERNS = (
    "compare",
    "difference",
    "different",
    "vs",
    "versus",
    "contrast",
)
DEBUG_PATTERNS = (
    "error",
    "bug",
    "issue",
    "not working",
    "failing",
    "fix",
    "exception",
    "traceback",
)


def _audio_signature(audio_bytes: bytes) -> str:
    """Create a lightweight signature for detecting new recordings."""
    if not audio_bytes:
        return ""
    head = audio_bytes[:24]
    tail = audio_bytes[-24:] if len(audio_bytes) > 24 else b""
    return f"{len(audio_bytes)}:{head!r}:{tail!r}"


def _contains_non_ascii(text: str) -> bool:
    """Return True when text contains non-ASCII characters."""
    return any(ord(char) > 127 for char in (text or ""))


def _grounding_failure_message(output_language: str, grounding: Dict[str, Any]) -> str:
    """Localized message when retrieval evidence is insufficient."""
    reason = grounding.get("reason", "low_score")
    anchors = grounding.get("anchor_terms", []) or []
    anchor_note = ", ".join(f"`{term}`" for term in anchors[:4]) if anchors else ""

    if output_language == "hindi":
        if reason == "missing_anchor" and anchor_note:
            return (
                "मुझे इस प्रश्न के लिए रिपॉजिटरी से पर्याप्त सटीक प्रमाण नहीं मिला।\n\n"
                f"इन anchors का स्पष्ट match नहीं मिला: {anchor_note}\n"
                "कृपया exact file/function/feature नाम के साथ फिर पूछें।"
            )
        return (
            "मुझे इस प्रश्न के लिए रिपॉजिटरी के रिट्रीव्ड snippets में पर्याप्त प्रमाण नहीं मिला।\n\n"
            "कृपया प्रश्न को थोड़ा specific करें (feature, file, function, route का नाम दें)।"
        )

    if output_language == "telugu":
        if reason == "missing_anchor" and anchor_note:
            return (
                "ఈ ప్రశ్నకు రిపోజిటరీలో తగిన స్పష్టమైన ఆధారాలు కనిపించలేదు.\n\n"
                f"ఈ anchors కు match కాలేదు: {anchor_note}\n"
                "దయచేసి exact file/function/feature పేరుతో మళ్లీ అడగండి."
            )
        return (
            "ఈ ప్రశ్నకు రిట్రీవ్ చేసిన repository snippets‌లో సరిపడే ఆధారాలు లభించలేదు.\n\n"
            "దయచేసి ప్రశ్నను మరింత specific గా అడగండి (feature/file/function/route పేరుతో)."
        )

    if reason == "missing_anchor" and anchor_note:
        return (
            "I could not find strong repository evidence for this question.\n\n"
            f"I could not match these query anchors: {anchor_note}\n"
            "Please ask with exact file/function/feature names."
        )
    return (
        "I could not find strong repository evidence for this question in retrieved snippets.\n\n"
        "Please rephrase with a specific feature, file, function, or route name."
    )


def _normalize_intent_for_search(intent_text: str, output_language: str, rag_explainer) -> str:
    """
    Convert multilingual user intent into an English retrieval query.
    Final explanation language remains unchanged.
    """
    cleaned_intent = (intent_text or "").strip()
    if not cleaned_intent:
        return cleaned_intent

    if output_language == "english" and not _contains_non_ascii(cleaned_intent):
        return cleaned_intent

    orchestrator = getattr(rag_explainer, "orchestrator", None)
    if not orchestrator or not hasattr(orchestrator, "generate_completion"):
        return cleaned_intent

    prompt = f"""Rewrite this user code question into concise English for code retrieval.
Rules:
- Keep framework, library, API, and file/function names unchanged.
- Keep the meaning exactly the same.
- Output exactly one line, no bullets or explanations.

User question:
{cleaned_intent}
"""
    try:
        rewritten = orchestrator.generate_completion(
            prompt,
            max_tokens=120,
            temperature=0.0,
        )
        rewritten = str(rewritten).strip().splitlines()[0].strip(" \"'")
        if not rewritten or rewritten.lower().startswith("error"):
            return cleaned_intent
        return rewritten
    except Exception as exc:
        logger.warning(f"Intent normalization failed, using original query: {exc}")
        return cleaned_intent


def _is_feature_overview_query(text: str) -> bool:
    """Detect broad feature-overview questions."""
    query = (text or "").lower()
    return any(pattern in query for pattern in FEATURE_OVERVIEW_PATTERNS)


def _classify_query_strategy(text: str) -> str:
    """Classify query to tune retrieval breadth."""
    query = (text or "").lower()
    if any(pattern in query for pattern in FEATURE_OVERVIEW_PATTERNS):
        return "overview"
    if any(pattern in query for pattern in COMPARISON_PATTERNS):
        return "comparison"
    if any(pattern in query for pattern in DEBUG_PATTERNS):
        return "debug"
    if any(pattern in query for pattern in LOCATION_PATTERNS):
        return "location"
    return "specific"


def _top_k_for_query_strategy(strategy: str) -> int:
    """Choose retrieval depth based on query strategy."""
    mapping = {
        "overview": 36,
        "comparison": 32,
        "debug": 30,
        "location": 20,
        "specific": 20,
    }
    return mapping.get(strategy, 20)


def render_codebase_chat(
    session_manager,
    semantic_search,
    rag_explainer,
    multi_intent_analyzer,
    memory_store=None
):
    """
    Render chat interface for codebase queries.
    
    Args:
        session_manager: SessionManager instance
        semantic_search: SemanticCodeSearch instance
        rag_explainer: RAGExplainer instance
        multi_intent_analyzer: MultiIntentAnalyzer instance
        memory_store: MemoryStore instance
    """
    section_header(
        "💬 Codebase Chat",
        "Ask questions about your codebase - like ChatGPT for code"
    )
    
    # Check if repository is loaded
    repo_context = session_manager.get_current_repository()
    
    if not repo_context:
        st.warning("⚠️ No codebase loaded")
        st.info("Please upload a repository first using the 'Upload Code' page")
        return
    
    repo_analysis = repo_context.get('repo_analysis')
    repo_path = repo_context.get('repo_path')

    # Chat language controls
    default_language = st.session_state.get("selected_language", "english")
    if default_language not in CHAT_LANGUAGE_LABELS:
        default_language = "english"
    if "codebase_chat_language" not in st.session_state:
        st.session_state.codebase_chat_language = default_language
    if "codebase_chat_language_notice" not in st.session_state:
        st.session_state.codebase_chat_language_notice = ""

    st.markdown("### 🌐 Chat Language")
    lang_col1, lang_col2 = st.columns([4, 1])
    with lang_col1:
        current_chat_language = st.session_state.get("codebase_chat_language", default_language)
        lang_options = list(CHAT_LANGUAGE_LABELS.keys())
        selected_chat_language = st.selectbox(
            "Choose chat language",
            options=lang_options,
            index=lang_options.index(current_chat_language) if current_chat_language in lang_options else 0,
            format_func=lambda key: CHAT_LANGUAGE_LABELS[key],
            key="codebase_chat_language_selector",
            label_visibility="collapsed",
        )
    with lang_col2:
        spacing("sm")
        if st.button("Apply", use_container_width=True, key="apply_codebase_chat_language"):
            st.session_state.codebase_chat_language = selected_chat_language
            st.session_state.codebase_chat_language_notice = (
                f"Language applied: {CHAT_LANGUAGE_LABELS[selected_chat_language]}. "
                "Voice and chat responses will use this language."
            )
            st.rerun()

    if st.session_state.codebase_chat_language_notice:
        st.success(st.session_state.codebase_chat_language_notice)
        st.session_state.codebase_chat_language_notice = ""

    output_language = st.session_state.get("codebase_chat_language", default_language)

    analysis_session_id = _ensure_analysis_session(
        memory_store,
        repo_analysis,
        repo_path,
        output_language,
    )
    
    # Check if semantic search is indexed
    if not hasattr(semantic_search, 'code_chunks') or not semantic_search.code_chunks:
        st.warning("⚠️ Codebase not indexed yet. Indexing now...")
        
        with st.spinner("Indexing codebase for intelligent search..."):
            try:
                semantic_search.index_repository(repo_path, repo_analysis)
                st.success("✅ Codebase indexed! You can now ask questions.")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to index codebase: {str(e)}")
                logger.error(f"Indexing failed: {e}")
                return
    
    # Show repository info
    with st.expander("📦 Current Codebase", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Files", repo_analysis.total_files)
        with col2:
            st.metric("Lines", f"{repo_analysis.total_lines:,}")
        with col3:
            st.metric("Languages", len(repo_analysis.languages))
        
        st.caption(f"**Path**: {repo_analysis.repo_url}")
        st.caption(f"**Indexed**: {len(semantic_search.code_chunks)} code chunks")
    
    spacing("md")

    # Voice prompt controls (native language input)
    voice_processor = st.session_state.get("voice_processor")
    with st.expander("🎤 Voice Prompt (Ask in Native Language)", expanded=False):
        if not voice_processor:
            st.warning("Voice processor not initialized.")
        else:
            if "codebase_voice_audio" not in st.session_state:
                st.session_state.codebase_voice_audio = b""
            if "codebase_voice_signature" not in st.session_state:
                st.session_state.codebase_voice_signature = ""
            if "codebase_voice_transcript" not in st.session_state:
                st.session_state.codebase_voice_transcript = ""

            active_voice_lang = CHAT_TO_VOICE_LANGUAGE.get(output_language, "en")
            st.caption(
                f"Voice language: {CHAT_LANGUAGE_LABELS.get(output_language, 'English')}. "
                "Recorded voice will be transcribed and inserted into chat input."
            )
            st.markdown(
                "1. Click the mic button to start recording.\n"
                "2. Click again after speaking to stop.\n"
                "3. Click `Translate` to insert the transcript into the prompt box."
            )

            try:
                from audio_recorder_streamlit import audio_recorder

                audio_bytes = audio_recorder(
                    text="🎙️ Start/Stop Recording",
                    recording_color="#0066CC",
                    neutral_color="#E5E5E5",
                    icon_size="2x",
                )
                if audio_bytes:
                    current_signature = _audio_signature(audio_bytes)
                    if current_signature != st.session_state.codebase_voice_signature:
                        st.session_state.codebase_voice_audio = audio_bytes
                        st.session_state.codebase_voice_signature = current_signature
                        st.session_state.codebase_voice_transcript = ""
                        st.success("Recording completed successfully.")

                if st.session_state.codebase_voice_audio:
                    col_translate, col_clear = st.columns(2)
                    with col_translate:
                        translate_clicked = st.button("Translate", key="translate_voice_prompt", type="primary")
                    with col_clear:
                        clear_clicked = st.button("Clear Voice", key="clear_voice_prompt", use_container_width=True)

                    if clear_clicked:
                        st.session_state.codebase_voice_audio = b""
                        st.session_state.codebase_voice_signature = ""
                        st.session_state.codebase_voice_transcript = ""
                        st.session_state["chat_input"] = ""
                        st.success("Voice recording and transcript cleared.")
                        st.rerun()

                    if translate_clicked:
                        with st.spinner("Translating your voice prompt..."):
                            result = voice_processor.process_audio(
                                st.session_state.codebase_voice_audio,
                                active_voice_lang,
                            )
                            if result and result.transcript:
                                transcript = result.transcript.strip()
                                st.session_state.codebase_voice_transcript = transcript
                                # Update prompt input before chat_input widget is created.
                                st.session_state["chat_input"] = transcript
                                st.success("Translated text inserted into prompt box.")
                            else:
                                st.error("Translation failed. Please record and try again.")

                if st.session_state.codebase_voice_transcript:
                    st.markdown("**Translated text:**")
                    st.text_area(
                        "Voice transcript",
                        value=st.session_state.codebase_voice_transcript,
                        height=90,
                        disabled=True,
                        key="voice_transcript_preview",
                        label_visibility="collapsed",
                    )
            except ImportError:
                st.warning(
                    "Voice recorder package not installed. Install with: "
                    "`pip install streamlit-audio-recorder`"
                )
    
    # Initialize chat history
    if (
        st.session_state.get("loaded_chat_session_id") != analysis_session_id
        or "chat_history" not in st.session_state
    ):
        persisted_messages = []
        if memory_store and analysis_session_id:
            persisted_messages = memory_store.get_chat_messages(analysis_session_id, limit=500)
        st.session_state.chat_history = [
            {
                "role": message.get("role"),
                "content": message.get("content", ""),
                "code_references": message.get("metadata", {}).get("code_references", []),
                "metadata": message.get("metadata", {}),
            }
            for message in persisted_messages
        ]
        st.session_state.loaded_chat_session_id = analysis_session_id

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'chat_processing' not in st.session_state:
        st.session_state.chat_processing = False

    if 'clear_chat_input' not in st.session_state:
        st.session_state.clear_chat_input = False

    # Streamlit only allows updating widget state before the widget is created.
    if st.session_state.clear_chat_input:
        st.session_state["chat_input"] = ""
        st.session_state.clear_chat_input = False
    
    # Chat container
    chat_container = st.container()
    
    # Display chat history
    with chat_container:
        if not st.session_state.chat_history:
            st.info("👋 Hi! I'm your codebase assistant. Ask me anything about the code!")
            
            # Suggested questions
            st.markdown("**Suggested questions:**")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔍 How is routing implemented?", use_container_width=True):
                    _process_query(
                        "How is routing implemented in this codebase?",
                        session_manager,
                        semantic_search,
                        rag_explainer,
                        multi_intent_analyzer,
                        repo_analysis,
                        repo_path,
                        memory_store,
                        analysis_session_id,
                        output_language,
            )
                
                if st.button("🔐 Explain authentication flow", use_container_width=True):
                    _process_query(
                        "Explain the authentication flow",
                        session_manager,
                        semantic_search,
                        rag_explainer,
                        multi_intent_analyzer,
                        repo_analysis,
                        repo_path,
                        memory_store,
                        analysis_session_id,
                        output_language,
                    )
            
            with col2:
                if st.button("🏗️ What's the architecture?", use_container_width=True):
                    _process_query(
                        "What's the overall architecture of this codebase?",
                        session_manager,
                        semantic_search,
                        rag_explainer,
                        multi_intent_analyzer,
                        repo_analysis,
                        repo_path,
                        memory_store,
                        analysis_session_id,
                        output_language,
                    )
                
                if st.button("📊 How is state managed?", use_container_width=True):
                    _process_query(
                        "How is state management implemented?",
                        session_manager,
                        semantic_search,
                        rag_explainer,
                        multi_intent_analyzer,
                        repo_analysis,
                        repo_path,
                        memory_store,
                        analysis_session_id,
                        output_language,
                    )
        
        else:
            # Display chat messages
            for message in st.session_state.chat_history:
                _render_message(message)
    
    spacing("md")
    
    # Chat input
    st.markdown("---")
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_query = st.text_area(
            "Ask a question about the codebase",
            placeholder="e.g., How is routing implemented? What does the authentication system do? Explain the database schema...",
            height=100,
            key="chat_input",
            label_visibility="collapsed"
        )
    
    with col2:
        spacing("sm")
        send_button = st.button("📤 Send", type="primary", use_container_width=True)
        
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.clear_chat_input = True
            st.rerun()
    
    # Process query
    if send_button and user_query and not st.session_state.chat_processing:
        # Defer input clear to next rerun before the widget is created.
        st.session_state.clear_chat_input = True
        _process_query(
            user_query,
            session_manager,
            semantic_search,
            rag_explainer,
            multi_intent_analyzer,
            repo_analysis,
            repo_path,
            memory_store,
            analysis_session_id,
            output_language,
        )
        st.rerun()


def _process_query(
    query: str,
    session_manager,
    semantic_search,
    rag_explainer,
    multi_intent_analyzer,
    repo_analysis,
    repo_path,
    memory_store,
    analysis_session_id: str,
    output_language: str,
):
    """Process user query and generate response."""
    start_time = time.perf_counter()
    try:
        st.session_state.chat_processing = True
        
        # Add user message
        st.session_state.chat_history.append({
            'role': 'user',
            'content': query
        })
        if memory_store and analysis_session_id:
            memory_store.save_chat_message(
                analysis_session_id,
                role="user",
                content=query,
                language=output_language,
            )
        
        # Show processing status
        with st.spinner("🤔 Analyzing your question..."):
            # Analyze intents
            logger.info(f"Analyzing query: {query}")
            intents = multi_intent_analyzer.analyze_query(query)
            logger.info(f"Found {len(intents)} intents")
        
        # Process each intent
        responses = []
        
        for i, intent in enumerate(intents, 1):
            with st.spinner(f"🔍 Searching codebase for intent {i}/{len(intents)}..."):
                # Search for relevant code
                search_query = _normalize_intent_for_search(
                    intent.intent_text,
                    output_language,
                    rag_explainer,
                )
                strategy = _classify_query_strategy(search_query)
                if strategy == "specific":
                    strategy = _classify_query_strategy(intent.intent_text)
                top_k = _top_k_for_query_strategy(strategy)
                logger.info(f"Searching for: {intent.intent_text}")
                logger.info(f"Search query used for retrieval: {search_query}")
                logger.info(f"Query strategy: {strategy} (top_k={top_k})")
                relevant_chunks = semantic_search.search_by_intent(search_query, top_k=top_k)

                # Fallback to original intent if rewritten query didn't find anything.
                if not relevant_chunks and search_query != intent.intent_text:
                    relevant_chunks = semantic_search.search_by_intent(intent.intent_text, top_k=top_k)

                logger.info(f"Found {len(relevant_chunks)} relevant chunks")

                grounding = {
                    "is_grounded": bool(relevant_chunks),
                    "reason": "no_chunks" if not relevant_chunks else "ok",
                    "anchor_terms": [],
                }
                if hasattr(semantic_search, "assess_grounding"):
                    grounding = semantic_search.assess_grounding(intent.intent_text, relevant_chunks)
                    logger.info(f"Grounding assessment: {grounding}")

                if not relevant_chunks or not grounding.get("is_grounded", False):
                    logger.warning(f"No relevant code found for: {intent.intent_text}")
                    responses.append({
                        'intent': intent.intent_text,
                        'explanation': _grounding_failure_message(output_language, grounding),
                        'code_references': []
                    })
                    continue
            
            with st.spinner(f"✍️ Generating detailed explanation {i}/{len(intents)}..."):
                # Generate explanation
                logger.info(f"Generating explanation for: {intent.intent_text}")
                explanation_result = rag_explainer.generate_detailed_explanation(
                    intent.intent_text,
                    relevant_chunks,
                    repo_analysis,
                    use_web_search=False,  # Set to False for now
                    output_language=output_language,
                )
                logger.info(f"Explanation generated: {len(explanation_result.get('explanation', ''))} chars")
                
                responses.append(explanation_result)
        
        # Combine responses
        combined_response = _combine_responses(responses)
        
        # Add assistant message
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': combined_response['explanation'],
            'code_references': combined_response.get('code_references', []),
            'metadata': {
                'intents_processed': len(intents),
                'files_analyzed': len(
                    set(
                        ref.get('file')
                        for resp in responses
                        for ref in resp.get('code_references', [])
                        if ref.get('file')
                    )
                )
            }
        })
        if memory_store and analysis_session_id:
            memory_store.save_chat_message(
                analysis_session_id,
                role="assistant",
                content=combined_response['explanation'],
                language=output_language,
                metadata={
                    "code_references": combined_response.get("code_references", []),
                    "intents_processed": len(intents),
                },
            )

        record_metric(
            "chat_query_total",
            time.perf_counter() - start_time,
            {
                "intents": len(intents),
                "language": output_language,
                "query_length": len(query),
            },
        )

        progress_tracker = st.session_state.get("progress_tracker")
        if progress_tracker:
            progress_tracker.record_activity(
                "chat_query",
                {
                    "topic": query[:80],
                    "skill": "codebase_chat",
                    "minutes_spent": max(1, min(8, len(query) // 45)),
                },
            )
        
        st.session_state.chat_processing = False
    
    except Exception as e:
        logger.error(f"Query processing failed: {e}", exc_info=True)
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': f"I encountered an error while processing your question:\n\n```\n{str(e)}\n```\n\nPlease try:\n1. Rephrasing your question\n2. Being more specific\n3. Checking if the codebase is properly loaded",
            'code_references': []
        })
        if memory_store and analysis_session_id:
            memory_store.save_chat_message(
                analysis_session_id,
                role="assistant",
                content=f"I encountered an error while processing your question:\n{str(e)}",
                language=output_language,
            )
        record_metric(
            "chat_query_total",
            time.perf_counter() - start_time,
            {"error": str(e), "language": output_language},
        )
        st.session_state.chat_processing = False


def _ensure_analysis_session(memory_store, repo_analysis, repo_path: str, language: str) -> str:
    """Create or reuse an analysis session id for persistent memory."""
    if not memory_store:
        return ""
    existing = st.session_state.get("current_analysis_session_id")
    if existing:
        existing_session = memory_store.get_session(existing)
        if existing_session and existing_session.get("source_ref") == repo_path:
            return existing

    repo_title = getattr(repo_analysis, "repo_url", None) or repo_path
    repo_title = repo_title.rstrip("/").split("/")[-1] if repo_title else "repository"
    user_id = st.session_state.get("user_id", "anonymous")
    summary = getattr(repo_analysis, "summary", "")

    session_id = memory_store.create_session(
        user_id=user_id,
        source_type="repository",
        title=repo_title,
        source_ref=repo_path,
        language=language,
        summary=summary[:800] if summary else "",
    )
    st.session_state.current_analysis_session_id = session_id
    return session_id


def _combine_responses(responses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Combine multiple intent responses into one."""
    if len(responses) == 1:
        return responses[0]
    
    # Multiple intents - combine explanations
    combined_explanation = ""
    all_code_refs = []
    
    for i, response in enumerate(responses, 1):
        if len(responses) > 1:
            combined_explanation += f"\n\n## {i}. {response['intent']}\n\n"
        
        combined_explanation += response['explanation']
        all_code_refs.extend(response.get('code_references', []))
    
    return {
        'explanation': combined_explanation,
        'code_references': all_code_refs
    }


def _render_message(message: Dict[str, Any]):
    """Render a chat message."""
    role = message['role']
    content = message['content']
    safe_content = html.escape(content or "")
    
    if role == 'user':
        st.markdown(
            f"""
                <div class="cg-chat-user">
                    <div class="cg-chat-label">You</div>
                    <div>{safe_content}</div>
                </div>
            """,
            unsafe_allow_html=True,
        )
    
    else:  # assistant
        st.markdown(
            """
            <div class="cg-chat-assistant">
                <div class="cg-chat-label">CodeGuru Assistant</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Render explanation
        st.markdown(content)
        
        # Show code references
        code_refs = message.get('code_references', [])
        if code_refs:
            with st.expander(f"📁 Code References ({len(code_refs)} files)"):
                for ref in code_refs[:5]:  # Show top 5
                    st.markdown(f"**{ref['file']}** (lines {ref['lines']})")
                    if 'content' in ref:
                        st.code(ref['content'][:300] + "..." if len(ref['content']) > 300 else ref['content'])
        
        # Show metadata
        metadata = message.get('metadata', {})
        if metadata:
            st.caption(f"✓ Analyzed {metadata.get('files_analyzed', 0)} files | Processed {metadata.get('intents_processed', 1)} intent(s)")
        
        spacing("sm")
