"""Unit tests for graded export INNER JOIN reads (mocked SQLAlchemy session)."""

from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from db.models.owned.nba_team_bet_h2h_grades import NbaTeamBetH2hGrade
from db.models.owned.nba_team_bet_h2h_pregame_snapshots import NbaTeamBetH2hPregameSnapshot
from repositories.team_bets._graded_export_reads import (
    apply_export_temporal_filters,
    fetch_graded_export_pairs,
)
from repositories.team_bets.team_bet_graded_export_read_repository import (
    TeamBetGradedExportReadRepository,
)
from schemas.export import GradedExportPair
from schemas.team_bets import NbaH2hGradeRecord, NbaH2hSnapshotRecord

OBSERVATION_TIME = datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc)
COMMENCE_TIME = datetime(2026, 7, 21, 23, 0, tzinfo=timezone.utc)
GRADED_AT = datetime(2026, 7, 22, 3, 0, tzinfo=timezone.utc)
CREATED_AT = datetime(2026, 7, 21, 12, 5, tzinfo=timezone.utc)


def _snapshot_orm(**overrides) -> NbaTeamBetH2hPregameSnapshot:
    defaults = {
        "observation_time": OBSERVATION_TIME,
        "event_id": "evt-1",
        "bookmaker": "draftkings",
        "outcome_name": "Boston Celtics",
        "snapshot_version": "nba_h2h_v1",
        "sport_key": "basketball_nba",
        "market_key": "h2h",
        "commence_time": COMMENCE_TIME,
        "outcome_point": None,
        "outcome_price": -110.0,
        "market_last_update": datetime(2026, 7, 21, 11, 30, tzinfo=timezone.utc),
        "home_team": "Boston Celtics",
        "away_team": "Los Angeles Lakers",
        "hit_rate_market_last_update": datetime(2026, 7, 21, 11, 0, tzinfo=timezone.utc),
        "created_at": CREATED_AT,
        "last_n_wins": 7,
        "last_n_losses": 3,
        "last_n_sample": 10,
        "last_n_window": 10,
    }
    defaults.update(overrides)
    return NbaTeamBetH2hPregameSnapshot(**defaults)


def _grade_orm(**overrides) -> NbaTeamBetH2hGrade:
    defaults = {
        "observation_time": OBSERVATION_TIME,
        "event_id": "evt-1",
        "bookmaker": "draftkings",
        "outcome_name": "Boston Celtics",
        "snapshot_version": "nba_h2h_v1",
        "sport_key": "basketball_nba",
        "market_key": "h2h",
        "grade_outcome": "win",
        "grade_version": "nba_h2h_grade_v1",
        "home_team_score": 112,
        "away_team_score": 105,
        "outcome_point": None,
        "commence_time": COMMENCE_TIME,
        "graded_at": GRADED_AT,
        "created_at": GRADED_AT,
    }
    defaults.update(overrides)
    return NbaTeamBetH2hGrade(**defaults)


def _mock_query_chain(db: MagicMock) -> MagicMock:
    chain = db.query.return_value.join.return_value
    chain.filter.return_value = chain
    return chain


class TestApplyExportTemporalFilters:
    def test_applies_no_filters_when_bounds_are_none(self):
        query = MagicMock()

        result = apply_export_temporal_filters(
            query,
            snapshot_model=NbaTeamBetH2hPregameSnapshot,
        )

        query.filter.assert_not_called()
        assert result is query

    @pytest.mark.parametrize(
        "kwargs",
        [
            pytest.param({"observation_time_start": OBSERVATION_TIME}, id="observation_start"),
            pytest.param({"observation_time_end": OBSERVATION_TIME}, id="observation_end"),
            pytest.param({"commence_time_start": COMMENCE_TIME}, id="commence_start"),
            pytest.param({"commence_time_end": COMMENCE_TIME}, id="commence_end"),
        ],
    )
    def test_applies_single_bound_filter(self, kwargs):
        query = MagicMock()
        query.filter.return_value = query

        apply_export_temporal_filters(
            query,
            snapshot_model=NbaTeamBetH2hPregameSnapshot,
            **kwargs,
        )

        query.filter.assert_called_once()

    def test_applies_all_bounds_when_provided(self):
        query = MagicMock()
        query.filter.return_value = query

        apply_export_temporal_filters(
            query,
            snapshot_model=NbaTeamBetH2hPregameSnapshot,
            observation_time_start=OBSERVATION_TIME,
            observation_time_end=OBSERVATION_TIME,
            commence_time_start=COMMENCE_TIME,
            commence_time_end=COMMENCE_TIME,
        )

        assert query.filter.call_count == 4


class TestFetchGradedExportPairs:
    def test_inner_join_returns_snapshot_and_grade_records(self):
        db = MagicMock()
        chain = _mock_query_chain(db)
        chain.all.return_value = [(_snapshot_orm(), _grade_orm())]

        pairs = fetch_graded_export_pairs(
            db,
            snapshot_model=NbaTeamBetH2hPregameSnapshot,
            grade_model=NbaTeamBetH2hGrade,
            snapshot_record_cls=NbaH2hSnapshotRecord,
            grade_record_cls=NbaH2hGradeRecord,
        )

        db.query.assert_called_once_with(
            NbaTeamBetH2hPregameSnapshot,
            NbaTeamBetH2hGrade,
        )
        db.query.return_value.join.assert_called_once()
        assert len(pairs) == 1
        assert isinstance(pairs[0], GradedExportPair)
        assert pairs[0].snapshot.event_id == "evt-1"
        assert pairs[0].grade.grade_outcome == "win"

    def test_passes_temporal_filters_to_query(self):
        db = MagicMock()
        chain = _mock_query_chain(db)
        chain.all.return_value = []

        fetch_graded_export_pairs(
            db,
            snapshot_model=NbaTeamBetH2hPregameSnapshot,
            grade_model=NbaTeamBetH2hGrade,
            snapshot_record_cls=NbaH2hSnapshotRecord,
            grade_record_cls=NbaH2hGradeRecord,
            observation_time_start=OBSERVATION_TIME,
            observation_time_end=OBSERVATION_TIME,
            commence_time_start=COMMENCE_TIME,
            commence_time_end=COMMENCE_TIME,
        )

        assert chain.filter.call_count == 4


class TestTeamBetGradedExportReadRepository:
    def test_fetch_graded_pairs_delegates_to_shared_helper(self):
        db = MagicMock()
        expected = [
            GradedExportPair(
                snapshot=NbaH2hSnapshotRecord.model_validate(_snapshot_orm()),
                grade=NbaH2hGradeRecord.model_validate(_grade_orm()),
            )
        ]
        repository = TeamBetGradedExportReadRepository(
            db,
            snapshot_model=NbaTeamBetH2hPregameSnapshot,
            grade_model=NbaTeamBetH2hGrade,
            snapshot_record_cls=NbaH2hSnapshotRecord,
            grade_record_cls=NbaH2hGradeRecord,
        )

        with patch(
            "repositories.team_bets.team_bet_graded_export_read_repository.fetch_graded_export_pairs",
            return_value=expected,
        ) as fetch_mock:
            pairs = repository.fetch_graded_pairs(
                observation_time_start=OBSERVATION_TIME,
                commence_time_end=COMMENCE_TIME,
            )

        assert pairs == expected
        fetch_mock.assert_called_once_with(
            db,
            snapshot_model=NbaTeamBetH2hPregameSnapshot,
            grade_model=NbaTeamBetH2hGrade,
            snapshot_record_cls=NbaH2hSnapshotRecord,
            grade_record_cls=NbaH2hGradeRecord,
            observation_time_start=OBSERVATION_TIME,
            observation_time_end=None,
            commence_time_start=None,
            commence_time_end=COMMENCE_TIME,
        )
