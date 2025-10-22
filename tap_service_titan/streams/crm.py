"""CRM streams for the ServiceTitan tap."""

from __future__ import annotations

import sys
from functools import cached_property
from typing import TYPE_CHECKING

from tap_service_titan.client import ServiceTitanExportStream, ServiceTitanStream
from tap_service_titan.openapi_specs import CRM, ServiceTitanSchema

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
    schema = ServiceTitanSchema(CRM, key="Crm.V2.BookingProviderTagResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self.tenant_id}/booking-provider-tags"


class BookingsStream(ServiceTitanExportStream):
    """Define bookings stream."""

    name = "bookings"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(CRM, key="Crm.V2.ExportBookingResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self.tenant_id}/export/bookings"


class CustomersStream(ServiceTitanExportStream):
    """Define customers stream."""

    name = "customers"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(CRM, key="Crm.V2.ExportCustomerResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self.tenant_id}/export/customers"

    @override
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
    schema = ServiceTitanSchema(CRM, key="Crm.V2.NoteResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self.tenant_id}/customers/{'{customer_id}'}/notes"


class CustomerContactsStream(ServiceTitanExportStream):
    """Define contacts stream."""

    name = "customer_contacts"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(CRM, key="Crm.V2.ExportCustomerContactResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self.tenant_id}/export/customers/contacts"


class LeadsStream(ServiceTitanExportStream):
    """Define leads stream."""

    name = "leads"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(CRM, key="Crm.V2.ExportLeadsResponse")

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
    schema = ServiceTitanSchema(CRM, key="Crm.V2.NoteResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self.tenant_id}/leads/{'{lead_id}'}/notes"


class LocationsStream(ServiceTitanExportStream):
    """Define locations stream."""

    name = "locations"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(CRM, key="Crm.V2.ExportLocationsResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self.tenant_id}/export/locations"

    @override
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
    schema = ServiceTitanSchema(CRM, key="Crm.V2.NoteResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self.tenant_id}/locations/{'{location_id}'}/notes"


class LocationContactsStream(ServiceTitanExportStream):
    """Define location contacts stream."""

    name = "location_contacts"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(CRM, key="Crm.V2.ExportLocationContactResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self.tenant_id}/export/locations/contacts"


class LocationsCustomFieldsStream(ServiceTitanStream):
    """Define locations custom fields stream."""

    name = "locations_custom_fields"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(CRM, key="Crm.V2.Locations.CustomFieldTypeResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self.tenant_id}/locations/custom-fields"


class CustomersCustomFieldsStream(ServiceTitanStream):
    """Define customers custom fields stream."""

    name = "customers_custom_fields"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(CRM, key="Crm.V2.Customers.CustomFieldTypeResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/crm/v2/tenant/{self.tenant_id}/customers/custom-fields"
