"""Stream type classes for tap-service-titan."""

from __future__ import annotations

import sys
import typing as t
from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_service_titan.client import ServiceTitanStream

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources


# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = importlib_resources.files(__package__) / "schemas"
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.


class AppointmentsStream(ServiceTitanStream):
    """Define custom stream."""

    name = "appointments"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"  # noqa: ERA001
    schema = th.PropertiesList(
        th.Property("active", th.BooleanType),
        th.Property("id", th.IntegerType),
        th.Property("jobId", th.IntegerType),
        th.Property("appointmentNumber", th.StringType),
        th.Property("start", th.StringType),
        th.Property("end", th.StringType),
        th.Property("arrivalWindowStart", th.StringType),
        th.Property("arrivalWindowEnd", th.StringType),
        th.Property("status", th.StringType),
        th.Property("specialInstructions", th.StringType),
        th.Property("createdOn", th.StringType),
        th.Property("modifiedOn", th.StringType),
        th.Property("customerId", th.IntegerType),
        th.Property("unused", th.BooleanType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/jpm/v2/tenant/{self._tap.config['tenant_id']}/export/appointments"
