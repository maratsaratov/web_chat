# Chat Web Interface

Веб-интерфейс для взаимодействия с нейросетью GigaChat через Flask приложение.

## 🚀 Возможности

- 💬 Чат в реальном времени с GigaChat AI
- 🎨 Красивый и адаптивный интерфейс
- 🔄 Управление сессиями чата
- 💾 Сохранение истории сообщений
- ⏰ Автоматическая очистка неактивных сессий
- 🩺 Health-check эндпоинты для мониторинга

## Структура проекта

```
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
```

## 📋 Описание файлов

### Основные файлы
- **app.py** - Главный файл приложения, инициализация Flask app
- **config.py** - Конфигурационные параметры (credentials, настройки сервера)
- **requirements.txt** - Зависимости Python

### Модули
- **models/session.py** - Модель сессии чата с историей сообщений
- **routes/api.py** - API endpoints для работы с чатом и сессиями
- **routes/frontend.py** - HTML фронтенд с интерфейсом чата
- **services/gigachat_service.py** - Сервис для взаимодействия с GigaChat API
- **utils/session_manager.py** - Менеджер для управления сессиями пользователей

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