import uuid
import logging
from datetime import datetime
from models import ChatSession

logger = logging.getLogger(__name__)

class SessionManager:
    def __init__(self):
        self.sessions = {}
    
    def create_session(self):
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = ChatSession(session_id)
        logger.info(f"Created new session: {session_id}")
        return session_id
    
    def get_session(self, session_id):
        if session_id in self.sessions:
            self.sessions[session_id].last_activity = datetime.now()
            return self.sessions[session_id]
        return None
    
    def delete_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Deleted session: {session_id}")
            return True
        return False
    
    def cleanup_old_sessions(self, timeout_hours):
        expired_sessions = []
        
        for session_id, session in self.sessions.items():
            if session.is_expired(timeout_hours):
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            self.delete_session(session_id)
            logger.info(f"Cleaned up expired session: {session_id}")

session_manager = SessionManager()