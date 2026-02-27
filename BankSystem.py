import json
from Account import Account
import time
from datetime import datetime


# GLOBAL variable - holds all accounts loaded from JSON
all_accounts = []

# TEST MODE flag
TEST_MODE = True

def test_print(*args, **kwargs):
    """Print only in test mode"""
    if TEST_MODE:
        print(*args, **kwargs)

def normal_print(*args, **kwargs):
    """Print only in normal mode"""
    if not TEST_MODE:
        print(*args, **kwargs)


class BankSystem:
    def __init__(self, transaction_path="t_data.txt"):
        self.current_user = None
        self.session_type = None
        self.is_logged_in = False
        self.s_trans = []
        self.transaction_path = transaction_path
     
     
    # function call for when user selects  login option   
    def login(self):
        if self.is_logged_in:
            test_print("Error: Already logged in")
            normal_print("Error: Already logged in. Please Logout first.")
            return False
            
        normal_print("\n--- LOGIN ---")
        normal_print("Select session type: ")
        normal_print("Standard (Account Holder)")
        normal_print("Admin (Bank Employee)")
        
        
        
        choice = input().strip().lower()
        
        if choice == "standard":
            self.session_type = "standard"
            name = input().strip()
            
            # Search for account in global list
            for acc in all_accounts:
                if acc.name.lower() == name.lower():
                    
                    # if the entered account is disabled, print a error message
                    if acc.is_disabled:
                        test_print("Error: Account disabled")
                        normal_print("\nError: This account has been disabled")
                        return False
                    
                    self.current_user = acc
                    self.is_logged_in = True
                    test_print(f"User Logged")
                    test_print(f"Standard Mode")
                    test_print(f"Welcome {name}!")
                    normal_print(f'Welcome {name}!')
                    self.current_user.printAccountInfo()
                    return True
            
            test_print("Error: Account not found")
            normal_print("\nError: Account not found.")
            return False
        
        # if they entered admin login
        elif choice == "admin":
            self.session_type = "admin"
            self.current_user = "admin"  # Admin has no specific account
            self.is_logged_in = True
            test_print("User Logged")
            test_print("Admin Mode")
            normal_print("\nAdmin Mode Enabled!")
            normal_print(f"Total accounts in system: {len(all_accounts)}")
            return True
        
        else:
            test_print("Error: Invalid session type")
            normal_print('Invalid session type. Please enter "standard" or "admin"')
            return False
     
    # function to log the current user out of the banking system        
    def logout(self):
        
        if not self.is_logged_in:
            test_print("Error: Not logged in")
            normal_print("Error: Not currently logged in.")
            return False
        
        self.writeFile()
        test_print("Logout successful")
        normal_print(f'\nLogging out {self.session_type} session...')
        self.current_user = None
        self.session_type = None
        self.is_logged_in = False
        normal_print("Logout successful!")
        return True
    
    
    # function to create a new account, make name, account, num, starign balance...            
    def createAccount(self):
        normal_print("\n--- CREATE NEW ACCOUNT ---")
        
        while True:
            name = input()
            if len(name) <= 20:
                break
            else:
                test_print("Error: Name too long (max 20 chars)")
                normal_print("Error: The length of the name is too long (max 20 chars)")
                
            
        try:
            balance = float(input())
            
        except ValueError:
            test_print("Error: Invalid amount, balance set to $0.00")
            normal_print("Invalid amount. Setting balance to $0.00")
            balance = 0.0
        
        # Generate unique account number
        acc_num = self.generateUniqueAccountNumber()
        
        
        # Create new account object
        new_account = Account(name, balance, False, "NP", False, acc_num)
        
        # Add to global list
        all_accounts.append(new_account)
        
        # Save to file
        self.saveAllAccounts()
        
        test_print(f"Account created: {name}")
        test_print(f"Account Number: {acc_num}")
        test_print(f"Balance: ${balance:.2f}")
        
        normal_print("\nAccount created successfully!")
        new_account.printAccountInfo()
        return new_account, balance


    # function to remove a accout from the system
    def Delete_Account(self):
        normal_print("\n--- DELETE ACCOUNT ---")
        name = input()
        acc_num = input()
        Match = False
        
        
        # searches through all acounts to look for the name the user entered in the json file
        for i, acc in enumerate(all_accounts):
            if acc.name.lower() == name.lower() and acc.acc_num == acc_num:
                # if found, its removed form the all_accounts global variable
                all_accounts.pop(i)
                Match = True
        if not Match:
            test_print("Error: Account not found")
            normal_print("Error: Account not found or name and account number do not match.")
        else:
            test_print(f"Account deleted: {name}")
            test_print(f"Account Number: {acc_num}")
            normal_print("\nAccount deleted")
            normal_print("\nAccounts remaining in system: " + str(len(all_accounts)))
            normal_print("\nTransaction code: ")
            normal_print("06 " + name + " " + acc_num)
        time.sleep(3)
        
        return name, acc_num
    
    
    # function that disables a customer account, stops them from being able to perform any transactions
    def Disable_Account(self):
        normal_print("\n--- DISABLE/RE-ENABLE ACCOUNT ---")
        name = input()
        acc_num = input()
        found_match = False
        is_disabled_check = False
        
        # searches throuhg list for the name and account number the user entered
        for i, acc in enumerate(all_accounts):
            if acc.name.lower() == name.lower() and acc.acc_num == acc_num:
                # if found and belong to the same person, the account is set to disabled
                if acc.is_disabled:
                    acc.is_disabled = False
                    test_print(f"Account enabled: {name}")
                else:
                    acc.is_disabled = True
                    is_disabled_check = True
                    test_print(f"Account disabled: {name}")
                    
                test_print(f"Account Number: {acc_num}")
                found_match = True

        if not found_match:
            test_print("Error: Account not found")
            normal_print("Error: Account not found or name and account number do not match.")
        else:
            if is_disabled_check:
                normal_print(f'{name} account {acc_num} disabled.')
            else:
                normal_print(f'{name} account {acc_num} enabled.')
            
            return name, acc_num
        time.sleep(2)
        
        
    # function that changes the payment plan type of a account between Student plan (SP) and Non-student (NP)
    def change_plan (self):
        normal_print("\n--- CHANGE ACCOUNT PAYMENT PLAN ---")
        name = input()
        acc_num = input()
        found_match = False
        new_plan = ""
        
        # searches though all acounts to find the one the user entered and changes it accordingly
        for i, acc in enumerate(all_accounts):
            if acc.name.lower() == name.lower() and acc.acc_num == acc_num:
                found_match = True
                if acc.payment_plan == "SP":
                    acc.payment_plan = "NP"
                else:
                    acc.payment_plan = "SP"
                new_plan = acc.payment_plan
        if not found_match:
            test_print("Error: Account not found")
            normal_print("Error: Account not found or name and account number do not match.")
        else:
            test_print(f"Plan changed: {name}")
            test_print(f"Account Number: {acc_num}")
            test_print(f"New Plan: {new_plan}")
            normal_print(f'{name} Account plan is changed to {new_plan}.')
            return name, acc_num
    
    # generates a unique account number    
    def generateUniqueAccountNumber(self):
        """Generate unique account number by finding max existing number"""
        
        # if the list is empty, assign 10000 as the acconut number 
        if not all_accounts:
            return "10000"
        
        # Find highest account number
        max_num = 9999
        for acc in all_accounts:
            if acc.acc_num:
                max_num = max(max_num, int(acc.acc_num))
        
        return str(max_num + 1)
    
    
    # Save all accounts from global list to JSON file
    def saveAllAccounts(self):
        """Save all accounts from global list to JSON file"""
        with open("accounts/accounts_valid.json", "w") as file:
            account_data = []
            # for every account in all_accounts, ovveride the json file with the new data
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
            normal_print("Accounts saved successfully")
    
    
    # function that determins if the current active user is allowed to use certain functions
    def isAuthorized(self, transaction_type):
        if not self.is_logged_in:
            test_print("Error: Must login first")
            normal_print("Error: Must login first.")
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
                test_print("Error: Do not have permissions to " + transaction_type.replace('create', 'create an account'))
                normal_print("Error: Admin privileges required for this transaction.")
                return False
        
        return False
    
    # funtion to transfer money from one customers account to another
    def transferMoney(self):
        from BankSystem import all_accounts  # Import the global list
        
        # Admin can transfer from any account, standard user only from their own
        if self.session_type == "admin":
            acc_name_from = input()
            
            # Find the account to transfer from
            from_account = None
            for acc in all_accounts:
                if acc.name.lower() == acc_name_from.lower():
                    from_account = acc
                    break
            
            if not from_account:
                test_print("Error: Source account not found")
                normal_print("Error: Source account not found.")
                return False, 0
        else:
            from_account = self.current_user
        
        acc_to = input()
        
        # Find destination account
        to_account = None
        for acc in all_accounts:
            if acc.acc_num == acc_to:
                to_account = acc
                break
        
        if not to_account:
            test_print("Error: Destination account not found")
            normal_print("Error: Destination account could not be found.")
            return False, 0
        
        try:
            amount = float(input())
            
            # Use the Account's transferTo method
            success = from_account.transferTo(to_account, amount)
            
            if success:
                # Save changes to file
                self.saveAllAccounts()
            
            return success, amount
        
        except ValueError:
            test_print("Error: Invalid amount")
            normal_print("Error: Invalid amount entered. Please enter a number.")
            return False, 0
        
    def withdraw(self):
        """
        Withdraw money from an account.
        Admin can withdraw from any account, standard user only from their own.
        
        Returns:
            tuple: (success, account_object, amount)
        """
        # Admin can withdraw from any account, standard user only from their own
        if self.session_type == "admin":
            acc_num = input().strip()
            
            # Find the account to withdraw from
            target_account = None
            for acc in all_accounts:
                if acc.acc_num == acc_num:
                    target_account = acc
                    break
            
            if not target_account:
                test_print("Error: Account not found")
                normal_print("Error: Account not found.")
                return False, None, 0
                
            # Check if account is disabled
            if target_account.is_disabled:
                test_print("Error: Account is disabled")
                normal_print("Error: This account is disabled and cannot perform transactions.")
                return False, None, 0
        else:
            target_account = self.current_user
        
        try:
            amount = float(input())
            
            # Use the Account's withdraw method
            result = target_account.withdraw(amount)
            
            if result is not None:  # Successful withdrawal
                # Save changes to file
                self.saveAllAccounts()
                return True, target_account, amount
            else:
                return False, target_account, 0
        
        except ValueError:
            test_print("Error: Invalid amount")
            normal_print("Error: Invalid amount entered. Please enter a number.")
            return False, None, 0
    
    def depositMoney(self):
        """
        Deposit money to an account.
        Admin can deposit to any account by account number, standard user only to their own.
        
        Returns:
            tuple: (success, account_object, amount)
        """
        # Admin can deposit to any account, standard user only to their own
        if self.session_type == "admin":
            acc_num = input().strip()
            
            # Find the account to deposit to
            target_account = None
            for acc in all_accounts:
                if acc.acc_num == acc_num:
                    target_account = acc
                    break
            
            if not target_account:
                test_print("Error: Account not found")
                normal_print("Error: Account not found.")
                return False, None, 0
                
            # Check if account is disabled
            if target_account.is_disabled:
                test_print("Error: Account is disabled")
                normal_print("Error: This account is disabled and cannot perform transactions.")
                return False, None, 0
        else:
            target_account = self.current_user
        
        try:
            amount = float(input())
            
            # Use the Account's deposit method
            result = target_account.deposit(amount)
            
            if result is not None:  # Successful deposit
                # Save changes to file
                self.saveAllAccounts()
                return True, target_account, amount
            else:
                return False, target_account, 0
        
        except ValueError:
            test_print("Error: Invalid amount")
            normal_print("Error: Invalid amount entered. Please enter a number.")
            return False, None, 0
    
    # Tracks the current activity for each transaction and function
    def t_activity(self, t_type, name, acc_num, cur_am, m="  "):

        m_name = name[:20].ljust(20)
        m_acc = str(acc_num)[:5].rjust(5)

        m_am = f"{cur_am:08.2f}"
        m_m = str(m)[:2].rjust(2)

        frmt= f"{t_type} {m_name} {m_acc} {m_am} {m_m}"


        self.s_trans.append(frmt)

    
    # Writes the file to t_data.txt
    
    def writeFile(self):

        with open(self.transaction_path,'a') as f:
            for txn in self.s_trans:
                    f.write(txn + "\n")
        self.s_trans = []


# GLOBAL FUNCTION - Call this once at program startup
def loadAllAccountsFromFile(accounts_file="accounts/accounts_valid.json"):
    """Load all accounts from JSON file into global all_accounts list"""
    global all_accounts
    
    try:
        with open(accounts_file, "r") as file:
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
            
            normal_print(f" Loaded {len(all_accounts)} account(s) from file")
            
    except FileNotFoundError:
        normal_print(" No accounts file found. Starting with empty account list.")
        all_accounts = []