#!/bin/bash
# Start nginx in background
nginx -g 'daemon off;' &

# Start Python bot
python bot.py 