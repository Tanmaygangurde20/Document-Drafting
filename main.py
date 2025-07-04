import streamlit as st
import os
import uuid
from datetime import datetime
from graph import LegalDocumentAgent, AgentState

# Page Configuration
st.set_page_config(
    page_title="Legal Document Drafting Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional, clean CSS styling
st.markdown("""
<style>
    /* Import professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global styles */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background-color: #f8fafc;
    }
    
    /* Header */
    .main-header {
        background: #1e293b;
        color: white;
        padding: 2rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .header-title {
        font-size: 2.25rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: white;
    }
    
    .header-subtitle {
        font-size: 1.125rem;
        color: #cbd5e1;
        font-weight: 400;
    }
    
    /* Content containers */
    .content-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    
    .api-setup {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 2rem;
        margin-bottom: 2rem;
    }
    
    .api-setup h3 {
        color: #1e293b;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .api-setup p {
        color: #64748b;
        margin-bottom: 1.5rem;
        line-height: 1.5;
    }
    
    /* Status messages */
    .status-message {
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        border-left: 4px solid;
        font-weight: 500;
    }
    
    .status-success {
        background-color: #f0fdf4;
        border-left-color: #22c55e;
        color: #166534;
    }
    
    .status-error {
        background-color: #fef2f2;
        border-left-color: #ef4444;
        color: #dc2626;
    }
    
    .status-warning {
        background-color: #fffbeb;
        border-left-color: #f59e0b;
        color: #d97706;
    }
    
    .status-info {
        background-color: #eff6ff;
        border-left-color: #3b82f6;
        color: #1d4ed8;
    }
    
    /* Chat interface */
    .chat-container {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        max-height: 500px;
        overflow-y: auto;
    }
    
    .chat-message {
        margin: 1rem 0;
        padding: 1rem;
        border-radius: 6px;
        border: 1px solid #e2e8f0;
    }
    
    .chat-message.user {
        background-color: #f1f5f9;
        border-left: 4px solid #3b82f6;
    }
    
    .chat-message.ai {
        background-color: #fafafa;
        border-left: 4px solid #64748b;
    }
    
    .chat-message.system {
        background-color: #f0f9ff;
        border-left: 4px solid #0ea5e9;
        text-align: center;
    }
    
    .message-role {
        font-weight: 600;
        font-size: 0.875rem;
        color: #374151;
        margin-bottom: 0.5rem;
    }
    
    .message-content {
        color: #1f2937;
        line-height: 1.6;
    }
    
    /* Progress indicator */
    .progress-container {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .progress-bar-container {
        background: #f1f5f9;
        border-radius: 4px;
        height: 8px;
        overflow: hidden;
    }
    
    .progress-bar {
        background: #3b82f6;
        height: 100%;
        transition: width 0.3s ease;
    }
    
    .progress-text {
        text-align: center;
        margin-top: 0.75rem;
        font-weight: 500;
        color: #374151;
        font-size: 0.875rem;
    }
    
    /* Document display */
    .document-container {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 2rem;
        margin-bottom: 2rem;
    }
    
    .document-header {
        text-align: center;
        padding: 1.5rem;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        margin-bottom: 2rem;
    }
    
    .document-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    
    .document-subtitle {
        color: #64748b;
        font-size: 0.875rem;
    }
    
    /* Feature grid */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .feature-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.75rem;
    }
    
    .feature-description {
        color: #64748b;
        font-size: 0.875rem;
        line-height: 1.5;
    }
    
    /* Input styling */
    .input-section {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .input-section h3 {
        color: #1e293b;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .input-section p {
        color: #64748b;
        margin-bottom: 1.5rem;
        line-height: 1.5;
    }
    
    /* Sidebar styling */
    .sidebar-section {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .sidebar-section h3 {
        color: #1e293b;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }
    
    .sidebar-section ul {
        list-style: none;
        padding: 0;
    }
    
    .sidebar-section li {
        color: #64748b;
        font-size: 0.875rem;
        margin-bottom: 0.5rem;
        padding-left: 1rem;
    }
    
    .sidebar-section li:before {
        content: "•";
        color: #3b82f6;
        font-weight: bold;
        display: inline-block;
        width: 1rem;
        margin-left: -1rem;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        font-size: 0.875rem;
        transition: background-color 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #2563eb;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #64748b;
        font-size: 0.875rem;
        border-top: 1px solid #e2e8f0;
        margin-top: 2rem;
    }
    
    .footer p {
        margin: 0.5rem 0;
    }
    
    .disclaimer {
        font-size: 0.75rem;
        color: #94a3b8;
        font-style: italic;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .feature-grid {
            grid-template-columns: 1fr;
        }
        
        .header-title {
            font-size: 1.75rem;
        }
        
        .content-card {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### Quick Actions")
    
    if st.button("New Session", use_container_width=True):
        for key in list(st.session_state.keys()):
            if key not in ['api_key', 'agent', 'agent_initialized']:
                del st.session_state[key]
        st.rerun()
    
    st.markdown("### Session Information")
    if 'session_id' in st.session_state:
        st.text(f"Session ID: {st.session_state.session_id[:8]}...")
    
    if 'chat_history' in st.session_state:
        st.text(f"Messages: {len(st.session_state.chat_history)}")
    
    st.markdown("### Supported Documents")
    documents = [
        "Non-Disclosure Agreement (NDA)",
        "Service Contracts",
        "Lease Agreements", 
        "Employment Contracts",
        "Partnership Agreements"
    ]
    
    st.markdown('<ul style="list-style: none; padding: 0;">', unsafe_allow_html=True)
    for doc in documents:
        st.markdown(f'<li style="margin-bottom: 0.5rem; padding-left: 1rem; position: relative;"><span style="position: absolute; left: 0; color: #3b82f6;">•</span>{doc}</li>', unsafe_allow_html=True)
    st.markdown('</ul>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main Header
st.markdown("""
<div class="main-header">
    <div class="header-title">Legal Document Drafting Assistant</div>
    <div class="header-subtitle">Professional Legal Document Creation Platform</div>
</div>
""", unsafe_allow_html=True)

# API Key Setup
def show_api_setup():
    st.markdown("""
    <div class="api-setup">
        <h3>API Configuration</h3>
        <p>Enter your OpenRouter API key to access the document generation service.</p>
    </div>
    """, unsafe_allow_html=True)
    
    api_key = st.text_input(
        "OpenRouter API Key",
        type="password",
        placeholder="Enter your API key",
        help="Required for AI document generation"
    )
    
    if api_key:
        os.environ["OPENROUTER_API_KEY"] = api_key
        st.session_state.api_key = api_key
        st.session_state.agent = LegalDocumentAgent()
        st.session_state.agent_initialized = True
        
        st.markdown("""
        <div class="status-message status-success">
            <strong>Success:</strong> API key configured successfully. You can now begin creating documents.
        </div>
        """, unsafe_allow_html=True)
        
        st.rerun()

# Check API Key
if "agent_initialized" not in st.session_state or not st.session_state.get("api_key"):
    show_api_setup()
    st.stop()

# Initialize Session State
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "state_dict" not in st.session_state:
    st.session_state.state_dict = None
if "input_counter" not in st.session_state:
    st.session_state.input_counter = 0
if "progress" not in st.session_state:
    st.session_state.progress = 0

agent = st.session_state.agent

# Welcome Screen
if not st.session_state.chat_history:
    # Service Overview
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <span class="feature-icon">📄</span>
            <div class="feature-title">Document Recognition</div>
            <div class="feature-description">
                Automatically identifies document types and guides you through the creation process.
            </div>
        </div>
        <div class="feature-card">
            <span class="feature-icon">🔍</span>
            <div class="feature-title">AI-Assisted Drafting</div>
            <div class="feature-description">
                Generates professional legal documents using advanced AI technology.
            </div>
        </div>
        <div class="feature-card">
            <span class="feature-icon">⚡</span>
            <div class="feature-title">Efficient Process</div>
            <div class="feature-description">
                Streamlined workflow to create complete documents quickly and accurately.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initial Input
    st.markdown("""
    <div class="input-section">
        <h3>Document Creation</h3>
        <p>Describe the type of legal document you need to create. Be as specific as possible to ensure accurate document generation.</p>
    </div>
    """, unsafe_allow_html=True)
    
    user_input = st.text_input(
        "Document Description",
        placeholder="Example: Create an NDA between ABC Corporation and John Smith",
        key="init_input"
    )
    
    if user_input:
        # Initialize the conversation
        state = AgentState(session_id=st.session_state.session_id, user_input=user_input)
        state_dict = state.model_dump() if hasattr(state, "model_dump") else state.dict()
        
        # Process the initial input
        state_dict = agent.identify_document_type(state_dict)
        st.session_state.state_dict = state_dict
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.progress = 20
        
        # Ask first question
        state_dict = agent.ask_question(state_dict)
        st.session_state.state_dict = state_dict
        question = state_dict.get("current_question", "")
        
        if question:
            st.session_state.chat_history.append({"role": "ai", "content": question})
        
        st.rerun()

# Chat Interface
if st.session_state.chat_history:
    # Progress Indicator
    progress_percentage = min(st.session_state.progress, 100)
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar-container">
            <div class="progress-bar" style="width: {progress_percentage}%;"></div>
        </div>
        <div class="progress-text">Document Creation Progress: {progress_percentage}%</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat History
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for i, msg in enumerate(st.session_state.chat_history):
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user">
                <div class="message-role">User Input</div>
                <div class="message-content">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        elif msg["role"] == "ai":
            content = msg["content"]
            if "Generated Legal Document" in content:
                st.markdown(f"""
                <div class="chat-message system">
                    <div class="message-content"><strong>Document Generated Successfully</strong></div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message ai">
                    <div class="message-role">Assistant</div>
                    <div class="message-content">{content}</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input for next response
    if st.session_state.state_dict and not st.session_state.state_dict.get("is_complete", False):
        st.markdown("""
        <div class="input-section">
            <h3>Response Required</h3>
            <p>Please provide your response to continue with the document creation process.</p>
        </div>
        """, unsafe_allow_html=True)
        
        input_key = f"chat_input_{st.session_state.input_counter}"
        answer = st.text_input(
            "Your Response",
            key=input_key,
            placeholder="Enter your answer here"
        )
        
        if answer:
            # Process the answer
            st.session_state.chat_history.append({"role": "user", "content": answer})
            st.session_state.state_dict["user_input"] = answer
            st.session_state.state_dict = agent.process_answer(st.session_state.state_dict)
            st.session_state.progress = min(st.session_state.progress + 15, 90)
            
            # Check if complete
            if st.session_state.state_dict.get("is_complete", False):
                st.session_state.state_dict = agent.generate_document(st.session_state.state_dict)
                st.session_state.progress = 100
                
                document = st.session_state.state_dict.get("final_document", "[No document generated]")
                st.session_state.chat_history.append({
                    "role": "ai", 
                    "content": "---\n**Generated Legal Document**\n" + document
                })
            else:
                # Ask next question
                st.session_state.state_dict = agent.ask_question(st.session_state.state_dict)
                question = st.session_state.state_dict.get("current_question", "")
                if question:
                    st.session_state.chat_history.append({"role": "ai", "content": question})
            
            st.session_state.input_counter += 1
            st.rerun()
    
    # Document Display
    elif st.session_state.state_dict and st.session_state.state_dict.get("is_complete", False):
        document = st.session_state.state_dict.get("final_document", "[No document generated]")
        error_message = st.session_state.state_dict.get("error_message", "")
        
        if error_message:
            st.markdown(f"""
            <div class="status-message status-error">
                <strong>Error:</strong> {error_message}
            </div>
            """, unsafe_allow_html=True)
        elif "[Generated by LLM" in document:
            st.markdown("""
            <div class="document-container">
                <div class="document-header">
                    <div class="document-title">Generated Legal Document</div>
                    <div class="document-subtitle">AI-Generated • Ready for Review</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            clean_doc = document.replace("\n\n[Generated by LLM (OpenRouter DeepSeek)]", "").strip()
            
            st.code(clean_doc, language="text")
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="Download Document",
                    data=clean_doc,
                    file_name=f"legal_document_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col2:
                if st.button("Create New Document", use_container_width=True):
                    for key in list(st.session_state.keys()):
                        if key not in ['api_key', 'agent', 'agent_initialized']:
                            del st.session_state[key]
                    st.rerun()
        else:
            st.markdown("""
            <div class="status-message status-warning">
                <strong>Notice:</strong> Document generation was not completed successfully. Please verify your API configuration and try again.
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p><strong>Legal Document Drafting Assistant</strong></p>
    <p class="disclaimer">
        Disclaimer: This application generates draft legal documents for informational purposes only. 
        All documents should be reviewed by a qualified legal professional before use.
    </p>
</div>
""", unsafe_allow_html=True)