"""Marketing reputation streams for the ServiceTitan tap."""

from __future__ import annotations

import typing as t
from functools import cached_property
from urllib.parse import urlencode

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_service_titan.client import ServiceTitanStream

if t.TYPE_CHECKING:
    from singer_sdk.streams.rest import _TToken


class ReviewsStream(ServiceTitanStream):
    """Define reviews stream."""

    name = "reviews"
    primary_keys: t.ClassVar[list[str]] = ["review", "platform", "address"]
    replication_key: str = "publishDate"

    schema = th.PropertiesList(
        th.Property("address", th.StringType, required=False),
        th.Property("platform", th.StringType, required=False),
        th.Property("authorEmail", th.StringType, required=False),
        th.Property("authorName", th.StringType, required=False),
        th.Property("review", th.StringType),
        th.Property("reviewResponse", th.StringType, required=False),
        th.Property("publishDate", th.DateTimeType, required=False),
        th.Property("rating", th.NumberType, required=False),
        th.Property("recommendationStatus", th.IntegerType, required=False),
        th.Property("verificationStatus", th.BooleanType, required=False),
        th.Property("jobId", th.IntegerType, required=False),
        th.Property("verifiedByUserId", th.IntegerType, required=False),
        th.Property("verifiedOn", th.DateTimeType, required=False),
        th.Property("isAutoVerified", th.BooleanType, required=False),
        th.Property("businessUnitId", th.IntegerType, required=False),
        th.Property("completedDate", th.StringType, required=False),
        th.Property("customerName", th.StringType, required=False),
        th.Property("customerId", th.IntegerType, required=False),
        th.Property("dispatchedDate", th.StringType, required=False),
        th.Property("jobStatus", th.IntegerType, required=False),
        th.Property("jobTypeName", th.StringType, required=False),
        th.Property("technicianFullName", th.StringType, required=False),
        th.Property("technicianId", th.IntegerType, required=False),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/marketingreputation/v2/tenant/{self._tap.config['tenant_id']}/reviews"

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
