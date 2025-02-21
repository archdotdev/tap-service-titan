"""Accounting streams for the ServiceTitan tap."""

from __future__ import annotations

import typing as t
from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers
import logging

from tap_service_titan.client import (
    ServiceTitanExportStream,
    ServiceTitanStream,
)


class InvoicesStream(ServiceTitanExportStream):
    """Define invoices stream."""

    name = "invoices"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("syncStatus", th.StringType),
        th.Property("summary", th.StringType),
        th.Property("referenceNumber", th.StringType),
        th.Property("invoiceDate", th.DateTimeType),
        th.Property("dueDate", th.DateTimeType),
        th.Property("subTotal", th.StringType),
        th.Property("salesTax", th.StringType),
        th.Property(
            "salesTaxCode",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
                th.Property("taxRate", th.NumberType),
            ),
        ),
        th.Property("total", th.StringType),
        th.Property("balance", th.StringType),
        th.Property(
            "invoiceType",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "customer",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "customerAddress",
            th.ObjectType(
                th.Property("street", th.StringType),
                th.Property("unit", th.StringType),
                th.Property("city", th.StringType),
                th.Property("state", th.StringType),
                th.Property("zip", th.StringType),
                th.Property("country", th.StringType),
            ),
        ),
        th.Property(
            "location",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "locationAddress",
            th.ObjectType(
                th.Property("street", th.StringType),
                th.Property("unit", th.StringType),
                th.Property("city", th.StringType),
                th.Property("state", th.StringType),
                th.Property("zip", th.StringType),
                th.Property("country", th.StringType),
            ),
        ),
        th.Property(
            "businessUnit",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property("termName", th.StringType),
        th.Property("createdBy", th.StringType),
        th.Property(
            "batch",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("number", th.StringType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property("depositedOn", th.DateTimeType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("adjustmentToId", th.IntegerType),
        th.Property(
            "job",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("number", th.StringType),
                th.Property("type", th.StringType),
            ),
        ),
        th.Property("projectId", th.IntegerType),
        th.Property(
            "royalty",
            th.ObjectType(
                th.Property("status", th.StringType),
                th.Property("date", th.DateTimeType),
                th.Property("sentOn", th.DateTimeType),
                th.Property("memo", th.StringType),
            ),
        ),
        th.Property(
            "employeeInfo",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
                th.Property("modifiedOn", th.DateTimeType),
            ),
        ),
        th.Property("commissionEligibilityDate", th.StringType),
        th.Property("sentStatus", th.StringType),
        th.Property("reviewStatus", th.StringType),
        th.Property(
            "assignedTo",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "items",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property("description", th.StringType),
                    th.Property("quantity", th.StringType),
                    th.Property("cost", th.StringType),
                    th.Property("totalCost", th.StringType),
                    th.Property("inventoryLocation", th.StringType),
                    th.Property("price", th.StringType),
                    th.Property("type", th.StringType),
                    th.Property("skuName", th.StringType),
                    th.Property("skuId", th.IntegerType),
                    th.Property("total", th.StringType),
                    th.Property("inventory", th.BooleanType),
                    th.Property("taxable", th.BooleanType),
                    th.Property(
                        "generalLedgerAccount",
                        th.ObjectType(
                            th.Property("id", th.IntegerType),
                            th.Property("name", th.StringType),
                            th.Property("number", th.StringType),
                            th.Property("type", th.StringType),
                            th.Property("detailType", th.StringType),
                        ),
                    ),
                    th.Property(
                        "costOfSaleAccount",
                        th.ObjectType(
                            th.Property("id", th.IntegerType),
                            th.Property("name", th.StringType),
                            th.Property("number", th.StringType),
                            th.Property("type", th.StringType),
                            th.Property("detailType", th.StringType),
                        ),
                    ),
                    th.Property(
                        "assetAccount",
                        th.ObjectType(
                            th.Property("id", th.IntegerType),
                            th.Property("name", th.StringType),
                            th.Property("number", th.StringType),
                            th.Property("type", th.StringType),
                            th.Property("detailType", th.StringType),
                        ),
                    ),
                    th.Property("membershipTypeId", th.IntegerType),
                    th.Property(
                        "itemGroup",
                        th.ObjectType(
                            th.Property("rootId", th.IntegerType),
                            th.Property("name", th.StringType),
                        ),
                    ),
                    th.Property("displayName", th.StringType),
                    th.Property("soldHours", th.NumberType),
                    th.Property("modifiedOn", th.DateTimeType),
                    th.Property("serviceDate", th.DateTimeType),
                    th.Property("order", th.IntegerType),
                    th.Property(
                        "businessUnit",
                        th.ObjectType(
                            th.Property("id", th.IntegerType),
                            th.Property("name", th.StringType),
                        ),
                    ),
                )
            ),
        ),
        th.Property(
            "customFields",
            th.ArrayType(
                th.ObjectType(
                    th.Property("name", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self._tap.config['tenant_id']}/export/invoices"


class InvoiceItemsStream(ServiceTitanExportStream):
    """Define invoice items stream."""

    name = "invoice_items"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("description", th.StringType),
        th.Property("quantity", th.StringType),
        th.Property("cost", th.StringType),
        th.Property("totalCost", th.StringType),
        th.Property("inventoryLocation", th.StringType),
        th.Property("price", th.StringType),
        th.Property("type", th.StringType),
        th.Property("skuName", th.StringType),
        th.Property("skuId", th.IntegerType),
        th.Property("total", th.StringType),
        th.Property("inventory", th.BooleanType),
        th.Property("taxable", th.BooleanType),
        th.Property(
            "generalLedgerAccount",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
                th.Property("number", th.StringType),
                th.Property("type", th.StringType),
                th.Property("detailType", th.StringType),
            ),
        ),
        th.Property(
            "costOfSaleAccount",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
                th.Property("number", th.StringType),
                th.Property("type", th.StringType),
                th.Property("detailType", th.StringType),
            ),
        ),
        th.Property(
            "assetAccount",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
                th.Property("number", th.StringType),
                th.Property("type", th.StringType),
                th.Property("detailType", th.StringType),
            ),
        ),
        th.Property("membershipTypeId", th.IntegerType),
        th.Property(
            "itemGroup",
            th.ObjectType(
                th.Property("rootId", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property("displayName", th.StringType),
        th.Property("soldHours", th.NumberType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("serviceDate", th.DateTimeType),
        th.Property("order", th.IntegerType),
        th.Property(
            "businessUnit",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property("active", th.BooleanType),
        th.Property("invoiceId", th.IntegerType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self._tap.config['tenant_id']}/export/invoice-items"  # noqa: E501


class PaymentsStream(ServiceTitanExportStream):
    """Define payments stream."""

    name = "payments"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("syncStatus", th.StringType),
        th.Property("referenceNumber", th.StringType),
        th.Property("date", th.DateTimeType),
        th.Property("type", th.StringType),
        th.Property("typeId", th.StringType),
        th.Property("total", th.StringType),
        th.Property("unappliedAmount", th.StringType),
        th.Property("memo", th.StringType),
        th.Property(
            "customer",
            th.ObjectType(
                th.Property("id", th.IntegerType), th.Property("name", th.StringType)
            ),
        ),
        th.Property(
            "businessUnit",
            th.ObjectType(
                th.Property("id", th.IntegerType), th.Property("name", th.StringType)
            ),
        ),
        th.Property(
            "batch",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("number", th.StringType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property("createdBy", th.StringType),
        th.Property(
            "generalLedgerAccount",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
                th.Property("number", th.StringType),
                th.Property("type", th.StringType),
                th.Property("detailType", th.StringType),
            ),
        ),
        th.Property(
            "appliedTo",
            th.ArrayType(
                th.ObjectType(
                    th.Property("appliedId", th.IntegerType),
                    th.Property("appliedTo", th.IntegerType),
                    th.Property("appliedAmount", th.StringType),
                    th.Property("appliedOn", th.DateTimeType),
                    th.Property("appliedBy", th.StringType),
                    th.Property("appliedToReferenceNumber", th.StringType),
                )
            ),
        ),
        th.Property(
            "customFields",
            th.ArrayType(
                th.ObjectType(
                    th.Property("name", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
        th.Property("authCode", th.StringType),
        th.Property("checkNumber", th.StringType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self._tap.config['tenant_id']}/export/payments"


class InventoryBillsStream(ServiceTitanExportStream):
    """Define inventory bills stream."""

    name = "inventory_bills"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "createdOn"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("purchaseOrderId", th.IntegerType),
        th.Property("syncStatus", th.StringType),
        th.Property("referenceNumber", th.StringType),
        th.Property("vendorNumber", th.StringType),
        th.Property("summary", th.StringType),
        th.Property("billDate", th.DateTimeType),
        th.Property("billAmount", th.StringType),
        th.Property("taxAmount", th.StringType),
        th.Property("shippingAmount", th.StringType),
        th.Property("createdBy", th.StringType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("termName", th.StringType),
        th.Property("dueDate", th.DateTimeType),
        th.Property("shipToDescription", th.StringType),
        th.Property(
            "batch",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("number", th.StringType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "businessUnit",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "vendor",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
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
        th.Property(
            "items",
            th.ArrayType(
                th.ObjectType(
                    th.Property("order", th.IntegerType),
                    th.Property("name", th.StringType),
                    th.Property("description", th.StringType),
                    th.Property("quantity", th.StringType),
                    th.Property("cost", th.StringType),
                    th.Property("inventoryLocation", th.StringType),
                    th.Property("serialNumber", th.StringType),
                    th.Property(
                        "generalLedgerAccount",
                        th.ObjectType(
                            th.Property("id", th.IntegerType),
                            th.Property("name", th.StringType),
                            th.Property("number", th.StringType),
                            th.Property("type", th.StringType),
                            th.Property("detailType", th.StringType),
                        ),
                    ),
                    th.Property(
                        "costOfSaleAccount",
                        th.ObjectType(
                            th.Property("id", th.IntegerType),
                            th.Property("name", th.StringType),
                            th.Property("number", th.StringType),
                            th.Property("type", th.StringType),
                            th.Property("detailType", th.StringType),
                        ),
                    ),
                    th.Property(
                        "assetAccount",
                        th.ObjectType(
                            th.Property("id", th.IntegerType),
                            th.Property("name", th.StringType),
                            th.Property("number", th.StringType),
                            th.Property("type", th.StringType),
                            th.Property("detailType", th.StringType),
                        ),
                    ),
                    th.Property("skuId", th.IntegerType),
                    th.Property("skuCode", th.StringType),
                )
            ),
        ),
        th.Property(
            "customFields",
            th.ArrayType(
                th.ObjectType(
                    th.Property("name", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
        th.Property("jobId", th.IntegerType),
        th.Property("jobNumber", th.StringType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self._tap.config['tenant_id']}/export/inventory-bills"


class ApCreditsStream(ServiceTitanStream):
    """Define ap credits stream."""

    name = "ap_credits"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("inventoryReturnId", th.IntegerType),
        th.Property("jobId", th.IntegerType),
        th.Property("active", th.BooleanType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("date", th.DateTimeType),
        th.Property("canceledOn", th.DateTimeType),
        th.Property("number", th.StringType),
        th.Property("referenceNumber", th.StringType),
        th.Property("memo", th.StringType),
        th.Property("amount", th.NumberType),
        th.Property("appliedAmount", th.NumberType),
        th.Property("status", th.StringType),
        th.Property("syncStatus", th.StringType),
        th.Property(
            "batch",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("number", th.StringType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "businessUnit",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "remittanceVendor",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "vendor",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property("paymentStatus", th.StringType),
        th.Property(
            "splits",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property("active", th.BooleanType),
                    th.Property("createdOn", th.DateTimeType),
                    th.Property("inventoryBillId", th.IntegerType),
                    th.Property("vendorCreditId", th.IntegerType),
                    th.Property("amount", th.NumberType),
                )
            ),
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self._tap.config['tenant_id']}/ap-credits"


class ApPaymentsStream(ServiceTitanStream):
    """Define ap payment stream."""

    name = "ap_payments"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("active", th.BooleanType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("date", th.DateTimeType),
        th.Property("approvedDate", th.DateTimeType),
        th.Property("method", th.StringType),
        th.Property("name", th.StringType),
        th.Property("printCheck", th.BooleanType),
        th.Property("amount", th.NumberType),
        th.Property("errorMessage", th.StringType),
        th.Property("status", th.StringType),
        th.Property("syncStatus", th.StringType),
        th.Property(
            "batch",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("number", th.StringType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "glAccount",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
                th.Property("number", th.StringType),
                th.Property("type", th.StringType),
                th.Property("detailType", th.StringType),
            ),
        ),
        th.Property(
            "businessUnit",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "vendor",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "remittanceVendor",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "splits",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property("active", th.BooleanType),
                    th.Property("createdOn", th.DateTimeType),
                    th.Property("documentId", th.IntegerType),
                    th.Property("inventoryBillId", th.IntegerType),
                    th.Property("amount", th.NumberType),
                )
            ),
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self._tap.config['tenant_id']}/ap-payments"


class PaymentTermsStream(ServiceTitanStream):
    """Define payment terms stream."""

    name = "payment_terms"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("dueDayType", th.StringType),
        th.Property("dueDay", th.IntegerType),
        th.Property("isCustomerDefault", th.BooleanType),
        th.Property("isVendorDefault", th.BooleanType),
        th.Property("active", th.BooleanType),
        th.Property("inUse", th.BooleanType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property(
            "paymentTermDiscountModel",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("discountApplyTo", th.StringType),
                th.Property("discount", th.NumberType),
                th.Property("discountType", th.StringType),
                th.Property("account", th.StringType),
                th.Property("applyBy", th.StringType),
                th.Property("applyByValue", th.IntegerType),
            ),
        ),
        th.Property(
            "interestSettings",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("rateType", th.StringType),
                th.Property("flatRateValue", th.NumberType),
                th.Property("percentageRateValue", th.NumberType),
                th.Property("chargeMethod", th.StringType),
                th.Property("frequency", th.StringType),
                th.Property("gracePeriod", th.IntegerType),
                th.Property("targetInvoices", th.ArrayType(th.StringType)),
                th.Property("taskId", th.IntegerType),
                th.Property("taskDisplayName", th.StringType),
            ),
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self._tap.config['tenant_id']}/payment-terms"


class PaymentTypesStream(ServiceTitanStream):
    """Define payment types stream."""

    name = "payment_types"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("modifiedOn", th.DateTimeType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self._tap.config['tenant_id']}/payment-types"


class TaxZonesStream(ServiceTitanStream):
    """Define tax zones stream."""

    name = "tax_zones"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("color", th.IntegerType),
        th.Property("isTaxRateSeparated", th.BooleanType),
        th.Property("isMultipleTaxZone", th.BooleanType),
        th.Property(
            "rates",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property("taxName", th.StringType),
                    th.Property("taxBaseType", th.ArrayType(th.StringType)),
                    th.Property("taxRate", th.NumberType),
                    th.Property("salesTaxItem", th.StringType),
                )
            ),
        ),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self._tap.config['tenant_id']}/tax-zones"


class PageSizeLimitMixin:
    def get_url_params(
        self,
        context: dict | None,
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params = super().get_url_params(context, next_page_token)
        # This endpoint has an undocumented max page size of 500
        params["pageSize"] = 500
        return params


class JournalEntriesStream(PageSizeLimitMixin, ServiceTitanStream):
    """Define journal entries stream."""

    name = "journal_entries"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("number", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("status", th.StringType),
        th.Property("postDate", th.DateTimeType),
        th.Property("exportedOn", th.DateTimeType),
        th.Property(
            "exportedBy",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "customFields",
            th.ArrayType(
                th.ObjectType(
                    th.Property("name", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
        th.Property("url", th.StringType),
    ).to_dict()

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params = super().get_url_params(context, next_page_token)
        # Some endpoints have an undocumented max page size of 500
        params["pageSize"] = 500
        return params

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self._tap.config['tenant_id']}/journal-entries"

    def get_child_context(self, record: dict, context: dict | None) -> dict:
        """Return a context dictionary for a child stream."""
        return {"journal_entry_id": record["id"]}


class JournalEntrySummaryStream(PageSizeLimitMixin, ServiceTitanStream):
    """Define journal entry summary stream."""

    name = "journal_entry_summaries"
    primary_keys: t.ClassVar[list[str]] = []
    replication_key: str | None = None
    parent_stream_type = JournalEntriesStream
    ignore_parent_replication_key = True

    schema = th.PropertiesList(
        th.Property("postDate", th.DateTimeType),
        th.Property(
            "account",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("number", th.StringType),
                th.Property("name", th.StringType),
                th.Property("type", th.StringType),
                th.Property("subtype", th.StringType),
            ),
        ),
        th.Property("credit", th.NumberType),
        th.Property("debit", th.NumberType),
        th.Property("memo", th.StringType),
        th.Property(
            "businessUnit",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self._tap.config['tenant_id']}/journal-entries/{'{journal_entry_id}'}/summary"


class JournalEntryDetailsStream(PageSizeLimitMixin, ServiceTitanStream):
    """Define journal entry details stream."""

    name = "journal_entry_details"
    primary_keys: t.ClassVar[list[str]] = []
    replication_key: str | None = None
    parent_stream_type = JournalEntriesStream
    ignore_parent_replication_key = True

    schema = th.PropertiesList(
        th.Property("postDate", th.DateTimeType),
        th.Property(
            "account",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("number", th.StringType),
                th.Property("name", th.StringType),
                th.Property("type", th.StringType),
                th.Property("subtype", th.StringType),
            ),
        ),
        th.Property("debit", th.NumberType),
        th.Property("credit", th.NumberType),
        th.Property("memo", th.StringType),
        th.Property(
            "transaction",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("type", th.StringType),
                th.Property("refNumber", th.StringType),
            ),
        ),
        th.Property(
            "businessUnit",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "customer",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "vendor",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "inventoryLocation",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "job",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("number", th.StringType),
            ),
        ),
        th.Property(
            "customerLocation",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "paymentType",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "project",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("number", th.StringType),
            ),
        ),
        th.Property(
            "serviceAgreement",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("number", th.StringType),
            ),
        ),
        th.Property(
            "appliedTo",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("type", th.StringType),
                th.Property("refNumber", th.StringType),
            ),
        ),
        th.Property(
            "sku",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("type", th.StringType),
                th.Property("code", th.StringType),
            ),
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self._tap.config['tenant_id']}/journal-entries/{'{journal_entry_id}'}/details"


class GLAccountsStream(ServiceTitanStream):
    """Define GL accounts stream."""

    name = "gl_accounts"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType, required=False),
        th.Property("number", th.StringType, required=False),
        th.Property("description", th.StringType, required=False),
        th.Property("type", th.StringType, required=False),
        th.Property("subtype", th.StringType, required=False),
        th.Property("isActive", th.BooleanType, required=False),
        th.Property("isIntacctGroup", th.BooleanType, required=False),
        th.Property("isIntacctBankAccount", th.BooleanType, required=False),
        th.Property("source", th.StringType, required=False),
        th.Property("createdOn", th.DateTimeType, required=False),
        th.Property("modifiedOn", th.DateTimeType, required=False),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self._tap.config['tenant_id']}/gl-accounts"
