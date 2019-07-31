import datetime
from datetime import datetime
import TablePrint
from operator import itemgetter
from passlib.hash import pbkdf2_sha256
BudgetTotal = 100
CurrentPermissions = 4
PurchaseDatabase = {}


# Purcase Object class, this will be used to define purchases
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

# Test Purchases
PurchaseDatabase[len(PurchaseDatabase)] = PurchaseObj('testuser', 1, 'a', 1, 'a', '2019-04-01')
PurchaseDatabase[len(PurchaseDatabase)] = PurchaseObj('testuser', 3, 'c', 3, 'c', '1633-01-01')
PurchaseDatabase[len(PurchaseDatabase)] = PurchaseObj('testuser', 2, 'b', 2, 'b', '2019-05-02')
PurchaseDatabase[len(PurchaseDatabase)] = PurchaseObj('testuser', 4, 'd', 4, 'd', '2019-05-03')

# User class, to be used for permission restrictions
class user:
    def __init__(self, name, password, permissions):
        self.name = name
        self.password = password
        self.permissions = permissions

admin =  user("admin", pbkdf2_sha256.hash("password"), 4)
UserDatabase = {0: admin,}
CurrentUser = "admin"

def AddUser():
    global UserDatabase 
    tmpPerms = None
    tmpName = None
    tmpPass = None
    # get temp vars to use for user generation
    tmpPerms = input('What permission level would you like?: ') 
    try:
        if int(tmpPerms) not in [0, 1, 2, 3]:
            print("Permissions must be 0, 1, 2 or 3")
            AddUser()
    except ValueError:
        print("Permissions must be 0, 1, 2 or 3")
        AddUser()
    tmpPerms = int(tmpPerms)
    tmpName = input('Enter Username: ')
    for k, v in UserDatabase.items():
        if v.name == tmpName:
            print("user under that name already exists, returning to main menu")
            main()
    tmpPass = input('Input a password: ')
    if tmpPass == input('Please Verify your password: '):
        UserDatabase[len(UserDatabase)] = user(tmpName, pbkdf2_sha256.hash(tmpPass), tmpPerms) #Creates user from tmp variables, encrypting pass with sha256
        print('User added successfully')
        main()
    else: # If password wrong, reset temp vars and rerun
        print("Incorrect Password, please try again")
        AddUser()

def ChangeUser():
    global CurrentUser, CurrentPermissions, UserDatabase
    tmpUser = input('What user would you like to log in: ')
    for k, v in UserDatabase.items():
        if v.name == tmpUser: #Make sure user exists
            if pbkdf2_sha256.verify(input('Please enter the password: '), v.password) == True: #check password
                    CurrentUser = v.name #Change current user to new user
                    CurrentPermissions = v.permissions
                    print('User changed successfully')
                    main()
            else:
                print('Incorrect Password')
                ChangeUser()
    print("User does not exist")

def addPurchase():
    global BudgetTotal, CurrentUser, PurchaseDatabase
    print("\nThe current budget balance is " + str(BudgetTotal))
    #Take inputs and calculate other vars
    amount = int(input("Input amount spent: "))
    TempBudget = BudgetTotal - amount
    item = input("What was the money spent on? ")
    count = input("How many items were purchased? ")
    purpose = input("Detail the purpose for the purchase: ")
    date = datetime.datetime.now().strftime('%Y-%m-%d') 
    # Print confirmation
    print("\nComplete the following purchase?")
    print("User: " + CurrentUser)
    print("Amount spent: " + str(amount))
    print("Number of items purchased: " + str(count))
    print("Reason for purchase: " + purpose)
    print("Date: " + date)
    print("New budget balance: " + str(TempBudget))
    #Get confirmation input
    confirmation = input("\nPlease confirm the purchase by entering YES (all caps)\n> ")
    if confirmation == 'YES':
        BudgetTotal = TempBudget
        #add new purchase to end of purchase database as PurchaseObj
        PurchaseDatabase[len(PurchaseDatabase)] = PurchaseObj(CurrentUser, amount, item, count, purpose, date) 
    else:
        print('Purchase Cancelled')
        main() # if YES not entered, cancel purchase and return to main
    main()
        

def printDatabase():
    global PurchaseDatabase
    DatabaseTable = [] #List that PurhaseDatabase will be sorted into, and printed with Tableprint
    print('1: User')
    print('2: Price')
    print('3: Item Name')
    print('4: Item Count')
    print('5: Date')
    SortChoice = input('what would you like to sort by? ') # Choose what to sort by
    DirectionChoice = input('invert direction (y/N): ') #check for reverse
    if DirectionChoice.lower() in ['y', 'yes']:
        DirectionChoice = True
    else:
        DirectionChoice = False
    for k, v in PurchaseDatabase.items():
        DatabaseTable.append([str(v.user), str(v.amount), str(v.item), str(v.purpose), str(v.count), str(v.date)]) #Add each object in PurchaseDatabase as list
        if SortChoice != '5':
            DatabaseTable = sorted(DatabaseTable, key=itemgetter(int(SortChoice) - 1), reverse=DirectionChoice) # Sort the list by SortChoice
        else:
            DatabaseTable = sorted(DatabaseTable, key=lambda x: datetime.strptime(x[5], '%Y-%m-%d'), reverse=DirectionChoice) #If sorting date, use more complicated sorting method
                    
    DatabaseTable.insert(0, ['User', 'Amount Spent', 'Item name', 'Reason for Purchase', 'Item Count', 'Purchase Date']) #inset key row
    TablePrint.table(*DatabaseTable) #print table with TablePrint
    print('')
    main() #Return to main

def main():
    # Simple menu system, redirecting to different functions
    print("Current Budget Balance: " + str(BudgetTotal))
    print("Current User: " + CurrentUser)
    print("Current Permissions: " + str(CurrentPermissions))
    print("What would you like to do?")
    print("1: View Database")
    print("2: Add a new purchase")
    print('3: Add a new User')
    print('4: Change User')
    MenuChoice = input('> ')
    if str(MenuChoice) == '1':
        if CurrentPermissions >= 1:
            printDatabase()
        else:
            print('Insufficent Permissions')
    if str(MenuChoice) == '2':
        if CurrentPermissions >= 2:
            addPurchase()
        else:
            print('Insufficent Permissions')
    if str(MenuChoice) == '3':
        if CurrentPermissions >= 3:
            AddUser()
        else:
            print('Insufficent Permissions')
    if str(MenuChoice) == '4':
        ChangeUser()
    else:
        main()
main()
