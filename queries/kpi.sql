-- KPI queries: DPMO, first-pass yield, defect rate by line.

-- DPMO by production line
SELECT
  l.line,
  COUNT(d.defect_id) AS defects,
  SUM(l.units * l.opportunities_per_unit) AS opportunities,
  ROUND(COUNT(d.defect_id) * 1000000.0
        / SUM(l.units * l.opportunities_per_unit), 1) AS dpmo
FROM production_lots l
LEFT JOIN defects d ON d.lot_id = l.lot_id
GROUP BY l.line
ORDER BY dpmo DESC;

-- First-pass yield by production line
SELECT
  l.line,
  SUM(i.inspected_units) AS inspected,
  SUM(i.passed_units) AS passed,
  ROUND(SUM(i.passed_units) * 100.0 / SUM(i.inspected_units), 2) AS fpy_pct
FROM inspections i
JOIN production_lots l ON l.lot_id = i.lot_id
GROUP BY l.line
ORDER BY fpy_pct;

-- Defect rate (defects per 1k units) by line and month
SELECT
  l.line,
  substr(l.produced_at, 1, 7) AS month,
  SUM(l.units) AS units,
  COUNT(d.defect_id) AS defects,
  ROUND(COUNT(d.defect_id) * 1000.0 / SUM(l.units), 2) AS defects_per_1k
FROM production_lots l
LEFT JOIN defects d ON d.lot_id = l.lot_id
GROUP BY l.line, month
ORDER BY month, l.line;
