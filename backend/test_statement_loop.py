import pytest
from MasterAccount import MasterAccount
from TransactionProcessor import*



# Helper function to create a MasterAccount object with default values
def create_account(balance=100.00, plan='SP', acc_num='12345'):
    return MasterAccount(
        name="John Doe",
        acc_num=acc_num,
        status='A',
        balance=balance,
        total_transactions=0,
        plan=plan
    )

# Helper function to create a transaction dict
def create_txn(code, acc_num='12345', amount=0.0):
    return {
        'code': code,
        'name': 'John Doe',
        'acc_num': acc_num,
        'amount': amount,
        'misc': ''
    }


# TC1: Fee deduction with insufficient balance for SP plan
def test_TC1_fee_negative_balance(capsys):
    processor = TransactionProcessor()
    acc = create_account(balance=0.04, plan='SP')

    expected_balance = 0.04
    expected_txn_count = 0

    processor.deduct_fee(acc)


    print("\n\nTC1 Expected: Error printed, balance unchanged, transaction count unchanged")

    print(f"TC1 Expected Balance: {expected_balance}, Actual Balance: {acc.balance}")
    print(f"TC1 Expected Transactions: {expected_txn_count}, Actual Transactions: {acc.total_transactions}")


    assert acc.balance == expected_balance, f"Expected balance {expected_balance}, got {acc.balance}"
    assert acc.total_transactions == expected_txn_count, (
        f"Expected transaction count {expected_txn_count}, got {acc.total_transactions}"
    )


# TC2: Successful fee deduction for SP plan
def test_TC2_fee_success_sp():
    processor = TransactionProcessor()
    acc = create_account(balance=100.00, plan='SP')

    expected_balance = 99.95
    expected_txn_count = 1

    processor.deduct_fee(acc)

    print("\n\nTC2 Expected: SP fee deducted successfully")
    print(f"TC2 Expected Balance: {expected_balance}, Actual Balance: {acc.balance}")
    print(f"TC2 Expected Transactions: {expected_txn_count}, Actual Transactions: {acc.total_transactions}")

    assert acc.balance == expected_balance, f"Expected balance {expected_balance}, got {acc.balance}"
    assert acc.total_transactions == expected_txn_count, (
        f"Expected transaction count {expected_txn_count}, got {acc.total_transactions}"
    )
    
# TC3: Successful fee deduction for NP plan
def test_TC3_fee_success_np():
    processor = TransactionProcessor()
    acc = create_account(balance=100.00, plan='NP')

    expected_balance = 99.90
    expected_txn_count = 1

    processor.deduct_fee(acc)

    print("\n\nTC3 Expected: NP fee deducted successfully")
    print(f"TC3 Expected Balance: {expected_balance}, Actual Balance: {acc.balance}")
    print(f"TC3 Expected Transactions: {expected_txn_count}, Actual Transactions: {acc.total_transactions}")

    assert acc.balance == expected_balance, f"Expected balance {expected_balance}, got {acc.balance}"
    assert acc.total_transactions == expected_txn_count, (
        f"Expected transaction count {expected_txn_count}, got {acc.total_transactions}"
    )

# TC4: Account not found for deposit
def test_TC4_account_not_found_deposit(capsys):
    processor = TransactionProcessor()
    accounts = []
    txn = create_txn(code='04', acc_num='12345', amount=50.00)

    processor.apply_deposit(accounts, txn)


    print("\n\nTC4 Expected: Error printed because account not found")

    print(f"TC4 Expected Account Count: 0, Actual Account Count: {len(accounts)}")


    assert len(accounts) == 0, f"Expected 0 accounts, got {len(accounts)}"


# TC5: Successful deposit and fee deduction
def test_TC5_successful_deposit():
    processor = TransactionProcessor()
    acc = create_account(balance=100.00, plan='SP')
    accounts = [acc]
    txn = create_txn(code='04', acc_num='12345', amount=50.00)

    expected_balance = 149.95
    expected_txn_count = 1

    processor.apply_deposit(accounts, txn)

    print("\n\nTC5 Expected: Deposit applied successfully and fee deducted")
    print(f"TC5 Expected Balance: {expected_balance}, Actual Balance: {acc.balance}")
    print(f"TC5 Expected Transactions: {expected_txn_count}, Actual Transactions: {acc.total_transactions}")

    assert acc.balance == expected_balance, f"Expected balance {expected_balance}, got {acc.balance}"
    assert acc.total_transactions == expected_txn_count, (
        f"Expected transaction count {expected_txn_count}, got {acc.total_transactions}"
    )
    
# TC6: Empty list – loop never executes
def test_find_account_empty_list(capsys):
    tp = TransactionProcessor()
    result = tp.find_account([], "123")

    print("\n\n--- TC6: FIND ACCOUNT (EMPTY LIST) ---")
    print("EXPECTED: None (no accounts to search)")
    print(f"ACTUAL:   {result}")

    assert result is None



# TC7: Account found on first iteration – loop runs once
def test_find_account_found_first(capsys):
    tp = TransactionProcessor()
    accounts = [
        MasterAccount("Alice", "123", "A", 100.0, 0, "SP"),
        MasterAccount("Bob", "456", "A", 50.0, 0, "NP"),
    ]

    result = tp.find_account(accounts, "123")

    print("\n\n--- TC7: FIND ACCOUNT (FOUND FIRST) ---")
    print("EXPECTED: Account object with acc_num='123'")
    print(f"ACTUAL:   {result.acc_num if result else None}")

    assert result is accounts[0]



# TC8: Account not found – loop runs to completion
def test_find_account_not_found(capsys):
    tp = TransactionProcessor()
    accounts = [
        MasterAccount("A", "111", "A", 0, 0, "SP"),
        MasterAccount("B", "222", "A", 0, 0, "NP"),
    ]

    result = tp.find_account(accounts, "999")

    print("\n\n--- TC8: FIND ACCOUNT (NOT FOUND) ---")
    print("EXPECTED: None")
    print(f"ACTUAL:   {result}")

    assert result is None
    
# TC9: Empty transaction list

def test_process_all_empty_transactions(capsys):
    tp = TransactionProcessor()
    tp.called = []

    tp.process_all([], [])

    print("\n\n--- TC9: PROCESS ALL (EMPTY LIST) ---")
    print("EXPECTED: No handlers called")
    print(f"ACTUAL:   {tp.called}")

    assert tp.called == []



# TC10: Valid transaction code

def test_process_all_valid_code(monkeypatch, capsys):
    tp = TransactionProcessor()
    tp.called = []

    def fake_deposit(accounts, txn):
        tp.called.append("04")

    monkeypatch.setattr(tp, "apply_deposit", fake_deposit)

    txn = {"code": "04", "acc_num": "123"}
    tp.process_all([], [txn])

    print("\n\n--- TC10: PROCESS ALL (VALID CODE) ---")
    print("EXPECTED: Handler '04' called")
    print(f"ACTUAL:   {tp.called}")

    assert tp.called == ["04"]



# TC11: Invalid transaction code

def test_process_all_invalid_code(capsys):
    tp = TransactionProcessor()
    txn = {"code": "99", "acc_num": "123"}

    # We expect an error message about the unknown code, so we capture stdout
    tp.process_all([], [txn])
    captured = capsys.readouterr().out.strip()

    print("\n\n--- TC11: PROCESS ALL (INVALID CODE) ---")
    print("EXPECTED: Error message about unknown code")
    print(f"ACTUAL:   {captured}")

    assert "Unknown transaction code" in captured



# TC12: Multiple transactions

def test_process_all_multiple_transactions(monkeypatch, capsys):
    tp = TransactionProcessor()
    tp.called = []


    # Used monkeypatch to replace the apply methods with lambdas that append the code to tp.called
    monkeypatch.setattr(tp, "apply_withdraw", lambda a, t: tp.called.append("01"))
    monkeypatch.setattr(tp, "apply_deposit", lambda a, t: tp.called.append("04"))
    monkeypatch.setattr(tp, "apply_disable", lambda a, t: tp.called.append("07"))
    
    # Create a list of transactions with different codes to test that the correct handlers are called for each code
    txns = [
        {"code": "01", "acc_num": "A"},
        {"code": "04", "acc_num": "B"},
        {"code": "07", "acc_num": "C"},
    ]

    tp.process_all([], txns)

    print("\n\n--- TC12: PROCESS ALL (MULTIPLE TXNS) ---")
    print("EXPECTED: ['01', '04', '07']")
    print(f"ACTUAL:   {tp.called}")

    assert tp.called == ["01", "04", "07"]
