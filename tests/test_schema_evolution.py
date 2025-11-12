"""Test schema evolution."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from syrupy.extensions.json import JSONSnapshotExtension

if TYPE_CHECKING:
    from pathlib import Path

    import pytest
    from syrupy.assertion import SnapshotAssertion


def test_catalog_changes(
    pytester: pytest.Pytester,
    tmp_path: Path,
    snapshot: SnapshotAssertion,
    subtests: pytest.Subtests,
) -> None:
    """Fail if the catalog has changed."""
    snapshot_json = snapshot.with_defaults(extension_class=JSONSnapshotExtension)

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
            assert snapshot_json(name=stream_id) == stream
