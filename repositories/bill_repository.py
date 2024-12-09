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
# repositories/bill_repository.py
from google.cloud import firestore
from typing import List, Dict, Optional
from decimal import Decimal
from datetime import datetime
from models.bill import Bill, BillItem  # Add this import

class BillRepository:
    def __init__(self):
        self.db = firestore.Client()
        self.collection = self.db.collection('bills')
    
    def create(self, bill: Bill) -> None:
        """Store bill in Firestore"""
        bill_ref = self.collection.document()
        
        # Convert to dictionary for Firestore
        bill_data = {
            'store_name': bill.store_name,
            'address': bill.address,
            'phone': bill.phone,
            'date': bill.date,
            'total': float(bill.total),
            'payment_method': bill.payment_method,
            'reference': bill.reference,
            'items': [{
                'description': item.description,
                'quantity': item.quantity,
                'unit_price': float(item.unit_price),
                'total_price': float(item.total_price)
            } for item in bill.items]
        }
        
        bill_ref.set(bill_data)