@echo off
chcp 65001 > nul
title Device Manager - Запуск

echo.
echo ╔═══════════════════════════════════════════════╗
echo ║       📱 Device Manager - Запуск              ║
echo ╚═══════════════════════════════════════════════╝
echo.

:: Проверка виртуального окружения
if not exist "venv\" (
    echo ⚠️  Виртуальное окружение не найдено!
    echo 🔧 Создание виртуального окружения...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Ошибка создания виртуального окружения!
        pause
        exit /b 1
    )
    echo ✅ Виртуальное окружение создано
    echo.
)

:: Активация виртуального окружения
call venv\Scripts\activate.bat

:: Проверка зависимостей
echo 📦 Проверка зависимостей...
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo 📥 Установка зависимостей...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Ошибка установки зависимостей!
        pause
        exit /b 1
    )
    echo ✅ Зависимости установлены
    echo.
)

:: Проверка config.env
if not exist "config.env" (
    echo.
    echo ⚠️  Файл config.env не найден!
    echo 📝 Создайте config.env на основе config.env.example
    echo.
    if exist "config.env.example" (
        copy config.env.example config.env
        echo ✅ Создан config.env из примера
        echo ⚠️  ВАЖНО: Отредактируйте config.env и добавьте ваш Telegram Bot Token!
        echo.
        notepad config.env
    )
)

:: Запуск приложения
echo.
echo ╔═══════════════════════════════════════════════╗
echo ║       🚀 Запуск Device Manager...             ║
echo ╚═══════════════════════════════════════════════╝
echo.
echo 🌐 Веб-интерфейс: http://localhost:8000
echo 📡 API документация: http://localhost:8000/docs
echo 🤖 Telegram бот: активен (webhook)
echo.
echo 💡 Для остановки нажмите Ctrl+C
echo.

python app\main.py

pause

