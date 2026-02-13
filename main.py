import time
import os
import sys
from BankSystem import BankSystem, loadAllAccountsFromFile
from Account import *
from src.account_modification import *
from src.transactions import *
from src.account_modification.deleteAccount import *

# LOAD ALL ACCOUNTS AT STARTUP
loadAllAccountsFromFile()


# global bank instance
bank = BankSystem()

def welcome():
    print("\n--------------------------------------------------------------------")
    print("Welcome To JST Banking! ")
    print("developed by\n \nJared Efrem\nSumukh  Jagirdar\nTony Akinniranye")
    print("--------------------------------------------------------------------")
    mainMenu()

def mainMenu():
    print("\nWhat would you like to do today? Select from the options below\n")
    print("1. Login") 
    print("2. Withdraw")
    print("3. Transfer")
    print("4. Paybills")
    print("5. Deposit")
    print("6. Create Account")
    print("7. Delete Account")
    print("8. Disable Account")
    print("9. Change Current Plan")
    print("10. Logout\n")
    print("11. EXIT")
    
    menuSelection = (input("\nEnter Choice: "))
    handleChoice(menuSelection)
    return menuSelection

def handleChoice(choice):
    choice = choice.lower()
    
    if choice == "login":
        print("LOGIN SELECTED...")
        bank.login()
        
    elif bank.current_user == None and choice != "login":
        print("\n------------ Login Required, please login first ------------")
        
    elif choice == "withdraw":
        print("WITHDRAW SELECTED...")
        if bank.isAuthorized('withdraw'):
            w_a = float(input("please enter the amount you want to withdraw:"))
          
            bank.current_user.withdraw(w_a)
            
     
        
    elif choice == "transfer":
        print("TRANSFER SELECTED...")
        # if bank.isAuthorized('transfer'):
        #     transfer()
            
    elif choice == "paybills":
        print("PAY BILLS SELECTED...")
        if bank.isAuthorized('paybills'):
            p_a= float(input("please enter the amount you want to pay bill to the company:"))

            bank.current_user.payBills(p_a)
        
    elif choice == "deposit":
        print("DEPOSIT SELECTED...")
        if bank.isAuthorized('deposit'):
            d_a = float(input("please enter the amount you want to Deposit:"))
          
            bank.current_user.deposite(d_a)
        
    elif choice == "create account":
        print("CREATE ACCOUNT SELECTED...")
        if bank.isAuthorized('create'):
            bank.createAccount()
    
    elif choice == "delete account":
        print("DELETE ACCOUNT SELECTED...")
        if bank.isAuthorized('delete'):
            bank.Delete_Account()
        
    elif choice == "disable account":
        print("DISABLE ACCOUNT SELECTED...")
        # if bank.isAuthorized('disable'):
        #     disableAccount()
        
    elif choice == "change plan":
        print("CHANGE PLAN SELECTED...")
        # if bank.isAuthorized('changeplan'):
        #     changePlan()
        
    elif choice == "logout":
        print("LOGOUT SELECTED...")
        bank.logout()
        
    elif choice == "exit":
        if bank.is_logged_in:
            bank.logout()
        print("Thank You for choosing JST Banking!")
        sys.exit()  # Actually exit the program
            
    else:
        print("\nInvalid choice! Please try again.\n")
        print("--------------------------------------------------------------------\n")
        time.sleep(1)
    
    # Return to menu after each transaction
    mainMenu()

if __name__ == "__main__":
    welcome()