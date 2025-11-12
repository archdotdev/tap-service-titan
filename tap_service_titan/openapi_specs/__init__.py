"""OpenAPI specs for the ServiceTitan tap."""

from __future__ import annotations

import logging
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
    "EQUIPMENT_SYSTEMS",
    "FORMS",
    "INVENTORY",
    "JBCE",
    "JPM",
    "MARKETING_ADS",
    "MARKETING_REPUTATION",
    "MEMBERSHIPS",
    "PAYROLL",
    "PRICEBOOK",
    "SALESTECH",
    "SCHEDULING_PRO",
    "SERVICE_AGREEMENTS",
    "SETTINGS",
    "TASK_MANAGEMENT",
    "TELECOM",
]

logger = logging.getLogger(__name__)


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

    # Remove 'enum' keyword
    result.pop("enum", None)

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

        if stream.name == "estimates":
            if "proposalTagName" in normalized["properties"]:
                logger.warning("proposalTagName is already present in the schema")
            else:
                normalized["properties"]["proposalTagName"] = {"type": ["string", "null"]}

        if stream.name == "estimate_items":
            normalized["properties"]["estimate_id"] = {
                "format": "int64",
                "type": "integer",
            }

        if stream.name == "categories":
            normalized["required"].remove("modifiedOn")

        if stream.name in ("campaign_performance", "keyword_performance", "adgroup_performance"):
            # TODO(maintainers): Remove these `status` patches once ServiceTitan fixes this.
            # https://github.com/archdotdev/tap-service-titan/issues/163
            normalized["properties"]["campaign"]["properties"]["status"]["type"] = [
                "integer",
                "null",
            ]
            normalized["properties"]["adGroup"]["properties"]["status"]["type"] = [
                "integer",
                "null",
            ]
            normalized["properties"]["keyword"]["properties"]["status"]["type"] = [
                "integer",
                "null",
            ]
            normalized["properties"] |= {
                "date": {
                    "type": ["string", "null"],
                    "format": "date",
                },
                "from_utc": {
                    "type": ["string", "null"],
                    "format": "date-time",
                },
                "to_utc": {
                    "type": ["string", "null"],
                    "format": "date-time",
                },
                "campaign_id": normalized["properties"]["campaign"]["properties"]["id"],
                "campaign_name": normalized["properties"]["campaign"]["properties"]["name"],
                "adGroup_id": normalized["properties"]["adGroup"]["properties"]["id"],
                "keyword_id": normalized["properties"]["keyword"]["properties"]["id"],
            }

        return normalized


SPECS = files("tap_service_titan") / "openapi_specs"
ACCOUNTING = ServiceTitanOpenAPISchema(SPECS / "accounting-v2.json")
CRM = ServiceTitanOpenAPISchema(SPECS / "crm-v2.json")
DISPATCH = ServiceTitanOpenAPISchema(SPECS / "dispatch-v2.json")
EQUIPMENT_SYSTEMS = ServiceTitanOpenAPISchema(SPECS / "equipment-systems-v2.json")
FORMS = ServiceTitanOpenAPISchema(SPECS / "forms-v2.json")
INVENTORY = ServiceTitanOpenAPISchema(SPECS / "inventory-v2.json")
JBCE = ServiceTitanOpenAPISchema(SPECS / "jbce-v2.json")
JPM = ServiceTitanOpenAPISchema(SPECS / "jpm-v2.json")
MARKETING = ServiceTitanOpenAPISchema(SPECS / "marketing-v2.json")
MARKETING_ADS = ServiceTitanOpenAPISchema(SPECS / "marketing-ads-v2.json")
MARKETING_REPUTATION = ServiceTitanOpenAPISchema(SPECS / "marketing-reputation-v2.json")
MEMBERSHIPS = ServiceTitanOpenAPISchema(SPECS / "memberships-v2.json")
PAYROLL = ServiceTitanOpenAPISchema(SPECS / "payroll-v2.json")
PRICEBOOK = ServiceTitanOpenAPISchema(SPECS / "pricebook-v2.json")
SALESTECH = ServiceTitanOpenAPISchema(SPECS / "salestech-v2.json")
SCHEDULING_PRO = ServiceTitanOpenAPISchema(SPECS / "scheduling-pro-v2.json")
SERVICE_AGREEMENTS = ServiceTitanOpenAPISchema(SPECS / "service-agreements-v2.json")
SETTINGS = ServiceTitanOpenAPISchema(SPECS / "settings-v2.json")
TASK_MANAGEMENT = ServiceTitanOpenAPISchema(SPECS / "task-management-v2.json")
TELECOM = ServiceTitanOpenAPISchema(SPECS / "telecom.json")
