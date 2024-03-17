# change for your use
from pypoller.messaging.contact import RCContact
from pypoller.poller import Poller
from pypoller.resource import USVisaResourceChecker
from pypoller.resource.request import DateRangeRequest
from pypoller.messaging import RocketChatNotifier
import datetime as dt
from dotenv import load_dotenv
import os

load_dotenv()

UGANDA_EMBASSY = "en-ug"
SCHEDULE_ID = "50295138"
FACILITY_ID = "106"
USER_EMAIL = "user_email"
PASSWORD = "password"

# Initialize resource checker for US Visa availability
availability_checker = USVisaResourceChecker(
    UGANDA_EMBASSY, SCHEDULE_ID, FACILITY_ID, USER_EMAIL, PASSWORD
)

notifier = RocketChatNotifier(
    user=os.getenv("RC_USER"),
    password=os.getenv("RC_PASS"),
    server_url=os.getenv("RC_SERVER"),
)

notifier.add_contact(RCContact(name="visa-updates", channel="visa-updates"))

date_range_request = DateRangeRequest(
    start_date=dt.datetime(2024, 3, 14),
    end_date=dt.datetime(2025, 7, 1),
)

# Start polling with specified frequency
Poller(availability_checker, notifier).poll(date_range_request, 300)
