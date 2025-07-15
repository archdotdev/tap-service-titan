"""Marketing ads streams for the ServiceTitan tap."""

from __future__ import annotations

import typing as t
from datetime import datetime, timedelta, timezone
from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk.exceptions import FatalAPIError
from singer_sdk.helpers.types import Context  # noqa: TC002

from tap_service_titan.client import (
    DateRange,
    DateRangePaginator,
    ServiceTitanStream,
)

if t.TYPE_CHECKING:
    from singer_sdk.helpers import types


class AttributedLeadsStream(ServiceTitanStream):
    """Define attributed leads stream."""

    name = "attributed_leads"
    primary_keys: tuple[str] = ("dateTime",)
    replication_key: str = "dateTime"

    schema = th.PropertiesList(
        th.Property("dateTime", th.DateTimeType),
        th.Property("leadType", th.StringType),
        th.Property(
            "attribution",
            th.ObjectType(
                th.Property("utmSource", th.StringType),
                th.Property("utmMedium", th.StringType),
                th.Property("utmCampaign", th.StringType),
                th.Property("landingPageUrl", th.StringType),
                th.Property("referrerUrl", th.StringType),
                th.Property("clickId", th.StringType),
                th.Property("stCampaignId", th.IntegerType),
                th.Property("originalCampaign", th.StringType),
                th.Property("attributionOverwriteType", th.StringType),
                th.Property("attributionOverwriteId", th.IntegerType),
                th.Property("overwrittenBookingJobId", th.IntegerType),
                th.Property("adGroupId", th.StringType),
                th.Property("adGroupName", th.StringType),
                th.Property("keywordId", th.StringType),
                th.Property("keywordName", th.StringType),
            ),
        ),
        th.Property(
            "job",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "customer",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "call",
            th.ObjectType(
                th.Property("duration", th.StringType),
                th.Property("id", th.IntegerType),
                th.Property("type", th.StringType),
                th.Property("source", th.StringType),
                th.Property("callerNumber", th.StringType),
                th.Property("trackingNumber", th.StringType),
                th.Property("excusedReason", th.StringType),
            ),
        ),
        th.Property(
            "leadForm",
            th.ObjectType(
                th.Property("leadNumber", th.IntegerType),
                th.Property("leadStatus", th.StringType),
                th.Property("notes", th.StringType),
            ),
        ),
        th.Property(
            "booking",
            th.ObjectType(
                th.Property("id", th.IntegerType),
            ),
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return (
            f"/marketingads/v2/tenant/{self._tap.config['tenant_id']}/attributed-leads"
        )

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.


        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = super().get_url_params(context, next_page_token)

        params["fromUtc"] = params.pop("modifiedOnOrAfter")
        params["toUtc"] = datetime.now(timezone.utc).isoformat()
        return params


class CapacityWarningsStream(ServiceTitanStream):
    """Define capacity warnings stream."""

    name = "capacity_warnings"
    primary_keys: tuple[str, str] = ("campaignName", "warningType")

    schema = th.PropertiesList(
        th.Property("campaignName", th.StringType),
        th.Property("warningType", th.StringType),
        th.Property("businessUnits", th.ArrayType(th.StringType)),
        th.Property("lookaheadWindow", th.IntegerType),
        th.Property("thresholdValue", th.IntegerType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return (
            f"/marketingads/v2/tenant/{self._tap.config['tenant_id']}/capacity-warnings"
        )


class PerformanceStream(ServiceTitanStream):
    """Define marketing performance stream."""

    name = "performance"
    primary_keys: tuple[str, str, str] = ("campaign_name", "adGroup_id", "keyword_id")
    replication_key: str = "from_utc"

    schema = th.PropertiesList(
        th.Property("from_utc", th.DateTimeType),
        th.Property("to_utc", th.DateTimeType),
        th.Property("campaign_name", th.StringType),
        th.Property("adGroup_id", th.StringType),
        th.Property("keyword_id", th.StringType),
        th.Property(
            "campaign",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
                th.Property("category", th.StringType),
                th.Property("launchDate", th.StringType),
                th.Property("status", th.IntegerType),
            ),
        ),
        th.Property(
            "adGroup",
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("name", th.StringType),
                th.Property("status", th.IntegerType),
            ),
        ),
        th.Property(
            "keyword",
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("name", th.StringType),
                th.Property("status", th.IntegerType),
            ),
        ),
        th.Property(
            "digitalStats",
            th.ObjectType(
                th.Property("impressionShare", th.NumberType),
                th.Property("impressions", th.IntegerType),
                th.Property("clicks", th.IntegerType),
                th.Property("averageCPC", th.NumberType),
                th.Property("conversions", th.IntegerType),
                th.Property("allConversions", th.NumberType),
                th.Property("cost", th.NumberType),
                th.Property("clickRate", th.NumberType),
                th.Property("costPerConversion", th.NumberType),
                th.Property("conversionRate", th.NumberType),
            ),
        ),
        th.Property(
            "leadStats",
            th.ObjectType(
                th.Property("leads", th.IntegerType),
                th.Property("leadCalls", th.IntegerType),
                th.Property("onlineBooking", th.IntegerType),
                th.Property("manualBooking", th.IntegerType),
                th.Property("bookedJobs", th.IntegerType),
                th.Property("ranJobs", th.IntegerType),
                th.Property("soldJobs", th.IntegerType),
                th.Property("revenue", th.NumberType),
                th.Property("bookingRate", th.NumberType),
                th.Property("avgTicket", th.NumberType),
            ),
        ),
        th.Property("returnOnInvestment", th.NumberType),
    ).to_dict()

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002 ANN003
        """Add report end time for consistency."""
        super().__init__(*args, **kwargs)
        self.end_time = datetime.now(timezone.utc)
        self.interval = timedelta(days=1)

    def _get_default_start_date(self) -> datetime:
        """Get default start date when none is provided."""
        return datetime.now(timezone.utc) - timedelta(days=30)

    def _get_effective_start_date(self, context: dict | None = None) -> datetime:
        """Get the effective start date for the current context."""
        start_date = self.get_starting_timestamp(context)
        return start_date if start_date is not None else self._get_default_start_date()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/marketingads/v2/tenant/{self._tap.config['tenant_id']}/performance"

    def post_process(
        self,
        row: types.Record,
        context: types.Context | None = None,  # noqa: ARG002
    ) -> dict | None:
        """Process the record to add top-level IDs.

        Args:
            row: Individual record in the stream.
            context: Stream partition or context dictionary.

        Returns:
            The resulting record dict, or `None` if the record should be excluded.
        """
        row["campaign_name"] = row.get("campaign", {}).get("name")
        row["adGroup_id"] = row.get("adGroup", {}).get("id")
        row["keyword_id"] = row.get("keyword", {}).get("id")
        return row

    def get_new_paginator(self) -> DateRangePaginator:
        """Create a new pagination helper instance for date ranges."""
        start_date = self._get_effective_start_date()
        return DateRangePaginator(start_date, self.interval, self.end_time)

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value (DateRange object).


        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}

        if next_page_token is not None:
            # next_page_token is a DateRange object
            params["fromUtc"] = next_page_token.start.isoformat()
            params["toUtc"] = next_page_token.end.isoformat()
        else:
            # First request
            start_date = self._get_effective_start_date(context)
            end_date = min(start_date + self.interval, self.end_time)
            params["fromUtc"] = start_date.isoformat()
            params["toUtc"] = end_date.isoformat()

        return params

    def get_records(self, context: Context | None) -> t.Iterable[dict[str, t.Any]]:
        """Return a generator of record-type dictionary objects with coerced values.

        Args:
            context: Stream partition or context dictionary.

        Yields:
            One item per record with string coercion only in the units section.
        """
        for record in super().get_records(context):
            # Create a fresh DateRange for the current request
            start_date = self._get_effective_start_date(context)
            current_range = DateRange(start_date, self.interval, self.end_time)

            record["from_utc"] = current_range.start.isoformat()
            record["to_utc"] = current_range.end.isoformat()
            yield record


class CampaignPerformanceStream(PerformanceStream):
    """Define marketing performance stream for campaigns."""

    name = "campaign_performance"

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.


        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = super().get_url_params(context, next_page_token)
        params["performanceSegmentationType"] = "Campaign"
        return params


class KeywordPerformanceStream(PerformanceStream):
    """Define marketing performance stream for campaigns."""

    name = "keyword_performance"

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.


        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = super().get_url_params(context, next_page_token)
        params["performanceSegmentationType"] = "Keyword"
        return params


class AdGroupPerformanceStream(PerformanceStream):
    """Define marketing performance stream for campaigns."""

    name = "adgroup_performance"

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.


        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = super().get_url_params(context, next_page_token)
        params["performanceSegmentationType"] = "AdGroup"
        return params
