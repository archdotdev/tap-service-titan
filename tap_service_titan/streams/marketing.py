"""Marketing streams for the ServiceTitan tap."""

from __future__ import annotations

import typing as t
from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_service_titan.client import ServiceTitanStream
from tap_service_titan.openapi_specs import MARKETING, ServiceTitanSchema


class CampaignsStream(ServiceTitanStream):
    """Define campaigns stream."""

    name = "campaigns"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(MARKETING, key="Marketing.V2.CampaignResponse")

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/marketing/v2/tenant/{self.tenant_id}/campaigns"


class MarketingCategoriesStream(ServiceTitanStream):
    """Define categories stream."""

    name = "marketing_categories"
    primary_keys = ("id",)
    replication_key: str = "createdOn"
    schema = ServiceTitanSchema(MARKETING, key="Marketing.V2.CampaignCategoryResponse")

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/marketing/v2/tenant/{self.tenant_id}/categories"


class CostsStream(ServiceTitanStream):
    """Define costs stream."""

    name = "costs"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("year", th.IntegerType),
        th.Property("month", th.IntegerType),
        th.Property("dailyCost", th.NumberType),
        th.Property("campaignId", th.IntegerType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/marketing/v2/tenant/{self._tap.config['tenant_id']}/costs"


class SuppressionsStream(ServiceTitanStream):
    """Define suppressions stream."""

    name = "suppressions"
    primary_keys: t.ClassVar[list[str]] = ["email"]
    schema = th.PropertiesList(
        th.Property("email", th.StringType),
        th.Property("reason", th.StringType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/marketing/v2/tenant/{self._tap.config['tenant_id']}/suppressions"
