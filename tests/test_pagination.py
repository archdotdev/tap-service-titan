"""Test pagination."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

import requests
import time_machine

from tap_service_titan.streams.dispatch import CapacitiesPaginator


def test_capacities_paginator_with_recent_start() -> None:
    """Test capacities paginator with recent start value (should use N-day lookback)."""
    fake_now = datetime(2025, 1, 25, tzinfo=timezone.utc)
    start_date = fake_now - timedelta(hours=1)
    response = Mock(spec=requests.Response)

    with time_machine.travel(fake_now):
        paginator = CapacitiesPaginator(start_value=start_date)

        # Initial value should be looking back `lookback_days` days from the current time
        assert (fake_now - paginator.current_value).days == paginator.lookback_days

        # Upper bound should be `lookahead_days` days from the current time
        assert (paginator.end_value - fake_now).days == paginator.lookahead_days
        assert paginator.has_more(response=response)

        paginator.advance(response=response)
        assert (paginator.current_value - fake_now).days == 1 - paginator.lookback_days
        assert paginator.has_more(response=response)

        # Advance through all remaining days to reach end_value
        for _ in range(paginator.lookahead_days + paginator.lookback_days - 1):
            paginator.advance(response=response)

        # After reaching end_value, should still have_more (because <= check)
        assert paginator.current_value == paginator.end_value
        assert paginator.has_more(response=response)

        # One more advance to go past end_value
        paginator.advance(response=response)
        assert not paginator.has_more(response=response)

        # Final value should be 1 day after the end value
        assert (paginator.current_value - paginator.end_value).days == 1


def test_capacities_paginator_with_old_start() -> None:
    """Test capacities paginator with old start value (should use provided start for backfill)."""
    fake_now = datetime(2025, 1, 25, tzinfo=timezone.utc)
    start_date = fake_now - timedelta(days=30)
    response = Mock(spec=requests.Response)

    with time_machine.travel(fake_now):
        paginator = CapacitiesPaginator(start_value=start_date)

        # Should start at 30 days ago (the provided value, not from the lookback days)
        assert paginator.current_value == start_date
        assert (paginator.end_value - fake_now).days == paginator.lookahead_days
        assert paginator.has_more(response=response)

        paginator.advance(response=response)
        assert paginator.current_value == start_date + timedelta(days=1)
        assert paginator.has_more(response=response)
