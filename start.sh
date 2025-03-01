#!/bin/bash

# Активируем виртуальное окружение
source /opt/venv/bin/activate

# Проверяем наличие файлов
echo "Checking files in /usr/share/nginx/html:"
ls -la /usr/share/nginx/html
echo "Checking index.html:"
cat /usr/share/nginx/html/index.html

# Проверяем конфигурацию nginx
echo "Testing nginx configuration..."
nginx -t

# Запускаем nginx в фоне
echo "Starting nginx..."
nginx
sleep 2

# Проверяем, что nginx запустился
echo "Checking nginx process..."
ps aux | grep nginx
echo "Checking nginx logs..."
tail /var/log/nginx/error.log

# Запускаем бота
echo "Starting bot..."
cd /app && python bot.py 