"""Generate 6 months of synthetic quality data into quality.db."""

import random
import sqlite3
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SCHEMA = (BASE / "schema.sql").read_text()
DB = BASE / "quality.db"

LINES = ["Line-A", "Line-B", "Line-C"]
PRODUCTS = ["Housing", "Shaft", "Pump"]
DEFECT_TYPES = [
    ("Surface finish", 0.30), ("Dimensional", 0.25), ("Seal leakage", 0.15),
    ("Labeling", 0.12), ("Torque", 0.10), ("Other", 0.08),
]
OPPORTUNITIES = 12


def main():
    rng = random.Random(7)
    if DB.exists():
        DB.unlink()
    conn = sqlite3.connect(DB)
    conn.executescript(SCHEMA)
    lot = 0
    for m in range(6):
        month = f"2026-{m + 1:02d}"
        for line in LINES:
            for _ in range(8):  # 8 lots per line per month
                lot += 1
                lot_id = f"LOT-{lot:04d}"
                units = rng.randint(400, 1200)
                product = rng.choice(PRODUCTS)
                conn.execute(
                    "INSERT INTO production_lots VALUES (?, ?, ?, ?, ?, ?)",
                    (lot_id, line, product, f"{month}-15", units,
                     OPPORTUNITIES))
                # defects: worse on Line-C to make the Pareto interesting
                rate = {"Line-A": 0.004, "Line-B": 0.007,
                        "Line-C": 0.012}[line]
                n_defects = rng.randint(0, int(units * rate * 3))
                for _ in range(n_defects):
                    r, acc = rng.random(), 0.0
                    dtype = DEFECT_TYPES[-1][0]
                    for name, w in DEFECT_TYPES:
                        acc += w
                        if r <= acc:
                            dtype = name
                            break
                    conn.execute(
                        "INSERT INTO defects (lot_id, defect_type, severity, found_at)"
                        " VALUES (?, ?, ?, ?)",
                        (lot_id, dtype, rng.choice(["minor", "major"]),
                         f"{month}-{rng.randint(1, 28):02d}"))
                inspected = units
                passed = inspected - rng.randint(0, int(units * rate * 2))
                conn.execute(
                    "INSERT INTO inspections (lot_id, inspected_units, passed_units, inspected_at)"
                    " VALUES (?, ?, ?, ?)",
                    (lot_id, inspected, passed, f"{month}-28"))
    conn.commit()
    n_lots = conn.execute("SELECT COUNT(*) FROM production_lots").fetchone()[0]
    n_def = conn.execute("SELECT COUNT(*) FROM defects").fetchone()[0]
    conn.close()
    print(f"wrote {n_lots} lots and {n_def} defects to {DB}")


if __name__ == "__main__":
    main()
