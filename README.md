# poller-framework

## Overview

poller-framework is a lightweight and easy-to-use framework for polling a resource at regular intervals and providing notifications on any updates. It is designed to simplify the process of monitoring a remote service for changes and alerting users or systems when relevant updates occur.

## Features

- **Polling**: The library allows you to define a polling interval, specifying how frequently the service should be checked for updates.

- **Notifications**: When a change is detected in the service, the library supports customizable notification mechanisms. Currently messaging via Twilio is implemented.

- **Configurability**: The library is highly configurable and extensible. Adding support for any notification mechanism or resource should be seamless.
## Installation

## Usage
Create a `.env` file by copying the `.env.sample` file, and replace the placeholder twilio parameters to enable notifications via SMS.

For an example of how to use the library refer to `__main__.py`. Currently it is set up to poll the Parks Canada website every 30 seconds and notify users (provided via command line input) if there are any availabilities.

## Configuration


## License
