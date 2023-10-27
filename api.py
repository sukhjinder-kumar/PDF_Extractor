from flask import Flask, request, jsonify
import PyPDF2
import fitz
import re
from datetime import datetime

app = Flask(__name__)


def extract_images_from_pdf(pdf_path):
    '''Save image in Output/Image folder'''
    images = []
    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc):
            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_data = base_image["image"]
                image_format = base_image["ext"]
                img_path = f"Output/Image/image_{page_num}_{img_index}.{image_format}"
                with open(img_path, "wb") as f:
                    f.write(image_data)
                images.append(img_path)
    return images


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text


class Transaction:
    def __init__(self, date, client, amount):
        self.date = date  # datetime object
        self.client = client
        self.amount = amount

    def to_dict(self):
        return {
            "date": self.date.strftime("%m/%d/%Y"),
            "client": self.client,
            "amount": self.amount,
        }

    @classmethod
    def from_dict(cls, data):
        date = datetime.strptime(data["date"], "%m/%d/%Y")
        client = data["client"]
        amount = data["amount"]
        return cls(date, client, amount)


@app.get("/filter_transactions")
def filter_transactions():
    '''Takes text and Returns a list of Transaction objects'''
    text = request.get_json()["text"]
    text_list = text.splitlines()  # Contains list of lines
    # Define the pattern to match the structure
    pattern = r'(\d{2}/\d{2}/\d{4})\s+(.+)\s+(\d+\.\d+)'
    transactions = []
    # Filter lines that match the pattern
    for line in text_list:
        match = re.match(pattern, line)
        if match:
            # Extract date, name, and number from the match object
            date = match.group(1)
            date = datetime.strptime(date, "%m/%d/%Y")
            client = match.group(2)
            amount = float(match.group(3))
            transactions.append(Transaction(date, client, amount).to_dict())
    return jsonify(transactions)


@app.get("/total_transactional_cost")
def total_transactional_cost():
    transactions = [Transaction.from_dict(transaction) for transaction in request.get_json()["transactions"]]
    total_amount = 0.0
    for transaction in transactions:
        total_amount += transaction.amount
    return str(total_amount)


@app.get("/transactional_cost_timeframe")
def transactional_cost_timeframe():
    transactions = [Transaction.from_dict(transaction) for transaction in request.get_json()["transactions"]]
    initial_date = request.get_json()["initial_date"]
    end_date = request.get_json()["end_date"]
    # both input dates are string
    total_amount = 0.0
    initial_date = datetime.strptime(initial_date, "%m/%d/%Y")
    end_date = datetime.strptime(end_date, "%m/%d/%Y")
    for transaction in transactions:
        if initial_date <= transaction.date <= end_date:
            total_amount += transaction.amount
    return str(total_amount)


pdf_path = "Attachements/Bank-Statement-Template-4-TemplateLab.pdf"

# Extract images
images = extract_images_from_pdf(pdf_path)
print("Image saved")

# Extract text
text = extract_text_from_pdf(pdf_path)
