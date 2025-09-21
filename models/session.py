from datetime import datetime
from gigachat.models import Messages, MessagesRole

class ChatSession:
    def __init__(self, session_id):
        self.session_id = session_id
        self.messages = []
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
    
    def add_message(self, role, content):
        message = Messages(role=role, content=content)
        self.messages.append(message)
        self.last_activity = datetime.now()
        
        if len(self.messages) > 20:
            self.messages = self.messages[-20:]
    
    def get_chat_history(self):
        return self.messages
    
    def clear_history(self):
        self.messages = []
        self.last_activity = datetime.now()
    
    def is_expired(self, timeout_hours):
        return (datetime.now() - self.last_activity).total_seconds() > timeout_hours * 3600