import streamlit as st
import os
import uuid
from datetime import datetime
from graph import LegalDocumentAgent, AgentState

st.set_page_config(page_title="Legal Document Drafting", layout="centered")

# --- Modern Header ---
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    color: #1f4e79;
    text-align: center;
    margin-bottom: 1.5rem;
    letter-spacing: 1px;
}
.section-card {
    background: #f7fafc;
    border-radius: 1.2rem;
    box-shadow: 0 4px 24px 0 rgba(26,35,126,0.08);
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
}
.info-box {
    background-color: #e3e9f7;
    border: 1px solid #b3d9ff;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
}
.warning-box {
    background-color: #fffaf0;
    border: 1px solid #f6ad55;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
}
.chat-bubble {
    background: #e3e9f7;
    border-radius: 1rem;
    padding: 1rem 1.5rem;
    margin-bottom: 0.7rem;
    box-shadow: 0 2px 8px 0 rgba(26,35,126,0.04);
}
.chat-bubble.user {
    background: #fffde7;
    color: #1a237e;
    border-left: 4px solid #ffd600;
}
.chat-bubble.ai {
    background: #e3e9f7;
    color: #1a237e;
    border-left: 4px solid #1976d2;
}
</style>
<div class="main-header">📝 Legal Document Drafting Assistant</div>
""", unsafe_allow_html=True)

# --- API Key Input ---
def api_key_form():
    st.markdown("#### Enter your OpenRouter API Key to begin:")
    api_key = st.text_input("OpenRouter API Key", type="password", key="api_key_input")
    if api_key:
        os.environ["OPENROUTER_API_KEY"] = api_key
        st.session_state.api_key = api_key
        st.session_state.agent = LegalDocumentAgent()
        st.session_state.agent_initialized = True
        st.success("API key set and agent initialized!")
        st.rerun()
    st.stop()

if "agent_initialized" not in st.session_state or not st.session_state.get("api_key"):
    api_key_form()

# --- Session State Init ---
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "state_dict" not in st.session_state:
    st.session_state.state_dict = None
if "input_counter" not in st.session_state:
    st.session_state.input_counter = 0

agent = st.session_state.agent

def reset_session():
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.chat_history = []
    st.session_state.state_dict = None
    st.session_state.input_counter = 0
st.button("Start New Session", on_click=reset_session)

# --- Initial User Input for Document Type ---
if not st.session_state.chat_history:
    st.markdown('<div class="section-card info-box">👋 <b>Welcome!</b> Describe the document you want to draft (e.g., "Draft an NDA between Alice and Bob").</div>', unsafe_allow_html=True)
    user_input = st.text_input(
        "Describe the document you want to draft:",
        key="init_input"
    )
    if user_input:
        state = AgentState(session_id=st.session_state.session_id, user_input=user_input)
        state_dict = state.model_dump() if hasattr(state, "model_dump") else state.dict()
        state_dict = agent.identify_document_type(state_dict)
        st.session_state.state_dict = state_dict
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        # Ask first question
        state_dict = agent.ask_question(state_dict)
        st.session_state.state_dict = state_dict
        question = state_dict.get("current_question", "")
        if question:
            st.session_state.chat_history.append({"role": "ai", "content": question})
        st.rerun()

# --- Chat Loop ---
if st.session_state.chat_history:
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-bubble user"><b>You:</b> {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble ai"><b>AI:</b> {msg["content"]}</div>', unsafe_allow_html=True)
    if st.session_state.state_dict and not st.session_state.state_dict.get("is_complete", False):
        input_key = f"chat_input_{st.session_state.input_counter}"
        answer = st.text_input("Your answer:", key=input_key)
        if answer:
            st.session_state.chat_history.append({"role": "user", "content": answer})
            st.session_state.state_dict["user_input"] = answer
            st.session_state.state_dict = agent.process_answer(st.session_state.state_dict)
            # If now complete, generate and show document
            if st.session_state.state_dict.get("is_complete", False):
                st.session_state.state_dict = agent.generate_document(st.session_state.state_dict)
                document = st.session_state.state_dict.get("final_document", "[No document generated]")
                st.session_state.chat_history.append({"role": "ai", "content": "---\n**Generated Legal Document**\n" + document})
            else:
                st.session_state.state_dict = agent.ask_question(st.session_state.state_dict)
                question = st.session_state.state_dict.get("current_question", "")
                if question:
                    st.session_state.chat_history.append({"role": "ai", "content": question})
            st.session_state.input_counter += 1
            st.rerun()
    elif st.session_state.state_dict and st.session_state.state_dict.get("is_complete", False):
        document = st.session_state.state_dict.get("final_document", "[No document generated]")
        error_message = st.session_state.state_dict.get("error_message", "")
        st.markdown("---")
        if error_message:
            st.markdown(f'<div class="warning-box"><b>Error:</b> {error_message}</div>', unsafe_allow_html=True)
        elif "[Generated by LLM" in document:
            st.markdown('<div class="section-card info-box"><b>✅ LLM-Generated Legal Document</b></div>', unsafe_allow_html=True)
            clean_doc = document.replace("\n\n[Generated by LLM (OpenRouter DeepSeek)]", "").strip()
            st.code(clean_doc)
            st.download_button(
                label="Download Document as TXT",
                data=clean_doc,
                file_name=f"legal_document_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        elif "[Generated by predefined template]" in document:
            st.markdown('<div class="warning-box"><b>⚠️ The document could not be generated by the LLM.</b> Please check your API key or try again later. Only LLM-generated documents are shown here.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-box"><b>⚠️ No LLM output available.</b> Please ensure your API key is correct and try again.</div>', unsafe_allow_html=True) 