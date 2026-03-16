# backend_main.py
#
# PROGRAM INTENTION:
#   The Back End overnight batch processor for the JST Banking System.
#   Reads the Old Master Bank Accounts File and the Merged Transaction File,
#   applies all transactions to produce the New Master Bank Accounts File
#   and the New Current Bank Accounts File for tomorrow's Front End sessions.
#
# INPUT FILES:
#   - accounts/accounts_master.txt   : Old master bank accounts file (fixed-width format)
#   - t_data.txt                     : Merged bank account transaction file
#
# OUTPUT FILES:
#   - accounts/accounts_master.txt   : New master bank accounts file (updated)
#   - accounts/accounts_current.json : New current bank accounts file (for Front End)
#
# HOW TO RUN:
#   python backend_main.py <master_accounts_file> <transaction_file> <new_master_file> <new_current_file>
#
#   Example:
#   python backend_main.py accounts/accounts_master.txt t_data.txt accounts/accounts_master.txt accounts/accounts_current.json

import sys
from FileReader import FileReader
from FileWriter import FileWriter
from TransactionProcessor import TransactionProcessor


def main():
    """
    Entry point for the Back End. Reads input files, processes all transactions,
    and writes the updated output files.
    """
    # Validate command line arguments
    if len(sys.argv) < 5:
        print("Use: python backend_main.py <master_accounts_file> <transaction_file> <new_master_file> <new_current_file>")
        sys.exit(1)

    master_accounts_file = sys.argv[1]
    transaction_file     = sys.argv[2]
    new_master_file      = sys.argv[3]
    new_current_file     = sys.argv[4]

    reader    = FileReader()
    writer    = FileWriter()
    processor = TransactionProcessor()

    # Step 1: Read old master accounts into memory
    accounts = reader.read_master_accounts(master_accounts_file)

    # Step 2: Read all transactions into memory
    transactions = reader.read_transactions(transaction_file)

    # Step 3: Apply all transactions to accounts
    processor.process_all(accounts, transactions)

    # Step 4: Write updated master accounts file
    writer.write_master_accounts(accounts, new_master_file)

    # Step 5: Write updated current accounts file for Front End
    writer.write_current_accounts(accounts, new_current_file)


if __name__ == "__main__":
    main()