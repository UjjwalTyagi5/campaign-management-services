#!/bin/sh

# This entrypoint is only for starting the FastAPI API server
# Usage: ./entrypoint.sh
# we can can add more commands here for other services if needed in the future.

exec uvicorn main:app --host 0.0.0.0 --port 8000


