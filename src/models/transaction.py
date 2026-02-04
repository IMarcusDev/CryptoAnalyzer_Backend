from pydantic import BaseModel
from datetime import datetime

class Transaction(BaseModel):
  text: str
  date: datetime
  inputSize: int

  sha256Time: float
  sha256OutputSize: int
  sha256ArbitrumPrice: float
  sha256OptimismPrice: float
  sha256BasePrice: float

  keccak256Time: float
  keccak256OutputSize: int
  keccak256ArbitrumPrice: float
  keccak256OptimismPrice: float
  keccak256BasePrice: float

  aes256Time: float
  aes256OutputSize: int
  aes256ArbitrumPrice: float
  aes256OptimismPrice: float
  aes256BasePrice: float

  rsaTime: float
  rsaOutputSize: int
  rsaArbitrumPrice: float
  rsaOptimismPrice: float
  rsaBasePrice: float
