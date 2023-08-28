import imaplib
import email
import logging
from email.header import decode_header
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_email_content(message):
    content = ""

    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            if "text/plain" in content_type:
                content += part.get_payload(decode=True).decode()
    else:
        content = message.get_payload(decode=True).decode()

    return content

def authenticate_with_oauth():
    # Set up OAuth credentials
    flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', ['https://www.googleapis.com/auth/gmail.modify'])
    credentials = flow.run_local_server(port=0)
    return credentials

def main():
    # Authenticate with OAuth
    credentials = authenticate_with_oauth()

    email_address = "your_email@gmail.com"  # Update with your email address
    mailbox = "inbox"

    rejection_keywords = ["unfortunately", "we regret to inform", "not selected", "position has been filled"]

    try:
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.authenticate('XOAUTH2', lambda x: (email_address, credentials.token))
        mail.select(mailbox)

        # Search for emails matching the criteria
        status, email_ids = mail.search(None, "ALL")
        email_id_list = email_ids[0].split()

        # Loop through emails and process rejections
        for email_id in email_id_list:
            try:
                status, email_data = mail.fetch(email_id, "(RFC822)")
                raw_email = email_data[0][1]
                email_message = email.message_from_bytes(raw_email)

                subject = email_message["Subject"]
                content = get_email_content(email_message)

                is_rejection = any(keyword in subject.lower() or keyword in content.lower() for keyword in rejection_keywords)

                if is_rejection:
                    # Move the email to trash
                    mail.store(email_id, "+FLAGS", "\\Deleted")
                    logging.info(f"Marked rejection email with subject '{subject}' for deletion.")
            except Exception as e:
                logging.error(f"Error processing email ID {email_id}: {e}")

        # Permanently delete marked emails
        mail.expunge()

    except Exception as e:
        logging.error(f"Error during IMAP operations: {e}")
    finally:
        # Logout and close connection
        mail.logout()

if __name__ == "__main__":
    main()

