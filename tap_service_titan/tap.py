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
            "internal_api_url",
            th.StringType,
            description="The url for the ServiceTitan API",
        ),
        th.Property(
            "internal_login_url",
            th.StringType,
            description="The url for the ServiceTitan login API",
        ),
        th.Property(
            "internal_username",
            th.StringType,
            description="The username for the Internal ServiceTitan login API",
        ),
        th.Property(
            "internal_password",
            th.StringType,
            description="The password for the Internal ServiceTitan login API",
        ),
        th.Property(
            "internal_cookie_set_url",
            th.StringType,
            description="The url for the ServiceTitan cookie set API, example https://enterprise-hub-eh-proxy-go.servicetitan.com/api/v1/account/set-cookie-for/3984754118/?tenant=handyman_vertex-99510&redirectUrl=https://handyman_vertex-99510.eh.go.servicetitan.com",
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
                        "lookback_window_days",
                        th.NumberType,
                        description=(
                            "The amount of days to lookback when running incrementally."
                            "This is used to handled retroactively updated data in "
                            "previously synced reports.",
                        ),
                        default=0,
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
            streams.accounting.JournalEntrySummaryStream(self),
            streams.accounting.JournalEntryDetailsStream(self),
            streams.accounting.GLAccountsStream(self),
            streams.accounting.InventoryBillsCustomFieldsStream(self),
            streams.crm.BookingProviderTagsStream(self),
            streams.crm.BookingsStream(self),
            streams.crm.CustomerContactsStream(self),
            streams.crm.CustomersStream(self),
            streams.crm.CustomerNotesStream(self),
            streams.crm.LeadsStream(self),
            streams.crm.LocationContactsStream(self),
            streams.crm.LocationsStream(self),
            streams.crm.LeadNotesStream(self),
            streams.crm.LocationNotesStream(self),
            streams.crm.LocationsCustomFieldsStream(self),
            streams.crm.CustomersCustomFieldsStream(self),
            streams.dispatch.CapacitiesStream(self),
            streams.dispatch.AppointmentAssignmentsStream(self),
            streams.dispatch.ArrivalWindowsStream(self),
            streams.dispatch.BusinessHoursStream(self),
            streams.dispatch.NonJobAppointmentsStream(self),
            streams.dispatch.TeamsStream(self),
            streams.dispatch.TechnicianShiftsStream(self),
            streams.dispatch.ZonesStream(self),
            streams.equipment_systems.InstalledEquipmentStream(self),
            streams.forms.JobAttachmentsStream(self),
            streams.forms.FormsStream(self),
            streams.forms.SubmissionsStream(self),
            streams.inventory.AdjustmentsStream(self),
            streams.inventory.ReturnTypesStream(self),
            streams.inventory.TransfersStream(self),
            streams.inventory.TrucksStream(self),
            streams.inventory.VendorsStream(self),
            streams.inventory.WarehousesStream(self),
            streams.inventory.PurchaseOrderMarkupsStream(self),
            streams.inventory.PurchaseOrdersStream(self),
            streams.inventory.PurchaseOrderTypesStream(self),
            streams.inventory.ReceiptsStream(self),
            streams.inventory.ReturnsStream(self),
            streams.job_booking.CallReasonsStream(self),
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
            streams.jpm.JobNotesStream(self),
            streams.jpm.ProjectNotesStream(self),
            streams.jpm.ProjectTypesStream(self),
            streams.jpm.JobBookedLogStream(self),
            streams.jpm.JobCanceledLogStream(self),
            streams.marketing_ads.AttributedLeadsStream(self),
            streams.marketing_ads.CapacityWarningsStream(self),
            streams.marketing_ads.AdGroupPerformanceStream(self),
            streams.marketing_ads.CampaignPerformanceStream(self),
            streams.marketing_ads.KeywordPerformanceStream(self),
            streams.marketing.CampaignsStream(self),
            streams.marketing.CategoriesStream(self),
            streams.marketing.CostsStream(self),
            streams.marketing.SuppressionsStream(self),
            streams.marketing_reputation.ReviewsStream(self),
            streams.memberships.MembershipsStream(self),
            streams.memberships.MembershipTypesStream(self),
            streams.memberships.MembershipStatusChangesStream(self),
            streams.memberships.RecurringServiceTypesStream(self),
            streams.memberships.InvoiceTemplatesStream(self),
            streams.memberships.RecurringServicesStream(self),
            streams.memberships.RecurringServiceEventsStream(self),
            streams.payroll.JobSplitsStream(self),
            streams.payroll.PayrollAdjustmentsStream(self),
            streams.payroll.JobTimesheetsStream(self),
            streams.payroll.ActivityCodesStream(self),
            streams.payroll.TimesheetCodesStream(self),
            streams.payroll.GrossPayItemsStream(self),
            streams.payroll.LocationRatesStream(self),
            streams.payroll.PayrollsStream(self),
            streams.payroll.NonJobTimesheetsStream(self),
            streams.pricebook.ClientSpecificPricingStream(self),
            streams.pricebook.PricebookCategoriesStream(self),
            streams.pricebook.DiscountsAndFeesStream(self),
            streams.pricebook.EquipmentStream(self),
            streams.pricebook.MaterialsStream(self),
            streams.pricebook.MaterialsMarkupStream(self),
            streams.pricebook.ServicesStream(self),
            streams.pricebook.ExportEquipmentStream(self),
            streams.pricebook.ExportMaterialsStream(self),
            streams.pricebook.ExportServicesStream(self),
            streams.sales_and_estimates.EstimatesStream(self),
            streams.sales_and_estimates.EstimateItemsStream(self),
            streams.service_agreements.ServiceAgreementsStream(self),
            streams.scheduling_pro.SchedulersStream(self),
            streams.scheduling_pro.SchedulerSessionsStream(self),
            streams.scheduling_pro.SchedulerPerformanceStream(self),
            streams.settings.BusinessUnitsStream(self),
            streams.settings.EmployeesStream(self),
            streams.settings.TechniciansStream(self),
            streams.settings.TagTypesStream(self),
            streams.settings.UserRolesStream(self),
            streams.task_management.TasksStream(self),
            streams.telecom.CallsStream(self),
            streams.telecom.OptOutsStream(self),
            streams.crm.CustomerAttachmentsStream(self),
            streams.crm.CustomerImageAttachmentsStream(self),
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
