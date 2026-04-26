# JST Banking System Simulation

**CSCI 3060U – Software Quality Assurance | Winter 2025**

A two-part console-based banking system built with Python, developed following Agile practices including continuous testing, pair programming, and frequent integration. The system simulates a real-world ATM terminal (Front End) and an overnight batch processor (Back End).

**Team:** Jared Efrem, Sumukh Jagirdar, Tony Akinniranye

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Setup](#setup)
- [Running the Front End](#running-the-front-end)
- [Running the Back End](#running-the-back-end)
- [Automation Scripts](#automation-scripts)
- [Running Tests](#running-tests)
- [File Formats](#file-formats)
- [Transaction Codes Reference](#transaction-codes-reference)

---

## Overview

The Banking System consists of two independent components:

**Front End** - An interactive ATM terminal that reads the current accounts file, processes a session of user transactions, and writes a transaction log on logout.

**Back End** - An overnight batch processor that reads the previous day's master accounts file and a merged transaction file, applies all transactions, and produces an updated master accounts file and a new current accounts file for the next day's Front End sessions.

---

## Project Structure

```
CSCI3060-Course-Project/
│
├── main.py                         # Front End entry point
├── BankSystem.py                   # Core banking session logic
├── Account.py                      # Account model and transaction methods
├── config.py                       # File path configuration
├── deposit.py                      # Deposit helper
├── withdraw.py                     # Withdraw helper
│
├── accounts/
│   ├── accounts_valid.json         # Active current accounts (Front End input/output)
│   ├── accounts_current.json       # Current accounts snapshot
│   ├── accounts_current_new.json   # Updated current accounts (Back End output)
│   ├── accounts_master.txt         # Master accounts file (Back End input)
│   └── accounts_master_new.txt     # Updated master accounts (Back End output)
│
├── backend/
│   ├── backend_main.py             # Back End entry point
│   ├── TransactionProcessor.py     # Applies transactions to master file
│   ├── FileReader.py               # Reads master and transaction files
│   ├── FileWriter.py               # Writes master and current accounts files
│   └── MasterAccount.py            # Master account model
│
├── src/
│   └── account_modification/       # Admin account operations (create, delete, disable, changeplan)
│   └── transactions/               # Transaction logic modules
│
├── automation/
│   └── run.py                      # Automation helper script
│
├── tests/                          # Test input/expected output pairs
│   ├── 001_session_rules-login_logout/
│   ├── 002_withdrawal/
│   ├── 003_transfer/
│   ├── 004_paybill/
│   ├── 005_deposit/
│   ├── 006_create_account/
│   ├── 007_disable_delete_changeplan/
│   └── 008_output_format/
│
├── results/                        # Actual test output files
│
├── daily_tmp/                      # Per-session ATF files for a single day
├── weekly_data/                    # Multi-day simulation data
│
├── run_one.sh                      # Run a single test case
├── run_all.sh                      # Run the full test suite
├── daily.sh                        # Simulate a single day (Front End + Back End)
└── weekly.sh                       # Simulate a full week of transactions
```

---

## Requirements

- Python 3.x (no external packages required)
- Bash (for running shell scripts on Linux/macOS; use Git Bash or WSL on Windows)

---

## Setup

```bash
git clone https://github.com/tonyranye/Banking-System-Simulation.git
cd Banking-System-Simulation
```

Ensure `accounts/accounts_valid.json` exists and is populated with at least one account before starting the Front End. The file uses the following format per entry:

```json
[
  {
    "name": "John Doe",
    "acc_num": "10000",
    "balance": 500.00,
    "payment plan": "SP",
    "is_disabled": false,
    "is_admin": false
  }
]
```

---

## Running the Front End

The Front End is an interactive console application. Run it from the project root:

```bash
python main.py
```

On startup, the program loads all accounts from `accounts/accounts_valid.json` and presents a menu. You must **login** before any other operation is available.

### Session Types

| Session | How to Login | Available Transactions |
|---|---|---|
| **Standard** | Enter `login` → `standard` → account holder name | withdraw, transfer, paybill, deposit |
| **Admin** | Enter `login` → `admin` | all of the above + create, delete, disable, changeplan |

### Available Menu Commands

```
login             Start a session (standard or admin)
withdraw          Withdraw funds from the current account
transfer          Transfer funds to another account
paybills          Pay a bill to an approved company
deposit           Deposit funds into the current account
create account    Create a new bank account (admin only)
delete account    Delete a bank account (admin only)
disable account   Disable a bank account (admin only)
change current plan  Change account payment plan SP ↔ NP (admin only)
logout            End the session and write the transaction log
exit              Logout (if logged in) and quit the program
```

At **logout**, all session transactions are appended to `t_data.txt` in the fixed-length ATF format required by the Back End.

### Standard Mode Limits

| Transaction | Limit per session |
|---|---|
| Withdrawal | $500.00 |
| Transfer | $1,000.00 |
| Pay Bill | $2,000.00 per company |

Approved bill companies: `EC` (The Bright Light Electric Company), `CQ` (Credit Card Company Q), `FI` (Fast Internet, Inc.)

---

## Running the Back End

The Back End is run after a day's Front End sessions are complete and their transaction files have been merged.

```bash
python backend/backend_main.py
```

The Back End reads:
- `accounts/accounts_master.txt` - the previous day's master accounts file
- `daily_merged.atf` - the merged transaction file from all Front End sessions

It produces:
- `accounts/accounts_master_new.txt` - the new master accounts file (sorted by account number)
- `accounts/accounts_current_new.json` - the new current accounts file for tomorrow's Front End

**Transaction fees** are applied automatically: $0.05 per transaction for Student Plan (SP) accounts, $0.10 per transaction for Non-Student Plan (NP) accounts.

Any constraint violations (e.g., negative balance, duplicate account number) are logged to the terminal in the form:

```
ERROR: <description of error and the transaction that caused it>
```

---

## Automation Scripts

### Simulate one full day

Runs multiple Front End sessions, merges the resulting `.atf` files, then runs the Back End:

```bash
bash daily.sh
```

Session transaction files are saved to `daily_tmp/` (e.g., `session_1.atf`, `session_2.atf`). These are concatenated into `daily_merged.atf` before the Back End runs.

### Simulate a full week

Runs the daily simulation across 7 sequential days, carrying the updated master and current accounts files forward each day:

```bash
bash weekly.sh
```

Weekly data snapshots are stored in `weekly_data/` with per-day master, current, merged, and session files.

---

## Running Tests

Each test case consists of an `_input.txt` (stdin) and an `_expected.txt` (expected stdout output). Results are written to the `results/` directory.

### Run a single test

```bash
bash run_one.sh tests/002_withdrawal/006_withdraws_over_limit_input.txt
```

### Run all tests

```bash
bash run_all.sh
```

This iterates over all test cases in `tests/`, pipes each input file through `main.py`, captures the output, and saves it to the corresponding location in `results/`. You can then diff actual vs. expected output to check for regressions.

### Test categories

| Folder | What is tested |
|---|---|
| `001_session_rules-login_logout` | Login/logout enforcement, privilege separation |
| `002_withdrawal` | Withdrawal limits, negative balance, disabled accounts |
| `003_transfer` | Transfer validation, session limits, owner verification |
| `004_paybill` | Company validation, bill payment limits |
| `005_deposit` | Deposit recording, funds not available same session |
| `006_create_account` | Admin-only creation, name length, account number uniqueness |
| `007_disable_delete_changeplan` | Admin-only operations, post-action transaction rejection |
| `008_output_format` | Transaction file written on logout, fixed-length line format |

---

## File Formats

### Current Bank Accounts File (37 characters + newline)

```
NNNNN AAAAAAAAAAAAAAAAAAAA S PPPPPPPP
```

| Field | Description |
|---|---|
| `NNNNN` | 5-digit account number, zero-padded, right-justified |
| `AAAAAAAAAAAAAAAAAAAA` | Account holder name, 20 chars, left-justified, space-padded |
| `S` | Status: `A` (active) or `D` (disabled) |
| `PPPPPPPP` | Balance in format `00000.00`, right-justified |

File ends with a special record where the name field is `END_OF_FILE`.

### Bank Account Transaction File / ATF (40 characters + newline)

```
CC AAAAAAAAAAAAAAAAAAAA NNNNN PPPPPPPP MM
```

| Field | Description |
|---|---|
| `CC` | 2-digit transaction code (see below) |
| `AAAAAAAAAAAAAAAAAAAA` | Account holder name, 20 chars |
| `NNNNN` | 5-digit account number |
| `PPPPPPPP` | Amount in format `00000.00` |
| `MM` | Miscellaneous info (e.g., bill company code) |

### Master Bank Accounts File (42 characters + newline)

Same as the Current Accounts File but with an additional `TTTT` field (4-digit transaction count, zero-padded) at the end:

```
NNNNN AAAAAAAAAAAAAAAAAAAA S PPPPPPPP TTTT
```

The master file must always be sorted in ascending order by account number.

---

## Transaction Codes Reference

| Code | Transaction |
|---|---|
| `00` | End of session |
| `01` | Withdrawal |
| `02` | Transfer |
| `03` | Pay bill |
| `04` | Deposit |
| `05` | Create account |
| `06` | Delete account |
| `07` | Disable account |
| `08` | Change payment plan |
