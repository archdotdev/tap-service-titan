"""Marketing streams for the ServiceTitan tap."""

from __future__ import annotations

import sys
from functools import cached_property

from tap_service_titan.client import ServiceTitanStream
from tap_service_titan.openapi_specs import MARKETING, ServiceTitanSchema

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


class CampaignsStream(ServiceTitanStream, active_any=True):
    """Define campaigns stream.

    https://developer.servicetitan.io/api-details/#api=tenant-marketing-v2&operation=Campaigns_GetList
    """

    name = "campaigns"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(MARKETING, key="Marketing.V2.CampaignResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/marketing/v2/tenant/{self.tenant_id}/campaigns"


class MarketingCategoriesStream(ServiceTitanStream):
    """Define categories stream.

    https://developer.servicetitan.io/api-details/#api=tenant-marketing-v2&operation=CampaignCategories_GetList
    """

    name = "marketing_categories"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(MARKETING, key="Marketing.V2.CampaignCategoryResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/marketing/v2/tenant/{self.tenant_id}/categories"


class CostsStream(ServiceTitanStream):
    """Define costs stream."""

    name = "costs"
    primary_keys = ("id",)
    schema = ServiceTitanSchema(MARKETING, key="Marketing.V2.CampaignCostResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/marketing/v2/tenant/{self.tenant_id}/costs"


class SuppressionsStream(ServiceTitanStream, active_any=True, sort_by="ModifiedOn"):
    """Define suppressions stream.

    https://developer.servicetitan.io/api-details/#api=tenant-marketing-v2&operation=Suppressions_GetList
    """

    name = "suppressions"
    primary_keys = ("email",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(MARKETING, key="Marketing.V2.SuppressionResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/marketing/v2/tenant/{self.tenant_id}/suppressions"
