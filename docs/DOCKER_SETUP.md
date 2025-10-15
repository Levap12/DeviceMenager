# 🐳 Docker Setup - Device Manager

Инструкция по развертыванию Device Manager с помощью Docker.

## 📋 Требования

- Docker 20.10+
- Docker Compose 2.0+

### Установка Docker (Ubuntu/Debian)

```bash
# Обновляем пакеты
sudo apt update

# Устанавливаем Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Добавляем пользователя в группу docker
sudo usermod -aG docker $USER

# Устанавливаем Docker Compose
sudo apt install docker-compose-plugin

# Перезаходим для применения изменений
newgrp docker
```

## 🚀 Быстрый старт

### 1. Создайте config.env

```bash
cat > config.env << EOF
# Telegram Bot Token
TELEGRAM_BOT_TOKEN=your_bot_token_here

# URLs (замените на ваш домен)
WEB_URL=https://your-domain.com
API_URL=https://your-domain.com
EOF
```

### 2. Запуск в режиме разработки

```bash
# Сборка и запуск
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

### 3. Запуск в production режиме

```bash
# Запуск с production конфигурацией
docker-compose -f docker-compose.prod.yml up -d

# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f
```

## 📦 Доступные команды

```bash
# Сборка образа
docker-compose build

# Запуск контейнеров
docker-compose up -d

# Остановка контейнеров
docker-compose down

# Перезапуск
docker-compose restart

# Просмотр логов
docker-compose logs -f device-manager

# Просмотр статуса
docker-compose ps

# Вход в контейнер
docker-compose exec device-manager bash

# Обновление (пересборка)
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 🔧 Структура проекта

```
DeviceManager/
├── Dockerfile                 # Основной Docker образ
├── docker-compose.yml         # Development конфигурация
├── docker-compose.prod.yml    # Production конфигурация
├── .dockerignore             # Исключения для Docker
├── nginx.conf                # Nginx конфигурация (для prod)
├── config.env                # Конфигурация (создайте сами!)
├── data/                     # База данных (автоматически)
│   └── devices.db
└── ...
```

## 🌐 Доступ к приложению

После запуска:
- **Веб-интерфейс**: http://localhost:8000
- **API документация**: http://localhost:8000/docs
- **Telegram webhook**: http://localhost:8000/telegram/webhook

## 🔐 Production с Nginx и SSL

### 1. Настройте nginx.conf

Отредактируйте `nginx.conf` и замените `your-domain.com` на ваш домен.

### 2. Получите SSL сертификат (Let's Encrypt)

```bash
# Установите certbot
sudo apt install certbot

# Получите сертификат
sudo certbot certonly --standalone -d your-domain.com

# Скопируйте сертификаты
mkdir -p ssl
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ssl/key.pem
sudo chmod 644 ssl/*.pem
```

### 3. Раскомментируйте SSL строки в nginx.conf

```nginx
ssl_certificate /etc/nginx/ssl/cert.pem;
ssl_certificate_key /etc/nginx/ssl/key.pem;
```

### 4. Запустите production режим

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 📊 Мониторинг

### Проверка здоровья контейнера

```bash
docker-compose ps
```

### Просмотр логов

```bash
# Все логи
docker-compose logs -f

# Только FastAPI
docker-compose logs -f device-manager

# Только Nginx (в prod режиме)
docker-compose -f docker-compose.prod.yml logs -f nginx
```

### Статистика ресурсов

```bash
docker stats device-manager
```

## 🔄 Обновление приложения

```bash
# 1. Остановите контейнеры
docker-compose down

# 2. Обновите код (git pull или загрузите новые файлы)
git pull

# 3. Пересоберите образ
docker-compose build --no-cache

# 4. Запустите снова
docker-compose up -d
```

**Важно**: База данных сохраняется в `./data/` и не удаляется при обновлении!

## 🗄️ Резервное копирование базы данных

```bash
# Создание бэкапа
docker-compose exec device-manager cp /app/data/devices.db /app/data/devices.db.backup
cp data/devices.db "backups/devices_$(date +%Y%m%d_%H%M%S).db"

# Восстановление из бэкапа
cp backups/devices_20231015_120000.db data/devices.db
docker-compose restart
```

## 🐛 Устранение проблем

### Контейнер не запускается

```bash
# Проверьте логи
docker-compose logs device-manager

# Проверьте конфигурацию
docker-compose config
```

### База данных не сохраняется

```bash
# Убедитесь что директория data существует
mkdir -p data

# Проверьте права доступа
sudo chown -R 1000:1000 data
```

### Порт 8000 занят

Измените порт в `docker-compose.yml`:
```yaml
ports:
  - "8080:8000"  # Внешний:Внутренний
```

## 🔒 Безопасность

1. **Никогда не коммитьте config.env в git!**
2. Используйте SSL в production
3. Ограничьте доступ к API через firewall
4. Регулярно обновляйте Docker образы

```bash
# Обновление базового образа
docker-compose pull
docker-compose up -d
```

## 📝 Переменные окружения

Все переменные в `config.env`:

```env
# Обязательные
TELEGRAM_BOT_TOKEN=your_token_here
WEB_URL=https://your-domain.com
API_URL=https://your-domain.com

# Опциональные
DATABASE_PATH=/app/data/devices.db
```

## 🎉 Готово!

Ваше приложение работает в Docker!
- Легко развертывается на любом сервере
- Автоматический перезапуск при сбоях
- Изолированное окружение
- Простое обновление

Для удаленного сервера просто скопируйте файлы и запустите:
```bash
scp -r * user@your-server:/path/to/app/
ssh user@your-server
cd /path/to/app/
docker-compose up -d
```

