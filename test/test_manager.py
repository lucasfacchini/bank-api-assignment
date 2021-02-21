import unittest

from bank.manager import Manager
from bank.account import Account

class TestManager(unittest.TestCase):
    def setUp(self):
        self.manager = Manager()

    def test_account_not_exists(self):
        assert self.manager.account_exists(1234) == False

    def test_account_exists(self):
        self.manager.create_account(100)

        assert self.manager.account_exists(100) == True

    def test_get_account(self):
        self.manager.create_account(101)

        assert isinstance(self.manager.get_account(101), Account)