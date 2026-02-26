"""Code explanation view component."""
import streamlit as st


def render_explanation_view():
    """Render code explanation interface with tabs."""
    st.title("💡 Code Explanations")
    
    session_manager = st.session_state.session_manager
    uploaded_code = session_manager.get_uploaded_code()
    
    if not uploaded_code:
        st.info("📤 Upload code first to see explanations!")
        if st.button("Go to Upload"):
            st.session_state.current_page = "Upload Code"
            st.rerun()
        return
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Summary", "📖 Details", "📊 Diagrams", "🐛 Issues"])
    
    with tab1:
        _render_summary_tab()
    
    with tab2:
        _render_details_tab()
    
    with tab3:
        _render_diagrams_tab()
    
    with tab4:
        _render_issues_tab()


def _render_summary_tab():
    """Render summary tab with mock data."""
    st.markdown("### 📝 Code Summary")
    
    # Mock summary
    st.markdown("""
    This code implements a user authentication system with JWT tokens. 
    It includes functions for user registration, login, and token validation.
    """)
    
    st.divider()
    
    # Key concepts
    st.markdown("### 🔑 Key Concepts")
    concepts = ["JWT Authentication", "Password Hashing", "Token Validation", "User Sessions"]
    
    cols = st.columns(2)
    for i, concept in enumerate(concepts):
        with cols[i % 2]:
            st.info(f"✓ {concept}")
    
    st.divider()
    
    # Analogies
    st.markdown("### 🎯 Simple Analogies")
    with st.expander("🔐 JWT Token - Like a Movie Ticket", expanded=True):
        st.markdown("""
        **Think of JWT tokens like a movie ticket at a cinema:**
        
        - When you buy a ticket (login), the cinema gives you a special ticket with your seat number
        - The ticket has a stamp that proves it's real (signature)
        - You show this ticket to enter the hall (access protected routes)
        - The ticket expires after the show (token expiration)
        - If someone tries to fake a ticket, security catches them (token validation)
        
        Just like how a chai stall owner remembers regular customers, JWT helps servers remember authenticated users!
        """)


def _render_details_tab():
    """Render detailed explanation tab."""
    st.markdown("### 📖 Detailed Explanation")
    
    # Mock detailed explanation
    st.markdown("""
    #### Function: `authenticate_user(username, password)`
    
    This function handles user authentication by:
    1. Retrieving user data from the database
    2. Comparing the provided password with the stored hash
    3. Generating a JWT token if credentials are valid
    4. Returning the token to the client
    
    **Security Features:**
    - Uses bcrypt for password hashing
    - Implements rate limiting to prevent brute force attacks
    - Tokens expire after 24 hours
    """)
    
    st.divider()
    
    # Code examples
    st.markdown("### 💻 Code Examples")
    
    with st.expander("Example 1: Basic Login", expanded=True):
        st.code("""
# Example usage
token = authenticate_user("john@example.com", "secure_password")
if token:
    print("Login successful!")
    # Use token for subsequent requests
else:
    print("Invalid credentials")
        """, language="python")
        
        st.caption("**Output:** Login successful!")


def _render_diagrams_tab():
    """Render diagrams tab."""
    st.markdown("### 📊 Visual Diagrams")
    
    diagram_type = st.selectbox(
        "Select Diagram Type",
        ["Flowchart", "Class Diagram", "Sequence Diagram", "Architecture"]
    )
    
    # Mock Mermaid diagram
    if diagram_type == "Flowchart":
        st.markdown("#### Authentication Flow")
        st.code("""
graph TD
    A[User Login] --> B{Valid Credentials?}
    B -->|Yes| C[Generate JWT Token]
    B -->|No| D[Return Error]
    C --> E[Return Token to Client]
    D --> F[Show Error Message]
        """, language="mermaid")
        
        # Download buttons
        col1, col2 = st.columns(2)
        with col1:
            st.button("📥 Download PNG", use_container_width=True)
        with col2:
            st.button("📥 Download SVG", use_container_width=True)
    
    elif diagram_type == "Class Diagram":
        st.markdown("#### User Authentication Classes")
        st.code("""
classDiagram
    class User {
        +String username
        +String email
        +String password_hash
        +authenticate()
        +generate_token()
    }
    class AuthService {
        +login()
        +logout()
        +validate_token()
    }
    User --> AuthService
        """, language="mermaid")


def _render_issues_tab():
    """Render issues tab with mock data."""
    st.markdown("### 🐛 Code Issues & Suggestions")
    
    # Mock issues
    issues = [
        {
            "severity": "critical",
            "line": 42,
            "description": "SQL Injection vulnerability detected",
            "suggestion": "Use parameterized queries instead of string concatenation"
        },
        {
            "severity": "warning",
            "line": 78,
            "description": "Unused variable 'temp_data'",
            "suggestion": "Remove unused variable or use it in the logic"
        },
        {
            "severity": "suggestion",
            "line": 105,
            "description": "Consider using list comprehension",
            "suggestion": "Replace for loop with list comprehension for better performance"
        }
    ]
    
    for issue in issues:
        severity_colors = {
            "critical": "🔴",
            "warning": "🟡",
            "suggestion": "🔵"
        }
        
        with st.expander(f"{severity_colors[issue['severity']]} Line {issue['line']}: {issue['description']}", expanded=True):
            st.markdown(f"**Severity:** {issue['severity'].upper()}")
            st.markdown(f"**Line Number:** {issue['line']}")
            st.markdown(f"**Issue:** {issue['description']}")
            st.markdown(f"**Suggestion:** {issue['suggestion']}")
    
    if not issues:
        st.success("✅ No issues found! Your code looks great!")
