from decimal import Decimal

from client import Client
from transaction import Transaction, TransactionState


def test_transaction_create():
    client1 = Client.from_name("John")
    client2 = Client.from_name("Bill")

    transaction = Transaction.new_transaction(client1, client2, Decimal(100))
    assert(isinstance(transaction, Transaction))
    assert(transaction.state == TransactionState.CREATED)


def test_transaction_error():
    client1 = Client.from_name("John")
    client2 = Client.from_name("Bill")

    transaction = Transaction.new_transaction(client1, client2, Decimal(-100))
    assert(isinstance(transaction, Transaction))
    transaction.check_amount(transaction.amount)
    assert(transaction.state == TransactionState.ERROR)
