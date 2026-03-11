from BankSystem import*
import json
from datetime import datetime
from config import *
# TEST MODE flag



# initializes an Account classes with parameters 
class Account:
    def __init__(self, name, balance, is_admin, payment_plan, is_disabled = None, acc_num=None):
        self.name = name
        self.balance = balance
        self.is_admin = is_admin
        self.acc_num = acc_num
        self.payment_plan = payment_plan
        self.is_disabled = is_disabled
        self.plans = ["SP", "NP"]
    
    '''
    Getters:
    '''
    def getName(self):
        return self.name    
    
    def getBalance(self):
        return self.balance
    
    def getAccNum(self):
        return self.acc_num
    
    def printAccountInfo(self):
        '''
        printAccountInfo, prints the account info for the user to see        

        '''
        normal_print("\n--------------------------------------------------------------------")
        normal_print("ACCOUNT INFORMATION")
        normal_print("--------------------------------------------------------------------")
        normal_print(f"Account Holder: {self.name}")
        normal_print(f"Account Number: {self.acc_num if self.acc_num else 'None'}")
        normal_print(f'Payment Plan: {self.payment_plan}')
        normal_print(f"Current Balance: ${self.balance:.2f}")
        normal_print(f"Admin Privileges: {'Yes' if self.is_admin else 'No'}")  # Changed from self.admin
        normal_print(f"Account status: {'Active' if not self.is_disabled else 'Disabled' } ")
        normal_print("--------------------------------------------------------------------")
    
    
    
   
        
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
            test_print("Error: Cannot transfer to same account")
            normal_print("Error: Cannot transfer to the same account.")
            return False
        
        if amount < 0.0:
            test_print("Error: Cannot transfer negative amounts")
            normal_print("Error: Cannot transfer negative amounts.")
            return False
        
        if self.balance < amount:
            test_print("Error: Insufficient funds")
            normal_print("Error: Insufficient funds to complete transfer.")
            return False
        
        if (to_account.balance + amount) > 99999:
            test_print("Error: Recipient account will exceed limit")
            normal_print("Error: recepiant account will exceed account limit. $99,999")
            return False
            
        
        # Perform transfer
        self.balance -= amount
        to_account.balance += amount
        
        test_print(f"Transfer successful: ${amount:.2f}")
        test_print(f"From: {self.name}")
        test_print(f"To: {to_account.name}")
        test_print(f"New balance: ${self.balance:.2f}")
        
        normal_print(f"\n✓ Transfer successful!")
        normal_print(f"  From: {self.name} (Account #{self.acc_num})")
        normal_print(f"  To: {to_account.name} (Account #{to_account.acc_num})")
        normal_print(f"  Amount: ${amount:.2f}")
        normal_print(f"  New balance for {self.name}: ${self.balance:.2f}")
        
        return True
    
    
    def withdraw(self, w_a):
        '''
        A withdraw function which allows the user to withdraw certain amount 
        Arg:
        w_a: prompting user to select the amount which they want to withdraw
        '''
        normal_print(f"\n{self.name}`s current balance: ${self.balance:.2f}")

        if w_a<0:
            test_print("Error: Withdraw amount cannot be negative")
            normal_print("Withdraw amount can not be negtive")
            return None  # Changed from return
        
        if w_a>500: # withdrawal limit added
            test_print("Error: Amount exceeds withdrawal limit of $500")
            normal_print("You can not draw amount higher than the balance")
            return None

        if self.balance<w_a:  # Fixed logic - removed "and self.balance<0"
            test_print("Error: Insufficient funds")
            normal_print("You can not draw amount higher than the balance")
            return None  # Changed from return
        else:
            self.balance-=w_a
            
        test_print(f"Withdrawal successful: ${w_a:.2f}")
        test_print(f"New balance: ${self.balance:.2f}")
        
        normal_print(f"{self.name}`s current balance after withdrawing: ${self.balance:.2f}")
        return self.balance
    
    def deposit(self, d_a):
        '''
        A deposite function which allows the user to deposite certain amount 
        Arg:
        d_a: prompting user to select the amount which they want to deposite
        '''
        # 1. Check for negative deposit amounts
        if d_a < 0:
            test_print("Error: Deposit amount cannot be negative")
            normal_print("Deposite amount can not be negtive")
            return self.balance

        # 2. Calculate what the new balance would be
        potential_balance = self.balance + d_a

        # 3. Verify that the balance does not exceed $99,999.99
        if potential_balance > 99999.99:
            test_print("Error: Balance cannot exceed $99,999.99")
            normal_print("Error: Account balance can be no more than $99,999.99")
            return self.balance
    
        # 4. If checks pass, update the balance
        self.balance = potential_balance
        
        test_print(f"Deposit successful: ${d_a:.2f}")
        test_print(f"New balance: ${self.balance:.2f}")
        
        normal_print(f"\n{self.name}'s current balance after deposite: ${self.balance:.2f}")
        return self.balance
    

    def payBills(self,amount):

        '''
        A payBills, which allows the user to pay to selected comapnies
        

         amount: User can slect the amount to pay
        '''

        
        company = input().upper()

        valid_companies = ["EC", "CQ", "FI"]

        if company not in valid_companies:
            test_print("Error: Invalid company")
            normal_print("Please enter a valid company")
            return 
        
        
        if amount>self.balance:
            test_print("Error: Insufficient funds")
            normal_print(f"You can not pay more than your current balance to {company} ")
        

        if  amount<0 or amount>2000:
            test_print("Error: Invalid amount (must be $0-$2000)")
            normal_print("Please enter a valid amount between $0 and $2000")
            return 
    
        else:
            self.balance-=amount
            test_print(f"Payment successful: ${amount:.2f} to {company}")
            test_print(f"New balance: ${self.balance:.2f}")
            
            normal_print(f"You have paid ${amount} to the company {company}")
        
        normal_print(f"{self.name}`s current balance {self.balance:.2f} after payment")
        return self.balance
