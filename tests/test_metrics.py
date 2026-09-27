"""Unit tests for quality metric functions (stdlib unittest)."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "python"))

from metrics import dpmo_value, fpy_value, pareto_table


class TestMetrics(unittest.TestCase):
    def test_dpmo(self):
        self.assertAlmostEqual(dpmo_value(34, 10_000, 1), 3400.0)
        self.assertEqual(dpmo_value(0, 100, 12), 0.0)
        with self.assertRaises(ValueError):
            dpmo_value(1, 0, 1)

    def test_fpy(self):
        self.assertAlmostEqual(fpy_value(950, 1000), 95.0)
        with self.assertRaises(ValueError):
            fpy_value(1, 0)

    def test_pareto_table(self):
        rows = pareto_table({"A": 50, "B": 30, "C": 20})
        self.assertEqual(rows[0][0], "A")
        self.assertAlmostEqual(rows[0][2], 50.0)
        self.assertAlmostEqual(rows[-1][3], 100.0)
        with self.assertRaises(ValueError):
            pareto_table({})


if __name__ == "__main__":
    unittest.main()
