import time
import os
import sys
from BankSystem import BankSystem, loadAllAccountsFromFile
from Account import *
from src.account_modification import *
from src.transactions import *
from src.account_modification.deleteAccount import *




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







# LOAD ALL ACCOUNTS AT STARTUP

'Loads the number of acccounts inside the file'



# global bank instance

bank = BankSystem()
session_transfer_limit = 1000.00

'prints a welcome message'
def welcome():
    print("\n--------------------------------------------------------------------")
    print("Welcome To JST Banking! ")
    print("developed by\n \nJared Efrem\nSumukh Jagirdar\nTony Akinniranye")
    print("--------------------------------------------------------------------")
    while True:
        try:
            selection = mainMenu()
           
            if selection is None or selection.lower() == "logout":
                break
        except EOFError:
           
            print("\nEnd of input reached. Exiting...")
            break

'Lists the avaliable options in the main menu'
def mainMenu():
    print("\nWhat would you like to do today? Select from the options below\n")
    print("Login") 
    print("Withdraw")
    print("Transfer")
    print("Paybills")
    print("Deposit")
    print("Create Account")
    print("Delete Account")
    print("Disable Account")
    print("Change Current Plan")
    print("Logout\n")
    print("EXIT")
    
    try:
        menuSelection = input("\nEnter Choice: ")
        if menuSelection.strip() == "":
                return None
        handleChoice(menuSelection)
        return menuSelection
    except EOFError:
        return None


'Handle choice functions allows the program to handle when the user selects diffrent choices from the main menu'
def handleChoice(choice):
    choice = choice.lower()
    print(f'CHOICE: {choice}')
    
    if choice == "login":
        print("LOGIN SELECTED...")
        bank.login()
        

        
        
    elif choice == "exit": 
        print("LOGOUT SELECTED..." if bank.is_logged_in else "")
        if bank.is_logged_in:
            bank.logout()
        print("Thank You for choosing JST Banking!")
        sys.exit()

        
    elif bank.current_user == None and (choice != "login" or choice != "exit"):
        print("\n------------ Login Required, please login first ------------")
        
    elif choice == "withdraw":
        print("WITHDRAW SELECTED...")
        if bank.isAuthorized('withdraw'):
            w_a = float(input("please enter the amount you want to withdraw: $"))
            bank.current_user.withdraw(w_a)
            bank.t_activity("01", bank.current_user.name, bank.current_user.acc_num, w_a)
        
    elif choice == "transfer":
        print("TRANSFER SELECTED...")
        if bank.isAuthorized('transfer'):
            sucess, amount = bank.transferMoney()
            bank.t_activity("02", bank.current_user.name, bank.current_user.acc_num, amount)
        
            
    elif choice == "paybills":
        print("PAY BILLS SELECTED...")
        if bank.isAuthorized('paybills'):
            p_a= float(input("please enter the amount you want to pay bill to the company: $"))
            bank.current_user.payBills(p_a)
            bank.t_activity("03", bank.current_user.name, bank.current_user.acc_num, p_a)
            
        
    elif choice == "deposit":
        print("DEPOSIT SELECTED...")
        if bank.isAuthorized('deposit'):
            d_a = float(input("Please enter the amount you want to Deposit: $"))
            bank.current_user.deposite(d_a)
            bank.t_activity("04", bank.current_user.name, bank.current_user.acc_num, d_a)
            
        
    elif choice == "create account":
        print("CREATE ACCOUNT SELECTED...")
        if bank.isAuthorized('create'):
           _, balance= bank.createAccount()
           bank.t_activity("05", _.name, _.acc_num, balance)
    
    elif choice == "delete account":
        print("DELETE ACCOUNT SELECTED...")
        if bank.isAuthorized('delete'):
           
            name, num = bank.Delete_Account()
            bank.t_activity("06", name, num, 0)
        
    elif choice == "disable account":
        print("DISABLE ACCOUNT SELECTED...")
        if bank.isAuthorized('disable'):
            name, num = bank.Disable_Account()
            bank.t_activity("07", name, num, 0)

        
    elif choice == "change current plan":
        print("CHANGE PLAN SELECTED...")
        if bank.isAuthorized('changeplan'):
            name,num = bank.change_plan()
            bank.t_activity("08", name, num, 0)
        
    elif choice == "logout":
        print("LOGOUT SELECTED...")
        bank.t_activity("00", bank.current_user.name, bank.current_user.acc_num, 0)
        bank.logout()
       
       
        
    
        
            
    else:
        print("\nInvalid choice! Please try again.\n")
        print("--------------------------------------------------------------------\n")
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