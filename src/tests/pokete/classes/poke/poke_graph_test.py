import unittest

from pokete.classes.poke import Poke

class AddXpGraphTest(unittest.TestCase):
    def create_temp_pokete(self, current_xp):
        pokete = Poke('steini', current_xp)
        return pokete
    
    def test_criteria_1(self):
        pokete = self.create_temp_pokete(19)
        result = pokete.add_xp(5)
        self.assertEqual(pokete.xp, 24, "Should be equal")
        self.assertEqual(pokete.lvl(), 5, "Should be equal")
        self.assertTrue(result, "Should return true")

    def test_criteria_2(self):
        pokete = self.create_temp_pokete(19)
        result = pokete.add_xp(4)
        self.assertEqual(pokete.xp, 23, "Should be equal")
        self.assertEqual(pokete.lvl(), 4, "Should be equal")
        self.assertFalse(result, "Should return false")

    def test_criteria_3(self):
        pokete = self.create_temp_pokete(5)
        self.assertRaises(Exception, pokete.add_xp, -4)
        self.assertEqual(pokete.xp, 5, "Should be equal")
        self.assertEqual(pokete.lvl(), 2, "Should be equal")

if __name__ == '__main__':
    unittest.main()