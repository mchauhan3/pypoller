# pypoller

## Overview

pypoller is a lightweight and easy-to-use framework for polling a resource at regular intervals and providing notifications on any updates. It is designed to simplify the process of monitoring a remote service for changes and alerting users or systems when relevant updates occur.

Detailed docs available [here](https://www.mohitc.com/pypoller/docs/).

## Features

- **Polling**: The library allows you to define a polling interval, specifying how frequently the resource should be checked for updates.

- **Notifications**: When a change is detected in the service, the library supports customizable notification mechanisms. Currently messaging via Twilio is implemented.

- **Configurability**: The library is highly configurable and extensible. Adding support for any notification mechanism or resource should be seamless.

Currently implemented resource checkers:
- US Visa appointments
- Parks Canada campsites

Currently implemented notifier:
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
## Installation

`pip install pypoller`

For playwrigt (US Visa):

`playwright install chromium`

## Usage
Refer to examples to learn how to use the library.

To provide twilio / rocketchat credentials for the examples, create a `.env` file by copying the `env.sample` file, and replace the placeholder twilio parameters to enable notifications via SMS.
