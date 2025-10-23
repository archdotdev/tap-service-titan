"""Test pagination."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

import requests
import time_machine

from tap_service_titan.streams.dispatch import CapacitiesPaginator


def test_capacities_paginator() -> None:
    """Test capacities paginator."""
    fake_now = datetime(2025, 1, 25, tzinfo=timezone.utc)
    three_days_ago = fake_now - timedelta(days=3)
    seven_days_from_now = fake_now + timedelta(days=7)
    response = Mock(spec=requests.Response)

    with time_machine.travel(fake_now):
        paginator = CapacitiesPaginator(start_value=three_days_ago)

    # Should start at 3 days ago
    assert paginator.current_value == three_days_ago
    assert paginator.end_value == seven_days_from_now
    assert paginator.has_more(response=response)

    paginator.advance(response=response)
    assert paginator.current_value == three_days_ago + timedelta(days=1)
    assert paginator.has_more(response=response)

    for _ in range(10):  # from 3 days ago to 7 days from now
        paginator.advance(response=response)

    assert not paginator.has_more(response=response)

    # Final value should be 1 day after the end value
    assert paginator.current_value - paginator.end_value == timedelta(days=1)
