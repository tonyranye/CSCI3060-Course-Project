# CSCI 3060U Course Project - JST Banking System

A command-line banking application developed as part of CSCI 3060U Software Quality Assurance course.

## Team Members
- **Jared Efrem**
- **Sumukh Jagirdar**
- **Tony Akinniranye**

## Project Overview

The JST Banking System is a front-end banking application that simulates real-world banking operations. It supports two types of sessions:
- **Standard Users** (Account Holders): Can perform personal banking transactions
- **Admin Users** (Bank Employees): Can perform all transactions plus account management

## Features

### Standard User Operations
- 🔐 Login/Logout
- 💰 Withdraw funds
- 💸 Transfer money between accounts
- 📄 Pay bills (EC, CQ, FI)
- 💵 Deposit funds

### Admin Operations
- ➕ Create new accounts
- ❌ Delete accounts
- 🚫 Disable/Enable accounts
- 🔄 Change payment plans (Student Plan ↔ Non-Student Plan)

## Project Structure
```
CSCI3060-Course-Project/
├── main.py                      # Main program entry point
├── BankSystem.py                # Banking system logic and session management
├── Account.py                   # Account class definition
├── accounts/
│   └── accounts_valid.json      # User account data
├── t_data.txt                   # Daily transaction log
└── src/                         # Additional modules
```

## How to Run

### Prerequisites
- Python 3.x
- No external dependencies required (uses only standard library)

### Running the Program

1. Clone the repository:
```bash
git clone https://github.com/tonyranye/CSCI3060-Course-Project.git
cd CSCI3060-Course-Project
```

2. Run the program:
```bash
python main.py
```

3. Follow the on-screen prompts -  For each prompt type in the name of the action you want to select: ex 'login', 'standard'...
   - Select **Login** from the menu
   - Choose session type: `standard` or `admin`
   - For standard users: Enter your account holder name
   - Perform transactions
   - **Logout** before exiting to save transaction log

## Usage Examples

### Login as Standard User
```
Enter session type: standard
Enter account holder name: John Doe
```

### Login as Admin
```
Enter session type: admin
```

### Menu Navigation
You can select options by typing:
- The full command name (e.g., `login`, `withdraw`, `transfer`)

## File Formats

### accounts_valid.json
```json
[
  {
    "name": "John Doe",
    "acc_num": "10000",
    "balance": 1000.00,
    "payment_plan": "SP",
    "is_disabled": false,
    "is_admin": false
  }
]
```

### t_data.txt (Transaction Log)
Format: `[Code] [Name(20)] [AccNum(5)] [Amount(8)] [Misc(2)]`
```
04 John Doe             10000 00200.00   
02 Jane Smith           10001 00150.00   
```

**Transaction Codes:**
- `00` - Logout
- `01` - Withdraw
- `02` - Transfer
- `03` - Paybill
- `04` - Deposit
- `05` - Create Account
- `06` - Delete Account
- `07` - Disable Account
- `08` - Change Plan

