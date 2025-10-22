"""Scheduling streams for the ServiceTitan tap."""

from __future__ import annotations

import sys
from functools import cached_property
from typing import TYPE_CHECKING

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_service_titan.client import ServiceTitanStream

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if TYPE_CHECKING:
    from singer_sdk.helpers.types import Context, Record


class SchedulersStream(ServiceTitanStream):
    """Define schedulers stream."""

    name = "schedulers"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("companyName", th.StringType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("schedulerStatus", th.StringType),
        th.Property("dataApiKey", th.StringType),
        th.Property("isDefault", th.BooleanType),
    ).to_dict()

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/schedulingpro/v2/tenant/{self.tenant_id}/schedulers"

    @override
    def get_child_context(self, record: Record, context: Context | None) -> dict:
        """Return a context dictionary for child streams."""
        return {"scheduler_id": record.get("id")}


class SchedulerSessionsStream(ServiceTitanStream):
    """Define scheduler sessions stream."""

    name = "scheduler_sessions"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    parent_stream_type = SchedulersStream

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("lastCheckinDate", th.DateTimeType),
        th.Property("sessionOutcome", th.StringType),
        th.Property("jobId", th.IntegerType),
        th.Property("bookingId", th.IntegerType),
        th.Property("timeslotStart", th.DateTimeType),
        th.Property("timeslotEnd", th.DateTimeType),
        th.Property("category", th.StringType),
        th.Property("jobTypeId", th.IntegerType),
        th.Property("businessUnitId", th.IntegerType),
        th.Property(
            "customer",
            th.ObjectType(
                th.Property("isNewCustomer", th.BooleanType),
                th.Property("id", th.IntegerType),
                th.Property("firstName", th.StringType),
                th.Property("lastName", th.StringType),
                th.Property("email", th.StringType),
                th.Property("phone", th.StringType),
                th.Property("isNewLocation", th.BooleanType),
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
            ),
        ),
        th.Property("zoneId", th.IntegerType),
        th.Property("customerResponses", th.ArrayType(th.StringType)),
        th.Property("notes", th.StringType),
        th.Property(
            "sourceTracking",
            th.ObjectType(
                th.Property("isRWGSession", th.BooleanType),
                th.Property("campaignId", th.StringType),
                th.Property("landingPageUrl", th.StringType),
                th.Property("gclid", th.StringType),
                th.Property("fbclid", th.StringType),
                th.Property("msclkid", th.StringType),
                th.Property("utmSource", th.StringType),
                th.Property("utmMedium", th.StringType),
                th.Property("utmCampaign", th.StringType),
                th.Property("utmAdgroup", th.StringType),
                th.Property("utmTerm", th.StringType),
                th.Property("utmContent", th.StringType),
                th.Property("googleAnalyticsClientId", th.StringType),
            ),
        ),
    ).to_dict()

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/schedulingpro/v2/tenant/{self.tenant_id}/schedulers/{'{scheduler_id}'}/sessions"


class SchedulerPerformanceStream(ServiceTitanStream):
    """Define scheduler performance stream."""

    name = "scheduler_performance"
    primary_keys = ("id",)
    parent_stream_type = SchedulersStream
    ignore_parent_replication_key = True

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("schedulerName", th.StringType),
        th.Property("totalSessions", th.IntegerType),
        th.Property("completedSessions", th.IntegerType),
        th.Property("bookedSessions", th.IntegerType),
        th.Property("abandonedSessions", th.IntegerType),
        th.Property("completionRate", th.NumberType),
        th.Property("bookingRate", th.NumberType),
        th.Property("abandonmentRate", th.NumberType),
        th.Property(
            "funnelMetrics",
            th.ObjectType(
                th.Property("landingPageViews", th.IntegerType),
                th.Property("customerInfoStarts", th.IntegerType),
                th.Property("customerInfoCompletes", th.IntegerType),
                th.Property("timeslotSelections", th.IntegerType),
                th.Property("confirmationViews", th.IntegerType),
                th.Property("bookingCompletes", th.IntegerType),
            ),
        ),
        th.Property(
            "averageSessionDuration",
            th.ObjectType(
                th.Property("minutes", th.IntegerType),
                th.Property("seconds", th.IntegerType),
            ),
        ),
        th.Property("dateRangeStart", th.DateTimeType),
        th.Property("dateRangeEnd", th.DateTimeType),
    ).to_dict()

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return (
            f"/schedulingpro/v2/tenant/{self.tenant_id}/schedulers/{'{scheduler_id}'}/performance"
        )
