from flask import Flask, request
import requests
import PyPDF2
from datetime import datetime


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


pdf_path = "Attachements/Bank-Statement-Template-4-TemplateLab.pdf"

# Extract text
text = extract_text_from_pdf(pdf_path)

################################################
# Test filter_transaction api
################################################

api_url = "http://127.0.0.1:5000/filter_transactions"

# Send a GET request to the Flask API
response = requests.get(api_url, json={"text": text})

if response.status_code == 200:
    # API call was successful, and the response contains Transaction objects
    transactions = [Transaction.from_dict(transaction) for transaction in response.json()]
    transactions2 = response.json()
    for transaction in transactions:
        print(f"Date: {transaction.date}, Client: {transaction.client}, Amount: {transaction.amount}")
else:
    print("API call failed with status code:", response.status_code)

################################################
# Test total_transactional_cost api
################################################

api_url = "http://127.0.0.1:5000/total_transactional_cost"

# Send a GET request to the Flask API
response = requests.get(api_url, json={"transactions": transactions2})

if response.status_code == 200:
    # API call was successful, and the response contains Transaction objects
    total_amount = response.json()
    print(total_amount)
else:
    print("API call failed with status code:", response.status_code)

################################################
# Test transactional_cost_timeframe
################################################

api_url = "http://127.0.0.1:5000/transactional_cost_timeframe"

# Send a GET request to the Flask API
initial_date = "02/10/2023"
end_date = "12/24/2023"
response = requests.get(api_url, json={"transactions": transactions2,
                                       "initial_date": initial_date,
                                       "end_date": end_date})

if response.status_code == 200:
    # API call was successful, and the response contains Transaction objects
    total_amount = response.json()
    print(total_amount)
else:
    print("API call failed with status code:", response.status_code)
