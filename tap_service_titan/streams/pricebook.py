"""Pricebook streams for the ServiceTitan tap."""

from __future__ import annotations

import sys
from functools import cached_property
from typing import Any

from tap_service_titan.client import ServiceTitanExportStream, ServiceTitanStream
from tap_service_titan.openapi_specs import PRICEBOOK, ServiceTitanSchema

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


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
        return {
            **super().get_url_params(*args, **kwargs),
            "calculatePrices": True,
        }


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
