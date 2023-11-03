from datetime import datetime
import marshmallow


class Transaction():
    def __init__(self, amount: float, date: str, debit: bool, description: str='') -> None:
        self.date = self._check_date(date)
        if debit:
            self.amount = -amount
            
    def __repr__(self) -> str:
        return f"{self.date} {self.amount} {self.description}"
    
    def get_amount(self) -> float:
        return self.amount
    
    def get_date(self) -> datetime:
        return self.date
    
    def get_description(self) -> str:
        return self.description
    
    def get_type(self) -> str:
        if self.debit:
            return "Debit"
        else:
            return "Credit"
    
    def set_date(self, date) -> None:
        self.date = self._check_date(date)
    
    def set_description(self, description: str) -> None:
        self.description = description
    
    def set_amount(self, amount: float, debit: bool) -> None:
        self.amount = amount
        if debit:
            self.amount = -amount
    
    def _check_date(self, date: str) -> datetime:
        try:
            return datetime.strptime(date, "%d %m %Y")
        except ValueError:
            raise ValueError("Incorrect date format, should be DD MM YYYY")
        

class TransactionSchema(marshmallow.Schema):
    amount = marshmallow.fields.Float()
    date = marshmallow.fields.Date()
    description = marshmallow.fields.Str()
    debit = marshmallow.fields.Boolean()
    
    @marshmallow.post_load
    def make_transaction(self, data, **kwargs):
        return Transaction(**data)
    

class User():
    def __init__(self, username: str, password: str, balance: float, transactions: [Transaction]=[], spending: float=0) -> None:
        self._name = username
        self.password = password
        self._balance = balance
        self._transactions = transactions
        self._spending_target = spending
        
    def get_name(self) -> str:
        return self._name
    
    def set_username(self, username: str) -> None:
        self._name = username
    
    def get_balance(self) -> float:
        return self._balance
    
    def get_transactions(self) -> list:
        return self._transactions
    
    def get_transaction_ids(self) -> list:
        return [transaction.id for transaction in self._transactions]
    
    def get_spending(self) -> float:
        return self._spending_target

    def create_transaction(self, amount: float, date: str, description: str, debit: bool) -> None:
        self._transactions.append(Transaction(amount, date, description, debit, self))
        if debit:
            self._balance -= amount
        else:
            self._balance += amount
    
    def delete_transaction(self, transaction) -> None:
        self._transactions.remove(transaction)
        
        
class UserSchema(marshmallow.Schema):
    username = marshmallow.fields.Str()
    password = marshmallow.fields.Str()
    balance = marshmallow.fields.Float()
    transactions = marshmallow.fields.List(marshmallow.fields.Nested(TransactionSchema))
    spending = marshmallow.fields.Float()
    
    @marshmallow.post_load
    def make_user(self, data, **kwargs):
        return User(**data)
    

class App():
    def __init__(self, transaction_ids: [str]=[], users: [User]=[]) -> None:
        self._transaction_ids = transaction_ids
        self._users = users
        self._current_user = None
        self.running = True
    
    def run(self) -> None:
        while self.running:
            if User == None:
                self._main_menu()
    
    def _exit(self) -> None:
        self.running = False
        result = AppSchema().dumps(self)
        with open("data.txt", "w") as file:
            file.write(result)
        file.close()
            
    def _main_menu(self) -> None:
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
    
    def _login(self) -> None:
        username = input("Username: ")
        password = input("Password: ")
        for user in self._users:
            if user.get_name() == username and user.password == password:
                self._current_user = user
                return
        print("Incorrect username or password")
    
    def _user_menu(self) -> None:
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
    
            
class AppSchema(marshmallow.Schema):
    transaction_ids = marshmallow.fields.List(marshmallow.fields.Str())
    users = marshmallow.fields.List(marshmallow.fields.Nested(UserSchema))
    
    @marshmallow.post_load
    def make_app(self, data, **kwargs):
        return App(**data)