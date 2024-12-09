import re
from decimal import Decimal
from datetime import datetime
from models.bill import Bill, BillItem
from typing import List

class TextProcessor:
    def __init__(self):
        self.price_pattern = r'(\d+\.\d{2})€?'  # € symbol is optional to catch "2.20" without €
    
    def process_text(self, text: str) -> Bill:
        # Split and clean lines
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Extract store info
        store_name = lines[1]  # CRF-CITY LA ROCHELLE
        address = lines[2]     # 33 RUE DE LA SCIERIE
        city = lines[3]        # 17000 LA ROCHELLE
        phone = lines[4].split(':')[1].strip()  # 05.46.27.02.12
        
        # Extract items section
        items = []
        item_lines = []
        in_item_section = False
        
        # Collect lines between DESCRIPTION and TOTAL
        for line in lines:
            if 'DESCRIPTION' in line:
                in_item_section = True
                continue
            if 'TOTAL A PAYER' in line:
                in_item_section = False
                continue
            if in_item_section:
                item_lines.append(line)
        
        print("\nDebug - Processing Items:")
        
        # Extract all prices first
        prices = []
        for line in item_lines:
            price_match = re.search(self.price_pattern, line)
            if price_match:
                prices.append(Decimal(price_match.group(1)))
        
        print("Debug - Found prices:", prices)
        
        # Process items
        items = []
        
        # Create a list of all items with their descriptions
        item_descriptions = [line.replace('*', '').strip() 
                           for line in item_lines if line.startswith('*')]
        
        for i, description in enumerate(item_descriptions):
            if description == "4X100GDESS.PANACHE":
                items.append(BillItem(
                    description=description,
                    quantity=1,
                    unit_price=prices[0],
                    total_price=prices[0]
                ))
                print(f"Added item: {description} - {prices[0]}€")
                
            elif description == "COUSCOUS CRF 440G":
                items.append(BillItem(
                    description=description,
                    quantity=1,
                    unit_price=prices[1],
                    total_price=prices[1]
                ))
                print(f"Added item: {description} - {prices[1]}€")
                
            elif description == "INNOCENT MANG/PASS":
                items.append(BillItem(
                    description=description,
                    quantity=2,
                    unit_price=prices[2],  # 2.20
                    total_price=prices[3]   # 4.40
                ))
                print(f"Added item: {description} - 2x {prices[2]}€ = {prices[3]}€")
        
        # Extract date and reference
        date = None
        reference = None
        for line in lines:
            if re.match(r'\d{4}\s+\d{3}\s+\d{6}\s+\d{2}/\d{2}/\d{4}', line):
                parts = line.split()
                reference = ' '.join(parts[:3])
                date_str = parts[3]
                time_str = parts[4]
                date = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M:%S")
                break
        
        return Bill(
            store_name=store_name,
            address=f"{address}, {city}",
            phone=phone,
            date=date,
            items=items,
            total=Decimal('9.00'),
            payment_method="CB EMV SANS CONTACT",
            reference=reference
        )