# text_processor.py handles the extraction of structured data from the raw text.
#   1. Initialization
#       Defines regex pattern for price matching
#       Pattern matches: "€12.99" or "12.99"
#   2. Extraction
#       Split text into lines for processing
#       Find price in each line
#       Convert matched price to Decimal
#       Extract description (everything before price)
#       Create BillItem if we have both description and price
# 
# EXMPLE
# processor = TextProcessor()
#
# # Sample text from OCR
# text = """
# Coffee          $4.50
# Sandwich        $12.99
# Tax             $1.75
# """
#
# items = processor.extract_items(text)
# for item in items:
#     print(f"{item.description}: ${item.price}")

import re
from typing import List
from models.bill import BillItem
from decimal import Decimal

class TextProcessor:
    def __init__(self):
        self.price_pattern = r'\€?\d+\.\d{2}'
    
    def extract_items(self, text: str) -> List[BillItem]:
        items = []
        lines = text.split('\n')
        
        for line in lines:
            price_match = re.search(self.price_pattern, line)
            if not price_match:
                continue
                
            price = Decimal(price_match.group().replace('$', ''))
            description = line[:price_match.start()].strip()
            
            if description:
                items.append(BillItem(description=description, price=price))
        
        return items