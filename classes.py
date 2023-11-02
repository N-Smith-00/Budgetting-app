from datetime import datetime

class User():
    def __init__(self, name: str, starting_balance: float, user_list: list):
        self._name = name
        self._balance = starting_balance
        self._transactions = []
        
    def get_name(self):
        return self._name
    
    def set_name(self, name: str):
        self._name = name
    
    def get_balance(self):
        return self._balance
    
    def get_transactions(self):
        return self._transactions

    def create_transaction(self, amount: float, date: str, description: str, debit: bool):
        self._transactions.append(Transaction(amount, date, description, debit, self))
    
    def delete_transaction(self, transaction):
        self._transactions.remove(transaction)
    
class Transaction():
    def __init__(self, amount: float, date: str, debit: bool, user: User, description: str=''):
        self.date = self._check_date(date)
        if debit:
            self.amount = -amount
            
    def __str__(self):
        return f"{self.date} {self.amount} {self.description}"
    
    def get_amount(self):
        return self.amount
    
    def get_date(self):
        return self.date
    
    def get_description(self):
        return self.description
    
    def get_type(self):
        if self.debit:
            return "Debit"
        else:
            return "Credit"
    
    def set_date(self, date):
        self.date = self._check_date(date)
    
    def set_description(self, description: str):
        self.description = description
    
    def set_amount(self, amount: float, debit: bool):
        self.amount = amount
        if debit:
            self.amount = -amount
    
    def _check_date(self, date: str):
        try:
            return datetime.strptime(date, "%d %m %Y")
        except ValueError:
            raise ValueError("Incorrect date format, should be DD MM YYYY")


