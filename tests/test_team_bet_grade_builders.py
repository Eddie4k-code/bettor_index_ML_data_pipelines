"""Tests for sport-agnostic team-bet grade builders (h2h, spreads, totals)."""

from datetime import datetime, timezone

import pytest

from builders.team_bets.h2h_grade_builder import H2hGradeBuilder
from builders.team_bets.spreads_grade_builder import SpreadsGradeBuilder
from builders.team_bets.totals_grade_builder import TotalsGradeBuilder
from schemas.games import CompletedGameRow
from schemas.team_bets import (
    NbaH2hGradeRecord,
    NbaH2hSnapshotRecord,
    NbaSpreadsGradeRecord,
    NbaSpreadsSnapshotRecord,
    NbaTotalsGradeRecord,
    NbaTotalsSnapshotRecord,
    NflH2hGradeRecord,
)

OBSERVATION_TIME = datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc)
GRADED_AT = datetime(2026, 7, 22, 4, 0, tzinfo=timezone.utc)
CREATED_AT = datetime(2026, 7, 22, 4, 5, tzinfo=timezone.utc)
COMMENCE_TIME = datetime(2026, 7, 21, 23, 0, tzinfo=timezone.utc)
GAME_DATE = datetime(2026, 7, 21, 23, 30, tzinfo=timezone.utc)


def _completed_game(**overrides) -> CompletedGameRow:
    defaults = {
        "sport_key": "basketball_nba",
        "status": "finished",
        "home_team": "Boston Celtics",
        "away_team": "Los Angeles Lakers",
        "home_team_id": 1,
        "away_team_id": 2,
        "home_team_score": 112,
        "away_team_score": 105,
        "date": GAME_DATE,
    }
    defaults.update(overrides)
    return CompletedGameRow(**defaults)


def _h2h_snapshot(**overrides) -> NbaH2hSnapshotRecord:
    defaults = {
        "observation_time": OBSERVATION_TIME,
        "event_id": "evt-1",
        "bookmaker": "draftkings",
        "outcome_name": "Boston Celtics",
        "commence_time": COMMENCE_TIME,
        "outcome_point": None,
        "outcome_price": -110.0,
        "market_last_update": datetime(2026, 7, 21, 11, 30, tzinfo=timezone.utc),
        "home_team": "Boston Celtics",
        "away_team": "Los Angeles Lakers",
        "home_team_id": 1,
        "away_team_id": 2,
        "outcome_team_id": 1,
        "hit_rate_market_last_update": datetime(2026, 7, 21, 11, 0, tzinfo=timezone.utc),
        "created_at": datetime(2026, 7, 21, 12, 5, tzinfo=timezone.utc),
        "last_n_wins": 7,
        "last_n_losses": 3,
        "last_n_sample": 10,
        "last_n_window": 10,
    }
    defaults.update(overrides)
    return NbaH2hSnapshotRecord(**defaults)


def _spreads_snapshot(**overrides) -> NbaSpreadsSnapshotRecord:
    defaults = {
        "observation_time": OBSERVATION_TIME,
        "event_id": "evt-1",
        "bookmaker": "draftkings",
        "outcome_name": "Boston Celtics",
        "commence_time": COMMENCE_TIME,
        "outcome_point": -3.5,
        "outcome_price": -110.0,
        "market_last_update": datetime(2026, 7, 21, 11, 30, tzinfo=timezone.utc),
        "home_team": "Boston Celtics",
        "away_team": "Los Angeles Lakers",
        "home_team_id": 1,
        "away_team_id": 2,
        "outcome_team_id": 1,
        "hit_rate_market_last_update": datetime(2026, 7, 21, 11, 0, tzinfo=timezone.utc),
        "created_at": datetime(2026, 7, 21, 12, 5, tzinfo=timezone.utc),
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
    return NbaSpreadsSnapshotRecord(**defaults)


def _totals_snapshot(**overrides) -> NbaTotalsSnapshotRecord:
    defaults = {
        "observation_time": OBSERVATION_TIME,
        "event_id": "evt-1",
        "bookmaker": "draftkings",
        "outcome_name": "over",
        "commence_time": COMMENCE_TIME,
        "outcome_point": 217.5,
        "outcome_price": -110.0,
        "market_last_update": datetime(2026, 7, 21, 11, 30, tzinfo=timezone.utc),
        "home_team": "Boston Celtics",
        "away_team": "Los Angeles Lakers",
        "home_team_id": 1,
        "away_team_id": 2,
        "outcome_team_id": None,
        "hit_rate_market_last_update": datetime(2026, 7, 21, 11, 0, tzinfo=timezone.utc),
        "created_at": datetime(2026, 7, 21, 12, 5, tzinfo=timezone.utc),
        "direction": "over",
        "line": 217.5,
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
    return NbaTotalsSnapshotRecord(**defaults)


class TestH2hGradeBuilder:
    def test_grades_home_team_win(self):
        builder = H2hGradeBuilder()

        record = builder.build(
            snapshot=_h2h_snapshot(),
            game=_completed_game(),
            record_cls=NbaH2hGradeRecord,
            graded_at=GRADED_AT,
            created_at=CREATED_AT,
        )

        assert record is not None
        assert isinstance(record, NbaH2hGradeRecord)
        assert record.grade_outcome == "win"
        assert record.grade_version == "nba_h2h_grade_v1"
        assert record.home_team_score == 112
        assert record.away_team_score == 105
        assert record.observation_time == OBSERVATION_TIME
        assert record.event_id == "evt-1"
        assert record.graded_at == GRADED_AT

    def test_grades_home_team_loss(self):
        builder = H2hGradeBuilder()

        record = builder.build(
            snapshot=_h2h_snapshot(outcome_name="Los Angeles Lakers", outcome_team_id=2),
            game=_completed_game(),
            record_cls=NbaH2hGradeRecord,
            graded_at=GRADED_AT,
            created_at=CREATED_AT,
        )

        assert record is not None
        assert record.grade_outcome == "loss"

    def test_grades_push_on_tie(self):
        builder = H2hGradeBuilder()

        record = builder.build(
            snapshot=_h2h_snapshot(),
            game=_completed_game(home_team_score=105, away_team_score=105),
            record_cls=NbaH2hGradeRecord,
            graded_at=GRADED_AT,
            created_at=CREATED_AT,
        )

        assert record is not None
        assert record.grade_outcome == "push"

    def test_builds_nfl_record_for_same_builder(self):
        builder = H2hGradeBuilder()

        record = builder.build(
            snapshot=_h2h_snapshot(
                sport_key="americanfootball_nfl",
                market_key="h2h",
                snapshot_version="nfl_h2h_v1",
                outcome_name="Kansas City Chiefs",
                home_team="Kansas City Chiefs",
                away_team="Buffalo Bills",
            ),
            game=_completed_game(
                sport_key="americanfootball_nfl",
                status="final",
                home_team="Kansas City Chiefs",
                away_team="Buffalo Bills",
                home_team_score=24,
                away_team_score=17,
            ),
            record_cls=NflH2hGradeRecord,
            graded_at=GRADED_AT,
            created_at=CREATED_AT,
        )

        assert record is not None
        assert record.sport_key == "americanfootball_nfl"
        assert record.grade_version == "nfl_h2h_grade_v1"
        assert record.grade_outcome == "win"

    def test_returns_none_when_outcome_name_does_not_match_either_team(self):
        builder = H2hGradeBuilder()

        record = builder.build(
            snapshot=_h2h_snapshot(outcome_name="Golden State Warriors"),
            game=_completed_game(),
            record_cls=NbaH2hGradeRecord,
            graded_at=GRADED_AT,
            created_at=CREATED_AT,
        )

        assert record is None


class TestSpreadsGradeBuilder:
    def test_grades_cover_as_win(self):
        builder = SpreadsGradeBuilder()

        record = builder.build(
            snapshot=_spreads_snapshot(outcome_point=-3.5),
            game=_completed_game(home_team_score=112, away_team_score=105),
            record_cls=NbaSpreadsGradeRecord,
            graded_at=GRADED_AT,
            created_at=CREATED_AT,
        )

        assert record is not None
        assert record.grade_outcome == "win"
        assert record.outcome_point == -3.5

    def test_grades_non_cover_as_loss(self):
        builder = SpreadsGradeBuilder()

        record = builder.build(
            snapshot=_spreads_snapshot(outcome_point=-10.5),
            game=_completed_game(home_team_score=112, away_team_score=105),
            record_cls=NbaSpreadsGradeRecord,
            graded_at=GRADED_AT,
            created_at=CREATED_AT,
        )

        assert record is not None
        assert record.grade_outcome == "loss"

    def test_grades_push_when_margin_is_zero(self):
        builder = SpreadsGradeBuilder()

        record = builder.build(
            snapshot=_spreads_snapshot(outcome_point=-7.0),
            game=_completed_game(home_team_score=112, away_team_score=105),
            record_cls=NbaSpreadsGradeRecord,
            graded_at=GRADED_AT,
            created_at=CREATED_AT,
        )

        assert record is not None
        assert record.grade_outcome == "push"

    def test_returns_none_when_spread_missing(self):
        builder = SpreadsGradeBuilder()

        record = builder.build(
            snapshot=_spreads_snapshot(outcome_point=None, spread=-3.5),
            game=_completed_game(),
            record_cls=NbaSpreadsGradeRecord,
            graded_at=GRADED_AT,
            created_at=CREATED_AT,
        )

        assert record is None


class TestTotalsGradeBuilder:
    def test_grades_over_clear_as_win(self):
        builder = TotalsGradeBuilder()

        record = builder.build(
            snapshot=_totals_snapshot(outcome_name="over", outcome_point=216.5, line=216.5),
            game=_completed_game(home_team_score=112, away_team_score=105),
            record_cls=NbaTotalsGradeRecord,
            graded_at=GRADED_AT,
            created_at=CREATED_AT,
        )

        assert record is not None
        assert record.grade_outcome == "win"

    def test_grades_over_miss_as_loss(self):
        builder = TotalsGradeBuilder()

        record = builder.build(
            snapshot=_totals_snapshot(outcome_name="over", outcome_point=220.5, line=220.5),
            game=_completed_game(home_team_score=112, away_team_score=105),
            record_cls=NbaTotalsGradeRecord,
            graded_at=GRADED_AT,
            created_at=CREATED_AT,
        )

        assert record is not None
        assert record.grade_outcome == "loss"

    def test_grades_under_clear_as_win(self):
        builder = TotalsGradeBuilder()

        record = builder.build(
            snapshot=_totals_snapshot(
                outcome_name="under",
                direction="under",
                outcome_point=220.5,
                line=220.5,
            ),
            game=_completed_game(home_team_score=112, away_team_score=105),
            record_cls=NbaTotalsGradeRecord,
            graded_at=GRADED_AT,
            created_at=CREATED_AT,
        )

        assert record is not None
        assert record.grade_outcome == "win"

    def test_grades_push_when_total_equals_line(self):
        builder = TotalsGradeBuilder()

        record = builder.build(
            snapshot=_totals_snapshot(outcome_name="over", outcome_point=217.0, line=217.0),
            game=_completed_game(home_team_score=112, away_team_score=105),
            record_cls=NbaTotalsGradeRecord,
            graded_at=GRADED_AT,
            created_at=CREATED_AT,
        )

        assert record is not None
        assert record.grade_outcome == "push"

    def test_returns_none_for_invalid_direction(self):
        builder = TotalsGradeBuilder()

        record = builder.build(
            snapshot=_totals_snapshot(outcome_name="maybe", direction="maybe"),
            game=_completed_game(),
            record_cls=NbaTotalsGradeRecord,
            graded_at=GRADED_AT,
            created_at=CREATED_AT,
        )

        assert record is None
