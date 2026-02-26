"""Custom styling and design system for CodeGuru India."""
import streamlit as st


def load_custom_css():
    """Load custom CSS for professional, minimalist design."""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main {
        padding: 2rem 3rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        padding: 2rem 1rem;
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stRadio label {
        color: #e0e0e0 !important;
        font-weight: 500;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Headings */
    h1 {
        font-weight: 700;
        font-size: 2.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
        letter-spacing: -0.5px;
    }
    
    h2 {
        font-weight: 600;
        font-size: 1.8rem;
        color: #2d3748;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        font-weight: 600;
        font-size: 1.3rem;
        color: #4a5568;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }
    
    /* Cards and containers */
    .stCard {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stCard:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Secondary buttons */
    .stButton > button[kind="secondary"] {
        background: white;
        color: #667eea;
        border: 2px solid #667eea;
        box-shadow: none;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: #f7fafc;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        padding: 0.6rem 1rem;
        font-size: 0.95rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: transparent;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        color: #718096;
        font-weight: 500;
        padding: 0.8rem 1.5rem;
        border-radius: 8px 8px 0 0;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #f7fafc;
        color: #667eea;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        font-weight: 500;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        height: 8px;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: #f7fafc;
        border-radius: 8px;
        padding: 1rem;
        font-weight: 500;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: #edf2f7;
        border-color: #667eea;
    }
    
    /* Info/Success/Warning/Error boxes */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
    }
    
    .stSuccess {
        background: #f0fdf4;
        border-left-color: #10b981;
        color: #065f46;
    }
    
    .stInfo {
        background: #eff6ff;
        border-left-color: #3b82f6;
        color: #1e40af;
    }
    
    .stWarning {
        background: #fffbeb;
        border-left-color: #f59e0b;
        color: #92400e;
    }
    
    .stError {
        background: #fef2f2;
        border-left-color: #ef4444;
        color: #991b1b;
    }
    
    /* Code blocks */
    .stCodeBlock {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        background: #1a1a2e;
    }
    
    code {
        background: #f7fafc;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-size: 0.9em;
        color: #e53e3e;
    }
    
    /* Dividers */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 2px solid #e2e8f0;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: #f7fafc;
        border: 2px dashed #cbd5e0;
        border-radius: 12px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    section[data-testid="stSidebar"]
    [data-testid="collapsedControl"]
    .stSidebar
    
    [data-testid="stFileUploader"]:hover {
        border-color: #667eea;
        background: #edf2f7;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: 8px;
    }
    
    /* Radio buttons */
    .stRadio > div {
        gap: 0.5rem;
    }
    
    .stRadio > div > label {
        background: #f7fafc;
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .stRadio > div > label:hover {
        background: #edf2f7;
        border-color: #667eea;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Dataframe */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Custom utility classes */
    .gradient-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
    }
    
    .card-hover {
        transition: all 0.3s ease;
    }
    
    .card-hover:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }
    
    /* Responsive spacing */
    @media (max-width: 768px) {
        .main {
            padding: 1rem;
        }
        
        h1 {
            font-size: 2rem;
        }
        
        h2 {
            font-size: 1.5rem;
        }
    }
    
    /* Animation */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #5568d3;
    }
    </style>
    """, unsafe_allow_html=True)


def create_card(content: str, icon: str = "📌"):
    """Create a styled card component."""
    st.markdown(f"""
    <div style="
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
    ">
        <div style="display: flex; align-items: center; gap: 0.8rem;">
            <span style="font-size: 1.5rem;">{icon}</span>
            <div style="flex: 1;">{content}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def create_feature_card(icon: str, title: str, description: str):
    """Create a feature card for home page."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
        height: 100%;
    " class="card-hover">
        <div style="font-size: 3rem; margin-bottom: 1rem;">{icon}</div>
        <h3 style="
            color: #2d3748;
            font-weight: 600;
            margin-bottom: 0.8rem;
            font-size: 1.2rem;
        ">{title}</h3>
        <p style="
            color: #718096;
            font-size: 0.95rem;
            line-height: 1.6;
        ">{description}</p>
    </div>
    """, unsafe_allow_html=True)


def create_stat_card(value: str, label: str, icon: str = "📊", delta: str = None):
    """Create a statistics card."""
    delta_html = ""
    if delta:
        delta_color = "#10b981" if delta.startswith("+") else "#ef4444"
        delta_html = f"""
        <div style="
            color: {delta_color};
            font-size: 0.85rem;
            font-weight: 500;
            margin-top: 0.3rem;
        ">{delta}</div>
        """
    
    st.markdown(f"""
    <div style="
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        text-align: center;
    ">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <div style="
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.3rem;
        ">{value}</div>
        <div style="
            font-size: 0.85rem;
            font-weight: 500;
            color: #718096;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        ">{label}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def add_spacing(size: str = "medium"):
    """Add consistent spacing."""
    sizes = {
        "small": "0.5rem",
        "medium": "1rem",
        "large": "2rem",
        "xlarge": "3rem"
    }
    st.markdown(f'<div style="height: {sizes.get(size, "1rem")}"></div>', unsafe_allow_html=True)


def create_section_header(title: str, subtitle: str = None):
    """Create a styled section header."""
    subtitle_html = ""
    if subtitle:
        subtitle_html = f"""
        <p style="
            color: #718096;
            font-size: 1.1rem;
            margin-top: 0.5rem;
            font-weight: 400;
        ">{subtitle}</p>
        """
    
    st.markdown(f"""
    <div style="margin-bottom: 2rem;">
        <h2 style="
            font-weight: 700;
            font-size: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        ">{title}</h2>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)
