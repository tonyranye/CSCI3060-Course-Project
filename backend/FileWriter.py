# FileWriter.py
# Responsible for writing the updated accounts data to both the
# New Master Bank Accounts File and the New Current Bank Accounts File.

import json


class FileWriter:
    """
    Writes output files for the Back End after all transactions are processed.

    Methods:
        write_master_accounts  -- writes the updated master accounts file (fixed-width .txt)
        write_current_accounts -- writes the updated current accounts file (JSON)
    """

    def write_master_accounts(self, accounts, file_path):
        """
        Writes all accounts to the Master Bank Accounts File in fixed-width format.
        Format per line (42 chars): NNNNN AAAAAAAAAAAAAAAAAAAA S PPPPPPPP TTTT
        Accounts are sorted in ascending order by account number.
        Ends with an END_OF_FILE marker line.

        Args:
            accounts  -- list of MasterAccount objects
            file_path -- path to write the master accounts file
        """
        # Sort accounts in ascending order by account number
        sorted_accounts = sorted(accounts, key=lambda acc: int(acc.acc_num))

        with open(file_path, 'w') as f:
            for acc in sorted_accounts:
                acc_num = acc.acc_num.zfill(5)
                name    = acc.name.ljust(20)[:20]
                status  = acc.status
                balance = f"{acc.balance:08.2f}"
                total_t = str(acc.total_transactions).zfill(4)

                line = f"{acc_num} {name} {status} {balance} {total_t}"
                f.write(line + "\n")

            # Write END_OF_FILE marker
            f.write("00000 END_OF_FILE          A 00000.00 0000\n")

    def write_current_accounts(self, accounts, file_path):
        """
        Writes all accounts to the Current Bank Accounts File in JSON format.
        This file is used by the Front End at the start of the next session.

        Args:
            accounts  -- list of MasterAccount objects
            file_path -- path to write the current accounts JSON file
        """
        account_data = []

        for acc in accounts:
            account_data.append({
                'name':         acc.name,
                'acc_num':      acc.acc_num,
                'balance':      acc.balance,
                'payment_plan': acc.plan,
                'is_disabled':  acc.status == 'D',
                'is_admin':     False,
                'total_t':      acc.total_transactions
            })

        with open(file_path, 'w') as f:
            json.dump(account_data, f, indent=4)