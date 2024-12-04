"""Settings streams for the ServiceTitan tap."""

from __future__ import annotations

import typing as t
from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_service_titan.client import ServiceTitanExportStream, ServiceTitanStream


class EmployeesStream(ServiceTitanExportStream):
    """Define employees stream."""

    name = "employees"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("userId", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("role", th.StringType),
        th.Property("roleIds", th.ArrayType(th.IntegerType)),
        th.Property("businessUnitId", th.IntegerType, required=False),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("email", th.StringType, required=False),
        th.Property("phoneNumber", th.StringType, required=False),
        th.Property("loginName", th.StringType, required=False),
        th.Property(
            "customFields",
            th.ArrayType(
                th.ObjectType(
                    th.Property("typeId", th.IntegerType),
                    th.Property("name", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
            required=False,
        ),
        th.Property("active", th.BooleanType),
        th.Property("aadUserId", th.StringType, required=False),
        th.Property(
            "permissions",
            th.ArrayType(
                th.OneOf(
                    th.ObjectType(
                        th.Property("id", th.IntegerType),
                        th.Property("value", th.StringType),
                    ),
                    # Array may contain Nones -- falling back to AnyType for now
                    th.AnyType,
                )
            ),
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/settings/v2/tenant/{self._tap.config['tenant_id']}/export/employees"


class BusinessUnitsStream(ServiceTitanExportStream):
    """Define business units stream."""

    name = "business_units"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("active", th.BooleanType),
        th.Property("name", th.StringType),
        th.Property("officialName", th.StringType, required=False),
        th.Property("email", th.StringType, required=False),
        th.Property("phoneNumber", th.StringType, required=False),
        th.Property("invoiceHeader", th.StringType, required=False),
        th.Property("invoiceMessage", th.StringType, required=False),
        th.Property("defaultTaxRate", th.NumberType, required=False),
        th.Property("authorizationParagraph", th.StringType, required=False),
        th.Property("acknowledgementParagraph", th.StringType, required=False),
        th.Property(
            "address",
            th.ObjectType(
                th.Property("street", th.StringType),
                th.Property("unit", th.StringType),
                th.Property("city", th.StringType),
                th.Property("state", th.StringType),
                th.Property("zip", th.StringType),
                th.Property("country", th.StringType),
            ),
            required=False,
        ),
        th.Property("materialSku", th.StringType, required=False),
        th.Property("quickbooksClass", th.StringType, required=False),
        th.Property("accountCode", th.StringType, required=False),
        th.Property("franchiseId", th.StringType, required=False),
        th.Property("conceptCode", th.StringType, required=False),
        th.Property("corporateContractNumber", th.StringType, required=False),
        th.Property(
            "tenant",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
                th.Property("accountCode", th.StringType),
                th.Property("franchiseId", th.StringType),
                th.Property("conceptCode", th.StringType),
                th.Property("modifiedOn", th.DateTimeType),
            ),
            required=False,
        ),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property(
            "externalData",
            th.ArrayType(
                th.ObjectType(
                    th.Property("key", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
            required=False,
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return (
            f"/settings/v2/tenant/{self._tap.config['tenant_id']}/export/business-units"
        )


class TechniciansStream(ServiceTitanExportStream):
    """Define technicians stream."""

    name = "technicians"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("userId", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("roleIds", th.ArrayType(th.IntegerType())),
        th.Property("businessUnitId", th.IntegerType),
        th.Property("mainZoneId", th.IntegerType),
        th.Property("zoneIds", th.ArrayType(th.IntegerType())),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("email", th.StringType),
        th.Property("phoneNumber", th.StringType),
        th.Property("loginName", th.StringType),
        th.Property(
            "home",
            th.ObjectType(
                th.Property("street", th.StringType),
                th.Property("unit", th.StringType),
                th.Property("country", th.StringType),
                th.Property("city", th.StringType),
                th.Property("state", th.StringType),
                th.Property("zip", th.StringType),
                th.Property("streetAddress", th.StringType),
                th.Property("latitude", th.NumberType),
                th.Property("longitude", th.NumberType),
            ),
        ),
        th.Property("dailyGoal", th.NumberType),
        th.Property("isManagedTech", th.BooleanType),
        th.Property(
            "customFields",
            th.ArrayType(
                th.ObjectType(
                    th.Property("typeId", th.IntegerType),
                    th.Property("name", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
        th.Property("active", th.BooleanType),
        th.Property("aadUserId", th.StringType),
        th.Property("burdenRate", th.NumberType),
        th.Property("team", th.StringType),
        th.Property("jobFilter", th.StringType),
        th.Property(
            "permissions",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/settings/v2/tenant/{self._tap.config['tenant_id']}/export/technicians"


class TagTypesStream(ServiceTitanStream):
    """Define tag types stream."""

    name = "tag_types"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("color", th.StringType),
        th.Property("code", th.StringType),
        th.Property("importance", th.StringType),
        th.Property("isConversionOpportunity", th.BooleanType),
        th.Property("active", th.BooleanType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/settings/v2/tenant/{self._tap.config['tenant_id']}/tag-types"
