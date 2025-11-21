FROM python:3.11-slim

# Создание рабочей директории
WORKDIR /app

# Копирование requirements и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Копирование проекта
COPY . .

# Создание статических файлов и настройка прав
RUN mkdir -p /app/static /app/media
RUN chmod +x /app/entrypoint.sh

# Создание пользователя для безопасности
RUN useradd -m -r medical_user && \
    chown -R medical_user:medical_user /app
USER medical_user

# Открытие порта
EXPOSE 8000

# Команда запуска
CMD ["gunicorn", "project_config.wsgi:application", "--bind", "127.0.0.1:8000", "--workers", "3"]