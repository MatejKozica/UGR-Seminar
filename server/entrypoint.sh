#!/bin/bash

if [ "$1" = "api_dev" ]; then
  exec uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
fi

if [ "$1" = "api" ]; then
  exec gunicorn src.app:app --config=config/gunicorn_config.py --bind=:8000 --preload
fi

exec "$@"
