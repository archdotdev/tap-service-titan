from tap_service_titan.client import ServiceTitanExportStream
import typing as t


class ApCreditsStream(ServiceTitanExportStream):
    """Define AP Credits stream."""

    name = "ap_credits"
    path = "/accounting/v2/tenant/{tenant}/export/ap-credits"
    primary_keys = ["id"]
    replication_key = "modifiedOn"
    schema = {
        "properties": {
            "id": {"type": ["null", "integer"]},
            "inventoryReturnId": {"type": ["null", "integer"]},
            "jobId": {"type": ["null", "integer"]},
            "active": {"type": ["null", "boolean"]},
            "createdOn": {"type": ["null", "string"], "format": "date-time"},
            "modifiedOn": {"type": ["null", "string"], "format": "date-time"},
            "date": {"type": ["null", "string"], "format": "date-time"},
            "canceledOn": {"type": ["null", "string"], "format": "date-time"},
            "number": {"type": ["null", "string"]},
            "referenceNumber": {"type": ["null", "string"]},
            "memo": {"type": ["null", "string"]},
            "amount": {"type": ["null", "number"]},
            "appliedAmount": {"type": ["null", "number"]},
            "status": {"type": ["null", "string"]},
            "syncStatus": {"type": ["null", "string"]},
            "batch": {
                "type": ["null", "object"],
                "properties": {
                    "id": {"type": ["null", "integer"]},
                    "number": {"type": ["null", "string"]},
                    "name": {"type": ["null", "string"]},
                },
            },
            "businessUnit": {
                "type": ["null", "object"],
                "properties": {
                    "id": {"type": ["null", "integer"]},
                    "name": {"type": ["null", "string"]},
                },
            },
            "remittanceVendor": {
                "type": ["null", "object"],
                "properties": {
                    "id": {"type": ["null", "integer"]},
                    "name": {"type": ["null", "string"]},
                },
            },
            "vendor": {
                "type": ["null", "object"],
                "properties": {
                    "id": {"type": ["null", "integer"]},
                    "name": {"type": ["null", "string"]},
                },
            },
            "paymentStatus": {"type": ["null", "string"]},
            "splits": {
                "type": ["null", "array"],
                "items": {
                    "type": ["null", "object"],
                    "properties": {
                        "id": {"type": ["null", "integer"]},
                        "active": {"type": ["null", "boolean"]},
                        "createdOn": {"type": ["null", "string"], "format": "date-time"},
                        "inventoryBillId": {"type": ["null", "integer"]},
                        "vendorCreditId": {"type": ["null", "integer"]},
                        "amount": {"type": ["null", "number"]},
                    },
                },
            },
        },
    }

    def get_child_context(self, record: dict, context: dict | None) -> dict:
        return {
            "ap_credit_id": record["id"],
        }
