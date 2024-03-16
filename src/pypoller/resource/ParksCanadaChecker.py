import datetime as dt
import json
from dataclasses import dataclass, field
from typing import List

import requests

from pypoller.messaging import Message
from pypoller.util.decorators import non_null_args, add_pre_delay
from . import ResourceChecker
from .request import DateRangeRequest
from .response import Response

DEFAULT_BOOKING_CATEGORY_ID = "0"
PARKS_CANADA_URL = "https://reservation.pc.gc.ca/api/availability/map"

IS_AVAILABLE = 0


@dataclass
class ParksCanadaResponse(Response):
    """
    Response class for Parks Canada campsite availability check.
    """

    available_sites: List[str] = field(default_factory=list)
    start_date: str = ""
    end_date: str = ""
    name_override: str = None

    def to_message(self) -> Message:
        """
        Convert the response to a message format.

        Returns:
            Message: The message containing the response body.
        """
        if self.error:
            return Message(is_error=True, body=self.error.__str__())

        if not self.available_sites:
            return Message()

        values = self.name_override if self.name_override else self.available_sites

        message_body = (
            f"Found campsites: {values} for dates: {self.start_date} to {self.end_date}"
        )

        return Message(body=message_body)


class ParksCanadaChecker(ResourceChecker):
    """
    Resource checker for Parks Canada campsite availability.
    """

    def __init__(
        self,
        resource_id: str,
        booking_category_id: str = DEFAULT_BOOKING_CATEGORY_ID,
        equipment_category_id: str = None,
        sub_equipment_category_id: str = None,
        name_override: str = None,
    ) -> None:
        """
        Initialize the Parks Canada campsite checker.

        Args:
            resource_id (str): The ID of the resource.
            booking_category_id (str): The booking category ID. Default is "0".
            equipment_category_id (str): The equipment category ID. Default is None.
            sub_equipment_category_id (str): The sub-equipment category ID. Default is None.
            name_override (str): An optional name override for the campsite. Default is None.
        """
        self.booking_category_id = booking_category_id
        self.sub_equipment_category_id = sub_equipment_category_id
        self.equipment_category_id = equipment_category_id
        self.resource_id = resource_id
        self.name_override = name_override

    @non_null_args
    @add_pre_delay(delay=1)
    def check_resource(self, date_range: DateRangeRequest) -> ParksCanadaResponse:
        """
        Check the availability of Parks Canada campsites within the given date range.

        Args:
            date_range (DateRangeRequest): The date range for which campsites are to be checked.

        Returns:
            ParksCanadaResponse: The response containing available campsites.
        """
        start_date, end_date = (
            self.format_date(date_range.start_date),
            self.format_date(date_range.end_date),
        )
        request_parameters = {
            "mapId": self.resource_id,
            "bookingCategoryId": self.booking_category_id,
            "equipmentCategoryId": self.equipment_category_id,
            "subEquipmentCategoryId": self.sub_equipment_category_id,
            "startDate": start_date,
            "endDate": end_date,
            "getDailyAvailability": "false",
            "isReserving": "true",
            "partySize": "6",
        }

        try:
            response = requests.get(PARKS_CANADA_URL, params=request_parameters)
            response = json.loads(response.content)
            campsites = response["resourceAvailabilities"]
        except Exception as e:
            return ParksCanadaResponse(error=e)

        available_sites = []

        for i, campsite in enumerate(campsites.values()):
            for d in campsite:
                if d["availability"] == IS_AVAILABLE:
                    print(f"Found campsite {i + 1} for date range: {date_range}")
                    available_sites.append(str(i + 1))

        return ParksCanadaResponse(
            available_sites=available_sites,
            start_date=start_date,
            end_date=end_date,
            name_override=self.name_override,
        )

    @staticmethod
    def format_date(date: dt.datetime) -> str:
        """
        Format the date in the required string format.

        Args:
            date (dt.datetime): The date to be formatted.

        Returns:
            str: The formatted date string.
        """
        return f"{date.year}-{date.month}-{date.day}"
