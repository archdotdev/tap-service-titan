"""Marketing ads streams for the ServiceTitan tap."""

from __future__ import annotations

import typing as t
from datetime import datetime, timezone
from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_service_titan.client import (
    ServiceTitanStream,
)


class AttributedLeadsStream(ServiceTitanStream):
    """Define attributed leads stream."""

    name = "attributed_leads"
    primary_keys: t.ClassVar[list[str]] = ["dateTime"]
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
    primary_keys: t.ClassVar[list[str]] = ["campaignName", "warningType"]

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
    primary_keys: t.ClassVar[list[str]] = ["campaign.name", "adGroup.id", "keyword.id"]

    schema = th.PropertiesList(
        th.Property(
            "campaign",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
                th.Property("category", th.StringType),
                th.Property("launchDate", th.StringType),
                th.Property("status", th.StringType),
            ),
        ),
        th.Property(
            "adGroup",
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("name", th.StringType),
                th.Property("status", th.StringType),
            ),
        ),
        th.Property(
            "keyword",
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("name", th.StringType),
                th.Property("status", th.StringType),
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

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/marketingads/v2/tenant/{self._tap.config['tenant_id']}/performance"
