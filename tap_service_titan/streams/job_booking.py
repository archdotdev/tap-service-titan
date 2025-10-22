"""Job booking streams for the ServiceTitan tap."""

from __future__ import annotations

from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_service_titan.client import (
    ServiceTitanStream,
)


class CallReasonsStream(ServiceTitanStream):
    """Define call reasons stream."""

    name = "call_reasons"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("isLead", th.BooleanType),
        th.Property("active", th.BooleanType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/jbce/v2/tenant/{self.tenant_id}/call-reasons"
