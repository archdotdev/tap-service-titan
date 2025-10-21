"""Tests standard tap features using the built-in SDK tests library."""

import datetime
from os import environ

import dotenv
from singer_sdk.testing import SuiteConfig, get_tap_test_class

from tap_service_titan.tap import TapServiceTitan

dotenv.load_dotenv()

SAMPLE_CONFIG = {
    # "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    "start_date": "2025-06-01",
    "client_id": environ["TAP_SERVICE_TITAN_CLIENT_ID"],
    "client_secret": environ["TAP_SERVICE_TITAN_CLIENT_SECRET"],
    "st_app_key": environ["TAP_SERVICE_TITAN_ST_APP_KEY"],
    "tenant_id": environ["TAP_SERVICE_TITAN_TENANT_ID"],
    # "api_url": "https://api-integration.servicetitan.io",
    # "auth_url": "https://auth-integration.servicetitan.io/connect/token",
}


# Run standard built-in tap tests from the SDK:
TestTapServiceTitan = get_tap_test_class(
    tap_class=TapServiceTitan,
    config=SAMPLE_CONFIG,
    suite_config=SuiteConfig(
        max_records_limit=25,
    ),
    # Enable these to run the tests
    # include_stream_attribute_tests=False,
    # include_stream_tests=False,
    # include_tap_tests=False,
)
