"""Equipment systems streams for the ServiceTitan tap."""

from __future__ import annotations

import typing as t
from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_service_titan.client import (
    ServiceTitanStream,
)


class InstalledEquipmentStream(ServiceTitanStream):
    """Define installed equipment stream."""

    name = "installed_equipment"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("equipmentId", th.IntegerType),
        th.Property("locationId", th.IntegerType),
        th.Property("customerId", th.IntegerType),
        th.Property("invoiceItemId", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("installedOn", th.DateTimeType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("serialNumber", th.StringType),
        th.Property("barcodeId", th.StringType),
        th.Property("memo", th.StringType),
        th.Property("manufacturer", th.StringType),
        th.Property("model", th.StringType),
        th.Property("cost", th.NumberType),
        th.Property("manufacturerWarrantyStart", th.DateTimeType),
        th.Property("manufacturerWarrantyEnd", th.DateTimeType),
        th.Property("serviceProviderWarrantyStart", th.DateTimeType),
        th.Property("serviceProviderWarrantyEnd", th.DateTimeType),
        th.Property(
            "tags",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property("ownerId", th.IntegerType),
                    th.Property("typeId", th.IntegerType),
                    th.Property("typeName", th.StringType),
                    th.Property("memo", th.StringType),
                    th.Property("color", th.StringType),
                    th.Property("textColor", th.StringType),
                    th.Property("code", th.StringType),
                )
            ),
        ),
        th.Property("actualReplacementDate", th.DateType),
        th.Property("predictedReplacementMonths", th.IntegerType),
        th.Property("predictedReplacementDate", th.DateType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/equipmentsystems/v2/tenant/{self._tap.config['tenant_id']}/installed-equipment"
