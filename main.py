from services.vision_service import VisionService
from services.text_processor import TextProcessor
from repositories.bill_repository import BillRepository
from typing import Dict, Optional

class BillProcessor:
    def __init__(self):
        self.vision_service = VisionService()
        self.text_processor = TextProcessor()
        self.bill_repository = BillRepository()
    
    def process_bill(self, image_path: str, metadata: Optional[Dict] = None) -> Bill:
        # Extract text from image
        text = self.vision_service.detect_text(image_path)
        if not text:
            raise ValueError("No text detected in image")
            
        # Process text into items
        items = self.text_processor.extract_items(text)
        if not items:
            raise ValueError("No items detected in bill")
            
        # Store bill and return result
        return self.bill_repository.create(items, metadata)

# Example usage
if __name__ == "__main__":
    processor = BillProcessor()
    
    try:
        bill = processor.process_bill(
            "path_to_bill_image.jpg",
            metadata={'store': 'Grocery Store', 'category': 'Food'}
        )
        print(f"Processed bill {bill.id} with {len(bill.items)} items")
        
    except Exception as e:
        print(f"Error processing bill: {str(e)}")