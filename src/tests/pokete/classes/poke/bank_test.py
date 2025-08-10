import unittest
from unittest.mock import patch
from pokete.figure.bank import Bank

with patch('os.get_terminal_size') as mock_get_terminal_size:
    mock_get_terminal_size.return_value = (140, 40)
    from pokete.figure.bank import Bank

class bank_test(unittest.TestCase):
 
    # negative init test case
    def test_initMoneyNegative(self):
        with self.assertRaises(AssertionError):
            Bank(-10)

    # positive init test case
    def test_initMoneyPositive(self):
        bank = Bank (10)
        self.assertEqual(bank.get_money(), 10)

    # negative test case
    def test_addMoneyNegative(self):
        bank = Bank (0)
        with self.assertRaises(AssertionError):
            bank.add_money(-10)

    # boundary test case - add 0
    def test_addMoneyZero(self):
        bank = Bank (0)
        bank.add_money(0)
        self.assertEqual(bank.get_money(), 0)
 
    # positive test case
    def test_addMoneyPositive(self):
        bank = Bank(0)
        bank.add_money(10)
        self.assertEqual(bank.get_money(), 10)

if __name__ == "__main__":
    unittest.main()
