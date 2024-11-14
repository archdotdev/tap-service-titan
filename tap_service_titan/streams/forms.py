"""Forms streams for the ServiceTitan tap."""

from __future__ import annotations

import typing as t
from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_service_titan.client import (
    ServiceTitanExportStream,
    ServiceTitanStream,
)


class FormsStream(ServiceTitanStream):
    """Define forms stream."""

    name = "forms"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("active", th.BooleanType),
        th.Property("name", th.StringType),
        th.Property("published", th.BooleanType),
        th.Property("hasConditionalLogic", th.BooleanType),
        th.Property("hasTriggers", th.BooleanType),
        th.Property("createdById", th.IntegerType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/forms/v2/tenant/{self._tap.config['tenant_id']}/forms"


class SubmissionsStream(ServiceTitanStream):
    """Define submissions stream."""

    name = "submissions"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "submittedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("formId", th.IntegerType),
        th.Property("formName", th.StringType),
        th.Property("submittedOn", th.DateTimeType),
        th.Property("createdById", th.IntegerType),
        th.Property("status", th.StringType),
        th.Property(
            "owners",
            th.ArrayType(
                th.ObjectType(
                    th.Property("type", th.StringType),
                    th.Property("id", th.IntegerType),
                )
            ),
        ),
        th.Property(
            "units",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("name", th.StringType),
                    th.Property("type", th.StringType),
                    th.Property("description", th.StringType),
                    th.Property(
                        "units",
                        th.ArrayType(
                            th.ObjectType(
                                th.Property("id", th.StringType),
                                th.Property("name", th.StringType),
                                th.Property("type", th.StringType),
                                th.Property("comment", th.StringType),
                                th.Property(
                                    "attachments",
                                    th.ArrayType(
                                        th.ObjectType(
                                            th.Property("fileName", th.StringType),
                                            th.Property("createdFrom", th.StringType),
                                            th.Property(
                                                "originalFileName", th.StringType
                                            ),
                                            th.Property("thumbnail", th.StringType),
                                        )
                                    ),
                                ),
                                th.Property("value", th.StringType),
                                th.Property("options", th.StringType),
                                th.Property("values", th.ArrayType(th.StringType)),
                                th.Property("isRefused", th.BooleanType),
                                th.Property("refusalReason", th.StringType),
                            )
                        ),
                    ),
                )
            ),
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/forms/v2/tenant/{self._tap.config['tenant_id']}/submissions"
