import streamlit as st
import os
import uuid
from pathlib import Path
from main import rag_graph

UPLOAD_FOLDER = "data/uploaded_docs"
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

st.set_page_config(
    page_title="📄 Agentic RAG Chatbot",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding-top: 2rem;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .header-title {
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin-bottom: 0;
    }
    
    /* Chat container styling */
    .chat-container {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
    }
    
    /* User message styling */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 0.5rem 0;
        margin-left: 20%;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* AI message styling */
    .ai-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 0.5rem 0;
        margin-right: 20%;
        box-shadow: 0 4px 12px rgba(240, 147, 251, 0.3);
    }
    
    /* Upload section styling */
    .upload-section {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
        border: 2px dashed #667eea;
        text-align: center;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: #764ba2;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }
    
    /* Success message styling */
    .success-message {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(86, 171, 47, 0.3);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #667eea;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #764ba2;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* File uploader styling */
    .uploadedFile {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Stats cards */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
        border-left: 4px solid #667eea;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .stat-label {
        color: #6c757d;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'file_path' not in st.session_state:
    st.session_state.file_path = None
if 'file_name' not in st.session_state:
    st.session_state.file_name = None


st.markdown("""
<div class="header-container">
    <div class="header-title">🧠 Agentic RAG Chatbot</div>
    <div class="header-subtitle">Transform your documents into intelligent conversations</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 📊 Session Stats")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{len(st.session_state.chat_history)//2}</div>
            <div class="stat-label">Questions Asked</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        file_status = "✅" if st.session_state.file_path else "❌"
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{file_status}</div>
            <div class="stat-label">Document Ready</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🔧 Features")
    st.markdown("""
    - 📄 Multi-format support (PDF, DOCX, PPTX, CSV, TXT, MD)
    - 🧠 AI-powered document analysis
    - 💬 Interactive chat interface
    - 📊 Real-time conversation tracking
    - 🔍 Intelligent context retrieval
    """)
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Upload clear, well-formatted documents
    - Ask specific questions for better results
    - Use follow-up questions to dive deeper
    - Try different phrasings if needed
    """)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("""
    <div class="upload-section">
        <h3>📤 Upload Your Document</h3>
        <p>Drag and drop or click to browse</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "docx", "pptx", "csv", "txt", "md"],
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        st.session_state.file_path = file_path
        st.session_state.file_name = uploaded_file.name
        
        st.markdown(f"""
        <div class="success-message">
            ✅ Successfully uploaded: {uploaded_file.name}
        </div>
        """, unsafe_allow_html=True)
        
        file_size = os.path.getsize(file_path) / 1024  # KB
        st.markdown(f"""
        **File Details:**
        - **Name:** {uploaded_file.name}
        - **Size:** {file_size:.1f} KB
        - **Type:** {uploaded_file.type}
        """)

with col2:
    if st.session_state.file_path:
        st.markdown("### 💬 Chat with Your Document")
        
        chat_container = st.container()
        with chat_container:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            
            if st.session_state.chat_history:
                for i, chat in enumerate(st.session_state.chat_history):
                    if chat['role'] == 'user':
                        st.markdown(f"""
                        <div class="user-message">
                            <strong>You:</strong> {chat['content']}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="ai-message">
                            <strong>AI:</strong> {chat['content']}
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="text-align: center; padding: 2rem; color: #6c757d;">
                    <h4>👋 Ready to chat!</h4>
                    <p>Ask me anything about your uploaded document.</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        

        st.markdown("---")
        col_input, col_button = st.columns([4, 1])
        
        with col_input:
            user_input = st.text_input(
                "Ask a question about your document...",
                key="user_input",
                placeholder="What is this document about?",
                label_visibility="collapsed"
            )
        
        with col_button:
            send_button = st.button("Send 🚀", use_container_width=True)
        

        if send_button or (user_input and st.session_state.get('last_input') != user_input):
            if user_input.strip():
                
                st.session_state.chat_history.append({
                    'role': 'user', 
                    'content': user_input
                })
                
                
                trace_id = str(uuid.uuid4())
                
                with st.spinner("🤖 AI is analyzing your document..."):
                    try:
                        response = rag_graph(
                            file_path=st.session_state.file_path,
                            user_query=user_input,
                            trace_id=trace_id
                        )
                        
                        if response is None or response.strip() == "":
                            response = "I apologize, but I couldn't generate a response. Please try rephrasing your question."
                            
                    except Exception as e:
                        response = f"An error occurred while processing your request: {str(e)}"
                
                
                st.session_state.chat_history.append({
                    'role': 'ai', 
                    'content': response
                })
                
                st.session_state.last_input = user_input
                st.rerun()
        
        
        if st.session_state.chat_history:
            st.markdown("---")
            if st.button("🗑️ Clear Chat History", type="secondary"):
                st.session_state.chat_history = []
                st.rerun()
    
    else:
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem; color: #6c757d;">
            <h3>📄 No Document Uploaded</h3>
            <p>Please upload a document to start chatting with your content.</p>
            <p>Supported formats: PDF, DOCX, PPTX, CSV, TXT, MD</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 2rem;">
    <p>🧠 Powered by AI • Made with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)