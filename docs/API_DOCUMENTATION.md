# 📡 API Documentation

## Base URL
```
http://localhost:8000
```

---

## 📱 Events API

### POST `/event`
Принимает JSON события от Android устройств.

**Типы событий:**
- `device_status` - статус устройства
- `sms` - SMS сообщение
- `boot_completed` - перезагрузка устройства

#### Пример 1: device_status
```json
{
  "type": "device_status",
  "timestamp": "15.10.2025 14:30:00",
  "device": {
    "name": "OnePlus GM1920",
    "id": "abd7b5e86a733e8c",
    "battery": 45
  },
  "network": {
    "hasSignal": true,
    "signalStrength": 4,
    "networkType": "4G (LTE) (Tele2)",
    "country": "KZ",
    "canReceiveSms": true
  },
  "internet": {
    "connected": true,
    "type": "Мобильные данные (4G (LTE))"
  }
}
```

#### Пример 2: sms
```json
{
  "type": "sms",
  "timestamp": "15.10.2025 14:32:00",
  "from": "+77051234567",
  "message": "Ваш код подтверждения: 123456",
  "device": {
    "name": "OnePlus GM1920",
    "battery": 45,
    "hasSignal": true,
    "signalStrength": 4,
    "networkType": "4G (LTE) (Tele2)",
    "internetConnected": true
  }
}
```

#### Пример 3: boot_completed
```json
{
  "type": "boot_completed",
  "timestamp": "15.10.2025 09:00:00",
  "device": {
    "name": "OnePlus GM1920",
    "id": "abd7b5e86a733e8c",
    "battery": 78
  },
  "network": {
    "hasSignal": true,
    "signalStrength": 3,
    "networkType": "4G (LTE) (Tele2)",
    "canReceiveSms": true
  },
  "internet": {
    "connected": true,
    "type": "Wi-Fi"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Событие device_status успешно обработано",
  "device_id": "abd7b5e86a733e8c"
}
```

---

## 📱 Devices API

### GET `/devices`
Получить список всех устройств.

**Response:**
```json
[
  {
    "id": "abd7b5e86a733e8c",
    "name": "OnePlus GM1920",
    "battery": 45,
    "signal_strength": 4,
    "network_type": "4G (LTE) (Tele2)",
    "internet": "Мобильные данные (4G (LTE))",
    "last_seen": "15.10.2025 14:30:00",
    "online": true
  }
]
```

**Online status:**
- `online: true` - последнее обновление < 20 минут назад
- `online: false` - последнее обновление > 20 минут назад

---

### GET `/device/{device_id}`
Получить информацию о конкретном устройстве.

**Parameters:**
- `device_id` (path) - ID устройства

**Response:**
```json
{
  "id": "abd7b5e86a733e8c",
  "name": "OnePlus GM1920",
  "battery": 45,
  "signal_strength": 4,
  "network_type": "4G (LTE) (Tele2)",
  "internet": "Мобильные данные (4G (LTE))",
  "last_seen": "15.10.2025 14:30:00",
  "online": true
}
```

**Error 404:**
```json
{
  "detail": "Устройство с ID xxx не найдено"
}
```

---

### PUT `/device/{device_id}/name`
Изменить имя устройства.

**Parameters:**
- `device_id` (path) - ID устройства

**Request Body:**
```json
{
  "name": "Новое имя устройства"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Имя устройства обновлено",
  "device_id": "abd7b5e86a733e8c",
  "name": "Новое имя устройства"
}
```

**Errors:**
- 404 - устройство не найдено
- 400 - имя пустое или слишком длинное (>100 символов)

---

## 💬 SMS API

### GET `/device/{device_id}/sms`
Получить все SMS сообщения устройства.

**Parameters:**
- `device_id` (path) - ID устройства

**Response:**
```json
[
  {
    "id": 1,
    "device_id": "abd7b5e86a733e8c",
    "timestamp": "15.10.2025 14:32:00",
    "sender": "+77051234567",
    "message": "Ваш код подтверждения: 123456"
  },
  {
    "id": 2,
    "device_id": "abd7b5e86a733e8c",
    "timestamp": "15.10.2025 15:00:00",
    "sender": "706",
    "message": "Баланс вашего счета: 1000 тг"
  }
]
```

---

## 🤖 Telegram Webhook API

### POST `/telegram/webhook`
Webhook для получения обновлений от Telegram Bot API.

**Note:** Этот эндпоинт используется автоматически Telegram серверами.

---

### GET `/telegram/webhook/info`
Получить информацию о текущем webhook.

**Response:**
```json
{
  "webhook_info": {
    "url": "https://your-domain.com/telegram/webhook",
    "has_custom_certificate": false,
    "pending_update_count": 0,
    "max_connections": 40,
    "ip_address": "1.2.3.4"
  }
}
```

---

## 🌐 Web Interface

### GET `/`
Главная страница - список всех устройств.

**Returns:** HTML страница

---

### GET `/device-page/{device_id}`
Страница конкретного устройства с SMS логами.

**Returns:** HTML страница

---

## 📊 Структура базы данных

### Таблица `devices`
```sql
CREATE TABLE devices (
    id TEXT PRIMARY KEY,
    name TEXT,
    battery INTEGER,
    signal_strength INTEGER,
    network_type TEXT,
    internet TEXT,
    last_seen TEXT,
    online INTEGER
)
```

### Таблица `events`
```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT,
    type TEXT,
    timestamp TEXT,
    data TEXT,
    FOREIGN KEY (device_id) REFERENCES devices (id)
)
```

### Таблица `sms_logs`
```sql
CREATE TABLE sms_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT,
    timestamp TEXT,
    sender TEXT,
    message TEXT,
    FOREIGN KEY (device_id) REFERENCES devices (id)
)
```

### Таблица `device_chat_bindings`
```sql
CREATE TABLE device_chat_bindings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT NOT NULL,
    chat_id INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE(device_id, chat_id),
    FOREIGN KEY (device_id) REFERENCES devices (id)
)
```

---

## 🔐 Безопасность

### Рекомендации:
1. **Используйте HTTPS** в production
2. **Ограничьте доступ к API** через firewall/IP whitelist
3. **Не храните токены в коде** - используйте переменные окружения
4. **Регулярно обновляйте зависимости**
5. **Делайте бэкапы базы данных**

---

## 🧪 Тестирование API

### С помощью curl:

```bash
# Отправить device_status
curl -X POST http://localhost:8000/event \
  -H "Content-Type: application/json" \
  -d '{
    "type": "device_status",
    "timestamp": "15.10.2025 14:30:00",
    "device": {"name": "Test Device", "id": "test123", "battery": 50},
    "network": {"hasSignal": true, "signalStrength": 4, "networkType": "4G"},
    "internet": {"connected": true, "type": "WiFi"}
  }'

# Получить список устройств
curl http://localhost:8000/devices

# Получить устройство
curl http://localhost:8000/device/test123

# Получить SMS
curl http://localhost:8000/device/test123/sms

# Изменить имя
curl -X PUT http://localhost:8000/device/test123/name \
  -H "Content-Type: application/json" \
  -d '{"name": "My New Device"}'
```

### С помощью Python:

```python
import requests

# Отправить событие
response = requests.post('http://localhost:8000/event', json={
    "type": "device_status",
    "timestamp": "15.10.2025 14:30:00",
    "device": {"name": "Test Device", "id": "test123", "battery": 50},
    "network": {"hasSignal": True, "signalStrength": 4, "networkType": "4G"},
    "internet": {"connected": True, "type": "WiFi"}
})
print(response.json())

# Получить устройства
devices = requests.get('http://localhost:8000/devices').json()
print(devices)
```

---

## 📝 Swagger/OpenAPI

Интерактивная документация доступна по адресу:
```
http://localhost:8000/docs
```

ReDoc документация:
```
http://localhost:8000/redoc
```

