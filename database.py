import datetime
import TablePrint
from passlib.hash import pbkdf2_sha256
BudgetTotal = 100
CurrentUser = "admin"
PurchaseDatabase = {}
UserDatabase = {}

class PurchaseObj:
    def __init__(self, user, amount, item, count, purpose, date):
        self.user = user
        self.amount = amount
        self.item = item
        self.count = count
        self.purpose = purpose
        self.date = date
    def printObj(self):
        print(self.user)

PurchaseDatabase[len(PurchaseDatabase)] = PurchaseObj('testuser', 1, 'drugs', 420, 'smonking', '12 oclock')
PurchaseDatabase[len(PurchaseDatabase)] = PurchaseObj('testuser', 5, 'cat', 2, 'eat', '12 oclock')
class user:
    def __init__(self, name, password, permissions):
        self.name = name
        self.password = password
        self.permissions = permissions

#TODO Stop the ability to add multiple users of same name
def AddUser():
    tmpPerms = input('What permission level would you like?: ')
    tmpName = input('Enter Username: ')
    tmpPass = input('Input a password: ')
    if tmpPass == input('Please Verify your password: '):
        UserDatabase[len(UserDatabase)] = user(tmpName, pbkdf2_sha256.hash(tmpPass), tmpPerms)
        print('User added successfully')
        tmpPerms = None
        tmpName = None
        tmpPass = None
        main()
    else:
        print("Incorrect Password, please try again")
        tmpPerms = None
        tmpName = None
        tmpPass = None
        AddUser()

def ChangeUser():
    tmpUser = input('What user would you like to log in: ')
    for k, v in UserDatabase:
        if v.name == tmpUser:
            if pbkdf2_sha256.verify(input('Please enter the password: ')) == True:
                    CurrentUser = v.name
                    print('User changed successfully')

def addPurchase():
    global BudgetTotal, CurrentUser, PurchaseDatabase
    print("\nThe current budget balance is " + str(BudgetTotal))
    amount = int(input("Input amount spent: "))
    TempBudget = BudgetTotal - amount
    item = input("What was the money spent on? ")
    count = input("How many items were purchased? ")
    purpose = input("Detail the purpose for the purchase: ")
    date = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S') 
    print("\nComplete the following purchase?")
    print("User: " + CurrentUser)
    print("Amount spent: " + str(amount))
    print("Number of items purchased: " + str(count))
    print("Reason for purchase: " + purpose)
    print("Date: " + date)
    print("New budget balance: " + str(TempBudget))

    confirmation = input("\nPlease confirm the purchase by entering YES (all caps)\n> ")
    if confirmation == 'YES':
        BudgetTotal = TempBudget
        PurchaseDatabase[len(PurchaseDatabase)] = PurchaseObj(CurrentUser, amount, item, count, purpose, date)
    else:
        print('Purchase Cancelled')
        main()
    printDatabase()
    main()
        

def printDatabase():
    global PurchaseDatabase
    DatabaseTable = []
    print('1: Date')
    print('2: Price')
    SortChoice = input('what would you like to sort by? ')
    if str(SortChoice) == '1':
        for k, v in PurchaseDatabase.items():
            DatabaseTable.append([str(v.user), str(v.amount), str(v.item), str(v.purpose), str(v.count), str(v.date)])
    
    if str(SortChoice) == '2':
        highestcost = 0
        for k, v in PurchaseDatabase.items():
            DatabaseTable.append([str(v.user), str(v.amount), str(v.item), str(v.purpose), str(v.count), str(v.date)])
            for counter, item in enumerate(DatabaseTable):
                if int(DatabaseTable[counter][1]) > int(DatabaseTable[counter - 1][1]):
                    DatabaseTable.insert(0, DatabaseTable.pop(counter))
    DatabaseTable.insert(0, ['User', 'Amount Spent', 'Item name', 'Reason for Purchase', 'Item Count', 'Purchase Date'])
    TablePrint.table(*DatabaseTable)
    print('')
    main()

def main():
    print("Current Budget Balance: " + str(BudgetTotal))
    print("What would you like to do?")
    print("1: View Database")
    print("2: Add a new purchase")
    print('3: Add a new User')
    MenuChoice = input('> ')
    if str(MenuChoice) == '1':
        printDatabase()
    if str(MenuChoice) == '2':
        addPurchase()
    if str(MenuChoice) == '3':
        AddUser()
    else:
        main()
main()
