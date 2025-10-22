"""Job booking streams for the ServiceTitan tap."""

from __future__ import annotations

import sys
from functools import cached_property

from tap_service_titan.client import ServiceTitanStream
from tap_service_titan.openapi_specs import JBCE, ServiceTitanSchema

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


class CallReasonsStream(ServiceTitanStream):
    """Define call reasons stream."""

    name = "call_reasons"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(JBCE, key="Jbce.V2.CallReasonResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/jbce/v2/tenant/{self.tenant_id}/call-reasons"
