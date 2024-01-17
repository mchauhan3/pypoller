import requests
import json

from checker import AvailabilityChecker
from util.decorators import non_null_args, add_pre_delay

BOOKING_CATEGORY_ID = "0"
EQUIPMENT_CATEGORY_ID = "-32768"
SUB_EQUIPMENT_CATEGORY_ID = "-32767"
PARKS_CANADA_URL = "https://reservation.pc.gc.ca/api/availability/map"


class ParksCanadaAvailabilityChecker(AvailabilityChecker):

	def __init__(self, resource_id):
		self.resource_id = resource_id

	@non_null_args
	@add_pre_delay(delay=1)
	def check_availability(self, date_range):
		start_date, end_date = date_range
		request_parameters = {'mapId': self.resource_id, 'bookingCategoryId': BOOKING_CATEGORY_ID,
							  'equipmentCategoryId': EQUIPMENT_CATEGORY_ID,
							  'subEquipmentCategoryId': SUB_EQUIPMENT_CATEGORY_ID,
							  'startDate': start_date, 'endDate': end_date, 'getDailyAvailability': "false",
							  'isReserving': "true", 'partySize': "6"}

		response = requests.get(PARKS_CANADA_URL, params=request_parameters).content
		response = json.loads(response)
		campsites = response['resourceAvailabilities']

		for campsite in campsites.values():

			for d in campsite:
				if d['availability'] == 0:
					print("Found campsite for date range: {}".format(date_range))
					return True

		return False
