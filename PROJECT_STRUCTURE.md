# 📂 Структура проекта Device Manager

```
DeviceManager/
│
├── 📦 app/                              # Основное приложение
│   ├── __init__.py                      # Инициализация модуля
│   ├── main.py                          # FastAPI сервер (главный файл)
│   ├── database.py                      # Работа с SQLite базой данных
│   ├── telegram_bot.py                  # Telegram бот (команды и обработчики)
│   └── telegram_notifications.py        # Модуль отправки уведомлений в Telegram
│
├── 🎨 templates/                        # HTML шаблоны
│   ├── index.html                       # Главная страница (список устройств)
│   └── device.html                      # Страница устройства (детали + SMS)
│
├── 🐳 docker/                           # Docker конфигурация
│   ├── Dockerfile                       # Docker образ приложения
│   ├── docker-compose.yml               # Development окружение
│   ├── docker-compose.prod.yml          # Production с Nginx и SSL
│   ├── nginx.conf                       # Конфигурация Nginx
│   └── .dockerignore                    # Исключения для Docker build
│
├── 📚 docs/                             # Документация
│   ├── README.md                        # Основная документация
│   ├── DOCKER_SETUP.md                  # Подробная инструкция по Docker
│   ├── README_DOCKER.md                 # Быстрый старт с Docker
│   └── TELEGRAM_BOT_SETUP.txt           # Настройка Telegram бота
│
├── 🔧 scripts/                          # Утилиты и скрипты
│   ├── deploy.sh                        # Автоматическое развертывание
│   └── delete_webhook.py                # Удаление Telegram webhook
│
├── 💾 data/                             # База данных (создается автоматически)
│   └── devices.db                       # SQLite база данных
│
├── 📝 Конфигурация и зависимости
│   ├── config.env                       # Конфигурация (создайте сами!)
│   ├── config.env.example               # Пример конфигурации
│   ├── requirements.txt                 # Python зависимости
│   ├── .gitignore                       # Git исключения
│   └── .dockerignore                    # Docker исключения
│
└── 📖 Документация корневого уровня
    ├── README.md                        # Главный README
    └── PROJECT_STRUCTURE.md             # Этот файл
```

## 📋 Описание компонентов

### 📦 app/ - Основное приложение

| Файл | Описание | Ключевые функции |
|------|----------|------------------|
| `main.py` | FastAPI сервер | API endpoints, webhook, роуты |
| `database.py` | БД слой | CRUD операции, SQLite |
| `telegram_bot.py` | Telegram бот | Команды, обработчики |
| `telegram_notifications.py` | Уведомления | Отправка SMS в Telegram |

### 🎨 templates/ - HTML шаблоны

| Файл | Описание | Особенности |
|------|----------|-------------|
| `index.html` | Главная страница | Список устройств, статистика |
| `device.html` | Страница устройства | Детали, SMS с раскрытием |

### 🐳 docker/ - Docker

| Файл | Назначение | Использование |
|------|------------|---------------|
| `Dockerfile` | Образ приложения | Сборка контейнера |
| `docker-compose.yml` | Development | Локальная разработка |
| `docker-compose.prod.yml` | Production | С Nginx, SSL, логами |
| `nginx.conf` | Nginx прокси | Reverse proxy, SSL |

### 📚 docs/ - Документация

| Файл | Содержание |
|------|------------|
| `README.md` | Полная документация API, установка |
| `DOCKER_SETUP.md` | Развертывание Docker, production |
| `README_DOCKER.md` | Быстрый старт с Docker |
| `TELEGRAM_BOT_SETUP.txt` | Настройка и команды бота |

### 🔧 scripts/ - Утилиты

| Скрипт | Назначение |
|--------|------------|
| `deploy.sh` | Автоматическое развертывание |
| `delete_webhook.py` | Удаление webhook (для отладки) |

## 🚀 Запуск

### Из корневой директории:

```bash
# Обычный запуск
python app/main.py

# Telegram бот (standalone)
python app/telegram_bot.py

# Docker
cd docker && docker-compose up -d
```

## 📊 Данные

```
data/
└── devices.db              # SQLite база
    ├── devices             # Таблица устройств
    ├── events              # Таблица событий
    ├── sms_logs            # Таблица SMS
    └── device_chat_bindings # Привязки устройств к Telegram чатам
```

## 🔐 Конфигурация

```
config.env                  # Создайте на основе config.env.example
├── TELEGRAM_BOT_TOKEN      # Токен от @BotFather
├── WEB_URL                 # URL веб-интерфейса
└── API_URL                 # URL API сервера
```

## 🎯 Точки входа

| Точка входа | Файл | Описание |
|-------------|------|----------|
| **FastAPI сервер** | `app/main.py` | Основной сервер с API и webhook |
| **Telegram бот** | `app/telegram_bot.py` | Standalone режим (polling) |
| **Docker** | `docker/docker-compose.yml` | Контейнеризация |
| **Deploy скрипт** | `scripts/deploy.sh` | Автоматизация развертывания |

## 📦 Зависимости

```
requirements.txt
├── fastapi                 # Web framework
├── uvicorn                 # ASGI server
├── aiogram                 # Telegram bot
├── pydantic                # Data validation
├── pytz                    # Timezone support
└── python-dotenv           # Environment variables
```

## 🔄 Workflow

```
1. Android устройство → POST /event → app/main.py
2. main.py → database.py → SQLite (devices.db)
3. main.py → telegram_notifications.py → Telegram API
4. Пользователь → Telegram бот → app/telegram_bot.py → database.py
5. Браузер → GET / → templates/index.html → API → database.py
```

## 🎨 Архитектура

```
┌─────────────┐
│   Android   │
│   Device    │
└──────┬──────┘
       │ POST /event
       ▼
┌─────────────────────────────────────┐
│         FastAPI (main.py)           │
│  ┌─────────────────────────────┐   │
│  │  API Routes                 │   │
│  │  - /event                   │   │
│  │  - /devices                 │   │
│  │  - /device/{id}             │   │
│  │  - /telegram/webhook        │   │
│  └─────────────────────────────┘   │
└────────┬────────────────────────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────────┐
│ SQLite │ │   Telegram   │
│   DB   │ │     Bot      │
└────────┘ └──────────────┘
    │              │
    ▼              ▼
┌────────┐    ┌─────────┐
│  Web   │    │ Telegram│
│  UI    │    │  Users  │
└────────┘    └─────────┘
```

---

**💡 Tip**: Начните изучение с `app/main.py` - это центральная точка приложения!

