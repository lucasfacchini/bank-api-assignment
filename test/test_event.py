import unittest

from bank.event import Event
from bank.manager import Manager

class TestEvent(unittest.TestCase):

    def setUp(self):
        self.manager = Manager()

    def test_deposit_event_create_account(self):
        event_data = {'type': Event.TYPE_DEPOSIT, 'destination': 100, 'amount': 10}

        deposit_event = Event(event_data, self.manager)
        success, result = deposit_event.execute()

        assert success == True and result['destination']['balance'] == 10

    def test_deposit_event_existing_account(self):
        account = self.manager.create_account(100)
        account.deposit(10)

        event_data = {'type': Event.TYPE_DEPOSIT, 'destination': 100, 'amount': 10}

        deposit_event = Event(event_data, self.manager)
        success, result = deposit_event.execute()

        assert success == True and result['destination']['balance'] == 20

    def test_withdraw_event_non_existing_account(self):
        event_data = {'type': Event.TYPE_WITHDRAW, 'origin': 100, 'amount': 10}

        withdraw_event = Event(event_data, self.manager)
        success, _ = withdraw_event.execute()

        assert success == False

    def test_withdraw_event_unsuficient_funds(self):
        account = self.manager.create_account(100)
        account.deposit(10)

        event_data = {'type': Event.TYPE_WITHDRAW, 'origin': 100, 'amount': 10.1}

        withdraw_event = Event(event_data, self.manager)
        success, _ = withdraw_event.execute()

        assert success == False

    def test_withdraw_event_success(self):
        account = self.manager.create_account(100)
        account.deposit(10)

        event_data = {'type': Event.TYPE_WITHDRAW, 'origin': 100, 'amount': 10}

        withdraw_event = Event(event_data, self.manager)
        success, result = withdraw_event.execute()

        assert success == True and result['origin']['balance'] == 0

    def test_transfer_event_from_non_existing_account(self):
        event_data = {'type': Event.TYPE_TRANSFER, 'origin': 100, 'amount': 15, 'destination': 300}

        transfer_event = Event(event_data, self.manager)
        success, _ = transfer_event.execute()

        assert success == False

    def test_transfer_event_unsuficient_funds(self):
        account = self.manager.create_account(100)
        account.deposit(10)

        event_data = {'type': Event.TYPE_TRANSFER, 'origin': 100, 'amount': 10.1, 'destination': 300}

        transfer_event = Event(event_data, self.manager)
        success, _ = transfer_event.execute()

        assert success == False

    def test_transfer_event_success(self):
        account = self.manager.create_account(100)
        account.deposit(10)

        event_data = {'type': Event.TYPE_TRANSFER, 'origin': 100, 'amount': 10, 'destination': 300}

        transfer_event = Event(event_data, self.manager)
        success, result = transfer_event.execute()

        assert success == True and result['origin']['balance'] == 0