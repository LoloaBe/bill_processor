# Bill Processor

A Python application that processes bills/receipts using Google Cloud Vision API for text extraction and Google Cloud Firestore for data storage.

## Features

- Extracts text from bill images using Google Cloud Vision API
- Processes and structures bill data including:
  - Store information (name, address, phone)
  - Individual items with quantities and prices
  - Total amount
  - Date and reference number
- Stores processed bills in Google Cloud Firestore
- Supports bills with multiple items and varying quantities

## Prerequisites

- Python 3.x
- Google Cloud account with:
  - Vision API enabled
  - Firestore enabled
  - Service account credentials

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd bill_processor
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up Google Cloud credentials:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
```

## Project Structure

```
bill_processor/
├── __init__.py
├── models/
│   ├── __init__.py
│   └── bill.py
├── services/
│   ├── __init__.py
│   ├── vision_service.py
│   └── text_processor.py
├── repositories/
│   ├── __init__.py
│   └── bill_repository.py
├── main.py
└── requirements.txt
```

## Usage

1. Process a bill image:
```python
from bill_processor import BillProcessor

processor = BillProcessor()
bill = processor.process_bill("path/to/image.jpg")
```

2. Read stored bills:
```python
from google.cloud import firestore

db = firestore.Client()
bills = db.collection('bills').stream()
for bill in bills:
    print(bill.to_dict())
```

## Data Models

### Bill
- store_name: str
- address: str
- phone: str
- date: datetime
- items: List[BillItem]
- total: Decimal
- payment_method: str
- reference: str

### BillItem
- description: str
- quantity: int
- unit_price: Decimal
- total_price: Decimal

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Cloud Vision API for OCR capabilities
- Google Cloud Firestore for database storage