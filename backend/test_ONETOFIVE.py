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

    processor.deduct_fee(acc)


    assert acc.balance == 0.04
    assert acc.total_transactions == 0



def test_TC2_fee_success_sp():
    processor = TransactionProcessor()
    acc = create_account(balance=100.00, plan='SP')

    processor.deduct_fee(acc)

    assert acc.balance == 99.95
    assert acc.total_transactions == 1


def test_TC3_fee_success_np():
    processor = TransactionProcessor()
    acc = create_account(balance=100.00, plan='NP')

    processor.deduct_fee(acc)

    assert acc.balance == 99.90
    assert acc.total_transactions == 1

def test_TC4_account_not_found_deposit(capsys):
    processor = TransactionProcessor()
    accounts = []
    txn = create_txn(code='04', acc_num='12345', amount=50.00)

    processor.apply_deposit(accounts, txn)

    captured = capsys.readouterr()

    assert "ERROR" in captured.out
    assert len(accounts) == 0

def test_TC5_successful_deposit():
    processor = TransactionProcessor()
    acc = create_account(balance=100.00, plan='SP')
    accounts = [acc]
    txn = create_txn(code='04', acc_num='12345', amount=50.00)

    processor.apply_deposit(accounts, txn)

    assert acc.balance == 149.95
    assert acc.total_transactions == 1