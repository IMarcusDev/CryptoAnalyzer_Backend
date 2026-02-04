# Install dependencies
## pip install -r requirements.txt

# Run
## uvicorn main:app --reload

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.transaction_routes import router as transaction_router

# Get environment variables
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
print(f"🔍 FRONTEND_URL configurado: {FRONTEND_URL}")

ALLOWED_ORIGINS = [origin.strip() for origin in FRONTEND_URL.split(",")]
print(f"🔍 ALLOWED_ORIGINS: {ALLOWED_ORIGINS}") 


app = FastAPI(
  title="Transactions API",
  version="1.0.0"
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=ALLOWED_ORIGINS,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.get("/")
def health_check():
  return {"status": "ok"}

app.include_router(transaction_router)
