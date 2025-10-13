"""Dispatch streams for the ServiceTitan tap."""

from __future__ import annotations

import sys
import typing as t
from datetime import datetime, timedelta, timezone
from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator

from tap_service_titan.client import ServiceTitanExportStream, ServiceTitanStream
from tap_service_titan.openapi_specs import DISPATCH, ServiceTitanSchema

if sys.version_info >= (3, 11):
    from http import HTTPMethod
else:
    from backports.httpmethod import HTTPMethod

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Context


class CapacitiesPaginator(BaseAPIPaginator):
    """Define paginator for the capacities stream."""

    @override
    def __init__(self, start_value: datetime, *args, **kwargs) -> None:  # noqa: ANN002 ANN003
        """Initialize the paginator."""
        super().__init__(start_value=start_value, *args, **kwargs)  # noqa: B026
        self.end_value = datetime.now(timezone.utc) + timedelta(days=7)

    @override
    def has_more(self, response: requests.Response) -> bool:
        """Check if there are more requests to make."""
        return self.current_value <= self.end_value

    @override
    def get_next(self, response: requests.Response) -> dict | None:
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
    http_method = HTTPMethod.POST
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
        th.Property(
            "totalAvailability",
            th.NumberType,  # TODO: Use SingerDecimalType. Requires SDK 0.45.0+.  # noqa: E501, FIX002, TD002, TD003
            description="Number of hours that total capacity can allow to be booked during this time frame",  # noqa: E501
        ),
        th.Property(
            "openAvailability",
            th.NumberType,  # TODO: Use SingerDecimalType. Requires SDK 0.45.0+.  # noqa: E501, FIX002, TD002, TD003
            description="Number of remaining hours that can be booked during this time frame",  # noqa: E501
        ),
        th.Property(
            "isExceedingIdealBookingPercentage",
            th.BooleanType,
            description="Indicate if Ideal Booking Percentage is exceeded",
        ),
    ).to_dict()

    @override
    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        for availability_dict in extract_jsonpath(
            self.records_jsonpath,
            input=response.json(),
        ):
            # We're only looking to get technician availabilities here
            for unused_key in [
                "isAvailable",
            ]:
                availability_dict.pop(unused_key)
            for technician in availability_dict.pop("technicians"):
                technician_dict = {
                    f"technician_{key}": val for key, val in technician.items()
                }
                yield {**availability_dict, **technician_dict}

    @override
    def get_new_paginator(self) -> CapacitiesPaginator:
        """Get the paginator."""
        return CapacitiesPaginator(self.get_starting_timestamp(self.context))

    @override
    def prepare_request_payload(
        self,
        context: Context | None,
        next_page_token: datetime,
    ) -> dict | None:
        """Prepare the request payload."""
        return {
            "startsOnOrAfter": next_page_token.isoformat(),
            "endsOnOrBefore": (next_page_token + timedelta(days=1)).isoformat(),
            "skillBasedAvailability": "false",
        }

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/dispatch/v2/tenant/{self._tap.config['tenant_id']}/capacity"


class ArrivalWindowsStream(ServiceTitanStream):
    """Define arrival windows stream."""

    name = "arrival_windows"
    primary_keys = ("id",)
    schema = ServiceTitanSchema(DISPATCH, key="Dispatch.V2.ArrivalWindowResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/dispatch/v2/tenant/{self.tenant_id}/arrival-windows"


class AppointmentAssignmentsStream(ServiceTitanExportStream):
    """Define appointment assignments stream."""

    name = "appointment_assignments"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(
        DISPATCH,
        key="Dispatch.V2.ExportAppointmentAssignmentsResponse",
    )

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/dispatch/v2/tenant/{self.tenant_id}/export/appointment-assignments"


class NonJobAppointmentsStream(ServiceTitanStream):
    """Define non job appointments stream."""

    name = "non_job_appointments"
    primary_keys = ("id",)
    replication_key: str = "createdOn"
    schema = ServiceTitanSchema(DISPATCH, key="Dispatch.V2.NonJobAppointmentResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/dispatch/v2/tenant/{self.tenant_id}/non-job-appointments"


class TeamsStream(ServiceTitanStream):
    """Define teams stream."""

    name = "teams"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(DISPATCH, key="Dispatch.V2.TeamResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/dispatch/v2/tenant/{self.tenant_id}/teams"


class TechnicianShiftsStream(ServiceTitanStream):
    """Define technician shifts stream."""

    name = "technician_shifts"
    primary_keys = ("id",)
    schema = ServiceTitanSchema(DISPATCH, key="Dispatch.V2.TechnicianShiftResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/dispatch/v2/tenant/{self.tenant_id}/technician-shifts"


class ZonesStream(ServiceTitanStream):
    """Define zones stream."""

    name = "zones"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(DISPATCH, key="Dispatch.V2.ZoneResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/dispatch/v2/tenant/{self.tenant_id}/zones"


class BusinessHoursStream(ServiceTitanStream):
    """Define business hours stream."""

    name = "business_hours"
    primary_keys: t.ClassVar[list[str]] = []
    schema = ServiceTitanSchema(DISPATCH, key="Dispatch.V2.BusinessHourModel")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/dispatch/v2/tenant/{self.tenant_id}/business-hours"
