"""Sales and estimates streams for the ServiceTitan tap."""

from __future__ import annotations

import sys
import typing as t
from functools import cached_property

from singer_sdk.streams import Stream

from tap_service_titan.client import ServiceTitanExportStream
from tap_service_titan.openapi_specs import SALESTECH, ServiceTitanSchema

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


class EstimatesStream(ServiceTitanExportStream):
    """Define estimates stream."""

    name = "estimates"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(SALESTECH, key="Estimates.V2.ExportEstimatesResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/sales/v2/tenant/{self.tenant_id}/estimates/export"

    @override
    def get_child_context(self, record: dict, context: dict | None) -> dict:
        # Was polluting our context with too many items causing logs to be >500 MB per run
        # for some tenants
        if not hasattr(self._tap, "_estimate_items_cache"):
            self._tap._estimate_items_cache = {}  # noqa: SLF001
        self._tap._estimate_items_cache[record["id"]] = record.get("items", [])  # noqa: SLF001

        return {
            "estimate_id": record["id"],
        }


class EstimateItemsStream(Stream):
    """Define estimate items stream as a child of estimates.

    It would be better if this class didn't exist and we used transformations instead as we're not
    actually doing a request here.
    """

    name = "estimate_items"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    parent_stream_type = EstimatesStream

    # We don't need to partition state since we rely on parent's state
    state_partitioning_keys: t.ClassVar[list[str]] = []

    schema = ServiceTitanSchema(SALESTECH, key="Estimates.V2.EstimateItemResponse")

    @override
    def get_records(self, context: dict | None) -> t.Iterable[dict]:
        """Return a generator of row-type dictionary objects.

        Args:
            context: The stream partition or context dictionary containing the parent's
                    estimate_id and items array.
        """
        if not context:
            return
        estimate_id = context["estimate_id"]
        items = getattr(self._tap, "_estimate_items_cache", {}).get(estimate_id, [])

        try:
            for item in items:
                transformed_item = {**item, "estimate_id": estimate_id}
                yield transformed_item
        finally:
            if hasattr(self._tap, "_estimate_items_cache"):
                self._tap._estimate_items_cache.pop(estimate_id, None)  # noqa: SLF001
