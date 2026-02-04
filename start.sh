#!/bin/bash

# Start the FastAPI application with uvicorn
# Render provides the PORT environment variable automatically
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
