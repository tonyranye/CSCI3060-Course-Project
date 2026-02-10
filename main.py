import time
import os
import sys

from src import *

def welcome():
    print("\n--------------------------------------------------------------------")
    print("Welcome To JST Banking! ")
    print("developed by\n \nJared Efrem\nSumukh  Jagirdar\nTony Akinniranye")
    print("--------------------------------------------------------------------")
    mainMenu()


def mainMenu():
    print("\nWhat would you like  to do today? Select from the options below\n")
    print("1. Login ") 
    print("2. Withdraw")
    print("3. Transfer")
    print("4. Paybills")
    print("5. Deposit")
    print("6. Create Account")
    print("7. Delete Account")
    print("8. Disable Account")
    print("9. Change Current Plan")
    print("10. Logout\n")
    
    print("0. EXIT ")
    
    menuSelection = (input("\nEnter Choice: "))
    
    handleChoice(menuSelection)
    
    return menuSelection

def handleChoice(choice):
    choice = choice.lower()
    if choice ==  "login":
        print("LOGIN SELECTED...")
        
    elif choice ==  "withdraw":
        print("WITHDRAW SELECTED...")
        
    elif choice ==  "transfer":
        print("TRANSFER SELECTED...")
        
    elif choice ==  "pay bills":
        print("PAY BILLS SELECTED...")
        
    elif choice ==  "deposit":
        print("DEPOSIT SELECTED...")
        
    elif choice ==  "create account":
        print("CREATE ACCOUNT SELECTED...")
    
    elif choice ==  "delete account":
        print("DELETE ACCOUNT SELECTED...")
        
    elif choice ==  "disable account":
        print("DISABLE ACCOUNT SELECTED...")
        
    elif choice ==  "change plan":
        print("CHANGE PLAN SELECTED...")
        
    elif choice ==  "logout":
        print("LOGOUT SELECTED...")
            
    elif choice ==  "exit":
        print("Thank You for choosing JST Banking!")
            
    else:
        print("\nInvalid choice! Please try again.\n")
        print("--------------------------------------------------------------------\n")
        time.sleep(1)
        mainMenu()

 
    
    

if __name__ == "__main__":
    welcome()
