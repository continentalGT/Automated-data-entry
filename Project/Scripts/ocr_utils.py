import os
import pytesseract
from PIL import Image
from datetime import datetime
import ollama

# Set pytesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(image_path):
    if os.path.exists(image_path):
        image = Image.open(image_path)
        return pytesseract.image_to_string(image, config='--psm 6')
    else:
        print('File does not exist')
        return ""

def generate_prompt(text):
    prompt = f"""You are a helpful assistant that parses the text
    received from OCR extraction into a JSON format.

    Here is the text provided to you:
    {text}

    Your task is to extract the following information:
    Vendor name, Date, Total Amount, Payment Method.

    The output should be JSON like this:
    {{
      "vendor_name": "Amazon",
      "date": "2023-10-01",
      "total_amount": 150.75,
      "payment_method": "Credit Card"
    }}

    Only provide the JSON response.
    """
    return prompt

def call_ollama(prompt):
    response = ollama.chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response['message']['content']

def get_today_archive_path(archive_folder):
    today = datetime.today().strftime("%Y-%m-%d")
    path = os.path.join(archive_folder, today)
    os.makedirs(path, exist_ok=True)
    return path
