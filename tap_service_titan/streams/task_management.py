"""Task management streams for the ServiceTitan tap."""

from __future__ import annotations

from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_service_titan.client import ServiceTitanStream


class TasksStream(ServiceTitanStream):
    """Define tasks stream."""

    name = "tasks"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("reportedById", th.IntegerType),
        th.Property("assignedToId", th.IntegerType),
        th.Property("active", th.BooleanType),
        th.Property("isClosed", th.BooleanType),
        th.Property("closedOn", th.DateTimeType),
        th.Property("name", th.StringType),
        th.Property("businessUnitId", th.IntegerType),
        th.Property("employeeTaskTypeId", th.IntegerType),
        th.Property("employeeTaskSourceId", th.IntegerType),
        th.Property("employeeTaskResolutionId", th.IntegerType),
        th.Property("reportedOn", th.DateTimeType),
        th.Property("completeBy", th.DateTimeType),
        th.Property("involvedEmployeeIdList", th.ArrayType(th.IntegerType)),
        th.Property("customerId", th.IntegerType),
        th.Property("jobId", th.IntegerType),
        th.Property("projectId", th.IntegerType),
        th.Property("description", th.StringType),
        th.Property("priority", th.StringType),
        th.Property("id", th.IntegerType),
        th.Property("taskNumber", th.IntegerType),
        th.Property("customerName", th.StringType),
        th.Property("jobNumber", th.StringType),
        th.Property("refundIssued", th.NumberType),
        th.Property("descriptionModifiedOn", th.DateTimeType),
        th.Property("descriptionModifiedById", th.IntegerType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property(
            "comments",
            th.ArrayType(
                th.ObjectType(
                    th.Property("employeeId", th.IntegerType),
                    th.Property("comment", th.StringType),
                    th.Property("createdOn", th.DateTimeType),
                )
            ),
        ),
        th.Property(
            "attachments",
            th.ArrayType(
                th.ObjectType(
                    th.Property("createdOn", th.DateTimeType),
                    th.Property("createdBy", th.IntegerType),
                    th.Property("count", th.IntegerType),
                    th.Property(
                        "files",
                        th.ArrayType(
                            th.ObjectType(
                                th.Property("url", th.StringType),
                                th.Property("filename", th.StringType),
                            )
                        ),
                    ),
                )
            ),
        ),
        th.Property(
            "subTasksData",
            th.ObjectType(
                th.Property("count", th.IntegerType),
                th.Property(
                    "subTasks",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("assignedToId", th.IntegerType),
                            th.Property("reportedById", th.IntegerType),
                            th.Property("active", th.BooleanType),
                            th.Property("isClosed", th.BooleanType),
                            th.Property("closedOn", th.DateTimeType),
                            th.Property("name", th.StringType),
                            th.Property("createdOn", th.DateTimeType),
                            th.Property("dueDateTime", th.DateTimeType),
                            th.Property("subtaskNumber", th.IntegerType),
                            th.Property("isViewed", th.BooleanType),
                            th.Property("assignedDateTime", th.DateTimeType),
                            th.Property(
                                "comments",
                                th.ArrayType(
                                    th.ObjectType(
                                        th.Property("employeeId", th.IntegerType),
                                        th.Property("comment", th.StringType),
                                        th.Property("createdOn", th.DateTimeType),
                                    )
                                ),
                            ),
                        )
                    ),
                ),
            ),
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/task-management/v2/tenant/{self.tenant_id}/tasks"
