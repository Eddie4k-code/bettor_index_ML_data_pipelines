"""Tests for shared team-bet snapshot request/result and base record fields."""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from schemas.snapshot import (
    ALLOWED_BOOKMAKERS,
    SnapshotRequest,
    SnapshotRunResult,
    TeamBetSnapshotRecordBase,
)


def _base_record_kwargs(**overrides):
    defaults = {
        "observation_time": datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc),
        "event_id": "evt-1",
        "sport_key": "basketball_nba",
        "market_key": "h2h",
        "bookmaker": "draftkings",
        "outcome_name": "Boston Celtics",
        "commence_time": datetime(2026, 7, 21, 23, 0, tzinfo=timezone.utc),
        "outcome_point": None,
        "outcome_price": -110.0,
        "market_last_update": datetime(2026, 7, 21, 11, 30, tzinfo=timezone.utc),
        "home_team": "Boston Celtics",
        "away_team": "Los Angeles Lakers",
        "home_team_id": 1,
        "away_team_id": 2,
        "outcome_team_id": 1,
        "hit_rate_market_last_update": datetime(2026, 7, 21, 11, 0, tzinfo=timezone.utc),
        "snapshot_version": "nba_h2h_v1",
        "created_at": datetime(2026, 7, 21, 12, 5, tzinfo=timezone.utc),
    }
    defaults.update(overrides)
    return defaults


def test_allowed_bookmakers_match_upstream_scope():
    assert ALLOWED_BOOKMAKERS == frozenset({
        "draftkings",
        "fanduel",
        "betmgm",
        "fanatics",
    })


def test_snapshot_request_normalizes_sport_key():
    request = SnapshotRequest(
        sport_key="FOOTBALL_NFL",
        market_key="spreads",
        observation_time=datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc),
    )

    assert request.normalized_sport_key == "americanfootball_nfl"


def test_snapshot_request_is_frozen():
    request = SnapshotRequest(
        sport_key="basketball_nba",
        market_key="h2h",
        observation_time=datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc),
    )

    with pytest.raises(ValidationError):
        request.sport_key = "baseball_mlb"


def test_team_bet_snapshot_record_base_accepts_required_fields():
    record = TeamBetSnapshotRecordBase(**_base_record_kwargs(season=2026))

    assert record.outcome_point is None
    assert record.season == 2026


def test_team_bet_snapshot_record_base_rejects_prop_only_fields():
    with pytest.raises(ValidationError):
        TeamBetSnapshotRecordBase(
            **_base_record_kwargs(
                player_id=99,
                player_team_id=1,
                outcome_description="Over 1.5",
            ),
        )


def test_snapshot_run_result_is_frozen():
    result = SnapshotRunResult(
        candidates=10,
        snapshotted=8,
        skipped_existing=1,
        skipped_leakage=1,
    )

    assert result.snapshotted == 8

    with pytest.raises(ValidationError):
        result.snapshotted = 9
