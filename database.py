import datetime
from datetime import datetime
import TablePrint
from operator import itemgetter
import os
import csv
import sys
BudgetTotal = 100
PurchaseDatabase = {} #Purchases will be stored here as a dictionary of objects
# Purcase Object class, this will be used to define purchases
class PurchaseObj: 
    #Each of these variables will corespond with a different aspect of a purchase
    def __init__(self, user, amount, item, count, purpose, date):
        self.user = user
        self.amount = amount
        self.item = item
        self.count = count 
        self.purpose = purpose
        self.date = date

#This function is a user interface for adding a new Purchase to the database
def addPurchase():
    global BudgetTotal, CurrentUser, PurchaseDatabase #Get Global vars
    item, count, purpose, date, TempBudget = '', '', '', '', '' #Clear vars incase function is restarting due to bad input 
    print("The current budget balance is " + str(BudgetTotal))
    #Take inputs and calculate other vars
    try: 
        amount = int(input("Input amount spent: "))
    except ValueError: #make sure input is an int
        os.system('clear')
        print("Invalid Data Type")
        addPurchase()
    TempBudget = BudgetTotal - amount #Calculate new budget
    item = input("What was the money spent on? ")
    try: 
        count = int(input("How many items were purchased? "))
    except ValueError: #make sure input is an int
        os.system('clear')
        print("Invalid Data Type")
        addPurchase()
    purpose = input("Detail the purpose for the purchase: ")
    date = datetime.now().strftime('%Y-%m-%d') #Automatically get date with datetime.now()
    # Print confirmation
    os.system('clear')
    print("Complete the following purchase?")
    print("User: " + CurrentUser)
    print("Amount spent: " + str(amount))
    print("Number of items purchased: " + str(count))
    print("Reason for purchase: " + purpose)
    print("Date: " + date)
    print("New budget balance: " + str(TempBudget))
    #Get confirmation input
    confirmation = input("Please confirm the purchase by entering YES (all caps)\n> ")
    if confirmation == 'YES':
        BudgetTotal = TempBudget
        #add new purchase to end of purchase database as PurchaseObj
        PurchaseDatabase[len(PurchaseDatabase)] = PurchaseObj(CurrentUser, amount, item, count, purpose, date) 
        os.system('clear')
        print("Purchase Successful\n")
        main()
    else:
        os.system('clear')
        print('Purchase Cancelled\n')
        main() # if YES not entered, cancel purchase and return to main
        

def printDatabase():
    global PurchaseDatabase
    DatabaseTable = [] #List that PurchaseDatabase will be sorted into, and printed with Tableprint
    print('1: User')
    print('2: Price')
    print('3: Item Name')
    print('4: Purchase Purpose')
    print('5: Item Count')
    print('6: Date')
    SortChoice = str(input('what would you like to sort by? ')) # Choose what to sort by
    if SortChoice not in ['1', '2', '3', '4', '5', '6']:
        os.system('clear')
        print("Invalid Sort Choice")
        printDatabase()
    DirectionChoice = input('invert direction (y/N): ') #check for reverse
    if DirectionChoice.lower() in ['y', 'yes']:
        DirectionChoice = True
    else:
        DirectionChoice = False
    os.system('clear')
    for k, v in PurchaseDatabase.items():
        DatabaseTable.append([str(v.user), int(v.amount), str(v.item), str(v.purpose), int(v.count), str(v.date)]) #Add each object in PurchaseDatabase as list
        if SortChoice != '6':
            DatabaseTable = sorted(DatabaseTable, key=itemgetter(int(SortChoice) - 1), reverse=DirectionChoice) # Sort the list by SortChoice
        elif SortChoice == '6':
            DatabaseTable = sorted(DatabaseTable, key=lambda x: datetime.strptime(x[5], '%Y-%m-%d'), reverse=DirectionChoice) #If sorting date, use more complicated sorting method
                    
    DatabaseTable.insert(0, ['User', 'Amount Spent', 'Item name', 'Reason for Purchase', 'Item Count', 'Purchase Date']) #inset key row
    TablePrint.table(*DatabaseTable) #print table with TablePrint
    print('')
    main() #Return to main

def ExportData(location):
    if os.path.exists(location): 
        os.remove(location) 
    with open(str(location), 'a',) as csvfile:
        writer = csv.writer(csvfile)
        for k, v in PurchaseDatabase.items():
            writer.writerow([k, v.user, v.amount, v.item, v.count, v.purpose, v.date])
    csvfile.close()

def ImportData(location):
    with open(str(location)) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            PurchaseDatabase[len(PurchaseDatabase)] = PurchaseObj(row[1], row[2], row[3], row[4], row[5], row[6])

def main():
    global CurrentUser
    ExportData('exported_data.csv')
    # Simple menu systemtem, redirecting to different functions
    print("Current Budget Balance: " + str(BudgetTotal))
    print("Current User: " + CurrentUser)
    print("What would you like to do?")
    print("1: View Database")
    print("2: Add a new purchase")
    print('3: Change User')
    print("4: Exit")
    MenuChoice = input('> ')
    if str(MenuChoice) == '1':
        os.system('clear')
        printDatabase()
    if str(MenuChoice) == '2':
        os.system('clear')
        addPurchase()
    if str(MenuChoice) == '3':
        CurrentUser = input("Who Would you like to log in as?\n> ")
        print('User changed to ' + str(CurrentUser))
    if str(MenuChoice) == '4':
        os.system('clear')
        sys.exit(0)
    else:
        os.system('clear')
        main()

CurrentUser = "defaultuser"
ImportData('exported_data.csv')
main()
