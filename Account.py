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