from mcp.protocol import MessageBus
from langchain_google_genai import ChatGoogleGenerativeAI

class LLMResponseAgent:
    def __init__(self, message_bus: MessageBus):
        self.bus = message_bus
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.1)

    def run(self):
        msg = self.bus.fetch(receiver="LLMResponseAgent", type="RETRIEVAL_RESULT")
        if not msg:
            return None

        context = msg.payload["retrieved_context"]
        query = msg.payload["query"]

        prompt = f"""You are answering based on these documents:\n\n{context}\n\nQuestion: {query}"""
        # print(f"🤖 LLM received query: {query}")

        response = self.llm.predict(prompt)

        # print(f"💬 LLM Response:\n{response}")
        return response
