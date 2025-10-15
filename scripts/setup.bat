@echo off
chcp 65001 > nul
title Device Manager - Первоначальная настройка

echo.
echo ╔═══════════════════════════════════════════════╗
echo ║    📱 Device Manager - Первоначальная настройка ║
echo ╚═══════════════════════════════════════════════╝
echo.

:: Переход в корневую директорию
cd /d %~dp0\..

:: Создание виртуального окружения
if not exist "venv\" (
    echo 🔧 Создание виртуального окружения...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Ошибка! Убедитесь, что Python установлен.
        pause
        exit /b 1
    )
    echo ✅ Виртуальное окружение создано
) else (
    echo ✅ Виртуальное окружение уже существует
)

:: Активация окружения
call venv\Scripts\activate.bat

:: Установка зависимостей
echo.
echo 📦 Установка зависимостей...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Ошибка установки зависимостей!
    pause
    exit /b 1
)
echo ✅ Зависимости установлены

:: Создание необходимых директорий
echo.
echo 📁 Создание директорий...
if not exist "data\" mkdir data
if not exist "static\" mkdir static
echo ✅ Директории созданы

:: Создание config.env
echo.
if not exist "config.env" (
    echo 📝 Создание config.env...
    copy config.env.example config.env
    echo ✅ Файл config.env создан
    echo.
    echo ╔═══════════════════════════════════════════════╗
    echo ║       ⚠️  ВАЖНО!                              ║
    echo ║                                               ║
    echo ║  Отредактируйте config.env:                   ║
    echo ║  1. Добавьте Telegram Bot Token               ║
    echo ║  2. Укажите URL вашего сайта                  ║
    echo ╚═══════════════════════════════════════════════╝
    echo.
    notepad config.env
) else (
    echo ✅ Файл config.env уже существует
)

:: Проверка базы данных
echo.
echo 🗄️  Инициализация базы данных...
python -c "from app.database import init_database; init_database(); print('✅ База данных инициализирована')"

echo.
echo ╔═══════════════════════════════════════════════╗
echo ║       ✅ Настройка завершена!                 ║
echo ║                                               ║
echo ║  Для запуска используйте:                     ║
echo ║  - start.bat (Windows)                        ║
echo ║  - docker-compose up (Docker)                 ║
echo ╚═══════════════════════════════════════════════╝
echo.

pause

