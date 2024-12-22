# Используем официальное slim-изображение Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем необходимые пакеты
RUN apt-get update && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install numpy
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update
RUN apt-get install -y ffmpeg
RUN apt-get install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev -y
RUN pip install gtts
RUN pip install pyTelegramBotAPI
RUN pip install nbmerge
RUN pip install music21
RUN pip install sound-to-midi
RUN pip install uuid
RUN pip install librosa
RUN pip install midiutil

# Копируем весь код вашего проекта в контейнер
COPY . .

# Указываем команду по умолчанию для запуска приложения
CMD ["python", "main.py"]


