# 🚀 Device Manager - Быстрое руководство

## ⚡ Запуск за 3 шага

### Windows:
```cmd
1. Дважды кликните: start.bat
2. Откройте браузер: http://localhost:8000
3. Готово! 🎉
```

### Linux/Mac:
```bash
1. python app/main.py
2. Откройте браузер: http://localhost:8000
3. Готово! 🎉
```

### Docker:
```bash
1. cd docker
2. docker-compose up -d
3. Откройте браузер: http://localhost:8000
4. Готово! 🎉
```

---

## 📋 Что где находится?

```
📱 Главная страница:         http://localhost:8000
📊 API документация:          http://localhost:8000/docs
🔧 Админка:                   http://localhost:8000/redoc
📱 Страница устройства:       http://localhost:8000/device-page/{id}
```

---

## 🤖 Настройка Telegram бота

### 1. Получите токен:
```
1. Напишите @BotFather в Telegram
2. Отправьте команду: /newbot
3. Следуйте инструкциям
4. Скопируйте токен (например: 6779117116:AAFlOu5e...)
```

### 2. Настройте config.env:
```env
TELEGRAM_BOT_TOKEN=6779117116:AAFlOu5eEt5eyf8cR7S3gK6kWk1fDGJfO_g
WEB_URL=https://your-domain.com
API_URL=https://your-domain.com
```

### 3. Команды бота:
```
/start            - Начать работу
/devices          - Показать все устройства
/add abc123       - Привязать устройство к чату
/remove abc123    - Отвязать устройство
/list             - Показать привязанные устройства
```

---

## 📡 Android приложение

### Формат JSON для отправки:

#### 1. Статус устройства:
```json
POST http://your-server:8000/event
{
  "type": "device_status",
  "timestamp": "15.10.2025 14:30:00",
  "device": {
    "name": "OnePlus GM1920",
    "id": "abc123",
    "battery": 45
  },
  "network": {
    "hasSignal": true,
    "signalStrength": 4,
    "networkType": "4G (LTE)",
    "canReceiveSms": true
  },
  "internet": {
    "connected": true,
    "type": "WiFi"
  }
}
```

#### 2. SMS:
```json
POST http://your-server:8000/event
{
  "type": "sms",
  "timestamp": "15.10.2025 14:32:00",
  "from": "+77051234567",
  "message": "Ваш код: 123456",
  "device": {
    "name": "OnePlus GM1920",
    "battery": 45
  }
}
```

#### 3. Перезагрузка:
```json
POST http://your-server:8000/event
{
  "type": "boot_completed",
  "timestamp": "15.10.2025 09:00:00",
  "device": {
    "name": "OnePlus GM1920",
    "id": "abc123",
    "battery": 78
  }
}
```

---

## 🔧 Полезные команды

### Запуск:
```bash
# Windows
start.bat

# Linux/Mac
python app/main.py

# Docker
cd docker && docker-compose up -d
```

### Остановка:
```bash
# Ctrl+C в консоли

# Docker
cd docker && docker-compose down
```

### Просмотр логов:
```bash
# Docker
cd docker && docker-compose logs -f

# Обычный запуск
# Логи выводятся в консоль
```

### Перезапуск:
```bash
# Docker
cd docker && docker-compose restart
```

---

## 📊 Структура проекта

```
DeviceManager/
├── app/                    # 📦 Основное приложение
│   ├── main.py            # ⭐ Главный файл (FastAPI)
│   ├── database.py        # База данных
│   └── telegram_bot.py    # Telegram бот
│
├── templates/             # 🎨 HTML страницы
│   ├── index.html         # Главная
│   └── device.html        # Страница устройства
│
├── docker/                # 🐳 Docker
├── docs/                  # 📚 Документация
├── scripts/               # 🔧 Скрипты
│
├── config.env             # ⚙️ Конфигурация
├── requirements.txt       # 📦 Зависимости
└── start.bat              # 🚀 Запуск (Windows)
```

---

## 🐛 Частые проблемы

### Проблема: Port 8000 already in use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

### Проблема: Telegram webhook conflict
```bash
python scripts/delete_webhook.py
```

### Проблема: SQLite database is locked
```bash
# Остановите все процессы приложения
# Удалите devices.db
# Перезапустите приложение
```

---

## 📖 Дополнительная документация

- **README.md** - Главная документация
- **PROJECT_STRUCTURE.md** - Подробная структура
- **STRUCTURE.txt** - ASCII дерево проекта
- **docs/API_DOCUMENTATION.md** - Полная документация API
- **docs/DOCKER_SETUP.md** - Docker инструкции
- **docs/TELEGRAM_BOT_SETUP.txt** - Настройка бота

---

## 💡 Советы

1. **Используйте ngrok** для тестирования webhook на локальной машине
2. **Регулярно делайте бэкап** `data/devices.db`
3. **Не коммитьте** `config.env` в Git (содержит токены!)
4. **Используйте Docker** для production развертывания
5. **Читайте логи** для отладки проблем

---

## 🎯 Что дальше?

1. ✅ Настройте `config.env`
2. ✅ Запустите сервер
3. ✅ Настройте Telegram бота
4. ✅ Добавьте первое устройство
5. ✅ Наслаждайтесь! 🎉

---

**💬 Вопросы?** Читайте полную документацию в папке `docs/`

**🐛 Проблемы?** Проверьте логи и раздел "Частые проблемы"

**🚀 Развертывание на сервере?** Читайте `docs/DOCKER_SETUP.md`

---

Made with ❤️ using FastAPI, SQLite, Tailwind CSS and aiogram

