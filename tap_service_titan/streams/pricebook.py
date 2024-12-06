"""Pricebook streams for the ServiceTitan tap."""

from __future__ import annotations

import typing as t
from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_service_titan.client import (
    ServiceTitanStream,
)


class ClientSpecificPricingStream(ServiceTitanStream):
    """Define client-specific pricing stream."""

    name = "client_specific_pricing"
    primary_keys: t.ClassVar[list[str]] = ["id"]

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property(
            "exceptions",
            th.ArrayType(
                th.ObjectType(
                    th.Property("skuId", th.IntegerType),
                    th.Property("skuType", th.StringType),
                    th.Property("value", th.NumberType),
                    th.Property("valueType", th.StringType),
                )
            ),
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/pricebook/v2/tenant/{self._tap.config['tenant_id']}/clientspecificpricing"


class PricebookCategoriesStream(ServiceTitanStream):
    """Define pricebook categories stream."""

    name = "categories"
    primary_keys: t.ClassVar[list[str]] = ["id"]

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("active", th.BooleanType),
        th.Property("description", th.StringType),
        th.Property("image", th.StringType),
        th.Property("parentId", th.IntegerType),
        th.Property("position", th.IntegerType),
        th.Property("categoryType", th.StringType),
        th.Property(
            "subcategories",
            th.ArrayType(
                th.ObjectType()  # Recursive definition, but left empty as details not specified
            ),
        ),
        th.Property("businessUnitIds", th.ArrayType(th.IntegerType)),
        th.Property("skuImages", th.ArrayType(th.StringType)),
        th.Property("skuVideos", th.ArrayType(th.StringType)),
        th.Property("source", th.StringType),
        th.Property("externalId", th.StringType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/pricebook/v2/tenant/{self._tap.config['tenant_id']}/categories"


class DiscountsAndFeesStream(ServiceTitanStream):
    """Define discounts and fees stream."""

    name = "discounts_and_fees"
    primary_keys: t.ClassVar[list[str]] = ["id"]

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("type", th.StringType),
        th.Property("code", th.StringType),
        th.Property("displayName", th.StringType),
        th.Property("description", th.StringType),
        th.Property("amountType", th.StringType),
        th.Property("amount", th.NumberType),
        th.Property("limit", th.NumberType),
        th.Property("taxable", th.BooleanType),
        th.Property("categories", th.ArrayType(th.IntegerType)),
        th.Property("hours", th.NumberType),
        th.Property(
            "assets",
            th.ArrayType(
                th.ObjectType(
                    th.Property("alias", th.StringType),
                    th.Property("fileName", th.StringType),
                    th.Property("type", th.StringType),
                    th.Property("url", th.StringType),
                )
            ),
        ),
        th.Property("account", th.StringType),
        th.Property("crossSaleGroup", th.StringType),
        th.Property("active", th.BooleanType),
        th.Property("bonus", th.NumberType),
        th.Property("commissionBonus", th.NumberType),
        th.Property("paysCommission", th.BooleanType),
        th.Property("excludeFromPayroll", th.BooleanType),
        th.Property(
            "externalData",
            th.ArrayType(
                th.ObjectType(
                    th.Property("key", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return (
            f"/pricebook/v2/tenant/{self._tap.config['tenant_id']}/discounts-and-fees"
        )


class EquipmentStream(ServiceTitanStream):
    """Define equipment stream."""

    name = "equipment"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("code", th.StringType),
        th.Property("displayName", th.StringType),
        th.Property("description", th.StringType),
        th.Property("active", th.BooleanType),
        th.Property("price", th.NumberType),
        th.Property("memberPrice", th.NumberType),
        th.Property("addOnPrice", th.NumberType),
        th.Property("addOnMemberPrice", th.NumberType),
        th.Property("manufacturer", th.StringType),
        th.Property("model", th.StringType),
        th.Property(
            "manufacturerWarranty",
            th.ObjectType(
                th.Property("duration", th.IntegerType),
                th.Property("description", th.StringType),
            ),
        ),
        th.Property(
            "serviceProviderWarranty",
            th.ObjectType(
                th.Property("duration", th.IntegerType),
                th.Property("description", th.StringType),
            ),
        ),
        th.Property("categories", th.ArrayType(th.IntegerType)),
        th.Property(
            "assets",
            th.ArrayType(
                th.ObjectType(
                    th.Property("alias", th.StringType),
                    th.Property("fileName", th.StringType),
                    th.Property("type", th.StringType),
                    th.Property("url", th.StringType),
                )
            ),
        ),
        th.Property(
            "recommendations",
            th.ArrayType(
                th.ObjectType(
                    th.Property("skuId", th.IntegerType),
                    th.Property("type", th.StringType),
                )
            ),
        ),
        th.Property("upgrades", th.ArrayType(th.IntegerType)),
        th.Property(
            "equipmentMaterials",
            th.ArrayType(
                th.ObjectType(
                    th.Property("skuId", th.IntegerType),
                    th.Property("quantity", th.NumberType),
                )
            ),
        ),
        th.Property(
            "primaryVendor",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("vendorName", th.StringType),
                th.Property("vendorId", th.IntegerType),
                th.Property("memo", th.StringType),
                th.Property("vendorPart", th.StringType),
                th.Property("cost", th.NumberType),
                th.Property("active", th.BooleanType),
                th.Property(
                    "primarySubAccount",
                    th.ObjectType(
                        th.Property("id", th.IntegerType),
                        th.Property("cost", th.NumberType),
                        th.Property("accountName", th.StringType),
                    ),
                ),
                th.Property(
                    "otherSubAccounts",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("id", th.IntegerType),
                            th.Property("cost", th.NumberType),
                            th.Property("accountName", th.StringType),
                        )
                    ),
                ),
            ),
        ),
        th.Property(
            "otherVendors",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property("vendorName", th.StringType),
                    th.Property("vendorId", th.IntegerType),
                    th.Property("memo", th.StringType),
                    th.Property("vendorPart", th.StringType),
                    th.Property("cost", th.NumberType),
                    th.Property("active", th.BooleanType),
                    th.Property(
                        "primarySubAccount",
                        th.ObjectType(
                            th.Property("id", th.IntegerType),
                            th.Property("cost", th.NumberType),
                            th.Property("accountName", th.StringType),
                        ),
                    ),
                    th.Property(
                        "otherSubAccounts",
                        th.ArrayType(
                            th.ObjectType(
                                th.Property("id", th.IntegerType),
                                th.Property("cost", th.NumberType),
                                th.Property("accountName", th.StringType),
                            )
                        ),
                    ),
                )
            ),
        ),
        th.Property("account", th.StringType),
        th.Property("costOfSaleAccount", th.StringType),
        th.Property("assetAccount", th.StringType),
        th.Property("crossSaleGroup", th.StringType),
        th.Property("paysCommission", th.BooleanType),
        th.Property("bonus", th.NumberType),
        th.Property("commissionBonus", th.NumberType),
        th.Property("hours", th.NumberType),
        th.Property("taxable", th.BooleanType),
        th.Property("cost", th.NumberType),
        th.Property("unitOfMeasure", th.StringType),
        th.Property("isInventory", th.BooleanType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("source", th.StringType),
        th.Property("externalId", th.StringType),
        th.Property(
            "externalData",
            th.ArrayType(
                th.ObjectType(
                    th.Property("key", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
        th.Property("isConfigurableEquipment", th.BooleanType),
        th.Property("variationsOrConfigurableEquipment", th.ArrayType(th.IntegerType)),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/pricebook/v2/tenant/{self._tap.config['tenant_id']}/equipment"


class MaterialsStream(ServiceTitanStream):
    """Define materials stream."""

    name = "materials"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("code", th.StringType),
        th.Property("displayName", th.StringType),
        th.Property("description", th.StringType),
        th.Property("cost", th.NumberType),
        th.Property("active", th.BooleanType),
        th.Property("price", th.NumberType),
        th.Property("memberPrice", th.NumberType),
        th.Property("addOnPrice", th.NumberType),
        th.Property("addOnMemberPrice", th.NumberType),
        th.Property("hours", th.NumberType),
        th.Property("bonus", th.NumberType),
        th.Property("commissionBonus", th.NumberType),
        th.Property("paysCommission", th.BooleanType),
        th.Property("deductAsJobCost", th.BooleanType),
        th.Property("unitOfMeasure", th.StringType),
        th.Property("isInventory", th.BooleanType),
        th.Property("account", th.StringType),
        th.Property("costOfSaleAccount", th.StringType),
        th.Property("assetAccount", th.StringType),
        th.Property("taxable", th.BooleanType),
        th.Property(
            "primaryVendor",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("vendorName", th.StringType),
                th.Property("vendorId", th.IntegerType),
                th.Property("memo", th.StringType),
                th.Property("vendorPart", th.StringType),
                th.Property("cost", th.NumberType),
                th.Property("active", th.BooleanType),
                th.Property(
                    "primarySubAccount",
                    th.ObjectType(
                        th.Property("id", th.IntegerType),
                        th.Property("cost", th.NumberType),
                        th.Property("accountName", th.StringType),
                    ),
                ),
                th.Property(
                    "otherSubAccounts",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("id", th.IntegerType),
                            th.Property("cost", th.NumberType),
                            th.Property("accountName", th.StringType),
                        )
                    ),
                ),
            ),
        ),
        th.Property(
            "otherVendors",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property("vendorName", th.StringType),
                    th.Property("vendorId", th.IntegerType),
                    th.Property("memo", th.StringType),
                    th.Property("vendorPart", th.StringType),
                    th.Property("cost", th.NumberType),
                    th.Property("active", th.BooleanType),
                    th.Property(
                        "primarySubAccount",
                        th.ObjectType(
                            th.Property("id", th.IntegerType),
                            th.Property("cost", th.NumberType),
                            th.Property("accountName", th.StringType),
                        ),
                    ),
                    th.Property(
                        "otherSubAccounts",
                        th.ArrayType(
                            th.ObjectType(
                                th.Property("id", th.IntegerType),
                                th.Property("cost", th.NumberType),
                                th.Property("accountName", th.StringType),
                            )
                        ),
                    ),
                )
            ),
        ),
        th.Property("categories", th.ArrayType(th.IntegerType)),
        th.Property(
            "assets",
            th.ArrayType(
                th.ObjectType(
                    th.Property("alias", th.StringType),
                    th.Property("fileName", th.StringType),
                    th.Property("type", th.StringType),
                    th.Property("url", th.StringType),
                )
            ),
        ),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("source", th.StringType),
        th.Property("externalId", th.StringType),
        th.Property(
            "externalData",
            th.ArrayType(
                th.ObjectType(
                    th.Property("key", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
        th.Property("isConfigurableMaterial", th.BooleanType),
        th.Property("chargeableByDefault", th.BooleanType),
        th.Property("variationsOrConfigurableMaterials", th.ArrayType(th.IntegerType)),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/pricebook/v2/tenant/{self._tap.config['tenant_id']}/materials"


class MaterialsMarkupStream(ServiceTitanStream):
    """Define materials markup stream."""

    name = "materials_markup"
    primary_keys: t.ClassVar[list[str]] = ["id"]

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("from", th.NumberType),
        th.Property("to", th.NumberType),
        th.Property("percent", th.NumberType),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/pricebook/v2/tenant/{self._tap.config['tenant_id']}/materialsmarkup"


class ServicesStream(ServiceTitanStream):
    """Define services stream."""

    name = "services"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("code", th.StringType),
        th.Property("displayName", th.StringType),
        th.Property("description", th.StringType),
        th.Property(
            "warranty",
            th.ObjectType(
                th.Property("duration", th.IntegerType),
                th.Property("description", th.StringType),
            ),
        ),
        th.Property(
            "categories",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property("name", th.StringType),
                    th.Property("active", th.BooleanType),
                )
            ),
        ),
        th.Property("price", th.NumberType),
        th.Property("memberPrice", th.NumberType),
        th.Property("addOnPrice", th.NumberType),
        th.Property("addOnMemberPrice", th.NumberType),
        th.Property("taxable", th.BooleanType),
        th.Property("account", th.StringType),
        th.Property("hours", th.NumberType),
        th.Property("isLabor", th.BooleanType),
        th.Property("recommendations", th.ArrayType(th.IntegerType)),
        th.Property("upgrades", th.ArrayType(th.IntegerType)),
        th.Property(
            "assets",
            th.ArrayType(
                th.ObjectType(
                    th.Property("alias", th.StringType),
                    th.Property("fileName", th.StringType),
                    th.Property("type", th.StringType),
                    th.Property("url", th.StringType),
                )
            ),
        ),
        th.Property(
            "serviceMaterials",
            th.ArrayType(
                th.ObjectType(
                    th.Property("skuId", th.IntegerType),
                    th.Property("quantity", th.NumberType),
                )
            ),
        ),
        th.Property(
            "serviceEquipment",
            th.ArrayType(
                th.ObjectType(
                    th.Property("skuId", th.IntegerType),
                    th.Property("quantity", th.NumberType),
                )
            ),
        ),
        th.Property("active", th.BooleanType),
        th.Property("crossSaleGroup", th.StringType),
        th.Property("paysCommission", th.BooleanType),
        th.Property("bonus", th.NumberType),
        th.Property("commissionBonus", th.NumberType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("source", th.StringType),
        th.Property("externalId", th.StringType),
        th.Property(
            "externalData",
            th.ArrayType(
                th.ObjectType(
                    th.Property("key", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/pricebook/v2/tenant/{self._tap.config['tenant_id']}/services"
