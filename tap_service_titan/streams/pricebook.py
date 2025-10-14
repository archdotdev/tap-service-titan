"""Pricebook streams for the ServiceTitan tap."""

from __future__ import annotations

import typing as t
from functools import cached_property

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_service_titan.client import (
    ServiceTitanExportStream,
    ServiceTitanStream,
)
from tap_service_titan.openapi_specs import PRICEBOOK, ServiceTitanSchema


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
        return f"/pricebook/v2/tenant/{self._tap.config['tenant_id']}/clientspecificpricing"  # noqa: E501


class PricebookCategoriesStream(ServiceTitanStream):
    """Define pricebook categories stream."""

    name = "categories"
    primary_keys = ("id",)
    schema = ServiceTitanSchema(PRICEBOOK, key="Pricebook.V2.ExportCategoryResponse")

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


class ExportEquipmentStream(ServiceTitanExportStream):
    """Define export equipment stream."""

    name = "export_equipment"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property(
            "id", th.IntegerType, description="Unique id for the SKU", required=True
        ),
        th.Property(
            "code", th.StringType, description="Code for the SKU", required=True
        ),
        th.Property(
            "displayName",
            th.StringType,
            description="Name that displays with the SKU",
            nullable=True,
        ),
        th.Property(
            "description",
            th.StringType,
            description="Description on the SKU that is displayed with the item",
            required=True,
        ),
        th.Property(
            "active",
            th.BooleanType,
            description="Active shows if the SKU is active or inactive",
            required=True,
        ),
        th.Property(
            "price", th.NumberType, description="Price of this SKU sold", required=True
        ),
        th.Property(
            "memberPrice",
            th.NumberType,
            description="The price if the item is sold to a member",
            required=True,
        ),
        th.Property(
            "addOnPrice",
            th.NumberType,
            description="The price of the SKU is sold as an add-on item",
            required=True,
        ),
        th.Property(
            "addOnMemberPrice",
            th.NumberType,
            description="The price if the SKU is sold to a member as an add-on item",
            required=True,
        ),
        th.Property(
            "manufacturer",
            th.StringType,
            description="Name of the manufactures",
            nullable=True,
        ),
        th.Property(
            "model",
            th.StringType,
            description="The model of the equipment",
            nullable=True,
        ),
        th.Property(
            "manufacturerWarranty",
            th.ObjectType(
                th.Property(
                    "duration",
                    th.IntegerType,
                    description="Warranty duration",
                    required=True,
                ),
                th.Property(
                    "description",
                    th.StringType,
                    description="Description of the warranty included in this SKU",
                    nullable=True,
                ),
            ),
            description="Description of the manufacturer warranty included in this SKU",
            required=True,
        ),
        th.Property(
            "serviceProviderWarranty",
            th.ObjectType(
                th.Property(
                    "duration",
                    th.IntegerType,
                    description="Warranty duration",
                    required=True,
                ),
                th.Property(
                    "description",
                    th.StringType,
                    description="Description of the warranty included in this SKU",
                    nullable=True,
                ),
            ),
            description="Description of the manufacturer warranty included in this SKU",
            required=True,
        ),
        th.Property(
            "categories",
            th.ArrayType(th.IntegerType),
            description="Categories that this SKU belongs to",
            required=True,
        ),
        th.Property(
            "assets",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "alias",
                        th.StringType,
                        description="Asset alias",
                        nullable=True,
                    ),
                    th.Property(
                        "fileName",
                        th.StringType,
                        description="Asset file name when downloaded",
                        nullable=True,
                    ),
                    th.Property(
                        "isDefault",
                        th.BooleanType,
                        description="It is the default asset",
                        required=True,
                    ),
                    th.Property(
                        "type",
                        th.StringType,
                        description="Asset type - image, video or PDF",
                        required=True,
                    ),
                    th.Property(
                        "url", th.StringType, description="Asset URL", required=True
                    ),
                )
            ),
            description="Images, videos or PDFs attached to SKU",
            required=True,
        ),
        th.Property(
            "recommendations",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "skuId",
                        th.IntegerType,
                        description="SKU unique identifier",
                        required=True,
                    ),
                    th.Property(
                        "type",
                        th.StringType,
                        description="Recommended SKU type (Service or Material)",
                        required=True,
                    ),
                )
            ),
            description="Recommended services and materials to include with this SKU",
            required=True,
        ),
        th.Property(
            "upgrades",
            th.ArrayType(th.IntegerType),
            description="Upgrades that can be sold for this SKU",
            required=True,
        ),
        th.Property(
            "equipmentMaterials",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "skuId",
                        th.IntegerType,
                        description="Linked SKU unique id",
                        required=True,
                    ),
                    th.Property(
                        "quantity",
                        th.NumberType,
                        description="Quantity of linked SKUs",
                        required=True,
                    ),
                )
            ),
            description="Array of materials used with this equipment",
            required=True,
        ),
        th.Property(
            "primaryVendor",
            th.ObjectType(
                th.Property("id", th.IntegerType, required=True),
                th.Property("vendorName", th.StringType, required=True),
                th.Property("vendorId", th.IntegerType, required=True),
                th.Property("memo", th.StringType, nullable=True),
                th.Property("vendorPart", th.StringType, nullable=True),
                th.Property("cost", th.NumberType, required=True),
                th.Property("active", th.BooleanType, required=True),
                th.Property(
                    "primarySubAccount",
                    th.ObjectType(
                        th.Property("id", th.IntegerType, required=True),
                        th.Property("cost", th.NumberType, required=True),
                        th.Property("accountName", th.StringType, required=True),
                    ),
                    nullable=True,
                ),
                th.Property(
                    "otherSubAccounts",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("id", th.IntegerType, required=True),
                            th.Property("cost", th.NumberType, required=True),
                            th.Property("accountName", th.StringType, required=True),
                        )
                    ),
                    nullable=True,
                ),
            ),
            description="The primary vendor you use to acquire this SKU",
            nullable=True,
        ),
        th.Property(
            "otherVendors",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType, required=True),
                    th.Property("vendorName", th.StringType, required=True),
                    th.Property("vendorId", th.IntegerType, required=True),
                    th.Property("memo", th.StringType, nullable=True),
                    th.Property("vendorPart", th.StringType, nullable=True),
                    th.Property("cost", th.NumberType, required=True),
                    th.Property("active", th.BooleanType, required=True),
                    th.Property(
                        "primarySubAccount",
                        th.ObjectType(
                            th.Property("id", th.IntegerType, required=True),
                            th.Property("cost", th.NumberType, required=True),
                            th.Property("accountName", th.StringType, required=True),
                        ),
                        nullable=True,
                    ),
                    th.Property(
                        "otherSubAccounts",
                        th.ArrayType(
                            th.ObjectType(
                                th.Property("id", th.IntegerType, required=True),
                                th.Property("cost", th.NumberType, required=True),
                                th.Property(
                                    "accountName", th.StringType, required=True
                                ),
                            )
                        ),
                        nullable=True,
                    ),
                )
            ),
            description="Other vendors that you might go to acquire this SKU",
            nullable=True,
        ),
        th.Property(
            "account",
            th.StringType,
            description="The accounting account assigned to the SKU",
            nullable=True,
        ),
        th.Property("costOfSaleAccount", th.StringType, nullable=True),
        th.Property("assetAccount", th.StringType, nullable=True),
        th.Property(
            "crossSaleGroup",
            th.StringType,
            description="A grouping of similar items that you'll then be able to track as a separate columns on the Technical Performance Board.",  # noqa: E501
            nullable=True,
        ),
        th.Property(
            "paysCommission",
            th.BooleanType,
            description="PaysCommissions shows if this task pays commission",
            required=True,
        ),
        th.Property(
            "bonus",
            th.NumberType,
            description="Flat rate bonus paid for this task",
            required=True,
        ),
        th.Property(
            "commissionBonus",
            th.NumberType,
            description="Percentage rate bonus paid for this task",
            required=True,
        ),
        th.Property(
            "hours",
            th.NumberType,
            description="The number of hours associated with the installing the equipment",  # noqa: E501
            required=True,
        ),
        th.Property(
            "taxable", th.BooleanType, description="Is this SKU taxable", required=True
        ),
        th.Property(
            "cost",
            th.NumberType,
            description="The cost paid to acquire the material",
            required=True,
        ),
        th.Property(
            "unitOfMeasure",
            th.StringType,
            description="The unit of measure used for this SKU",
            nullable=True,
        ),
        th.Property(
            "isInventory",
            th.BooleanType,
            description="Is this equipment a part of your inventory",
            required=True,
        ),
        th.Property(
            "modifiedOn",
            th.DateTimeType,
            description="Timestamp where the item was last modified",
            required=True,
        ),
        th.Property(
            "source",
            th.StringType,
            description="The source catalog for this SKU.",
            nullable=True,
        ),
        th.Property(
            "externalId",
            th.StringType,
            description="External id is the id of the original source of the item when it comes from a catalog",  # noqa: E501
            nullable=True,
        ),
        th.Property(
            "externalData",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "key",
                        th.StringType,
                        description="External data key.",
                        required=True,
                    ),
                    th.Property(
                        "value",
                        th.StringType,
                        description="External data value.",
                        required=True,
                    ),
                )
            ),
            description="List of external data attached to this job, that corresponds to the application guid provided in the request.",  # noqa: E501
            nullable=True,
        ),
        th.Property(
            "isConfigurableEquipment",
            th.BooleanType,
            description="Shows if is a Configurable Equipment",
            required=True,
        ),
        th.Property(
            "variationsOrConfigurableEquipment",
            th.ArrayType(th.IntegerType),
            description="List of added Variations if is a Configurable Equipment, or else the List of Configurable Equipment assigned to",  # noqa: E501
            nullable=True,
        ),
        th.Property(
            "typeId",
            th.IntegerType,
            description="Shows Equipment's Type Id",
            nullable=True,
        ),
        th.Property(
            "displayInAmount",
            th.BooleanType,
            description="Shows if it should be displayed in the amount",
            required=True,
        ),
        th.Property(
            "generalLedgerAccountId",
            th.IntegerType,
            description="The General Ledger Account assigned to the SKU",
            nullable=True,
        ),
        th.Property(
            "createdOn",
            th.DateTimeType,
            description="Shows Equipment's Created On Date",
            required=True,
        ),
        th.Property(
            "defaultAssetUrl",
            th.StringType,
            description="Default Asset Url",
            nullable=True,
        ),
        th.Property(
            "dimensions",
            th.ObjectType(
                th.Property(
                    "height",
                    th.NumberType,
                    description="Height",
                    nullable=True,
                ),
                th.Property(
                    "width",
                    th.NumberType,
                    description="Width",
                    nullable=True,
                ),
                th.Property(
                    "depth",
                    th.NumberType,
                    description="Depth",
                    nullable=True,
                ),
            ),
            description="The equipment dimensions",
            nullable=True,
        ),
        th.Property(
            "budgetCostCode",
            th.StringType,
            description="The Budget CostCode segment for this entity. (Note: BudgetCostType should also be provided)",  # noqa: E501
            nullable=True,
        ),
        th.Property(
            "budgetCostType",
            th.StringType,
            description="The Budget CostType segment for this entity (Note: BudgetCostCode should also be provided)",  # noqa: E501
            nullable=True,
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/pricebook/v2/tenant/{self._tap.config['tenant_id']}/export/equipment"


class ExportMaterialsStream(ServiceTitanExportStream):
    """Define export materials stream."""

    name = "export_materials"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property(
            "id",
            th.IntegerType,
            description="Unique id for the SKU",
            required=True,
        ),
        th.Property(
            "code",
            th.StringType,
            description="Code for the SKU",
            required=True,
        ),
        th.Property(
            "displayName",
            th.StringType,
            description="Name that displays with the SKU",
            nullable=True,
        ),
        th.Property(
            "description",
            th.StringType,
            description="Description on the SKU that is displayed with the item",
            required=True,
        ),
        th.Property(
            "cost",
            th.NumberType,
            description="The cost paid to acquire the material",
            required=True,
        ),
        th.Property(
            "active",
            th.BooleanType,
            description="Active shows if the SKU is active or inactive",
            required=True,
        ),
        th.Property(
            "price", th.NumberType, description="Price of this SKU sold", required=True
        ),
        th.Property(
            "memberPrice",
            th.NumberType,
            description="The price if the item is sold to a member",
            required=True,
        ),
        th.Property(
            "addOnPrice",
            th.NumberType,
            description="The price of the SKU is sold as an add-on item",
            required=True,
        ),
        th.Property(
            "addOnMemberPrice",
            th.NumberType,
            description="The price if the SKU is sold to a member as an add-on item",
            required=True,
        ),
        th.Property(
            "hours",
            th.NumberType,
            description="The number of hours associated with the installing the material",  # noqa: E501
            required=True,
        ),
        th.Property(
            "bonus",
            th.NumberType,
            description="Flat rate bonus paid for this task",
            required=True,
        ),
        th.Property(
            "commissionBonus",
            th.NumberType,
            description="Percentage rate bonus paid for this task",
            required=True,
        ),
        th.Property(
            "paysCommission",
            th.BooleanType,
            description="PaysCommissions shows if this task pays commission",
            required=True,
        ),
        th.Property(
            "deductAsJobCost",
            th.BooleanType,
            description="Is this deducted as job cost",
            required=True,
        ),
        th.Property(
            "unitOfMeasure",
            th.StringType,
            description="The unit of measure used for this SKU",
            nullable=True,
        ),
        th.Property(
            "isInventory",
            th.BooleanType,
            description="Is this material a part of your inventory",
            required=True,
        ),
        th.Property(
            "account",
            th.StringType,
            description="The accounting account assigned to the SKU",
            nullable=True,
        ),
        th.Property("costOfSaleAccount", th.StringType, nullable=True),
        th.Property("assetAccount", th.StringType, nullable=True),
        th.Property(
            "taxable", th.BooleanType, description="Is this SKU taxable", nullable=True
        ),
        th.Property(
            "primaryVendor",
            th.ObjectType(
                th.Property("id", th.IntegerType, required=True),
                th.Property("vendorName", th.StringType, required=True),
                th.Property("vendorId", th.IntegerType, required=True),
                th.Property("memo", th.StringType, nullable=True),
                th.Property("vendorPart", th.StringType, nullable=True),
                th.Property("cost", th.NumberType, required=True),
                th.Property("active", th.BooleanType, required=True),
                th.Property(
                    "primarySubAccount",
                    th.ObjectType(
                        th.Property("id", th.IntegerType, required=True),
                        th.Property("cost", th.NumberType, required=True),
                        th.Property("accountName", th.StringType, required=True),
                    ),
                    nullable=True,
                ),
                th.Property(
                    "otherSubAccounts",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("id", th.IntegerType, required=True),
                            th.Property("cost", th.NumberType, required=True),
                            th.Property("accountName", th.StringType, required=True),
                        )
                    ),
                    nullable=True,
                ),
            ),
            nullable=True,
        ),
        th.Property(
            "otherVendors",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType, required=True),
                    th.Property("vendorName", th.StringType, required=True),
                    th.Property("vendorId", th.IntegerType, required=True),
                    th.Property("memo", th.StringType, nullable=True),
                    th.Property("vendorPart", th.StringType, nullable=True),
                    th.Property("cost", th.NumberType, required=True),
                    th.Property("active", th.BooleanType, required=True),
                    th.Property(
                        "primarySubAccount",
                        th.ObjectType(
                            th.Property("id", th.IntegerType, required=True),
                            th.Property("cost", th.NumberType, required=True),
                            th.Property("accountName", th.StringType, required=True),
                        ),
                        nullable=True,
                    ),
                    th.Property(
                        "otherSubAccounts",
                        th.ArrayType(
                            th.ObjectType(
                                th.Property("id", th.IntegerType, required=True),
                                th.Property("cost", th.NumberType, required=True),
                                th.Property(
                                    "accountName", th.StringType, required=True
                                ),
                            )
                        ),
                        nullable=True,
                    ),
                )
            ),
            nullable=True,
        ),
        th.Property(
            "categories",
            th.ArrayType(th.IntegerType),
            description="Categories that this SKU belongs to",
            required=True,
        ),
        th.Property(
            "assets",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "alias", th.StringType, description="Asset alias", nullable=True
                    ),
                    th.Property(
                        "fileName",
                        th.StringType,
                        description="Asset file name when downloaded",
                        nullable=True,
                    ),
                    th.Property(
                        "isDefault",
                        th.BooleanType,
                        description="It is the default asset",
                        required=True,
                    ),
                    th.Property(
                        "type",
                        th.StringType,
                        description="Asset type - image, video or PDF",
                        required=True,
                    ),
                    th.Property(
                        "url", th.StringType, description="Asset URL", required=True
                    ),
                )
            ),
            description="Images, videos or PDFs attached to SKU",
            required=True,
        ),
        th.Property(
            "modifiedOn",
            th.DateTimeType,
            description="Timestamp where the item was last modified",
            required=True,
        ),
        th.Property(
            "source",
            th.StringType,
            description="The source catalog for this SKU.",
            nullable=True,
        ),
        th.Property(
            "externalId",
            th.StringType,
            description="External id is the id of the original source of the item when it comes from a catalog",  # noqa: E501
            nullable=True,
        ),
        th.Property(
            "externalData",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "key",
                        th.StringType,
                        description="External data key.",
                        required=True,
                    ),
                    th.Property(
                        "value",
                        th.StringType,
                        description="External data value.",
                        required=True,
                    ),
                )
            ),
            description="List of external data attached to this job, that corresponds to the application guid provided in the request.",  # noqa: E501
            nullable=True,
        ),
        th.Property(
            "isConfigurableMaterial",
            th.BooleanType,
            description="Shows if is a Configurable Material",
            required=True,
        ),
        th.Property(
            "chargeableByDefault",
            th.BooleanType,
            description="Shows if material is going to be chargeable by default on Estimate or Invoice",  # noqa: E501
            required=True,
        ),
        th.Property(
            "variationsOrConfigurableMaterials",
            th.ArrayType(th.IntegerType),
            description="List of added Variations if is a Configurable Material, or else the List of Configurable Materials assigned to",  # noqa: E501
            nullable=True,
        ),
        th.Property(
            "businessUnitId",
            th.IntegerType,
            description="Material's business unit id",
            nullable=True,
        ),
        th.Property(
            "createdById",
            th.IntegerType,
            description="Material's created by user id",
            required=True,
        ),
        th.Property(
            "createdOn",
            th.DateTimeType,
            description="Date Material was created",
            required=True,
        ),
        th.Property(
            "displayInAmount",
            th.BooleanType,
            description="Shows if material is going to be displayed in amount",
            required=True,
        ),
        th.Property(
            "generalLedgerAccountId",
            th.IntegerType,
            description="Material's General Ledger Account Id",
            nullable=True,
        ),
        th.Property(
            "isOtherDirectCost",
            th.BooleanType,
            description="Shows if is Other Direct Cost",
            required=True,
        ),
        th.Property(
            "costTypeId",
            th.IntegerType,
            description="The Cost Type of this Other Direct Cost",
            nullable=True,
        ),
        th.Property(
            "defaultAssetUrl",
            th.StringType,
            description="Default Asset Url",
            nullable=True,
        ),
        th.Property(
            "budgetCostCode",
            th.StringType,
            description="The Budget CostCode segment for this entity. (Note: BudgetCostType should also be provided)",  # noqa: E501
            nullable=True,
        ),
        th.Property(
            "budgetCostType",
            th.StringType,
            description="The Budget CostType segment for this entity (Note: BudgetCostCode should also be provided)",  # noqa: E501
            nullable=True,
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/pricebook/v2/tenant/{self._tap.config['tenant_id']}/export/materials"


class ExportServicesStream(ServiceTitanExportStream):
    """Define export services stream."""

    name = "export_services"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key: str = "modifiedOn"

    schema = th.PropertiesList(
        th.Property(
            "id", th.IntegerType, description="Unique id for the SKU", required=True
        ),
        th.Property(
            "code", th.StringType, description="Code for the SKU", required=True
        ),
        th.Property(
            "displayName",
            th.StringType,
            description="Name that displays with the SKU",
            nullable=True,
        ),
        th.Property(
            "description",
            th.StringType,
            description="Description on the SKU that is displayed with the item",
            required=True,
        ),
        th.Property(
            "warranty",
            th.ObjectType(
                th.Property(
                    "duration",
                    th.IntegerType,
                    description="Warranty duration",
                    required=True,
                ),
                th.Property(
                    "description",
                    th.StringType,
                    description="Description of the warranty included in this SKU",
                    nullable=True,
                ),
            ),
            description="Warranty included with this SKU",
            nullable=True,
        ),
        th.Property(
            "categories",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "id",
                        th.IntegerType,
                        description="Unique Category Id",
                        required=True,
                    ),
                    th.Property(
                        "name",
                        th.StringType,
                        description="Category name",
                        required=True,
                    ),
                    th.Property(
                        "active",
                        th.BooleanType,
                        description="Active shows if the Category is active or inactive",  # noqa: E501
                        required=True,
                    ),
                )
            ),
            description="Categories that this SKU belongs to",
            required=True,
        ),
        th.Property(
            "price", th.NumberType, description="Price of this SKU sold", required=True
        ),
        th.Property(
            "memberPrice",
            th.NumberType,
            description="The price if the item is sold to a member",
            required=True,
        ),
        th.Property(
            "addOnPrice",
            th.NumberType,
            description="The price of the SKU is sold as an add-on item",
            required=True,
        ),
        th.Property(
            "addOnMemberPrice",
            th.NumberType,
            description="The price if the SKU is sold to a member as an add-on item",
            required=True,
        ),
        th.Property(
            "taxable", th.BooleanType, description="Is this SKU taxable", required=True
        ),
        th.Property(
            "account",
            th.StringType,
            description="The accounting account assigned to this SKU",
            nullable=True,
        ),
        th.Property(
            "hours",
            th.NumberType,
            description="Hours needed to complete this service",
            required=True,
        ),
        th.Property(
            "isLabor", th.BooleanType, description="Is a labor service", nullable=True
        ),
        th.Property(
            "recommendations",
            th.ArrayType(th.IntegerType),
            description="Recommended other service or materials to include with this SKU",  # noqa: E501
            required=True,
        ),
        th.Property(
            "upgrades",
            th.ArrayType(th.IntegerType),
            description="Upgrades that can be sold for this SKU",
            required=True,
        ),
        th.Property(
            "assets",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "alias", th.StringType, description="Asset alias", nullable=True
                    ),
                    th.Property(
                        "fileName",
                        th.StringType,
                        description="Asset file name when downloaded",
                        nullable=True,
                    ),
                    th.Property(
                        "isDefault",
                        th.BooleanType,
                        description="It is the default asset",
                        required=True,
                    ),
                    th.Property(
                        "type",
                        th.StringType,
                        description="Asset type - image, video or PDF",
                        required=True,
                    ),
                    th.Property(
                        "url", th.StringType, description="Asset URL", required=True
                    ),
                )
            ),
            description="Images, videos or PDFs attached to SKU",
            required=True,
        ),
        th.Property(
            "serviceMaterials",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "skuId",
                        th.IntegerType,
                        description="Linked SKU unique id",
                        required=True,
                    ),
                    th.Property(
                        "quantity",
                        th.NumberType,
                        description="Quantity of linked SKUs",
                        required=True,
                    ),
                )
            ),
            description="Array of materials that is used with this service",
            required=True,
        ),
        th.Property(
            "serviceEquipment",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "skuId",
                        th.IntegerType,
                        description="Linked SKU unique id",
                        required=True,
                    ),
                    th.Property(
                        "quantity",
                        th.NumberType,
                        description="Quantity of linked SKUs",
                        required=True,
                    ),
                )
            ),
            description="Array of equipment used with this service",
            required=True,
        ),
        th.Property(
            "active",
            th.BooleanType,
            description="Active shows if the SKU is active or inactive",
            required=True,
        ),
        th.Property(
            "crossSaleGroup",
            th.StringType,
            description="A grouping of similar items that you'll then be able to track as a separate columns on the Technical Performance Board.",  # noqa: E501
            nullable=True,
        ),
        th.Property(
            "paysCommission",
            th.BooleanType,
            description="PaysCommissions shows if this task pays commission",
            required=True,
        ),
        th.Property(
            "bonus",
            th.NumberType,
            description="Flat rate bonus paid for this task",
            required=True,
        ),
        th.Property(
            "commissionBonus",
            th.NumberType,
            description="Percentage rate bonus paid for this task",
            required=True,
        ),
        th.Property(
            "modifiedOn",
            th.DateTimeType,
            description="Timestamp when the item was last modified",
            required=True,
        ),
        th.Property(
            "source",
            th.StringType,
            description="The source catalog for this SKU.",
            nullable=True,
        ),
        th.Property(
            "externalId",
            th.StringType,
            description="External id is the id of the original source of the item when it comes from a catalog",  # noqa: E501
            nullable=True,
        ),
        th.Property(
            "externalData",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "key",
                        th.StringType,
                        description="External data key.",
                        required=True,
                    ),
                    th.Property(
                        "value",
                        th.StringType,
                        description="External data value.",
                        required=True,
                    ),
                )
            ),
            description="List of external data attached to this job, that corresponds to the application guid provided in the request.",  # noqa: E501
            nullable=True,
        ),
        th.Property(
            "businessUnitId",
            th.IntegerType,
            description="Service's Bussiness Unit Id",
            nullable=True,
        ),
        th.Property("cost", th.NumberType, description="Service Cost", required=True),
        th.Property(
            "createdOn",
            th.DateTimeType,
            description="Timestamp when the item was created",
            required=True,
        ),
        th.Property(
            "soldByCommission",
            th.NumberType,
            description="Sold by commission",
            required=True,
        ),
        th.Property(
            "defaultAssetUrl",
            th.StringType,
            description="Default Asset Url",
            nullable=True,
        ),
        th.Property(
            "budgetCostCode",
            th.StringType,
            description="The Budget CostCode segment for this entity. (Note: BudgetCostType should also be provided)",  # noqa: E501
            nullable=True,
        ),
        th.Property(
            "budgetCostType",
            th.StringType,
            description="The Budget CostType segment for this entity (Note: BudgetCostCode should also be provided)",  # noqa: E501
            nullable=True,
        ),
    ).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        return f"/pricebook/v2/tenant/{self._tap.config['tenant_id']}/export/services"
