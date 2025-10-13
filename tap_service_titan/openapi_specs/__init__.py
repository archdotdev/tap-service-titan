"""OpenAPI specs for the ServiceTitan tap."""

from __future__ import annotations

import sys
from copy import deepcopy
from functools import cached_property
from importlib.resources import files
from typing import Any

from singer_sdk import OpenAPISchema

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

__all__ = [
    "ACCOUNTING",
    "CRM",
    "DISPATCH",
    "INVENTORY",
    "SALESTECH",
    "SETTINGS",
    "TELECOM",
]


def _normalize_schema(schema: dict[str, Any]) -> dict[str, Any]:
    """Normalize OpenAPI attributes to standard JSON Schema features.

    Args:
        schema: A JSON Schema dictionary.

    - Converts 'nullable' to 'type': [<type>, "null"]
    - Converts {'field': {'oneOf': [{...} (1 item only)]}} to {'field': {...}}

    Returns:
        A new JSON Schema dictionary, normalized.
    """
    result = deepcopy(schema)
    schema_type: str | list[str] = result.get("type", [])

    if "object" in schema_type:
        for prop, prop_schema in result.get("properties", {}).items():
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

    return result


class ServiceTitanOpenAPISchema(OpenAPISchema):
    """ServiceTitan OpenAPI schema."""

    @override
    @cached_property
    def spec(self) -> dict[str, Any]:
        """Get the spec."""
        spec = super().spec
        schemas = spec["components"]["schemas"]
        if "Crm.V2.AddressModel" in schemas:
            schemas["Crm.V2.AddressModel"]["properties"]["street"]["nullable"] = True
            schemas["Crm.V2.AddressModel"]["properties"]["city"]["nullable"] = True
            schemas["Crm.V2.AddressModel"]["properties"]["state"]["nullable"] = True
            schemas["Crm.V2.AddressModel"]["properties"]["zip"]["nullable"] = True
            schemas["Crm.V2.AddressModel"]["properties"]["country"]["nullable"] = True
        if "Crm.V2.CustomerType" in schemas:
            schemas["Crm.V2.CustomerType"]["enum"].append(None)
        return spec

    @override
    def fetch_schema(self, key: str) -> dict[str, Any]:
        """Fetch the schema for the given key."""
        schema = super().fetch_schema(key)
        return _normalize_schema(schema)


OPENAPI_SPECS = files("tap_service_titan") / "openapi_specs"
ACCOUNTING = ServiceTitanOpenAPISchema(OPENAPI_SPECS / "accounting-v2.json")
CRM = ServiceTitanOpenAPISchema(OPENAPI_SPECS / "crm-v2.json")
DISPATCH = ServiceTitanOpenAPISchema(OPENAPI_SPECS / "dispatch-v2.json")
INVENTORY = ServiceTitanOpenAPISchema(OPENAPI_SPECS / "inventory-v2.json")
SALESTECH = ServiceTitanOpenAPISchema(OPENAPI_SPECS / "salestech-v2.json")
SETTINGS = ServiceTitanOpenAPISchema(OPENAPI_SPECS / "settings-v2.json")
TELECOM = ServiceTitanOpenAPISchema(OPENAPI_SPECS / "telecom.json")
