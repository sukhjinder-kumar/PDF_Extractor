from flask import Flask, request, jsonify
import PyPDF2
import re
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


def filter_transactions(text):
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
            transactions.append(Transaction(date, client, amount))
    return transactions


def total_transactional_cost(transactions):
    total_amount = 0.0
    for transaction in transactions:
        total_amount += transaction.amount
    return total_amount


def transactional_cost_timeframe(transactions, initial_date, end_date):
    total_amount = 0.0
    initial_date = datetime.strptime(initial_date, "%m/%d/%Y")
    end_date = datetime.strptime(end_date, "%m/%d/%Y")
    for transaction in transactions:
        if initial_date <= transaction.date <= end_date:
            total_amount += transaction.amount
    return total_amount


pdf_path = "Attachements/Bank-Statement-Template-4-TemplateLab.pdf"
text = extract_text_from_pdf(pdf_path)
filter_transactions(text)

transactions = [
    Transaction(datetime.strptime("01/01/2023", "%m/%d/%Y"),"a" ,100.12),
    Transaction(datetime.strptime("02/15/2022", "%m/%d/%Y"),"a" ,150.50),
    Transaction(datetime.strptime("03/10/2023", "%m/%d/%Y"),"a" ,75.25),
    Transaction(datetime.strptime("04/20/2023", "%m/%d/%Y"),"a" ,200.30),
]

print(transactional_cost_timeframe(transactions, "02/10/2023", "03/15/2023"))
