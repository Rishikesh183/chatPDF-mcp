from typing import Dict, Any
import uuid
import datetime

class MCPMessage:
    def __init__(self, sender: str, receiver: str, type: str, payload: Dict[str, Any], trace_id: str = None):
        self.sender = sender
        self.receiver = receiver
        self.type = type
        self.payload = payload
        self.trace_id = trace_id or str(uuid.uuid4())
        self.timestamp = datetime.datetime.utcnow().isoformat()

    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "type": self.type,
            "trace_id": self.trace_id,
            "timestamp": self.timestamp,
            "payload": self.payload
        }

    def __repr__(self):
        return f"MCPMessage({self.to_dict()})"

class MessageBus:
    def __init__(self):
        self.messages = []

    def send(self, message: MCPMessage):
        # print(f"🔁 Message sent: {message}")
        self.messages.append(message)

    def fetch(self, receiver: str, type: str = None):
        for msg in self.messages:
            if msg.receiver == receiver and (type is None or msg.type == type):
                self.messages.remove(msg)
                return msg
        return None
