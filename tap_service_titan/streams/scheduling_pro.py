"""Scheduling streams for the ServiceTitan tap."""

from __future__ import annotations

import sys
from functools import cached_property
from typing import TYPE_CHECKING

from tap_service_titan.client import ServiceTitanStream
from tap_service_titan.openapi_specs import SCHEDULING_PRO, ServiceTitanSchema

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if TYPE_CHECKING:
    from singer_sdk.helpers.types import Context, Record


class SchedulersStream(ServiceTitanStream):
    """Define schedulers stream."""

    name = "schedulers"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(SCHEDULING_PRO, key="SchedulingPro.V2.SchedulerResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/schedulingpro/v2/tenant/{self.tenant_id}/schedulers"

    @override
    def get_child_context(self, record: Record, context: Context | None) -> dict:
        """Return a context dictionary for child streams."""
        return {"scheduler_id": record.get("id")}


class SchedulerSessionsStream(ServiceTitanStream):
    """Define scheduler sessions stream."""

    name = "scheduler_sessions"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    parent_stream_type = SchedulersStream
    schema = ServiceTitanSchema(
        SCHEDULING_PRO,
        key="SchedulingPro.V2.SchedulerSessionResponse",
    )

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/schedulingpro/v2/tenant/{self.tenant_id}/schedulers/{{scheduler_id}}/sessions"


class SchedulerPerformanceStream(ServiceTitanStream):
    """Define scheduler performance stream."""

    name = "scheduler_performance"
    primary_keys = ("id",)
    parent_stream_type = SchedulersStream
    ignore_parent_replication_key = True
    schema = ServiceTitanSchema(
        SCHEDULING_PRO,
        key="SchedulingPro.V2.SchedulerPerformanceResponse",
    )

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/schedulingpro/v2/tenant/{self.tenant_id}/schedulers/{{scheduler_id}}/performance"
