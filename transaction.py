from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from client import Client


class TransactionState(Enum):
    CREATED: str = "Created"
    ERROR: str = "Error"
    COMPLETED: str = "Completed"


@dataclass
class Transaction:
    id: UUID
    client_from: Optional[Client]
    client_to: Client
    amount: Decimal
    state: str = TransactionState.CREATED

    @classmethod
    def new_transaction(cls, client_from: Client, client_to: Client, amount: Decimal):
        return cls(
            id=uuid4(),
            client_from=client_from,
            client_to=client_to,
            amount=amount
        )

    def check_amount(self, amount: Decimal):
        if amount < 0:
            self.state = TransactionState.ERROR
