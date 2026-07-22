"""Tests for sport-agnostic team-bet snapshot builders (h2h, spreads, totals)."""

from datetime import datetime, timezone

import pytest

from builders.team_bets.h2h_snapshot_builder import H2hSnapshotBuilder
from builders.team_bets.spreads_snapshot_builder import SpreadsSnapshotBuilder
from builders.team_bets.totals_snapshot_builder import TotalsSnapshotBuilder
from schemas.team_bets import (
    NbaH2hSnapshotRecord,
    NbaSpreadsSnapshotRecord,
    NbaTotalsSnapshotRecord,
    NflH2hSnapshotRecord,
)
from schemas.team_bets.upstream_rows import (
    FeaturedOddsRow,
    TeamBetH2hHitRateRow,
    TeamBetSpreadsHitRateRow,
    TeamBetTotalsHitRateRow,
)

OBSERVATION_TIME = datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc)
CREATED_AT = datetime(2026, 7, 21, 12, 5, tzinfo=timezone.utc)
COMMENCE_TIME = datetime(2026, 7, 21, 23, 0, tzinfo=timezone.utc)


def _odds_row(**overrides) -> FeaturedOddsRow:
    defaults = {
        "event_id": "evt-1",
        "bookmaker": "draftkings",
        "market_key": "h2h",
        "outcome_name": "Boston Celtics",
        "sport_key": "basketball_nba",
        "commence_time": COMMENCE_TIME,
        "outcome_price": -110.0,
        "outcome_point": None,
        "market_last_update": datetime(2026, 7, 21, 11, 30, tzinfo=timezone.utc),
        "home_team": "Boston Celtics",
        "away_team": "Los Angeles Lakers",
        "home_team_id": 1,
        "away_team_id": 2,
    }
    defaults.update(overrides)
    return FeaturedOddsRow(**defaults)


def _h2h_hit_rate_row(**overrides) -> TeamBetH2hHitRateRow:
    defaults = {
        "event_id": "evt-1",
        "bookmaker": "draftkings",
        "market_key": "h2h",
        "outcome_name": "Boston Celtics",
        "market_last_update": datetime(2026, 7, 21, 11, 0, tzinfo=timezone.utc),
        "home_team": "Boston Celtics",
        "away_team": "Los Angeles Lakers",
        "home_team_id": 1,
        "away_team_id": 2,
        "outcome_team_id": 1,
        "last_n_wins": 7,
        "last_n_losses": 3,
        "last_n_sample": 10,
        "last_n_window": 10,
        "venue_wins": 4,
        "venue_losses": 1,
        "venue_sample": 5,
        "venue_window": 10,
        "venue_type": "home",
        "h2h_wins": 2,
        "h2h_losses": 1,
        "h2h_sample": 3,
        "h2h_window": 10,
    }
    defaults.update(overrides)
    return TeamBetH2hHitRateRow(**defaults)


def _spreads_hit_rate_row(**overrides) -> TeamBetSpreadsHitRateRow:
    defaults = {
        "event_id": "evt-1",
        "bookmaker": "draftkings",
        "market_key": "spreads",
        "outcome_name": "Boston Celtics",
        "market_last_update": datetime(2026, 7, 21, 11, 0, tzinfo=timezone.utc),
        "home_team": "Boston Celtics",
        "away_team": "Los Angeles Lakers",
        "home_team_id": 1,
        "away_team_id": 2,
        "outcome_team_id": 1,
        "spread": -3.5,
        "last_n_covers": 6,
        "last_n_sample": 10,
        "last_n_window": 10,
        "h2h_covers": 2,
        "h2h_sample": 3,
        "h2h_window": 10,
        "venue_covers": 4,
        "venue_sample": 5,
        "venue_window": 10,
        "venue_type": "home",
    }
    defaults.update(overrides)
    return TeamBetSpreadsHitRateRow(**defaults)


def _totals_hit_rate_row(**overrides) -> TeamBetTotalsHitRateRow:
    defaults = {
        "event_id": "evt-1",
        "bookmaker": "draftkings",
        "market_key": "totals",
        "outcome_name": "over",
        "market_last_update": datetime(2026, 7, 21, 11, 0, tzinfo=timezone.utc),
        "home_team": "Boston Celtics",
        "away_team": "Los Angeles Lakers",
        "home_team_id": 1,
        "away_team_id": 2,
        "direction": "over",
        "line": 224.5,
        "configured_window": 10,
        "home_team_clears": 6,
        "home_team_sample": 10,
        "away_team_clears": 5,
        "away_team_sample": 10,
        "h2h_window": 10,
        "h2h_sample": 3,
        "h2h_clears": 2,
        "h2h_avg_total": 218.3,
    }
    defaults.update(overrides)
    return TeamBetTotalsHitRateRow(**defaults)


class TestH2hSnapshotBuilder:
    def test_builds_nba_record_from_odds_and_hit_rate(self):
        builder = H2hSnapshotBuilder()

        record = builder.build(
            observation_time=OBSERVATION_TIME,
            odds=_odds_row(),
            hit_rate=_h2h_hit_rate_row(),
            record_cls=NbaH2hSnapshotRecord,
            created_at=CREATED_AT,
        )

        assert record is not None
        assert isinstance(record, NbaH2hSnapshotRecord)
        assert record.observation_time == OBSERVATION_TIME
        assert record.event_id == "evt-1"
        assert record.sport_key == "basketball_nba"
        assert record.market_key == "h2h"
        assert record.snapshot_version == "nba_h2h_v1"
        assert record.outcome_price == -110.0
        assert record.market_last_update == _odds_row().market_last_update
        assert record.hit_rate_market_last_update == _h2h_hit_rate_row().market_last_update
        assert record.outcome_team_id == 1
        assert record.last_n_wins == 7
        assert record.created_at == CREATED_AT

    def test_builds_nfl_record_for_same_builder(self):
        builder = H2hSnapshotBuilder()

        record = builder.build(
            observation_time=OBSERVATION_TIME,
            odds=_odds_row(
                sport_key="americanfootball_nfl",
                market_key="h2h",
                outcome_name="Kansas City Chiefs",
                home_team="Kansas City Chiefs",
                away_team="Buffalo Bills",
            ),
            hit_rate=_h2h_hit_rate_row(
                outcome_name="Kansas City Chiefs",
                home_team="Kansas City Chiefs",
                away_team="Buffalo Bills",
            ),
            record_cls=NflH2hSnapshotRecord,
            created_at=CREATED_AT,
        )

        assert record is not None
        assert record.sport_key == "americanfootball_nfl"
        assert record.snapshot_version == "nfl_h2h_v1"

    @pytest.mark.parametrize(
        "odds_overrides",
        [
            {"market_last_update": datetime(2026, 7, 21, 12, 1, tzinfo=timezone.utc)},
            {"commence_time": datetime(2026, 7, 21, 11, 0, tzinfo=timezone.utc)},
            {"bookmaker": "caesars"},
        ],
        ids=["odds_after_observation", "commence_before_observation", "disallowed_bookmaker"],
    )
    def test_returns_none_for_odds_leakage(self, odds_overrides):
        builder = H2hSnapshotBuilder()

        record = builder.build(
            observation_time=OBSERVATION_TIME,
            odds=_odds_row(**odds_overrides),
            hit_rate=_h2h_hit_rate_row(),
            record_cls=NbaH2hSnapshotRecord,
            created_at=CREATED_AT,
        )

        assert record is None

    def test_returns_none_when_hit_rate_after_observation_time(self):
        builder = H2hSnapshotBuilder()

        record = builder.build(
            observation_time=OBSERVATION_TIME,
            odds=_odds_row(),
            hit_rate=_h2h_hit_rate_row(
                market_last_update=datetime(2026, 7, 21, 12, 1, tzinfo=timezone.utc),
            ),
            record_cls=NbaH2hSnapshotRecord,
            created_at=CREATED_AT,
        )

        assert record is None

    def test_returns_none_on_join_key_mismatch(self):
        builder = H2hSnapshotBuilder()

        record = builder.build(
            observation_time=OBSERVATION_TIME,
            odds=_odds_row(),
            hit_rate=_h2h_hit_rate_row(event_id="evt-other"),
            record_cls=NbaH2hSnapshotRecord,
            created_at=CREATED_AT,
        )

        assert record is None


class TestSpreadsSnapshotBuilder:
    def test_builds_nba_record_when_spread_matches_outcome_point(self):
        builder = SpreadsSnapshotBuilder()

        record = builder.build(
            observation_time=OBSERVATION_TIME,
            odds=_odds_row(
                market_key="spreads",
                outcome_point=-3.5,
            ),
            hit_rate=_spreads_hit_rate_row(),
            record_cls=NbaSpreadsSnapshotRecord,
            created_at=CREATED_AT,
        )

        assert record is not None
        assert record.market_key == "spreads"
        assert record.outcome_point == -3.5
        assert record.spread == -3.5
        assert record.last_n_covers == 6

    def test_returns_none_when_spread_does_not_match_outcome_point(self):
        builder = SpreadsSnapshotBuilder()

        record = builder.build(
            observation_time=OBSERVATION_TIME,
            odds=_odds_row(
                market_key="spreads",
                outcome_point=-4.5,
            ),
            hit_rate=_spreads_hit_rate_row(spread=-3.5),
            record_cls=NbaSpreadsSnapshotRecord,
            created_at=CREATED_AT,
        )

        assert record is None


class TestTotalsSnapshotBuilder:
    def test_builds_nba_record_when_line_matches_outcome_point(self):
        builder = TotalsSnapshotBuilder()

        record = builder.build(
            observation_time=OBSERVATION_TIME,
            odds=_odds_row(
                market_key="totals",
                outcome_name="over",
                outcome_point=224.5,
            ),
            hit_rate=_totals_hit_rate_row(),
            record_cls=NbaTotalsSnapshotRecord,
            created_at=CREATED_AT,
        )

        assert record is not None
        assert record.market_key == "totals"
        assert record.outcome_point == 224.5
        assert record.line == 224.5
        assert record.direction == "over"
        assert record.outcome_team_id is None
        assert record.home_team_clears == 6

    def test_returns_none_when_line_does_not_match_outcome_point(self):
        builder = TotalsSnapshotBuilder()

        record = builder.build(
            observation_time=OBSERVATION_TIME,
            odds=_odds_row(
                market_key="totals",
                outcome_name="over",
                outcome_point=225.5,
            ),
            hit_rate=_totals_hit_rate_row(line=224.5),
            record_cls=NbaTotalsSnapshotRecord,
            created_at=CREATED_AT,
        )

        assert record is None

    def test_returns_none_when_outcome_name_direction_mismatch(self):
        builder = TotalsSnapshotBuilder()

        record = builder.build(
            observation_time=OBSERVATION_TIME,
            odds=_odds_row(
                market_key="totals",
                outcome_name="under",
                outcome_point=224.5,
            ),
            hit_rate=_totals_hit_rate_row(direction="over"),
            record_cls=NbaTotalsSnapshotRecord,
            created_at=CREATED_AT,
        )

        assert record is None
