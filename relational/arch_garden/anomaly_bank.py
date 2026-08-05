"""
anomaly_bank.py — persistent memory for the infant's growing edge.

All prediction errors, high-entropy outputs, and grounding failures
are stored here for later review, pattern detection, and manifold
revision. SQLite for portability (works on phones via Termux; no
server required).

Two tables: `anomalies` (per-generation records) and `audits`
(per-review-cycle summaries). Read-only helpers for pattern
detection. Nothing here talks to a model — this is just the memory.
"""

import datetime
import sqlite3
from typing import Dict, List, Optional, Tuple


class AnomalyBank:
    def __init__(self, db_path: str = "anomaly_bank.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS anomalies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                prompt TEXT,
                output TEXT,
                entropy REAL,
                grounding_passed INTEGER,
                mode TEXT,
                processed INTEGER DEFAULT 0,
                protector_note TEXT
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS audits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                audit_type TEXT,
                summary TEXT,
                anomalies_reviewed INTEGER,
                action_taken TEXT
            )
        """)
        self.conn.commit()

    # ------------------------------------------------ writes

    def store(self, prompt: str, output: str, entropy: float,
              grounding_ok: bool, mode: str) -> int:
        cursor = self.conn.execute(
            "INSERT INTO anomalies "
            "(timestamp, prompt, output, entropy, grounding_passed, mode) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (datetime.datetime.now().isoformat(), prompt, output,
             entropy, int(grounding_ok), mode))
        self.conn.commit()
        return cursor.lastrowid

    def mark_processed(self, anomaly_id: int,
                       note: Optional[str] = None):
        if note is not None:
            self.conn.execute(
                "UPDATE anomalies SET processed=1, protector_note=? "
                "WHERE id=?", (note, anomaly_id))
        else:
            self.conn.execute(
                "UPDATE anomalies SET processed=1 WHERE id=?",
                (anomaly_id,))
        self.conn.commit()

    def log_audit(self, audit_type: str, summary: str,
                  anomalies_reviewed: int, action_taken: str):
        self.conn.execute(
            "INSERT INTO audits "
            "(timestamp, audit_type, summary, anomalies_reviewed, action_taken) "
            "VALUES (?, ?, ?, ?, ?)",
            (datetime.datetime.now().isoformat(), audit_type, summary,
             anomalies_reviewed, action_taken))
        self.conn.commit()

    # ------------------------------------------------ reads

    def count_unprocessed(self) -> int:
        cursor = self.conn.execute(
            "SELECT COUNT(*) FROM anomalies WHERE processed=0")
        return cursor.fetchone()[0]

    def get_unprocessed(self, limit: int = 50) -> List[sqlite3.Row]:
        cursor = self.conn.execute(
            "SELECT * FROM anomalies WHERE processed=0 "
            "ORDER BY id DESC LIMIT ?", (limit,))
        return cursor.fetchall()

    def recent_patterns(self) -> Dict[str, Dict]:
        """Grouping by mode: count, avg entropy, grounding fail rate."""
        cursor = self.conn.execute(
            "SELECT mode, "
            "  COUNT(*) as total, "
            "  AVG(entropy) as avg_entropy, "
            "  SUM(CASE WHEN grounding_passed=0 THEN 1 ELSE 0 END) as fails "
            "FROM anomalies WHERE processed=0 GROUP BY mode")
        out = {}
        for row in cursor.fetchall():
            mode, total, avg_ent, fails = row["mode"], row["total"], row["avg_entropy"], row["fails"]
            out[mode] = {
                "count": total,
                "avg_entropy": float(avg_ent) if avg_ent is not None else 0.0,
                "grounding_fail_rate": fails / total if total > 0 else 0.0,
            }
        return out

    def close(self):
        self.conn.close()


# --------------------------------------------------- smoke test

def _smoke_test():
    import os
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        db = os.path.join(td, "test.db")
        bank = AnomalyBank(db)

        ids = []
        ids.append(bank.store("what is fire?", "fire is heat + light",
                              entropy=0.35, grounding_ok=True, mode="explore"))
        ids.append(bank.store("do rocks fall up?", "sometimes",
                              entropy=0.85, grounding_ok=False, mode="observe"))
        ids.append(bank.store("hello", "hi",
                              entropy=0.10, grounding_ok=True, mode="explore"))

        assert bank.count_unprocessed() == 3
        bank.mark_processed(ids[0], note="benign")
        assert bank.count_unprocessed() == 2

        patterns = bank.recent_patterns()
        assert "explore" in patterns
        assert "observe" in patterns
        assert patterns["observe"]["grounding_fail_rate"] == 1.0

        bank.log_audit("three_way", "checked recent anomalies",
                       anomalies_reviewed=2, action_taken="marked")
        bank.close()
        print("anomaly_bank.py smoke test: OK")
        print(f"  stored 3, marked 1, 2 remain unprocessed")
        print(f"  patterns keyed by mode: {list(patterns)}")


if __name__ == "__main__":
    _smoke_test()
