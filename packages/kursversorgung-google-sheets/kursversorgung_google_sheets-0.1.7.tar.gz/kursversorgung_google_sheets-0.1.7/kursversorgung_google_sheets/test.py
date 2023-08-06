from dotenv import load_dotenv
from accessOutlookEmail import create_account, send_email
import os

load_dotenv()

# v = create_account(os.getenv('email_valentin'), os.getenv('password_valentin'))
print(type(os.getenv('email_valentin')))
