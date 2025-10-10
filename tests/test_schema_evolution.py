"""Test schema evolution."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    import pytest
    from pytest_snapshot.plugin import Snapshot


def test_catalog_changes(
    pytester: pytest.Pytester,
    snapshot: Snapshot,
    tmp_path: Path,
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
    catalog = json.loads("".join(result.outlines))
    pretty_catalog = json.dumps(catalog, indent=2)

    assert result.ret == 0, "Tap discovery failed"
    snapshot.assert_match(pretty_catalog, "catalog.json")
