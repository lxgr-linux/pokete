import unittest
from unittest.mock import patch, mock_open
from pokete.figure.bank import Bank

class bank_test(unittest.TestCase):
 

    def test_addMoneyNegative(self):
        try:
            Bank.__init__(self, -10)
        except ValueError as err:
            self.assertEqual(str(err), "Money cannot be negative")

    # boundary test case
    def test_addMoneyZero(self):
        try:
            Bank.__init__(self, 0)
        except ValueError as err:
            self.assertEqual(str(err), "Money cannot be negative")
 
    def test_addMoneyPositive(self):
        Bank.__init__(self, 10)
        self.assertEqual(Bank.get_money(self), 10)


if __name__ == "__main__":
    unittest.main()
