import os
import json
import shutil
import pandas as pd
from datetime import datetime
from ocr_utils import extract_text, generate_prompt, call_ollama, get_today_archive_path

# ==================== CONFIG ====================
BILL_PATH = r'C:\Users\esvit\Data Science\Final solutions\Automated-data-entry\Project\Bills'
ARCHIVE_FOLDER = r'C:\Users\esvit\Data Science\Final solutions\Automated-data-entry\Project\Archive'
EXCEL_PATH = r'C:\Users\esvit\Data Science\Final solutions\Automated-data-entry\Project\Invoices.xlsx'

# ==================== MAIN WORKFLOW ====================
all_data = []

for file in os.listdir(BILL_PATH):
    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf')):
        file_path = os.path.join(BILL_PATH, file)
        print(f"Processing file: {file_path}")

        text = extract_text(file_path)
        prompt = generate_prompt(text)
        response = call_ollama(prompt)

        try:
            data = json.loads(response)
            all_data.append(data)

            # Move file to archive
            archive_path = get_today_archive_path(ARCHIVE_FOLDER)
            shutil.move(file_path, os.path.join(archive_path, file))

        except json.JSONDecodeError:
            print(f"JSON parsing failed for {file}")
            print(response)

if all_data:
    df = pd.DataFrame(all_data)
    df.insert(0, "entry_date", datetime.today().strftime("%Y-%m-%d"))

    if os.path.exists(EXCEL_PATH):
        existing_df = pd.read_excel(EXCEL_PATH)
        df = pd.concat([existing_df, df], ignore_index=True)

    df.to_excel(EXCEL_PATH, index=False)
    print("Data saved to Invoices.xlsx")
else:
    print("No valid data extracted.")

