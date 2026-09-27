# Quality Metrics SQL Dashboard

SQL-first quality analytics: a SQLite data model for production lots,
defects and inspections, reusable KPI queries (DPMO, first-pass yield,
defect rates, Pareto, trends), a synthetic data generator, and a
Python/matplotlib dashboard that renders the charts.

## Layout

- `schema.sql` — tables: `production_lots`, `defects`, `inspections`
- `queries/` — `kpi.sql`, `pareto.sql`, `trends.sql`
- `python/seed_data.py` — generates 6 months of synthetic data into `quality.db`
- `python/dashboard.py` — renders Pareto, trend and DPMO-by-line charts to PNG
- `python/metrics.py` — pure metric functions (DPMO, FPY, Pareto table)

## Quick start

```bash
pip install -r requirements.txt
python python/seed_data.py
python python/dashboard.py        # writes charts/*.png
```

## Tests

```bash
python -m unittest discover -s tests -v
```

The SQL in `queries/` is written to also run in Power BI / Excel Power Query
with minimal changes — the same KPI logic powers both.
