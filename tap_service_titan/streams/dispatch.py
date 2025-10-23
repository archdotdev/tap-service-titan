"""Dispatch streams for the ServiceTitan tap."""

from __future__ import annotations

import sys
import typing as t
from datetime import datetime, timedelta, timezone
from functools import cached_property

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


class CapacitiesPaginator(BaseAPIPaginator[datetime]):
    """Define paginator for the capacities stream."""

    @override
    def __init__(
        self,
        start_value: datetime,
        *args: t.Any,
        **kwargs: t.Any,
    ) -> None:
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
    primary_keys = (
        "startUtc",
        "businessUnitIds",
        "technician_id",
    )
    replication_key = "startUtc"
    http_method = HTTPMethod.POST
    records_jsonpath = "$.availabilities[*]"
    schema = ServiceTitanSchema(
        DISPATCH,
        key="Dispatch.V2.CapacityResponseAvailability",
    )

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
        return f"/dispatch/v2/tenant/{self.tenant_id}/capacity"


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
