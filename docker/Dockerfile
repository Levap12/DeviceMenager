# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY ../requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение
COPY ../app ./app
COPY ../templates ./templates
COPY ../config.env.example ./config.env.example

# Создаем директорию для базы данных
RUN mkdir -p /app/data

# Переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Открываем порт 8000
EXPOSE 8000

# Запускаем приложение
CMD ["python", "-m", "app.main"]

