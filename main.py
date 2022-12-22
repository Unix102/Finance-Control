class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def changeName(self): #меняет название счёта
        new_account_name = input("Введите новое название счёта: ")
        self.name = new_account_name

    def changeBalance(self): #Изменяет сумму баланса
        new_account_balance = int(input("Введите сумму на вашем счету: "))
        self.balance = new_account_balance

    def addOperation(self):
        amount = int(input("Введите сумму дохода/расхода: "))
        type = int(input("Доход - i, расход - e: "))
        if type == "i":
            self.balance += amount
        elif type == "e":
            self.balance -= amount
        else:
            print('Введите либо доход - i либо e без ковычек.')


account = Account("ваня", 1000)
print(account.name, account.balance)
account.changeName()
print(account.name, account.balance)
account.changeBalance()
print(account.name, account.balance)
account.addOperation()
print(account.name, account.balance)