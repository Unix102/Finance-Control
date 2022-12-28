import openpyxl
import os

'''
Для синхронизации с таблицей нам нужно следущее: 
import openpyxl  (по факту уже есть)
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.append([name, ]) ну и сюда соответствующие элементы которые мы хотим добавить.

workbook.save("C:\\data.xlsx")
print("Сохранено на C:\\data.xlsx")
'''

logs = []


class Main():
    def __init__(self, name):
        self.name = name
        self.accounts = {}
        self.selected_account = None


    def select_account(self, name):
        self.selected_account = name
        logs.append('[INFO] Счёт успешно выбран!')

    def get_selected_account(self, name):
        return self.accounts[self.selected_account]

    def add_account(self, name: str = 'Счёт', balance: float = 0.0, plus: float = 0.0, minus: float = 0.0, transactions: float = 0.0, operations: list = []):
        self.accounts[name] = Account(name, balance, plus, minus, transactions, operations)
        logs.append('[INFO] Счёт успешно создан!')

    def delete_account(self, name):
        del self.accounts[f'{name}']
        logs.append('[INFO] Счёт успешно удалён!')



class Account():
    def __init__(self, name: str = 'Счёт', balance: float = 0.0, plus: float = 0.0, minus: float = 0.0, transactions: float = 0.0, operations: list = []):
        self.name = name
        self.balance = balance
        self.plus = plus
        self.minus = minus
        self.transactions = transactions
        self.operations = operations


    def set_name(self, name: str): # Изменяет название счёта
        self.name = str(name)
        logs.append('[INFO] Название счёта успешно изменено!')


    def set_balance(self, balance: float): # Изменяет сумму на балансе
        self.balance = round(float(balance), 2)
        logs.append('[INFO] Сумма на балансе успешно установлена!')


    def set_plus(self, plus: float):
        self.plus = float(plus)
        logs.append('[INFO] Сумма доходов успешно установена!')

    def change_plus(self, plus: float): # Изменяет сумму дохода
        self.set_balance(self.balance - self.plus)
        self.plus = self.plus + float(plus)
        self.set_balance(self.balance + self.plus)
        logs.append('[INFO] Сумма доходов успешно изменена!')


    def set_minus(self, minus: float):
        self.minus = float(minus)
        logs.append('[INFO] Сумма расходов успешно установена!')

    def change_minus(self, minus: float): # Изменяет сумму расхода
        self.set_balance(self.balance + self.minus)
        self.minus = self.minus + float(minus)
        self.set_balance(self.balance - self.minus)
        logs.append('[INFO] Сумма расходов успешно изменена!')


    def set_transactions(self, transactions: float):
        self.transactions = float(transactions)
        logs.append('[INFO] Сумма переводов успешно установена!')

    def change_transactions(self, transactions: float): # Изменяет сумму переводов
        self.set_balance(self.balance - self.transactions)
        self.transactions = self.transactions + float(transactions)
        self.set_balance(self.balance + self.transactions)
        logs.append('[INFO] Сумма переводов успешно изменена!')


    def add_operation(self, date: str, type: str, amount: float, description: str):
        self.operations.append( Operation(date, type, amount, description) )
        logs.append('[INFO] Операция успешно создана!')

    def delete_operation(self, index):
        if self.operations[index].type == 'Доход':
            self.balance = self.balance - self.operations[index].amount
            self.plus = self.plus - self.operations[index].amount
        elif self.operations[index].type == 'Расход':
            self.balance = self.balance + self.operations[index].amount
            self.minus = self.minus - self.operations[index].amount
        elif self.operations[index].type == 'Перевод':
            self.balance = self.balance - self.operations[index].amount
            self.transactions = self.transactions - self.operations[index].amount
        self.operations.pop(index)
        logs.append('[INFO] Операция успешно удалена!')



class Operation():
    def __init__(self, date: str, type: str, amount: float, description: str):
        self.date = date
        self.type = type
        self.amount = float(amount)
        self.description = description
    
    def change_amount(self, amount):
        self.amount = float(amount)
        logs.append('[INFO] Сумма операции успешно изменена!')




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
                symbol = '+' if operation.type == 'Доход' else ''

            print(f'│ {operation.date:<20}{operation.type:<15}{symbol+str(operation.amount)+"₽":<15}{operation.description:<15}│')


        print(f'└{"─" * 66}┘')
        print()


        command = input('> ')
        command = command.split(' ')
        print()

        
        if command[0] == 'help':
            print('operation add/delete/change - Управление операциями \n\naccount new/select/set name/balance/plus/minus/transactions - Управление аккаунтами \n\nlogs - Просмотр логов')
            input()

        if command[0] == 'operation':
            try:
                if command[1] == 'add':
                    data = input('Данные операции (через ";"): ').split(';')
                    if data[1] == 'Доход':
                        account.change_plus(data[2])
                    elif data[1] == 'Расход':
                        account.change_minus(data[2])
                    elif data[1] == 'Перевод':
                        account.change_transactions(data[2])
                    account.add_operation(*data)

                elif command[1] == 'delete':
                    index = int(input('Порядковый номер операции, которую нужно удалить: ')) - 1
                    account.delete_operation(index)

                elif command[1] == 'change':
                    index, amount = input('Порядковый номер операции, и сумма для изменения (через ";"): ').split(';')
                    account.operations[int(index)-1].change_amount(float(amount))
            except Exception as e:
                logs.append('[ERROR] ' + str(e))
                print('Example: "operation add/delete/change"')
                input()


        elif command[0] == 'account':
            try:
                if command[1] == 'set':
                    if command[2] == 'name':
                        name = input('Новое имя счёта: ')
                        account.set_name(name)
                    elif command[2] == 'balance':
                        account.set_balance(command[3])
                    elif command[2] == 'plus':
                        account.set_plus(command[3])
                    elif command[2] == 'minus':
                        account.set_minus(command[3])
                    elif command[2] == 'transactions':
                        account.set_transactions(command[3])

                elif command[1] == 'new':
                    name = input('Имя нового счёта: ')
                    main.accounts[name] = Account(name)
                elif command[1] == 'select':
                    x = 1
                    for i in main.accounts:
                        print(f'{x}) {i}')
                        x+=1
                    main.select_account(main.accounts[int(command[3])-1])
            except Exception as e:
                logs.append('[ERROR] ' + str(e))
                print('Example: "account new/select {number}/set name/balance/plus/minus/transactions {amount}"')
                input()

        elif command[0] == 'logs':
            for i in logs:
                print(i)
            input()





