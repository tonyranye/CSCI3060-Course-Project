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
    match choice:
        case "1":
            print("LOGIN SELECTED...")
            
        case "2":
            print("WITHDRAW SELECTED...")
            
        case "3":
            print("TRANSFER SELECTED...")
            
        case "4":
            print("PAY BILLS SELECTED...")
            
        case "5":
            print("DEPOSIT SELECTED...")
            
        case "6":
            print("CREATE ACCOUNT SELECTED...")
        
        case "7":
            print("DELETE ACCOUNT SELECTED...")
            
        case "8":
            print("DISABLE ACCOUNT SELECTED...")
            
        case "9":
            print("CHANGE PLAN SELECTED...")
            
        case "10":
            print("LOGOUT SELECTED...")
            
        case "0":
            print("Thank You for choosing JST Banking!")
            
        case _:
            print("\nInvalid choice! Please try again.\n")
            print("--------------------------------------------------------------------\n")
            (1)
            mainMenu()

 
    
    

if __name__ == "__main__":
    welcome()
