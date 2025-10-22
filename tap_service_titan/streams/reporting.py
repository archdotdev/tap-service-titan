"""Custom report streams for the ServiceTitan tap."""

from __future__ import annotations

import math
import sys
import typing as t
from datetime import datetime, timedelta, timezone
from functools import cached_property

import requests
import requests.exceptions
from singer_sdk import typing as th
from singer_sdk.exceptions import RetriableAPIError
from singer_sdk.helpers import types  # noqa: TC002
from singer_sdk.helpers.types import Context  # noqa: TC002
from singer_sdk.streams.core import REPLICATION_FULL_TABLE, REPLICATION_INCREMENTAL

from tap_service_titan.client import ServiceTitanStream

if sys.version_info >= (3, 11):
    from http import HTTPMethod
else:
    from backports.httpmethod import HTTPMethod

if t.TYPE_CHECKING:
    from datetime import date

    from singer_sdk.streams.rest import _TToken


class CustomReports(ServiceTitanStream):
    """Define reviews stream."""

    name = "custom_report"
    http_method = HTTPMethod.POST
    replication_method = REPLICATION_FULL_TABLE
    is_sorted = True

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002 ANN003
        """Initialize the stream."""
        self._report = kwargs.pop("report")
        self._backfill_params = [
            obj["value"]
            for obj in self._report["parameters"]
            if obj["name"] == self._report.get("backfill_date_parameter", "")
        ]
        super().__init__(
            *args,
            **kwargs,
            name=f"custom_report_{self._report['report_name']}",
        )
        self._curr_backfill_date_param: date | None = None

    # This data is sorted but we use a lookback window to get overlapping historical
    # data. This causes the sort check to fail because the bookmark gets updated to
    # and older value than previously saved.
    @property
    def check_sorted(self) -> bool:
        """Check if stream is sorted.

        This setting enables additional checks which may trigger
        `InvalidStreamSortException` if records are found which are unsorted.

        Returns:
            `True` if sorting is checked. Defaults to `True`.
        """
        return False

    @property
    def curr_backfill_date_param(self) -> date | None:
        """Get current backfill date parameter."""
        # This is the first iteration.
        # Retrieve the backfill date parameter value for iterating.
        # We cant do this in the init due to timing with the state file.
        if len(self._backfill_params) == 1 and self._curr_backfill_date_param is None:
            self.replication_method = REPLICATION_INCREMENTAL
            self.replication_key = self._report["backfill_date_parameter"]
            self._curr_backfill_date_param = self._get_initial_date_param()
        return self._curr_backfill_date_param

    @curr_backfill_date_param.setter
    def curr_backfill_date_param(self, value: datetime) -> None:
        """Set  the current backfill date parameter."""
        self._curr_backfill_date_param = value

    def _get_initial_date_param(self) -> date | None:
        configured_date_param = datetime.strptime(  # noqa: DTZ007
            self._backfill_params[0],
            "%Y-%m-%d",
        ).date()
        bookmark = self.stream_state.get("replication_key_value")
        if bookmark:
            # Parse to a date and subtract the lookback window days if configured
            bookmark_dt = datetime.strptime(bookmark, "%Y-%m-%dT%H:%M:%S%z").date() - timedelta(
                days=self._report["lookback_window_days"]
            )
            return max(
                configured_date_param,
                bookmark_dt,
            )
        return configured_date_param

    @staticmethod
    def _get_datatype(string_type: str) -> th.JSONTypeHelper:  # noqa: ARG004
        # TODO: Use proper types once the API is fixed https://github.com/archdotdev/tap-service-titan/issues/67
        return th.StringType()
        # mapping = {
        #     # String , Number , Boolean , Date , Time
        #     "String": th.StringType(),
        #     "Number": th.NumberType(),
        #     "Boolean": th.BooleanType(),
        #     "Date": th.DateTimeType(),
        #     "Time": th.StringType(),
        # }
        # return mapping.get(string_type, th.StringType())

    def _get_report_metadata(self) -> dict:
        report_category = self._report["report_category"]
        report_id = self._report["report_id"]
        self.requests_session.auth = self.authenticator
        resp = self.requests_session.get(
            f"{self.url_base}/reporting/v2/tenant/{self.config['tenant_id']}/report-category/{report_category}/reports/{report_id}?pageSize=5000&page=1",
            headers=self.http_headers,
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
        msg = f"Available parameters for custom report `{self._report['report_name']}`: {metadata['parameters']}"  # noqa: E501
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
            f"/reporting/v2/tenant/{self.tenant_id}/report-category"
            f"/{report_category}/reports/{report_id}/data"
        )

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: _TToken | None,
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
        params["pageSize"] = 25000
        return params

    def prepare_request_payload(
        self,
        context: types.Context | None,  # noqa: ARG002
        next_page_token: _TToken | None,  # noqa: ARG002
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
        if self.curr_backfill_date_param:
            params = [
                param
                for param in self._report["parameters"]
                if param["name"] != self._report["backfill_date_parameter"]
            ]
            params.append(
                {
                    "name": self._report["backfill_date_parameter"],
                    "value": self.curr_backfill_date_param.strftime("%Y-%m-%d"),
                }
            )
            msg = f"Custom report request parameters {params}"
            self.logger.info(msg)
        return {"parameters": params}

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
            # TODO: Use proper types once the API is fixed https://github.com/archdotdev/tap-service-titan/issues/67
            string_record = [str(val) if val is not None else "" for val in record]
            data = dict(zip(field_names, string_record, strict=False))
            # Add the backfill date to the record if configured
            if "backfill_date_parameter" in self._report:
                data[self._report["backfill_date_parameter"]] = (
                    self.curr_backfill_date_param.strftime("%Y-%m-%d")  # type: ignore[union-attr]
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
        if self.curr_backfill_date_param is None:
            # No backfill date parameter, just get the records
            yield from super().get_records(context)
        else:
            while datetime.now(timezone.utc).date() >= self.curr_backfill_date_param:
                yield from super().get_records(context)
                # Increment date for next iteration
                self.curr_backfill_date_param = self.curr_backfill_date_param + timedelta(days=1)

    def backoff_wait_generator(self) -> t.Generator[float, None, None]:
        """Return a generator for backoff wait times."""

        def _backoff_from_headers(retriable_api_error: Exception) -> int:
            if (
                isinstance(
                    retriable_api_error,
                    (RetriableAPIError, requests.exceptions.HTTPError),
                )
                and retriable_api_error.response is not None
            ):
                response_headers = retriable_api_error.response.headers
                return math.ceil(float(response_headers.get("Retry-After", 0)))

            return 1

        return self.backoff_runtime(value=_backoff_from_headers)
