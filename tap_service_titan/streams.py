"""Stream type classes for tap-service-titan."""

from __future__ import annotations

import sys
import typing as t
from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_service_titan.client import (
    ServiceTitanStream,
    ServiceTitanExportStream,
    ServiceTitanBaseStream,
)

from singer_sdk.pagination import SinglePagePaginator

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources


# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = importlib_resources.files(__package__) / "schemas"
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.


# JPM Streams
class AppointmentsStream(ServiceTitanExportStream):
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


class JobsStream(ServiceTitanExportStream):
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

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for a child stream."""
        return {"job_id": record["id"]}


class ProjectsStream(ServiceTitanExportStream):
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
    """Define custom stream."""

    name = "job_canceled_logs"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "createdOn"
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"  # noqa: ERA001
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


# CRM Streams
class BookingsStream(ServiceTitanExportStream):
    """Define custom stream."""

    name = "bookings"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"  # noqa: ERA001
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("source", th.StringType),
        th.Property("createdOn", th.DateTimeType),
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
            ),
        ),
        th.Property(
            "customerType", th.StringType
        ),  # Enum values are actually treated as strings
        th.Property("start", th.DateTimeType),
        th.Property("summary", th.StringType),
        th.Property("campaignId", th.IntegerType),
        th.Property("businessUnitId", th.IntegerType),
        th.Property("isFirstTimeClient", th.BooleanType),
        th.Property("uploadedImages", th.ArrayType(th.StringType)),
        th.Property("isSendConfirmationEmail", th.BooleanType),
        th.Property(
            "status", th.StringType
        ),  # Enum values are actually treated as strings
        th.Property("dismissingReasonId", th.IntegerType),
        th.Property("jobId", th.IntegerType),
        th.Property("externalId", th.StringType),
        th.Property(
            "priority", th.StringType
        ),  # Enum values are actually treated as strings
        th.Property("jobTypeId", th.IntegerType),
        th.Property("bookingProviderId", th.IntegerType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self._tap.config['tenant_id']}/export/bookings"


class CustomersStream(ServiceTitanExportStream):
    """Define custom stream."""

    name = "customers"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"  # noqa: ERA001
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("active", th.BooleanType),
        th.Property("name", th.StringType),
        th.Property("type", th.StringType),  # Enum values are treated as strings
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
        th.Property("balance", th.NumberType),
        th.Property("tagTypeIds", th.ArrayType(th.IntegerType)),
        th.Property("doNotMail", th.BooleanType),
        th.Property("doNotService", th.BooleanType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("createdById", th.IntegerType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("mergedToId", th.IntegerType),
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
        return f"/crm/v2/tenant/{self._tap.config['tenant_id']}/export/customers"


class CustomerContactsStream(ServiceTitanExportStream):
    """Define custom stream."""

    name = "customer_contacts"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"  # noqa: ERA001

    schema = th.PropertiesList(
        th.Property("modifiedOn", th.DateTimeType),
        th.Property(
            "phoneSettings",
            th.ObjectType(
                th.Property("phoneNumber", th.StringType),
                th.Property("doNotText", th.BooleanType),
            ),
        ),
        th.Property("id", th.IntegerType),
        th.Property("type", th.StringType),  # Enum values are treated as strings
        th.Property("value", th.StringType),
        th.Property("memo", th.StringType),
        th.Property("customerId", th.IntegerType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return (
            f"/crm/v2/tenant/{self._tap.config['tenant_id']}/export/customers/contacts"
        )


class LeadsStream(ServiceTitanExportStream):
    """Define custom stream."""

    name = "leads"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"  # noqa: ERA001
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("status", th.StringType),  # Enum values are treated as strings
        th.Property("customerId", th.IntegerType),
        th.Property("locationId", th.IntegerType),
        th.Property("businessUnitId", th.IntegerType),
        th.Property("jobTypeId", th.IntegerType),
        th.Property("priority", th.StringType),  # Enum values are treated as strings
        th.Property("campaignId", th.IntegerType),
        th.Property("summary", th.StringType),
        th.Property("callReasonId", th.IntegerType),
        th.Property("callId", th.IntegerType),
        th.Property("bookingId", th.IntegerType),
        th.Property("manualCallId", th.IntegerType),
        th.Property("followUpDate", th.DateTimeType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("createdById", th.IntegerType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("tagTypeIds", th.ArrayType(th.IntegerType)),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self._tap.config['tenant_id']}/export/leads"


class LocationsStream(ServiceTitanExportStream):
    """Define custom stream."""

    name = "locations"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"  # noqa: ERA001
    schema = th.PropertiesList(
        th.Property("taxZoneId", th.IntegerType),
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
        th.Property("tagTypeIds", th.ArrayType(th.IntegerType())),
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
        return f"/crm/v2/tenant/{self._tap.config['tenant_id']}/export/locations"


class LocationContactsStream(ServiceTitanExportStream):
    """Define custom stream."""

    name = "location_contacts"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"  # noqa: ERA001
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("type", th.StringType),  # Enum values are treated as strings
        th.Property("value", th.StringType),
        th.Property("memo", th.StringType),
        th.Property(
            "phoneSettings",
            th.ObjectType(
                th.Property("phoneNumber", th.StringType),
                th.Property("doNotText", th.BooleanType),
            ),
        ),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("locationId", th.IntegerType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return (
            f"/crm/v2/tenant/{self._tap.config['tenant_id']}/export/locations/contacts"
        )


# Accounting Streams
class InvoicesStream(ServiceTitanExportStream):
    """Define custom stream."""

    name = "invoices"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"  # noqa: ERA001
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("syncStatus", th.StringType),
        th.Property("summary", th.StringType),
        th.Property("referenceNumber", th.StringType),
        th.Property("invoiceDate", th.StringType),
        th.Property("dueDate", th.StringType),
        th.Property("subTotal", th.StringType),
        th.Property("salesTax", th.StringType),
        th.Property(
            "salesTaxCode",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
                th.Property("taxRate", th.NumberType),
            ),
        ),
        th.Property("total", th.StringType),
        th.Property("balance", th.StringType),
        th.Property(
            "invoiceType",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "customer",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "customerAddress",
            th.ObjectType(
                th.Property("street", th.StringType),
                th.Property("unit", th.StringType),
                th.Property("city", th.StringType),
                th.Property("state", th.StringType),
                th.Property("zip", th.StringType),
                th.Property("country", th.StringType),
            ),
        ),
        th.Property(
            "location",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "locationAddress",
            th.ObjectType(
                th.Property("street", th.StringType),
                th.Property("unit", th.StringType),
                th.Property("city", th.StringType),
                th.Property("state", th.StringType),
                th.Property("zip", th.StringType),
                th.Property("country", th.StringType),
            ),
        ),
        th.Property(
            "businessUnit",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "batch",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("number", th.StringType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property("depositedOn", th.StringType),
        th.Property("createdOn", th.StringType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("adjustmentToId", th.IntegerType),
        th.Property(
            "job",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("number", th.StringType),
                th.Property("type", th.StringType),
            ),
        ),
        th.Property("projectId", th.IntegerType),
        th.Property(
            "royalty",
            th.ObjectType(
                th.Property("status", th.StringType),
                th.Property("date", th.StringType),
                th.Property("sentOn", th.StringType),
                th.Property("memo", th.StringType),
            ),
        ),
        th.Property(
            "employeeInfo",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
                th.Property("modifiedOn", th.DateTimeType),
            ),
        ),
        th.Property("commissionEligibilityDate", th.StringType),
        th.Property("sentStatus", th.StringType),  # Assuming this is a string type
        th.Property("reviewStatus", th.StringType),  # Assuming this is a string type
        th.Property(
            "assignedTo",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "items",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property("description", th.StringType),
                    th.Property("quantity", th.StringType),
                    th.Property("cost", th.StringType),
                    th.Property("totalCost", th.StringType),
                    th.Property("inventoryLocation", th.StringType),
                    th.Property("price", th.StringType),
                    th.Property(
                        "type", th.StringType
                    ),  # Assuming this is a string type
                    th.Property("skuName", th.StringType),
                    th.Property("skuId", th.IntegerType),
                    th.Property("total", th.StringType),
                    th.Property("inventory", th.BooleanType),
                    th.Property("taxable", th.BooleanType),
                    th.Property(
                        "generalLedgerAccount",
                        th.ObjectType(
                            th.Property("id", th.IntegerType),
                            th.Property("name", th.StringType),
                            th.Property("number", th.StringType),
                            th.Property("type", th.StringType),
                            th.Property("detailType", th.StringType),
                        ),
                    ),
                    th.Property(
                        "costOfSaleAccount",
                        th.ObjectType(
                            th.Property("id", th.IntegerType),
                            th.Property("name", th.StringType),
                            th.Property("number", th.StringType),
                            th.Property("type", th.StringType),
                            th.Property("detailType", th.StringType),
                        ),
                    ),
                    th.Property(
                        "assetAccount",
                        th.ObjectType(
                            th.Property("id", th.IntegerType),
                            th.Property("name", th.StringType),
                            th.Property("number", th.StringType),
                            th.Property("type", th.StringType),
                            th.Property("detailType", th.StringType),
                        ),
                    ),
                    th.Property("membershipTypeId", th.IntegerType),
                    th.Property(
                        "itemGroup",
                        th.ObjectType(
                            th.Property("rootId", th.IntegerType),
                            th.Property("name", th.StringType),
                        ),
                    ),
                    th.Property("displayName", th.StringType),
                    th.Property("soldHours", th.NumberType),
                    th.Property("modifiedOn", th.DateTimeType),
                    th.Property("serviceDate", th.StringType),
                    th.Property("order", th.IntegerType),
                    th.Property(
                        "businessUnit",
                        th.ObjectType(
                            th.Property("id", th.IntegerType),
                            th.Property("name", th.StringType),
                        ),
                    ),
                )
            ),
        ),
        th.Property(
            "customFields",
            th.ArrayType(
                th.ObjectType(
                    th.Property("name", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self._tap.config['tenant_id']}/export/invoices"


class InvoiceItemsStream(ServiceTitanExportStream):
    """Define custom stream."""

    name = "invoice_items"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"  # noqa: ERA001
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("description", th.StringType),
        th.Property("quantity", th.StringType),
        th.Property("cost", th.StringType),
        th.Property("totalCost", th.StringType),
        th.Property("inventoryLocation", th.StringType),
        th.Property("price", th.StringType),
        th.Property("type", th.StringType),
        th.Property("skuName", th.StringType),
        th.Property("skuId", th.IntegerType),
        th.Property("total", th.StringType),
        th.Property("inventory", th.BooleanType),
        th.Property("taxable", th.BooleanType),
        th.Property(
            "generalLedgerAccount",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
                th.Property("number", th.StringType),
                th.Property("type", th.StringType),
                th.Property("detailType", th.StringType),
            ),
        ),
        th.Property(
            "costOfSaleAccount",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
                th.Property("number", th.StringType),
                th.Property("type", th.StringType),
                th.Property("detailType", th.StringType),
            ),
        ),
        th.Property(
            "assetAccount",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
                th.Property("number", th.StringType),
                th.Property("type", th.StringType),
                th.Property("detailType", th.StringType),
            ),
        ),
        th.Property("membershipTypeId", th.IntegerType),
        th.Property(
            "itemGroup",
            th.ObjectType(
                th.Property("rootId", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property("displayName", th.StringType),
        th.Property("soldHours", th.NumberType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("serviceDate", th.DateTimeType),
        th.Property("order", th.IntegerType),
        th.Property(
            "businessUnit",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property("active", th.BooleanType),
        th.Property("invoiceId", th.IntegerType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self._tap.config['tenant_id']}/export/invoice-items"


class EstimatesStream(ServiceTitanExportStream):
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


class EstimateItemsStream(ServiceTitanStream):
    """Define custom stream for estimate items."""

    name = "estimate_items"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    schema = th.PropertiesList(
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
                th.Property("modifiedOn", th.StringType),
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
        th.Property("createdOn", th.StringType),  # Assuming datetime format as string
        th.Property("modifiedOn", th.StringType),  # Assuming datetime format as string
        th.Property("chargeable", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/sales/v2/tenant/{self._tap.config['tenant_id']}/estimates/items"


class CallsStream(ServiceTitanExportStream):
    """Define custom stream."""

    name = "calls"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("duration", th.StringType),
        th.Property("from", th.StringType),
        th.Property("to", th.StringType),
        th.Property("direction", th.StringType),
        th.Property("status", th.StringType),
        th.Property("type", th.StringType),
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


class PaymentsStream(ServiceTitanExportStream):
    """Define custom stream."""

    name = "payments"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("syncStatus", th.StringType),
        th.Property("referenceNumber", th.StringType),
        th.Property("date", th.DateTimeType),
        th.Property("type", th.StringType),
        th.Property("typeId", th.StringType),
        th.Property("total", th.StringType),
        th.Property("unappliedAmount", th.StringType),
        th.Property("memo", th.StringType),
        th.Property(
            "customer",
            th.ObjectType(
                th.Property("id", th.IntegerType), th.Property("name", th.StringType)
            ),
        ),
        th.Property(
            "businessUnit",
            th.ObjectType(
                th.Property("id", th.IntegerType), th.Property("name", th.StringType)
            ),
        ),
        th.Property(
            "batch",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("number", th.StringType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property("createdBy", th.StringType),
        th.Property(
            "generalLedgerAccount",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
                th.Property("number", th.StringType),
                th.Property("type", th.StringType),
                th.Property("detailType", th.StringType),
            ),
        ),
        th.Property(
            "appliedTo",
            th.ArrayType(
                th.ObjectType(
                    th.Property("appliedId", th.IntegerType),
                    th.Property("appliedTo", th.IntegerType),
                    th.Property("appliedAmount", th.StringType),
                    th.Property("appliedOn", th.DateTimeType),
                    th.Property("appliedBy", th.StringType),
                    th.Property("appliedToReferenceNumber", th.StringType),
                )
            ),
        ),
        th.Property(
            "customFields",
            th.ArrayType(
                th.ObjectType(
                    th.Property("name", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
        th.Property("authCode", th.StringType),
        th.Property("checkNumber", th.StringType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/accounting/v2/tenant/{self._tap.config['tenant_id']}/export/payments"


class EmployeesStream(ServiceTitanExportStream):
    """Define custom stream."""

    name = "employees"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("userId", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("role", th.StringType),
        th.Property("roleIds", th.ArrayType(th.IntegerType)),
        th.Property("businessUnitId", th.IntegerType, required=False),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("email", th.StringType, required=False),
        th.Property("phoneNumber", th.StringType, required=False),
        th.Property("loginName", th.StringType, required=False),
        th.Property(
            "customFields",
            th.ArrayType(
                th.ObjectType(
                    th.Property("typeId", th.IntegerType),
                    th.Property("name", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
            required=False,
        ),
        th.Property("active", th.BooleanType),
        th.Property("aadUserId", th.StringType, required=False),
        th.Property(
            "permissions",
            th.ArrayType(
                th.OneOf(
                    th.ObjectType(
                        th.Property("id", th.IntegerType),
                        th.Property("value", th.StringType),
                    ),
                    # Array may contain Nones -- falling back to AnyType for now
                    th.AnyType,
                )
            ),
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/settings/v2/tenant/{self._tap.config['tenant_id']}/export/employees"


class BusinessUnitsStream(ServiceTitanExportStream):
    """Define custom stream."""

    name = "business_units"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("active", th.BooleanType),
        th.Property("name", th.StringType),
        th.Property("officialName", th.StringType, required=False),
        th.Property("email", th.StringType, required=False),
        th.Property("phoneNumber", th.StringType, required=False),
        th.Property("invoiceHeader", th.StringType, required=False),
        th.Property("invoiceMessage", th.StringType, required=False),
        th.Property("defaultTaxRate", th.NumberType, required=False),
        th.Property("authorizationParagraph", th.StringType, required=False),
        th.Property("acknowledgementParagraph", th.StringType, required=False),
        th.Property(
            "address",
            th.ObjectType(
                th.Property("street", th.StringType),
                th.Property("unit", th.StringType),
                th.Property("city", th.StringType),
                th.Property("state", th.StringType),
                th.Property("zip", th.StringType),
                th.Property("country", th.StringType),
            ),
            required=False,
        ),
        th.Property("materialSku", th.StringType, required=False),
        th.Property("quickbooksClass", th.StringType, required=False),
        th.Property("accountCode", th.StringType, required=False),
        th.Property("franchiseId", th.StringType, required=False),
        th.Property("conceptCode", th.StringType, required=False),
        th.Property("corporateContractNumber", th.StringType, required=False),
        th.Property(
            "tenant",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
                th.Property("accountCode", th.StringType),
                th.Property("franchiseId", th.StringType),
                th.Property("conceptCode", th.StringType),
                th.Property("modifiedOn", th.DateTimeType),
            ),
            required=False,
        ),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property(
            "externalData",
            th.ArrayType(
                th.ObjectType(
                    th.Property("key", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
            required=False,
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return (
            f"/settings/v2/tenant/{self._tap.config['tenant_id']}/export/business-units"
        )


class TechniciansStream(ServiceTitanExportStream):
    """Define custom stream."""

    name = "technicians"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("userId", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("roleIds", th.ArrayType(th.IntegerType())),
        th.Property("businessUnitId", th.IntegerType),
        th.Property("mainZoneId", th.IntegerType),
        th.Property("zoneIds", th.ArrayType(th.IntegerType())),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("email", th.StringType),
        th.Property("phoneNumber", th.StringType),
        th.Property("loginName", th.StringType),
        th.Property(
            "home",
            th.ObjectType(
                th.Property("street", th.StringType),
                th.Property("unit", th.StringType),
                th.Property("country", th.StringType),
                th.Property("city", th.StringType),
                th.Property("state", th.StringType),
                th.Property("zip", th.StringType),
                th.Property("streetAddress", th.StringType),
                th.Property("latitude", th.NumberType),
                th.Property("longitude", th.NumberType),
            ),
        ),
        th.Property("dailyGoal", th.NumberType),
        th.Property("isManagedTech", th.BooleanType),
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
        th.Property("active", th.BooleanType),
        th.Property("aadUserId", th.StringType),
        th.Property("burdenRate", th.NumberType),
        th.Property("team", th.StringType),
        th.Property("jobFilter", th.StringType),
        th.Property(
            "permissions",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/settings/v2/tenant/{self._tap.config['tenant_id']}/export/technicians"


class JobCancelReasonsStream(ServiceTitanStream):
    """Define custom stream."""

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
    """Define custom stream."""

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
    """Define custom stream."""

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
    """Define custom stream."""

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
    """Define custom stream."""

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


class CampaignsStream(ServiceTitanStream):
    """Define custom stream."""

    name = "campaigns"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("active", th.BooleanType),
        th.Property(
            "category",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
                th.Property("active", th.BooleanType),
            ),
        ),
        th.Property("source", th.StringType),
        th.Property("otherSource", th.StringType),
        th.Property("businessUnit", th.StringType),
        th.Property("medium", th.StringType),
        th.Property("otherMedium", th.StringType),
        th.Property("campaignPhoneNumbers", th.ArrayType(th.StringType)),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/marketing/v2/tenant/{self._tap.config['tenant_id']}/campaigns"
