class Account:
    def __init__(self, name, balance, is_admin, acc_num=None):
        self.name = name
        self.balance = balance
        self.is_admin = is_admin
        self.acc_num = acc_num
        
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
        print(f"Current Balance: ${self.balance:.2f}")
        print(f"Admin Privileges: {'Yes' if self.is_admin else 'No'}")  # Changed from self.admin
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