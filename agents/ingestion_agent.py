from utils.loader import load_and_split_document
from mcp.protocol import MCPMessage, MessageBus

class IngestionAgent:
    def __init__(self, message_bus: MessageBus):
        self.bus = message_bus

    def run(self, file_path: str, trace_id: str):
        # print(f"📥 IngestionAgent processing: {file_path}")
        chunks = load_and_split_document(file_path)

        message = MCPMessage(
            sender="IngestionAgent",
            receiver="RetrievalAgent",
            type="DOCUMENT_CHUNKS",
            trace_id=trace_id,
            payload={
                "chunks": [chunk.page_content for chunk in chunks],
                "metadata": [chunk.metadata for chunk in chunks]
            }
        )
        self.bus.send(message)
