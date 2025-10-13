"""Accounting streams for the ServiceTitan tap."""

from __future__ import annotations

import sys
import typing as t
from functools import cached_property

from singer_sdk import StreamSchema

from tap_service_titan.client import ServiceTitanExportStream, ServiceTitanStream
from tap_service_titan.openapi_specs import ACCOUNTING

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if t.TYPE_CHECKING:
    from singer_sdk.helpers.types import Context, Record


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
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = StreamSchema(ACCOUNTING, key="Accounting.V2.ExportPaymentResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self.tenant_id}/export/payments"


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
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = StreamSchema(ACCOUNTING, key="Accounting.V2.ApCreditResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self.tenant_id}/ap-credits"


class ApPaymentsStream(ServiceTitanStream):
    """Define ap payment stream."""

    name = "ap_payments"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = StreamSchema(ACCOUNTING, key="Accounting.V2.ApPaymentResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self.tenant_id}/ap-payments"


class PaymentTermsStream(ServiceTitanStream):
    """Define payment terms stream."""

    name = "payment_terms"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = StreamSchema(ACCOUNTING, key="Accounting.V2.PaymentTermAPIModel")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self.tenant_id}/payment-terms"


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
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = StreamSchema(ACCOUNTING, key="Accounting.V2.TaxZoneResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self.tenant_id}/tax-zones"


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

    @override
    def post_process(self, row: Record, context: Context | None = None) -> Record:
        """Post-process the record."""
        row = super().post_process(row, context)
        if (post_date := row.get("postDate")) and isinstance(post_date, str):
            row["postDate"] = post_date.split("T")[0]
        return row


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

    @override
    def post_process(self, row: Record, context: Context | None = None) -> Record:
        """Post-process the record."""
        row = super().post_process(row, context)
        if (post_date := row.get("postDate")) and isinstance(post_date, str):
            row["postDate"] = post_date.split("T")[0]
        return row


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

    @override
    def post_process(self, row: Record, context: Context | None = None) -> Record:
        """Post-process the record."""
        row = super().post_process(row, context)
        if (post_date := row.get("postDate")) and isinstance(post_date, str):
            row["postDate"] = post_date.split("T")[0]
        return row


class InventoryBillsCustomFieldsStream(ServiceTitanStream):
    """Define inventory bills custom fields stream."""

    name = "inventory_bills_custom_fields"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = StreamSchema(ACCOUNTING, key="Accounting.V2.CustomFieldTypeResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self.tenant_id}/inventory-bills/custom-fields"


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
