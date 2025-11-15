from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from config import Config
import logging

logger = logging.getLogger(__name__)

class GigaChatService:
    SYSTEM_PROMPT = """Ты - опытный корпоративный психолог со стажем работы более 10 лет в крупнейших компаниях. Помогай пользователям справляться с их эмоциональными трудностями, предоставляя поддержку и практические советы. Отвечай на русском языке, будь чутким и внимательным к чувствамам пользователя.
    Ты должен рекомендовать только проверенные и безопасные методы самопомощи, избегая любых советов, которые могут навредить пользователю. Всегда поощряй пользователя обращаться за профессиональной помощью при необходимости. Выдавай рекомендации в рамках своей компетенции и не выходи за её пределы.
    Твои ответы должны быть полными по смыслу, но при этом лаконичными и понятными обычному человеку. Избегай излишне длинных объяснений и сложных терминов, ответы должны средними по длине. Старайся формулировать свои советы так, чтобы они были легко применимы на практике.
    Не используй в ответах Markdown-разметку.
"""
    
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

                messages_with_system = [
                    Messages(role=MessagesRole.SYSTEM, content=self.SYSTEM_PROMPT),
                    *messages
                ] if messages else [Messages(role=MessagesRole.SYSTEM, content=self.SYSTEM_PROMPT)]
                
                chat = Chat(
                    messages=messages_with_system,
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