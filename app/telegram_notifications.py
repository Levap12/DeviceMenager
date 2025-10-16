"""
Модуль для отправки уведомлений в Telegram
Работает асинхронно, не блокируя основной поток FastAPI
"""
import asyncio
import os
import re
from typing import Optional, Tuple
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

from app.database import get_device_chats, get_device_by_id

# Загружаем переменные окружения
load_dotenv('config.env')

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Глобальный экземпляр бота
_bot: Optional[Bot] = None
_loop: Optional[asyncio.AbstractEventLoop] = None


def init_telegram_bot():
    """Инициализировать Telegram бота для отправки уведомлений"""
    global _bot, _loop
    
    if not BOT_TOKEN:
        print("⚠️ TELEGRAM_BOT_TOKEN не установлен, уведомления отключены")
        return
    
    try:
        _bot = Bot(
            token=BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        print("✅ Telegram бот для уведомлений инициализирован")
    except Exception as e:
        print(f"❌ Ошибка инициализации Telegram бота: {e}")


def extract_halyk_code(sender: str, message: str) -> Tuple[Optional[str], bool]:
    """
    Извлечь код из SMS от Halyk и определить тип (Google Pay или Apple Wallet)
    
    Returns:
        Tuple[code, is_apple]: (код или None, True если Apple Wallet)
    """
    # Проверяем, что SMS от Halyk (проверяем отправителя)
    if 'halyk' not in sender.lower():
        return None, False
    
    # Ищем 6-значный код в начале сообщения
    code_match = re.search(r'^(\d{6})', message.strip())
    if not code_match:
        return None, False
    
    code = code_match.group(1)
    
    # Определяем тип (Apple Wallet или Google Pay)
    is_apple = 'apple' in message.lower() or 'iphone' in message.lower()
    
    return code, is_apple


async def _send_sms_notification_async(device_id: str, sender: str, message: str, timestamp: str):
    """Асинхронная отправка уведомления о SMS"""
    if not _bot:
        return
    
    try:
        # Получаем список чатов для этого устройства
        chat_ids = get_device_chats(device_id)
        
        if not chat_ids:
            print(f"   ℹ️ Нет привязанных чатов для устройства {device_id}")
            return
        
        # Получаем информацию об устройстве
        device = get_device_by_id(device_id)
        device_name = device.get('name', 'Неизвестное устройство') if device else device_id
        
        # Проверяем, есть ли код от Halyk
        code, is_apple = extract_halyk_code(sender, message)
        
        # Форматируем сообщение с кодом в <pre> если это Halyk
        formatted_message = message
        if code:
            formatted_message = message.replace(code, f'<pre>{code}</pre>', 1)
        
        # Базовое уведомление
        notification = (
            f"📨 <b>Новое SMS</b>\n\n"
            f"<b>Устройство:</b> {device_name}\n"
            f"<b>От:</b> <code>{sender}</code>\n"
            f"<b>Время:</b> {timestamp}\n\n"
            f"<b>Сообщение:</b>\n{formatted_message}"
        )
        
        # Добавляем предупреждение для Apple Wallet
        if code and is_apple:
            notification += "\n\n⚠️ <b>ВНИМАНИЕ!</b> Это код для <b>iPhone</b> (Apple Wallet)!\n🚨 В вашей работе такие коды считаются опасными!"
        
        # Отправляем уведомления во все чаты
        for chat_id in chat_ids:
            try:
                # Отправляем основное сообщение
                await _bot.send_message(chat_id, notification)
                print(f"   ✅ SMS отправлено в Telegram чат {chat_id}")
                    
            except Exception as e:
                print(f"   ❌ Ошибка отправки в чат {chat_id}: {e}")
    
    except Exception as e:
        print(f"❌ Ошибка отправки SMS уведомлений: {e}")


def send_sms_notification(device_id: str, sender: str, message: str, timestamp: str):
    """
    Отправить уведомление о новом SMS (синхронная обертка)
    Вызывается из FastAPI
    """
    if not _bot:
        return
    
    try:
        # Создаем новый event loop в отдельном потоке или используем существующий
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(
            _send_sms_notification_async(device_id, sender, message, timestamp)
        )
        loop.close()
    except Exception as e:
        print(f"❌ Ошибка в send_sms_notification: {e}")


async def send_sms_notification_async(device_id: str, sender: str, message: str, timestamp: str):
    """
    Асинхронная версия для использования внутри async контекста
    """
    try:
        await _send_sms_notification_async(device_id, sender, message, timestamp)
    except Exception as e:
        print(f"❌ Ошибка в send_sms_notification_async: {e}")
        import traceback
        traceback.print_exc()

