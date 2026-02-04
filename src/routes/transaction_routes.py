from fastapi import APIRouter
from src.controllers.transaction_controller import TransactionController

router = APIRouter(
  prefix="/transactions",
  tags=["transactions"]
)

controller = TransactionController()

@router.get("/")
def get_transactions():
  return controller.list_transactions()

@router.post("/")
def create_transaction(payload: dict):
  transaction = controller.create_transaction(payload)
  return transaction
