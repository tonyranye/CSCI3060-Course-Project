import time
import os
import sys
from BankSystem import BankSystem, loadAllAccountsFromFile
from Account import *
from config import *
# from src.account_modification import *
# from src.transactions import *




"""

PROGRAM INTENTION:
    Command-line banking application supporting standard user and admin sessions.
    Provides banking operations through an interactive menu system including
    login, withdraw, transfer, deposit, paybill, and admin functions (create,
    delete, disable accounts, change payment plans).

GROUP MEMBERS:
    Jared Efrem, Sumukh Jagirdar, Tony Akinniranye

INPUT FILES:
    - accounts/accounts_valid.json: Current user accounts (JSON format)

OUTPUT FILES:
    - accounts/accounts_valid.json: Updated account balances after transactions
    - t_data.txt: Daily transaction log (appended at logout)

INPUTS (STDIN):
    User menu selections, transaction amounts, account credentials

OUTPUTS (STDOUT):
    Menu displays, transaction confirmations, error messages, account info

HOW TO RUN:
    1. Ensure Python 3.x and required files are present (BankSystem.py, 
       Account.py, accounts/accounts_valid.json)
    2. Run: python main.py
    3. Select operations from menu (must login first)
    4. Logout to save transaction log before exiting

"""

# TEST MODE - set to True for concise test output, False for full dialogue
TEST_MODE=True
MADE_DURING_SESSION = False



# LOAD ALL ACCOUNTS AT STARTUP

'Loads the number of acccounts inside the file'



# global bank instance

bank = BankSystem()
session_transfer_limit = 1000.00

'prints a welcome message'
def welcome():
    normal_print("\n--------------------------------------------------------------------")
    normal_print("Welcome To JST Banking! ")
    normal_print("developed by\n \nJared Efrem\nSumukh Jagirdar\nTony Akinniranye")
    normal_print("--------------------------------------------------------------------")
    while True:
        try:
            selection = mainMenu()
           
            if selection is None or selection.lower() == "logout":
                break
        except EOFError:
            normal_print("\nEnd of input reached. Exiting...")
            break

'Lists the avaliable options in the main menu'
def mainMenu():
    normal_print("\nWhat would you like to do today? Enter a option from the choices below\n")
    normal_print("Login") 
    normal_print("Withdraw")
    normal_print("Transfer")
    normal_print("Paybills")
    normal_print("Deposit")
    normal_print("Create Account")
    normal_print("Delete Account")
    normal_print("Disable Account")
    normal_print("Change Plan")
    normal_print("Logout\n")
    normal_print("EXIT\n")
    
    try:
        menuSelection = input()
        if menuSelection.strip() == "":
                return None
        handleChoice(menuSelection)
        return menuSelection
    except EOFError:
        return None


'Handle choice functions allows the program to handle when the user selects diffrent choices from the main menu'
def handleChoice(choice):
    global MADE_DURING_SESSION
    choice = choice.lower()
    normal_print(f'CHOICE: {choice}')
    
    if choice == "login":
        normal_print("LOGIN SELECTED...")
        bank.login()
        

        
    elif choice == "exit": 
        normal_print("LOGOUT SELECTED..." if bank.is_logged_in else "")
        if bank.is_logged_in:
            bank.logout()
        MADE_DURING_SESSION = False
        normal_print("Thank You for choosing JST Banking!")
        sys.exit()
        
    elif bank.current_user == None and (choice != "login" or choice != "exit"):
        test_print("Error: Login Required")
        normal_print("\n------------ Login Required, please login first ------------")
        
    elif MADE_DURING_SESSION == True:
        print("NOTE: No transactions available in the same session as account creation, please login again to perform transactions")

    
    elif choice == "withdraw":
        normal_print("WITHDRAW SELECTED...")
        if bank.isAuthorized('withdraw'):
            success, account, amount = bank.withdraw()
            if success and account:
                bank.t_activity("01", account.name, account.acc_num, amount)    
            
            
        
    elif choice == "transfer":
        normal_print("TRANSFER SELECTED...")
        if bank.isAuthorized('transfer'):
            sucess, amount = bank.transferMoney()
            if sucess:
                bank.t_activity("02", bank.current_user.name, bank.current_user.acc_num, amount)
        
            
    elif choice == "paybills":
        normal_print("PAY BILLS SELECTED...")
        if bank.isAuthorized('paybills'):
            p_a= float(input())
            bank.current_user.payBills(p_a)
            bank.t_activity("03", bank.current_user.name, bank.current_user.acc_num, p_a)
            
    # here  
    elif choice == "deposit":
        normal_print("DEPOSIT SELECTED...")
        if bank.isAuthorized('deposit'):
            success, account, amount = bank.depositMoney()
            if success and account:
                bank.t_activity("04", account.name, account.acc_num, amount)
            
        
    elif choice == "create account":
        normal_print("CREATE ACCOUNT SELECTED...")
        
        if bank.isAuthorized('create'):
           _, balance= bank.createAccount()
           MADE_DURING_SESSION = True
           bank.t_activity("05", _.name, _.acc_num, balance)
    
    elif choice == "delete account":
        normal_print("DELETE ACCOUNT SELECTED...")
        if bank.isAuthorized('delete'):
           
            name, num = bank.Delete_Account()
            bank.t_activity("06", name, num, 0)
        
    elif choice == "disable account":
        normal_print("DISABLE ACCOUNT SELECTED...")
        if bank.isAuthorized('disable'):
            name, num = bank.Disable_Account()
            bank.t_activity("07", name, num, 0)

        
    elif choice == "change plan":
        normal_print("CHANGE PLAN SELECTED...")
        if bank.isAuthorized('changeplan'):
            name,num = bank.change_plan()
            bank.t_activity("08", name, num, 0)
        
    elif choice == "logout":
        normal_print("LOGOUT SELECTED...")
        bank.t_activity("00", bank.current_user.name, bank.current_user.acc_num, 0)
        bank.logout()  
            
    else:
        test_print("Error: Invalid choice")
        normal_print("\nInvalid choice! Please try again.\n")
        normal_print("--------------------------------------------------------------------\n")
        time.sleep(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Use: python main.py <current_accounts_file> <transaction_output_file>")
        sys.exit(1)

    
    accounts_file = sys.argv[1]
    transaction_log_file = sys.argv[2]
    loadAllAccountsFromFile(accounts_file)
    bank.transaction_file_path = transaction_log_file

    welcome()