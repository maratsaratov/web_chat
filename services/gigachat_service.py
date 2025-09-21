from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from config import Config
import logging

logger = logging.getLogger(__name__)

class GigaChatService:
    def __init__(self):
        self.credentials = Config.CREDENTIALS
        self.ssl_context = Config.SSL_CONTEXT
    
    def get_response(self, messages, temperature=0.7, max_tokens=1024):
        try:
            with GigaChat(
                credentials=self.credentials,
                ssl_context=self.ssl_context,
                verify_ssl_certs=False
            ) as giga:
                chat = Chat(
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    profanity_check=False
                )
                
                response = giga.chat(chat)
                return response.choices[0].message.content
                
        except Exception as e:
            logger.error(f"GigaChat error: {str(e)}")
            raise
    
    def health_check(self):
        try:
            with GigaChat(
                credentials=self.credentials,
                ssl_context=self.ssl_context,
                verify_ssl_certs=False
            ) as giga:
                test_chat = Chat(
                    messages=[Messages(role=MessagesRole.USER, content="Привет")],
                    max_tokens=10
                )
                response = giga.chat(test_chat)
                return True
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False
        
gigachat_service = GigaChatService()