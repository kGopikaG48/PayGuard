
# 🛡️ PayGuard
> A fault-tolerant, retry-safe payment gateway built with FastAPI, SQLite, and JavaScript to ensure strict idempotency and prevent duplicate customer charges.

---

## 🚀 The Problem
In distributed payment systems, network timeouts and client-side retries are inevitable. If a user clicks "Pay" and experiences lag, they often click it again. Without idempotency, naive servers process both clicks, leading to accidental **double-charging**.

## 💡 The Solution (Idempotency & Concurrency Control)
PayGuard solves this by implementing an enterprise-grade payment architecture:
1. **Idempotency-Key Headers:** Every checkout session passes a unique transaction fingerprint.

2. **Persistent Ledger:** An embedded SQLite database acts as the single source of truth for all transaction states.
3. **Thread Mutex Locking (`threading.Lock`):** Wraps ledger checks and writes to prevent race conditions during simultaneous request bursts.
4. **Cache-Hit Interception:** Identifies duplicate requests, blocks redundant debits, and safely returns the original receipt.

---

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI, Pydantic, SQLite, Threading (Concurrency)

- **Frontend:** HTML5, CSS3, JavaScript (Fetch API / AJAX)

- **Architecture:** RESTful API Design, Exact-Once Processing Semantics


---

## 📁 Project Structure
```text
payguard/
│
├── paymain.py       # FastAPI backend server with SQLite ledger & thread locks
├── index.html       # Modern fintech checkout frontend UI with retry simulation
└── ledger.db        # Embedded SQLite transaction database (auto-generated)

```
## 🚀 How to Run Locally

Follow these exact steps to run the complete PayGuard full-stack application on your machine:

1.💻 Clone the repository:
Bash
git clone https://github.com/yourusername/payguard.git
cd payguard

2.📦 Install required Python dependencies:
Bash
pip install fastapi uvicorn pydantic

3.⚡ Start the FastAPI backend server:
In your terminal, start the server using Uvicorn:
Bash
python -m uvicorn paymain:app --reload
(Keep this terminal open and running in the background).

4.🌐 Launch the frontend UI:
Open your File Explorer and navigate to your project folder.
Double-click index.html to open it directly in your web browser.
Click Pay Now to process a transaction, and use Simulate Double-Click to watch the server instantly catch and block duplicate requests live 🛡️
