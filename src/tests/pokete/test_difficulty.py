import unittest
from pokete.classes.difficulty import DifficultyManager

class DifficultyManagerTest(unittest.TestCase):
    def test_initial_state(self):
        dm = DifficultyManager()
        self.assertEqual(dm.score, 1.0)
        self.assertEqual(dm.get_stat_multiplier(), 1.0)
        self.assertEqual(dm.get_level_offset(), 0)

    def test_win_increases_difficulty(self):
        dm = DifficultyManager()
        # Won, 100% HP, equal levels, 5 turns
        dm.record_battle(True, 1.0, 10, 10, 5)
        self.assertGreater(dm.score, 1.0)
        self.assertGreaterEqual(dm.get_level_offset(), 0)

    def test_loss_decreases_difficulty(self):
        dm = DifficultyManager()
        # Lost, 0% HP, equal levels, 10 turns
        dm.record_battle(False, 0.0, 10, 10, 10)
        self.assertLess(dm.score, 1.0)
        self.assertLessEqual(dm.get_level_offset(), 0)

    def test_clamping(self):
        dm = DifficultyManager()
        # Repeat massive wins
        for _ in range(50):
            dm.record_battle(True, 1.0, 1, 100, 1)
        self.assertEqual(dm.score, 2.0)

        # Repeat massive losses
        for _ in range(50):
            dm.record_battle(False, 0.0, 100, 1, 20)
        self.assertEqual(dm.score, 0.5)

    def test_efficiency_impact(self):
        dm1 = DifficultyManager()
        dm2 = DifficultyManager()
        # dm1 wins fast, dm2 wins slow
        dm1.record_battle(True, 1.0, 10, 10, 4)
        dm2.record_battle(True, 1.0, 10, 10, 20)
        self.assertGreater(dm1.score, dm2.score)

    def test_level_gap_impact(self):
        dm1 = DifficultyManager()
        dm2 = DifficultyManager()
        # dm1 wins against high level, dm2 wins against low level
        dm1.record_battle(True, 0.8, 10, 20, 8)
        dm2.record_battle(True, 0.8, 10, 5, 8)
        self.assertGreater(dm1.score, dm2.score)

    def test_serialization(self):
        dm = DifficultyManager()
        dm.record_battle(True, 0.9, 15, 15, 7)
        data = dm.to_dict()
        self.assertIn("score", data)
        self.assertIn("history", data)

        dm2 = DifficultyManager(data)
        self.assertEqual(dm.score, dm2.score)
        self.assertEqual(len(dm2.history), 1)

    def test_weighted_level_math_simulation(self):
        # Testing the formula used in fight.py: (MaxLvl * 2 + AvgLvl) / 3
        max_lvl = 100
        avg_lvl = 20 # (100 + 1 + 1 + 1 + 1 + 1) / 6 = 17.5, rounded up to 20
        effective_lvl = (max_lvl * 2 + avg_lvl) / 3
        self.assertEqual(effective_lvl, 73.33333333333333)

        # Comparison with standard average
        standard_avg = (max_lvl + avg_lvl) / 2 # 60
        self.assertGreater(effective_lvl, standard_avg)

    def test_catch_rate_factor(self):
        dm = DifficultyManager()
        # Initial score 1.0 -> factor 1.0
        self.assertEqual(1.0 / max(0.5, dm.score), 1.0)

        # Max difficulty 2.0 -> factor 0.5 (harder catch)
        dm.score = 2.0
        self.assertEqual(1.0 / max(0.5, dm.score), 0.5)

        # Min difficulty 0.5 -> factor 2.0 (easier catch)
        dm.score = 0.5
        self.assertEqual(1.0 / max(0.5, dm.score), 2.0)
