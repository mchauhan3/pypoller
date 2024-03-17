from pypoller.messaging.contact import PhoneContact
from pypoller.poller import Poller
from pypoller.resource import USVisaResourceChecker
from pypoller.resource.request import DateRangeRequest
from pypoller.messaging import (
    TwilioSMSNotifier,
    ConsoleNotifier,
    TryNextOnFailNotifier,
)
import datetime as dt
from dotenv import load_dotenv
import os

# change for your use
UGANDA_EMBASSY = "en-ug"
SCHEDULE_ID = "50295138"
FACILITY_ID = "106"
USER_EMAIL = "user_email"
PASSWORD = "password"

# Initialize resource checker for US Visa availability
availability_checker = USVisaResourceChecker(
    UGANDA_EMBASSY, SCHEDULE_ID, FACILITY_ID, USER_EMAIL, PASSWORD
)

# Load Twilio credentials from environment variables
load_dotenv()
notifier = None

TWILIO_ACCOUNT_SID_KEY = "TWILIO_ACCOUNT_SID"
TWILIO_AUTH_TOKEN_KEY = "TWILIO_AUTH_TOKEN"
TWILIO_PHONE_NUMBER_KEY = "TWILIO_PHONE_NUMBER"

try:
    # Attempt to initialize Twilio notifier
    twilio_account_sid = os.getenv(TWILIO_ACCOUNT_SID_KEY)
    twilio_auth_token = os.getenv(TWILIO_AUTH_TOKEN_KEY)
    twilio_phone_number = os.getenv(TWILIO_PHONE_NUMBER_KEY)

    notifier = TwilioSMSNotifier(
        twilio_account_sid, twilio_auth_token, twilio_phone_number
    )
except Exception as e:
    # If Twilio initialization fails, fall back to using ConsoleNotifier
    print(e)
    print("Could not initialize Twilio Client, using ConsoleNotifier")
    notifier = ConsoleNotifier()


def configure_contacts():
    contacts = []
    add_contact = input("Add contact? Y/N \n")
    while add_contact == "Y":
        # Collect contact information from user input
        name = input("Contact name? \n")
        phone_number = input("Phone number? \n")
        notify_error = input("Should be notified on errors? Y/N \n") == "Y"
        # Create Contact object and append to contacts list
        contacts.append(
            PhoneContact(
                name=name, phone_number=phone_number, notify_error=notify_error
            )
        )
        print("Added contact!")
        # Prompt user to add another contact
        add_contact = input("Add another contact? Y/N \n")
    return contacts


if not (isinstance(notifier, ConsoleNotifier)):
    # If notifier is not ConsoleNotifier, configure contacts and use TryNextOnFailNotifier
    notifier.add_contacts(configure_contacts())
    notifier = TryNextOnFailNotifier([notifier, ConsoleNotifier()])

# Initialize Poller with resource checker and notifier
poller = Poller(availability_checker, notifier)

# Define date range for polling
date_range_request = DateRangeRequest(
    start_date=dt.datetime(2024, 3, 14),
    end_date=dt.datetime(2025, 7, 1),
)

# Start polling with specified frequency
poller.poll(date_range_request, 300)
