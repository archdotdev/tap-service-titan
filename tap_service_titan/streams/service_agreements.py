"""Service agreements streams for the ServiceTitan tap."""

from __future__ import annotations

import sys
from functools import cached_property
from typing import TYPE_CHECKING

from tap_service_titan.client import ServiceTitanExportStream
from tap_service_titan.openapi_specs import SERVICE_AGREEMENTS, ServiceTitanSchema

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if TYPE_CHECKING:
    from singer_sdk.helpers.types import Context, Record


class ServiceAgreementsStream(ServiceTitanExportStream):
    """Define service agreements stream."""

    name = "service_agreements"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(
        SERVICE_AGREEMENTS,
        key="ServiceAgreements.V2.ExportServiceAgreementResponse",
    )

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/service-agreements/v2/tenant/{self.tenant_id}/export/service-agreements"

    @override
    def post_process(self, row: Record, context: Context | None = None) -> Record | None:
        # Fix date fields, e.g. 2025-08-01T00:00:00 -> 2025-08-01
        if start_date := row.get("startDate"):
            row["startDate"] = start_date.split("T")[0]
        if end_date := row.get("endDate"):
            row["endDate"] = end_date.split("T")[0]
        return row
