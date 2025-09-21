# Chat Web Interface

Веб-интерфейс для взаимодействия с нейросетью GigaChat через Flask приложение.

## 🚀 Возможности

- 💬 Чат в реальном времени с GigaChat AI
- 🎨 Красивый и адаптивный интерфейс
- 🔄 Управление сессиями чата
- 💾 Сохранение истории сообщений
- ⏰ Автоматическая очистка неактивных сессий
- 🩺 Health-check эндпоинты для мониторинга

chat-app/
├── app.py                 # Главный файл приложения
├── config.py             # Конфигурационные параметры
├── requirements.txt      # Зависимости проекта
├── models/
│   ├── __init__.py
│   └── session.py       # Модель сессии чата
├── routes/
│   ├── __init__.py
│   ├── api.py           # API эндпоинты
│   └── frontend.py      # Frontend роуты
├── services/
│   ├── __init__.py
│   └── gigachat_service.py # Сервис работы с GigaChat
└── utils/
    ├── __init__.py
    └── session_manager.py  # Менеджер сессий

## 📦 Установка

```bash
# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate # Windows

# Установка зависимостей
pip install -r requirements.txt

# Запуск приложения
python app.py