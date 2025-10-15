# 📂 Device Manager - Визуальная структура проекта

## 🎯 Обзор структуры

```
┌─────────────────────────────────────────────────────────────────┐
│                   📱 DEVICE MANAGER                             │
│                                                                 │
│  Система управления Android устройствами                        │
│  FastAPI + SQLite + Telegram Bot + Web UI                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🗂️ Основные директории

```
DeviceManager/
│
├── 📦 app/                  ← ОСНОВНОЕ ПРИЛОЖЕНИЕ (Python)
├── 🎨 templates/            ← HTML СТРАНИЦЫ
├── 📁 static/               ← СТАТИКА (CSS, JS, изображения)
├── 🐳 docker/               ← DOCKER КОНФИГУРАЦИЯ
├── 📚 docs/                 ← ДОКУМЕНТАЦИЯ
├── 🔧 scripts/              ← УТИЛИТЫ И СКРИПТЫ
└── 💾 data/                 ← БАЗА ДАННЫХ (автосоздание)
```

---

## 📦 app/ - Ядро приложения

```
app/
├── __init__.py              # Инициализация модуля
│
├── ⭐ main.py               # ГЛАВНЫЙ ФАЙЛ - FastAPI сервер
│   ├── Роуты API
│   ├── Webhook Telegram
│   ├── HTML страницы
│   └── Обработка событий
│
├── database.py              # Работа с SQLite
│   ├── Создание таблиц
│   ├── CRUD операции
│   └── Привязки устройств
│
├── models.py                # Pydantic модели
│   └── Валидация данных
│
├── telegram_bot.py          # Telegram бот
│   ├── Команды: /start, /devices, /add, /remove
│   ├── Обработчики кнопок
│   └── Форматирование сообщений
│
└── telegram_notifications.py # Уведомления
    └── Отправка SMS в Telegram
```

### 🔗 Связи между модулями:

```
┌──────────────┐
│   main.py    │◄─────┐
└──────┬───────┘      │
       │              │
       ├──►┌──────────────┐
       │   │ database.py  │
       ├──►└──────────────┘
       │              ▲
       ├──►┌──────────┴───────────┐
       │   │ telegram_bot.py      │
       └──►└──────────────────────┘
                      │
                      ▼
           ┌──────────────────────┐
           │ telegram_notifications│
           └──────────────────────┘
```

---

## 🎨 templates/ - Веб-интерфейс

```
templates/
├── index.html               # 🏠 Главная страница
│   ├── Список устройств
│   ├── Статистика (онлайн/оффлайн)
│   ├── Цветовая индикация батареи
│   ├── Auto-refresh (10 сек)
│   └── Темная тема (Tailwind)
│
└── device.html              # 📱 Страница устройства
    ├── Детали устройства
    ├── Редактирование имени
    ├── Таблица SMS
    ├── Раскрытие длинных SMS
    └── Auto-refresh (10 сек)
```

### 🎨 UI Flow:

```
┌─────────────┐
│  index.html │
│  (Главная)  │
└──────┬──────┘
       │ клик на устройство
       ▼
┌─────────────────┐
│  device.html    │
│  (Устройство)   │
└─────────────────┘
       │
       ├── GET /device/{id}        ← Данные устройства
       └── GET /device/{id}/sms    ← SMS логи
```

---

## 🐳 docker/ - Контейнеризация

```
docker/
├── Dockerfile               # 📦 Образ приложения
│   ├── Python 3.11
│   ├── Установка зависимостей
│   └── Запуск приложения
│
├── docker-compose.yml       # 🔧 Development
│   ├── FastAPI сервер
│   ├── Volume для БД
│   └── Health check
│
├── docker-compose.prod.yml  # 🚀 Production
│   ├── FastAPI сервер
│   ├── Nginx reverse proxy
│   ├── SSL поддержка
│   └── Логирование
│
└── nginx.conf               # ⚙️ Nginx конфигурация
    ├── Proxy к FastAPI
    ├── WebSocket поддержка
    └── SSL настройки
```

### 🐳 Docker архитектура:

```
Development:
┌──────────────────┐
│  FastAPI:8000    │
└────────┬─────────┘
         │
         ▼
    ┌─────────┐
    │ SQLite  │
    └─────────┘

Production:
┌──────────────────┐
│   Nginx:80/443   │
└────────┬─────────┘
         │ reverse proxy
         ▼
┌──────────────────┐
│  FastAPI:8000    │
└────────┬─────────┘
         │
         ▼
    ┌─────────┐
    │ SQLite  │
    └─────────┘
```

---

## 📚 docs/ - Документация

```
docs/
├── README.md                # 📖 Основная документация
│   ├── Общее описание
│   ├── Установка
│   └── Использование
│
├── API_DOCUMENTATION.md     # 📡 API документация
│   ├── Все эндпоинты
│   ├── Примеры запросов
│   ├── Структура БД
│   └── Тестирование
│
├── DOCKER_SETUP.md          # 🐳 Docker инструкции
│   ├── Установка Docker
│   ├── Development setup
│   ├── Production setup
│   └── Troubleshooting
│
├── README_DOCKER.md         # 🚀 Docker быстрый старт
│   └── Краткая инструкция
│
└── TELEGRAM_BOT_SETUP.txt   # 🤖 Настройка бота
    ├── Создание бота
    ├── Webhook setup
    └── Команды
```

---

## 🔧 scripts/ - Утилиты

```
scripts/
├── deploy.sh                # 🚀 Автодеплой (Linux/Mac)
│   ├── Проверка Docker
│   ├── Создание config.env
│   ├── Сборка образа
│   └── Запуск контейнеров
│
├── setup.bat                # ⚙️ Настройка (Windows)
│   ├── Создание venv
│   ├── Установка зависимостей
│   ├── Создание config.env
│   └── Инициализация БД
│
└── delete_webhook.py        # 🗑️ Удаление webhook
    └── Решение конфликтов
```

---

## 💾 data/ - База данных

```
data/
└── devices.db               # 📊 SQLite база
    │
    ├── devices              # Таблица устройств
    │   ├── id (PK)
    │   ├── name
    │   ├── battery
    │   ├── signal_strength
    │   ├── network_type
    │   ├── internet
    │   ├── last_seen
    │   └── online
    │
    ├── events               # Таблица событий
    │   ├── id (PK)
    │   ├── device_id (FK)
    │   ├── type
    │   ├── timestamp
    │   └── data (JSON)
    │
    ├── sms_logs             # Таблица SMS
    │   ├── id (PK)
    │   ├── device_id (FK)
    │   ├── timestamp
    │   ├── sender
    │   └── message
    │
    └── device_chat_bindings # Привязки к чатам
        ├── id (PK)
        ├── device_id (FK)
        ├── chat_id
        └── created_at
```

### 📊 Связи в БД:

```
┌──────────┐         ┌─────────┐
│ devices  │◄────────┤ events  │
└────┬─────┘         └─────────┘
     │
     ├──────────────►┌──────────┐
     │               │ sms_logs │
     │               └──────────┘
     │
     └──────────────►┌──────────────────────┐
                     │ device_chat_bindings │
                     └──────────────────────┘
```

---

## 📄 Корневые файлы

```
DeviceManager/
│
├── ⭐ start.bat             # БЫСТРЫЙ ЗАПУСК (Windows)
├── README.md                # Главная документация
├── PROJECT_STRUCTURE.md     # Подробная структура
├── STRUCTURE.txt            # ASCII дерево
├── STRUCTURE_VISUAL.md      # Этот файл
├── QUICK_START_GUIDE.md     # Быстрое руководство
│
├── requirements.txt         # Python зависимости
├── config.env               # ⚠️ Конфигурация (НЕ КОММИТИТЬ!)
├── config.env.example       # Пример конфигурации
│
└── .gitignore              # Git исключения
```

---

## 🔄 Поток данных

```
┌─────────────┐
│   Android   │
│   Device    │
└──────┬──────┘
       │ POST /event
       │ (JSON)
       ▼
┌────────────────────────┐
│   FastAPI (main.py)    │
└──────┬────────┬────────┘
       │        │
       │        └──────────┐
       ▼                   ▼
┌──────────┐      ┌────────────────┐
│ SQLite   │      │ Telegram API   │
│   DB     │      │  (webhook)     │
└──────────┘      └────────────────┘
       │                   │
       │                   ▼
       │          ┌────────────────┐
       │          │ Telegram Users │
       │          └────────────────┘
       ▼
┌──────────┐
│  Web UI  │
│ Browser  │
└──────────┘
```

---

## 🎯 Точки входа

```
1. start.bat                      ← Windows пользователи
   └─► Автоматическая настройка и запуск

2. python app/main.py             ← Прямой запуск
   └─► Для разработки

3. docker-compose up              ← Docker развертывание
   └─► Для production

4. scripts/deploy.sh              ← Автоматический деплой
   └─► Для серверов
```

---

## 📊 Статистика проекта

```
Директории:   7
Файлы Python: 5
HTML файлы:   2
Документация: 9
Скрипты:      3
Docker файлы: 3

Строк кода:   ~3000+
API эндпоинты: 8
Команды бота:  5
Таблиц в БД:   4
```

---

## 🚀 Рекомендуемый порядок изучения

```
1. README.md                      ← Начните здесь
2. QUICK_START_GUIDE.md           ← Быстрый старт
3. STRUCTURE.txt                  ← ASCII дерево
4. app/main.py                    ← Главный код
5. templates/index.html           ← Веб-интерфейс
6. docs/API_DOCUMENTATION.md      ← API детали
7. docker/docker-compose.yml      ← Docker setup
```

---

## 💡 Советы по навигации

### Хотите понять API?
→ `docs/API_DOCUMENTATION.md`

### Хотите запустить быстро?
→ `start.bat` (Windows) или `python app/main.py`

### Хотите настроить Docker?
→ `docs/DOCKER_SETUP.md`

### Хотите кастомизировать веб-интерфейс?
→ `templates/*.html`

### Хотите добавить функционал бота?
→ `app/telegram_bot.py`

### Нужна структура БД?
→ `app/database.py` (функция `init_database()`)

---

## 🎨 Цветовая легенда

```
📦 = Python код
🎨 = Frontend (HTML/CSS/JS)
🐳 = Docker
📚 = Документация
🔧 = Утилиты/скрипты
💾 = Данные/база
⭐ = Важные файлы
⚠️ = Требует внимания
✅ = Готово к использованию
```

---

**🎯 Следующий шаг:** Откройте `QUICK_START_GUIDE.md` для быстрого старта!

Made with ❤️ for easy understanding and navigation

