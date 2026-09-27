"""Render quality dashboard charts from quality.db into charts/*.png."""

import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from metrics import pareto_table

BASE = Path(__file__).resolve().parent.parent
DB = BASE / "quality.db"
CHARTS = BASE / "charts"
CHARTS.mkdir(exist_ok=True)


def query(sql):
    conn = sqlite3.connect(DB)
    try:
        return pd.read_sql_query(sql, conn)
    finally:
        conn.close()


def pareto_chart():
    df = query("SELECT defect_type, COUNT(*) AS n FROM defects "
               "GROUP BY defect_type")
    rows = pareto_table(dict(zip(df["defect_type"], df["n"])))
    pdf = pd.DataFrame(rows, columns=["type", "n", "pct", "cum_pct"])
    fig, ax1 = plt.subplots(figsize=(9, 5))
    ax1.bar(pdf["type"], pdf["n"])
    ax1.set_ylabel("Defects")
    ax1.tick_params(axis="x", rotation=30)
    ax2 = ax1.twinx()
    ax2.plot(pdf["type"], pdf["cum_pct"], marker="o", color="red")
    ax2.axhline(80, linestyle="--", color="gray")
    ax2.set_ylabel("Cumulative %")
    plt.title("Pareto of Defect Types")
    fig.tight_layout()
    fig.savefig(CHARTS / "pareto.png")
    plt.close(fig)


def trend_chart():
    df = query((BASE / "queries" / "trends.sql").read_text())
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(df["month"], df["dpmo"], marker="o")
    ax.set_ylabel("DPMO")
    ax.set_xlabel("Month")
    plt.title("DPMO Trend")
    fig.tight_layout()
    fig.savefig(CHARTS / "dpmo_trend.png")
    plt.close(fig)


def dpmo_by_line():
    df = query((BASE / "queries" / "kpi.sql").read_text().split(";")[0])
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(df["line"], df["dpmo"])
    ax.set_ylabel("DPMO")
    plt.title("DPMO by Production Line")
    fig.tight_layout()
    fig.savefig(CHARTS / "dpmo_by_line.png")
    plt.close(fig)


def main():
    if not DB.exists():
        raise SystemExit("quality.db not found — run python/seed_data.py first")
    pareto_chart()
    trend_chart()
    dpmo_by_line()
    print(f"charts written to {CHARTS}")


if __name__ == "__main__":
    main()
