"""Sales and estimates streams for the ServiceTitan tap."""

from __future__ import annotations

import typing as t
from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_service_titan.client import (
    ServiceTitanExportStream,
)


class EstimatesStream(ServiceTitanExportStream):
    """Define estimates stream."""

    name = "estimates"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("jobId", th.IntegerType),
        th.Property("projectId", th.IntegerType),
        th.Property("locationId", th.IntegerType),
        th.Property("customerId", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("jobNumber", th.StringType),
        th.Property(
            "status",
            th.ObjectType(
                th.Property("value", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property("reviewStatus", th.StringType),
        th.Property("summary", th.StringType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("soldOn", th.DateTimeType),
        th.Property("soldBy", th.IntegerType),
        th.Property("active", th.BooleanType),
        th.Property(
            "items",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property(
                        "sku",
                        th.ObjectType(
                            th.Property("id", th.IntegerType),
                            th.Property("name", th.StringType),
                            th.Property("displayName", th.StringType),
                            th.Property("type", th.StringType),
                            th.Property("soldHours", th.NumberType),
                            th.Property("generalLedgerAccountId", th.IntegerType),
                            th.Property("generalLedgerAccountName", th.StringType),
                            th.Property("modifiedOn", th.DateTimeType),
                        ),
                    ),
                    th.Property("skuAccount", th.StringType),
                    th.Property("description", th.StringType),
                    th.Property("membershipTypeId", th.IntegerType),
                    th.Property("qty", th.NumberType),
                    th.Property("unitRate", th.NumberType),
                    th.Property("total", th.NumberType),
                    th.Property("unitCost", th.NumberType),
                    th.Property("totalCost", th.NumberType),
                    th.Property("itemGroupName", th.StringType),
                    th.Property("itemGroupRootId", th.IntegerType),
                    th.Property("createdOn", th.DateTimeType),
                    th.Property("modifiedOn", th.DateTimeType),
                    th.Property("chargeable", th.BooleanType),
                ),
            ),
        ),
        th.Property(
            "externalLinks",
            th.ArrayType(
                th.ObjectType(
                    th.Property("name", th.StringType),
                    th.Property("url", th.StringType),
                )
            ),
        ),
        th.Property("subtotal", th.NumberType),
        th.Property("businessUnitId", th.IntegerType),
        th.Property("businessUnitName", th.StringType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/sales/v2/tenant/{self._tap.config['tenant_id']}/estimates/export"
