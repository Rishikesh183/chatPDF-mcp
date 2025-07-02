from mcp.protocol import MessageBus
from agents.ingestion_agent import IngestionAgent
from agents.retrival_agent import RetrievalAgent
from agents.llm_response_agent import LLMResponseAgent

def rag_graph(file_path: str, user_query: str, trace_id: str):
    bus = MessageBus()
    ingestion_agent = IngestionAgent(bus)
    retrieval_agent = RetrievalAgent(bus)
    llm_agent = LLMResponseAgent(bus)

    ingestion_agent.run(file_path, trace_id)
    
    retrieval_agent.run()

    retrieval_agent.retrieve(user_query, trace_id)

    return llm_agent.run()
