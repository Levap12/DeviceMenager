# 📱 Device Manager

Система управления Android устройствами с веб-интерфейсом и Telegram ботом.

## ✨ Возможности

- 📊 **Мониторинг устройств** - статус, батарея, сигнал, сеть
- 💬 **SMS логи** - все SMS сообщения с устройств
- 🤖 **Telegram бот** - уведомления и управление через Telegram
- 🌐 **Веб-интерфейс** - красивый dashboard с автообновлением
- 🐳 **Docker** - легкое развертывание на любом сервере
- 🔐 **API** - REST API для интеграций

## 🚀 Быстрый старт

### Вариант 1: Docker (рекомендуется)

```bash
# 1. Клонируйте репозиторий
git clone <repo-url>
cd DeviceManager

# 2. Создайте config.env
cp config.env.example config.env
# Отредактируйте config.env и добавьте ваш Telegram Bot Token

# 3. Запустите
cd docker
docker-compose up -d

# 4. Откройте http://localhost:8000
```

### Вариант 2: Без Docker

```bash
# 1. Установите зависимости
pip install -r requirements.txt

# 2. Создайте config.env
cp config.env.example config.env

# 3. Запустите
python app/main.py

# 4. Откройте http://localhost:8000
```

## 📂 Структура проекта

```
DeviceManager/
├── app/                          # Основное приложение
│   ├── __init__.py
│   ├── main.py                   # FastAPI сервер
│   ├── database.py               # Работа с SQLite
│   ├── telegram_bot.py           # Telegram бот
│   └── telegram_notifications.py # Уведомления
│
├── templates/                    # HTML шаблоны
│   ├── index.html               # Главная страница
│   └── device.html              # Страница устройства
│
├── docker/                       # Docker конфигурация
│   ├── Dockerfile
│   ├── docker-compose.yml       # Development
│   ├── docker-compose.prod.yml  # Production
│   ├── nginx.conf               # Nginx для prod
│   └── .dockerignore
│
├── docs/                         # Документация
│   ├── README.md                # Подробная документация
│   ├── DOCKER_SETUP.md          # Docker инструкция
│   └── README_DOCKER.md         # Docker quick start
│
├── scripts/                      # Утилиты
│   ├── deploy.sh                # Скрипт развертывания
│   └── delete_webhook.py        # Удаление Telegram webhook
│
├── data/                         # База данных (создается автоматически)
│   └── devices.db
│
├── config.env                    # Конфигурация (создайте сами!)
├── config.env.example           # Пример конфигурации
├── requirements.txt             # Python зависимости
├── .gitignore
└── README.md                    # Этот файл
```

## 📡 API Endpoints

### Прием событий
- `POST /event` - Прием событий от устройств

### Устройства
- `GET /devices` - Список всех устройств
- `GET /device/{id}` - Информация об устройстве
- `PUT /device/{id}/name` - Изменить имя устройства

### SMS
- `GET /device/{id}/sms` - SMS устройства

### Telegram Webhook
- `POST /telegram/webhook` - Webhook для Telegram бота
- `GET /telegram/webhook/info` - Информация о webhook

### Веб-интерфейс
- `GET /` - Главная страница
- `GET /device-page/{id}` - Страница устройства

## 🤖 Telegram Бот

### Команды:
- `/start` - Приветствие и список устройств
- `/devices` - Показать все устройства
- `/add <device_id>` - Привязать устройство к чату
- `/remove <device_id>` - Отвязать устройство
- `/list` - Показать привязанные устройства

### Настройка:
1. Создайте бота через @BotFather
2. Добавьте токен в `config.env`
3. Запустите приложение - webhook настроится автоматически

## 🔧 Конфигурация

Файл `config.env`:
```env
TELEGRAM_BOT_TOKEN=your_token_here
WEB_URL=https://your-domain.com
API_URL=https://your-domain.com
```

## 📊 Технологии

- **Backend**: Python 3.11, FastAPI, SQLite
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Bot**: aiogram 3.x
- **Deploy**: Docker, Docker Compose, Nginx

## 📖 Документация

- [Подробная документация](docs/README.md)
- [Docker Setup](docs/DOCKER_SETUP.md)
- [Docker Quick Start](docs/README_DOCKER.md)

## 🔐 Безопасность

- Не коммитьте `config.env` в git
- Используйте SSL в production
- Ограничьте доступ через firewall
- Регулярно делайте бэкапы БД

## 📝 Лицензия

MIT License

## 👨‍💻 Автор

Created with ❤️ using FastAPI, SQLite, Tailwind CSS and aiogram

---

**[📚 Документация](docs/)** | **[🐳 Docker](docker/)** | **[🤖 Telegram Bot](docs/TELEGRAM_BOT_SETUP.txt)**
