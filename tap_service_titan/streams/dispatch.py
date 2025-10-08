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

if sys.version_info >= (3, 11):
    from http import HTTPMethod
else:
    from backports.httpmethod import HTTPMethod

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
                "isAvailable",
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


class ArrivalWindowsStream(ServiceTitanStream):
    """Define arrival windows stream."""

    name = "arrival_windows"
    primary_keys: t.ClassVar[list[str]] = ["id"]

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("start", th.StringType),
        th.Property("duration", th.StringType),
        th.Property("businessUnitIds", th.ArrayType(th.IntegerType)),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/dispatch/v2/tenant/{self._tap.config['tenant_id']}/arrival-windows"


class AppointmentAssignmentsStream(ServiceTitanExportStream):
    """Define appointment assignments stream."""

    name = "appointment_assignments"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("technicianId", th.IntegerType),
        th.Property("technicianName", th.StringType),
        th.Property("assignedById", th.IntegerType),
        th.Property("assignedOn", th.DateTimeType),
        th.Property("status", th.StringType),
        th.Property("isPaused", th.BooleanType),
        th.Property("jobId", th.IntegerType),
        th.Property("appointmentId", th.IntegerType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/dispatch/v2/tenant/{self._tap.config['tenant_id']}/export/appointment-assignments"


class NonJobAppointmentsStream(ServiceTitanStream):
    """Define non job appointments stream."""

    name = "non_job_appointments"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "createdOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("technicianId", th.IntegerType),
        th.Property("start", th.DateTimeType),
        th.Property("name", th.StringType),
        th.Property("duration", th.StringType),
        th.Property("timesheetCodeId", th.IntegerType),
        th.Property("summary", th.StringType),
        th.Property("clearDispatchBoard", th.BooleanType),
        th.Property("clearTechnicianView", th.BooleanType),
        th.Property("removeTechnicianFromCapacityPlanning", th.BooleanType),
        th.Property("allDay", th.BooleanType),
        th.Property("showOnTechnicianSchedule", th.BooleanType),
        th.Property("active", th.BooleanType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("createdById", th.IntegerType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return (
            f"/dispatch/v2/tenant/{self._tap.config['tenant_id']}/non-job-appointments"
        )


class TeamsStream(ServiceTitanStream):
    """Define teams stream."""

    name = "teams"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("active", th.BooleanType),
        th.Property("name", th.StringType),
        th.Property("createdBy", th.IntegerType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/dispatch/v2/tenant/{self._tap.config['tenant_id']}/teams"


class TechnicianShiftsStream(ServiceTitanStream):
    """Define technician shifts stream."""

    name = "technician_shifts"
    primary_keys: t.ClassVar[list[str]] = ["id"]

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("shiftType", th.StringType),
        th.Property("title", th.StringType),
        th.Property("note", th.StringType),
        th.Property("active", th.BooleanType),
        th.Property("technicianId", th.IntegerType),
        th.Property("start", th.DateTimeType),
        th.Property("end", th.DateTimeType),
        th.Property("timesheetCodeId", th.IntegerType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/dispatch/v2/tenant/{self._tap.config['tenant_id']}/technician-shifts"


class ZonesStream(ServiceTitanStream):
    """Define zones stream."""

    name = "zones"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("active", th.BooleanType),
        th.Property("name", th.StringType),
        th.Property("zips", th.ArrayType(th.StringType)),
        th.Property("cities", th.ArrayType(th.StringType)),
        th.Property("territoryNumbers", th.ArrayType(th.StringType)),
        th.Property("locnNumbers", th.ArrayType(th.StringType)),
        th.Property("createdBy", th.IntegerType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("serviceDaysEnabled", th.BooleanType),
        th.Property("serviceDays", th.ArrayType(th.StringType)),
        th.Property("businessUnits", th.ArrayType(th.IntegerType)),
        th.Property("technicians", th.ArrayType(th.IntegerType)),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/dispatch/v2/tenant/{self._tap.config['tenant_id']}/zones"


class BusinessHoursStream(ServiceTitanStream):
    """Define business hours stream."""

    name = "business_hours"
    primary_keys: t.ClassVar[list[str]] = []

    schema = th.PropertiesList(
        th.Property(
            "weekdays",
            th.ArrayType(
                th.ObjectType(
                    th.Property("fromHour", th.IntegerType),
                    th.Property("toHour", th.IntegerType),
                )
            ),
        ),
        th.Property(
            "saturday",
            th.ArrayType(
                th.ObjectType(
                    th.Property("fromHour", th.IntegerType),
                    th.Property("toHour", th.IntegerType),
                )
            ),
        ),
        th.Property(
            "sunday",
            th.ArrayType(
                th.ObjectType(
                    th.Property("fromHour", th.IntegerType),
                    th.Property("toHour", th.IntegerType),
                )
            ),
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/dispatch/v2/tenant/{self._tap.config['tenant_id']}/business-hours"
