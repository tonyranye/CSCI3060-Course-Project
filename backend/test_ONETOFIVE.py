import pytest
from MasterAccount import MasterAccount
from TransactionProcessor import*




def create_account(balance=100.00, plan='SP', acc_num='12345'):
    return MasterAccount(
        name="John Doe",
        acc_num=acc_num,
        status='A',
        balance=balance,
        total_transactions=0,
        plan=plan
    )


def create_txn(code, acc_num='12345', amount=0.0):
    return {
        'code': code,
        'name': 'John Doe',
        'acc_num': acc_num,
        'amount': amount,
        'misc': ''
    }



def test_TC1_fee_negative_balance(capsys):
    processor = TransactionProcessor()
    acc = create_account(balance=0.04, plan='SP')

    expected_balance = 0.04
    expected_txn_count = 0

    processor.deduct_fee(acc)


    print("\nTC1 Expected: Error printed, balance unchanged, transaction count unchanged")

    print(f"TC1 Expected Balance: {expected_balance}, Actual Balance: {acc.balance}")
    print(f"TC1 Expected Transactions: {expected_txn_count}, Actual Transactions: {acc.total_transactions}")


    assert acc.balance == expected_balance, f"Expected balance {expected_balance}, got {acc.balance}"
    assert acc.total_transactions == expected_txn_count, (
        f"Expected transaction count {expected_txn_count}, got {acc.total_transactions}"
    )



def test_TC2_fee_success_sp():
    processor = TransactionProcessor()
    acc = create_account(balance=100.00, plan='SP')

    expected_balance = 99.95
    expected_txn_count = 1

    processor.deduct_fee(acc)

    print("\nTC2 Expected: SP fee deducted successfully")
    print(f"TC2 Expected Balance: {expected_balance}, Actual Balance: {acc.balance}")
    print(f"TC2 Expected Transactions: {expected_txn_count}, Actual Transactions: {acc.total_transactions}")

    assert acc.balance == expected_balance, f"Expected balance {expected_balance}, got {acc.balance}"
    assert acc.total_transactions == expected_txn_count, (
        f"Expected transaction count {expected_txn_count}, got {acc.total_transactions}"
    )

def test_TC3_fee_success_np():
    processor = TransactionProcessor()
    acc = create_account(balance=100.00, plan='NP')

    expected_balance = 99.90
    expected_txn_count = 1

    processor.deduct_fee(acc)

    print("\nTC3 Expected: NP fee deducted successfully")
    print(f"TC3 Expected Balance: {expected_balance}, Actual Balance: {acc.balance}")
    print(f"TC3 Expected Transactions: {expected_txn_count}, Actual Transactions: {acc.total_transactions}")

    assert acc.balance == expected_balance, f"Expected balance {expected_balance}, got {acc.balance}"
    assert acc.total_transactions == expected_txn_count, (
        f"Expected transaction count {expected_txn_count}, got {acc.total_transactions}"
    )

def test_TC4_account_not_found_deposit(capsys):
    processor = TransactionProcessor()
    accounts = []
    txn = create_txn(code='04', acc_num='12345', amount=50.00)

    processor.apply_deposit(accounts, txn)


    print("\nTC4 Expected: Error printed because account not found")

    print(f"TC4 Expected Account Count: 0, Actual Account Count: {len(accounts)}")


    assert len(accounts) == 0, f"Expected 0 accounts, got {len(accounts)}"



def test_TC5_successful_deposit():
    processor = TransactionProcessor()
    acc = create_account(balance=100.00, plan='SP')
    accounts = [acc]
    txn = create_txn(code='04', acc_num='12345', amount=50.00)

    expected_balance = 149.95
    expected_txn_count = 1

    processor.apply_deposit(accounts, txn)

    print("\nTC5 Expected: Deposit applied successfully and fee deducted")
    print(f"TC5 Expected Balance: {expected_balance}, Actual Balance: {acc.balance}")
    print(f"TC5 Expected Transactions: {expected_txn_count}, Actual Transactions: {acc.total_transactions}")

    assert acc.balance == expected_balance, f"Expected balance {expected_balance}, got {acc.balance}"
    assert acc.total_transactions == expected_txn_count, (
        f"Expected transaction count {expected_txn_count}, got {acc.total_transactions}"
    )