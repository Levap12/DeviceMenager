# 🚀 Инструкция по развертыванию Device Manager

## 📋 Быстрое развертывание на сервере

### 1. Клонирование репозитория

```bash
# Клонируйте проект
git clone https://github.com/YOUR_USERNAME/DeviceManager.git /opt/device-manager
cd /opt/device-manager
```

### 2. Создание конфигурации

```bash
# Создайте config.env
nano config.env
```

Вставьте:
```env
# Telegram Bot Token (получите у @BotFather)
TELEGRAM_BOT_TOKEN=your_bot_token_here

# URL вашего веб-интерфейса
WEB_URL=https://your-domain.com

# URL API сервера
API_URL=https://your-domain.com
```

Сохраните: `Ctrl+O`, `Enter`, `Ctrl+X`

### 3. Установка зависимостей

#### Вариант A: Docker (рекомендуется)

```bash
# Установите Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установите Docker Compose
sudo apt update
sudo apt install docker-compose-plugin

# Запустите проект
cd docker
sudo docker compose up -d

# Проверьте логи
sudo docker compose logs -f
```

#### Вариант B: Без Docker

```bash
# Установите Python зависимости
sudo apt update
sudo apt install -y python3-pip python3-venv

# Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Запустите приложение
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 4. Настройка Nginx + SSL

```bash
# Установите Nginx
sudo apt install nginx

# Создайте конфигурацию
sudo nano /etc/nginx/sites-available/device-manager
```

Вставьте:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

```bash
# Активируйте конфигурацию
sudo ln -s /etc/nginx/sites-available/device-manager /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# Получите SSL сертификат
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 5. Настройка firewall

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 6. Проверка

```bash
# Проверьте что приложение работает
curl http://localhost:8000

# Откройте в браузере
# https://your-domain.com
```

---

## 🌐 Настройка бесплатного домена (DuckDNS)

1. Зарегистрируйтесь на https://www.duckdns.org
2. Создайте поддомен (например: `mydevices.duckdns.org`)
3. Укажите IP вашего сервера
4. Используйте этот домен в `config.env`:
   ```env
   WEB_URL=https://mydevices.duckdns.org
   API_URL=https://mydevices.duckdns.org
   ```

---

## 🔧 Полезные команды

### Docker

```bash
# Просмотр логов
cd /opt/device-manager/docker
sudo docker compose logs -f

# Перезапуск
sudo docker compose restart

# Остановка
sudo docker compose down

# Обновление (после git pull)
sudo docker compose down
sudo docker compose build --no-cache
sudo docker compose up -d
```

### Без Docker

```bash
# Запуск в фоне с помощью screen
sudo apt install screen
screen -S devicemanager
cd /opt/device-manager
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Отсоединиться: Ctrl+A затем D
# Вернуться: screen -r devicemanager
```

---

## 🐛 Решение проблем

### Приложение не запускается

```bash
# Проверьте логи
cd /opt/device-manager/docker
sudo docker compose logs

# Пересоберите образ
sudo docker compose down
sudo docker compose build --no-cache
sudo docker compose up -d
```

### Nginx показывает welcome page

```bash
# Проверьте конфигурацию
sudo nginx -t

# Проверьте что FastAPI работает
curl http://localhost:8000

# Перезапустите Nginx
sudo systemctl restart nginx
```

### Telegram webhook не работает

```bash
# Убедитесь что у вас HTTPS
# Webhook требует SSL сертификат!

# Проверьте webhook
curl https://api.telegram.org/bot<YOUR_TOKEN>/getWebhookInfo

# Удалите webhook (если нужно)
python scripts/delete_webhook.py
```

---

## 📊 Мониторинг

```bash
# Статус Docker контейнера
sudo docker ps

# Логи в реальном времени
sudo docker compose logs -f

# Статус Nginx
sudo systemctl status nginx

# Использование портов
sudo ss -tlnp | grep -E ':80|:443|:8000'
```

---

## 🔄 Обновление проекта

```bash
cd /opt/device-manager

# Получите последние изменения
git pull

# Перезапустите Docker
cd docker
sudo docker compose down
sudo docker compose build --no-cache
sudo docker compose up -d

# Или без Docker
source venv/bin/activate
pip install -r requirements.txt
# Перезапустите uvicorn
```

---

**💡 Совет:** Используйте DuckDNS для бесплатного домена и Let's Encrypt для бесплатного SSL!

