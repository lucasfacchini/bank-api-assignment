class Event:
    TYPE_DEPOSIT = 'deposit'
    TYPE_WITHDRAW = 'withdraw'
    TYPE_TRANSFER = 'transfer'

    def __init__(self, event, manager):
        self.type = event['type']
        self.event = event
        self.manager = manager

    def execute(self):
        if self.type == self.TYPE_DEPOSIT:
            return self.deposit()
        elif self.type == self.TYPE_WITHDRAW:
            return self.withdraw()
        elif self.type == self.TYPE_TRANSFER:
            return self.transfer()
        else:
            print('Tipo de operação não reconhecida', str(self.event))

            return False, {}

    def validate_deposit(self):
        return {'destination', 'amount'}.issubset(set(self.event.keys()))

    def deposit(self):
        if not self.validate_deposit():
            return False, {}

        account = None
        if self.manager.account_exists(self.event['destination']):
            account = self.manager.get_account(self.event['destination'])
        else:
            account = self.manager.create_account(self.event['destination'])

        if account:
            success = account.deposit(self.event['amount'])

            if success:
                return True, {'destination': {'id': self.event['destination'], 'balance': account.get_balance()}}

        return False, {}

    def validate_withdraw(self):
        return {'origin', 'amount'}.issubset(set(self.event.keys()))

    def withdraw(self):
        if self.validate_withdraw() and self.manager.account_exists(self.event['origin']):
            account = self.manager.get_account(self.event['origin'])
            success = account.withdraw(self.event['amount'])

            if success:
                return True, {'origin': {'id': self.event['origin'], 'balance': account.get_balance()}}

        return False, {}

    def validate_transfer(self):
        return {'origin', 'amount', 'destination'}.issubset(set(self.event.keys()))

    def transfer(self):
        if not self.validate_transfer():
            return False, {}

        origin_account, destination_account = None, None

        if self.manager.account_exists(self.event['origin']):
            origin_account = self.manager.get_account(self.event['origin'])

        if not origin_account or not origin_account.validate_withdraw(self.event['amount']):
            return False, {}

        if self.manager.account_exists(self.event['destination']):
            destination_account = self.manager.get_account(self.event['destination'])
        else:
            destination_account = self.manager.create_account(self.event['destination'])

        if origin_account and destination_account:
            success = origin_account.withdraw(self.event['amount'])

            if success:
                destination_account.deposit(self.event['amount'])

                return True, {
                    'origin': {
                        'id': self.event['origin'], 'balance': origin_account.get_balance()
                    },
                    'destination': {
                        'id': self.event['destination'], 'balance': destination_account.get_balance()
                    }
                }

        return False, {}