# TransactionProcessor.py
# Applies each transaction from the merged transaction file to the master accounts list.
# Enforces business constraints and logs errors to the terminal.
# Also calculates and deducts transaction fees based on account plan.

# Transaction fee constants
STUDENT_FEE     = 0.05   # fee per transaction for student plan (SP)
NON_STUDENT_FEE = 0.10   # fee per transaction for non-student plan (NP)


class TransactionProcessor:
    """
    Applies transactions to a list of MasterAccount objects.

    Each apply_* method handles one transaction code and deducts the
    appropriate transaction fee after a successful transaction.

    Methods:
        process_all      -- processes every transaction in the list
        find_account     -- finds an account by account number
        deduct_fee       -- deducts the transaction fee based on account plan
        apply_withdraw   -- applies a withdrawal transaction (code 01)
        apply_transfer   -- applies a transfer transaction (code 02)
        apply_paybill    -- applies a paybill transaction (code 03)
        apply_deposit    -- applies a deposit transaction (code 04)
        apply_create     -- applies an account creation transaction (code 05)
        apply_delete     -- applies an account deletion transaction (code 06)
        apply_disable    -- applies an account disable transaction (code 07)
        apply_changeplan -- applies a payment plan change transaction (code 08)
    """

    def process_all(self, accounts, transactions):
        """
        Iterates through every transaction and calls the appropriate apply method.

        Args:
            accounts     -- list of MasterAccount objects
            transactions -- list of transaction dicts from FileReader
        """
        # Map transaction codes to their handler methods
        handlers = {
            "01": self.apply_withdraw,
            "02": self.apply_transfer,
            "03": self.apply_paybill,
            "04": self.apply_deposit,
            "05": self.apply_create,
            "06": self.apply_delete,
            "07": self.apply_disable,
            "08": self.apply_changeplan,
        }

        for txn in transactions:
            code = txn['code']
            if code in handlers:
                handlers[code](accounts, txn)
            else:
                print(f"ERROR: Unknown transaction code '{code}' for account {txn['acc_num']}")

    def find_account(self, accounts, acc_num):
        """
        Finds and returns a MasterAccount object by account number.
        Returns None if not found.

        Args:
            accounts -- list of MasterAccount objects
            acc_num  -- account number string to search for
        """
        for acc in accounts:
            if acc.acc_num == acc_num:
                return acc
        return None

    def deduct_fee(self, account):
        """
        Deducts the transaction fee from the account balance based on its plan.
        Logs an error if the fee would cause a negative balance.

        Args:
            account -- MasterAccount object to deduct fee from
        """
        fee = STUDENT_FEE if account.plan == "SP" else NON_STUDENT_FEE

        if account.balance - fee < 0:
            print(f"ERROR: Transaction fee of ${fee:.2f} would cause negative balance for account {account.acc_num} ({account.name})")
            return

        account.balance -= fee
        account.balance = round(account.balance, 2)
        account.total_transactions += 1

    def apply_withdraw(self, accounts, txn):
        """
        Applies a withdrawal (code 01) to the account.
        Constraint: balance must not go negative after withdrawal.

        Args:
            accounts -- list of MasterAccount objects
            txn      -- transaction dict with keys: code, name, acc_num, amount
        """
        account = self.find_account(accounts, txn['acc_num'])

        if not account:
            print(f"ERROR: Withdrawal failed - account {txn['acc_num']} not found")
            return

        if account.balance - txn['amount'] < 0:
            print(f"ERROR: Withdrawal of ${txn['amount']:.2f} would cause negative balance for account {txn['acc_num']} ({account.name})")
            return

        account.balance -= txn['amount']
        account.balance = round(account.balance, 2)
        self.deduct_fee(account)

    def apply_transfer(self, accounts, txn):
        """
        Applies a transfer (code 02) from one account to another.
        Constraint: source balance must not go negative after transfer.

        Args:
            accounts -- list of MasterAccount objects
            txn      -- transaction dict with keys: code, name, acc_num, amount
        """
        from_account = self.find_account(accounts, txn['acc_num'])
        to_account   = self.find_account(accounts, txn['misc'])

        if not from_account:
            print(f"ERROR: Transfer failed - source account {txn['acc_num']} not found")
            return

        if not to_account:
            print(f"ERROR: Transfer failed - destination account {txn['misc']} not found")
            return

        if from_account.balance - txn['amount'] < 0:
            print(f"ERROR: Transfer of ${txn['amount']:.2f} would cause negative balance for account {txn['acc_num']} ({from_account.name})")
            return

        from_account.balance -= txn['amount']
        to_account.balance   += txn['amount']
        from_account.balance  = round(from_account.balance, 2)
        to_account.balance    = round(to_account.balance, 2)
        self.deduct_fee(from_account)

    def apply_paybill(self, accounts, txn):
        """
        Applies a bill payment (code 03) to the account.
        Constraint: balance must not go negative after payment.

        Args:
            accounts -- list of MasterAccount objects
            txn      -- transaction dict with keys: code, name, acc_num, amount
        """
        account = self.find_account(accounts, txn['acc_num'])

        if not account:
            print(f"ERROR: Paybill failed - account {txn['acc_num']} not found")
            return

        if account.balance - txn['amount'] < 0:
            print(f"ERROR: Paybill of ${txn['amount']:.2f} would cause negative balance for account {txn['acc_num']} ({account.name})")
            return

        account.balance -= txn['amount']
        account.balance = round(account.balance, 2)
        self.deduct_fee(account)

    def apply_deposit(self, accounts, txn):
        """
        Applies a deposit (code 04) to the account.

        Args:
            accounts -- list of MasterAccount objects
            txn      -- transaction dict with keys: code, name, acc_num, amount
        """
        account = self.find_account(accounts, txn['acc_num'])

        if not account:
            print(f"ERROR: Deposit failed - account {txn['acc_num']} not found")
            return

        account.balance += txn['amount']
        account.balance = round(account.balance, 2)
        self.deduct_fee(account)

    def apply_create(self, accounts, txn):
        """
        Applies an account creation (code 05) by adding a new MasterAccount to the list.
        Constraint: new account number must be unique.

        Args:
            accounts -- list of MasterAccount objects
            txn      -- transaction dict with keys: code, name, acc_num, amount
        """
        from backend.MasterAccount import MasterAccount

        # Check for duplicate account number
        if self.find_account(accounts, txn['acc_num']):
            print(f"ERROR: Create failed - account number {txn['acc_num']} already exists")
            return

        new_account = MasterAccount(
            name               = txn['name'],
            acc_num            = txn['acc_num'],
            status             = 'A',
            balance            = txn['amount'],
            total_transactions = 0,
            plan               = 'NP'
        )
        accounts.append(new_account)

    def apply_delete(self, accounts, txn):
        """
        Applies an account deletion (code 06) by removing the account from the list.

        Args:
            accounts -- list of MasterAccount objects
            txn      -- transaction dict with keys: code, name, acc_num, amount
        """
        account = self.find_account(accounts, txn['acc_num'])

        if not account:
            print(f"ERROR: Delete failed - account {txn['acc_num']} not found")
            return

        accounts.remove(account)

    def apply_disable(self, accounts, txn):
        """
        Applies an account disable (code 07) by setting account status to 'D'.

        Args:
            accounts -- list of MasterAccount objects
            txn      -- transaction dict with keys: code, name, acc_num, amount
        """
        account = self.find_account(accounts, txn['acc_num'])

        if not account:
            print(f"ERROR: Disable failed - account {txn['acc_num']} not found")
            return

        account.status = 'D'

    def apply_changeplan(self, accounts, txn):
        """
        Applies a payment plan change (code 08) by toggling between SP and NP.

        Args:
            accounts -- list of MasterAccount objects
            txn      -- transaction dict with keys: code, name, acc_num, amount
        """
        account = self.find_account(accounts, txn['acc_num'])

        if not account:
            print(f"ERROR: Change plan failed - account {txn['acc_num']} not found")
            return

        account.plan = 'NP' if account.plan == 'SP' else 'SP'