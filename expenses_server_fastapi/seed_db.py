from typing import Any
from sqlalchemy import Table, Connection


categories_data = [
    {"id": 1, "name": "groceries"},
    {"id": 2, "name": "plants"},
    {"id": 3, "name": "eating-out"},
    {"id": 4, "name": "rent"},
    {"id": 5, "name": "travel"},
    {"id": 6, "name": "car"},
    {"id": 7, "name": "pet"},
    {"id": 8, "name": "family"},
    {"id": 9, "name": "gadgets"},
    {"id": 10, "name": "medical"},
    {"id": 11, "name": "hobbies"},
    {"id": 12, "name": "atm"},
    {"id": 13, "name": "other"},
]


def populate_categories(target: Table, connection: Connection, **kw: Any) -> None:
    connection.execute(target.insert(), categories_data)


# TODO: Ask if id should be int (to be compatible with current frontend) or uuid4?
accounts_data = [
    {"id": 0, "name": "Joint Revolut"},
    {"id": 1, "name": "Wise David"},
    {"id": 2, "name": "Wise Dini"},
    {"id": 3, "name": "Revolut David"},
    {"id": 4, "name": "Revolut Dini"},
]


def populate_accounts(target: Table, connection: Connection, **ke: Any) -> None:
    connection.execute(target.insert(), accounts_data)
