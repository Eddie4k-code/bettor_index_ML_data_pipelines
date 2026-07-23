"""Parametrized tests for explicit team-bet grade write repositories."""

import importlib
from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

OBSERVATION_TIME = datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc)


def _base_record_fields(**overrides):
    defaults = {
        "observation_time": OBSERVATION_TIME,
        "event_id": "evt-1",
        "bookmaker": "draftkings",
        "outcome_name": "Boston Celtics",
        "snapshot_version": "nba_h2h_v1",
        "grade_outcome": "win",
        "grade_version": "nba_h2h_grade_v1",
        "home_team_score": 110,
        "away_team_score": 102,
        "outcome_point": None,
        "commence_time": datetime(2026, 7, 21, 23, 0, tzinfo=timezone.utc),
        "graded_at": datetime(2026, 7, 22, 2, 0, tzinfo=timezone.utc),
        "created_at": datetime(2026, 7, 22, 2, 5, tzinfo=timezone.utc),
    }
    defaults.update(overrides)
    return defaults


GRADE_REPO_CASES = [
    pytest.param(
        "repositories.team_bets.nba_h2h_grade_repository",
        "NbaH2hGradeRepository",
        "schemas.team_bets.NbaH2hGradeRecord",
        "db.models.owned.nba_team_bet_h2h_grades.NbaTeamBetH2hGrade",
        "nba_h2h_v1",
        "nba_h2h_grade_v1",
        _base_record_fields(),
        id="nba_h2h",
    ),
    pytest.param(
        "repositories.team_bets.nba_spreads_grade_repository",
        "NbaSpreadsGradeRepository",
        "schemas.team_bets.NbaSpreadsGradeRecord",
        "db.models.owned.nba_team_bet_spreads_grades.NbaTeamBetSpreadsGrade",
        "nba_spreads_v1",
        "nba_spreads_grade_v1",
        _base_record_fields(
            snapshot_version="nba_spreads_v1",
            grade_version="nba_spreads_grade_v1",
            outcome_point=-3.5,
        ),
        id="nba_spreads",
    ),
    pytest.param(
        "repositories.team_bets.nba_totals_grade_repository",
        "NbaTotalsGradeRepository",
        "schemas.team_bets.NbaTotalsGradeRecord",
        "db.models.owned.nba_team_bet_totals_grades.NbaTeamBetTotalsGrade",
        "nba_totals_v1",
        "nba_totals_grade_v1",
        _base_record_fields(
            snapshot_version="nba_totals_v1",
            grade_version="nba_totals_grade_v1",
            outcome_name="Over",
            outcome_point=224.5,
        ),
        id="nba_totals",
    ),
    pytest.param(
        "repositories.team_bets.mlb_h2h_grade_repository",
        "MlbH2hGradeRepository",
        "schemas.team_bets.MlbH2hGradeRecord",
        "db.models.owned.mlb_team_bet_h2h_grades.MlbTeamBetH2hGrade",
        "mlb_h2h_v1",
        "mlb_h2h_grade_v1",
        _base_record_fields(
            snapshot_version="mlb_h2h_v1",
            grade_version="mlb_h2h_grade_v1",
        ),
        id="mlb_h2h",
    ),
    pytest.param(
        "repositories.team_bets.mlb_spreads_grade_repository",
        "MlbSpreadsGradeRepository",
        "schemas.team_bets.MlbSpreadsGradeRecord",
        "db.models.owned.mlb_team_bet_spreads_grades.MlbTeamBetSpreadsGrade",
        "mlb_spreads_v1",
        "mlb_spreads_grade_v1",
        _base_record_fields(
            snapshot_version="mlb_spreads_v1",
            grade_version="mlb_spreads_grade_v1",
            outcome_point=-1.5,
        ),
        id="mlb_spreads",
    ),
    pytest.param(
        "repositories.team_bets.mlb_totals_grade_repository",
        "MlbTotalsGradeRepository",
        "schemas.team_bets.MlbTotalsGradeRecord",
        "db.models.owned.mlb_team_bet_totals_grades.MlbTeamBetTotalsGrade",
        "mlb_totals_v1",
        "mlb_totals_grade_v1",
        _base_record_fields(
            snapshot_version="mlb_totals_v1",
            grade_version="mlb_totals_grade_v1",
            outcome_name="Over",
            outcome_point=8.5,
        ),
        id="mlb_totals",
    ),
    pytest.param(
        "repositories.team_bets.nfl_h2h_grade_repository",
        "NflH2hGradeRepository",
        "schemas.team_bets.NflH2hGradeRecord",
        "db.models.owned.nfl_team_bet_h2h_grades.NflTeamBetH2hGrade",
        "nfl_h2h_v1",
        "nfl_h2h_grade_v1",
        _base_record_fields(
            snapshot_version="nfl_h2h_v1",
            grade_version="nfl_h2h_grade_v1",
        ),
        id="nfl_h2h",
    ),
    pytest.param(
        "repositories.team_bets.nfl_spreads_grade_repository",
        "NflSpreadsGradeRepository",
        "schemas.team_bets.NflSpreadsGradeRecord",
        "db.models.owned.nfl_team_bet_spreads_grades.NflTeamBetSpreadsGrade",
        "nfl_spreads_v1",
        "nfl_spreads_grade_v1",
        _base_record_fields(
            snapshot_version="nfl_spreads_v1",
            grade_version="nfl_spreads_grade_v1",
            outcome_point=-3.5,
        ),
        id="nfl_spreads",
    ),
    pytest.param(
        "repositories.team_bets.nfl_totals_grade_repository",
        "NflTotalsGradeRepository",
        "schemas.team_bets.NflTotalsGradeRecord",
        "db.models.owned.nfl_team_bet_totals_grades.NflTeamBetTotalsGrade",
        "nfl_totals_v1",
        "nfl_totals_grade_v1",
        _base_record_fields(
            snapshot_version="nfl_totals_v1",
            grade_version="nfl_totals_grade_v1",
            outcome_name="Over",
            outcome_point=44.5,
        ),
        id="nfl_totals",
    ),
    pytest.param(
        "repositories.team_bets.cfb_h2h_grade_repository",
        "CfbH2hGradeRepository",
        "schemas.team_bets.CfbH2hGradeRecord",
        "db.models.owned.cfb_team_bet_h2h_grades.CfbTeamBetH2hGrade",
        "cfb_h2h_v1",
        "cfb_h2h_grade_v1",
        _base_record_fields(
            snapshot_version="cfb_h2h_v1",
            grade_version="cfb_h2h_grade_v1",
        ),
        id="cfb_h2h",
    ),
    pytest.param(
        "repositories.team_bets.cfb_spreads_grade_repository",
        "CfbSpreadsGradeRepository",
        "schemas.team_bets.CfbSpreadsGradeRecord",
        "db.models.owned.cfb_team_bet_spreads_grades.CfbTeamBetSpreadsGrade",
        "cfb_spreads_v1",
        "cfb_spreads_grade_v1",
        _base_record_fields(
            snapshot_version="cfb_spreads_v1",
            grade_version="cfb_spreads_grade_v1",
            outcome_point=-7.0,
        ),
        id="cfb_spreads",
    ),
    pytest.param(
        "repositories.team_bets.cfb_totals_grade_repository",
        "CfbTotalsGradeRepository",
        "schemas.team_bets.CfbTotalsGradeRecord",
        "db.models.owned.cfb_team_bet_totals_grades.CfbTeamBetTotalsGrade",
        "cfb_totals_v1",
        "cfb_totals_grade_v1",
        _base_record_fields(
            snapshot_version="cfb_totals_v1",
            grade_version="cfb_totals_grade_v1",
            outcome_name="Over",
            outcome_point=52.5,
        ),
        id="cfb_totals",
    ),
]


def _import_symbol(dotted_path: str):
    module_path, _, symbol = dotted_path.rpartition(".")
    module = importlib.import_module(module_path)
    return getattr(module, symbol)


@pytest.mark.parametrize(
    "repo_path,repo_cls,record_path,orm_path,snapshot_version,grade_version,record_fields",
    GRADE_REPO_CASES,
)
class TestTeamBetGradeRepositories:
    def test_insert_if_absent_returns_false_when_row_exists(
        self,
        repo_path,
        repo_cls,
        record_path,
        orm_path,
        snapshot_version,
        grade_version,
        record_fields,
    ):
        repository_cls = _import_symbol(f"{repo_path}.{repo_cls}")
        record_cls = _import_symbol(record_path)

        db = MagicMock()
        db.query.return_value.filter_by.return_value.first.return_value = MagicMock()

        inserted = repository_cls(db).insert_if_absent(record_cls(**record_fields))

        assert inserted is False
        db.add.assert_not_called()

    def test_insert_if_absent_persists_new_row(
        self,
        repo_path,
        repo_cls,
        record_path,
        orm_path,
        snapshot_version,
        grade_version,
        record_fields,
    ):
        repository_cls = _import_symbol(f"{repo_path}.{repo_cls}")
        record_cls = _import_symbol(record_path)
        orm_cls = _import_symbol(orm_path)

        db = MagicMock()
        db.query.return_value.filter_by.return_value.first.return_value = None

        inserted = repository_cls(db).insert_if_absent(record_cls(**record_fields))

        assert inserted is True
        db.add.assert_called_once()
        orm_row = db.add.call_args.args[0]
        assert isinstance(orm_row, orm_cls)
        assert orm_row.snapshot_version == snapshot_version
        assert orm_row.grade_version == grade_version
        db.commit.assert_called_once()
