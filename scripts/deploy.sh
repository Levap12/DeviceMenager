#!/bin/bash

# Скрипт быстрого развертывания Device Manager в Docker

set -e

echo "🐳 Device Manager - Быстрое развертывание"
echo "=========================================="
echo ""

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен!"
    echo "Установите Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose не установлен!"
    echo "Установите Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

# Проверка config.env
if [ ! -f "config.env" ]; then
    echo "⚠️  Файл config.env не найден!"
    echo "Создаем config.env..."
    
    read -p "Введите Telegram Bot Token: " BOT_TOKEN
    read -p "Введите URL сайта (например: https://your-domain.com): " WEB_URL
    
    cat > config.env << EOF
# Telegram Bot Token
TELEGRAM_BOT_TOKEN=${BOT_TOKEN}

# URLs
WEB_URL=${WEB_URL}
API_URL=${WEB_URL}
EOF
    
    echo "✅ Файл config.env создан!"
    echo ""
fi

# Создание директории для данных
mkdir -p data
chmod 755 data

echo "🔨 Сборка Docker образа..."
docker-compose build

echo ""
echo "🚀 Запуск контейнеров..."
docker-compose up -d

echo ""
echo "⏳ Ожидание запуска сервера..."
sleep 5

# Проверка статуса
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "✅ Device Manager успешно запущен!"
    echo ""
    echo "📊 Информация:"
    echo "   🌐 Веб-интерфейс: http://localhost:8000"
    echo "   📡 API документация: http://localhost:8000/docs"
    echo "   📱 Telegram webhook: http://localhost:8000/telegram/webhook"
    echo ""
    echo "📝 Полезные команды:"
    echo "   docker-compose logs -f         # Просмотр логов"
    echo "   docker-compose ps              # Статус контейнеров"
    echo "   docker-compose restart         # Перезапуск"
    echo "   docker-compose down            # Остановка"
    echo ""
else
    echo ""
    echo "❌ Ошибка запуска!"
    echo "Проверьте логи: docker-compose logs"
    exit 1
fi

