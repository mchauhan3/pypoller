import os
from dotenv import load_dotenv

from pypoller.poller import Poller
from pypoller.resource import ParksCanadaChecker
from pypoller.resource.request import DateRangeRequest
from pypoller.messaging import (
    TwilioSMSNotifier,
    ConsoleNotifier,
    TryNextOnFailNotifier,
)
from pypoller.messaging.contact import PhoneContact
import datetime as dt

# Load environment variables from .env file
load_dotenv()
notifier = None

TWILIO_ACCOUNT_SID_KEY = "TWILIO_ACCOUNT_SID"
TWILIO_AUTH_TOKEN_KEY = "TWILIO_AUTH_TOKEN"
TWILIO_PHONE_NUMBER_KEY = "TWILIO_PHONE_NUMBER"

try:
    # Try to initialize Twilio notifier using environment variables
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

# Define constants for equipment and booking IDs
EQUIPMENT_CATEGORY_ID = "-32768"
SUB_EQUIPMENT_CATEGORY_ID = "-32767"
PARKS_CANADA_ACCOMMODATION_BOOKING_ID = "1"
GREEN_POINT_DRIVE_IN_CAMPSITES_ID = "-2147483314"
GREEN_POINT_WALK_IN_CAMPSITES_ID = "-2147483313"


# Initialize ParksCanadaChecker instances for drive-in and otentik campsites
drive_in_availability_checker = ParksCanadaChecker(
    resource_id=GREEN_POINT_DRIVE_IN_CAMPSITES_ID,
    equipment_category_id=EQUIPMENT_CATEGORY_ID,
    sub_equipment_category_id=SUB_EQUIPMENT_CATEGORY_ID,
)

otentik_availability_checker = ParksCanadaChecker(
    resource_id=GREEN_POINT_WALK_IN_CAMPSITES_ID,
    booking_category_id=PARKS_CANADA_ACCOMMODATION_BOOKING_ID,
    name_override="Otentik",
)

# Combine availability checkers for both types of campsites
availability_checker = drive_in_availability_checker + otentik_availability_checker


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

# Initialize Poller with availability checker and notifier
poller = Poller(availability_checker, notifier)

# Define date range for polling
date_range_request = DateRangeRequest(
    start_date=dt.datetime(2024, 8, 1),
    end_date=dt.datetime(2024, 8, 5),
)

# Start polling
poller.poll(date_range_request)
