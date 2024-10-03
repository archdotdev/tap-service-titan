"""Stream type classes for tap-service-titan."""

from __future__ import annotations

import sys
import typing as t
from datetime import datetime, timedelta, timezone
from functools import cached_property

import backoff
import requests
from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk.helpers import types
from singer_sdk.helpers.types import Context
from singer_sdk.pagination import BaseAPIPaginator
from singer_sdk.streams.core import REPLICATION_FULL_TABLE, REPLICATION_INCREMENTAL

from tap_service_titan.client import (
    ServiceTitanStream,
)

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.streams.rest import _TToken

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources


class CustomReports(ServiceTitanStream):
    """Define reviews stream."""

    name = "custom_report"
    rest_method = "POST"
    replication_method = REPLICATION_FULL_TABLE

    def __init__(self, *args, **kwargs) -> None:
        self._report = kwargs.pop("report")
        # Retrieve the backfill date parameter value for iterating
        backfill_params = [
            obj["value"]
            for obj in self._report["parameters"]
            if obj["name"] == self._report.get("backfill_date_parameter", "")
        ]
        super().__init__(
            *args,
            **kwargs,
            name=f"custom_report_{self._report['report_name']}",
        )
        self._curr_backfill_date_param = None
        if len(backfill_params) == 1:
            self._curr_backfill_date_param = datetime.strptime(
                backfill_params[0], "%Y-%m-%d"
            ).date()
            self.replication_method = REPLICATION_INCREMENTAL
            self.replication_key = self._report["backfill_date_parameter"]

    @staticmethod
    def _get_datatype(string_type: str) -> th.JSONTypeHelper:
        mapping = {
            # String , Number , Boolean , Date , Time
            "String": th.StringType(),
            "Number": th.NumberType(),
            "Boolean": th.BooleanType(),
            "Date": th.DateTimeType(),
            "Time": th.StringType(),
        }
        return mapping.get(string_type, th.StringType())

    def _get_report_metadata(self) -> dict:
        report_category = self._report["report_category"]
        report_id = self._report["report_id"]
        resp = requests.get(
            f"{self.url_base}/reporting/v2/tenant/{self.config['tenant_id']}/report-category/{report_category}/reports/{report_id}?pageSize=5000&page=1",
            headers={**self.http_headers, **self.authenticator.auth_headers},
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return resp.json()

    @cached_property
    def schema(self) -> dict:
        """Get schema.

        Returns:
            JSON Schema dictionary for this stream.
        """
        metadata = self._get_report_metadata()
        msg = f"Available parameters for custom report `{self._report['report_name']}`: {metadata['parameters']}"
        self.logger.info(msg)
        properties: list[th.Property] = [
            th.Property(field["name"], self._get_datatype(field["dataType"]))
            for field in metadata["fields"]
        ]
        if self._report.get("backfill_date_parameter"):
            properties.append(
                th.Property(
                    self._report["backfill_date_parameter"],
                    th.DateTimeType(),
                )
            )
        return th.PropertiesList(*properties).to_dict()

    @cached_property
    def path(self) -> str:
        """Return the API path for the stream."""
        report_category = self._report["report_category"]
        report_id = self._report["report_id"]
        return (
            f"/reporting/v2/tenant/{self._tap.config['tenant_id']}/report-category"
            f"/{report_category}/reports/{report_id}/data"
        )

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params = super().get_url_params(context, next_page_token)
        params.pop("modifiedOnOrAfter", "")
        return params

    def prepare_request_payload(
        self,
        context: types.Context | None,
        next_page_token: _TToken | None,
    ) -> dict | None:
        """Prepare the data payload for the REST API request.

        By default, no payload will be sent (return None).

        Developers may override this method if the API requires a custom payload along
        with the request. (This is generally not required for APIs which use the
        HTTP 'GET' method.)

        Args:
            context: Stream partition or context dictionary.
            next_page_token: Token, page number or any request argument to request the
                next page of data.
        """
        params = self._report["parameters"]
        if self._curr_backfill_date_param:
            params = [
                param
                for param in self._report["parameters"]
                if param["name"] != self._report["backfill_date_parameter"]
            ]
            params.append(
                {
                    "name": self._report["backfill_date_parameter"],
                    "value": self._curr_backfill_date_param.strftime("%Y-%m-%d"),
                }
            )
        return {"parameters": self._report["parameters"]}

    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        resp = response.json()
        field_names = [field["name"] for field in resp["fields"]]
        for record in resp["data"]:
            data = dict(zip(field_names, record))
            # Add the backfill date to the record if configured
            if "backfill_date_parameter" in self._report:
                data[self._report["backfill_date_parameter"]] = (
                    self._curr_backfill_date_param.strftime("%Y-%m-%d")
                    + "T00:00:00-00:00"
                )
            yield data

    def get_records(self, context: Context | None) -> t.Iterable[dict[str, t.Any]]:
        """Return a generator of record-type dictionary objects.

        Each record emitted should be a dictionary of property names to their values.

        Args:
            context: Stream partition or context dictionary.

        Yields:
            One item per (possibly processed) record in the API.
        """
        if self._curr_backfill_date_param is None:
            # No backfill date parameter, just get the records
            yield from super().get_records(context)
        else:
            while datetime.now(timezone.utc).date() >= self._curr_backfill_date_param:
                yield from super().get_records(context)
                # Increment date for next iteration
                self._curr_backfill_date_param = (
                    self._curr_backfill_date_param + timedelta(days=1)
                )

    def backoff_wait_generator(self) -> t.Callable[..., t.Generator[int, t.Any, None]]:
        def _backoff_from_headers(retriable_api_error):
            response_headers = retriable_api_error.response.headers
            return int(response_headers.get("Retry-After", 0))

        return self.backoff_runtime(value=_backoff_from_headers)
