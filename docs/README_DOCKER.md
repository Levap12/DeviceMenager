# 🐳 Device Manager - Docker Quick Start

## ⚡ Быстрый запуск (3 команды)

```bash
# 1. Создайте config.env с вашим токеном
echo "TELEGRAM_BOT_TOKEN=ваш_токен" > config.env
echo "WEB_URL=http://localhost:8000" >> config.env
echo "API_URL=http://localhost:8000" >> config.env

# 2. Запустите Docker
docker-compose up -d

# 3. Откройте браузер
# http://localhost:8000
```

## 📦 Что включено?

✅ FastAPI сервер на порту 8000
✅ Автоматическая инициализация БД
✅ Telegram webhook поддержка
✅ Автоперезапуск при сбоях
✅ Сохранение данных в `./data/`

## 🔧 Основные команды

```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Логи
docker-compose logs -f

# Перезапуск
docker-compose restart

# Обновление
docker-compose down && docker-compose build && docker-compose up -d
```

## 📊 Проверка работы

```bash
# Статус контейнера
docker-compose ps

# Проверка здоровья
curl http://localhost:8000/

# Логи в реальном времени
docker-compose logs -f device-manager
```

## 🌐 Production развертывание

Для production с SSL и Nginx:

```bash
# Используйте production конфигурацию
docker-compose -f docker-compose.prod.yml up -d
```

Подробная инструкция: **DOCKER_SETUP.md**

## 🔐 Конфигурация

Файл `config.env`:
```env
TELEGRAM_BOT_TOKEN=6779117116:AAF...
WEB_URL=https://your-domain.com
API_URL=https://your-domain.com
```

## 🗂️ Структура данных

```
./data/
└── devices.db    # База данных SQLite (автоматически создается)
```

**Важно**: Директория `data/` сохраняется между перезапусками!

## 🚀 Развертывание на сервере

```bash
# 1. Скопируйте проект на сервер
scp -r * user@server:/opt/device-manager/

# 2. Подключитесь к серверу
ssh user@server

# 3. Перейдите в директорию
cd /opt/device-manager/

# 4. Создайте config.env с нужными параметрами
nano config.env

# 5. Запустите
docker-compose up -d

# Готово! Приложение доступно на порту 8000
```

## 🔄 Обновление на сервере

```bash
# Остановите контейнер
docker-compose down

# Обновите код (git pull или загрузите новые файлы)
git pull

# Пересоберите и запустите
docker-compose build --no-cache
docker-compose up -d
```

## 💾 Бэкап базы данных

```bash
# Создать бэкап
cp data/devices.db "backup_$(date +%Y%m%d).db"

# Восстановить
cp backup_20231015.db data/devices.db
docker-compose restart
```

## 🐛 Проблемы?

**Порт занят:**
```yaml
# В docker-compose.yml измените:
ports:
  - "8080:8000"  # Используйте другой порт
```

**Контейнер падает:**
```bash
# Смотрите логи
docker-compose logs device-manager
```

**База данных не создается:**
```bash
# Создайте директорию вручную
mkdir -p data
chmod 777 data
```

## 📝 Дополнительно

- Полная документация: `DOCKER_SETUP.md`
- Основной README: `README.md`
- Telegram бот: Автоматически работает через webhook

---

**Made with ❤️ using Docker + FastAPI + SQLite**

