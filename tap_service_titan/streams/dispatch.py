"""Dispatch streams for the ServiceTitan tap."""

from __future__ import annotations

import typing as t
from datetime import datetime, timedelta, timezone
from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator

from tap_service_titan.client import ServiceTitanStream

if t.TYPE_CHECKING:
    import requests


class CapacitiesPaginator(BaseAPIPaginator):
    """Define paginator for the capacities stream."""

    def __init__(self, start_value: datetime, *args, **kwargs) -> None:  # noqa: ANN002 ANN003
        """Initialize the paginator."""
        super().__init__(start_value=start_value, *args, **kwargs)  # noqa: B026
        self.end_value = datetime.now(timezone.utc) + timedelta(days=7)

    def has_more(self, response: requests.Response) -> bool:  # noqa: ARG002
        """Check if there are more requests to make."""
        return self.current_value <= self.end_value

    def get_next(self, response: requests.Response) -> dict | None:  # noqa: ARG002
        """Get the next page token."""
        return self.current_value + timedelta(days=1)


class CapacitiesStream(ServiceTitanStream):
    """Define capacities stream."""

    name = "capacities"
    primary_keys: t.ClassVar[list[str]] = [
        "startUtc",
        "businessUnitIds",
        "technician_id",
    ]
    replication_key = "startUtc"
    rest_method = "POST"
    records_jsonpath = "$.availabilities[*]"

    schema = th.PropertiesList(
        th.Property("start", th.DateTimeType),
        th.Property("end", th.DateTimeType),
        th.Property("startUtc", th.DateTimeType),
        th.Property("endUtc", th.DateTimeType),
        th.Property("businessUnitIds", th.ArrayType(th.IntegerType)),
        th.Property("technician_id", th.IntegerType),
        th.Property("technician_name", th.StringType),
        th.Property("technician_status", th.StringType),
        th.Property("technician_hasRequiredSkills", th.BooleanType),
    ).to_dict()

    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        for availability_dict in extract_jsonpath(
            self.records_jsonpath, input=response.json()
        ):
            # We're only looking to get technician availabilities here
            for unused_key in [
                "totalAvailability",
                "openAvailability",
                "isAvailable",
                "isExceedingIdealBookingPercentage",
            ]:
                availability_dict.pop(unused_key)
            for technician in availability_dict.pop("technicians"):
                technician_dict = {
                    f"technician_{key}": val for key, val in technician.items()
                }
                yield {**availability_dict, **technician_dict}

    def get_new_paginator(self) -> CapacitiesPaginator:
        """Get the paginator."""
        return CapacitiesPaginator(self.get_starting_timestamp(self.context))

    def prepare_request_payload(
        self,
        context: dict | None,  # noqa: ARG002
        next_page_token: datetime,
    ) -> dict | None:
        """Prepare the request payload."""
        return {
            "startsOnOrAfter": next_page_token.isoformat(),
            "endsOnOrBefore": (next_page_token + timedelta(days=1)).isoformat(),
            "skillBasedAvailability": "false",
        }

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/dispatch/v2/tenant/{self._tap.config['tenant_id']}/capacity"
