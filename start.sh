#!/bin/bash

# Активируем виртуальное окружение
source /opt/venv/bin/activate

# Запускаем nginx в фоне
nginx

# Запускаем бота
cd /app && python bot.py 