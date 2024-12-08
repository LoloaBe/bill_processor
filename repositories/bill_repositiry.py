# bill_repository.py handles all database operations.
#   1. Initialization
#       Creates Firestore client
#       References 'bills' collection in Firestore
#   2. Create
#       Generates unique UUID for the bill
#       Creates Bill object with given items
#       Calculates total automatically
#       Stores in Firestore
#       Returns created Bill object
#   3. Read
#       Retrieves bill by ID
#       Returns None if not found
#       Uses helper method to convert document to Bill object
#   4. Query
#       Supports flexible filtering
#       Example usage: query(store_name="Walmart", category="Groceries")
#       Returns list of matching Bills
#   5. Helper Method for Document Conversion
#       Converts Firestore document to Bill object
#       Handles conversion of float back to Decimal
#       Private method (indicated by underscore prefix)
#
# # Create new bill
# repo = BillRepository()
# items = [BillItem("Coffee", Decimal("4.50")), BillItem("Sandwich", Decimal("12.00"))]
# bill = repo.create(items, metadata={"category": "Lunch"})

# # Retrieve bill
# same_bill = repo.get(bill.id)

# # Query bills
# lunch_bills = repo.query(category="Lunch")

from google.cloud import firestore
from models.bill import Bill
from typing import List, Dict, Optional
import uuid
from datetime import datetime

class BillRepository:
    def __init__(self):
        self.db = firestore.Client()
        self.collection = self.db.collection('bills')
    
    def create(self, items: List[BillItem], metadata: Dict = None) -> Bill:
        bill_id = str(uuid.uuid4())
        bill = Bill(
            id=bill_id,
            items=items,
            total=sum(item.price for item in items),
            timestamp=datetime.now(),
            metadata=metadata or {}
        )
        
        self.collection.document(bill_id).set(bill.to_dict())
        return bill
    
    def get(self, bill_id: str) -> Optional[Bill]:
        doc = self.collection.document(bill_id).get()
        return self._doc_to_bill(doc) if doc.exists else None
    
    def query(self, **filters) -> List[Bill]:
        query = self.collection
        for key, value in filters.items():
            query = query.where(key, '==', value)
        return [self._doc_to_bill(doc) for doc in query.stream()]
    
    def _doc_to_bill(self, doc) -> Bill:
        data = doc.to_dict()
        items = [
            BillItem(description=item['description'], price=Decimal(str(item['price'])))
            for item in data['items']
        ]
        return Bill(
            id=doc.id,
            items=items,
            total=Decimal(str(data['total'])),
            timestamp=data['timestamp'],
            metadata=data['metadata'],
            store_name=data.get('store_name')
        )