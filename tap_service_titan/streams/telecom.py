"""Telecom streams for the ServiceTitan tap."""

from __future__ import annotations

import sys
from functools import cached_property

from tap_service_titan.client import ServiceTitanExportStream, ServiceTitanStream
from tap_service_titan.openapi_specs import TELECOM, ServiceTitanSchema

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


class CallsStream(ServiceTitanExportStream):
    """Define calls stream."""

    name = "calls"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(TELECOM, key="Telecom.V2.ExportCallResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/telecom/v2/tenant/{self.tenant_id}/export/calls"


class OptOutsStream(ServiceTitanStream):
    """Define opt-outs stream."""

    name = "opt_outs"
    primary_keys = ("contactNumber",)
    schema = ServiceTitanSchema(TELECOM, key="Telecom.V3.OptOutResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/telecom/v3/tenant/{self.tenant_id}/optinouts/optouts"
