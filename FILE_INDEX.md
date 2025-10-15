# 📑 Device Manager - Индекс файлов

## 📂 Полный список файлов проекта

### 🔴 Корневая директория

| Файл | Описание | Тип |
|------|----------|-----|
| `start.bat` | **⭐ ЗАПУСК** - Главный скрипт запуска (Windows) | Executable |
| `README.md` | **⭐ ДОКУМЕНТАЦИЯ** - Главная документация проекта | Documentation |
| `QUICK_START_GUIDE.md` | **⭐ ГАЙД** - Быстрое руководство для начала работы | Documentation |
| `PROJECT_STRUCTURE.md` | Подробное описание структуры проекта | Documentation |
| `STRUCTURE.txt` | ASCII-дерево структуры проекта | Documentation |
| `STRUCTURE_VISUAL.md` | Визуальное представление структуры | Documentation |
| `FILE_INDEX.md` | Этот файл - индекс всех файлов | Documentation |
| `requirements.txt` | Python зависимости проекта | Configuration |
| `config.env` | **⚠️ ВАЖНО** - Конфигурация (токены, URLs) | Configuration |
| `config.env.example` | Пример конфигурации | Configuration |
| `.gitignore` | Git исключения | Configuration |

---

### 📦 app/ - Основное приложение

| Файл | Описание | Строк | Важность |
|------|----------|-------|----------|
| `__init__.py` | Инициализация Python модуля | ~4 | Low |
| `main.py` | **⭐⭐⭐ ГЛАВНЫЙ ФАЙЛ** - FastAPI сервер, все API эндпоинты | ~420 | Critical |
| `database.py` | **⭐⭐⭐ БАЗА ДАННЫХ** - SQLite операции, CRUD | ~300 | Critical |
| `models.py` | Pydantic модели для валидации данных | ~50 | Medium |
| `telegram_bot.py` | **⭐⭐ ТЕЛЕГРАМ БОТ** - Команды, обработчики | ~350 | High |
| `telegram_notifications.py` | **⭐⭐ УВЕДОМЛЕНИЯ** - Отправка SMS в Telegram | ~80 | High |

#### 🔗 Зависимости между файлами:
```
main.py
├── import database
├── import telegram_bot
└── import telegram_notifications
    └── import database

telegram_bot.py
└── import database
```

---

### 🎨 templates/ - HTML шаблоны

| Файл | Описание | Строк | Features |
|------|----------|-------|----------|
| `index.html` | **⭐⭐ ГЛАВНАЯ СТРАНИЦА** - Список всех устройств | ~250 | Tailwind CSS, Auto-refresh, Dark theme |
| `device.html` | **⭐⭐ СТРАНИЦА УСТРОЙСТВА** - Детали устройства + SMS | ~380 | Collapsible SMS, Edit name, Auto-refresh |

#### 🎨 Features:
- ✨ Tailwind CSS для стилизации
- ✨ Темная тема
- ✨ Автообновление каждые 10 секунд
- ✨ Responsive design (адаптивный дизайн)
- ✨ Цветовая индикация (батарея, статус)
- ✨ Анимации и transitions

---

### 🐳 docker/ - Docker конфигурация

| Файл | Описание | Использование |
|------|----------|---------------|
| `Dockerfile` | **⭐ ОБРАЗ** - Docker образ приложения | `docker build` |
| `docker-compose.yml` | **⭐ DEV** - Development окружение | `docker-compose up` |
| `docker-compose.prod.yml` | **⭐ PROD** - Production с Nginx | Production deploy |
| `nginx.conf` | Конфигурация Nginx reverse proxy | Production only |

#### 🐳 Команды:
```bash
# Development
cd docker
docker-compose up -d

# Production
cd docker
docker-compose -f docker-compose.prod.yml up -d
```

---

### 📚 docs/ - Документация

| Файл | Описание | Для кого |
|------|----------|----------|
| `README.md` | Основная документация проекта | Все |
| `API_DOCUMENTATION.md` | **⭐⭐⭐ API DOCS** - Полная документация API | Разработчики |
| `DOCKER_SETUP.md` | Подробная инструкция по Docker | DevOps |
| `README_DOCKER.md` | Быстрый старт с Docker | Новички |
| `TELEGRAM_BOT_SETUP.txt` | Настройка Telegram бота | Администраторы |

#### 📖 Что читать:
1. Новичкам → `README.md`
2. Разработчикам → `API_DOCUMENTATION.md`
3. DevOps → `DOCKER_SETUP.md`
4. Телеграм → `TELEGRAM_BOT_SETUP.txt`

---

### 🔧 scripts/ - Утилиты и скрипты

| Файл | Описание | Платформа |
|------|----------|-----------|
| `deploy.sh` | **⭐ ДЕПЛОЙ** - Автоматическое развертывание | Linux/Mac |
| `setup.bat` | **⭐ НАСТРОЙКА** - Первоначальная настройка | Windows |
| `delete_webhook.py` | Удаление Telegram webhook | Все |

#### 🔧 Когда использовать:
- `setup.bat` - При первом запуске на Windows
- `deploy.sh` - При развертывании на Linux сервере
- `delete_webhook.py` - При ошибке "webhook conflict"

---

### 💾 data/ - База данных

| Файл | Описание | Размер | Бэкап |
|------|----------|--------|-------|
| `devices.db` | **⚠️ БАЗА ДАННЫХ** - SQLite база | ~100KB+ | Обязательно! |

#### 📊 Таблицы:
1. `devices` - Устройства (id, name, battery, etc.)
2. `events` - Все события (device_status, sms, boot)
3. `sms_logs` - SMS сообщения
4. `device_chat_bindings` - Привязки к Telegram чатам

---

### 📁 static/ - Статические файлы

| Статус | Описание |
|--------|----------|
| 📁 Пустая | Резерв для CSS, JS, изображений |

---

### 🔒 Системные папки (игнорируются)

| Папка | Описание | В Git? |
|-------|----------|--------|
| `venv/` | Python виртуальное окружение | ❌ Нет |
| `__pycache__/` | Скомпилированные Python файлы | ❌ Нет |
| `.idea/` | PyCharm конфигурация | ❌ Нет |

---

## 🎯 Файлы по важности

### ⭐⭐⭐ Критически важные:
1. `app/main.py` - Главный файл, FastAPI сервер
2. `app/database.py` - Работа с базой данных
3. `data/devices.db` - База данных (ДЕЛАЙТЕ БЭКАП!)
4. `config.env` - Конфигурация (НЕ КОММИТИТЬ!)

### ⭐⭐ Очень важные:
5. `app/telegram_bot.py` - Telegram бот
6. `app/telegram_notifications.py` - Уведомления
7. `templates/index.html` - Главная страница
8. `templates/device.html` - Страница устройства
9. `start.bat` - Скрипт запуска
10. `README.md` - Документация

### ⭐ Важные:
11. `docker/Dockerfile` - Docker образ
12. `docker/docker-compose.yml` - Docker compose
13. `docs/API_DOCUMENTATION.md` - API docs
14. `requirements.txt` - Зависимости
15. `scripts/deploy.sh` - Деплой скрипт

---

## 📊 Статистика проекта

```
Всего файлов:     ~30
Python файлов:    6
HTML файлов:      2
Docker файлов:    4
Документации:     10
Скриптов:         3
Конфигураций:     5

Всего строк кода: ~3500+
Размер проекта:   ~500KB (без venv)
```

---

## 🔍 Как найти нужный файл?

### Хочу изменить...

**...внешний вид сайта:**
→ `templates/index.html` или `templates/device.html`

**...API эндпоинты:**
→ `app/main.py`

**...структуру базы данных:**
→ `app/database.py` (функция `init_database()`)

**...команды Telegram бота:**
→ `app/telegram_bot.py`

**...логику уведомлений:**
→ `app/telegram_notifications.py`

**...Docker конфигурацию:**
→ `docker/docker-compose.yml` или `docker/Dockerfile`

**...зависимости проекта:**
→ `requirements.txt`

**...настройки (токены, URLs):**
→ `config.env`

---

## 🚀 Порядок изучения файлов

### Для начинающих:
```
1. README.md                      ← Обзор проекта
2. QUICK_START_GUIDE.md           ← Быстрый старт
3. start.bat                      ← Запуск
4. config.env.example             ← Настройка
5. templates/index.html           ← Веб-интерфейс
```

### Для разработчиков:
```
1. app/main.py                    ← Главная логика
2. app/database.py                ← База данных
3. app/models.py                  ← Модели данных
4. docs/API_DOCUMENTATION.md      ← API docs
5. app/telegram_bot.py            ← Telegram бот
```

### Для DevOps:
```
1. docker/Dockerfile              ← Образ
2. docker/docker-compose.yml      ← Compose
3. docker/nginx.conf              ← Nginx
4. docs/DOCKER_SETUP.md           ← Инструкции
5. scripts/deploy.sh              ← Деплой
```

---

## 📝 Чеклист файлов перед деплоем

- [ ] `config.env` создан и заполнен
- [ ] `requirements.txt` актуален
- [ ] `data/` директория создана
- [ ] `.gitignore` настроен правильно
- [ ] `docker/docker-compose.yml` проверен
- [ ] Все Python файлы без ошибок
- [ ] HTML файлы валидны
- [ ] Документация актуальна

---

## 🎨 Легенда

| Символ | Значение |
|--------|----------|
| ⭐ | Важный файл |
| ⭐⭐ | Очень важный файл |
| ⭐⭐⭐ | Критически важный файл |
| ⚠️ | Требует осторожности |
| ✅ | Готово к использованию |
| 📦 | Python код |
| 🎨 | Frontend |
| 🐳 | Docker |
| 📚 | Документация |
| 🔧 | Утилита |
| 💾 | Данные |

---

**💡 Совет:** Добавьте эту страницу в закладки для быстрой навигации по проекту!

---

Made with ❤️ for better project organization

