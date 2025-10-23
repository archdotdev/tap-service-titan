"""Payroll streams for the ServiceTitan tap."""

from __future__ import annotations

import typing as t
from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_service_titan.client import ServiceTitanExportStream, ServiceTitanStream


class JobSplitsStream(ServiceTitanExportStream):
    """Define job splits stream."""

    name = "job_splits"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("jobId", th.IntegerType),
        th.Property("technicianId", th.IntegerType),
        th.Property("split", th.NumberType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/payroll/v2/tenant/{self._tap.config['tenant_id']}/export/jobs/splits"


class PayrollAdjustmentsStream(ServiceTitanExportStream):
    """Define payroll adjustments stream."""

    name = "payroll_adjustments"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("employeeType", th.StringType),
        th.Property("employeeId", th.IntegerType),
        th.Property("postedOn", th.DateTimeType),
        th.Property("amount", th.NumberType),
        th.Property("memo", th.StringType),
        th.Property("activityCodeId", th.IntegerType),
        th.Property("invoiceId", th.IntegerType),
        th.Property("hours", th.NumberType),
        th.Property("rate", th.NumberType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/payroll/v2/tenant/{self._tap.config['tenant_id']}/export/payroll-adjustments"


class JobTimesheetsStream(ServiceTitanExportStream):
    """Define job timesheets stream."""

    name = "job_timesheets"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("jobId", th.IntegerType),
        th.Property("appointmentId", th.IntegerType),
        th.Property("technicianId", th.IntegerType),
        th.Property("dispatchedOn", th.DateTimeType),
        th.Property("arrivedOn", th.DateTimeType),
        th.Property("canceledOn", th.DateTimeType),
        th.Property("doneOn", th.DateTimeType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return (
            f"/payroll/v2/tenant/{self._tap.config['tenant_id']}/export/jobs/timesheets"
        )


class ActivityCodesStream(ServiceTitanExportStream):
    """Define activity codes stream."""

    name = "activity_codes"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("code", th.StringType),
        th.Property("earningCategory", th.StringType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return (
            f"/payroll/v2/tenant/{self._tap.config['tenant_id']}/export/activity-codes"
        )


class TimesheetCodesStream(ServiceTitanExportStream):
    """Define timesheet codes stream."""

    name = "timesheet_codes"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("code", th.StringType),
        th.Property("description", th.StringType),
        th.Property("type", th.StringType),
        th.Property("applicableEmployeeType", th.StringType),
        th.Property(
            "rateInfo",
            th.ObjectType(
                th.Property("hourlyRate", th.StringType),
                th.Property("customHourlyRate", th.NumberType),
                th.Property("rateMultiplier", th.NumberType),
            ),
        ),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return (
            f"/payroll/v2/tenant/{self._tap.config['tenant_id']}/export/timesheet-codes"
        )


class GrossPayItemsStream(ServiceTitanExportStream):
    """Define gross pay items stream."""

    name = "gross_pay_items"
    primary_keys: t.ClassVar[list[str]] = ["payrollId", "date"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("employeeId", th.IntegerType),
        th.Property("employeeType", th.StringType),
        th.Property("businessUnitName", th.StringType),
        th.Property("payrollId", th.IntegerType),
        th.Property("employeePayrollId", th.StringType),
        th.Property("date", th.DateTimeType),
        th.Property("activity", th.StringType),
        th.Property("activityCodeId", th.IntegerType),
        th.Property("activityCode", th.StringType),
        th.Property("amount", th.NumberType),
        th.Property("amountAdjustment", th.NumberType),
        th.Property("payoutBusinessUnitName", th.StringType),
        th.Property("grossPayItemType", th.StringType),
        th.Property("startedOn", th.DateTimeType),
        th.Property("endedOn", th.DateTimeType),
        th.Property("paidDurationHours", th.NumberType),
        th.Property("paidTimeType", th.StringType),
        th.Property("jobId", th.IntegerType),
        th.Property("jobNumber", th.StringType),
        th.Property("jobTypeName", th.StringType),
        th.Property("projectNumber", th.StringType),
        th.Property("projectId", th.IntegerType),
        th.Property("invoiceId", th.IntegerType),
        th.Property("invoiceNumber", th.StringType),
        th.Property("invoiceItemId", th.IntegerType),
        th.Property("customerId", th.IntegerType),
        th.Property("customerName", th.StringType),
        th.Property("locationId", th.IntegerType),
        th.Property("locationName", th.StringType),
        th.Property("locationAddress", th.StringType),
        th.Property("locationZip", th.StringType),
        th.Property("zoneName", th.StringType),
        th.Property("taxZoneName", th.StringType),
        th.Property("laborTypeId", th.IntegerType),
        th.Property("laborTypeCode", th.StringType),
        th.Property("isPrevailingWageJob", th.BooleanType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return (
            f"/payroll/v2/tenant/{self._tap.config['tenant_id']}/export/gross-pay-items"
        )


class LocationRatesStream(ServiceTitanStream):
    """Define location rates stream."""

    name = "location_rates"
    primary_keys: t.ClassVar[list[str]] = ["locationId", "laborTypeCode"]

    schema = th.PropertiesList(
        th.Property("locationId", th.IntegerType),
        th.Property("hourlyRate", th.NumberType),
        th.Property("laborTypeName", th.StringType),
        th.Property("laborTypeCode", th.StringType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/payroll/v2/tenant/{self._tap.config['tenant_id']}/locations/rates"


class PayrollsStream(ServiceTitanStream):
    """Define payrolls stream."""

    name = "payrolls"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("startedOn", th.DateTimeType),
        th.Property("endedOn", th.DateTimeType),
        th.Property("employeeId", th.IntegerType),
        th.Property("employeeType", th.StringType),
        th.Property("status", th.StringType),
        th.Property("burdenRate", th.NumberType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("managerApprovedOn", th.DateTimeType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/payroll/v2/tenant/{self._tap.config['tenant_id']}/payrolls"


class NonJobTimesheetsStream(ServiceTitanStream):
    """Define non-job timesheets stream."""

    name = "non_job_timesheets"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("employeeId", th.IntegerType),
        th.Property("employeeType", th.StringType),
        th.Property("timesheetCodeId", th.IntegerType),
        th.Property("startedOn", th.DateTimeType),
        th.Property("endedOn", th.DateTimeType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/payroll/v2/tenant/{self._tap.config['tenant_id']}/non-job-timesheets"
