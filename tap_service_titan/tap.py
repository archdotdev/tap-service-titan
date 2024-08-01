"""ServiceTitan tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_service_titan import streams


class TapServiceTitan(Tap):
    """ServiceTitan tap class."""

    name = "tap-service-titan"

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
    ).to_dict()

    def discover_streams(self) -> list[streams.ServiceTitanStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.AppointmentsStream(self),
            streams.JobsStream(self),
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
        ]


if __name__ == "__main__":
    TapServiceTitan.cli()
