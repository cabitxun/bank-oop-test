from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID

from client import Client
from transaction import Transaction, TransactionState
from views import Views


@dataclass
class Bank:
    clients: dict[UUID, Client]
    transactions: list[Transaction]
    views: dict[Views]

    @classmethod
    def new_bank(cls) -> "Bank":
        return cls(
            clients=dict(),
            transactions=list(),
        )

    def get_balance(self, client_id: UUID) -> Decimal:
        assert client_id in self.clients
        result = Decimal(0)
        client = self.clients[client_id]
        for transaction in self.transactions:
            if transaction.state == TransactionState.COMPLETED:
                if transaction.client_to == client:
                    result += transaction.amount
                if transaction.client_from == client:
                    result -= transaction.amount
        return result


    def new_transaction(
            self,
            client_to: Client,
            amount: Decimal,
            client_from: Optional[Client] = None,
    ) -> Transaction:
        transaction = Transaction.new_transaction(client_from, client_to, amount)
        if client_from is not None:
            if client_to.id not in self.clients or client_from.id not in self.clients:
                transaction.state = TransactionState.ERROR
            elif client_to.id not in self.clients:
                transaction.state = TransactionState.ERROR
        self.transactions.append(transaction)
        return transaction

    def add_client(self, client: Client):
        if client.id not in self.clients:
            self.clients[client.id] = client
            return client

    def complete_transaction(
            self,
            transaction: Transaction,
    ):
        if transaction.state != TransactionState.CREATED:
            return
        if transaction.client_from is not None:
            if self.get_balance(client_id = transaction.client_from.id) < transaction.amount:
                transaction.state = TransactionState.ERROR
                return
        transaction.state = TransactionState.COMPLETED

