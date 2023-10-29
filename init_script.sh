#!/bin/sh

if [ -d "/app/ssl" ]; then
    chown -R nanocalc:nanocalc /app/ssl/
fi

su nanocalc -c "python /app/flaskapp.py"
