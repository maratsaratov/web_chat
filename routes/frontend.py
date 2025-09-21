from flask import Blueprint

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def serve_frontend():
    """Отдает HTML фронтенд"""
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Чат с GigaChat</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                height: 100vh; 
                display: flex; 
                justify-content: center; 
                align-items: center; 
            }
            .chat-container { 
                width: 100%; max-width: 500px; height: 600px; 
                background: white; border-radius: 20px; 
                box-shadow: 0 20px 40px rgba(0,0,0,0.1); 
                display: flex; flex-direction: column; overflow: hidden; 
            }
            .chat-header { 
                background: #4a5568; color: white; padding: 20px; 
                text-align: center; font-weight: bold; font-size: 18px; 
            }
            .chat-messages { 
                flex: 1; padding: 20px; overflow-y: auto; 
                display: flex; flex-direction: column; gap: 15px; 
            }
            .message { 
                max-width: 80%; padding: 12px 16px; border-radius: 18px; 
                line-height: 1.4; animation: fadeIn 0.3s ease-in; 
            }
            .user-message { 
                align-self: flex-end; background: #667eea; color: white; 
                border-bottom-right-radius: 6px; 
            }
            .ai-message { 
                align-self: flex-start; background: #f7fafc; color: #2d3748; 
                border: 1px solid #e2e8f0; border-bottom-left-radius: 6px; 
            }
            .chat-input { 
                padding: 20px; background: #f7fafc; 
                border-top: 1px solid #e2e8f0; display: flex; gap: 10px; 
            }
            .message-input { 
                flex: 1; padding: 12px 16px; border: 2px solid #e2e8f0; 
                border-radius: 25px; outline: none; font-size: 14px; 
                transition: border-color 0.3s; 
            }
            .message-input:focus { border-color: #667eea; }
            .send-button { 
                padding: 12px 20px; background: #667eea; color: white; 
                border: none; border-radius: 25px; cursor: pointer; 
                font-weight: bold; transition: background 0.3s; 
            }
            .send-button:hover { background: #5a67d8; }
            .send-button:disabled { background: #cbd5e0; cursor: not-allowed; }
            .typing-indicator { 
                align-self: flex-start; background: #f7fafc; 
                padding: 12px 16px; border-radius: 18px; 
                border: 1px solid #e2e8f0; color: #718096; font-style: italic; 
            }
            .welcome-message { 
                text-align: center; color: #718096; margin-top: 50%; 
                padding: 20px; 
            }
            @keyframes fadeIn { 
                from { opacity: 0; transform: translateY(10px); } 
                to { opacity: 1; transform: translateY(0); } 
            }
            .chat-messages::-webkit-scrollbar { width: 6px; }
            .chat-messages::-webkit-scrollbar-track { background: #f1f1f1; }
            .chat-messages::-webkit-scrollbar-thumb { 
                background: #cbd5e0; border-radius: 3px; 
            }
            .chat-messages::-webkit-scrollbar-thumb:hover { background: #a0aec0; }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-header">💬 Чат с GigaChat</div>
            <div class="chat-messages" id="chatMessages">
                <div class="welcome-message">
                    Привет! Я ваш AI-ассистент. Задайте мне любой вопрос.
                </div>
            </div>
            <div class="chat-input">
                <input type="text" class="message-input" id="messageInput" 
                       placeholder="Введите ваше сообщение..." autocomplete="off">
                <button class="send-button" id="sendButton" disabled>Отправить</button>
            </div>
        </div>

        <script>
            class ChatApp {
                constructor() {
                    this.sessionId = null;
                    this.isTyping = false;
                    this.initializeElements();
                    this.initializeEventListeners();
                    this.createSession();
                }

                initializeElements() {
                    this.chatMessages = document.getElementById('chatMessages');
                    this.messageInput = document.getElementById('messageInput');
                    this.sendButton = document.getElementById('sendButton');
                }

                initializeEventListeners() {
                    this.sendButton.addEventListener('click', () => this.sendMessage());
                    this.messageInput.addEventListener('input', () => {
                        this.sendButton.disabled = !this.messageInput.value.trim();
                    });
                    this.messageInput.addEventListener('keypress', (e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                            e.preventDefault();
                            this.sendMessage();
                        }
                    });
                }

                async createSession() {
                    try {
                        const response = await fetch('/api/session/new', {
                            method: 'POST'
                        });
                        const data = await response.json();
                        if (data.success) {
                            this.sessionId = data.session_id;
                            console.log('Сессия создана:', this.sessionId);
                        }
                    } catch (error) {
                        console.error('Ошибка создания сессии:', error);
                        this.showError('Не удалось создать сессию');
                    }
                }

                async sendMessage() {
                    const message = this.messageInput.value.trim();
                    if (!message || !this.sessionId) return;

                    this.messageInput.value = '';
                    this.sendButton.disabled = true;

                    this.addMessage(message, 'user');
                    this.showTypingIndicator();

                    try {
                        const response = await fetch('/api/chat', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                session_id: this.sessionId,
                                message: message
                            })
                        });

                        const data = await response.json();
                        this.hideTypingIndicator();

                        if (data.success) {
                            this.addMessage(data.message, 'ai');
                        } else {
                            this.showError('Ошибка: ' + (data.error || 'Неизвестная ошибка'));
                        }
                    } catch (error) {
                        this.hideTypingIndicator();
                        console.error('Ошибка отправки сообщения:', error);
                        this.showError('Ошибка соединения с сервером');
                    }
                }

                addMessage(text, type) {
                    const messageDiv = document.createElement('div');
                    messageDiv.className = `message ${type}-message`;
                    messageDiv.textContent = text;
                    this.chatMessages.appendChild(messageDiv);
                    this.scrollToBottom();
                }

                showTypingIndicator() {
                    if (this.isTyping) return;
                    this.isTyping = true;
                    const typingDiv = document.createElement('div');
                    typingDiv.className = 'message typing-indicator';
                    typingDiv.textContent = 'AI печатает...';
                    typingDiv.id = 'typingIndicator';
                    this.chatMessages.appendChild(typingDiv);
                    this.scrollToBottom();
                }

                hideTypingIndicator() {
                    this.isTyping = false;
                    const typingIndicator = document.getElementById('typingIndicator');
                    if (typingIndicator) typingIndicator.remove();
                }

                showError(message) {
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'message ai-message';
                    errorDiv.style.color = '#e53e3e';
                    errorDiv.textContent = message;
                    this.chatMessages.appendChild(errorDiv);
                    this.scrollToBottom();
                }

                scrollToBottom() {
                    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
                }
            }

            document.addEventListener('DOMContentLoaded', () => {
                new ChatApp();
            });
        </script>
    </body>
    </html>
    """