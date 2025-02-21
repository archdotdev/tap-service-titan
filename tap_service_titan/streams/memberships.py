"""Memberships streams for the ServiceTitan tap."""

from __future__ import annotations

import typing as t
from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_service_titan.client import ServiceTitanExportStream


class MembershipsStream(ServiceTitanExportStream):
    """Define memberships export stream."""

    name = "memberships_export"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("createdById", th.IntegerType, required=False),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("followUpOn", th.DateTimeType),
        th.Property("cancellationDate", th.DateTimeType, required=False),
        th.Property("from", th.DateTimeType, required=False),
        th.Property("nextScheduledBillDate", th.DateTimeType, required=False),
        th.Property("to", th.DateTimeType, required=False),
        th.Property("billingFrequency", th.StringType),
        th.Property("renewalBillingFrequency", th.StringType, required=False),
        th.Property("status", th.StringType),
        th.Property("followUpStatus", th.StringType),
        th.Property("active", th.BooleanType),
        th.Property("initialDeferredRevenue", th.NumberType),
        th.Property("duration", th.IntegerType, required=False),
        th.Property("renewalDuration", th.IntegerType, required=False),
        th.Property("businessUnitId", th.IntegerType),
        th.Property("customerId", th.IntegerType),
        th.Property("membershipTypeId", th.IntegerType),
        th.Property("activatedById", th.IntegerType, required=False),
        th.Property("activatedFromId", th.IntegerType, required=False),
        th.Property("billingTemplateId", th.IntegerType, required=False),
        th.Property("cancellationBalanceInvoiceId", th.IntegerType, required=False),
        th.Property("cancellationInvoiceId", th.IntegerType, required=False),
        th.Property("followUpCustomStatusId", th.IntegerType, required=False),
        th.Property("locationId", th.IntegerType, required=False),
        th.Property("paymentMethodId", th.IntegerType, required=False),
        th.Property("paymentTypeId", th.IntegerType, required=False),
        th.Property("recurringLocationId", th.IntegerType, required=False),
        th.Property("renewalMembershipTaskId", th.IntegerType, required=False),
        th.Property("renewedById", th.IntegerType, required=False),
        th.Property("soldById", th.IntegerType, required=False),
        th.Property("customerPo", th.StringType, required=False),
        th.Property("importId", th.StringType, required=False),
        th.Property("memo", th.StringType, required=False),
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
        return (
            f"/memberships/v2/tenant/{self._tap.config['tenant_id']}/export/memberships"
        )


class MembershipTypesStream(ServiceTitanExportStream):
    """Define membership types stream."""

    name = "membership_types"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("createdById", th.IntegerType, required=False),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("importId", th.StringType, required=False),
        th.Property("billingTemplateId", th.IntegerType, required=False),
        th.Property(
            "durationBilling",
            th.ArrayType(
                th.OneOf(
                    None,
                    th.ObjectType(
                        th.Property("duration", th.IntegerType, required=False),
                        th.Property("billingFrequency", th.StringType, required=True),
                        additional_properties=False,
                    ),
                )
            ),
            required=False,
        ),
        th.Property("name", th.StringType),
        th.Property("displayName", th.StringType, required=False),
        th.Property("active", th.BooleanType),
        th.Property("discountMode", th.StringType),
        th.Property("locationTarget", th.StringType),
        th.Property("revenueRecognitionMode", th.StringType),
        th.Property("autoCalculateInvoiceTemplates", th.BooleanType),
        th.Property("useMembershipPricingTable", th.BooleanType),
        th.Property("showMembershipSavings", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/memberships/v2/tenant/{self._tap.config['tenant_id']}/export/membership-types"


class RecurringServiceTypesStream(ServiceTitanExportStream):
    """Define recurring service types stream."""

    name = "recurring_service_types"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("createdById", th.IntegerType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("active", th.BooleanType),
        th.Property("recurrenceType", th.StringType),
        th.Property("recurrenceInterval", th.IntegerType),
        th.Property("recurrenceMonths", th.ArrayType(th.StringType)),
        th.Property("durationType", th.StringType),
        th.Property("durationLength", th.IntegerType),
        th.Property("invoiceTemplateId", th.IntegerType),
        th.Property("businessUnitId", th.IntegerType),
        th.Property("jobTypeId", th.IntegerType),
        th.Property("priority", th.StringType),
        th.Property("campaignId", th.IntegerType),
        th.Property("jobSummary", th.StringType),
        th.Property("name", th.StringType),
        th.Property("importId", th.StringType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/memberships/v2/tenant/{self._tap.config['tenant_id']}/export/recurring-service-types"


class InvoiceTemplatesStream(ServiceTitanExportStream):
    """Define invoice templates stream."""

    name = "invoice_templates"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("createdById", th.IntegerType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("active", th.BooleanType),
        th.Property("total", th.NumberType),
        th.Property("isSettingsTemplate", th.BooleanType),
        th.Property("importId", th.StringType),
        th.Property(
            "items",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property("skuId", th.IntegerType),
                    th.Property("skuType", th.StringType),
                    th.Property("quantity", th.NumberType),
                    th.Property("unitPrice", th.NumberType),
                    th.Property("isAddOn", th.BooleanType),
                    th.Property("importId", th.StringType),
                    th.Property("workflowActionItemId", th.IntegerType),
                    th.Property("description", th.StringType),
                    th.Property("cost", th.NumberType),
                    th.Property("hours", th.NumberType),
                )
            ),
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/memberships/v2/tenant/{self._tap.config['tenant_id']}/export/invoice-templates"


class RecurringServicesStream(ServiceTitanExportStream):
    """Define recurring services stream."""

    name = "recurring_services"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("active", th.BooleanType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("createdById", th.IntegerType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("importId", th.StringType),
        th.Property("membershipId", th.IntegerType),
        th.Property("locationId", th.IntegerType),
        th.Property("recurringServiceTypeId", th.IntegerType),
        th.Property("durationType", th.StringType),
        th.Property("durationLength", th.IntegerType),
        th.Property("from", th.DateTimeType),
        th.Property("to", th.DateTimeType),
        th.Property("memo", th.StringType),
        th.Property("invoiceTemplateId", th.IntegerType),
        th.Property("invoiceTemplateForFollowingYearsId", th.IntegerType),
        th.Property("firstVisitComplete", th.BooleanType),
        th.Property("activatedFromId", th.IntegerType),
        th.Property("allocation", th.NumberType),
        th.Property("businessUnitId", th.IntegerType),
        th.Property("jobTypeId", th.IntegerType),
        th.Property("campaignId", th.IntegerType),
        th.Property("priority", th.StringType),
        th.Property("jobSummary", th.StringType),
        th.Property("recurrenceType", th.StringType),
        th.Property("recurrenceInterval", th.IntegerType),
        th.Property("recurrenceMonths", th.ArrayType(th.StringType)),
        th.Property("recurrenceDaysOfWeek", th.ArrayType(th.StringType)),
        th.Property("recurrenceWeek", th.StringType),
        th.Property("recurrenceDayOfNthWeek", th.StringType),
        th.Property("recurrenceDaysOfMonth", th.ArrayType(th.IntegerType)),
        th.Property("jobStartTime", th.StringType),
        th.Property("estimatedPayrollCost", th.NumberType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/memberships/v2/tenant/{self._tap.config['tenant_id']}/export/recurring-services"


class RecurringServiceEventsStream(ServiceTitanExportStream):
    """Define recurring service events stream."""

    name = "recurring_service_events"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("locationRecurringServiceId", th.IntegerType),
        th.Property("locationRecurringServiceName", th.StringType),
        th.Property("membershipId", th.IntegerType),
        th.Property("membershipName", th.StringType),
        th.Property("status", th.StringType),
        th.Property("date", th.DateTimeType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("jobId", th.IntegerType),
        th.Property("createdById", th.IntegerType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/memberships/v2/tenant/{self._tap.config['tenant_id']}/export/recurring-service-events"


class MembershipStatusChangesStream(ServiceTitanExportStream):
    """Define membership status changes export stream."""

    name = "membership_status_changes"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("oldStatus", th.StringType),
        th.Property("newStatus", th.StringType),
        th.Property("note", th.StringType, required=False),
        th.Property("createdOn", th.DateTimeType),
        th.Property("createdById", th.IntegerType, required=False),
        th.Property("membershipId", th.IntegerType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/memberships/v2/tenant/{self._tap.config['tenant_id']}/export/membership-status-changes"
