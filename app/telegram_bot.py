"""
Telegram Bot для управления устройствами и получения уведомлений
Использует aiogram 3.x
"""
import asyncio
import os
import sys
from datetime import datetime, timedelta
from typing import List
import pytz

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
import aiohttp

from app.database import (
    init_database,
    get_all_devices,
    get_device_by_id,
    add_device_binding,
    remove_device_binding,
    get_chat_bindings,
    get_device_chats
)

# Загружаем переменные окружения
load_dotenv('config.env')

# Конфигурация
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEB_URL = os.getenv('WEB_URL', 'http://localhost:8000')
API_URL = os.getenv('API_URL', 'http://localhost:8000')

# ID администраторов
ADMIN_IDS = [452398375, 8151581578]

# Часовой пояс Казахстана
KAZAKHSTAN_TZ = pytz.timezone('Asia/Ashkhabad')  # UTC+5

# Инициализация бота
if not BOT_TOKEN:
    print("❌ Ошибка: TELEGRAM_BOT_TOKEN не установлен в config.env")
    print("Создайте файл config.env на основе config.env.example")
    sys.exit(1)

bot = Bot(
    token=BOT_TOKEN, 
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
router = Router()

# Регистрируем роутер сразу
dp.include_router(router)

# Глобальная переменная для хранения бота (для отправки уведомлений)
_bot_instance = None


def is_admin(user_id: int) -> bool:
    """Проверка, является ли пользователь администратором"""
    return user_id in ADMIN_IDS


def format_time_ago(timestamp_str: str) -> str:
    """Форматирование времени относительно текущего момента (Казахстан)"""
    if not timestamp_str:
        return "Неизвестно"
    
    try:
        # Парсим время
        try:
            # Формат: "DD.MM.YYYY HH:MM:SS"
            last_seen = datetime.strptime(timestamp_str, "%d.%m.%Y %H:%M:%S")
        except:
            # Формат ISO
            last_seen = datetime.fromisoformat(timestamp_str)
        
        # Добавляем часовой пояс Казахстана к времени устройства
        last_seen = KAZAKHSTAN_TZ.localize(last_seen)
        
        # Текущее время в Казахстане
        now = datetime.now(KAZAKHSTAN_TZ)
        
        # Разница
        diff = now - last_seen
        minutes = int(diff.total_seconds() / 60)
        hours = int(diff.total_seconds() / 3600)
        days = diff.days
        
        if minutes < 1:
            return "только что"
        elif minutes < 60:
            return f"{minutes} мин. назад"
        elif hours < 24:
            return f"{hours} ч. назад"
        elif days < 7:
            return f"{days} дн. назад"
        else:
            # Если больше недели, показываем конкретную дату
            return last_seen.strftime("%d.%m.%Y %H:%M")
    except Exception as e:
        return timestamp_str


def format_device_info(device: dict) -> str:
    """Форматирование информации об устройстве"""
    status = "🟢 Онлайн" if device.get('online') else "🔴 Оффлайн"
    battery = device.get('battery', 0)
    
    # Emoji для батареи
    if battery < 20:
        battery_emoji = "🔴"
    elif battery < 50:
        battery_emoji = "🟡"
    else:
        battery_emoji = "🟢"
    
    # Форматируем время последнего обновления
    last_seen = format_time_ago(device.get('last_seen'))
    
    return (
        f"<b>{device.get('name', 'Без имени')}</b>\n"
        f"├ ID: <code>{device.get('id')}</code>\n"
        f"├ Статус: {status}\n"
        f"├ Батарея: {battery_emoji} {battery}%\n"
        f"├ Сигнал: {device.get('signal_strength', 0)}%\n"
        f"├ Сеть: {device.get('network_type', 'Unknown')}\n"
        f"├ Интернет: {device.get('internet', 'Unknown')}\n"
        f"└ Обновлено: {last_seen}"
    )


def get_devices_keyboard() -> InlineKeyboardMarkup:
    """Создать клавиатуру с кнопкой обновления"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔄 Обновить", callback_data="refresh_devices"),
            InlineKeyboardButton(text="🌐 Открыть сайт", url=WEB_URL)
        ]
    ])
    return keyboard


async def get_devices_message() -> str:
    """Получить сообщение со списком устройств"""
    try:
        devices = get_all_devices()
        
        if not devices:
            return "📱 <b>Устройства</b>\n\n❌ Нет подключенных устройств"
        
        online_count = sum(1 for d in devices if d.get('online'))
        offline_count = len(devices) - online_count
        
        message = (
            f"📱 <b>Устройства ({len(devices)})</b>\n"
            f"🟢 Онлайн: {online_count} | 🔴 Оффлайн: {offline_count}\n\n"
        )
        
        for i, device in enumerate(devices, 1):
            message += f"{i}. {format_device_info(device)}\n\n"
        
        return message
    except Exception as e:
        return f"❌ Ошибка получения списка устройств: {str(e)}"


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    
    if not is_admin(user_id):
        await message.answer(
            "❌ У вас нет доступа к этому боту.\n"
            "Только администраторы могут использовать этого бота."
        )
        return
    
    # Получаем информацию об устройствах
    devices_text = await get_devices_message()
    
    await message.answer(
        f"👋 <b>Добро пожаловать в Device Manager!</b>\n\n"
        f"{devices_text}\n"
        f"<b>Доступные команды:</b>\n"
        f"/start - Показать это сообщение\n"
        f"/add &lt;device_id&gt; - Привязать устройство к этому чату\n"
        f"/remove &lt;device_id&gt; - Отвязать устройство от чата\n"
        f"/list - Показать привязанные устройства\n"
        f"/devices - Показать все устройства",
        reply_markup=get_devices_keyboard()
    )


@router.message(Command("devices"))
async def cmd_devices(message: Message):
    """Показать все устройства"""
    user_id = message.from_user.id
    
    if not is_admin(user_id):
        await message.answer("❌ У вас нет доступа к этой команде.")
        return
    
    devices_text = await get_devices_message()
    await message.answer(devices_text, reply_markup=get_devices_keyboard())


@router.callback_query(F.data == "refresh_devices")
async def refresh_devices(callback: CallbackQuery):
    """Обработчик кнопки обновления"""
    user_id = callback.from_user.id
    
    if not is_admin(user_id):
        await callback.answer("❌ У вас нет доступа", show_alert=True)
        return
    
    devices_text = await get_devices_message()
    
    try:
        await callback.message.edit_text(
            devices_text,
            reply_markup=get_devices_keyboard()
        )
        await callback.answer("✅ Обновлено")
    except Exception as e:
        error_message = str(e)
        # Если сообщение не изменилось, просто уведомляем пользователя
        if "message is not modified" in error_message:
            await callback.answer("ℹ️ Данные не изменились")
        else:
            await callback.answer(f"❌ Ошибка: {error_message}", show_alert=True)


@router.message(Command("add"))
async def cmd_add_device(message: Message):
    """Привязать устройство к чату"""
    user_id = message.from_user.id
    
    if not is_admin(user_id):
        await message.answer("❌ У вас нет доступа к этой команде.")
        return
    
    # Извлекаем device_id из команды
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer(
            "❌ Использование: <code>/add &lt;device_id&gt;</code>\n\n"
            "Пример: <code>/add abd7b5e86a733e8c</code>"
        )
        return
    
    device_id = parts[1].strip()
    chat_id = message.chat.id
    
    # Проверяем существование устройства
    device = get_device_by_id(device_id)
    if not device:
        await message.answer(f"❌ Устройство с ID <code>{device_id}</code> не найдено.")
        return
    
    # Добавляем привязку
    success = add_device_binding(device_id, chat_id)
    
    if success:
        await message.answer(
            f"✅ Устройство привязано к этому чату!\n\n"
            f"{format_device_info(device)}\n\n"
            f"Теперь вы будете получать все SMS с этого устройства."
        )
    else:
        await message.answer(
            f"⚠️ Устройство уже привязано к этому чату.\n\n"
            f"{format_device_info(device)}"
        )


@router.message(Command("remove"))
async def cmd_remove_device(message: Message):
    """Отвязать устройство от чата"""
    user_id = message.from_user.id
    
    if not is_admin(user_id):
        await message.answer("❌ У вас нет доступа к этой команде.")
        return
    
    # Извлекаем device_id из команды
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer(
            "❌ Использование: <code>/remove &lt;device_id&gt;</code>\n\n"
            "Пример: <code>/remove abd7b5e86a733e8c</code>"
        )
        return
    
    device_id = parts[1].strip()
    chat_id = message.chat.id
    
    # Удаляем привязку
    success = remove_device_binding(device_id, chat_id)
    
    if success:
        await message.answer(
            f"✅ Устройство <code>{device_id}</code> отвязано от этого чата.\n"
            f"Вы больше не будете получать SMS с этого устройства."
        )
    else:
        await message.answer(
            f"❌ Устройство <code>{device_id}</code> не привязано к этому чату."
        )


@router.message(Command("list"))
async def cmd_list_bindings(message: Message):
    """Показать привязанные к чату устройства"""
    user_id = message.from_user.id
    
    if not is_admin(user_id):
        await message.answer("❌ У вас нет доступа к этой команде.")
        return
    
    chat_id = message.chat.id
    device_ids = get_chat_bindings(chat_id)
    
    if not device_ids:
        await message.answer(
            "📋 <b>Привязанные устройства</b>\n\n"
            "❌ К этому чату не привязано ни одного устройства.\n\n"
            "Используйте /add &lt;device_id&gt; для привязки."
        )
        return
    
    message_text = f"📋 <b>Привязанные устройства ({len(device_ids)})</b>\n\n"
    
    for i, device_id in enumerate(device_ids, 1):
        device = get_device_by_id(device_id)
        if device:
            message_text += f"{i}. {format_device_info(device)}\n\n"
        else:
            message_text += f"{i}. <code>{device_id}</code> (устройство не найдено)\n\n"
    
    await message.answer(message_text)


async def send_sms_notification(device_id: str, sender: str, message: str, timestamp: str):
    """Отправить уведомление о новом SMS во все привязанные чаты"""
    try:
        # Получаем список чатов для этого устройства
        chat_ids = get_device_chats(device_id)
        
        if not chat_ids:
            print(f"   ℹ️ Нет привязанных чатов для устройства {device_id}")
            return
        
        # Получаем информацию об устройстве
        device = get_device_by_id(device_id)
        device_name = device.get('name', 'Неизвестное устройство') if device else device_id
        
        # Форматируем сообщение
        notification = (
            f"📨 <b>Новое SMS</b>\n\n"
            f"<b>Устройство:</b> {device_name}\n"
            f"<b>От:</b> <code>{sender}</code>\n"
            f"<b>Время:</b> {timestamp}\n\n"
            f"<b>Сообщение:</b>\n{message}"
        )
        
        # Отправляем уведомления во все чаты
        for chat_id in chat_ids:
            try:
                await bot.send_message(chat_id, notification)
                print(f"   ✅ SMS отправлено в чат {chat_id}")
            except Exception as e:
                print(f"   ❌ Ошибка отправки в чат {chat_id}: {e}")
    
    except Exception as e:
        print(f"❌ Ошибка отправки SMS уведомлений: {e}")


async def main():
    """Главная функция запуска бота (только для standalone режима)"""
    global _bot_instance
    _bot_instance = bot
    
    # Инициализация базы данных
    init_database()
    print("✅ База данных инициализирована")
    
    # Запускаем бота в режиме polling
    print("🤖 Telegram бот запущен (polling режим)!")
    print(f"📱 Администраторы: {', '.join(map(str, ADMIN_IDS))}")
    print(f"🌐 Веб-интерфейс: {WEB_URL}")
    print("⚠️ Для webhook режима используйте main.py")
    
    await dp.start_polling(bot)


def get_bot() -> Bot:
    """Получить экземпляр бота для внешнего использования"""
    return _bot_instance


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен")

