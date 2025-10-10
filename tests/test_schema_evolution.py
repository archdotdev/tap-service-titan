"""Test schema evolution."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    import pytest
    from pytest_snapshot.plugin import Snapshot
    from pytest_subtests.plugin import SubTests


def test_catalog_changes(
    pytester: pytest.Pytester,
    tmp_path: Path,
    snapshot: Snapshot,
    subtests: SubTests,
) -> None:
    """Fail if the catalog has changed."""
    config = {
        "tenant_id": "1234567890",
        "client_id": "1234567890",
        "client_secret": "1234567890",
        "st_app_key": "1234567890",
        "api_url": "https://api-integration.servicetitan.io",
        "auth_url": "https://auth-integration.servicetitan.io/connect/token",
    }
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(config))

    result = pytester.run(
        "tap-service-titan",
        "--discover",
        "--config",
        config_path.as_posix(),
    )
    assert result.ret == 0, "Tap discovery failed"

    catalog = json.loads("".join(result.outlines))
    for stream in catalog["streams"]:
        stream_id = stream["tap_stream_id"]
        with subtests.test(stream_id):
            pretty_stream = json.dumps(stream, indent=2)
            snapshot.assert_match(pretty_stream, f"{stream_id}.json")
