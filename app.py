"""Main entry point for CodeGuru India application."""
import streamlit as st
from session_manager import SessionManager
from config import load_config
from ai.bedrock_client import BedrockClient
from ai.prompt_templates import PromptManager
from ai.langchain_orchestrator import LangChainOrchestrator
from analyzers.code_analyzer import CodeAnalyzer


def main():
    """Initialize and run the Streamlit application."""
    setup_page_config()
    initialize_session_state()
    initialize_backend_services()
    
    # Import sidebar and route to selected page.
    from ui.sidebar import render_sidebar
    
    selected_page = render_sidebar()
    route_to_page(selected_page)


def setup_page_config():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="CodeGuru India - AI-Powered Code Learning",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': "CodeGuru India - Learn code faster with AI-powered explanations"
        }
    )
    
    # Load custom CSS
    from ui.design_system import load_design_system
    load_design_system()
    
    # Add custom CSS for sidebar toggle functionality
    st.markdown("""
    <style>
    /* Make sure the default Streamlit collapse button is always visible and functional */
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        position: fixed !important;
        top: 0.5rem !important;
        left: 0.5rem !important;
        z-index: 999999 !important;
        background: white !important;
        border: 1px solid #E5E5E5 !important;
        border-radius: 6px !important;
        padding: 8px 12px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        cursor: pointer !important;
    }
    
    [data-testid="collapsedControl"]:hover {
        background: #F9F9F9 !important;
        border-color: #0066CC !important;
    }
    
    /* Style the hamburger icon */
    [data-testid="collapsedControl"] svg {
        color: #1A1A1A !important;
        width: 20px !important;
        height: 20px !important;
    }
    
    /* Ensure sidebar close button is visible */
    [data-testid="stSidebar"] button[kind="header"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        background: white !important;
        border: 1px solid #E5E5E5 !important;
        border-radius: 6px !important;
        padding: 8px !important;
        margin: 8px !important;
    }
    
    [data-testid="stSidebar"] button[kind="header"]:hover {
        background: #F9F9F9 !important;
        border-color: #0066CC !important;
    }
    
    /* Make sure sidebar can be interacted with */
    [data-testid="stSidebar"] {
        z-index: 999998 !important;
    }
    
    /* Ensure main content doesn't overlap with toggle button */
    .main .block-container {
        padding-left: 3rem !important;
    }
    </style>
    """, unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if "session_manager" not in st.session_state:
        st.session_state.session_manager = SessionManager()
    
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"

    if "current_analysis_session_id" not in st.session_state:
        st.session_state.current_analysis_session_id = None


def initialize_backend_services():
    """Initialize AI and analysis services."""
    if "backend_initialized" not in st.session_state:
        try:
            # Load configuration
            aws_config, app_config = load_config()
            
            # Initialize AI services
            bedrock_client = BedrockClient(aws_config)
            prompt_manager = PromptManager()
            orchestrator = LangChainOrchestrator(bedrock_client, prompt_manager)
            
            from ai.voice_processor import VoiceProcessor
            voice_processor = VoiceProcessor(aws_config)
            
            # Initialize analyzers and engines
            code_analyzer = CodeAnalyzer(orchestrator)
            
            from engines.explanation_engine import ExplanationEngine
            from engines.quiz_engine import QuizEngine
            from generators.diagram_generator import DiagramGenerator
            from learning.path_manager import LearningPathManager
            from learning.progress_tracker import ProgressTracker
            from learning.flashcard_manager import FlashcardManager
            from analyzers.repo_analyzer import RepoAnalyzer
            
            explanation_engine = ExplanationEngine(orchestrator)
            quiz_engine = QuizEngine(orchestrator)
            diagram_generator = DiagramGenerator()
            path_manager = LearningPathManager()
            progress_tracker = ProgressTracker(st.session_state.session_manager)
            flashcard_manager = FlashcardManager(st.session_state.session_manager)
            repo_analyzer = RepoAnalyzer(code_analyzer)
            
            # Initialize intent-driven analysis components
            from analyzers.intent_interpreter import IntentInterpreter
            from analyzers.file_selector import FileSelector
            from analyzers.multi_file_analyzer import MultiFileAnalyzer
            from analyzers.repository_manager import RepositoryManager
            from generators.learning_artifact_generator import LearningArtifactGenerator
            from learning.traceability_manager import TraceabilityManager
            from analyzers.intent_driven_orchestrator import IntentDrivenOrchestrator
            
            # Initialize new AI-powered components
            from analyzers.semantic_code_search import SemanticCodeSearch
            from analyzers.multi_intent_analyzer import MultiIntentAnalyzer
            from analyzers.rag_explainer import RAGExplainer
            from storage.memory_store import MemoryStore
            from generators.chat_learning_generator import ChatLearningGenerator
            
            intent_interpreter = IntentInterpreter(orchestrator)
            file_selector = FileSelector(orchestrator)
            multi_file_analyzer = MultiFileAnalyzer(code_analyzer, orchestrator)
            repository_manager = RepositoryManager(repo_analyzer, max_size_mb=100)
            learning_artifact_generator = LearningArtifactGenerator(
                flashcard_manager,
                quiz_engine,
                orchestrator
            )
            traceability_manager = TraceabilityManager(st.session_state.session_manager)
            intent_driven_orchestrator = IntentDrivenOrchestrator(
                repository_manager,
                intent_interpreter,
                file_selector,
                multi_file_analyzer,
                learning_artifact_generator,
                traceability_manager,
                st.session_state.session_manager
            )
            
            # Initialize AI-powered search and explanation
            semantic_search = SemanticCodeSearch(orchestrator)
            multi_intent_analyzer = MultiIntentAnalyzer(orchestrator)
            rag_explainer = RAGExplainer(orchestrator, web_search_available=False)
            memory_store = MemoryStore()
            chat_learning_generator = ChatLearningGenerator(orchestrator)
            
            # Store in session state
            st.session_state.bedrock_client = bedrock_client
            st.session_state.prompt_manager = prompt_manager
            st.session_state.orchestrator = orchestrator
            st.session_state.voice_processor = voice_processor
            st.session_state.code_analyzer = code_analyzer
            st.session_state.explanation_engine = explanation_engine
            st.session_state.quiz_engine = quiz_engine
            st.session_state.diagram_generator = diagram_generator
            st.session_state.path_manager = path_manager
            st.session_state.progress_tracker = progress_tracker
            st.session_state.flashcard_manager = flashcard_manager
            st.session_state.repo_analyzer = repo_analyzer
            
            # Intent-driven analysis components
            st.session_state.intent_interpreter = intent_interpreter
            st.session_state.file_selector = file_selector
            st.session_state.multi_file_analyzer = multi_file_analyzer
            st.session_state.repository_manager = repository_manager
            st.session_state.learning_artifact_generator = learning_artifact_generator
            st.session_state.traceability_manager = traceability_manager
            st.session_state.intent_driven_orchestrator = intent_driven_orchestrator
            
            # AI-powered search and explanation
            st.session_state.semantic_search = semantic_search
            st.session_state.multi_intent_analyzer = multi_intent_analyzer
            st.session_state.rag_explainer = rag_explainer
            st.session_state.memory_store = memory_store
            st.session_state.chat_learning_generator = chat_learning_generator
            
            st.session_state.backend_initialized = True
            
        except Exception as e:
            st.session_state.backend_initialized = False
            st.session_state.backend_error = str(e)


def route_to_page(page: str):
    """Route to the selected page component."""
    from ui.explanation_view import render_explanation_view
    from ui.learning_path import render_learning_path
    from ui.progress_dashboard import render_progress_dashboard
    
    if page == "Home":
        from ui.design_system import section_header, spacing, info_box
        
        # Hero section - minimal and clean
        st.markdown("# CodeGuru India")
        st.markdown('<p style="color: #666666; font-size: 17px; margin-top: -8px; margin-bottom: 32px;">Learn code faster with AI-powered explanations</p>', unsafe_allow_html=True)
        
        spacing("lg")
        
        # Features grid - simple cards
        section_header("Features")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: white; border: 1px solid #E5E5E5; border-radius: 6px; padding: 24px; margin-bottom: 16px;">
                <h3 style="font-size: 18px; font-weight: 600; color: #1A1A1A; margin-bottom: 8px;">Smart Code Analysis</h3>
                <p style="font-size: 15px; color: #666666; line-height: 1.6; margin: 0;">Upload files or GitHub repos for instant AI-powered analysis with detailed insights</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background: white; border: 1px solid #E5E5E5; border-radius: 6px; padding: 24px;">
                <h3 style="font-size: 18px; font-weight: 600; color: #1A1A1A; margin-bottom: 8px;">Interactive Learning</h3>
                <p style="font-size: 15px; color: #666666; line-height: 1.6; margin: 0;">Flashcards, quizzes, and structured learning paths tailored to your goals</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: white; border: 1px solid #E5E5E5; border-radius: 6px; padding: 24px; margin-bottom: 16px;">
                <h3 style="font-size: 18px; font-weight: 600; color: #1A1A1A; margin-bottom: 8px;">Voice Queries</h3>
                <p style="font-size: 15px; color: #666666; line-height: 1.6; margin: 0;">Ask questions in English, Hindi, or Telugu and get instant answers</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background: white; border: 1px solid #E5E5E5; border-radius: 6px; padding: 24px;">
                <h3 style="font-size: 18px; font-weight: 600; color: #1A1A1A; margin-bottom: 8px;">Progress Tracking</h3>
                <p style="font-size: 15px; color: #666666; line-height: 1.6; margin: 0;">Monitor your growth with detailed analytics and achievement badges</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: white; border: 1px solid #E5E5E5; border-radius: 6px; padding: 24px; margin-bottom: 16px;">
                <h3 style="font-size: 18px; font-weight: 600; color: #1A1A1A; margin-bottom: 8px;">Simple Analogies</h3>
                <p style="font-size: 15px; color: #666666; line-height: 1.6; margin: 0;">Complex concepts explained with culturally relevant Indian examples</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background: white; border: 1px solid #E5E5E5; border-radius: 6px; padding: 24px;">
                <h3 style="font-size: 18px; font-weight: 600; color: #1A1A1A; margin-bottom: 8px;">Visual Diagrams</h3>
                <p style="font-size: 15px; color: #666666; line-height: 1.6; margin: 0;">Auto-generate flowcharts, class diagrams, and architecture visualizations</p>
            </div>
            """, unsafe_allow_html=True)
        
        spacing("2xl")
        
        # Status section
        section_header("Get Started")
        
        if st.session_state.get("backend_initialized", False):
            info_box("AI Services Active - Full functionality enabled with AWS Bedrock", "success")
        else:
            info_box("Demo Mode - AI services not configured. Add AWS credentials to .env file for full functionality.", "warning")
            info_box("You can still explore - All features work with mock data for demonstration purposes.", "info")
        
        spacing("md")
        
        if st.button("Upload Code Now", type="primary"):
            st.session_state.current_page = "Upload Code"
            st.rerun()
        
        spacing("2xl")
        
        # Quick stats - minimal version
        st.markdown("""
        <div style="background: #F9F9F9; border: 1px solid #E5E5E5; border-radius: 6px; padding: 32px; text-align: center;">
            <h3 style="font-size: 18px; font-weight: 600; color: #1A1A1A; margin-bottom: 24px;">Supported Technologies</h3>
            <div style="display: flex; justify-content: center; gap: 48px; flex-wrap: wrap;">
                <div>
                    <div style="font-size: 32px; font-weight: 600; color: #1A1A1A;">10+</div>
                    <div style="font-size: 13px; color: #666666;">Languages</div>
                </div>
                <div>
                    <div style="font-size: 32px; font-weight: 600; color: #1A1A1A;">5</div>
                    <div style="font-size: 13px; color: #666666;">Learning Paths</div>
                </div>
                <div>
                    <div style="font-size: 32px; font-weight: 600; color: #1A1A1A;">3</div>
                    <div style="font-size: 13px; color: #666666;">Languages (UI)</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    elif page == "Upload Code":
        # Use unified code analysis interface
        from ui.unified_code_analysis import render_unified_code_analysis
        render_unified_code_analysis(
            st.session_state.intent_driven_orchestrator,
            st.session_state.repository_manager,
            st.session_state.intent_interpreter,
            st.session_state.session_manager,
            st.session_state.code_analyzer,
            st.session_state.flashcard_manager,
        )
    elif page == "Codebase Chat":
        from ui.codebase_chat import render_codebase_chat
        render_codebase_chat(
            st.session_state.session_manager,
            st.session_state.semantic_search,
            st.session_state.rag_explainer,
            st.session_state.multi_intent_analyzer,
            st.session_state.get("memory_store"),
        )
    elif page == "Learning Memory":
        from ui.learning_memory import render_learning_memory
        render_learning_memory(
            st.session_state.session_manager,
            st.session_state.get("memory_store"),
            st.session_state.get("chat_learning_generator"),
        )
    elif page == "Explanations":
        render_explanation_view()
    elif page == "Learning Paths":
        render_learning_path()
    elif page == "Progress":
        render_progress_dashboard()
    else:
        st.session_state.current_page = "Home"
        st.rerun()


if __name__ == "__main__":
    main()
