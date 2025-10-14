"""Marketing reputation streams for the ServiceTitan tap."""

from __future__ import annotations

import typing as t
from functools import cached_property
from urllib.parse import urlencode

from tap_service_titan.client import ServiceTitanStream
from tap_service_titan.openapi_specs import MARKETING_REPUTATION, ServiceTitanSchema

if t.TYPE_CHECKING:
    from singer_sdk.streams.rest import _TToken


class ReviewsStream(ServiceTitanStream):
    """Define reviews stream."""

    name = "reviews"
    primary_keys = ("review", "platform", "address")
    replication_key: str = "publishDate"
    schema = ServiceTitanSchema(
        MARKETING_REPUTATION,
        key="ServiceTitan.Marketing.ReviewEngine.Services.Models.Reviews.ReviewReport",
    )

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/marketingreputation/v2/tenant/{self.tenant_id}/reviews"

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: _TToken | None,
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params = super().get_url_params(context, next_page_token)
        flags = [
            "includeReviewsWithoutLocation",
            "includeReviewsWithoutCampaign",
            "includeReviewsWithoutTechnician",
        ]
        for flag in flags:
            params[flag] = None
        encoded = urlencode(params)
        return encoded.replace("=None", "")  # type: ignore[return-value]
