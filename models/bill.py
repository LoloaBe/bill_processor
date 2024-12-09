# The bill.py contains two dataclasses that represent our core domain models:
#  - BillItem represents a single item on a bill
#  - Bill represents the entire bill document
#  - The to_dict() method converts the Bill object to a dictionary for Firestore storage

# models/bill.py
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import List, Dict

@dataclass
class BillItem:
    description: str
    quantity: int
    unit_price: Decimal
    total_price: Decimal

@dataclass
class Bill:
    store_name: str
    address: str
    phone: str
    date: datetime
    items: List[BillItem]
    total: Decimal
    payment_method: str
    reference: str