# agents/retrieval_agent.py

from mcp.protocol import MCPMessage, MessageBus
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

class RetrievalAgent:
    def __init__(self, message_bus: MessageBus):
        self.bus = message_bus
        self.embedding = HuggingFaceEmbeddings()
        self.db = None

    def run(self):
        msg = self.bus.fetch(receiver="RetrievalAgent", type="DOCUMENT_CHUNKS")
        if not msg:
            return

        chunks = msg.payload["chunks"]
        metadata = msg.payload["metadata"]

        docs = [Document(page_content=c, metadata=m) for c, m in zip(chunks, metadata)]
        self.db = FAISS.from_documents(docs, self.embedding)

        # print("✅ RetrievalAgent: Document chunks embedded and stored.")

    def retrieve(self, query: str, trace_id: str):
        if not self.db:
            raise RuntimeError("Vector store not initialized.")

        results = self.db.similarity_search(query, k=4)

        message = MCPMessage(
            sender="RetrievalAgent",
            receiver="LLMResponseAgent",
            type="RETRIEVAL_RESULT",
            trace_id=trace_id,
            payload={
                "retrieved_context": [doc.page_content for doc in results],
                "query": query
            }
        )
        self.bus.send(message)
