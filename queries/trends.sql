-- Monthly quality trends: units, defects, DPMO.

SELECT
  substr(l.produced_at, 1, 7) AS month,
  SUM(l.units) AS units,
  COUNT(d.defect_id) AS defects,
  ROUND(COUNT(d.defect_id) * 1000000.0
        / SUM(l.units * l.opportunities_per_unit), 1) AS dpmo
FROM production_lots l
LEFT JOIN defects d ON d.lot_id = l.lot_id
GROUP BY month
ORDER BY month;
