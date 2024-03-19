## Overview

![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fmchauhan3%2Fpypoller%2Fmaster%2Fpyproject.toml)
![GitHub License](https://img.shields.io/github/license/mchauhan3/pypoller)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pypoller)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/mchauhan3/pypoller)


pypoller is a lightweight and easy-to-use framework for polling a resource at regular intervals and providing notifications on any updates. It is designed to simplify the process of monitoring a remote service for changes and alerting users or systems when relevant updates occur.

Detailed docs available [here](https://www.mohitc.com/pypoller/docs/).

## Features

- **Polling**: The library allows you to define a polling interval, specifying how frequently the resource should be checked for updates.

- **Notifications**: When a change is detected in the service, the library supports customizable notification mechanisms.
- **Configurability**: The library is highly configurable and extensible. Adding support for any notification mechanism or resource should be seamless.

Currently implemented resource checkers:
- US Visa appointments
- Parks Canada campsites

Currently implemented notifiers:
- SMS (via Twilio)
- Rocket.Chat

All submodules can be used independently as well. For example, to check for availability of US Visa appointments:

```
UGANDA_EMBASSY = "en-ug"
SCHEDULE_ID = "50295138"
FACILITY_ID = "106"
USER_EMAIL = "user_email"
PASSWORD = "password"

# Initialize resource checker for US Visa availability
availability_checker = USVisaResourceChecker(
    UGANDA_EMBASSY, SCHEDULE_ID, FACILITY_ID, USER_EMAIL, PASSWORD
)

date_range_request = DateRangeRequest(
    start_date=dt.datetime(2024, 3, 14),
    end_date=dt.datetime(2025, 7, 1),
)

response = availability_checker.check_resource(date_range_request)
```

Modules of the same base type (`Notifier` / `ResourceChecker`) can be combined as well, for eg. 
```
us_visa_checker = USVisaResourceChecker(
    EMBASSY_ID, SCHEDULE_ID, FACILITY_ID, USER_EMAIL, PASSWORD
)

parks_canada_checker = ParksCanadaChecker(
    resource_id=GREEN_POINT_DRIVE_IN_CAMPSITES_ID,
    equipment_category_id=EQUIPMENT_CATEGORY_ID,
    sub_equipment_category_id=SUB_EQUIPMENT_CATEGORY_ID,
)

aggregate_checker = us_visa_checker + parks_canada_checker

date_range_request = DateRangeRequest(
    start_date=dt.datetime(2024, 3, 14),
    end_date=dt.datetime(2025, 7, 1),
)
response = aggregate_checker.check_resource(date_range_request)
```

This will check both resources with the input.

Similarly for notifiers:
```
twilio_notifier = TwilioSMSNotifier(
        twilio_account_sid,
        twilio_auth_token,
        twilio_phone_number
)

rocket_chat_notifier = RocketChatNotifier(
    user,
    password,
    server_url
)

aggregate_notifier = twilio_notifier + rocket_chat_notifier
aggregate_notifier.add_contacts([<LIST_OF_CONTACTS>])

aggregate_notifier.notify(new Message("test"))
```
This will send both (1) an SMS via twilio and (2) a rocket chat message.



## Installation

`pip install pypoller`

For playwrigt (US Visa):

`playwright install chromium`

## Usage
Refer to examples to learn how to use the library.

To provide twilio / rocketchat credentials for the examples, create a `.env` file by copying the `env.sample` file, and replace the placeholder parameters.
