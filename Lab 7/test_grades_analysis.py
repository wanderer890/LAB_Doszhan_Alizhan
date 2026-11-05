import unittest
from grades_analysis import (
    validate_score,
    build_report,
    recursive_max,
    calculate_median,
    calculate_average,
    admission_status
)

class FunctionalCoreTests(unittest.TestCase):

    def test_build_report_does_not_change_source(self):
        source = [80, 75, 90]
        snapshot = source.copy()
        report = build_report("Student", source)
        self.assertEqual(source, snapshot)
        self.assertEqual(report["status"], "допущен")
        self.assertIsInstance(report["scores"], tuple)

    def test_recursive_max_rejects_empty_sequence(self):
        with self.assertRaisesRegex(ValueError, "пуста"):
            recursive_max([])

    def test_validate_score_rejects_bool(self):
        with self.assertRaisesRegex(TypeError, "Балл должен быть числом"):
            validate_score(True)

    def test_validate_score_out_of_bounds(self):
        with self.assertRaisesRegex(ValueError, "Балл должен быть от 0 до 100"):
            validate_score(105)
        with self.assertRaisesRegex(ValueError, "Балл должен быть от 0 до 100"):
            validate_score(-5)

    def test_calculate_average(self):
        self.assertAlmostEqual(calculate_average([50, 100]), 75.0)
        self.assertIsNone(calculate_average([]))

    def test_calculate_median(self):
        self.assertEqual(calculate_median([10, 30, 20]), 20.0)
        self.assertEqual(calculate_median([10, 40, 20, 30]), 25.0)
        self.assertIsNone(calculate_median([]))

    def test_admission_status(self):
        self.assertEqual(admission_status([50, 50]), "допущен")
        self.assertEqual(admission_status([40, 40]), "не допущен")
        self.assertEqual(admission_status([]), "нет данных")

    def test_recursive_max_valid(self):
        self.assertEqual(recursive_max([10, 50, 20, 90, 5]), 90.0)
        self.assertEqual(recursive_max([100]), 100.0)

if __name__ == "__main__":
    unittest.main()