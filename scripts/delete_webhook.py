"""
Скрипт для удаления webhook Telegram бота
Запустите этот скрипт если получаете ошибку "webhook is active"
"""
import asyncio
import os
import sys
from aiogram import Bot
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv('config.env')

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not BOT_TOKEN:
    print("❌ Ошибка: TELEGRAM_BOT_TOKEN не установлен в config.env")
    sys.exit(1)


async def delete_webhook():
    """Удалить webhook"""
    bot = Bot(token=BOT_TOKEN)
    
    try:
        # Удаляем webhook
        await bot.delete_webhook(drop_pending_updates=True)
        print("✅ Webhook успешно удален!")
        print("✅ Pending updates очищены!")
        print("\nТеперь можете запустить: python telegram_bot.py")
    except Exception as e:
        print(f"❌ Ошибка при удалении webhook: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    print("🔧 Удаление webhook Telegram бота...\n")
    asyncio.run(delete_webhook())

