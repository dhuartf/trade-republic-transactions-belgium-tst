import sqlite3, json, logging
from decimal import Decimal
from datetime import datetime
from typing import List, Optional
from ..models.transaction import Transaction

logger = logging.getLogger(__name__)
DB_PATH = "transactions.db"

class DynamoDBService:
    def __init__(self, **kwargs):
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS pdfs (
                pdf_id TEXT PRIMARY KEY, filename TEXT,
                file_size INT, parsed_at TEXT, transaction_count INT
            )""")
            conn.execute("""CREATE TABLE IF NOT EXISTS transactions (
                pdf_id TEXT, idx INT, date TEXT, isin TEXT,
                product_name TEXT, quantity TEXT, amount_euros TEXT,
                transaction_type TEXT
            )""")

    def check_pdf_exists(self, pdf_sha256):
        with sqlite3.connect(DB_PATH) as conn:
            row = conn.execute("SELECT 1 FROM pdfs WHERE pdf_id=?", (pdf_sha256,)).fetchone()
            return row is not None

    def get_pdf_metadata(self, pdf_sha256):
        with sqlite3.connect(DB_PATH) as conn:
            row = conn.execute("SELECT * FROM pdfs WHERE pdf_id=?", (pdf_sha256,)).fetchone()
            if row:
                return {"parsedAt": row[3]}
            return None

    def get_transactions_for_pdf(self, pdf_sha256):
        with sqlite3.connect(DB_PATH) as conn:
            rows = conn.execute(
                "SELECT * FROM transactions WHERE pdf_id=? ORDER BY idx", (pdf_sha256,)
            ).fetchall()
        return [Transaction(
            date=r[2], isin=r[3], product_name=r[4],
            quantity=Decimal(r[5]), amount_euros=Decimal(r[6]),
            transaction_type=r[7]
        ) for r in rows]

    def store_pdf_with_transactions(self, pdf_sha256, pdf_filename, pdf_size, transactions, parsed_at):
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("INSERT OR REPLACE INTO pdfs VALUES (?,?,?,?,?)",
                (pdf_sha256, pdf_filename, pdf_size, parsed_at, len(transactions)))
            for i, t in enumerate(transactions):
                conn.execute("INSERT INTO transactions VALUES (?,?,?,?,?,?,?,?)",
                    (pdf_sha256, i, t.date, t.isin, t.product_name,
                     str(t.quantity), str(t.amount_euros), t.transaction_type))
        return pdf_sha256