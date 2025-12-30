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
    start_date = fake_now - timedelta(days=30)
    response = Mock(spec=requests.Response)

    with time_machine.travel(fake_now):
        paginator = CapacitiesPaginator(start_value=start_date)

        # Should start at 30 days ago
        assert paginator.current_value == start_date
        assert (paginator.end_value - fake_now).days == paginator.lookahead_days
        assert paginator.has_more(response=response)

        # Advance through all remaining days to reach the end_value
        for _ in range(paginator.lookahead_days + 30):
            paginator.advance(response=response)

        # After reaching end_value, should still have_more (because <= check)
        assert paginator.current_value == paginator.end_value
        assert paginator.has_more(response=response)

        # One more advance to go past end_value
        paginator.advance(response=response)
        assert not paginator.has_more(response=response)

        # Final value should be 1 day after the end value
        assert (paginator.current_value - paginator.end_value).days == 1
