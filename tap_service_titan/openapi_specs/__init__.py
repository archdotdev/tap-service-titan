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
        result["nullable"] = len(key_properties) == 0
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
    if result.get("nullable", False) and "null" not in types:
        result["type"] = [*types, "null"]

    if "string" in types and "enum" in result:
        result.pop("enum")

    return result


class ServiceTitanOpenAPISchema(OpenAPISchema):
    """ServiceTitan OpenAPI schema."""

    @override
    @cached_property
    def spec(self) -> dict[str, Any]:
        """Get the spec."""
        spec = super().spec
        schemas = spec["components"]["schemas"]

        # Accounting
        for comp in (
            "Accounting.V2.JournalEntryResponse",
            "Accounting.V2.JournalEntrySummaryResponse",
            "Accounting.V2.JournalEntryDetailsResponse",
        ):
            if comp in schemas:
                props = schemas[comp]["properties"]
                # Values are coming in as '2025-10-13T00:00:00', so not valid ISO dates
                props["postDate"]["format"] = "date-time"

        return spec


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
        normalized = _normalize_schema(schema, key_properties=stream.primary_keys)

        if stream.name == "capacities":
            normalized["required"].remove("isAvailable")
            normalized["required"].remove("technicians")
            normalized["properties"].pop("isAvailable")
            technician_schema = normalized["properties"].pop("technicians")["items"]
            for prop, prop_schema in technician_schema["properties"].items():
                normalized["properties"][f"technician_{prop}"] = prop_schema

        if stream.name == "job_history":
            normalized["required"].append("jobId")
            normalized["properties"]["jobId"] = {
                "description": "ID of the job",
                "format": "int64",
                "type": "integer",
            }

        return normalized


OPENAPI_SPECS = files("tap_service_titan") / "openapi_specs"
ACCOUNTING = ServiceTitanOpenAPISchema(OPENAPI_SPECS / "accounting-v2.json")
CRM = ServiceTitanOpenAPISchema(OPENAPI_SPECS / "crm-v2.json")
DISPATCH = ServiceTitanOpenAPISchema(OPENAPI_SPECS / "dispatch-v2.json")
INVENTORY = ServiceTitanOpenAPISchema(OPENAPI_SPECS / "inventory-v2.json")
JPM = ServiceTitanOpenAPISchema(OPENAPI_SPECS / "jpm-v2.json")
SALESTECH = ServiceTitanOpenAPISchema(OPENAPI_SPECS / "salestech-v2.json")
SETTINGS = ServiceTitanOpenAPISchema(OPENAPI_SPECS / "settings-v2.json")
TELECOM = ServiceTitanOpenAPISchema(OPENAPI_SPECS / "telecom.json")
