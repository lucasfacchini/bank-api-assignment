import unittest

from bank.account import Account

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account(100)

    def test_deposit(self):
        self.account.deposit(10)
        assert self.account.balance == 10

    def test_withdraw_invalid(self):
        assert self.account.withdraw(1) == False

    def test_withdraw_success(self):
        self.account.deposit(1)
        assert self.account.withdraw(1) == True

    def test_get_balance(self):
        assert self.account.get_balance() == 0
        self.account.deposit(1)
        assert self.account.get_balance() == 1