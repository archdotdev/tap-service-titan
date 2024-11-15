"""ServiceTitan tap class."""

from __future__ import annotations

import typing as t

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_service_titan import streams

if t.TYPE_CHECKING:
    from tap_service_titan.client import ServiceTitanStream


class TapServiceTitan(Tap):
    """ServiceTitan tap class."""

    name = "tap-service-titan"

    dynamic_catalog: bool = True

    config_jsonschema = th.PropertiesList(
        th.Property(
            "client_id",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The client ID to use in authenticating.",
        ),
        th.Property(
            "client_secret",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The client secret to use in authenticating.",
        ),
        th.Property(
            "st_app_key",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The app key for the Service Titan app used to authenticate.",
        ),
        th.Property(
            "tenant_id",
            th.StringType,
            required=True,
            description="Tenant ID to pull records for.",
        ),
        th.Property(
            "api_url",
            th.StringType,
            default="https://api-integration.servicetitan.io",
            description="The url for the ServiceTitan API",
        ),
        th.Property(
            "auth_url",
            th.StringType,
            default="https://auth-integration.servicetitan.io/connect/token",
            description="The url for the ServiceTitan OAuth API",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            default="2024-01-01T00:00:00Z",
            description="The start date for the records to pull.",
        ),
        th.Property(
            "custom_reports",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "report_category",
                        th.StringType,
                        required=True,
                        description="The category of the report to pull.",
                    ),
                    th.Property(
                        "report_name",
                        th.StringType,
                        required=True,
                        description="The name of the report to pull.",
                    ),
                    th.Property(
                        "report_id",
                        th.StringType,
                        required=True,
                        description="The ID of the report to pull.",
                    ),
                    th.Property(
                        "backfill_date_parameter",
                        th.StringType,
                        description="The date parameter to use for backfilling. The report will be retrieved for each date until the current date.",  # noqa: E501
                    ),
                    th.Property(
                        "parameters",
                        th.ArrayType(
                            th.ObjectType(
                                th.Property(
                                    "name",
                                    th.StringType,
                                    required=True,
                                    description="The name of the parameter.",
                                ),
                                th.Property(
                                    "value",
                                    th.StringType,
                                    required=True,
                                    description="The value of the parameter.",
                                ),
                            ),
                        ),
                        required=True,
                        description="The parameters to pass to the report.",
                    ),
                )
            ),
            description="Custom reports to extract.",
        ),
    ).to_dict()

    def discover_streams(self) -> list[ServiceTitanStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        streams_list = [
            streams.accounting.EstimateItemsStream(self),
            streams.accounting.InvoiceItemsStream(self),
            streams.accounting.InvoicesStream(self),
            streams.accounting.PaymentsStream(self),
            streams.accounting.InventoryBillsStream(self),
            streams.accounting.ApCreditsStream(self),
            streams.accounting.ApPaymentsStream(self),
            streams.accounting.PaymentTermsStream(self),
            streams.accounting.PaymentTypesStream(self),
            streams.accounting.TaxZonesStream(self),
            streams.accounting.JournalEntriesStream(self),
            streams.crm.BookingsStream(self),
            streams.crm.CustomerContactsStream(self),
            streams.crm.CustomersStream(self),
            streams.crm.LeadsStream(self),
            streams.crm.LocationContactsStream(self),
            streams.crm.LocationsStream(self),
            streams.dispatch.CapacitiesStream(self),
            streams.inventory.PurchaseOrderMarkupsStream(self),
            streams.inventory.PurchaseOrdersStream(self),
            streams.inventory.PurchaseOrderTypesStream(self),
            streams.inventory.ReceiptsStream(self),
            streams.inventory.ReturnsStream(self),
            streams.jpm.AppointmentsStream(self),
            streams.jpm.JobCancelReasonsStream(self),
            streams.jpm.JobCancelledLogsStream(self),
            streams.jpm.JobHistoryStream(self),
            streams.jpm.JobHoldReasonsStream(self),
            streams.jpm.JobsStream(self),
            streams.jpm.JobTypesStream(self),
            streams.jpm.ProjectStatusesStream(self),
            streams.jpm.ProjectSubStatusesStream(self),
            streams.jpm.ProjectsStream(self),
            streams.marketing.CampaignsStream(self),
            streams.marketing_reputation.ReviewsStream(self),
            streams.sales_and_estimates.EstimatesStream(self),
            streams.settings.BusinessUnitsStream(self),
            streams.settings.EmployeesStream(self),
            streams.settings.TechniciansStream(self),
            streams.telecom.CallsStream(self),
        ]
        custom_reports_config = self.config.get("custom_reports", [])
        if custom_reports_config:
            streams_list.extend(
                [
                    streams.reporting.CustomReports(self, report=report)
                    for report in custom_reports_config
                ]
            )
        return streams_list


if __name__ == "__main__":
    TapServiceTitan.cli()
