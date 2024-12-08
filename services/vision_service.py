# vision_service.py handles the interaction with Google Cloud Vision API for extracting text from images.
#   1. Main Class Structure, Initializes client in constructor
#   2. Text Detection 
#       -  Reading the image
#       - Creating Vision image object
#       - Making API call
#       - Processing response
#
# EXAMPLE
# service = VisionService()
#
# # Basic usage
# text = service.detect_text("receipt.jpg")
# print(f"Extracted text: {text}")
#
# # With error handling
# try:
#     text = service.detect_text("receipt.jpg")
#     if text is None:
#         print("No text found in image")
#     else:
#         print(f"Extracted text: {text}")
# except Exception as e:
#     print(f"Error: {str(e)}")

from google.cloud import vision
from typing import Optional

class VisionService:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()
    
    def detect_text(self, image_path: str) -> Optional[str]:
        with open(image_path, 'rb') as image_file:
            content = image_file.read()
        
        image = vision.Image(content=content)
        response = self.client.text_detection(image=image)
        return response.text_annotations[0].description if response.text_annotations else None