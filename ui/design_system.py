"""
Unified visual design system for CodeGuru India.

Minimal but intentional styling for hackathon demo quality.
"""

import html
import streamlit as st


def load_design_system():
    """Inject global CSS tokens and component styles."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=IBM+Plex+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

        :root {
            --cg-bg: #f2f6f8;
            --cg-bg-soft: #ecf3f4;
            --cg-surface: #ffffff;
            --cg-surface-soft: #f8fbfb;
            --cg-text: #0f2537;
            --cg-muted: #4e6473;
            --cg-border: #d4e2e2;
            --cg-primary: #0f766e;
            --cg-primary-strong: #0a5a54;
            --cg-accent: #f59e0b;
            --cg-success: #0f9d68;
            --cg-danger: #d13d4a;
            --cg-shadow: 0 8px 24px rgba(15, 37, 55, 0.07);
            --cg-radius: 14px;
        }

        #MainMenu, footer, header {visibility: hidden;}
        .stDeployButton {display: none;}

        .stApp {
            background:
                radial-gradient(1200px 460px at -10% -10%, rgba(15, 118, 110, 0.11), transparent 65%),
                radial-gradient(1100px 460px at 110% -15%, rgba(245, 158, 11, 0.10), transparent 65%),
                var(--cg-bg);
            color: var(--cg-text);
        }

        .main .block-container {
            max-width: 1280px;
            padding-top: 1.3rem;
            padding-bottom: 3.2rem;
            padding-left: 1.8rem;
            padding-right: 1.8rem;
        }

        html, body, [class*="css"] {
            font-family: "IBM Plex Sans", "Sora", sans-serif;
            color: var(--cg-text);
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        h1, h2, h3, h4, h5 {
            font-family: "Sora", "IBM Plex Sans", sans-serif;
            color: var(--cg-text);
            letter-spacing: -0.015em;
        }

        h1 {
            font-weight: 800;
            font-size: clamp(1.9rem, 3vw, 2.55rem);
            line-height: 1.12;
            margin: 0 0 0.5rem 0;
        }

        h2 {
            font-weight: 700;
            margin: 0 0 0.65rem 0;
            font-size: clamp(1.35rem, 2vw, 1.75rem);
        }

        h3 {
            font-weight: 700;
            font-size: 1.05rem;
            margin: 0 0 0.45rem 0;
        }

        p, .stMarkdown, .stCaption {
            color: var(--cg-text);
            line-height: 1.56;
        }

        .stCaption, [data-testid="stCaptionContainer"] {
            color: var(--cg-muted) !important;
        }

        code, pre, .stCodeBlock code {
            font-family: "JetBrains Mono", "SFMono-Regular", Menlo, monospace !important;
        }

        [data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, rgba(15, 118, 110, 0.07) 0%, rgba(15, 118, 110, 0.02) 22%, rgba(255,255,255,0.95) 64%),
                var(--cg-surface);
            border-right: 1px solid var(--cg-border);
        }

        [data-testid="stSidebar"] .block-container {
            padding-top: 0.95rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .cg-sidebar-brand {
            padding: 0.9rem 0.95rem;
            border: 1px solid rgba(15, 118, 110, 0.22);
            border-radius: 12px;
            background: linear-gradient(130deg, rgba(15, 118, 110, 0.10), rgba(245, 158, 11, 0.10));
            margin-bottom: 0.9rem;
        }

        .cg-sidebar-brand .title {
            font-family: "Sora", sans-serif;
            font-size: 1.02rem;
            font-weight: 700;
            color: var(--cg-text);
        }

        .cg-sidebar-brand .sub {
            font-size: 0.83rem;
            color: var(--cg-muted);
            margin-top: 0.18rem;
        }

        .cg-nav-caption {
            font-size: 0.72rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--cg-muted);
            font-weight: 700;
            margin: 0.15rem 0 0.5rem 0.15rem;
        }

        .stRadio > div {
            gap: 0.46rem !important;
        }

        .stRadio label {
            border: 1px solid transparent !important;
            border-radius: 10px !important;
            padding: 0.42rem 0.52rem !important;
            background: rgba(255, 255, 255, 0.65);
        }

        .stRadio label:hover {
            background: #ffffff;
            border-color: var(--cg-border) !important;
        }

        .stRadio [data-testid="stMarkdownContainer"] p {
            margin: 0 !important;
            font-weight: 600 !important;
            color: #1f384a !important;
        }

        .stButton > button {
            border-radius: 10px;
            border: 1px solid transparent;
            font-family: "IBM Plex Sans", sans-serif;
            font-weight: 600;
            letter-spacing: 0.01em;
            min-height: 2.55rem;
            transition: all 0.16s ease;
        }

        .stButton > button[kind="primary"] {
            background: linear-gradient(120deg, var(--cg-primary), #179187);
            color: #ffffff;
            box-shadow: 0 7px 16px rgba(15, 118, 110, 0.22);
        }

        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(120deg, var(--cg-primary-strong), var(--cg-primary));
            transform: translateY(-1px);
        }

        .stButton > button[kind="secondary"] {
            background: rgba(255, 255, 255, 0.86);
            border-color: var(--cg-border);
            color: #1f384a;
        }

        .stButton > button[kind="secondary"]:hover {
            border-color: #a9c0c1;
            background: #ffffff;
            transform: translateY(-1px);
        }

        .stTextInput input, .stTextArea textarea, .stSelectbox > div > div {
            border-radius: 10px !important;
            border-color: #c9d9da !important;
            background: #ffffff !important;
        }

        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: rgba(15, 118, 110, 0.65) !important;
            box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.14) !important;
        }

        .stAlert {
            border-radius: 12px;
            border: 1px solid var(--cg-border);
            box-shadow: none;
        }

        [data-testid="stMetric"] {
            background: var(--cg-surface);
            border: 1px solid var(--cg-border);
            border-radius: 12px;
            padding: 0.65rem 0.8rem;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.58rem;
            font-weight: 700;
            color: #0f2537;
        }

        [data-testid="stMetricLabel"] {
            color: var(--cg-muted);
            font-weight: 600;
            letter-spacing: 0.01em;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.4rem;
            background: transparent;
            border-bottom: 1px solid var(--cg-border);
        }

        .stTabs [data-baseweb="tab"] {
            height: 2.45rem;
            border-radius: 9px 9px 0 0;
            padding: 0.3rem 0.85rem;
            color: #436073;
            font-weight: 600;
        }

        .stTabs [aria-selected="true"] {
            color: #0f2537;
            background: rgba(255,255,255,0.85);
            border-bottom: 2px solid var(--cg-primary);
        }

        .streamlit-expanderHeader {
            border: 1px solid var(--cg-border);
            border-radius: 10px;
            background: rgba(255,255,255,0.78);
            padding: 0.58rem 0.8rem;
        }

        .streamlit-expanderContent {
            border: 1px solid var(--cg-border);
            border-top: none;
            border-radius: 0 0 10px 10px;
            background: rgba(255,255,255,0.92);
        }

        .cg-hero {
            border: 1px solid rgba(15, 118, 110, 0.26);
            border-radius: 18px;
            background:
                radial-gradient(circle at 84% 24%, rgba(245, 158, 11, 0.22), transparent 45%),
                linear-gradient(145deg, rgba(15, 118, 110, 0.15), rgba(255,255,255,0.94));
            padding: 1.35rem 1.4rem 1.2rem 1.4rem;
            margin-bottom: 1rem;
            box-shadow: var(--cg-shadow);
        }

        .cg-hero .subtitle {
            color: #27485a;
            max-width: 68ch;
            margin-top: 0.15rem;
            font-size: 1rem;
            line-height: 1.52;
        }

        .cg-pill-wrap {
            display: flex;
            flex-wrap: wrap;
            gap: 0.42rem;
            margin-top: 0.95rem;
        }

        .cg-pill {
            padding: 0.3rem 0.58rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.82);
            border: 1px solid rgba(15, 118, 110, 0.24);
            color: #20556f;
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.01em;
        }

        .cg-card {
            border: 1px solid var(--cg-border);
            background: var(--cg-surface);
            border-radius: 14px;
            padding: 1rem 1rem 0.95rem 1rem;
            box-shadow: 0 3px 14px rgba(15, 37, 55, 0.05);
            height: 100%;
        }

        .cg-card .title {
            font-family: "Sora", sans-serif;
            font-weight: 700;
            color: #0f2f43;
            margin-bottom: 0.3rem;
            font-size: 1rem;
        }

        .cg-card .copy {
            color: #446173;
            font-size: 0.94rem;
            line-height: 1.48;
        }

        .cg-card .chip {
            display: inline-flex;
            align-items: center;
            margin-bottom: 0.55rem;
            border-radius: 999px;
            padding: 0.18rem 0.5rem;
            font-size: 0.72rem;
            border: 1px solid #bdd2d3;
            color: #225064;
            background: #f5fbfb;
            font-weight: 700;
            letter-spacing: 0.02em;
        }

        .cg-section-title {
            margin-top: 1.35rem;
            margin-bottom: 0.65rem;
        }

        .cg-section-title h2 {
            margin-bottom: 0.16rem;
        }

        .cg-section-title p {
            margin: 0;
            color: var(--cg-muted);
            font-size: 0.95rem;
        }

        .cg-stats-grid {
            display: grid;
            gap: 0.7rem;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            margin-top: 0.35rem;
        }

        .cg-stat {
            border: 1px solid var(--cg-border);
            border-radius: 12px;
            background: linear-gradient(180deg, #ffffff, #f8fcfc);
            padding: 0.75rem 0.82rem;
        }

        .cg-stat .value {
            font-family: "Sora", sans-serif;
            font-size: 1.55rem;
            font-weight: 700;
            line-height: 1.1;
            color: #0f2537;
        }

        .cg-stat .label {
            margin-top: 0.15rem;
            color: #486072;
            font-size: 0.82rem;
            font-weight: 600;
            letter-spacing: 0.02em;
            text-transform: uppercase;
        }

        .cg-soft-panel {
            margin-top: 0.95rem;
            border: 1px solid var(--cg-border);
            background: rgba(255,255,255,0.86);
            border-radius: 14px;
            padding: 0.9rem 1rem;
        }

        .cg-soft-panel h4 {
            font-family: "Sora", sans-serif;
            font-size: 0.98rem;
            margin: 0 0 0.35rem 0;
            font-weight: 700;
        }

        .cg-soft-panel p {
            margin: 0;
            color: #466072;
            font-size: 0.93rem;
        }

        .cg-chat-user, .cg-chat-assistant {
            border: 1px solid var(--cg-border);
            border-radius: 12px;
            padding: 0.82rem 0.9rem;
            margin: 0.45rem 0;
        }

        .cg-chat-user {
            background: linear-gradient(135deg, rgba(15, 118, 110, 0.09), rgba(15, 118, 110, 0.03));
            border-color: rgba(15, 118, 110, 0.25);
        }

        .cg-chat-assistant {
            background: rgba(255,255,255,0.88);
        }

        .cg-chat-label {
            font-family: "Sora", sans-serif;
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            color: #2d4d5f;
            margin-bottom: 0.18rem;
        }

        .cg-fade-in {
            animation: cgFadeIn 0.42s ease both;
        }

        @keyframes cgFadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 900px) {
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
                padding-top: 1.1rem;
            }

            .cg-hero {
                padding: 1rem 1rem 0.95rem 1rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _escape(value: str) -> str:
    return html.escape(value or "")


def section_header(title: str, subtitle: str = None):
    """Render a consistent section heading."""
    safe_title = _escape(title)
    if subtitle:
        safe_subtitle = _escape(subtitle)
        st.markdown(
            f"""
            <div class="cg-section-title cg-fade-in">
                <h2>{safe_title}</h2>
                <p>{safe_subtitle}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(f"## {safe_title}")


def render_hero(title: str, subtitle: str, pills=None):
    """Render a hero banner with optional pill highlights."""
    safe_title = _escape(title)
    safe_subtitle = _escape(subtitle)
    pill_html = ""
    if pills:
        entries = "".join(f'<span class="cg-pill">{_escape(str(item))}</span>' for item in pills[:8])
        pill_html = f'<div class="cg-pill-wrap">{entries}</div>'

    st.markdown(
        f"""
        <section class="cg-hero cg-fade-in">
            <h1>{safe_title}</h1>
            <p class="subtitle">{safe_subtitle}</p>
            {pill_html}
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_feature_card(title: str, description: str, chip: str = ""):
    """Render one feature card."""
    safe_title = _escape(title)
    safe_description = _escape(description)
    chip_html = f'<span class="chip">{_escape(chip)}</span>' if chip else ""
    st.markdown(
        f"""
        <article class="cg-card cg-fade-in">
            {chip_html}
            <div class="title">{safe_title}</div>
            <p class="copy">{safe_description}</p>
        </article>
        """,
        unsafe_allow_html=True,
    )


def render_stats(items):
    """Render a responsive stats strip. items=[(value,label), ...]."""
    cards = []
    for value, label in items:
        cards.append(
            f"""
            <div class="cg-stat">
                <div class="value">{_escape(str(value))}</div>
                <div class="label">{_escape(str(label))}</div>
            </div>
            """
        )

    st.markdown(
        f'<div class="cg-stats-grid cg-fade-in">{"".join(cards)}</div>',
        unsafe_allow_html=True,
    )


def render_soft_panel(title: str, body: str):
    """Render a subtle informational panel."""
    st.markdown(
        f"""
        <div class="cg-soft-panel cg-fade-in">
            <h4>{_escape(title)}</h4>
            <p>{_escape(body)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(value: str, label: str, delta: str = None):
    """Thin wrapper around Streamlit metric for compatibility."""
    st.metric(label=label, value=value, delta=delta)


def info_box(message: str, type: str = "info"):
    """Compatibility wrapper for alerts."""
    if type == "success":
        st.success(message)
    elif type == "warning":
        st.warning(message)
    elif type == "error":
        st.error(message)
    else:
        st.info(message)


def spacing(size: str = "md"):
    """Vertical spacing utility."""
    sizes = {
        "xs": "6px",
        "sm": "10px",
        "md": "16px",
        "lg": "24px",
        "xl": "34px",
        "2xl": "48px",
    }
    st.markdown(f'<div style="height: {sizes.get(size, "16px")}"></div>', unsafe_allow_html=True)


def card(content: str):
    """Compatibility helper for rendering generic card content."""
    st.markdown(
        f"""
        <div class="cg-card cg-fade-in">
            {content}
        </div>
        """,
        unsafe_allow_html=True,
    )
