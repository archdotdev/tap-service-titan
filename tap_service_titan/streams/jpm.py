"""JPM streams for the ServiceTitan tap."""

from __future__ import annotations

import typing as t
from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_service_titan.client import (
    ServiceTitanExportStream,
    ServiceTitanStream,
)

if t.TYPE_CHECKING:
    import requests


# JPM Streams
class AppointmentsStream(ServiceTitanExportStream):
    """Define appointments stream."""

    name = "appointments"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("active", th.BooleanType),
        th.Property("id", th.IntegerType),
        th.Property("jobId", th.IntegerType),
        th.Property("appointmentNumber", th.StringType),
        th.Property("start", th.DateTimeType),
        th.Property("end", th.DateTimeType),
        th.Property("arrivalWindowStart", th.DateTimeType),
        th.Property("arrivalWindowEnd", th.DateTimeType),
        th.Property("status", th.StringType),
        th.Property("specialInstructions", th.StringType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("customerId", th.IntegerType),
        th.Property("unused", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/jpm/v2/tenant/{self._tap.config['tenant_id']}/export/appointments"


class JobsStream(ServiceTitanExportStream):
    """Define jobs stream."""

    name = "jobs"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("active", th.BooleanType),
        th.Property("id", th.IntegerType),
        th.Property("jobNumber", th.StringType),
        th.Property("projectId", th.IntegerType),
        th.Property("customerId", th.IntegerType),
        th.Property("locationId", th.IntegerType),
        th.Property("jobStatus", th.StringType),
        th.Property("completedOn", th.DateTimeType),
        th.Property("businessUnitId", th.IntegerType),
        th.Property("jobTypeId", th.IntegerType),
        th.Property("priority", th.StringType),
        th.Property("campaignId", th.IntegerType),
        th.Property("summary", th.StringType),
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
        th.Property("appointmentCount", th.IntegerType),
        th.Property("firstAppointmentId", th.IntegerType),
        th.Property("lastAppointmentId", th.IntegerType),
        th.Property("recallForId", th.IntegerType),
        th.Property("warrantyId", th.IntegerType),
        th.Property(
            "jobGeneratedLeadSource",
            th.ObjectType(
                th.Property("jobId", th.IntegerType),
                th.Property("employeeId", th.IntegerType),
            ),
        ),
        th.Property("noCharge", th.BooleanType),
        th.Property("notificationsEnabled", th.BooleanType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("createdById", th.IntegerType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("tagTypeIds", th.ArrayType(th.IntegerType)),
        th.Property("leadCallId", th.IntegerType),
        th.Property("bookingId", th.IntegerType),
        th.Property("soldById", th.IntegerType),
        th.Property("externalData", th.StringType),
        th.Property("customerPo", th.StringType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/jpm/v2/tenant/{self._tap.config['tenant_id']}/export/jobs"

    def get_child_context(self, record: dict, context: dict | None) -> dict:  # noqa: ARG002
        """Return a context dictionary for a child stream."""
        return {"job_id": record["id"]}


class JobHistoryStream(ServiceTitanExportStream):
    """Define job history stream."""

    name = "job_history"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: th.DateTimeType = "date"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("jobId", th.IntegerType),
        th.Property("employeeId", th.IntegerType, required=False),
        th.Property("eventType", th.StringType),
        th.Property("date", th.DateTimeType),
        th.Property(
            "usedSchedulingTool",
            th.StringType,
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/jpm/v2/tenant/{self._tap.config['tenant_id']}/export/job-history"

    # Parse the default 'data' path for response records but the real contents are in
    # the nested history array. Keep the jobID from the top level then yield
    # each history item as its own record.
    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        for record in super().parse_response(response):
            for hist_record in record.get("history", []):
                yield {"jobId": record.get("jobId"), **hist_record}


class ProjectsStream(ServiceTitanExportStream):
    """Define projects stream."""

    name = "projects"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("active", th.BooleanType),
        th.Property("id", th.IntegerType),
        th.Property("number", th.StringType),
        th.Property("name", th.StringType),
        th.Property("summary", th.StringType),
        th.Property("status", th.StringType),
        th.Property("statusId", th.IntegerType),
        th.Property("subStatus", th.StringType),
        th.Property("subStatusId", th.IntegerType),
        th.Property("customerId", th.IntegerType),
        th.Property("locationId", th.IntegerType),
        th.Property("projectManagerIds", th.ArrayType(th.IntegerType)),
        th.Property("businessUnitIds", th.ArrayType(th.IntegerType)),
        th.Property("startDate", th.DateTimeType),
        th.Property("targetCompletionDate", th.DateTimeType),
        th.Property("actualCompletionDate", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("createdOn", th.DateTimeType),
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
        th.Property("externalData", th.StringType),
        th.Property("jobIds", th.ArrayType(th.IntegerType)),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/jpm/v2/tenant/{self._tap.config['tenant_id']}/export/projects"


class JobCancelledLogsStream(ServiceTitanExportStream):
    """Define cancelled job stream."""

    name = "job_canceled_logs"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "createdOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("jobId", th.IntegerType),
        th.Property("reasonId", th.IntegerType),
        th.Property("memo", th.StringType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("createdById", th.IntegerType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return (
            f"/jpm/v2/tenant/{self._tap.config['tenant_id']}/export/job-canceled-logs"
        )


class JobCancelReasonsStream(ServiceTitanStream):
    """Define job cancel reasons stream."""

    name = "job_cancel_reasons"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("active", th.BooleanType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/jpm/v2/tenant/{self._tap.config['tenant_id']}/job-cancel-reasons"


class JobHoldReasonsStream(ServiceTitanStream):
    """Define job hold reasons stream."""

    name = "job_hold_reasons"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("active", th.BooleanType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/jpm/v2/tenant/{self._tap.config['tenant_id']}/job-hold-reasons"


class JobTypesStream(ServiceTitanStream):
    """Define job types stream."""

    name = "job_types"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("businessUnitIds", th.ArrayType(th.IntegerType)),
        th.Property("skills", th.ArrayType(th.StringType)),
        th.Property("tagTypeIds", th.ArrayType(th.IntegerType)),
        th.Property("priority", th.StringType),
        th.Property("duration", th.IntegerType),
        th.Property("soldThreshold", th.NumberType),
        th.Property("class", th.StringType),
        th.Property("summary", th.StringType),
        th.Property("noCharge", th.BooleanType),
        th.Property("enforceRecurringServiceEventSelection", th.BooleanType),
        th.Property("invoiceSignaturesRequired", th.BooleanType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property(
            "externalData",
            th.ArrayType(
                th.ObjectType(
                    th.Property("key", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/jpm/v2/tenant/{self._tap.config['tenant_id']}/job-types"


class ProjectStatusesStream(ServiceTitanStream):
    """Define project statuses stream."""

    name = "project_statuses"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("order", th.IntegerType),
        th.Property("modifiedOn", th.DateTimeType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/jpm/v2/tenant/{self._tap.config['tenant_id']}/project-statuses"


class ProjectSubStatusesStream(ServiceTitanStream):
    """Define project substatuses stream."""

    name = "project_sub_statuses"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("statusId", th.IntegerType),
        th.Property("order", th.IntegerType),
        th.Property("modifiedOn", th.DateTimeType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/jpm/v2/tenant/{self._tap.config['tenant_id']}/project-substatuses"


class JobNotesStream(ServiceTitanExportStream):
    """Define job notes stream."""

    name = "job_notes"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("active", th.BooleanType),
        th.Property("text", th.StringType),
        th.Property("isPinned", th.BooleanType),
        th.Property("createdById", th.IntegerType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("jobId", th.IntegerType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/jpm/v2/tenant/{self._tap.config['tenant_id']}/export/job-notes"


class ProjectNotesStream(ServiceTitanExportStream):
    """Define project notes stream."""

    name = "project_notes"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("active", th.BooleanType),
        th.Property("text", th.StringType),
        th.Property("isPinned", th.BooleanType),
        th.Property("createdById", th.IntegerType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("projectId", th.IntegerType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/jpm/v2/tenant/{self._tap.config['tenant_id']}/export/project-notes"


class ProjectTypesStream(ServiceTitanStream):
    """Define project types stream."""

    name = "project_types"
    primary_keys: t.ClassVar[list[str]] = ["id"]

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("description", th.StringType),
        th.Property("createdById", th.IntegerType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/jpm/v2/tenant/{self._tap.config['tenant_id']}/project-types"
