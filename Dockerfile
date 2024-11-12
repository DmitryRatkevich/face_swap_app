# Используем официальный образ Python как базовый
FROM python:3.9-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    curl \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-dev \
    libgl1-mesa-glx

# Устанавливаем pip и обновляем его
RUN pip install --upgrade pip

# Устанавливаем зависимости проекта
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем исходный код проекта в контейнер
COPY . /app

# Устанавливаем рабочую директорию
WORKDIR /app

# Указываем команду для запуска сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
