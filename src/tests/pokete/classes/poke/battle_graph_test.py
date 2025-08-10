import unittest
from datetime import datetime
import os
from unittest.mock import patch

# Mock the terminal size call that causes issues during import
with patch.object(os, 'get_terminal_size', return_value=os.terminal_size((80, 24))):
    from pokete.classes.poke import Stats

class StatsTest(unittest.TestCase):

    def test_add_battle_case1(self):
        stats = Stats("TestPokeGraph", datetime.now())

        stats.add_battle(win=True)

        self.assertEqual(stats.win_battles, 1)
        self.assertEqual(stats.lost_battles, 0)
        self.assertEqual(stats.total_battles, 1)

    def test_add_battle_case2(self):
        stats = Stats("TestPokeGraph", datetime.now())

        stats.add_battle(win=False)

        self.assertEqual(stats.win_battles, 0)
        self.assertEqual(stats.lost_battles, 1)
        self.assertEqual(stats.total_battles, 1)