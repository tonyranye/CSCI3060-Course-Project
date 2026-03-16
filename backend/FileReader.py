# FileReader.py
# Responsible for reading the Master Bank Accounts File and the Merged Transaction File
# into memory for the Back End to process.

from MasterAccount import MasterAccount


class FileReader:
    """
    Reads input files for the Back End.

    Methods:
        read_master_accounts -- reads the master accounts file into a list of MasterAccount objects
        read_transactions    -- reads the merged transaction file into a list of transaction dicts
    """

    def read_master_accounts(self, file_path):
        """
        Reads the Master Bank Accounts File and returns a list of MasterAccount objects.
        Each line is 42 characters in the format: NNNNN AAAAAAAAAAAAAAAAAAAA S PPPPPPPP TTTT
        Stops reading when END_OF_FILE account is encountered.

        Args:
            file_path -- path to the master accounts file

        Returns:
            list of MasterAccount objects
        """
        accounts = []

        with open(file_path, 'r') as f:
            for line in f:
                clean_line = line.rstrip('\n')

                # Stop at END_OF_FILE marker
                if 'END_OF_FILE' in clean_line:
                    break

                # Check for valid line length -- fatal error if wrong
                if len(clean_line) != 42:
                    print(f"ERROR: Fatal error - File {file_path} - Invalid line length ({len(clean_line)} chars, expected 42): {clean_line}")
                    exit(1)

                # Parse fields by position
                acc_num           = clean_line[0:5].strip()
                name              = clean_line[6:26].strip()
                status            = clean_line[27]
                balance           = float(clean_line[29:37].strip())
                total_transactions = int(clean_line[38:42].strip())

                # Determine plan -- master file does not store plan, default to NP
                # Plan will be updated when transactions are applied
                plan = "NP"

                accounts.append(MasterAccount(name, acc_num, status, balance, total_transactions, plan))

        return accounts

    def read_transactions(self, file_path):
        """
        Reads the Merged Bank Account Transaction File and returns a list of transaction dicts.
        Each line is 40 characters in the format: CC AAAAAAAAAAAAAAAAAAAA NNNNN PPPPPPPP MM
        Skips end-of-session (code 00) lines.

        Args:
            file_path -- path to the merged transaction file

        Returns:
            list of dicts with keys: code, name, acc_num, amount, misc
        """
        transactions = []

        with open(file_path, 'r') as f:
            for line in f:
                clean_line = line.rstrip('\n')

                # Skip empty lines
                if not clean_line.strip():
                    continue

                # Check for valid line length -- fatal error if wrong
                if len(clean_line) != 41:
                    print(f"ERROR: Fatal error - File {file_path} - Invalid line length ({len(clean_line)} chars, expected 40): {clean_line}")
                    exit(1)

                # Parse fields by position
                code    = clean_line[0:2].strip()
                name    = clean_line[3:23].strip()
                acc_num = clean_line[24:29].strip()
                amount  = float(clean_line[30:38].strip())
                misc    = clean_line[39:41].strip() if len(clean_line) > 39 else ""

                # Skip end of session markers
                if code == "00":
                    continue

                transactions.append({
                    'code':    code,
                    'name':    name,
                    'acc_num': acc_num,
                    'amount':  amount,
                    'misc':    misc
                })

        return transactions