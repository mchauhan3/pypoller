from dataclasses import dataclass, field
from playwright.sync_api import sync_playwright, Playwright, expect
from . import ResourceChecker
from .request import DateRangeRequest
from .response import Response
from pypoller.messaging import Message
from pypoller.util.decorators import non_null_args
from typing import List
import datetime as dt
import json

# JavaScript block for making the request to get availabile dates
JS_SCRIPT = (
    "() => {"
    "var req = new XMLHttpRequest();"
    "req.open('GET', '%s', false);"
    "req.setRequestHeader('Accept', 'application/json, text/javascript, */*; q=0.01');"
    "req.setRequestHeader('X-Requested-With', 'XMLHttpRequest');"
    "req.send(null);"
    "return req.responseText;"
    "};"
)


DATE_FORMAT = "%Y-%m-%d"


@dataclass
class USVisaResponse(Response):
    """
    Response class for US Visa availability check.
    """

    available_dates: List[str] = field(default_factory=lambda: [])

    def to_message(self) -> Message:
        """
        Convert the response to a message format.

        Returns:
            Message: The message containing the response body.
        """
        if self.error:
            return Message(is_error=True, body=self.error.__str__())

        if not self.available_dates:
            return Message()

        message_body = f"Found dates for US Visa: {[d.strftime(DATE_FORMAT) for d in self.available_dates]}"

        return Message(body=message_body)


class USVisaResourceChecker(ResourceChecker):
    """
    Resource checker for US Visa availability.
    """

    @non_null_args
    def __init__(self, embassy_id, schedule_id, facility_id, user_email, password):
        """
        Initialize the US Visa Resource Checker.

        Args:
            embassy_id (str): ID of the embassy.
            schedule_id (str): ID of the schedule.
            facility_id (str): ID of the facility.
            user_email (str): User email for authentication.
            password (str): Password for authentication.
        """
        self.dates_url = f"https://ais.usvisa-info.com/{embassy_id}/niv/schedule/{schedule_id}/appointment/days/{facility_id}.json?appointments[expedite]=false"
        self.sign_in_url = f"https://ais.usvisa-info.com/{embassy_id}/niv/users/sign_in"
        self.user_email = user_email
        self.password = password

    def check_resource(self, date_range: DateRangeRequest):
        """
        Check the availability of US Visa appointments within the given date range.

        Args:
            date_range (DateRangeRequest): The date range for which appointments are to be checked.

        Returns:
            USVisaResponse: The response containing available dates.
        """
        available_dates = []

        def run(playwright: Playwright):
            chromium = playwright.chromium
            browser = chromium.launch()
            page = browser.new_page()
            page.goto(self.sign_in_url)
            page.get_by_label("Email").fill(self.user_email)
            page.get_by_label("Password").fill(self.password)
            page.locator(".icheckbox").click()
            page.get_by_role("button", name="Sign in").click()
            expect(page.get_by_text("Continue")).to_be_visible()
            resp = page.evaluate(JS_SCRIPT % self.dates_url)
            resp = json.loads(resp)
            for d in resp:
                date = d["date"]
                date = dt.datetime.strptime(date, DATE_FORMAT)
                if date >= date_range.start_date and date <= date_range.end_date:
                    available_dates.append(date)

            browser.close()

        with sync_playwright() as playwright:
            try:
                run(playwright)
            except Exception as e:
                return USVisaResponse(error=e)

        return USVisaResponse(available_dates=available_dates)
