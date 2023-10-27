import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv

load_dotenv()
# account credentials
username = os.getenv('username')
password = os.getenv('password')
target_header = os.getenv("target_header")

# use your email provider's IMAP server, you can look for your provider's IMAP server on Google
# or check this page: https://www.systoolsgroup.com/imap/
# for gmail, it's this:
imap_server = "imap.gmail.com"

# create an IMAP4 class with SSL 
mail = imaplib.IMAP4_SSL(imap_server)
# authenticate
mail.login(username, password)
mail.select('Inbox')

# Search for emails with the specific header
search_query = f'SUBJECT "{target_header}"'
result, email_ids = mail.search(None, search_query)
# Get the list of email IDs that match the search query
email_id_list = email_ids[0].split()

if not email_id_list:
    print("No emails found with the specified header.")
else:
    # Loop through the matching emails and download the PDF attachments
    for email_id in email_id_list:
        # Fetch the email
        result, message_data = mail.fetch(email_id, "(RFC822)")
        raw_email = message_data[0][1]

        # Parse the email message
        msg = email.message_from_bytes(raw_email)

        # Check for attachments
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                continue
            filename = part.get_filename()

            if filename:
                # Decode the filename if needed
                filename = decode_header(filename)[0][0]
                if isinstance(filename, bytes):
                    filename = filename.decode('utf-8')

                # Check if the attachment is a PDF
                if filename.endswith(".pdf"):
                    # Save the PDF attachment to a file
                    filepath = 'Attachements/' + filename
                    with open(filepath, 'wb') as pdf_file:
                        pdf_file.write(part.get_payload(decode=True))
                    print(f"Downloaded the PDF attachment: {filename}")

# Logout and close the connection
mail.logout()
