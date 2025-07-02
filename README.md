# 🧠 Agentic RAG Chatbot with MCP (LangGraph + LangChain)

This project is a **Retrieval-Augmented Generation (RAG)** chatbot that answers user queries using uploaded documents. It is built with an **agentic architecture** using LangGraph and follows a custom **Model Context Protocol (MCP)** to simulate inter-agent communication.

---

## 🚀 Features

- ✅ **Multi-format document ingestion** (`PDF`, `PPTX`, `DOCX`, `CSV`, `TXT`, `MD`)
- 🧠 **Three-Agent Architecture**:
  - `IngestionAgent`: Parses and splits documents
  - `RetrievalAgent`: Embeds + semantically searches relevant chunks
  - `LLMResponseAgent`: Builds prompt and generates final answer
- 🔗 **MCP (Model Context Protocol)** message-passing system
- 🧩 Powered by `LangGraph`, `LangChain`, `FAISS`, `Google Gemini / OpenAI`
- 🌐 **Streamlit UI** for uploads and multi-turn Q&A

---

## 🧱 Tech Stack

| Layer        | Tool                              |
|--------------|-----------------------------------|
| LLM          | Gemini 2.0 Flash / OpenAI         |
| Embeddings   | HuggingFace / OpenAI              |
| Vector DB    | FAISS                             |
| Framework    | LangChain + LangGraph             |
| UI           | Streamlit                         |
| Protocol     | Custom MCP (in-memory)            |

---

## 📁 Project Structure

```
rag-chatbot/
│
├── main.py # LangGraph pipeline runner
├── agents/ # All 3 agents
│ ├── ingestion_agent.py
│ ├── retrieval_agent.py
│ └── llm_response_agent.py
│
├── mcp/
│ └── protocol.py # MCPMessage + MessageBus
│
├── utils/
│ └── loaders.py # Multi-format document loaders
│
├── data/uploaded_docs/ # File uploads (PDF, PPTX, etc.)
│
├── ui/
│ └── app.py # Streamlit UI
│
├── README.md
└── architecture.pptx # Slide deck for submission
```

---

## 🛠️ Setup Instructions

### 1. 📦 Install Dependencies

```bash
uv pip install -r requirements.txt ( if you are not using uv use `pip install -r requirements.txt` )
```

### 2. 🔑 Set API Keys

```
set up a .env file with GOOGLE_API_KEY="get your api key from "https://aistudio.google.com/app/apikey"
```

### 3.🖥️ Launch the UI

```bash
streamlit run app.py
```


