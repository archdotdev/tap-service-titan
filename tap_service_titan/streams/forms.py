"""Forms streams for the ServiceTitan tap."""

from __future__ import annotations

import typing as t
from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk.helpers.types import Context  # noqa: TCH002

from tap_service_titan.client import (
    ServiceTitanStream,
)
from tap_service_titan.streams.jpm import JobsStream


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

    def get_records(self, context: Context | None) -> t.Iterable[dict[str, t.Any]]:
        """Return a generator of record-type dictionary objects with coerced values.

        Args:
            context: Stream partition or context dictionary.

        Yields:
            One item per record with string coercion only in the units section.
        """

        def coerce_value(value: t.Any) -> str | None:
            """Convert value to string if it has content, else None."""
            if value is None or value == "":
                return None
            return str(value)

        def process_units(units_data: dict) -> dict:
            """Recursively process units dictionary values."""
            result = {}
            for key, value in units_data.items():
                if isinstance(value, dict):
                    result[key] = process_units(value)
                elif isinstance(value, list):
                    result[key] = [
                        process_units(item)
                        if isinstance(item, dict)
                        else coerce_value(item)
                        for item in value
                    ]
                else:
                    result[key] = coerce_value(value)
            return result

        # Get records from parent class implementation
        parent_records = super().get_records(context)

        # Process each record
        for record in parent_records:
            if "units" in record:
                # Only process the units section, leaving the rest of the record unchanged
                record["units"] = [process_units(unit) for unit in record["units"]]
            yield record


class JobAttachmentsStream(ServiceTitanStream):
    """Define forms stream."""

    name = "job_attachments"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "createdOn"
    parent_stream_type = JobsStream

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("fileName", th.StringType),
        th.Property("createdById", th.IntegerType),
        th.Property("createdOn", th.DateTimeType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/forms/v2/tenant/{self._tap.config['tenant_id']}/jobs/{'{job_id}'}/attachments"
