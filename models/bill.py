# The bill.py contains two dataclasses that represent our core domain models:
#  - BillItem represents a single item on a bill
#  - Bill represents the entire bill document
#  - The to_dict() method converts the Bill object to a dictionary for Firestore storage

from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import List, Dict, Optional

@dataclass
class BillItem:
    description: str
    price: Decimal

@dataclass
class Bill:
    id: str
    items: List[BillItem]
    total: Decimal
    timestamp: datetime
    metadata: Dict
    store_name: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'items': [{'description': item.description, 'price': float(item.price)} for item in self.items],
            'total': float(self.total),
            'timestamp': self.timestamp,
            'metadata': self.metadata,
            'store_name': self.store_name
        }