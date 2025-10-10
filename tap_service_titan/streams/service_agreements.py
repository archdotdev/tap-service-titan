"""Service agreements streams for the ServiceTitan tap."""

from __future__ import annotations

import typing as t
from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers
from typing_extensions import override

from tap_service_titan.client import (
    ServiceTitanExportStream,
)


class ServiceAgreementsStream(ServiceTitanExportStream):
    """Define service agreements stream."""

    name = "service_agreements"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("createdById", th.IntegerType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("modifiedById", th.IntegerType),
        th.Property(
            "templateFields",
            th.ObjectType(
                th.Property("originalTemplateId", th.IntegerType),
                th.Property("revenueRecognitionMode", th.StringType),
                th.Property("generalLedgerAccountId", th.IntegerType),
                th.Property("invoiceCancellationMode", th.StringType),
                th.Property("billingServiceId", th.IntegerType),
                th.Property("negativeLiabilityServiceId", th.IntegerType),
                th.Property("positiveIncomeServiceId", th.IntegerType),
                th.Property("defaultLaborCostPerHour", th.NumberType),
                th.Property("defaultExtraTravelCostPerHour", th.NumberType),
                th.Property("defaultLaborMarkupPercentage", th.NumberType),
                th.Property("defaultMaterialMarkupPercentage", th.NumberType),
                th.Property("defaultLaborSurcharge", th.NumberType),
                th.Property("defaultMaterialSurcharge", th.NumberType),
                th.Property("defaultRateSheetId", th.IntegerType),
                th.Property("defaultCampaignId", th.IntegerType),
            ),
        ),
        th.Property("customerId", th.IntegerType),
        th.Property("businessUnitId", th.IntegerType),
        th.Property("status", th.StringType),
        th.Property("locationIds", th.ArrayType(th.IntegerType)),
        th.Property("origin", th.StringType),
        th.Property("summary", th.StringType),
        th.Property("importId", th.StringType),
        th.Property("importedDeferredAmount", th.NumberType),
        th.Property("importedRecognizedAmount", th.NumberType),
        th.Property("durationMonths", th.IntegerType),
        th.Property("autoRenew", th.BooleanType),
        th.Property("renewalAgreementId", th.IntegerType),
        th.Property("startDate", th.DateType),
        th.Property("endDate", th.DateType),
        th.Property("billingSchedule", th.StringType),
        th.Property("paymentTermId", th.IntegerType),
        th.Property("paymentMethodId", th.IntegerType),
        th.Property("estimatedTravelCost", th.NumberType),
        th.Property("estimatedLaborCost", th.NumberType),
        th.Property("estimatedMaterialCost", th.NumberType),
        th.Property("laborMarkupPercentage", th.NumberType),
        th.Property("materialMarkupPercentage", th.NumberType),
        th.Property("laborSurcharge", th.NumberType),
        th.Property("materialSurcharge", th.NumberType),
        th.Property("totalAgreementPrice", th.NumberType),
        th.Property("estimatedGrossMarginAmount", th.NumberType),
        th.Property("estimatedGrossMarginPercentage", th.NumberType),
        th.Property("rateSheetId", th.IntegerType),
        th.Property("accountManagerId", th.IntegerType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/service-agreements/v2/tenant/{self._tap.config['tenant_id']}/export/service-agreements"

    @override
    def post_process(self, row, context=None) -> dict | None:
        # Fix date fields, e.g. 2025-08-01T00:00:00 -> 2025-08-01
        if start_date := row.get("startDate"):
            row["startDate"] = start_date.split("T")[0]
        if end_date := row.get("endDate"):
            row["endDate"] = end_date.split("T")[0]
        return row
