#!/bin/sh
set -e
# This entrypoint is only for starting the FastAPI API server
# Usage: ./entrypoint.sh
# we can can add more commands here for other services if needed in the future.


case "$1" in
  "start-api-server")
    exec uvicorn main:app --host 0.0.0.0 --port 8080 --workers 1
    ;;
  *)
    echo "Unknown command: $1"
    echo "Usage : start-api-server"
    exit 1
    ;;
esac



