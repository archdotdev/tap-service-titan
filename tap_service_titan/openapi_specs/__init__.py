"""OpenAPI specs for the ServiceTitan tap."""

from __future__ import annotations

import sys
from copy import deepcopy
from functools import cached_property
from importlib.resources import files
from typing import TYPE_CHECKING, Any

from singer_sdk import OpenAPISchema, StreamSchema

if TYPE_CHECKING:
    from collections.abc import Sequence

    from singer_sdk.streams import Stream

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

__all__ = [
    "ACCOUNTING",
    "CRM",
    "DISPATCH",
    "INVENTORY",
    "JPM",
    "SALESTECH",
    "SETTINGS",
    "TELECOM",
]


def _normalize_schema(
    schema: dict[str, Any],
    key_properties: Sequence[str] = (),
) -> dict[str, Any]:
    """Normalize OpenAPI attributes to standard JSON Schema features.

    Args:
        schema: A JSON Schema dictionary.
        key_properties: The key properties of the stream.

    - Converts 'nullable' to 'type': [<type>, "null"]
    - Converts {'field': {'oneOf': [{...} (1 item only)]}} to {'field': {...}}

    Returns:
        A new JSON Schema dictionary, normalized.
    """
    result = deepcopy(schema)
    schema_type: str | list[str] = result.get("type", [])

    if "object" in schema_type:
        for prop, prop_schema in result.get("properties", {}).items():
            prop_schema["nullable"] = prop not in key_properties
            result["properties"][prop] = _normalize_schema(prop_schema)

    elif "array" in schema_type:
        result["items"] = _normalize_schema(result["items"])

    if "oneOf" in result and len(result["oneOf"]) == 1:
        inner = result.pop("oneOf")[0]
        result.update(_normalize_schema(inner))
        schema_type = result.get("type", [])

    types = [schema_type] if isinstance(schema_type, str) else schema_type
    if result.get("nullable", False):
        result["type"] = [*types, "null"]

    if "string" in types and "enum" in result:
        result.pop("enum")

    return result


# class ServiceTitanOpenAPISchema(OpenAPISchema):
#     """ServiceTitan OpenAPI schema."""

#     @override
#     @cached_property
#     def spec(self) -> dict[str, Any]:  # noqa: C901
#         """Get the spec."""
#         spec = super().spec
#         schemas = spec["components"]["schemas"]

#         # Accounting
#         if "Accounting.V2.JournalEntryResponse" in schemas:
#             props = schemas["Accounting.V2.JournalEntryResponse"]["properties"]
#             # Values are coming in as '2025-10-13T00:00:00', so not valid ISO dates
#             props["postDate"]["format"] = "date-time"
#         if "Accounting.V2.JournalEntrySummaryResponse" in schemas:
#             props = schemas["Accounting.V2.JournalEntrySummaryResponse"]["properties"]
#             # Values are coming in as '2025-10-13T00:00:00', so not valid ISO dates
#             props["postDate"]["format"] = "date-time"
#         if "Accounting.V2.JournalEntryDetailsResponse" in schemas:
#             props = schemas["Accounting.V2.JournalEntryDetailsResponse"]["properties"]
#             # Values are coming in as '2025-10-13T00:00:00', so not valid ISO dates
#             props["postDate"]["format"] = "date-time"

#         # CRM
#         if "Crm.V2.AddressModel" in schemas:
#             props = schemas["Crm.V2.AddressModel"]["properties"]
#             props["street"]["nullable"] = True
#             props["city"]["nullable"] = True
#             props["state"]["nullable"] = True
#             props["zip"]["nullable"] = True
#             props["country"]["nullable"] = True

#         if "Crm.V2.Customers.CustomerAddress" in schemas:
#             props = schemas["Crm.V2.Customers.CustomerAddress"]["properties"]
#             props["country"]["nullable"] = True

#         if "Crm.V2.ExportCustomerResponse" in schemas:
#             props = schemas["Crm.V2.ExportCustomerResponse"]["properties"]
#             props["externalData"]["nullable"] = True

#         if "Crm.V2.ExportLocationsResponse" in schemas:
#             props = schemas["Crm.V2.ExportLocationsResponse"]["properties"]
#             props["externalData"]["nullable"] = True

#         # Dispatch
#         if "Dispatch.V2.NonJobAppointmentResponse" in schemas:
#             props = schemas["Dispatch.V2.NonJobAppointmentResponse"]["properties"]
#             props["summary"]["nullable"] = True

#         # JPM
#         if "CustomFieldApiModel" in schemas:
#             props = schemas["CustomFieldApiModel"]["properties"]
#             props["value"]["nullable"] = True

#         if "Jpm.V2.ExportJobsResponse" in schemas:
#             props = schemas["Jpm.V2.ExportJobsResponse"]["properties"]
#             props["customerPo"]["nullable"] = True
#             props["externalData"]["nullable"] = True

#         if "Jpm.V2.ExportProjectsResponse" in schemas:
#             props = schemas["Jpm.V2.ExportProjectsResponse"]["properties"]
#             props["externalData"]["nullable"] = True

#         if "Jpm.V2.JobTypeResponse" in schemas:
#             props = schemas["Jpm.V2.JobTypeResponse"]["properties"]
#             props["externalData"]["nullable"] = True

#         # Telecom
#         if "Telecom.V2.ExportCallResponse" in schemas:
#             props = schemas["Telecom.V2.ExportCallResponse"]["properties"]
#             props["excuseMemo"]["nullable"] = True
#             props["tag"]["nullable"] = True

#         return spec

#     @override
#     def fetch_schema(self, key: str) -> dict[str, Any]:
#         """Fetch the schema for the given key."""
#         schema = super().fetch_schema(key)
#         return _normalize_schema(schema)


class ServiceTitanSchema(StreamSchema):
    """ServiceTitan schema."""

    @override
    def get_stream_schema(
        self,
        stream: Stream,
        stream_class: type[Stream],
    ) -> dict[str, Any]:
        """Get the schema for the given stream."""
        schema = super().get_stream_schema(stream, stream_class)
        return _normalize_schema(schema, key_properties=stream.primary_keys)


OPENAPI_SPECS = files("tap_service_titan") / "openapi_specs"
ACCOUNTING = OpenAPISchema(OPENAPI_SPECS / "accounting-v2.json")
CRM = OpenAPISchema(OPENAPI_SPECS / "crm-v2.json")
DISPATCH = OpenAPISchema(OPENAPI_SPECS / "dispatch-v2.json")
INVENTORY = OpenAPISchema(OPENAPI_SPECS / "inventory-v2.json")
JPM = OpenAPISchema(OPENAPI_SPECS / "jpm-v2.json")
SALESTECH = OpenAPISchema(OPENAPI_SPECS / "salestech-v2.json")
SETTINGS = OpenAPISchema(OPENAPI_SPECS / "settings-v2.json")
TELECOM = OpenAPISchema(OPENAPI_SPECS / "telecom.json")
