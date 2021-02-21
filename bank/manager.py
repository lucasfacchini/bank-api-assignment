from bank.account import Account

class Manager:
    def __init__(self):
        self.reset()

    def account_exists(self, account_id):
        return account_id in self.accounts

    def get_account(self, account_id):
        if self.account_exists(account_id):
            return self.accounts[account_id]

        return None

    def create_account(self, account_id):
        if not self.account_exists(account_id):
            self.accounts[account_id] = Account(account_id)

            return self.get_account(account_id)

        return None

    def get_account_balance(self, account_id):
        if self.account_exists(account_id):
            balance = self.get_account(account_id).get_balance()
            return True, balance

        return False, 0


    def reset(self):
        self.accounts = {}