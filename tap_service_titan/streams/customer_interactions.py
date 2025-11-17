"""Customer interactions streams for the ServiceTitan tap."""

from __future__ import annotations

import sys
from functools import cached_property

from tap_service_titan.client import ServiceTitanExportStream
from tap_service_titan.openapi_specs import CUSTOMER_INTERACTIONS, ServiceTitanSchema

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


class TechnicianRatingsStream(ServiceTitanExportStream):
    """Define technician ratings stream."""

    name = "technician_ratings"
    primary_keys = ("technicianId", "jobId")
    replication_key = "modifiedOn"
    schema = ServiceTitanSchema(
        CUSTOMER_INTERACTIONS,
        key="CustomerInteractions.V2.ExportTechnicianAssessmentResponse",
    )

    @override
    @cached_property
    def path(self) -> str:
        return f"/customer-interactions/v2/tenant/{self.tenant_id}/export/technician-ratings"
