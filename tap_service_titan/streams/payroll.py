"""Payroll streams for the ServiceTitan tap."""

from __future__ import annotations

import sys
from functools import cached_property

from tap_service_titan.client import ServiceTitanExportStream, ServiceTitanStream
from tap_service_titan.openapi_specs import PAYROLL, ServiceTitanSchema

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


class JobSplitsStream(ServiceTitanExportStream):
    """Define job splits stream."""

    name = "job_splits"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(PAYROLL, key="Payroll.V2.JobSplits.JobSplitExportResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/payroll/v2/tenant/{self.tenant_id}/export/jobs/splits"


class PayrollAdjustmentsStream(ServiceTitanExportStream):
    """Define payroll adjustments stream."""

    name = "payroll_adjustments"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(
        PAYROLL,
        key="Payroll.V2.PayrollAdjustments.PayrollAdjustmentExportResponse",
    )

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/payroll/v2/tenant/{self.tenant_id}/export/payroll-adjustments"


class JobTimesheetsStream(ServiceTitanExportStream):
    """Define job timesheets stream."""

    name = "job_timesheets"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(
        PAYROLL,
        key="Payroll.V2.Timesheets.JobTimesheetExportResponse",
    )

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/payroll/v2/tenant/{self.tenant_id}/export/jobs/timesheets"


class ActivityCodesStream(ServiceTitanExportStream):
    """Define activity codes stream."""

    name = "activity_codes"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(
        PAYROLL,
        key="Payroll.V2.PayrollActivityCodes.PayrollActivityCodeExportResponse",
    )

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/payroll/v2/tenant/{self.tenant_id}/export/activity-codes"


class TimesheetCodesStream(ServiceTitanExportStream):
    """Define timesheet codes stream."""

    name = "timesheet_codes"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(
        PAYROLL,
        key="Payroll.V2.TimesheetCodes.TimesheetCodeExportResponse",
    )

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/payroll/v2/tenant/{self.tenant_id}/export/timesheet-codes"


class GrossPayItemsStream(ServiceTitanExportStream):
    """Define gross pay items stream."""

    name = "gross_pay_items"
    primary_keys = ("payrollId", "date")
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(
        PAYROLL,
        key="Payroll.V2.GrossPayItems.GrossPayItemExportResponse",
    )

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/payroll/v2/tenant/{self.tenant_id}/export/gross-pay-items"


class LocationRatesStream(ServiceTitanStream):
    """Define location rates stream."""

    name = "location_rates"
    primary_keys = ("locationId", "laborTypeCode")
    schema = ServiceTitanSchema(
        PAYROLL,
        key="Payroll.V2.LocationLaborTypes.LocationLaborTypeResponse",
    )

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/payroll/v2/tenant/{self.tenant_id}/locations/rates"


class PayrollsStream(ServiceTitanStream):
    """Define payrolls stream."""

    name = "payrolls"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(PAYROLL, key="Payroll.V2.Payrolls.PayrollResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/payroll/v2/tenant/{self.tenant_id}/payrolls"


class NonJobTimesheetsStream(ServiceTitanStream):
    """Define non-job timesheets stream."""

    name = "non_job_timesheets"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(
        PAYROLL,
        key="Payroll.V2.Timesheets.NonJobTimesheetResponse",
    )

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/payroll/v2/tenant/{self.tenant_id}/non-job-timesheets"
