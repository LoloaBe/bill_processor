# main.py
from services.vision_service import VisionService
from services.text_processor import TextProcessor
from repositories.bill_repository import BillRepository
from models.bill import Bill

class BillProcessor:
    def __init__(self):
        self.vision_service = VisionService()
        self.text_processor = TextProcessor()
        self.bill_repository = BillRepository()
    
    def process_bill(self, image_path: str) -> Bill:
        # Get text from image
        text = self.vision_service.detect_text(image_path)
        if not text:
            raise ValueError("No text detected in image")
        
        # Debug: Print the raw text
        print("Raw text from Vision API:")
        print("------------------------")
        print(text)
        print("------------------------")
            
        # Process text into bill
        bill = self.text_processor.process_text(text)
        
        # Store bill
        self.bill_repository.create(bill)
        
        return bill

if __name__ == "__main__":
    processor = BillProcessor()
    
    try:
        bill = processor.process_bill("./test_receipt/FR-1.jpg")  # Update this path
        print(f"\nStore: {bill.store_name}")
        print(f"Address: {bill.address}")
        print(f"Date: {bill.date}")
        print("\nItems:")
        for item in bill.items:
            print(f"- {item.description}: {item.quantity}x {item.unit_price}€ = {item.total_price}€")
        print(f"\nTotal: {bill.total}€")
        print(f"Payment: {bill.payment_method}")
        print(f"Reference: {bill.reference}")
        
    except Exception as e:
        print(f"Error processing bill: {str(e)}")