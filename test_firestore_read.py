# test_firestore_read.py
from google.cloud import firestore
from decimal import Decimal
from datetime import datetime

def read_bills():
    # Initialize Firestore client
    db = firestore.Client()
    
    # Get all bills from the collection
    bills_ref = db.collection('bills')
    bills = bills_ref.stream()
    
    print("\nStored Bills in Firestore:")
    print("==========================")
    
    for bill in bills:
        data = bill.to_dict()
        print(f"\nBill ID: {bill.id}")
        print(f"Store: {data['store_name']}")
        print(f"Date: {data['date']}")
        print(f"Items:")
        for item in data['items']:
            print(f"- {item['description']}: {item['quantity']}x {item['unit_price']}€ = {item['total_price']}€")
        print(f"Total: {data['total']}€")
        print(f"Payment: {data['payment_method']}")
        print("-" * 50)

if __name__ == "__main__":
    try:
        read_bills()
    except Exception as e:
        print(f"Error reading from Firestore: {str(e)}")