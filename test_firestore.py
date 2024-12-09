# test_firestore.py
from google.cloud import firestore

def test_firestore():
    try:
        # Initialize Firestore client
        db = firestore.Client()
        print("Successfully connected to Firestore!")

        # Try to create a test collection and document
        doc_ref = db.collection('test').document('test_doc')
        doc_ref.set({
            'message': 'Hello from bill processor!',
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        print("Successfully wrote to Firestore!")

        # Try to read it back
        doc = doc_ref.get()
        if doc.exists:
            print("Successfully read from Firestore!")
            print(f"Document data: {doc.to_dict()}")
        
        # Clean up - delete the test document
        doc_ref.delete()
        print("Successfully deleted test document!")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_firestore()