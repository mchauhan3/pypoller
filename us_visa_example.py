from poller import Poller
from resource import USVisaResourceChecker
from resource.request import DateRangeRequest
from messaging import Contact, TwilioSMSNotifier, ConsoleNotifier, TryNextOnFailNotifier
import datetime as dt
from dotenv import load_dotenv
from util.constants import (
	TWILIO_AUTH_TOKEN_KEY, TWILIO_PHONE_NUMBER_KEY, TWILIO_ACCOUNT_SID_KEY)
import os

# change for your use
UGANDA_EMBASSY = "en-ug"
SCHEDULE_ID = "50295138"
FACILITY_ID = "106"
USER_EMAIL = "user_email"
PASSWORD = "password"

availability_checker = USVisaResourceChecker(UGANDA_EMBASSY, SCHEDULE_ID, FACILITY_ID, USER_EMAIL, PASSWORD)

load_dotenv()
notifier = None

try:
	twilio_account_sid = os.getenv(TWILIO_ACCOUNT_SID_KEY)
	twilio_auth_token = os.getenv(TWILIO_AUTH_TOKEN_KEY)
	twilio_phone_number = os.getenv(TWILIO_PHONE_NUMBER_KEY)

	notifier = TwilioSMSNotifier(twilio_account_sid, twilio_auth_token, twilio_phone_number)
except ValueError as e:
	print(e)
	print("Twilio arguments not provided, using console notifier")
	notifier = ConsoleNotifier()

def configure_contacts():
	contacts = []
	add_contact = input("Add contact? Y/N \n")
	while add_contact == "Y":
		name = input("Contact name? \n")
		phone_number = input("Phone number? \n")
		email = input("Email?")
		notify_error = input("Should be notified on errors? Y/N \n") == "Y"
		contacts.append(Contact(name, phone_number, email, notify_error))
		print("Added contact!")
		add_contact = input("Add another contact? Y/N \n")
		contacts.append(add_contact)
	return contacts

if not (isinstance(notifier, ConsoleNotifier)):
	notifier.add_contacts(configure_contacts())
	notifier = TryNextOnFailNotifier([notifier, ConsoleNotifier()])

poller = Poller(availability_checker, notifier)

date_range_request = DateRangeRequest(
	start_date=dt.datetime(2024, 3, 14),
	end_date=dt.datetime(2024, 7, 1),
)
poller.poll(date_range_request, 300)