# MasterAccount.py
# Represents a single bank account record from the Master Bank Accounts File.
# Used by the Back End to load, modify, and save account data.


class MasterAccount:
    """
    Stores all data for a single bank account in the master accounts file.
    
    Fields:
        name               -- account holder's name (max 20 characters)
        acc_num            -- unique 5-digit account number (string)
        status             -- account status, either 'A' (active) or 'D' (disabled)
        balance            -- current account balance in Canadian dollars
        total_transactions -- total number of transactions ever made on this account
        plan               -- payment plan, either 'SP' (student) or 'NP' (non-student)
    """
    def __init__(self, name, acc_num, status, balance, total_transactions, plan):
        self.name = name
        self.acc_num = acc_num
        self.status = status
        self.balance = balance
        self.total_transactions = total_transactions
        self.plan = plan