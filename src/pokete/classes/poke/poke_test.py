import unittest

from .poke import Poke

class AddXpTest(unittest.TestCase):
    def create_temp_pokete(self, current_xp):
        pokete = Poke('steini', current_xp)
        return pokete
    
    def test_criteria_A1(self):
        self.assertRaises(Exception, self.create_temp_pokete, -1)

    def test_criteria_A2(self):
        pokete = self.create_temp_pokete(0)
        result = pokete.add_xp(4)
        self.assertEqual(pokete.xp, 4, "Should be equal")
        self.assertEqual(pokete.lvl(), 2, "Should be equal")
        self.assertTrue(result, "Should return true")

    def test_criteria_A3(self):
        pokete = self.create_temp_pokete(4)
        result = pokete.add_xp(5)
        self.assertEqual(pokete.xp, 9, "Should be equal")
        self.assertEqual(pokete.lvl(), 3, "Should be equal")
        self.assertTrue(result, "Should return true")

    def test_criteria_B2(self):
        pokete = self.create_temp_pokete(0)
        result = pokete.add_xp(3)
        self.assertEqual(pokete.xp, 3, "Should be equal")
        self.assertEqual(pokete.lvl(), 2, "Should be equal")
        self.assertTrue(result, "Should return true")
    
    def test_criteria_B3(self):
        pokete = self.create_temp_pokete(9)
        result = pokete.add_xp(6)
        self.assertEqual(pokete.xp, 15, "Should be equal")
        self.assertEqual(pokete.lvl(), 4, "Should be equal")
        self.assertTrue(result, "Should return true")

    def test_criteria_C2(self):
        pokete = self.create_temp_pokete(0)
        result = pokete.add_xp(2)
        self.assertEqual(pokete.xp, 2, "Should be equal")
        self.assertEqual(pokete.lvl(), 1, "Should be equal")
        self.assertFalse(result, "Should return false")

    def test_criteria_C3(self):
        pokete = self.create_temp_pokete(19)
        result = pokete.add_xp(4)
        self.assertEqual(pokete.xp, 23, "Should be equal")
        self.assertEqual(pokete.lvl(), 4, "Should be equal")
        self.assertFalse(result, "Should return false")

    def test_criteria_D2(self):
        pokete = self.create_temp_pokete(0)
        self.assertRaises(Exception, pokete.add_xp, -1)
        self.assertEqual(pokete.xp, 0, "Should be equal")
        self.assertEqual(pokete.lvl(), 1, "Should be equal")

    def test_criteria_E3(self):
        pokete = self.create_temp_pokete(26)
        result = pokete.add_xp(0)
        self.assertEqual(pokete.xp, 26, "Should be equal")
        self.assertEqual(pokete.lvl(), 5, "Should be equal")
        self.assertFalse(result, "Should return false")

if __name__ == '__main__':
    unittest.main()
