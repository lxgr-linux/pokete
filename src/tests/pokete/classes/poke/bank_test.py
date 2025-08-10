import unittest
from unittest.mock import patch

with patch('os.get_terminal_size') as mock_get_terminal_size:
    mock_get_terminal_size.return_value = (140, 40)
    from pokete.figure.bank import Bank

class bank_test(unittest.TestCase):
 
    # negative test case
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
 
    # positive test case
    def test_addMoneyPositive(self):
        Bank.__init__(self, 10)
        self.assertEqual(Bank.get_money(self), 10)


if __name__ == "__main__":
    unittest.main()
