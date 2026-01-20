"""Pricebook streams for the ServiceTitan tap."""

from __future__ import annotations

import sys
from functools import cached_property
from typing import TYPE_CHECKING, Any, cast

from tap_service_titan.client import ServiceTitanExportStream, ServiceTitanStream
from tap_service_titan.openapi_specs import PRICEBOOK, ServiceTitanSchema

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if TYPE_CHECKING:
    from singer_sdk.helpers.types import Context


class ClientSpecificPricingStream(ServiceTitanStream):
    """Define client-specific pricing stream."""

    name = "client_specific_pricing"
    primary_keys = ("id",)
    schema = ServiceTitanSchema(
        PRICEBOOK,
        key="Estimates.V2.ClientSpecificPricingResponse",
    )

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/pricebook/v2/tenant/{self.tenant_id}/clientspecificpricing"


class PricebookCategoriesStream(ServiceTitanStream):
    """Define pricebook categories stream."""

    name = "categories"
    primary_keys = ("id",)
    schema = ServiceTitanSchema(PRICEBOOK, key="Pricebook.V2.ExportCategoryResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/pricebook/v2/tenant/{self.tenant_id}/categories"

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: Any | None,
    ) -> dict[str, Any] | str:
        params = cast("dict[str, Any]", super().get_url_params(context, next_page_token))
        # https://developer.servicetitan.io/api-details/#api=tenant-pricebook-v2&operation=Categories_GetList

        # Return both active and inactive pricebook categories
        params["active"] = "Any"
        return params


class DiscountsAndFeesStream(ServiceTitanStream):
    """Define discounts and fees stream."""

    name = "discounts_and_fees"
    primary_keys = ("id",)
    schema = ServiceTitanSchema(PRICEBOOK, key="Pricebook.V2.DiscountAndFeesResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/pricebook/v2/tenant/{self.tenant_id}/discounts-and-fees"


class EquipmentStream(ServiceTitanStream):
    """Define equipment stream."""

    name = "equipment"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(PRICEBOOK, key="Pricebook.V2.EquipmentResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/pricebook/v2/tenant/{self.tenant_id}/equipment"


class MaterialsStream(ServiceTitanStream):
    """Define materials stream."""

    name = "materials"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(PRICEBOOK, key="Pricebook.V2.MaterialResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/pricebook/v2/tenant/{self.tenant_id}/materials"

    @override
    def get_url_params(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        params = cast("dict[str, Any]", super().get_url_params(*args, **kwargs))
        # https://developer.servicetitan.io/api-details/#api=tenant-pricebook-v2&operation=Materials_GetList

        # Return both active and inactive materials
        params["active"] = "Any"
        return params


class MaterialsMarkupStream(ServiceTitanStream):
    """Define materials markup stream."""

    name = "materials_markup"
    primary_keys = ("id",)
    schema = ServiceTitanSchema(PRICEBOOK, key="Pricebook.V2.MaterialsMarkupResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/pricebook/v2/tenant/{self.tenant_id}/materialsmarkup"


class ServicesStream(ServiceTitanStream):
    """Define services stream."""

    name = "services"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(PRICEBOOK, key="Pricebook.V2.ServiceGetResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/pricebook/v2/tenant/{self.tenant_id}/services"

    @override
    def get_url_params(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        # https://developer.servicetitan.io/api-details/#api=tenant-pricebook-v2&operation=Services_GetList
        params = cast("dict[str, Any]", super().get_url_params(*args, **kwargs))

        # If true, the prices will be calculated based on the current dynamic pricing rules.
        params["calculatePrices"] = True

        # Return both active and inactive materials
        params["active"] = "Any"
        return params


class ExportEquipmentStream(ServiceTitanExportStream):
    """Define export equipment stream."""

    name = "export_equipment"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(PRICEBOOK, key="Pricebook.V2.ExportEquipmentResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/pricebook/v2/tenant/{self.tenant_id}/export/equipment"


class ExportMaterialsStream(ServiceTitanExportStream):
    """Define export materials stream."""

    name = "export_materials"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(PRICEBOOK, key="Pricebook.V2.ExportMaterialResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/pricebook/v2/tenant/{self.tenant_id}/export/materials"


class ExportServicesStream(ServiceTitanExportStream):
    """Define export services stream."""

    name = "export_services"
    primary_keys = ("id",)
    replication_key: str = "modifiedOn"
    schema = ServiceTitanSchema(PRICEBOOK, key="Pricebook.V2.ExportServiceResponse")

    @override
    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/pricebook/v2/tenant/{self.tenant_id}/export/services"
