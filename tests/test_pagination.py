"""Test pagination."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

import requests
import time_machine

from tap_service_titan.streams.dispatch import CapacitiesPaginator


def test_capacities_paginator_with_recent_start() -> None:
    """Test capacities paginator with recent start value (should use 7-day lookback)."""
    fake_now = datetime(2025, 1, 25, tzinfo=timezone.utc)
    three_days_ago = fake_now - timedelta(days=3)
    seven_days_ago = fake_now - timedelta(days=7)
    seven_days_from_now = fake_now + timedelta(days=7)
    response = Mock(spec=requests.Response)

    with time_machine.travel(fake_now):
        paginator = CapacitiesPaginator(start_value=three_days_ago)

        # Should start at 7 days ago, not 3 days ago
        assert paginator.current_value == seven_days_ago
        assert paginator.end_value.replace(microsecond=0) == seven_days_from_now
        assert paginator.has_more(response=response)

        paginator.advance(response=response)
        assert paginator.current_value == seven_days_ago + timedelta(days=1)
        assert paginator.has_more(response=response)

        # Advance through all remaining days (13 more times to reach end_value)
        for _ in range(13):
            paginator.advance(response=response)

        # After reaching end_value, should still have_more (because <= check)
        assert paginator.current_value.replace(microsecond=0) == seven_days_from_now
        assert paginator.has_more(response=response)

        # One more advance to go past end_value
        paginator.advance(response=response)
        assert not paginator.has_more(response=response)

        # Final value should be 1 day after the end value (within microsecond precision)
        assert abs((paginator.current_value - paginator.end_value) - timedelta(days=1)) < timedelta(
            microseconds=1000
        )


def test_capacities_paginator_with_old_start() -> None:
    """Test capacities paginator with old start value (should use provided start for backfill)."""
    fake_now = datetime(2025, 1, 25, tzinfo=timezone.utc)
    thirty_days_ago = fake_now - timedelta(days=30)
    seven_days_from_now = fake_now + timedelta(days=7)
    response = Mock(spec=requests.Response)

    with time_machine.travel(fake_now):
        paginator = CapacitiesPaginator(start_value=thirty_days_ago)

        # Should start at 30 days ago (the provided value, not 7 days ago)
        assert paginator.current_value == thirty_days_ago
        assert paginator.end_value.replace(microsecond=0) == seven_days_from_now
        assert paginator.has_more(response=response)

        paginator.advance(response=response)
        assert paginator.current_value == thirty_days_ago + timedelta(days=1)
        assert paginator.has_more(response=response)
