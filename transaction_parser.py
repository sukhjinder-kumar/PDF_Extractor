import re
from datetime import datetime


class Transaction:
    def __init__(self, date, client, amount):
        self.date = date  # datetime object
        self.client = client
        self.amount = amount


def filter_transactions(text):
    '''Takes text and Returns a list of Transaction objects'''
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
    # both input dates are string
    total_amount = 0.0
    initial_date = datetime.strptime(initial_date, "%m/%d/%Y")
    end_date = datetime.strptime(end_date, "%m/%d/%Y")
    for transaction in transactions:
        if initial_date <= transaction.date <= end_date:
            total_amount += transaction.amount
    return total_amount


text_path = "Output/Text/pdf_text.txt"
text = ""

with open(text_path, "r") as file:
    text = file.read()

transactions = filter_transactions(text)
for transaction in transactions:
    print(f"{transaction.date} {transaction.client} {transaction.amount}")

print(total_transactional_cost(transactions))
initial_date = "02/11/2021"
end_date = "02/11/2023"
print(transactional_cost_timeframe(transactions, initial_date, end_date))
