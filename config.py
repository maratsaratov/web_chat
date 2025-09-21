import ssl
import os

class Config:
    SSL_CONTEXT = ssl.create_default_context()
    SSL_CONTEXT.check_hostname = False
    SSL_CONTEXT.verify_mode = ssl.CERT_NONE
    
    CREDENTIALS = "your_GigaChat_token"
    SESSION_TIMEOUT_HOURS = 24
    MAX_MESSAGES_PER_SESSION = 200
    
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = True