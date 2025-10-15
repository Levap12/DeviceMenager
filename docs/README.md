# Device Manager - Система управления Android устройствами

Backend-сервер на Python + FastAPI + SQLite для приема и отображения данных от Android-устройств.

## 🚀 Возможности

- **Прием событий** от Android устройств (device_status, sms, boot_completed)
- **Хранение данных** в SQLite базе данных
- **REST API** для получения информации об устройствах и SMS
- **Веб-интерфейс** с автообновлением каждые 10 секунд
- **Автоопределение статуса** онлайн/оффлайн (< 20 минут)
- **Красивый UI** на Tailwind CSS в темном стиле

## 📋 Требования

- Python 3.8+
- pip

## 🔧 Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Запустите сервер:
```bash
python main.py
```

Сервер будет доступен по адресу: `http://localhost:8000`

## 📡 API Endpoints

### POST /event
Принимает события от устройств

**Пример device_status:**
```json
{
  "type": "device_status",
  "timestamp": "14.10.2025 12:00:00",
  "device": {
    "name": "OnePlus GM1920",
    "id": "abd7b5e86a733e8c",
    "battery": 85
  },
  "network": {
    "hasSignal": true,
    "signalStrength": 3,
    "networkType": "4G (LTE) (Tele2)",
    "country": "KZ",
    "canReceiveSms": true
  },
  "internet": {
    "connected": true,
    "type": "WiFi"
  }
}
```

**Пример sms:**
```json
{
  "type": "sms",
  "timestamp": "14.10.2025 12:00:00",
  "from": "+77053161050",
  "message": "Привет, как дела?",
  "device": {
    "name": "OnePlus GM1920",
    "battery": 82,
    "hasSignal": true,
    "signalStrength": 3,
    "networkType": "4G (LTE)",
    "internetConnected": true
  }
}
```

**Пример boot_completed:**
```json
{
  "type": "boot_completed",
  "timestamp": "14.10.2025 12:00:00",
  "device": {
    "name": "OnePlus GM1920",
    "id": "abd7b5e86a733e8c",
    "battery": 78
  },
  "network": {
    "hasSignal": true,
    "signalStrength": 2,
    "networkType": "4G (LTE)",
    "canReceiveSms": true
  },
  "internet": {
    "connected": true,
    "type": "Мобильные данные (4G)"
  }
}
```

### GET /devices
Получить список всех устройств

**Ответ:**
```json
{
  "status": "success",
  "count": 1,
  "devices": [
    {
      "id": "device_001",
      "name": "Мой телефон",
      "battery": 85,
      "signal_strength": 75,
      "network_type": "4G",
      "internet": "WiFi",
      "last_seen": "2025-10-14T12:00:00",
      "online": true
    }
  ]
}
```

### GET /device/{id}
Получить информацию о конкретном устройстве

### GET /device/{id}/sms
Получить список SMS для устройства

## 🎨 Веб-интерфейс

- **Главная страница** (`/`) - список всех устройств
- **Страница устройства** (`/device-page/{id}`) - детальная информация и SMS

### Особенности UI:

- ✅ Цветовая индикация заряда батареи (красный < 20%, желтый 20-50%, зеленый > 50%)
- ✅ Статус онлайн/оффлайн с цветными индикаторами 🟢🔴
- ✅ Автообновление данных каждые 10 секунд
- ✅ Спиннер загрузки
- ✅ Темный дизайн с Tailwind CSS
- ✅ Серая подсветка оффлайн устройств

## 🗄️ Структура базы данных

### devices
- `id` (TEXT) - уникальный идентификатор устройства
- `name` (TEXT) - название устройства
- `battery` (INTEGER) - уровень заряда
- `signal_strength` (INTEGER) - уровень сигнала
- `network_type` (TEXT) - тип сети
- `internet` (TEXT) - тип подключения
- `last_seen` (TEXT) - время последнего события
- `online` (BOOLEAN) - статус онлайн/оффлайн

### events
- `id` (INTEGER) - автоинкремент
- `device_id` (TEXT) - ID устройства
- `type` (TEXT) - тип события
- `timestamp` (TEXT) - время события
- `data` (TEXT) - JSON данные события

### sms_logs
- `id` (INTEGER) - автоинкремент
- `device_id` (TEXT) - ID устройства
- `timestamp` (TEXT) - время получения
- `sender` (TEXT) - отправитель
- `message` (TEXT) - текст сообщения

## 🧪 Тестирование

Используйте файл `test_api.py` для отправки тестовых данных:

```bash
python test_api.py
```

Или отправьте запрос вручную с помощью curl (Windows PowerShell):

```powershell
$body = @{
    type = "device_status"
    timestamp = "14.10.2025 12:00:00"
    device = @{
        name = "Тестовое устройство"
        id = "test_device_001"
        battery = 95
    }
    network = @{
        hasSignal = $true
        signalStrength = 3
        networkType = "4G (LTE)"
        country = "RU"
        canReceiveSms = $true
    }
    internet = @{
        connected = $true
        type = "WiFi"
    }
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/event" -Method POST -Body $body -ContentType "application/json"
```

Или с помощью curl (Linux/Mac):
```bash
curl -X POST http://localhost:8000/event \
  -H "Content-Type: application/json" \
  -d '{
    "type": "device_status",
    "timestamp": "14.10.2025 12:00:00",
    "device": {
      "name": "Тестовое устройство",
      "id": "test_device_001",
      "battery": 95
    },
    "network": {
      "hasSignal": true,
      "signalStrength": 3,
      "networkType": "4G (LTE)",
      "country": "RU",
      "canReceiveSms": true
    },
    "internet": {
      "connected": true,
      "type": "WiFi"
    }
  }'
```

## 📂 Структура проекта

```
DeviceManager/
├── main.py              # FastAPI сервер
├── database.py          # Работа с SQLite
├── models.py            # Pydantic модели
├── requirements.txt     # Зависимости
├── index.html          # Главная страница
├── device.html         # Страница устройства
├── test_api.py         # Скрипт для тестирования
├── devices.db          # База данных (создается автоматически)
└── README.md           # Документация
```

## 📝 Примечания

- База данных создается автоматически при первом запуске
- Статус "онлайн" определяется автоматически (последнее обновление < 35 минут)
- Все события сохраняются в таблицу `events` независимо от типа
- Веб-интерфейс обновляется автоматически каждые 10 секунд

## 🔐 Безопасность

⚠️ Это демонстрационный проект. Для production использования добавьте:
- Аутентификацию и авторизацию
- HTTPS
- Валидацию и санитизацию входных данных
- Rate limiting
- CORS настройки

## 📄 Лицензия

MIT License

## 👨‍💻 Автор

Создано с использованием FastAPI, SQLite и Tailwind CSS

