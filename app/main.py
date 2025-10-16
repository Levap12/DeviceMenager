"""
FastAPI сервер для приема данных от Android-устройств
Принимает события трех типов: device_status, sms, boot_completed
+ Webhook для Telegram бота
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from contextlib import asynccontextmanager
import uvicorn
from typing import Dict, Any
import os

from aiogram import Bot, Dispatcher, Router
from aiogram.types import Update
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from app.database import (
    init_database, 
    save_event, 
    update_device, 
    save_sms,
    get_all_devices,
    get_device_by_id,
    get_device_sms
)
from app.telegram_notifications import init_telegram_bot, send_sms_notification_async

# Загружаем конфигурацию
load_dotenv('config.env')

# Импортируем обработчики Telegram бота
from app import telegram_bot


# Инициализация базы данных при запуске
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    # Startup
    init_database()
    print("✅ База данных инициализирована")
    
    # Инициализация Telegram бота для уведомлений
    init_telegram_bot()
    
    # Настройка webhook для Telegram
    webhook_url = os.getenv('WEB_URL', 'http://localhost:8000')
    if webhook_url and webhook_url != 'http://localhost:8000':
        try:
            await telegram_bot.bot.set_webhook(
                url=f"{webhook_url}/telegram/webhook",
                drop_pending_updates=True
            )
            print(f"✅ Telegram webhook установлен: {webhook_url}/telegram/webhook")
        except Exception as e:
            print(f"⚠️ Ошибка установки webhook: {e}")
    else:
        print("⚠️ WEB_URL не настроен, webhook не установлен")
    
    yield
    
    # Shutdown
    try:
        await telegram_bot.bot.delete_webhook()
        print("✅ Telegram webhook удален")
    except:
        pass
    print("👋 Сервер остановлен")


# Инициализация FastAPI приложения
app = FastAPI(
    title="Device Manager API",
    description="API для управления Android устройствами",
    version="1.0.0",
    lifespan=lifespan
)


@app.post("/event")
async def receive_event(event: Dict[str, Any]):
    """
    Принимает события от Android-устройств
    
    Типы событий:
    - device_status: обновление статуса устройства
    - sms: новое SMS сообщение
    - boot_completed: уведомление о перезагрузке
    """
    try:
        print(f"\n📥 Получено событие: {event.get('type', 'unknown')}")
        
        # Получаем тип события
        event_type = event.get('type')
        timestamp = event.get('timestamp')
        
        if not event_type or not timestamp:
            print(f"❌ Отсутствуют обязательные поля. Event: {event}")
            raise HTTPException(
                status_code=400, 
                detail="Отсутствуют обязательные поля: type, timestamp"
            )
        
        # Для SMS выводим дополнительную информацию
        if event_type == "sms":
            print(f"   📨 SMS данные: from={event.get('from')}, message_length={len(event.get('message', ''))}")
        
        # Извлекаем данные устройства из вложенной структуры
        device_data = event.get('device', {})
        device_id = device_data.get('id')
        device_name = device_data.get('name')
        battery = device_data.get('battery', 0)
        
        # Если ID нет в device, пытаемся найти в корне
        if not device_id:
            device_id = event.get('device_id')
        
        # Для SMS событий может не быть ID в device, но имя должно быть
        # Используем имя устройства для поиска существующего ID
        if not device_id and event_type == "sms" and device_name:
            # Ищем устройство по имени
            from app.database import get_connection
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM devices WHERE name = ? LIMIT 1", (device_name,))
            row = cursor.fetchone()
            if row:
                device_id = row['id']
                print(f"   Найден device_id по имени: {device_id}")
            conn.close()
        
        if not device_id:
            print(f"❌ Отсутствует device_id. Device data: {device_data}, event_type: {event_type}")
            raise HTTPException(
                status_code=400, 
                detail=f"Отсутствует device.id для события {event_type}. Убедитесь, что устройство было зарегистрировано через device_status"
            )
        
        print(f"   Device ID: {device_id}, Type: {event_type}")
        
        # Сохраняем событие в таблицу events
        save_event(device_id, event_type, timestamp, event)
        
        # Обрабатываем событие в зависимости от типа
        if event_type == "device_status":
            # Извлекаем данные о сети
            network_data = event.get('network', {})
            internet_data = event.get('internet', {})
            
            # Преобразуем уровень сигнала (1-4) в проценты
            signal_strength_raw = network_data.get('signalStrength', 0)
            signal_strength = int((signal_strength_raw / 4) * 100) if signal_strength_raw else 0
            
            # Получаем тип сети
            network_type = network_data.get('networkType', 'Unknown')
            
            # Получаем тип интернета
            internet_type = internet_data.get('type', 'Unknown')
            
            # Проверяем, есть ли уже устройство в базе
            existing_device = get_device_by_id(device_id)
            
            # Обновляем информацию об устройстве
            update_data = {
                'battery': battery,
                'signal_strength': signal_strength,
                'network_type': network_type,
                'internet': internet_type,
                'timestamp': timestamp
            }
            
            # Имя добавляем ТОЛЬКО если устройства еще нет в базе
            # Для существующих устройств имя НЕ обновляется (можно менять только вручную через API)
            if not existing_device:
                # Новое устройство - используем имя из события
                update_data['name'] = device_name if device_name else f'Device {device_id}'
            # Для существующих устройств НЕ добавляем 'name' - имя сохраняется
            
            update_device(device_id, update_data)
            
        elif event_type == "sms":
            try:
                # Сохраняем SMS
                sender = event.get('from', 'Unknown')
                message = event.get('message', '')
                print(f"   📨 SMS от {sender}: {message[:50]}...")
                save_sms(device_id, timestamp, sender, message)
                
                # Отправляем уведомление в Telegram
                try:
                    await send_sms_notification_async(device_id, sender, message, timestamp)
                except Exception as e:
                    print(f"   ⚠️ Ошибка отправки в Telegram: {e}")
                    import traceback
                    traceback.print_exc()
                
                # Обновляем информацию об устройстве из SMS события
                has_signal = device_data.get('hasSignal', False)
                signal_strength_raw = device_data.get('signalStrength', 0)
                signal_strength = int((signal_strength_raw / 4) * 100) if signal_strength_raw else 0
                network_type = device_data.get('networkType', 'Unknown')
                internet_connected = device_data.get('internetConnected', False)
                
                # Обновляем данные устройства (без имени, чтобы не перезаписать пользовательское)
                update_device(device_id, {
                    'battery': battery,
                    'signal_strength': signal_strength,
                    'network_type': network_type,
                    'internet': 'Connected' if internet_connected else 'Disconnected',
                    'timestamp': timestamp
                })
            except Exception as sms_error:
                print(f"❌ Ошибка обработки SMS: {sms_error}")
                import traceback
                traceback.print_exc()
                raise HTTPException(status_code=500, detail=f"Ошибка обработки SMS: {str(sms_error)}")
            
        elif event_type == "boot_completed":
            # Извлекаем данные о сети
            network_data = event.get('network', {})
            internet_data = event.get('internet', {})
            
            signal_strength_raw = network_data.get('signalStrength', 0)
            signal_strength = int((signal_strength_raw / 4) * 100) if signal_strength_raw else 0
            network_type = network_data.get('networkType', 'Unknown')
            internet_type = internet_data.get('type', 'Unknown')
            
            # Проверяем, есть ли уже устройство в базе
            existing_device = get_device_by_id(device_id)
            
            # Обновляем информацию об устройстве после перезагрузки
            update_data = {
                'battery': battery,
                'signal_strength': signal_strength,
                'network_type': network_type,
                'internet': internet_type,
                'timestamp': timestamp
            }
            
            # Имя добавляем ТОЛЬКО если устройства еще нет в базе
            # Для существующих устройств имя НЕ обновляется (можно менять только вручную через API)
            if not existing_device:
                # Новое устройство - используем имя из события
                update_data['name'] = device_name if device_name else f'Device {device_id}'
            # Для существующих устройств НЕ добавляем 'name' - имя сохраняется
            
            update_device(device_id, update_data)
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": f"Событие {event_type} успешно обработано",
                "device_id": device_id,
                "type": event_type
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА при обработке события:")
        print(error_traceback)
        raise HTTPException(status_code=500, detail=f"Ошибка обработки события: {str(e)}")


@app.get("/devices")
async def list_devices():
    """
    Получить список всех устройств
    """
    try:
        devices = get_all_devices()
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "count": len(devices),
                "devices": devices
            }
        )
    except Exception as e:
        import traceback
        print(f"❌ Ошибка в /devices: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Ошибка получения списка устройств: {str(e)}")


@app.get("/device/{device_id}")
async def get_device(device_id: str):
    """
    Получить информацию о конкретном устройстве
    """
    try:
        device = get_device_by_id(device_id)
        
        if not device:
            raise HTTPException(
                status_code=404, 
                detail=f"Устройство с ID {device_id} не найдено"
            )
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "device": device
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения данных устройства: {str(e)}")


@app.get("/device/{device_id}/sms")
async def get_device_sms_logs(device_id: str):
    """
    Получить список всех SMS для конкретного устройства
    """
    try:
        # Проверяем существование устройства
        device = get_device_by_id(device_id)
        if not device:
            raise HTTPException(
                status_code=404, 
                detail=f"Устройство с ID {device_id} не найдено"
            )
        
        sms_list = get_device_sms(device_id)
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "device_id": device_id,
                "count": len(sms_list),
                "sms": sms_list
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения SMS: {str(e)}")


@app.put("/device/{device_id}/name")
async def update_device_name(device_id: str, request: Request):
    """
    Обновить имя устройства
    """
    try:
        # Проверяем существование устройства
        device = get_device_by_id(device_id)
        if not device:
            raise HTTPException(
                status_code=404, 
                detail=f"Устройство с ID {device_id} не найдено"
            )
        
        # Получаем новое имя из тела запроса
        body = await request.json()
        new_name = body.get('name', '').strip()
        
        if not new_name:
            raise HTTPException(
                status_code=400,
                detail="Имя устройства не может быть пустым"
            )
        
        if len(new_name) > 100:
            raise HTTPException(
                status_code=400,
                detail="Имя устройства слишком длинное (максимум 100 символов)"
            )
        
        # Обновляем имя в базе данных
        update_device(device_id, {'name': new_name})
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Имя устройства обновлено",
                "device_id": device_id,
                "name": new_name
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обновления имени: {str(e)}")


@app.get("/")
async def root():
    """
    Главная страница - возвращает HTML интерфейс
    """
    index_path = os.path.join("templates", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Device Manager API работает"}


@app.get("/device-page/{device_id}")
async def device_page(device_id: str):
    """
    Страница конкретного устройства
    """
    device_path = os.path.join("templates", "device.html")
    if os.path.exists(device_path):
        return FileResponse(device_path)
    return {"message": f"Страница устройства {device_id}"}


@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    """
    Webhook для Telegram бота
    Принимает обновления от Telegram и обрабатывает их
    """
    try:
        update_data = await request.json()
        update = Update(**update_data)
        
        # Обрабатываем обновление через диспетчер
        await telegram_bot.dp.feed_update(telegram_bot.bot, update)
        
        return JSONResponse({"ok": True})
    except Exception as e:
        print(f"❌ Ошибка обработки Telegram webhook: {e}")
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500)


@app.get("/telegram/webhook/info")
async def webhook_info():
    """
    Получить информацию о webhook
    """
    try:
        info = await telegram_bot.bot.get_webhook_info()
        return JSONResponse({
            "url": info.url,
            "has_custom_certificate": info.has_custom_certificate,
            "pending_update_count": info.pending_update_count,
            "last_error_date": info.last_error_date,
            "last_error_message": info.last_error_message,
            "max_connections": info.max_connections,
            "allowed_updates": info.allowed_updates
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")


# Запуск сервера
if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )

