import time
import hashlib
from datetime import datetime
from typing import List

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


from src.models.transaction import Transaction


GAS_PER_BYTE = 16       # worst-case calldata
L1_GAS_PRICE = 30       # gwei (fixed for reproducibility)
L2_GAS_PRICE = 0.015    # gwei


class TransactionController:
  def __init__(self):
    self.transactions: List[Transaction] = []

  def create_transaction(self, data: dict) -> Transaction:
    text: str = data["text"]

    sha256Time, sha256Size = self._executeSHA256(text)
    sha_a = self._estimate_arbitrum_fee(sha256Size)
    sha_o = self._estimate_op_stack_fee(sha256Size)

    keccakTime, keccakSize = self._executeKECCAK256(text)
    keccak_a = self._estimate_arbitrum_fee(keccakSize)
    keccak_o = self._estimate_op_stack_fee(keccakSize)

    aesTime, aesSize = self._executeAES256(text)
    aes_a = self._estimate_arbitrum_fee(aesSize)
    aes_o = self._estimate_op_stack_fee(aesSize)

    rsaTime, rsaSize = self._executeRSA(text)
    rsa_a = self._estimate_arbitrum_fee(rsaSize)
    rsa_o = self._estimate_op_stack_fee(rsaSize)


    transaction = Transaction(
      text=text,
      date=datetime.now(),
      inputSize=len(text.encode("utf-8")),

      # SHA-256
      sha256Time=sha256Time,
      sha256OutputSize=sha256Size,
      sha256ArbitrumPrice=sha_a,
      sha256OptimismPrice=sha_o,
      sha256BasePrice=sha_o,

      # KECCAK256
      keccak256Time=keccakTime,
      keccak256OutputSize=keccakSize,
      keccak256ArbitrumPrice=keccak_a,
      keccak256OptimismPrice=keccak_o,
      keccak256BasePrice=keccak_o,

      # AES-256
      aes256Time=aesTime,
      aes256OutputSize=aesSize,
      aes256ArbitrumPrice=aes_a,
      aes256OptimismPrice=aes_o,
      aes256BasePrice=aes_o,

      # RSA
      rsaTime=rsaTime,
      rsaOutputSize=rsaSize,
      rsaArbitrumPrice=rsa_a,
      rsaOptimismPrice=rsa_o,
      rsaBasePrice=rsa_o,
    )

    self.transactions.append(transaction)
    return transaction

  def list_transactions(self) -> List[Transaction]:
    return self.transactions

  # Algoritmos
  def _executeSHA256(self, text: str):
    data = text.encode("utf-8")

    start = time.perf_counter()
    digest = hashlib.sha256(data).digest()
    elapsed = time.perf_counter() - start

    return elapsed, len(digest)

  def _executeKECCAK256(self, text: str):
    data = text.encode("utf-8")

    start = time.perf_counter()
    digest = hashlib.sha3_256(data).digest()
    elapsed = time.perf_counter() - start

    return elapsed, len(digest)

  def _executeAES256(self, text: str):
    data = text.encode("utf-8")

    key = get_random_bytes(32)   # 256 bits
    iv = get_random_bytes(16)

    cipher = AES.new(key, AES.MODE_CBC, iv)

    # PKCS7 padding
    pad_len = 16 - len(data) % 16
    padded_data = data + bytes([pad_len]) * pad_len

    start = time.perf_counter()
    ciphertext = cipher.encrypt(padded_data)
    elapsed = time.perf_counter() - start

    return elapsed, len(ciphertext)

  def _executeRSA(self, text: str):
    """
    Cifra el texto usando RSA-2048 con chunking para textos largos.
    
    RSA-2048 con OAEP padding solo puede cifrar ~214 bytes por operación.
    Para textos más largos, dividimos en chunks y ciframos cada uno.
    
    Esta implementación refleja el uso real de RSA donde típicamente
    se cifran claves simétricas pequeñas en lugar de datos extensos.
    """
    data = text.encode("utf-8")

    # Generar clave RSA-2048
    key = RSA.generate(2048)
    cipher = PKCS1_OAEP.new(key.publickey())

    # RSA-2048 con OAEP puede cifrar hasta ~214 bytes
    # Usamos 190 como límite seguro para evitar edge cases
    MAX_CHUNK_SIZE = 190

    start = time.perf_counter()
    
    # Si el texto cabe en un chunk, cifrar directamente
    if len(data) <= MAX_CHUNK_SIZE:
      ciphertext = cipher.encrypt(data)
    else:
      # Para textos largos, dividir en chunks
      chunks = []
      for i in range(0, len(data), MAX_CHUNK_SIZE):
        chunk = data[i:i + MAX_CHUNK_SIZE]
        encrypted_chunk = cipher.encrypt(chunk)
        chunks.append(encrypted_chunk)
      
      # Concatenar todos los chunks cifrados
      ciphertext = b''.join(chunks)
    
    elapsed = time.perf_counter() - start

    return elapsed, len(ciphertext)

  # Layer2
  def _estimate_arbitrum_fee(self, data_size: int) -> float:
    calldata_gas = data_size * 16
    l1_fee = calldata_gas * 30 * 1e-9
    l2_fee = 30000 * 0.1 * 1e-9
    return l1_fee + l2_fee

  def _estimate_op_stack_fee(self, data_size: int) -> float:
    OP_L1_FEE_SCALAR = 0.684
    calldata_gas = data_size * 16
    l1_fee = calldata_gas * 30 * OP_L1_FEE_SCALAR * 1e-9
    l2_fee = 21000 * 0.015 * 1e-9
    return l1_fee + l2_fee