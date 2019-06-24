import datetime
import TablePrint
BudgetTotal = 100
CurrentUser = "admin"
PurchaseDatabase = {}

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
    DatabaseTable = [['User', 'Amount Spent', 'Item name', 'Reason for Purchase', 'Item Count', 'Purchase Date']]
    for k, v in PurchaseDatabase.items():
        DatabaseTable.append([str(v.user), str(v.amount), str(v.item), str(v.purpose), str(v.count), str(v.date)])
    TablePrint.table(*DatabaseTable)
    print('')
    main()

def main():
    print("Current Budget Balance: " + str(BudgetTotal))
    print("What would you like to do?")
    print("1: View Database")
    print("2: Add a new purchase")
    MenuChoice = input('> ')
    if str(MenuChoice) == '1':
        printDatabase()
    if str(MenuChoice) == '2':
        addPurchase()
    else:
        main()
main()
