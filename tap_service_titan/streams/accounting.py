"""Accounting streams for the ServiceTitan tap."""

from __future__ import annotations

import sys
import typing as t
from functools import cached_property

from singer_sdk import StreamSchema
from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_service_titan.client import ServiceTitanExportStream, ServiceTitanStream
from tap_service_titan.openapi_specs import ACCOUNTING

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if t.TYPE_CHECKING:
    from singer_sdk.helpers.types import Context


class InvoicesStream(ServiceTitanExportStream):
    """Define invoices stream."""

    name = "invoices"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = StreamSchema(ACCOUNTING, key="Accounting.V2.ExportInvoiceResponse")

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self.tenant_id}/export/invoices"


class InvoiceItemsStream(ServiceTitanExportStream):
    """Define invoice items stream."""

    name = "invoice_items"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = StreamSchema(ACCOUNTING, key="Accounting.V2.ExportInvoiceItemResponse")

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self.tenant_id}/export/invoice-items"


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
    primary_keys = ("id",)
    replication_key: str = "createdOn"
    schema = StreamSchema(ACCOUNTING, key="Accounting.V2.ExportInventoryBillResponse")

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self.tenant_id}/export/inventory-bills"


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
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = StreamSchema(ACCOUNTING, key="Accounting.V2.PaymentTypeResponse")

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self.tenant_id}/payment-types"


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
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = StreamSchema(ACCOUNTING, key="Accounting.V2.JournalEntryResponse")

    @override
    def get_url_params(
        self,
        context: dict | None,
        next_page_token: t.Any | None,
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

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self.tenant_id}/journal-entries"

    @override
    def get_child_context(self, record: dict, context: Context | None) -> dict:
        """Return a context dictionary for a child stream."""
        return {"journal_entry_id": record["id"]}


class JournalEntrySummaryStream(PageSizeLimitMixin, ServiceTitanStream):
    """Define journal entry summary stream."""

    name = "journal_entry_summaries"
    primary_keys = ()
    replication_key: str | None = None
    parent_stream_type = JournalEntriesStream
    ignore_parent_replication_key = True
    schema = StreamSchema(ACCOUNTING, key="Accounting.V2.JournalEntrySummaryResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self.tenant_id}/journal-entries/{{journal_entry_id}}/summary"  # noqa: E501


class JournalEntryDetailsStream(PageSizeLimitMixin, ServiceTitanStream):
    """Define journal entry details stream."""

    name = "journal_entry_details"
    primary_keys = ()
    replication_key: str | None = None
    parent_stream_type = JournalEntriesStream
    ignore_parent_replication_key = True
    schema = StreamSchema(ACCOUNTING, key="Accounting.V2.JournalEntryDetailsResponse")

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self.tenant_id}/journal-entries/{{journal_entry_id}}/details"  # noqa: E501


class InventoryBillsCustomFieldsStream(ServiceTitanStream):
    """Define inventory bills custom fields stream."""

    name = "inventory_bills_custom_fields"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("displayName", th.StringType),
        th.Property("dataType", th.StringType),
        th.Property("required", th.BooleanType),
        th.Property("enabled", th.BooleanType),
        th.Property("allowOnBulkUpdate", th.BooleanType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self._tap.config['tenant_id']}/inventory-bills/custom-fields"


class GLAccountsStream(ServiceTitanStream):
    """Define GL accounts stream."""

    name = "gl_accounts"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = StreamSchema(ACCOUNTING, key="Accounting.V2.GlAccountExtendedResponse")

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self.tenant_id}/gl-accounts"
