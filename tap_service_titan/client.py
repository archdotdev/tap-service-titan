"""REST client handling, including ServiceTitanStream base class."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import cached_property
from typing import Any, Callable, Iterable

import requests
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import (
    BaseAPIPaginator,
    BasePageNumberPaginator,
)
from singer_sdk.streams import RESTStream

from tap_service_titan.auth import ServiceTitanAuthenticator

if sys.version_info >= (3, 9):
    pass
else:
    pass

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]


@dataclass
class DateRange:
    """Represents a date range for pagination."""

    start: datetime
    interval: timedelta
    max_date: datetime

    @property
    def end(self) -> datetime:
        """Calculate the end date of the current range."""
        return self.start + self.interval

    def increase(self) -> DateRange:
        """Create a new DateRange with the next interval."""
        return DateRange(self.end, self.interval, self.max_date)

    def is_valid(self) -> bool:
        """Check if the current range is within the maximum date."""
        return self.start < self.max_date


class DateRangePaginator(BaseAPIPaginator[DateRange]):
    """Paginator that uses date ranges for pagination."""

    def __init__(self, start_date: datetime, interval: timedelta, max_date: datetime):
        """Initialize DateRangePaginator.

        Args:
            start_date: Starting date for pagination
            interval: Time interval for each page
            max_date: Maximum date to paginate to
        """
        date_range = DateRange(start_date, interval, max_date)
        super().__init__(start_value=date_range)

    def get_next(self, response: requests.Response) -> DateRange | None:
        """Get the next date range for pagination.

        Args:
            response: The HTTP response (unused in this implementation)

        Returns:
            Next DateRange or None if no more pages
        """
        if not isinstance(self.current_value, DateRange):
            return None

        new_range = self.current_value.increase()
        return new_range if new_range.is_valid() else None


class ServiceTitanBaseStream(RESTStream):
    """ServiceTitan base stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["api_url"]

    records_jsonpath = "$.data[*]"  # Or override `parse_response`.

    @cached_property
    def authenticator(self) -> _Auth:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return ServiceTitanAuthenticator.create_for_stream(self)

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        headers["ST-App-Key"] = self.config["st_app_key"]
        return headers

    def get_new_paginator(self) -> BaseAPIPaginator:
        """Create a new pagination helper instance.

        If the source API can make use of the `next_page_token_jsonpath`
        attribute, or it contains a `X-Next-Page` header in the response
        then you can remove this method.

        If you need custom pagination that uses page numbers, "next" links, or
        other approaches, please read the guide: https://sdk.meltano.com/en/v0.25.0/guides/pagination-classes.html.

        Returns:
            A pagination helper instance.
        """
        return super().get_new_paginator()

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def response_error_message(self, response: requests.Response) -> str:
        """Build error message for invalid http statuses.

        WARNING - Override this method when the URL path may contain secrets or PII

        Args:
            response: A :class:`requests.Response` object.

        Returns:
            str: The error message
        """
        default = super().response_error_message(response)
        if response.content:
            try:
                json_response = response.json()
                if "title" in json_response:
                    title = json_response["title"]
                    return f"{default}. {title}"
            except (requests.exceptions.JSONDecodeError, ValueError):
                # Response content is not valid JSON - log the full content
                # This helps debug unexpected responses (e.g., HTML error pages)
                return f"{default}. Response body: {response.text}"
        return default


class ServiceTitanExportStream(ServiceTitanBaseStream):
    """ServiceTitan stream class for export endpoints."""

    next_page_token_jsonpath = "$.continueFrom"  # noqa: S105

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
        params: dict = {}
        starting_date = self.get_starting_timestamp(context)

        if next_page_token:
            params["from"] = next_page_token

        # The Service Titan API uses the "from" param for both continuation tokens
        # and for the starting timestamp for the first request of an export
        if self.replication_key and starting_date and (next_page_token is None):
            # "from" param is inclusive of start date
            # this prevents duplicating of single record in each run
            starting_date += timedelta(milliseconds=1)
            params["from"] = starting_date.isoformat()

        return params


class ServiceTitanPaginator(BasePageNumberPaginator):
    """ServiceTitan paginator class."""

    def has_more(self, response: requests.Response) -> bool:
        """Return True if there are more pages available."""
        return response.json().get("hasMore", False)


class ServiceTitanStream(ServiceTitanBaseStream):
    """ServiceTitan stream class for endpoints without export support."""

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
        params: dict = {}
        starting_date = self.get_starting_timestamp(context)

        # The Service Titan API uses the "from" param for both continuation tokens
        # and for the starting timestamp for the first request of an export
        if self.replication_key and starting_date:
            # "from" param is inclusive of start date
            # this prevents duplicating of single record in each run
            starting_date += timedelta(milliseconds=1)
            params["modifiedOnOrAfter"] = starting_date.isoformat()
        params["pageSize"] = 5000
        params["page"] = next_page_token
        return params

    def get_new_paginator(self) -> ServiceTitanPaginator:
        """Create a new pagination helper instance."""
        return ServiceTitanPaginator(start_value=1)
