class Account:
    def __init__(self, name, balance, is_admin, acc_num=None):
        self.name = name
        self.balance = balance
        self.is_admin = is_admin
        self.acc_num = acc_num
  
        
    def printAccountInfo(self):
        print("\n--------------------------------------------------------------------")
        print("ACCOUNT INFORMATION")
        print("--------------------------------------------------------------------")
        print(f"Account Holder: {self.name}")
        print(f"Account Number: {self.acc_num if self.acc_num else 'None'}")
        print(f"Current Balance: ${self.balance:.2f}")
        print(f"Admin Privileges: {'Yes' if self.is_admin else 'No'}")  # Changed from self.admin
        print("--------------------------------------------------------------------")

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
        print(f"{self.name}`s current balance after withdrawing: {self.balance}")
        return self.balance
    def deposite(self, d_a):
        if d_a<0:
            print("Deposite amount can not be negtive")
            return
        if self.balance>5000:
            print("Your balance is already more than 5000")
            return 
        else:
            self.balance+=d_a
        print(f"{self.name}`s current balance after deposite: {self.balance}")
        return self.balance

      