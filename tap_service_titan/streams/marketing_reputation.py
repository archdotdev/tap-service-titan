"""Marketing reputation streams for the ServiceTitan tap."""

from __future__ import annotations

import sys
from functools import cached_property

from tap_service_titan.client import ServiceTitanStream
from tap_service_titan.openapi_specs import MARKETING_REPUTATION, ServiceTitanSchema

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


class ReviewsStream(ServiceTitanStream):
    """Define reviews stream."""

    name = "reviews"
    primary_keys = ("review", "platform", "address")
    replication_key: str = "publishDate"
    schema = ServiceTitanSchema(
        MARKETING_REPUTATION,
        key="ServiceTitan.Marketing.ReviewEngine.Services.Models.Reviews.ReviewReport",
    )

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/marketingreputation/v2/tenant/{self.tenant_id}/reviews"
