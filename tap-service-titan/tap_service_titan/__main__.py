"""ServiceTitan entry point."""

from __future__ import annotations

from tap_service_titan.tap import TapServiceTitan

TapServiceTitan.cli()
