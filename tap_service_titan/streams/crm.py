"""CRM streams for the ServiceTitan tap."""

from __future__ import annotations

import sys
from functools import cached_property
from typing import TYPE_CHECKING

from singer_sdk import StreamSchema
from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_service_titan.client import ServiceTitanExportStream, ServiceTitanStream
from tap_service_titan.openapi_specs import CRM

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if TYPE_CHECKING:
    from singer_sdk.helpers.types import Context



# CRM Streams
class BookingProviderTagsStream(ServiceTitanStream):
    """Define booking provider tags stream."""

    name = "booking_provider_tags"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("tagName", th.StringType),
        th.Property("description", th.StringType),
        th.Property("type", th.StringType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self._tap.config['tenant_id']}/booking-provider-tags"


class BookingsStream(ServiceTitanExportStream):
    """Define bookings stream."""

    name = "bookings"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"

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
    """Define customers stream."""

    name = "customers"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"

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

    def get_child_context(self, record: dict, context: dict | None) -> dict:
        """Return a context dictionary for a child stream."""
        return {"customer_id": record["id"]}


class CustomerNotesStream(ServiceTitanStream):
    """Define customer notes stream."""

    name = "customer_notes"
    primary_keys = ("createdById", "createdOn")
    replication_key: str = "modifiedOn"
    parent_stream_type = CustomersStream
    ignore_parent_replication_key = True

    schema = th.PropertiesList(
        th.Property("text", th.StringType),
        th.Property("isPinned", th.BooleanType),
        th.Property("createdById", th.IntegerType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self._tap.config['tenant_id']}/customers/{'{customer_id}'}/notes"  # noqa: E501


class CustomerContactsStream(ServiceTitanExportStream):
    """Define contacts stream."""

    name = "customer_contacts"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"

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
    """Define leads stream."""

    name = "leads"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = StreamSchema(CRM, key="Crm.V2.ExportLeadsResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self.tenant_id}/export/leads"

    @override
    def get_child_context(self, record: dict, context: Context | None) -> dict:
        """Return a context dictionary for a child stream."""
        return {"lead_id": record["id"]}


class LeadNotesStream(ServiceTitanStream):
    """Define lead notes stream."""

    name = "lead_notes"
    primary_keys = ("createdById", "createdOn")
    replication_key: str = "modifiedOn"
    parent_stream_type = LeadsStream
    ignore_parent_replication_key = True

    schema = th.PropertiesList(
        th.Property("text", th.StringType),
        th.Property("isPinned", th.BooleanType),
        th.Property("createdById", th.IntegerType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return (
            f"/crm/v2/tenant/{self._tap.config['tenant_id']}/leads/{'{lead_id}'}/notes"
        )


class LocationsStream(ServiceTitanExportStream):
    """Define locations stream."""

    name = "locations"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"

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

    def get_child_context(self, record: dict, context: dict | None) -> dict:
        """Return a context dictionary for a child stream."""
        return {"location_id": record["id"]}


class LocationNotesStream(ServiceTitanStream):
    """Define location notes stream."""

    name = "location_notes"
    primary_keys = ("createdById", "createdOn")
    replication_key: str = "modifiedOn"
    parent_stream_type = LocationsStream
    ignore_parent_replication_key = True

    schema = th.PropertiesList(
        th.Property("text", th.StringType),
        th.Property("isPinned", th.BooleanType),
        th.Property("createdById", th.IntegerType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self._tap.config['tenant_id']}/locations/{'{location_id}'}/notes"  # noqa: E501


class LocationContactsStream(ServiceTitanExportStream):
    """Define location contacts stream."""

    name = "location_contacts"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"

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


class LocationsCustomFieldsStream(ServiceTitanStream):
    """Define locations custom fields stream."""

    name = "locations_custom_fields"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("displayName", th.StringType),
        th.Property("dataType", th.StringType),
        th.Property(
            "dataTypeOptions",
            th.ArrayType(th.StringType),
            description="The type custom field type (e.g. Text, Dropdown, or Numeric)",
            nullable=True,
        ),
        th.Property("required", th.BooleanType),
        th.Property("enabled", th.BooleanType),
        th.Property("allowOnBulkUpdate", th.BooleanType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self._tap.config['tenant_id']}/locations/custom-fields"


class CustomersCustomFieldsStream(ServiceTitanStream):
    """Define customers custom fields stream."""

    name = "customers_custom_fields"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("displayName", th.StringType),
        th.Property("dataType", th.StringType),
        th.Property(
            "dataTypeOptions",
            th.ArrayType(th.StringType),
            description="The type custom field type (e.g. Text, Dropdown, or Numeric)",
            nullable=True,
        ),
        th.Property("required", th.BooleanType),
        th.Property("enabled", th.BooleanType),
        th.Property("allowOnBulkUpdate", th.BooleanType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("active", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self._tap.config['tenant_id']}/customers/custom-fields"
