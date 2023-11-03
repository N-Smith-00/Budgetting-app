from datetime import datetime
import marshmallow


class Transaction():
    def __init__(self, amount: float, date: str, debit: bool, description: str=''):
        self.date = self._check_date(date)
        if debit:
            self.amount = -amount
            
    def __repr__(self):
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
        

class TransactionSchema(marshmallow.Schema):
    amount = marshmallow.fields.Float()
    date = marshmallow.fields.Date()
    description = marshmallow.fields.Str()
    debit = marshmallow.fields.Boolean()
    

class User():
    def __init__(self, username: str, password: str, starting_balance: float):
        self._name = username
        self.password = password
        self._balance = starting_balance
        self._transactions = []
        
    def get_name(self):
        return self._name
    
    def set_username(self, username: str):
        self._name = username
    
    def get_balance(self):
        return self._balance
    
    def get_transactions(self):
        return self._transactions

    def create_transaction(self, amount: float, date: str, description: str, debit: bool):
        self._transactions.append(Transaction(amount, date, description, debit, self))
    
    def delete_transaction(self, transaction):
        self._transactions.remove(transaction)
    
    def save(self):
        self.transactions = marshmallow.dump(self._transactions)
        
        
class UserSchema(marshmallow.Schema):
    username = marshmallow.fields.Str()
    password = marshmallow.fields.Str()
    balance = marshmallow.fields.Float()
    transactions = marshmallow.fields.List(marshmallow.fields.Nested(TransactionSchema))
    

class App():
    def __init__(self):
        self._users = []
        self._current_user = None
        self.running = True
    
    def run(self):
        while self.running:
            if User == None:
                self._main_menu()
    
    def _exit(self):
        self.running = False
        for user in self._users:
            user.save()
            
    def _main_menu(self):
        print("1. Login")
        print("2. Create User")
        print("3. Exit")
        choice = input("Enter choice: ")
        match choice:
            case '1':
                self._login()
            case '2':
                self._create_user()
            case '3':
                self.running = False
    
    def _create_user(self):
        unique = False
        while not unique:
            username = input("Username: ")
            if username in self._users:
                print("Username already exists")
            else:
                unique = True
            
        matching = False
        while not matching:
            password = input("Password: ")
            password2 = input("Confirm Password: ")
            if password != password2:
                print("Passwords do not match")
            else:
                matching = True
        
        num = False
        while not num:
            try:
                starting_balance = float(input("Starting Balance: "))
                num = True
            except ValueError:
                print("Starting balance must be a number")
    
        self._users.append(User(username, password, starting_balance))
        
        return
    
    def _login(self):
        username = input("Username: ")
        password = input("Password: ")
        for user in self._users:
            if user.get_name() == username and user.password == password:
                self._current_user = user
                return
        print("Incorrect username or password")
    
    def _user_menu(self):
        print("1. View Balance")
        print("2. View Transactions")
        print("3. Add Transaction")
        print("4. Delete Transaction")
        print("5. Logout")
        print("6. Exit")
        choice = input("Enter choice: ")
        match choice:
            case '1':
                self._view_balance()
            case '2':
                self._view_transactions()
            case '3':
                self._add_transaction()
            case '4':
                self._delete_transaction()
            case '5':
                self._current_user = None
            case '6':
                self._exit()
            
        