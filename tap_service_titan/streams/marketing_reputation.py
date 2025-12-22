"""Marketing reputation streams for the ServiceTitan tap."""

from __future__ import annotations

import sys
import typing as t
from functools import cached_property
from urllib.parse import urlencode

from tap_service_titan.client import ServiceTitanStream
from tap_service_titan.openapi_specs import MARKETING_REPUTATION, ServiceTitanSchema

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if t.TYPE_CHECKING:
    from singer_sdk.helpers.types import Context


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

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: int | None,
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params = t.cast("dict[str, t.Any]", super().get_url_params(context, next_page_token))
        flags = [
            "includeReviewsWithoutLocation",
            "includeReviewsWithoutCampaign",
            "includeReviewsWithoutTechnician",
        ]
        for flag in flags:
            params[flag] = None
        encoded = urlencode(params)
        return encoded.replace("=None", "")  # type: ignore[return-value]
