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

    # --- more choose tests ---
    #test that empty pokes list returns None
    #Fallback identifier returns None even with hp > 0
    #In fight with hp == 0 returns None
    #In fight with hp > 0 returns the correct index

    # --- deck state setup tests ---
    #self.pokes is correctly sliced to p_len from figure.pokes
    #self.in_fight is set correctly
    #self.indici is reset to empty on each cell




if __name__ == "__main__":
    unittest.main()
