"""Stream type classes for tap-service-titan."""

from __future__ import annotations

import sys
import typing as t
from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_service_titan.client import ServiceTitanStream

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources


# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = importlib_resources.files(__package__) / "schemas"
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.


class AppointmentsStream(ServiceTitanStream):
    """Define custom stream."""

    name = "appointments"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"  # noqa: ERA001
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


class JobsStream(ServiceTitanStream):
    """Define custom stream."""

    name = "jobs"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"  # noqa: ERA001
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


class ProjectsStream(ServiceTitanStream):
    """Define custom stream."""

    name = "projects"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"  # noqa: ERA001
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
        th.Property("projectManagerIds", th.ArrayType(th.IntegerType())),
        th.Property("businessUnitIds", th.ArrayType(th.IntegerType())),
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
        th.Property("jobIds", th.ArrayType(th.IntegerType())),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/jpm/v2/tenant/{self._tap.config['tenant_id']}/export/projects"


class EstimatesStream(ServiceTitanStream):
    """Define custom stream for estimates."""

    name = "estimates"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("jobId", th.IntegerType),
        th.Property("projectId", th.IntegerType),
        th.Property("locationId", th.IntegerType),
        th.Property("customerId", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("jobNumber", th.StringType),
        th.Property(
            "status",
            th.ObjectType(
                th.Property("value", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property("reviewStatus", th.StringType),
        th.Property("summary", th.StringType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("soldOn", th.DateTimeType),
        th.Property("soldBy", th.IntegerType),
        th.Property("active", th.BooleanType),
        th.Property(
            "items",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property(
                        "sku",
                        th.ObjectType(
                            th.Property("id", th.IntegerType),
                            th.Property("name", th.StringType),
                            th.Property("displayName", th.StringType),
                            th.Property("type", th.StringType),
                            th.Property("soldHours", th.NumberType),
                            th.Property("generalLedgerAccountId", th.IntegerType),
                            th.Property("generalLedgerAccountName", th.StringType),
                            th.Property("modifiedOn", th.DateTimeType),
                        ),
                    ),
                    th.Property("skuAccount", th.StringType),
                    th.Property("description", th.StringType),
                    th.Property("membershipTypeId", th.IntegerType),
                    th.Property("qty", th.NumberType),
                    th.Property("unitRate", th.NumberType),
                    th.Property("total", th.NumberType),
                    th.Property("unitCost", th.NumberType),
                    th.Property("totalCost", th.NumberType),
                    th.Property("itemGroupName", th.StringType),
                    th.Property("itemGroupRootId", th.IntegerType),
                    th.Property("createdOn", th.DateTimeType),
                    th.Property("modifiedOn", th.DateTimeType),
                    th.Property("chargeable", th.BooleanType),
                ),
            ),
        ),
        th.Property(
            "externalLinks",
            th.ArrayType(
                th.ObjectType(
                    th.Property("name", th.StringType),
                    th.Property("url", th.StringType),
                )
            ),
        ),
        th.Property("subtotal", th.NumberType),
        th.Property("businessUnitId", th.IntegerType),
        th.Property("businessUnitName", th.StringType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/sales/v2/tenant/{self._tap.config['tenant_id']}/estimates/export"


class CallsStream(ServiceTitanStream):
    """Define custom stream."""

    name = "calls"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("duration", th.StringType),
        th.Property("from", th.StringType),
        th.Property("to", th.StringType),
        th.Property(
            "direction", th.StringType
        ),  # Assuming it's a nested object, no properties specified
        th.Property(
            "status", th.StringType
        ),  # Assuming it's a nested object, no properties specified
        th.Property(
            "type", th.StringType
        ),  # Assuming it's a nested object, no properties specified
        th.Property("recordingUrl", th.StringType),
        th.Property("voiceMailPath", th.StringType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property(
            "reason",
            th.ObjectType(
                th.Property("id", th.IntegerType), th.Property("name", th.StringType)
            ),
        ),
        th.Property(
            "customer",
            th.ObjectType(
                th.Property("id", th.IntegerType), th.Property("name", th.StringType)
            ),
        ),
        th.Property(
            "location",
            th.ObjectType(
                th.Property("id", th.IntegerType), th.Property("name", th.StringType)
            ),
        ),
        th.Property(
            "campaign",
            th.ObjectType(
                th.Property("id", th.IntegerType), th.Property("name", th.StringType)
            ),
        ),
        th.Property(
            "job",
            th.ObjectType(
                th.Property("id", th.IntegerType), th.Property("number", th.StringType)
            ),
        ),
        th.Property(
            "agent",
            th.ObjectType(
                th.Property("id", th.IntegerType), th.Property("name", th.StringType)
            ),
        ),
        th.Property(
            "createdBy",
            th.ObjectType(
                th.Property("id", th.IntegerType), th.Property("name", th.StringType)
            ),
        ),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/telecom/v2/tenant/{self._tap.config['tenant_id']}/export/calls"


class LocationsStream(ServiceTitanStream):
    """Define custom stream."""

    name = "locations"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("customerId", th.IntegerType),
        th.Property("active", th.BooleanType),
        th.Property("name", th.StringType),
        th.Property(
            "address",
            th.ObjectType(
                th.Property("street", th.StringType),
                th.Property("unit", th.StringType),
                th.Property("city", th.StringType),
                th.Property("state", th.StringType),
                th.Property("zip", th.StringType),
                th.Property("country", th.StringType),
                th.Property("latitude", th.NumberType),
                th.Property("longitude", th.NumberType),
            ),
        ),
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
        th.Property("createdOn", th.DateTimeType),
        th.Property("createdById", th.IntegerType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("mergedToId", th.IntegerType),
        th.Property("zoneId", th.IntegerType),
        th.Property("tagTypeIds", th.ArrayType(th.IntegerType)),
        th.Property(
            "externalData",
            th.ArrayType(
                th.ObjectType(
                    th.Property("key", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
        th.Property("taxZoneId", th.IntegerType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self._tap.config['tenant_id']}/locations"
