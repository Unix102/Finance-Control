import openpyxl
import os

messages = []


class Main():
    def __init__(self, name):
        self.name = name
        self.accounts = {}
        self.selected_account = None

    def select_account(self, name):
        self.selected_account = name

    def get_selected_account(self, name):
        return self.accounts[self.selected_account]

    def add_account(self, name: str = 'Счёт', balance: float = 0.0, plus: float = 0.0, minus: float = 0.0, transactions: float = 0.0, operations: list = []):
        self.accounts[name] = Account(name, balance, plus, minus, transactions, operations)
        messages.append('[INFO] Счёт успешно создан!')

    def delete_account(self, name):
        del self.accounts[f'{name}']
        messages.append('[INFO] Счёт успешно удалён!')


class Account():
    def __init__(self, name: str = 'Счёт', balance: float = 0.0, plus: float = 0.0, minus: float = 0.0, transactions: float = 0.0, operations: list = []):
        self.name = name
        self.balance = balance
        self.plus = plus
        self.minus = minus
        self.transactions = transactions
        self.operations = operations

    def change_name(self, name: str): # Изменяет название счёта
        self.name = name
        messages.append('[INFO] Название счёта успешно изменено!')

    def change_balance(self, balance: float): # Изменяет сумму на балансе
        self.balance = round(float(balance), 2)
        messages.append('[INFO] Сумма на балансе успешно изменена!')

    def change_plus(self, plus: float): # Изменяет сумму дохода
        self.change_balance(self.balance - self.plus)
        self.plus = self.plus + float(plus)
        self.change_balance(self.balance + self.plus)
        messages.append('[INFO] Сумма доходов успешно изменена!')

    def change_minus(self, minus: float): # Изменяет сумму расхода
        self.change_balance(self.balance + self.minus)
        self.minus = self.minus + float(minus)
        self.change_balance(self.balance - self.minus)
        messages.append('[INFO] Сумма расходов успешно изменена!')

    def change_transactions(self, transactions: float): # Изменяет сумму переводов
        self.change_balance(self.balance - self.transactions)
        self.transactions = self.transactions + float(transactions)
        self.change_balance(self.balance + self.transactions)
        messages.append('[INFO] Сумма переводов успешно изменена!')

    def add_operation(self, date, type, amount, description):
        self.operations.append( Operation(date, type, amount, description) )
        messages.append('[INFO] Операция успешно создана!')

    def delete_operation(self, index):
        self.operations.pop(index)
        messages.append('[INFO] Операция успешно удалена!')


class Operation():
    def __init__(self, date, type, amount, description):
        self.date = date
        self.type = type
        self.amount = float(amount)
        self.description = description
    
    def change_amount(self, amount):
        self.amount = amount
        messages.append('[INFO] Сумма операции успешно изменена!')




if __name__ == '__main__':
    name = input('Введите ваше имя: ')
    account = input('Введите название счёта: ')
    main = Main(name)
    main.add_account(account)
    main.select_account(account)

    while True:
        account = main.accounts[main.selected_account]

        os.system('cls')

        print(f'''
┌{"─" * 66}┐
│ {account.name:<20}{"Доход":<15}{"Расход":<15}{"Переводы":<15}│
│ {str(account.balance)+"₽":<20}{"+"+str(account.plus)+"₽":<15}{"-"+str(account.minus)+"₽":<15}{str(account.transactions)+"₽":<15}│
│{" " * 66}│
│{" " * 66}│''')


        for operation in account.operations:

            if operation.type == 'Перевод':
                symbol = '+' if operation.amount > 0 else ''
            else:
                symbol = '+' if operation.type == 'Доход' else '-'

            print(f'│ {operation.date:<20}{operation.type:<15}{symbol+str(operation.amount)+"₽":<15}{operation.description:<15}│')


        print(f'└{"─" * 66}┘')
        print()


        command = input('> ')
        command = command.split(' ')
        
        if command[0] == 'operation':
            if command[1] == 'add':
                data = input('Данные операции (через ";"): ').split(';')
                if data[1] == 'Доход':
                    account.change_plus(data[2])
                elif data[1] == 'Расход':
                    account.change_minus(data[2])
                elif data[1] == 'Перевод':
                    account.change_transactions(data[2])

                account.add_operation(*data)

