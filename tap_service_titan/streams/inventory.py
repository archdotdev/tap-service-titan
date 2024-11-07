"""Inventory streams for the ServiceTitan tap."""

from __future__ import annotations

import typing as t
from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_service_titan.client import (
    ServiceTitanExportStream,
    ServiceTitanStream,
)


class PurchaseOrdersStream(ServiceTitanExportStream):
    """Define purchase orders stream."""

    name = "purchase_orders"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("number", th.StringType),
        th.Property("invoiceId", th.IntegerType),
        th.Property("jobId", th.IntegerType),
        th.Property("projectId", th.IntegerType),
        th.Property("status", th.StringType),
        th.Property("typeId", th.IntegerType),
        th.Property("vendorId", th.IntegerType),
        th.Property("technicianId", th.IntegerType),
        th.Property(
            "shipTo",
            th.ObjectType(
                th.Property("street", th.StringType),
                th.Property("unit", th.StringType),
                th.Property("city", th.StringType),
                th.Property("state", th.StringType),
                th.Property("zip", th.StringType),
                th.Property("country", th.StringType),
            ),
        ),
        th.Property("businessUnitId", th.IntegerType),
        th.Property("inventoryLocationId", th.IntegerType),
        th.Property("batchId", th.IntegerType),
        th.Property("vendorDocumentNumber", th.StringType),
        th.Property("date", th.StringType),
        th.Property("requiredOn", th.StringType),
        th.Property("sentOn", th.StringType),
        th.Property("receivedOn", th.StringType),
        th.Property("createdOn", th.StringType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("total", th.NumberType),
        th.Property("tax", th.NumberType),
        th.Property("shipping", th.NumberType),
        th.Property("summary", th.StringType),
        th.Property(
            "items",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property("skuId", th.IntegerType),
                    th.Property("skuName", th.StringType),
                    th.Property("skuCode", th.StringType),
                    th.Property("skuType", th.StringType),
                    th.Property("description", th.StringType),
                    th.Property("vendorPartNumber", th.StringType),
                    th.Property("quantity", th.NumberType),
                    th.Property("quantityReceived", th.NumberType),
                    th.Property("cost", th.NumberType),
                    th.Property("total", th.NumberType),
                    th.Property(
                        "serialNumbers",
                        th.ArrayType(
                            th.ObjectType(
                                th.Property("id", th.IntegerType),
                                th.Property("number", th.StringType),
                            )
                        ),
                    ),
                    th.Property("status", th.StringType),
                    th.Property("chargeable", th.BooleanType),
                )
            ),
        ),
        th.Property(
            "customFields",
            th.ArrayType(
                th.ObjectType(
                    th.Property("typeId", th.IntegerType),
                    th.Property("name", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/inventory/v2/tenant/{self._tap.config['tenant_id']}/export/purchase-orders"  # noqa: E501


class PurchaseOrderMarkupsStream(ServiceTitanStream):
    """Define purchase order markups stream."""

    name = "purchase_order_markups"
    primary_keys: t.ClassVar[list[str]] = ["id"]

    schema = th.PropertiesList(
        th.Property("from", th.NumberType),
        th.Property("to", th.NumberType),
        th.Property("percent", th.NumberType),
        th.Property("id", th.IntegerType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/inventory/v2/tenant/{self._tap.config['tenant_id']}/purchase-order-markups"  # noqa: E501


class PurchaseOrderTypesStream(ServiceTitanStream):
    """Define purchase order types stream."""

    name = "purchase_order_types"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("active", th.BooleanType),
        th.Property("automaticallyReceive", th.BooleanType),
        th.Property("displayToTechnician", th.BooleanType),
        th.Property("impactToTechnicianPayroll", th.BooleanType),
        th.Property("allowTechniciansToSendPo", th.BooleanType),
        th.Property("defaultRequiredDateDaysOffset", th.IntegerType),
        th.Property("skipWeekends", th.BooleanType),
        th.Property("excludeTaxFromJobCosting", th.BooleanType),
        th.Property("createdOn", th.StringType),
        th.Property("modifiedOn", th.DateTimeType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return (
            f"/inventory/v2/tenant/{self._tap.config['tenant_id']}/purchase-order-types"
        )


class ReceiptsStream(ServiceTitanStream):
    """Define receipts stream."""

    name = "receipts"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("active", th.BooleanType),
        th.Property("number", th.StringType),
        th.Property("vendorInvoiceNumber", th.StringType),
        th.Property("createdById", th.IntegerType),
        th.Property("memo", th.StringType),
        th.Property("purchaseOrderId", th.IntegerType),
        th.Property("billId", th.IntegerType),
        th.Property("jobId", th.IntegerType),
        th.Property("businessUnitId", th.IntegerType),
        th.Property("vendorId", th.IntegerType),
        th.Property("technicianId", th.IntegerType),
        th.Property("inventoryLocationId", th.IntegerType),
        th.Property(
            "shipTo",
            th.ObjectType(
                th.Property("street", th.StringType),
                th.Property("unit", th.StringType),
                th.Property("city", th.StringType),
                th.Property("state", th.StringType),
                th.Property("zip", th.StringType),
                th.Property("country", th.StringType),
            ),
        ),
        th.Property("shipToDescription", th.StringType),
        th.Property("receiptAmount", th.NumberType),
        th.Property("taxAmount", th.NumberType),
        th.Property("shippingAmount", th.NumberType),
        th.Property("receivedOn", th.DateTimeType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("batchId", th.IntegerType),
        th.Property("syncStatus", th.StringType),
        th.Property(
            "items",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property("skuId", th.IntegerType),
                    th.Property("name", th.StringType),
                    th.Property("code", th.StringType),
                    th.Property("description", th.StringType),
                    th.Property("quantity", th.NumberType),
                    th.Property("cost", th.NumberType),
                    th.Property(
                        "generalLedgerAccount",
                        th.ObjectType(
                            th.Property("name", th.StringType),
                            th.Property("number", th.StringType),
                            th.Property("type", th.StringType),
                            th.Property("detailType", th.StringType),
                        ),
                    ),
                    th.Property(
                        "costOfSaleAccount",
                        th.ObjectType(
                            th.Property("name", th.StringType),
                            th.Property("number", th.StringType),
                            th.Property("type", th.StringType),
                            th.Property("detailType", th.StringType),
                        ),
                    ),
                    th.Property(
                        "assetAccount",
                        th.ObjectType(
                            th.Property("name", th.StringType),
                            th.Property("number", th.StringType),
                            th.Property("type", th.StringType),
                            th.Property("detailType", th.StringType),
                        ),
                    ),
                )
            ),
        ),
        th.Property(
            "customFields",
            th.ArrayType(
                th.ObjectType(
                    th.Property("typeId", th.IntegerType),
                    th.Property("name", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/inventory/v2/tenant/{self._tap.config['tenant_id']}/receipts"


class ReturnsStream(ServiceTitanStream):
    """Define returns stream."""

    name = "returns"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("active", th.BooleanType),
        th.Property("number", th.StringType),
        th.Property("referenceNumber", th.StringType),
        th.Property("status", th.StringType),
        th.Property("vendorId", th.IntegerType),
        th.Property("purchaseOrderId", th.IntegerType),
        th.Property("jobId", th.IntegerType),
        th.Property("businessUnitId", th.IntegerType),
        th.Property("inventoryLocationId", th.IntegerType),
        th.Property("createdById", th.IntegerType),
        th.Property("memo", th.StringType),
        th.Property("returnAmount", th.NumberType),
        th.Property("taxAmount", th.NumberType),
        th.Property("shippingAmount", th.NumberType),
        th.Property("returnDate", th.DateTimeType),
        th.Property("returnedOn", th.DateTimeType),
        th.Property("creditReceivedOn", th.DateTimeType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("batchId", th.IntegerType),
        th.Property(
            "batch",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("number", th.StringType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property("syncStatus", th.ObjectType()),  # Empty object in the input
        th.Property(
            "items",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property("skuId", th.IntegerType),
                    th.Property("name", th.StringType),
                    th.Property("code", th.StringType),
                    th.Property("description", th.StringType),
                    th.Property("quantity", th.NumberType),
                    th.Property("cost", th.NumberType),
                    th.Property(
                        "generalLedgerAccount",
                        th.ObjectType(
                            th.Property("name", th.StringType),
                            th.Property("number", th.StringType),
                            th.Property("type", th.StringType),
                            th.Property("detailType", th.StringType),
                        ),
                    ),
                    th.Property(
                        "costOfSaleAccount",
                        th.ObjectType(
                            th.Property("name", th.StringType),
                            th.Property("number", th.StringType),
                            th.Property("type", th.StringType),
                            th.Property("detailType", th.StringType),
                        ),
                    ),
                    th.Property(
                        "assetAccount",
                        th.ObjectType(
                            th.Property("name", th.StringType),
                            th.Property("number", th.StringType),
                            th.Property("type", th.StringType),
                            th.Property("detailType", th.StringType),
                        ),
                    ),
                )
            ),
        ),
        th.Property(
            "customFields",
            th.ArrayType(
                th.ObjectType(
                    th.Property("typeId", th.IntegerType),
                    th.Property("name", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
        th.Property(
            "externalData",
            th.ArrayType(
                th.ObjectType(
                    th.Property("key", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/inventory/v2/tenant/{self._tap.config['tenant_id']}/returns"
