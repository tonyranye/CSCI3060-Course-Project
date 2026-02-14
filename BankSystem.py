import json
from Account import Account
import time
from datetime import datetime


# GLOBAL variable - holds all accounts loaded from JSON
all_accounts = []




class BankSystem:
    def __init__(self):
        self.current_user = None
        self.session_type = None
        self.is_logged_in = False
        self.s_trans = []
        
    def login(self):
        if self.is_logged_in:
            print("Error: Already logged in. Please Logout first.")
            
            return False
        print("\n--- LOGIN ---")
        print("Select session type: ")
        print("Standard (Account Holder)")
        print("Admin (Bank Employee)")
        
        
        
        choice = input("Enter session type: ").lower()
        
        if choice == "standard":
            self.session_type = "standard"
            name = input("Enter account holder name: ")
            
            # Search for account in global list
            for acc in all_accounts:
                if acc.name.lower() == name.lower():
                    if acc.is_disabled:
                        print("\nError: This account has been disabled")
                        
                        return False
                    
                    self.current_user = acc
                    self.is_logged_in = True
                    print(f'Welcome {name}!')
                    self.current_user.printAccountInfo()
                    # print(self.current_user)
                    return True
            
            print("\nError: Account not found.")
            return False
        
        elif choice == "admin":
            self.session_type = "admin"
            self.current_user = "admin"  # Admin has no specific account
            self.is_logged_in = True
            print("\nAdmin Mode Enabled!")
            print(f"Total accounts in system: {len(all_accounts)}")
            return True
        
        else:
            print('Invalid session type. Please enter "standard" or "admin"')
            return False
            
    def logout(self):
        
        if not self.is_logged_in:
            print("Error: Not currently logged in.")
            return False
        
        self.writeFile()
        print(f'\nLogging out {self.session_type} session...')
        self.current_user = None
        self.session_type = None
        self.is_logged_in = False
        print("Logout successful!")
        return True
            
    def createAccount(self):
        print("\n--- CREATE NEW ACCOUNT ---")
        name = input("Enter account holder name: ")
        balance = float(input("Enter initial deposit: $"))
        
        # Generate unique account number
        acc_num = self.generateUniqueAccountNumber()
        
        
        # Create new account object
        new_account = Account(name, balance, False, "NP", False, acc_num)
        
        # Add to global list
        all_accounts.append(new_account)
        
        # Save to file
        self.saveAllAccounts()
        
        print("\nAccount created successfully!")
        new_account.printAccountInfo()
        return new_account, balance


    def Delete_Account(self):
        print("\n--- DELETE ACCOUNT ---")
        name = input("Enter the account holder name:")
        acc_num = input("Enter the account number:")
        Match = False

        for i, acc in enumerate(all_accounts):
            if acc.name.lower() == name.lower() and acc.acc_num == acc_num:
                all_accounts.pop(i)
                Match = True
        if not Match:
            print("Error: Account not found or name and account number do not match.")
        else:
            print("\nAccount deleted")
            print("\nAccounts remaining in system: " + str(len(all_accounts)))
            print("\nTransaction code: ")
            print("06 " + name + " " + acc_num)
        time.sleep(3)
        
        return name, acc_num

    def Disable_Account(self):
        print("\n--- DISABLE/RE-ENABLE ACCOUNT ---")
        name = input("Enter the account holder name:")
        acc_num = input("Enter the account number:")
        found_match = False
        is_disabled_check = False

        for i, acc in enumerate(all_accounts):
            if acc.name.lower() == name.lower() and acc.acc_num == acc_num:
                if acc.is_disabled:
                    acc.is_disabled = False
                else:
                    acc.is_disabled = True
                    is_disabled_check = True
                found_match = True

        if not found_match:
            print("Error: Account not found or name and account number do not match.")
        else:
            if is_disabled_check:
                print(f'{name} account {acc_num} disabled.')
            else:
                print(f'{name} account {acc_num} enabled.')
            
            return name, acc_num
        time.sleep(2)
        
        

    def change_plan (self):
        print("\n--- CHANGE ACCOUNT PAYMENT PLAN ---")
        name = input("Enter the account holder name:")
        acc_num = input("Enter the account number:")
        found_match = False
        new_plan = ""
        for i, acc in enumerate(all_accounts):
            if acc.name.lower() == name.lower() and acc.acc_num == acc_num:
                found_match = True
                if acc.payment_plan == "SP":
                    acc.payment_plan = "NP"
                else:
                    acc.payment_plan = "SP"
                new_plan = acc.payment_plan
        if not found_match:
            print("Error: Account not found or name and account number do not match.")
        else:
            print(f'{name} Account plan is changed to {new_plan}.')
            return name, acc_num
        
    def generateUniqueAccountNumber(self):
        """Generate unique account number by finding max existing number"""
        if not all_accounts:
            return "10000"
        
        # Find highest account number
        max_num = 9999
        for acc in all_accounts:
            if acc.acc_num:
                max_num = max(max_num, int(acc.acc_num))
        
        return str(max_num + 1)
    
    def saveAllAccounts(self):
        """Save all accounts from global list to JSON file"""
        with open("accounts/accounts_valid.json", "w") as file:
            account_data = []
            for acc in all_accounts:
                account_data.append({
                    'name': acc.name,
                    'acc_num': acc.acc_num,
                    'balance': acc.balance,
                    'payment plan': acc.payment_plan,
                    'is_disabled': acc.is_disabled,
                    'is_admin': acc.is_admin
                })
                
            json.dump(account_data, file, indent=4)
            print("Accounts saved successfully")
    
    def isAuthorized(self, transaction_type):
        if not self.is_logged_in:
            print("Error: Must login first.")
            return False
        
        # Unprivileged transactions (standard users can do)
        unprivileged = ['withdraw', 'deposit', 'transfer', 'paybills']
        
        # Privileged transactions (only admin can do)
        privileged = ['create', 'delete', 'disable', 'changeplan']
        
        if transaction_type in unprivileged:
            return True  # Both admin and standard can do these
        
        if transaction_type in privileged:
            if self.session_type == 'admin':
                return True
            else:
                print("Error: Admin privileges required for this transaction.")
                return False
        
        return False
    
    def transferMoney(self):
        from BankSystem import all_accounts  # Import the global list
        
        # Admin can transfer from any account, standard user only from their own
        if self.session_type == "admin":
            acc_name_from = input("Enter account holder name to transfer FROM: ")
            
            # Find the account to transfer from
            from_account = None
            for acc in all_accounts:
                if acc.name.lower() == acc_name_from.lower():
                    from_account = acc
                    break
            
            if not from_account:
                print("Error: Source account not found.")
                return False
        else:
            from_account = self.current_user
        
        acc_to = input("Enter account number to send money TO: ")
        
        # Find destination account
        to_account = None
        for acc in all_accounts:
            if acc.acc_num == acc_to:
                to_account = acc
                break
        
        if not to_account:
            print("Error: Destination account could not be found.")
            return False
        
        try:
            amount = float(input("Enter transfer amount: $"))
            
            # Use the Account's transferTo method
            success = from_account.transferTo(to_account, amount)
            
            if success:
                # Save changes to file
                self.saveAllAccounts()
            
            return success, amount
        
        except ValueError:
            print("Error: Invalid amount entered. Please enter a number.")
            return False
    def t_activity(self, t_type, name, acc_num, cur_am, m="  "):

        m_name = name[:20].ljust(20)
        m_acc = str(acc_num)[:5].rjust(5)

        m_am = f"{cur_am:08.2f}"
        m_m = str(m)[:2].rjust(2)

        frmt= f"{t_type} {m_name} {m_acc} {m_am} {m_m}"


        self.s_trans.append(frmt)

        print(f"Format length:{len(frmt)}")
    
    def writeFile(self):

        with open("t_data.txt",'a') as f:
            for txn in self.s_trans:
                    f.write(txn + "\n")
        self.s_trans = []


# GLOBAL FUNCTION - Call this once at program startup
def loadAllAccountsFromFile():
    """Load all accounts from JSON file into global all_accounts list"""
    global all_accounts
    
    try:
        with open("accounts/accounts_valid.json", "r") as file:
            data = json.load(file)
            all_accounts = []
            
            for acc_dict in data:
                # Handle both 'is_admin' and 'admin' keys for backward compatibility
                is_admin = acc_dict.get('is_admin', acc_dict.get('admin', False))
                
                is_disabled = acc_dict.get("is_disabled", acc_dict.get("is_disabled", False))
                
                account = Account(
                    acc_dict['name'],
                    acc_dict['balance'],
                    is_admin,
                    acc_dict.get('payment_plan','SP'),
                    is_disabled,
                    acc_dict.get('acc_num'),
                    
                    
                )
                all_accounts.append(account)
            
            print(f" Loaded {len(all_accounts)} account(s) from file")
            
    except FileNotFoundError:
        print(" No accounts file found. Starting with empty account list.")
        all_accounts = []

