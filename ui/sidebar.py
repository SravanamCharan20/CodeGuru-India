import streamlit as st

st.set_page_config(layout="wide")

# ---------- GLOBAL STYLES ----------
st.markdown("""
<style>
.app {
    display: grid;
    grid-template-columns: 260px 1fr;
    min-height: 100vh;
}

.nav {
    border-right: 1px solid #E5E7EB;
    padding: 24px 16px;
}

.nav-title {
    font-size: 18px;
    font-weight: 600;
}

.nav-sub {
    font-size: 13px;
    color: #6B7280;
    margin-top: 2px;
}

.nav-section {
    margin-top: 32px;
    font-size: 12px;
    color: #6B7280;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.nav button {
    width: 100%;
    text-align: left;
    background: transparent;
    border: none;
    padding: 10px 12px;
    margin-top: 6px;
    border-radius: 8px;
    font-size: 14px;
}

.nav button:hover {
    background: #F3F4F6;
}

.nav-active {
    background: #EEF4FF !important;
    color: #0B5FFF;
    font-weight: 600;
}

.main {
    padding: 48px;
}
</style>
""", unsafe_allow_html=True)

# ---------- STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ---------- LAYOUT ----------
st.markdown('<div class="app">', unsafe_allow_html=True)

# ---------- NAV ----------
st.markdown('<div class="nav">', unsafe_allow_html=True)

st.markdown("""
<div class="nav-title">CodeGuru India</div>
<div class="nav-sub">AI-Powered Learning</div>
""", unsafe_allow_html=True)

st.markdown('<div class="nav-section">Navigation</div>', unsafe_allow_html=True)

pages = [
    "Home",
    "Upload Code",
    "Explanations",
    "Learning Paths",
    "Quizzes",
    "Flashcards",
    "Progress"
]

for p in pages:
    active = "nav-active" if st.session_state.page == p else ""
    if st.button(p, key=p):
        st.session_state.page = p
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ---------- MAIN ----------
st.markdown('<div class="main">', unsafe_allow_html=True)

st.markdown(f"## {st.session_state.page}")

st.markdown("""
This is your main content area.
It will **never disappear**.
Navigation is **always visible**.
""")

st.markdown('</div></div>', unsafe_allow_html=True)