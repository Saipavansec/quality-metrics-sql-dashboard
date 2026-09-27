-- Quality metrics data model (SQLite)

CREATE TABLE IF NOT EXISTS production_lots (
  lot_id TEXT PRIMARY KEY,
  line TEXT NOT NULL,
  product TEXT NOT NULL,
  produced_at TEXT NOT NULL,          -- ISO date
  units INTEGER NOT NULL CHECK (units > 0),
  opportunities_per_unit INTEGER NOT NULL DEFAULT 12
);

CREATE TABLE IF NOT EXISTS defects (
  defect_id INTEGER PRIMARY KEY AUTOINCREMENT,
  lot_id TEXT NOT NULL REFERENCES production_lots(lot_id),
  defect_type TEXT NOT NULL,
  severity TEXT,
  found_at TEXT NOT NULL              -- ISO date
);

CREATE TABLE IF NOT EXISTS inspections (
  inspection_id INTEGER PRIMARY KEY AUTOINCREMENT,
  lot_id TEXT NOT NULL REFERENCES production_lots(lot_id),
  inspected_units INTEGER NOT NULL,
  passed_units INTEGER NOT NULL,
  inspected_at TEXT NOT NULL          -- ISO date
);
