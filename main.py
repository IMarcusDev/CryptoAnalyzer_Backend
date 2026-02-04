# Install dependencies
## pip install -r requirements.txt

# Run
## uvicorn main:app --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.transaction_routes import router as transaction_router

app = FastAPI(
  title="Transactions API",
  version="1.0.0"
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.get("/")
def health_check():
  return {"status": "ok"}

app.include_router(transaction_router)
