"""CRM streams for the ServiceTitan tap."""

from __future__ import annotations

import typing as t
from urllib.parse import urlparse
from http import HTTPStatus
import time
from functools import cached_property
from singer_sdk.authenticators import SingletonMeta
import requests
from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
from singer_sdk.exceptions import FatalAPIError
import datetime
import threading
import atexit
from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk.streams import RESTStream
from tap_service_titan.client import ServiceTitanExportStream, ServiceTitanStream


# CRM Streams
class BookingProviderTagsStream(ServiceTitanStream):
    """Define booking provider tags stream."""

    name = "booking_provider_tags"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("tagName", th.StringType),
        th.Property("description", th.StringType),
        th.Property("type", th.StringType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self._tap.config['tenant_id']}/booking-provider-tags"


class BookingsStream(ServiceTitanExportStream):
    """Define bookings stream."""

    name = "bookings"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("source", th.StringType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("name", th.StringType),
        th.Property(
            "address",
            th.ObjectType(
                th.Property("street", th.StringType),
                th.Property("unit", th.StringType),
                th.Property("city", th.StringType),
                th.Property("state", th.StringType),
                th.Property("zip", th.StringType),
                th.Property("country", th.StringType),
            ),
        ),
        th.Property(
            "customerType", th.StringType
        ),  # Enum values are actually treated as strings
        th.Property("start", th.DateTimeType),
        th.Property("summary", th.StringType),
        th.Property("campaignId", th.IntegerType),
        th.Property("businessUnitId", th.IntegerType),
        th.Property("isFirstTimeClient", th.BooleanType),
        th.Property("uploadedImages", th.ArrayType(th.StringType)),
        th.Property("isSendConfirmationEmail", th.BooleanType),
        th.Property(
            "status", th.StringType
        ),  # Enum values are actually treated as strings
        th.Property("dismissingReasonId", th.IntegerType),
        th.Property("jobId", th.IntegerType),
        th.Property("externalId", th.StringType),
        th.Property(
            "priority", th.StringType
        ),  # Enum values are actually treated as strings
        th.Property("jobTypeId", th.IntegerType),
        th.Property("bookingProviderId", th.IntegerType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self._tap.config['tenant_id']}/export/bookings"


class CustomersStream(ServiceTitanExportStream):
    """Define customers stream."""

    name = "customers"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("active", th.BooleanType),
        th.Property("name", th.StringType),
        th.Property("type", th.StringType),  # Enum values are treated as strings
        th.Property(
            "address",
            th.ObjectType(
                th.Property("street", th.StringType),
                th.Property("unit", th.StringType),
                th.Property("city", th.StringType),
                th.Property("state", th.StringType),
                th.Property("zip", th.StringType),
                th.Property("country", th.StringType),
                th.Property("latitude", th.NumberType),
                th.Property("longitude", th.NumberType),
            ),
        ),
        th.Property(
            "customFields",
            th.ArrayType(
                th.ObjectType(
                    th.Property("typeId", th.IntegerType),
                    th.Property("name", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
        th.Property("balance", th.NumberType),
        th.Property("tagTypeIds", th.ArrayType(th.IntegerType)),
        th.Property("doNotMail", th.BooleanType),
        th.Property("doNotService", th.BooleanType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("createdById", th.IntegerType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("mergedToId", th.IntegerType),
        th.Property(
            "externalData",
            th.ArrayType(
                th.ObjectType(
                    th.Property("key", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self._tap.config['tenant_id']}/export/customers"

    def get_child_context(self, record: dict, context: dict | None) -> dict:
        """Return a context dictionary for a child stream."""
        return {"customer_id": record["id"]}


class CustomerNotesStream(ServiceTitanStream):
    """Define customer notes stream."""

    name = "customer_notes"
    primary_keys: t.ClassVar[list[str]] = ["createdById", "createdOn"]
    replication_key: str = "modifiedOn"
    parent_stream_type = CustomersStream
    ignore_parent_replication_key = True

    schema = th.PropertiesList(
        th.Property("text", th.StringType),
        th.Property("isPinned", th.BooleanType),
        th.Property("createdById", th.IntegerType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self._tap.config['tenant_id']}/customers/{'{customer_id}'}/notes"  # noqa: E501


class CustomerContactsStream(ServiceTitanExportStream):
    """Define contacts stream."""

    name = "customer_contacts"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("modifiedOn", th.DateTimeType),
        th.Property(
            "phoneSettings",
            th.ObjectType(
                th.Property("phoneNumber", th.StringType),
                th.Property("doNotText", th.BooleanType),
            ),
        ),
        th.Property("id", th.IntegerType),
        th.Property("type", th.StringType),  # Enum values are treated as strings
        th.Property("value", th.StringType),
        th.Property("memo", th.StringType),
        th.Property("customerId", th.IntegerType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return (
            f"/crm/v2/tenant/{self._tap.config['tenant_id']}/export/customers/contacts"
        )
class CookieAuthenticator(metaclass=SingletonMeta):
    COOKIE_EXPIRATION = 10 * 60  # 10 minutes in seconds, TODO use the expire time from the cookie

    def __init__(self, stream):
        """
        Initialize the authenticator with the tap's configuration.

        Args:
            stream: The stream instance containing configuration.
        """
        self.stream = stream
        self.config = stream.config or {}
        self.login_endpoint = self.config.get("internal_login_url")
        if not self.login_endpoint:
            raise ValueError("Missing login endpoint configuration ('login_endpoint').")
        self.username = self.config.get("internal_username")
        self.password = self.config.get("internal_password")
        if not self.username or not self.password:
            raise ValueError("Username and password must be provided.")
        self.cookies = None
        self.last_login = None
        self._login_lock = threading.Lock()  # Lock to guard login so we only have 1 thread logging in at a time

        # Register the logout method to be called on process exit.
        atexit.register(self.logout)

    def login(self) -> None:
        """
        Uses Playwright to login and retrieve cookies from the browser session.
        This method will only perform login once, guarded by a thread lock.
        """
        with sync_playwright() as p:
            self.stream.logger.info(f"Logging in to {self.login_endpoint}")
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent=UserAgent().chrome)
            context.tracing.start(screenshots=True, snapshots=True, sources=True)
            page = context.new_page()
            page.goto(self.login_endpoint)
            page.fill("input[name='Username']", self.username)
            page.click("button[value='ContinueLogin']")
            page.fill("input[name='Password']", self.password)
            page.click("button[value='login']")
            page.click('h3:has-text("My Tenants")', timeout=30000)
            page.goto(self.config["internal_cookie_set_url"])  # Would be better to just click the Sign In link then having to set this URL
            # Need to wait for page to load, can't use network_idle as it never stops
            try:
                settings = page.locator("[title='Settings']") #Settings
                settings.wait_for()
            except:
                pass
            self.cookies = context.cookies()
            self.last_login = datetime.datetime.utcnow()
            context.tracing.stop(path="trace.zip")
            browser.close()

    def authenticate_request(self, request: requests.PreparedRequest) -> requests.PreparedRequest:
        """
        Attach valid cookies to the request. If the current cookie is invalid,
        re-authenticate first.
        """
        with self._login_lock: # Lock to guard login so we only have 1 thread logging in at a time
            if self.last_login is None or datetime.datetime.utcnow() > self.last_login + datetime.timedelta(seconds=self.COOKIE_EXPIRATION):
                self.login()
        request.headers["Cookie"] = "; ".join(
            [f"{cookie['name']}={cookie['value']}" for cookie in self.cookies]
        )
        self.stream.logger.info(f"{len(request.headers['Cookie'].split(';'))=}")
        return request

    def __call__(self, request: requests.PreparedRequest) -> requests.PreparedRequest:
        return self.authenticate_request(request)
    
    def logout(self) -> None:
        """
        Log out from the Workwave session by calling the logout endpoint. This helps
        free up sessions on the Workwave API once the tap finishes.
        """
        if not self.cookies:
            return
        cookie_header = "; ".join(
            [f"{cookie['name']}={cookie['value']}" for cookie in self.cookies]
        )
        headers = {"Cookie": cookie_header}
        logout_url = "https://enterprise-hub.servicetitan.com/api/v1/account/logout"
        try:
            response = requests.get(logout_url, headers=headers)
            if response.ok:
                self.stream.logger.info("Successfully logged out via %s", logout_url)
            else:
                self.stream.logger.warning(
                    "Logout request failed with status %s: %s",
                    response.status_code,
                    response.text,
                )
        except Exception as e:
            self.stream.logger.error("Error occurred during logout: %s", e)
        self.cookies = None
        self.last_login = None

    @classmethod
    def create_for_stream(cls, stream: RESTStream) -> CookieAuthenticator:
        return cls(stream=stream)

class CustomerAttachmentsStream(RESTStream):
    """Define customer attachments stream."""

    name = "customer_attachment"
    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["internal_api_url"]

    path = "/Customer/GetNonImageOrVideoAttachments/{customer_id}"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = None
    parent_stream_type = CustomersStream
    records_jsonpath = "$.Attachments[*]"
    @property
    def authenticator(self) -> CookieAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return CookieAuthenticator.create_for_stream(self)

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("filename", th.StringType),
        th.Property("originalFilename", th.StringType),
        th.Property("title", th.StringType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("createdBy", th.StringType),
        th.Property("jobId", th.IntegerType),
        th.Property("jobNumber", th.StringType),
        th.Property("projectId", th.IntegerType),
        th.Property("projectNumber", th.StringType),
        th.Property("isImageOrVideo", th.BooleanType),
        th.Property("paymentInvoiceId", th.IntegerType),
        th.Property("paymentInvoiceNumber", th.StringType),
        th.Property("isAdvancePayment", th.BooleanType),
        th.Property("isPaymentAttachment", th.BooleanType),
        th.Property("customerId", th.IntegerType),
    ).to_dict()
    
    def validate_response(self, response: requests.Response) -> None:
        if "<title>Login | ServiceTitan</title>" in response.text:
            raise FatalAPIError("Not logged in, properly")
        super().validate_response(response)

    def response_error_message(self, response: requests.Response) -> str:
        """Build error message for invalid http statuses.

        WARNING - Override this method when the URL path may contain secrets or PII

        Args:
            response: A :class:`requests.Response` object.

        Returns:
            str: The error message
        """
        full_path = urlparse(response.url).path or self.path
        error_type = (
            "Client"
            if HTTPStatus.BAD_REQUEST
            <= response.status_code
            < HTTPStatus.INTERNAL_SERVER_ERROR
            else "Server"
        )

        return (
            f"{response.status_code} {error_type} Error: "
            f"{response.reason} for path: {full_path}. "
            f"{response.text=}."
            f"{len(response.request.headers['Cookie'].split(';'))=}"
        )

class CustomerImageAttachmentsStream(RESTStream):
    """Define customer image attachments stream."""

    name = "customer_image_attachment"
    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["internal_api_url"]

    path = "/app/api/fam/attachments/3/{customer_id}"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    records_jsonpath = "$.Attachments[*]"
    
    replication_key: str = None
    parent_stream_type = CustomersStream
    @property
    def authenticator(self) -> CookieAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return CookieAuthenticator.create_for_stream(self)

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("filename", th.StringType),
        th.Property("originalFilename", th.StringType),
        th.Property("title", th.StringType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("createdBy", th.StringType),
        th.Property("jobId", th.IntegerType),
        th.Property("jobNumber", th.StringType),
        th.Property("projectId", th.IntegerType),
        th.Property("projectNumber", th.StringType),
        th.Property("isImageOrVideo", th.BooleanType),
        th.Property("paymentInvoiceId", th.IntegerType),
        th.Property("paymentInvoiceNumber", th.StringType),
        th.Property("isAdvancePayment", th.BooleanType),
        th.Property("isPaymentAttachment", th.BooleanType),
        th.Property("customerId", th.IntegerType),
    ).to_dict()
    
    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,  # noqa: ANN401
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        return {"limit": 1000, "photosVideosOnly": True, "includeRelatedEntities": False}
    
    def validate_response(self, response: requests.Response) -> None:
        if "<title>Login | ServiceTitan</title>" in response.text:
            raise FatalAPIError("Not logged in, properly")
        super().validate_response(response)

    def response_error_message(self, response: requests.Response) -> str:
        """Build error message for invalid http statuses.

        WARNING - Override this method when the URL path may contain secrets or PII

        Args:
            response: A :class:`requests.Response` object.

        Returns:
            str: The error message
        """
        full_path = urlparse(response.url).path or self.path
        error_type = (
            "Client"
            if HTTPStatus.BAD_REQUEST
            <= response.status_code
            < HTTPStatus.INTERNAL_SERVER_ERROR
            else "Server"
        )

        return (
            f"{response.status_code} {error_type} Error: "
            f"{response.reason} for path: {full_path}. "
            f"{response.text=}."
            f"{len(response.request.headers['Cookie'].split(';'))=}"
        )

class LeadsStream(ServiceTitanExportStream):
    """Define leads stream."""

    name = "leads"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("status", th.StringType),  # Enum values are treated as strings
        th.Property("customerId", th.IntegerType),
        th.Property("locationId", th.IntegerType),
        th.Property("businessUnitId", th.IntegerType),
        th.Property("jobTypeId", th.IntegerType),
        th.Property("priority", th.StringType),  # Enum values are treated as strings
        th.Property("campaignId", th.IntegerType),
        th.Property("summary", th.StringType),
        th.Property("callReasonId", th.IntegerType),
        th.Property("callId", th.IntegerType),
        th.Property("bookingId", th.IntegerType),
        th.Property("manualCallId", th.IntegerType),
        th.Property("followUpDate", th.DateTimeType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("createdById", th.IntegerType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("tagTypeIds", th.ArrayType(th.IntegerType)),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self._tap.config['tenant_id']}/export/leads"

    def get_child_context(self, record: dict, context: dict | None) -> dict:
        """Return a context dictionary for a child stream."""
        return {"lead_id": record["id"]}


class LeadNotesStream(ServiceTitanStream):
    """Define lead notes stream."""

    name = "lead_notes"
    primary_keys: t.ClassVar[list[str]] = ["createdById", "createdOn"]
    replication_key: str = "modifiedOn"
    parent_stream_type = LeadsStream
    ignore_parent_replication_key = True

    schema = th.PropertiesList(
        th.Property("text", th.StringType),
        th.Property("isPinned", th.BooleanType),
        th.Property("createdById", th.IntegerType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return (
            f"/crm/v2/tenant/{self._tap.config['tenant_id']}/leads/{'{lead_id}'}/notes"
        )


class LocationsStream(ServiceTitanExportStream):
    """Define locations stream."""

    name = "locations"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("taxZoneId", th.IntegerType),
        th.Property("id", th.IntegerType),
        th.Property("customerId", th.IntegerType),
        th.Property("active", th.BooleanType),
        th.Property("name", th.StringType),
        th.Property(
            "address",
            th.ObjectType(
                th.Property("street", th.StringType),
                th.Property("unit", th.StringType),
                th.Property("city", th.StringType),
                th.Property("state", th.StringType),
                th.Property("zip", th.StringType),
                th.Property("country", th.StringType),
                th.Property("latitude", th.NumberType),
                th.Property("longitude", th.NumberType),
            ),
        ),
        th.Property(
            "customFields",
            th.ArrayType(
                th.ObjectType(
                    th.Property("typeId", th.IntegerType),
                    th.Property("name", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
        th.Property("createdOn", th.DateTimeType),
        th.Property("createdById", th.IntegerType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("mergedToId", th.IntegerType),
        th.Property("zoneId", th.IntegerType),
        th.Property("tagTypeIds", th.ArrayType(th.IntegerType())),
        th.Property(
            "externalData",
            th.ArrayType(
                th.ObjectType(
                    th.Property("key", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self._tap.config['tenant_id']}/export/locations"

    def get_child_context(self, record: dict, context: dict | None) -> dict:
        """Return a context dictionary for a child stream."""
        return {"location_id": record["id"]}


class LocationNotesStream(ServiceTitanStream):
    """Define location notes stream."""

    name = "location_notes"
    primary_keys: t.ClassVar[list[str]] = ["createdById", "createdOn"]
    replication_key: str = "modifiedOn"
    parent_stream_type = LocationsStream
    ignore_parent_replication_key = True

    schema = th.PropertiesList(
        th.Property("text", th.StringType),
        th.Property("isPinned", th.BooleanType),
        th.Property("createdById", th.IntegerType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self._tap.config['tenant_id']}/locations/{'{location_id}'}/notes"  # noqa: E501


class LocationContactsStream(ServiceTitanExportStream):
    """Define location contacts stream."""

    name = "location_contacts"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("type", th.StringType),  # Enum values are treated as strings
        th.Property("value", th.StringType),
        th.Property("memo", th.StringType),
        th.Property(
            "phoneSettings",
            th.ObjectType(
                th.Property("phoneNumber", th.StringType),
                th.Property("doNotText", th.BooleanType),
            ),
        ),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("locationId", th.IntegerType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return (
            f"/crm/v2/tenant/{self._tap.config['tenant_id']}/export/locations/contacts"
        )
