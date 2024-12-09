# test_vision.py
from google.cloud import vision

def test_vision(image_path: str):
    try:
        # Create Vision client
        client = vision.ImageAnnotatorClient()
        print("Successfully created Vision client!")

        # Read image file
        with open(image_path, 'rb') as image_file:
            content = image_file.read()
        
        # Create image object
        image = vision.Image(content=content)
        print("Successfully loaded image!")

        # Perform text detection
        response = client.text_detection(image=image)
        texts = response.text_annotations
        
        if texts:
            print("\nSuccessfully detected text!")
            print("Extracted text:")
            print(texts[0].description)  # First element contains all text
        else:
            print("No text found in image")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Replace with path to your bill image
    image_path = "./test_receipt/FR-1.jpg"  
    test_vision(image_path)