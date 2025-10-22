"""Task management streams for the ServiceTitan tap."""

from __future__ import annotations

import sys
from functools import cached_property

from tap_service_titan.client import ServiceTitanStream
from tap_service_titan.openapi_specs import TASK_MANAGEMENT, ServiceTitanSchema

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


class TasksStream(ServiceTitanStream):
    """Define tasks stream."""

    name = "tasks"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(TASK_MANAGEMENT, key="TaskManagement.V2.TaskGetResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/task-management/v2/tenant/{self.tenant_id}/tasks"
