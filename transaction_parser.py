import re

text_path = "Output/Text/pdf_text.txt"
text = ""

with open(text_path, "r") as file:
    text = file.read()

print(text)
text_list = text.splitlines()  # Contains list of lines

# Define the pattern to match the structure
pattern = r'\d{2}/\d{2}/\d{4} .+ \d+\.\d+'

# Filter lines that match the pattern
filtered_lines = [line for line in text_list if re.match(pattern, line)]

# Print the filtered lines
for line in filtered_lines:
    print(line)
