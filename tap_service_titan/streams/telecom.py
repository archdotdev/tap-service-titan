"""Telecom streams for the ServiceTitan tap."""

from __future__ import annotations

import typing as t
from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_service_titan.client import (
    ServiceTitanExportStream,
)


class CallsStream(ServiceTitanExportStream):
    """Define calls stream."""

    name = "calls"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("duration", th.StringType),
        th.Property("from", th.StringType),
        th.Property("to", th.StringType),
        th.Property("direction", th.StringType),
        th.Property("status", th.StringType),
        th.Property("type", th.StringType),
        th.Property("recordingUrl", th.StringType),
        th.Property("voiceMailPath", th.StringType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property(
            "reason",
            th.ObjectType(
                th.Property("id", th.IntegerType), th.Property("name", th.StringType)
            ),
        ),
        th.Property(
            "customer",
            th.ObjectType(
                th.Property("id", th.IntegerType), th.Property("name", th.StringType)
            ),
        ),
        th.Property(
            "location",
            th.ObjectType(
                th.Property("id", th.IntegerType), th.Property("name", th.StringType)
            ),
        ),
        th.Property(
            "campaign",
            th.ObjectType(
                th.Property("id", th.IntegerType), th.Property("name", th.StringType)
            ),
        ),
        th.Property(
            "job",
            th.ObjectType(
                th.Property("id", th.IntegerType), th.Property("number", th.StringType)
            ),
        ),
        th.Property(
            "agent",
            th.ObjectType(
                th.Property("id", th.IntegerType), th.Property("name", th.StringType)
            ),
        ),
        th.Property(
            "createdBy",
            th.ObjectType(
                th.Property("id", th.IntegerType), th.Property("name", th.StringType)
            ),
        ),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/telecom/v2/tenant/{self._tap.config['tenant_id']}/export/calls"
