#!/bin/sh
set -e

# If tests pass, start the FastAPI app
exec uvicorn app.main:app --host 0.0.0.0 --port 8000