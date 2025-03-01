#!/bin/bash

# Активируем виртуальное окружение
source /opt/venv/bin/activate

# Проверяем наличие файлов
echo "Checking files in /usr/share/nginx/html:"
ls -la /usr/share/nginx/html

# Проверяем конфигурацию nginx
nginx -t

# Запускаем nginx в фоне
nginx

# Проверяем, что nginx запустился
ps aux | grep nginx

# Запускаем бота
cd /app && python bot.py 