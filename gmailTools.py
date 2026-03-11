import os.path, base64
from agent_framework import tool
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from email.message import EmailMessage
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Change from .readonly to .send (or include both)
SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.readonly']


def _get_credentials():
    """Internal helper to handle Gmail authentication."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # This is where the browser login is triggered
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

@tool(approval_mode="never_require")
def read_emails(max_results: int = 20):
    """Accesses Gmail and returns the 20 most recent emails."""
    
    print("DEBUG: [Step 1] read_emails function has been TRIGGERED by the agent.") # <--- ADD THIS

    creds = _get_credentials() # Reuse the logic
    print("DEBUG: [Step 2] Credentials acquired successfully.") # <--- ADD THIS
    service = build('gmail', 'v1', credentials=creds)
    
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])

    print(f"DEBUG: [Step 3] Found {len(messages)} emails.") # <--- ADD THIS

    email_list = []
    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = txt['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
        sender = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown Sender")
        email_list.append({"from": sender, "subject": subject})
    
    return email_list


@tool(approval_mode="never_require")
def send_gmail_message(recipient: str, subject: str, body: str):
    """Sends an email and returns a confirmation message."""
    creds = _get_credentials() # Reuse the logic
    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()
        message.set_content(body)
        message['To'] = recipient
        message['From'] = 'me'
        message['Subject'] = subject

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        send_receipt = service.users().messages().send(userId="me", body={'raw': encoded_message}).execute()
        return f"Email sent successfully! Message ID: {send_receipt['id']}"
    except Exception as error:
        return f"An error occurred: {error}"