"""
Production-grade design system for CodeGuru India
Designed with Apple-level restraint and intentionality
"""
import streamlit as st


def load_design_system():
    """Load the complete design system with calm, minimal aesthetics."""
    st.markdown("""
    <style>
    /* ============================================
       DESIGN SYSTEM - CodeGuru India
       Philosophy: Calm, minimal, confident
       ============================================ */
    
    /* === RESET & BASE === */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* System fonts - native, fast, familiar */
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', system-ui, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    code, pre, .stCodeBlock {
        font-family: 'SF Mono', 'Menlo', 'Monaco', 'Courier New', monospace !important;
    }
    
    /* === HIDE STREAMLIT CHROME === */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* === LAYOUT === */
    .main {
        max-width: 1200px;
        margin: 0 auto;
        padding: 32px;
    }
    
    .main .block-container {
        padding-top: 32px;
        padding-bottom: 64px;
        max-width: 100%;
    }
    
    /* === SIDEBAR === */
    [data-testid="stSidebar"] {
        background: #FAFAFA;
        border-right: 1px solid #E5E5E5;
        padding: 24px 16px;
    }
    
    [data-testid="stSidebar"] * {
        font-size: 14px;
    }
    
    /* === TYPOGRAPHY === */
    h1 {
        font-size: 32px;
        font-weight: 600;
        line-height: 1.2;
        color: #1A1A1A;
        margin-bottom: 8px;
        letter-spacing: -0.02em;
    }
    
    h2 {
        font-size: 24px;
        font-weight: 600;
        line-height: 1.3;
        color: #1A1A1A;
        margin-top: 48px;
        margin-bottom: 16px;
        letter-spacing: -0.01em;
    }
    
    h3 {
        font-size: 18px;
        font-weight: 600;
        line-height: 1.4;
        color: #1A1A1A;
        margin-top: 32px;
        margin-bottom: 12px;
    }
    
    p, .stMarkdown {
        font-size: 15px;
        line-height: 1.6;
        color: #1A1A1A;
    }
    
    .stCaption, caption {
        font-size: 13px;
        line-height: 1.5;
        color: #666666;
    }
    
    /* === BUTTONS === */
    .stButton > button {
        background: #0066CC;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-size: 15px;
        font-weight: 500;
        transition: background 0.15s ease;
        cursor: pointer;
        height: 44px;
    }
    
    .stButton > button:hover {
        background: #0052A3;
    }
    
    .stButton > button:active {
        background: #004080;
    }
    
    .stButton > button[kind="secondary"] {
        background: white;
        color: #1A1A1A;
        border: 1px solid #E5E5E5;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: #F9F9F9;
        border-color: #CCCCCC;
    }
    
    /* === INPUTS === */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border: 1px solid #E5E5E5;
        border-radius: 6px;
        padding: 10px 12px;
        font-size: 15px;
        color: #1A1A1A;
        background: white;
        transition: border-color 0.15s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #0066CC;
        outline: none;
        box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
    }
    
    /* === CARDS === */
    .element-container {
        margin-bottom: 16px;
    }
    
    /* === METRICS === */
    [data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: 600;
        color: #1A1A1A;
        letter-spacing: -0.02em;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 13px;
        font-weight: 500;
        color: #666666;
        text-transform: none;
        letter-spacing: 0;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 13px;
        font-weight: 500;
    }
    
    /* === TABS === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 1px solid #E5E5E5;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        color: #666666;
        font-size: 15px;
        font-weight: 500;
        padding: 12px 20px;
        border-bottom: 2px solid transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #1A1A1A;
    }
    
    .stTabs [aria-selected="true"] {
        color: #1A1A1A;
        border-bottom-color: #0066CC;
        background: transparent;
    }
    
    /* === PROGRESS === */
    .stProgress > div > div > div {
        background: #0066CC;
        height: 4px;
        border-radius: 2px;
    }
    
    .stProgress > div > div {
        background: #E5E5E5;
        border-radius: 2px;
    }
    
    /* === ALERTS === */
    .stAlert {
        border-radius: 6px;
        border: 1px solid #E5E5E5;
        padding: 16px;
        margin: 16px 0;
        background: white;
    }
    
    .stSuccess {
        border-left: 3px solid #00A86B;
        background: #F0FFF4;
    }
    
    .stInfo {
        border-left: 3px solid #0066CC;
        background: #F0F7FF;
    }
    
    .stWarning {
        border-left: 3px solid #FF9500;
        background: #FFF9F0;
    }
    
    .stError {
        border-left: 3px solid #FF3B30;
        background: #FFF0F0;
    }
    
    /* === CODE BLOCKS === */
    .stCodeBlock {
        border: 1px solid #E5E5E5;
        border-radius: 6px;
        background: #FAFAFA;
        margin: 16px 0;
    }
    
    code {
        background: #F5F5F5;
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 14px;
        color: #1A1A1A;
    }
    
    /* === FILE UPLOADER === */
    [data-testid="stFileUploader"] {
        border: 1px dashed #CCCCCC;
        border-radius: 6px;
        padding: 32px;
        background: #FAFAFA;
        text-align: center;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #0066CC;
        background: white;
    }
    
    /* === EXPANDER === */
    .streamlit-expanderHeader {
        background: transparent;
        border: 1px solid #E5E5E5;
        border-radius: 6px;
        padding: 12px 16px;
        font-size: 15px;
        font-weight: 500;
        color: #1A1A1A;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #CCCCCC;
    }
    
    /* === DIVIDER === */
    hr {
        border: none;
        border-top: 1px solid #E5E5E5;
        margin: 32px 0;
    }
    
    /* === SCROLLBAR === */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #CCCCCC;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #999999;
    }
    
    /* === RADIO & CHECKBOX === */
    .stRadio > div,
    .stCheckbox > div {
        gap: 8px;
    }
    
    /* === SELECTBOX === */
    .stSelectbox > div > div {
        border-radius: 6px;
    }
    
    /* === RESPONSIVE === */
    @media (max-width: 768px) {
        .main {
            padding: 16px;
        }
        
        h1 {
            font-size: 28px;
        }
        
        h2 {
            font-size: 20px;
        }
    }
    
    /* === UTILITY CLASSES === */
    .text-secondary {
        color: #666666;
    }
    
    .text-tertiary {
        color: #999999;
    }
    
    .border-light {
        border: 1px solid #E5E5E5;
    }
    
    .bg-secondary {
        background: #F9F9F9;
    }
    
    /* === REMOVE UNNECESSARY ANIMATIONS === */
    * {
        transition-duration: 0.15s !important;
    }
    
    /* === FOCUS VISIBLE (ACCESSIBILITY) === */
    *:focus-visible {
        outline: 2px solid #0066CC;
        outline-offset: 2px;
    }
    </style>
    """, unsafe_allow_html=True)


def section_header(title: str, subtitle: str = None):
    """
    Clean section header with optional subtitle.
    No decoration, just clear hierarchy.
    """
    st.markdown(f"## {title}")
    if subtitle:
        st.markdown(f'<p style="color: #666666; margin-top: -8px; margin-bottom: 24px;">{subtitle}</p>', unsafe_allow_html=True)


def metric_card(value: str, label: str, delta: str = None):
    """
    Simple metric display. No icons, no gradients.
    Just the number and what it means.
    """
    st.metric(label=label, value=value, delta=delta)


def info_box(message: str, type: str = "info"):
    """
    Minimal info box. Border-left accent only.
    """
    if type == "info":
        st.info(message)
    elif type == "success":
        st.success(message)
    elif type == "warning":
        st.warning(message)
    elif type == "error":
        st.error(message)


def spacing(size: str = "md"):
    """
    Consistent vertical spacing.
    sm=8px, md=16px, lg=24px, xl=32px
    """
    sizes = {"sm": "8px", "md": "16px", "lg": "24px", "xl": "32px", "2xl": "48px"}
    st.markdown(f'<div style="height: {sizes.get(size, "16px")}"></div>', unsafe_allow_html=True)


def card(content: str):
    """
    Minimal card: white background, subtle border, no shadow.
    """
    st.markdown(f"""
    <div style="
        background: white;
        border: 1px solid #E5E5E5;
        border-radius: 6px;
        padding: 24px;
        margin: 16px 0;
    ">
        {content}
    </div>
    """, unsafe_allow_html=True)
