"""ServiceTitan tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_service_titan import custom_reports, streams


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
                        description="The date parameter to use for backfilling. The report will be retrieved for each date until the current date.",
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

    def discover_streams(self) -> list[streams.ServiceTitanStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        streams_list = [
            streams.AppointmentsStream(self),
            streams.JobsStream(self),
            streams.JobHistoryStream(self),
            streams.ProjectsStream(self),
            streams.JobCancelledLogsStream(self),
            streams.BookingsStream(self),
            streams.CustomersStream(self),
            streams.CustomerContactsStream(self),
            streams.LeadsStream(self),
            streams.LocationsStream(self),
            streams.LocationContactsStream(self),
            streams.InvoicesStream(self),
            streams.EstimatesStream(self),
            streams.CallsStream(self),
            streams.PaymentsStream(self),
            streams.EmployeesStream(self),
            streams.JobCancelReasonsStream(self),
            streams.JobHoldReasonsStream(self),
            streams.JobTypesStream(self),
            streams.ProjectStatusesStream(self),
            streams.ProjectSubStatusesStream(self),
            streams.TechniciansStream(self),
            streams.CampaignsStream(self),
            streams.BusinessUnitsStream(self),
            streams.InvoiceItemsStream(self),
            streams.EstimateItemsStream(self),
            streams.PurchaseOrdersStream(self),
            streams.PurchaseOrderMarkupsStream(self),
            streams.PurchaseOrderTypesStream(self),
            streams.ReceiptsStream(self),
            streams.ReturnsStream(self),
            streams.ReviewsStream(self),
            streams.CapacitiesStream(self),
        ]
        custom_reports_config = self.config.get("custom_reports", [])
        if custom_reports_config:
            streams_list.extend(
            [
                custom_reports.CustomReports(self, report=report)
                for report in custom_reports_config
            ]            )
        return streams_list


if __name__ == "__main__":
    TapServiceTitan.cli()
