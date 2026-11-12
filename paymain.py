from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import uuid
import threading

app = FastAPI(title="PayGuard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

db_lock = threading.Lock()
DB_NAME = "ledger.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            idempotency_key TEXT PRIMARY KEY,
            transaction_id TEXT,
            amount REAL,
            recipient TEXT,
            payer TEXT,
            ledger_status TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

class PaymentRequest(BaseModel):
    amount: float
    recipient: str
    payer: str

@app.get("/")
def health_check():
    return {"status": "PayGuard API is running with SQLite persistence!"}

# CHANGED FROM 'def' TO 'async def' TO FIX THE THREAD CRASH
@app.post("/pay")
async def process_payment(payment: PaymentRequest, idempotency_key: str = Header(None)):
    if not idempotency_key:
        raise HTTPException(status_code=400, detail="Idempotency-Key header is missing")

    with db_lock:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT transaction_id, amount, recipient, payer, ledger_status FROM transactions WHERE idempotency_key = ?",
            (idempotency_key,)
        )
        existing_tx = cursor.fetchone()

        if existing_tx:
            conn.close()
            return {
                "status": "cached",
                "message": "Duplicate request blocked. Returning original receipt.",
                "data": {
                    "transaction_id": existing_tx[0],
                    "amount": existing_tx[1],
                    "recipient": existing_tx[2],
                    "payer": existing_tx[3],
                    "ledger_status": existing_tx[4]
                }
            }

        new_tx_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO transactions (idempotency_key, transaction_id, amount, recipient, payer, ledger_status) VALUES (?, ?, ?, ?, ?, ?)",
            (idempotency_key, new_tx_id, payment.amount, payment.recipient, payment.payer, "DEBITED")
        )
        conn.commit()
        conn.close()

        return {
            "status": "success",
            "message": "Payment processed successfully!",
            "data": {
                "transaction_id": new_tx_id,
                "amount": payment.amount,
                "recipient": payment.recipient,
                "payer": payment.payer,
                "ledger_status": "DEBITED"
            }
        }