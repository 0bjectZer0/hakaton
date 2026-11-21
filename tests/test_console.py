"""Проверки нормальных точек входа и перехода от часов к повторяющимся парам."""
from pathlib import Path
import os
import subprocess
import sys
import unittest

from planner.sgu import recurrence_counts


ROOT = Path(__file__).resolve().parents[1]


class ConsoleTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, "-B", str(ROOT / "raspisanie_sgu.py"),
                               "--data", str(ROOT / "examples"), "--no-menu", *args],
                              text=True, encoding="utf-8", capture_output=True,
                              env={**os.environ, "PYTHONIOENCODING": "utf-8"})

    def test_views_keep_week_and_resource(self):
        for view, resource in (("group", "Г-101"), ("teacher", "Ильина"), ("room", "А-101")):
            with self.subTest(view=view):
                result = self.run_cli("--view", view, "--resource", resource, "--week", "З", "--variant", "1")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("Получено вариантов: 4 из 4", result.stdout)
                self.assertIn("Неделя знаменатель", result.stdout)
                self.assertNotIn("Неделя числитель", result.stdout)
                lines = [line for line in result.stdout.splitlines() if line[0:2].isdigit() and "–" in line[:11]]
                self.assertTrue(lines)
                self.assertTrue(all(resource in line.split(" | ")[1] for line in lines))

    def test_unknown_resource(self):
        result = self.run_cli("--view", "teacher", "--resource", "несуществующий")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("отсутствует", result.stderr)

    def test_recurrences_respect_available_days(self):
        options = [(0, "08:00", "09:30", n) for n in (6, 4, 4, 4)]
        self.assertEqual(recurrence_counts(24, options), (4, 4, 4))
        self.assertFalse(recurrence_counts(26, options))
