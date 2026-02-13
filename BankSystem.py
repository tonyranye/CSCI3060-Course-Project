import json
from Account import *

# GLOBAL variable - holds all accounts loaded from JSON
all_accounts = []

class BankSystem:
    def __init__(self):
        self.current_user = None
        self.session_type = None
        self.is_logged_in = False
        
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
                    self.current_user = acc
                    self.is_logged_in = True
                    print(f'Welcome {name}!')
                    self.current_user.printAccountInfo()
                    print(self.current_user)
                    return True
            
            print("Error: Account not found.")
            return False
        
        elif choice == "admin":
            self.session_type = "admin"
            self.current_user = "admin"  # Admin has no specific account
            self.is_logged_in = True
            print("Admin Mode Enabled!")
            print(f"Total accounts in system: {len(all_accounts)}")
            return True
        
        else:
            print('Invalid session type. Please enter "standard" or "admin"')
            return False
            
    def logout(self):
        if not self.is_logged_in:
            print("Error: Not currently logged in.")
            return False
        
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
        
        admin_choice = input("Is this an admin account? (yes/no): ").lower()
        is_admin = admin_choice == "yes"
        
        # Create new account object
        new_account = Account(name, balance, is_admin, acc_num)
        
        # Add to global list
        all_accounts.append(new_account)
        
        # Save to file
        self.saveAllAccounts()
        
        print("\nAccount created successfully!")
        new_account.printAccountInfo()
        return new_account
        
    def generateUniqueAccountNumber(self):
        """Generate unique account number by finding max existing number"""
        if not all_accounts:
            return "1000"
        
        # Find highest account number
        max_num = 999
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
                
                account = Account(
                    acc_dict['name'],
                    acc_dict['balance'],
                    is_admin,
                    acc_dict.get('acc_num')
                )
                all_accounts.append(account)
            
            print(f" Loaded {len(all_accounts)} account(s) from file")
            
    except FileNotFoundError:
        print(" No accounts file found. Starting with empty account list.")
        all_accounts = []