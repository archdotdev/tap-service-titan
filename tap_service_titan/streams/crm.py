"""CRM streams for the ServiceTitan tap."""

from __future__ import annotations

import typing as t
from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_service_titan.client import ServiceTitanExportStream


# CRM Streams
class BookingsStream(ServiceTitanExportStream):
    """Define bookings stream."""

    name = "bookings"
    primary_keys: t.ClassVar[list[str]] = ["id"]
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
    primary_keys: t.ClassVar[list[str]] = ["id"]
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


class CustomerContactsStream(ServiceTitanExportStream):
    """Define contacts stream."""

    name = "customer_contacts"
    primary_keys: t.ClassVar[list[str]] = ["id"]
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
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

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
    """Define locations stream."""

    name = "locations"
    primary_keys: t.ClassVar[list[str]] = ["id"]
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


class LocationContactsStream(ServiceTitanExportStream):
    """Define location contacts stream."""

    name = "location_contacts"
    primary_keys: t.ClassVar[list[str]] = ["id"]
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
