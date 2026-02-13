from BankSystem import*
import json
from datetime import datetime

class Account:
    def __init__(self, name, balance, is_admin, payment_plan, is_disabled = None, acc_num=None):
        self.name = name
        self.balance = balance
        self.is_admin = is_admin
        self.acc_num = acc_num
        self.payment_plan = payment_plan
        self.is_disabled = is_disabled
        self.plans = ["SP", "NP"]
        
    def getName(self):
        return self.name    
    
    def getBalance(self):
        return self.balance
    
    def getAccNum(self):
        return self.acc_num
    
    def printAccountInfo(self):
        print("\n--------------------------------------------------------------------")
        print("ACCOUNT INFORMATION")
        print("--------------------------------------------------------------------")
        print(f"Account Holder: {self.name}")
        print(f"Account Number: {self.acc_num if self.acc_num else 'None'}")
        print(f'Payment Plan: {self.payment_plan}')
        print(f"Current Balance: ${self.balance:.2f}")
        print(f"Admin Privileges: {'Yes' if self.is_admin else 'No'}")  # Changed from self.admin
        print(f"Account status: {'Active' if not self.is_disabled else 'Disabled' } ")
        print("--------------------------------------------------------------------")
    
    
    

        
    def transferTo(self, to_account, amount):
        """
        Transfer money from this account to another account.
        
        Args:
            to_account: The Account object to transfer money to
            amount: The amount to transfer
            
        Returns:
            bool: True if transfer successful, False otherwise
        """
        # Validation checks
        if self == to_account:
            print("Error: Cannot transfer to the same account.")
            return False
        
        if amount < 0.0:
            print("Error: Cannot transfer negative amounts.")
            return False
        
        if self.balance < amount:
            print("Error: Insufficient funds to complete transfer.")
            return False
        
        # Perform transfer
        self.balance -= amount
        to_account.balance += amount
        
        print(f"\n✓ Transfer successful!")
        print(f"  From: {self.name} (Account #{self.acc_num})")
        print(f"  To: {to_account.name} (Account #{to_account.acc_num})")
        print(f"  Amount: ${amount:.2f}")
        print(f"  New balance for {self.name}: ${self.balance:.2f}")
        
        return True
    
    
    def withdraw(self, w_a):
        print(f"{self.name}`s current balance: {self.balance}")


        if w_a<0:
            print("Withdraw amount can not be negtive")
            return


        if self.balance<w_a and self.balance<0:
            print("You can not draw amount higher than the balance")
            return 
        else:
            self.balance-=w_a
        print(f"{self.name}`s current balance after withdrawing: ${self.balance:.2f}")
        return self.balance
    
    def deposite(self, d_a):
        if d_a<0:
            print("Deposite amount can not be negtive")
            return
        if self.balance>5000:
            print("Your balance is already more than $5000")
            return 
        else:
            self.balance+=d_a
        print(f"{self.name}`s current balance after deposite: ${self.balance:.2f}")
        return self.balance
    

    def payBills(self,amount):

        
        company = input("Enter company (EC / CQ / FI): ").upper()

        valid_companies = ["EC", "CQ", "FI"]

        if company not in valid_companies:
            print("Please enter a valid company")
            return 
        
        
        if amount>self.balance:
            print(f"You can not pay more than your current balance to {company} ")
        

        if  amount<0 or amount>2000:
            print("Please enter a valid amount between $0 and $2000")
            return 
    
        else:
            self.balance-=amount
            print(f"You have paid ${amount} to the company {company}")
        
        print(f"{self.name}`s current balance {self.balance:.2f} after payment")
        return self.balance


        

      