"""Marketing streams for the ServiceTitan tap."""

from __future__ import annotations

import typing as t
from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_service_titan.client import (
    ServiceTitanStream,
)


class CampaignsStream(ServiceTitanStream):
    """Define campaigns stream."""

    name = "campaigns"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("active", th.BooleanType),
        th.Property(
            "category",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
                th.Property("active", th.BooleanType),
            ),
        ),
        th.Property("source", th.StringType),
        th.Property("otherSource", th.StringType),
        th.Property("businessUnit", th.StringType),
        th.Property("medium", th.StringType),
        th.Property("otherMedium", th.StringType),
        th.Property("campaignPhoneNumbers", th.ArrayType(th.StringType)),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/marketing/v2/tenant/{self._tap.config['tenant_id']}/campaigns"
