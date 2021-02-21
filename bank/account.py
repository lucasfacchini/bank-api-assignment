class Account:
    def __init__(self, account_id):
        self.id = account_id
        self.statement = []
        self.balance = 0

    def deposit(self, value):
        if value > 0:
            self.statement.append({value: value})
            self.balance += value
            return True

        return False

    def validate_withdraw(self, value):
        return value > 0 and self.get_balance() - value >= 0

    def withdraw(self, value):
        if self.validate_withdraw(value):
            self.statement.append({value: -value})
            self.balance -= value
            return True

        return False

    def get_balance(self):
        return self.balance