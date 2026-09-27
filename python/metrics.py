"""Pure quality-metric functions (no I/O) used by the dashboard."""

from __future__ import annotations


def dpmo_value(defects, units, opportunities_per_unit):
    if units <= 0 or opportunities_per_unit <= 0:
        raise ValueError("units and opportunities must be positive")
    return defects / (units * opportunities_per_unit) * 1_000_000


def fpy_value(passed_units, inspected_units):
    if inspected_units <= 0:
        raise ValueError("inspected_units must be positive")
    return passed_units / inspected_units * 100.0


def pareto_table(defect_counts):
    """Build a Pareto table from a {defect_type: count} mapping.

    Returns rows of (defect_type, count, pct, cum_pct) sorted desc.
    """
    total = sum(defect_counts.values())
    if total <= 0:
        raise ValueError("no defects to tabulate")
    rows = sorted(defect_counts.items(), key=lambda kv: kv[1], reverse=True)
    cum = 0
    out = []
    for dtype, n in rows:
        cum += n
        out.append((dtype, n, round(n / total * 100, 1),
                    round(cum / total * 100, 1)))
    return out
