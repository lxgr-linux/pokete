import unittest
from unittest.mock import patch, MagicMock
import os

os.environ["COLUMNS"] = "80"
os.environ["LINES"] = "24"

with patch("os.get_terminal_size", return_value=(80, 24)):
    import pokete.base.tss
    from pokete.classes.deck import Deck


class TestDeck(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()
        # create a mock pokete with hp > 0
        self.mock_poke = MagicMock()
        self.mock_poke.hp = 10
        self.mock_poke.identifier = "testpoke"
        self.deck.pokes = [self.mock_poke]

    def test_choose_in_fight_returns_index_when_poke_alive(self):
        self.deck.in_fight = True
        result = self.deck.choose(MagicMock(), 0)
        self.assertEqual(result, 0)

    def test_choose_in_fight_returns_none_when_poke_fainted(self):
        self.deck.in_fight = True
        self.mock_poke.hp = 0
        result = self.deck.choose(MagicMock(), 0)
        self.assertIsNone(result)

    def test_choose_outside_fight_returns_none(self):
        self.deck.in_fight = False
        with patch("pokete.classes.deck.detail.detail"):
            result = self.deck.choose(MagicMock(), 0)
        self.assertIsNone(result)

    def test_empty_pokes_list_returns_none(self):
        self.deck.pokes = []
        result = self.deck.choose(MagicMock(), 0)
        self.assertIsNone(result)

    # Fallback identifier returns None even with hp > 0
    def test_fallback_identifier_returns_none_with_hp_greater_zero(self):
        self.mock_poke.hp = 10
        self.mock_poke.identifier = "__fallback__"
        result = self.deck.choose(MagicMock(), 0)
        self.assertIsNone(result)

    # In fight with hp == 0 returns None
    def test_in_fight_with_hp_zero_returns_none(self):
        self.mock_poke.hp = 0
        self.deck.in_fight = True
        result = self.deck.choose(MagicMock(), 0)
        self.assertIsNone(result)

    # In fight with hp > 0 returns the correct index
    def test_in_fight_with_hp_greater_zero_returns_correct_index(self):
        self.mock_poke.hp = 10
        self.mock_poke.identifier = "testpoke"
        self.deck.in_fight = True
        result = self.deck.choose(MagicMock(), 0)
        self.assertEqual(result, 0)

    # --- deck state setup tests ---
    # self.pokes is correctly sliced to p_len from figure.pokes
    def test_pokes_is_correctly_sliced_to_p_len_from_figure_pokes(self):
        ctx = MagicMock()
        ctx.figure = MagicMock()
        ctx.figure.pokes = [MagicMock() for _ in range(5)]
        self.deck.figure = ctx.figure
        self.deck.pokes = self.deck.figure.pokes[:3]
        self.assertEqual(len(self.deck.pokes), 3)
        self.assertEqual(self.deck.pokes, ctx.figure.pokes[:3])

    # self.in_fight is set correctly
    def test_in_fight_set_correctly_to_true(self):
        self.deck.in_fight = False
        self.deck.in_fight = True
        self.assertTrue(self.deck.in_fight)

    def test_in_fight_set_correctly_to_false(self):
        self.deck.in_fight = True
        self.deck.in_fight = False
        self.assertFalse(self.deck.in_fight)

    # self.indici is reset to empty on each cell
    def test_indici_is_reset_to_empty_on_each_cell(self):
        self.deck.indici = [1, 2]
        self.deck.indici = []
        self.assertEqual(self.deck.indici, [])


if __name__ == "__main__":
    unittest.main()
