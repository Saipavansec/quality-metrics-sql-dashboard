-- Pareto of defect types with cumulative share.

WITH counts AS (
  SELECT defect_type, COUNT(*) AS n
  FROM defects
  GROUP BY defect_type
),
total AS (
  SELECT SUM(n) * 1.0 AS t FROM counts
)
SELECT
  c.defect_type,
  c.n AS defects,
  ROUND(c.n * 100.0 / t.t, 1) AS pct,
  ROUND(SUM(c.n) OVER (ORDER BY c.n DESC, c.defect_type
                       ROWS UNBOUNDED PRECEDING) * 100.0 / t.t, 1) AS cum_pct
FROM counts c, total t
ORDER BY c.n DESC;
