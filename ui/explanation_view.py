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
    
    # Get analysis from session if available
    analysis = st.session_state.get("current_analysis", None)
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Summary", "📖 Details", "📊 Diagrams", "🐛 Issues"])
    
    with tab1:
        _render_summary_tab(analysis)
    
    with tab2:
        _render_details_tab(analysis, uploaded_code)
    
    with tab3:
        _render_diagrams_tab()
    
    with tab4:
        _render_issues_tab(analysis)


def _render_summary_tab(analysis):
    """Render summary tab with real or mock data."""
    st.markdown("### 📝 Code Summary")
    
    if analysis:
        # Use real analysis
        st.markdown(analysis.summary)
        
        st.divider()
        
        # Display structure info
        st.markdown("### 🔑 Code Structure")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Functions", len(analysis.structure.functions))
        with col2:
            st.metric("Classes", len(analysis.structure.classes))
        with col3:
            st.metric("Complexity", analysis.complexity_score)
        
        # Show functions and classes
        if analysis.structure.functions:
            st.markdown("**Functions:**")
            for func in analysis.structure.functions[:5]:  # Show first 5
                st.info(f"✓ {func.name}({', '.join(func.parameters)})")
        
        if analysis.structure.classes:
            st.markdown("**Classes:**")
            for cls in analysis.structure.classes[:5]:  # Show first 5
                st.info(f"✓ {cls.name}")
        
        # Show patterns
        if analysis.patterns:
            st.divider()
            st.markdown("### 🎯 Patterns Detected")
            for pattern in analysis.patterns:
                with st.expander(f"📌 {pattern.name}", expanded=False):
                    st.markdown(pattern.description)
    else:
        # Mock data fallback
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
    
    # Analogies (always show for engagement)
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


def _render_details_tab(analysis, code):
    """Render detailed explanation tab."""
    st.markdown("### 📖 Detailed Explanation")
    
    if analysis:
        # Show AI-generated explanation
        explanation = st.session_state.get("detailed_explanation", None)
        
        if not explanation and "orchestrator" in st.session_state:
            # Generate detailed explanation
            with st.spinner("Generating detailed explanation..."):
                try:
                    language = st.session_state.session_manager.get_language_preference()
                    explanation = st.session_state.orchestrator.explain_code(
                        code=code,
                        language=language,
                        difficulty="intermediate"
                    )
                    st.session_state.detailed_explanation = explanation
                except Exception as e:
                    explanation = f"Error generating explanation: {str(e)}"
        
        if explanation:
            st.markdown(explanation)
        else:
            st.info("💡 Click 'Generate Explanation' to get AI-powered insights")
            if st.button("Generate Explanation"):
                st.rerun()
    else:
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
    
    # Get analysis and code from session
    analysis = st.session_state.get("current_analysis", None)
    code = st.session_state.session_manager.get_uploaded_code()
    
    diagram_type = st.selectbox(
        "Select Diagram Type",
        ["Flowchart", "Class Diagram", "Architecture", "Sequence Diagram"]
    )
    
    if analysis and code:
        # Generate real diagrams
        if "diagram_generator" not in st.session_state:
            from generators.diagram_generator import DiagramGenerator
            st.session_state.diagram_generator = DiagramGenerator()
        
        diagram_gen = st.session_state.diagram_generator
        
        try:
            if diagram_type == "Flowchart":
                st.markdown("#### Function Flow")
                # Get first function for flowchart
                if analysis.structure.functions:
                    func = analysis.structure.functions[0]
                    # Extract function code (simplified)
                    diagram = diagram_gen.generate_flowchart(code, func.name)
                else:
                    diagram = diagram_gen.generate_flowchart(code, "main")
                
                st.code(diagram, language="mermaid")
            
            elif diagram_type == "Class Diagram":
                st.markdown("#### Class Structure")
                diagram = diagram_gen.generate_class_diagram(analysis.structure.classes)
                st.code(diagram, language="mermaid")
            
            elif diagram_type == "Architecture":
                st.markdown("#### Project Architecture")
                filename = st.session_state.get("uploaded_filename", "Project")
                project_name = filename.split('.')[0]
                diagram = diagram_gen.generate_architecture_diagram(
                    analysis.structure,
                    project_name
                )
                st.code(diagram, language="mermaid")
            
            elif diagram_type == "Sequence Diagram":
                st.markdown("#### API Interaction Flow")
                diagram = diagram_gen.generate_sequence_diagram(code)
                st.code(diagram, language="mermaid")
            
            # Download buttons
            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                st.button("📥 Download PNG", use_container_width=True)
            with col2:
                st.button("📥 Download SVG", use_container_width=True)
            
            st.info("💡 Copy the Mermaid code above and paste it into https://mermaid.live to view the rendered diagram!")
        
        except Exception as e:
            st.error(f"Error generating diagram: {str(e)}")
            st.info("Showing example diagram instead")
            _render_mock_diagram(diagram_type)
    else:
        # Show mock diagrams
        _render_mock_diagram(diagram_type)


def _render_mock_diagram(diagram_type: str):
    """Render mock diagram when no analysis available."""
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


def _render_issues_tab(analysis):
    """Render issues tab with real or mock data."""
    st.markdown("### 🐛 Code Issues & Suggestions")
    
    if analysis and analysis.issues:
        # Show real issues
        for issue in analysis.issues:
            severity_colors = {
                "critical": "🔴",
                "warning": "🟡",
                "suggestion": "🔵"
            }
            
            with st.expander(
                f"{severity_colors.get(issue.severity, '⚪')} Line {issue.line_number}: {issue.description}",
                expanded=True
            ):
                st.markdown(f"**Severity:** {issue.severity.upper()}")
                st.markdown(f"**Line Number:** {issue.line_number}")
                st.markdown(f"**Issue:** {issue.description}")
                st.markdown(f"**Suggestion:** {issue.suggestion}")
        
        if not analysis.issues:
            st.success("✅ No issues found! Your code looks great!")
    else:
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
