"""REST client handling, including ServiceTitanStream base class."""

from __future__ import annotations

import sys
from datetime import timedelta
from functools import cached_property
from typing import Any, Callable, Iterable

import requests
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator  # noqa: TCH002
from singer_sdk.streams import RESTStream

from tap_service_titan.auth import ServiceTitanAuthenticator

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = importlib_resources.files(__package__) / "schemas"


class ServiceTitanStream(RESTStream):
    """ServiceTitan stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["api_url"]

    records_jsonpath = "$.data[*]"  # Or override `parse_response`.

    next_page_token_jsonpath = "$.continueFrom"  # noqa: S105

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

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())
