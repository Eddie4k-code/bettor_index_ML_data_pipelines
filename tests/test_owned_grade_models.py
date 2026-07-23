"""Tests for owned team-bet grade SQLAlchemy models."""

import pytest
from sqlalchemy import create_engine, inspect

from db.db import create_owned_tables
from db.models import owned
from db.models.owned.cfb_team_bet_h2h_grades import CfbTeamBetH2hGrade
from db.models.owned.cfb_team_bet_spreads_grades import CfbTeamBetSpreadsGrade
from db.models.owned.cfb_team_bet_totals_grades import CfbTeamBetTotalsGrade
from db.models.owned.mlb_team_bet_h2h_grades import MlbTeamBetH2hGrade
from db.models.owned.mlb_team_bet_spreads_grades import MlbTeamBetSpreadsGrade
from db.models.owned.mlb_team_bet_totals_grades import MlbTeamBetTotalsGrade
from db.models.owned.nba_team_bet_h2h_grades import NbaTeamBetH2hGrade
from db.models.owned.nba_team_bet_spreads_grades import NbaTeamBetSpreadsGrade
from db.models.owned.nba_team_bet_totals_grades import NbaTeamBetTotalsGrade
from db.models.owned.nfl_team_bet_h2h_grades import NflTeamBetH2hGrade
from db.models.owned.nfl_team_bet_spreads_grades import NflTeamBetSpreadsGrade
from db.models.owned.nfl_team_bet_totals_grades import NflTeamBetTotalsGrade

GRADE_PK_COLUMNS = frozenset({
    "observation_time",
    "event_id",
    "bookmaker",
    "outcome_name",
    "snapshot_version",
})

GRADE_COLUMNS = GRADE_PK_COLUMNS | {
    "sport_key",
    "market_key",
    "grade_outcome",
    "grade_version",
    "home_team_score",
    "away_team_score",
    "outcome_point",
    "commence_time",
    "graded_at",
    "created_at",
}

OWNED_GRADE_TABLES = {
    NbaTeamBetH2hGrade: "nba_team_bet_h2h_grades",
    NbaTeamBetSpreadsGrade: "nba_team_bet_spreads_grades",
    NbaTeamBetTotalsGrade: "nba_team_bet_totals_grades",
    MlbTeamBetH2hGrade: "mlb_team_bet_h2h_grades",
    MlbTeamBetSpreadsGrade: "mlb_team_bet_spreads_grades",
    MlbTeamBetTotalsGrade: "mlb_team_bet_totals_grades",
    NflTeamBetH2hGrade: "nfl_team_bet_h2h_grades",
    NflTeamBetSpreadsGrade: "nfl_team_bet_spreads_grades",
    NflTeamBetTotalsGrade: "nfl_team_bet_totals_grades",
    CfbTeamBetH2hGrade: "cfb_team_bet_h2h_grades",
    CfbTeamBetSpreadsGrade: "cfb_team_bet_spreads_grades",
    CfbTeamBetTotalsGrade: "cfb_team_bet_totals_grades",
}

OWNED_GRADE_MODELS = [
    pytest.param(NbaTeamBetH2hGrade, "nba_team_bet_h2h_grades", id="nba_h2h"),
    pytest.param(NbaTeamBetSpreadsGrade, "nba_team_bet_spreads_grades", id="nba_spreads"),
    pytest.param(NbaTeamBetTotalsGrade, "nba_team_bet_totals_grades", id="nba_totals"),
    pytest.param(MlbTeamBetH2hGrade, "mlb_team_bet_h2h_grades", id="mlb_h2h"),
    pytest.param(MlbTeamBetSpreadsGrade, "mlb_team_bet_spreads_grades", id="mlb_spreads"),
    pytest.param(MlbTeamBetTotalsGrade, "mlb_team_bet_totals_grades", id="mlb_totals"),
    pytest.param(NflTeamBetH2hGrade, "nfl_team_bet_h2h_grades", id="nfl_h2h"),
    pytest.param(NflTeamBetSpreadsGrade, "nfl_team_bet_spreads_grades", id="nfl_spreads"),
    pytest.param(NflTeamBetTotalsGrade, "nfl_team_bet_totals_grades", id="nfl_totals"),
    pytest.param(CfbTeamBetH2hGrade, "cfb_team_bet_h2h_grades", id="cfb_h2h"),
    pytest.param(CfbTeamBetSpreadsGrade, "cfb_team_bet_spreads_grades", id="cfb_spreads"),
    pytest.param(CfbTeamBetTotalsGrade, "cfb_team_bet_totals_grades", id="cfb_totals"),
]


def test_owned_models_registry_includes_twelve_grade_models():
    assert len(OWNED_GRADE_TABLES) == 12
    assert set(OWNED_GRADE_TABLES).issubset(set(owned.OWNED_MODELS))


@pytest.mark.parametrize(("model_cls", "table_name"), OWNED_GRADE_MODELS)
def test_model_table_name(model_cls, table_name):
    assert model_cls.__tablename__ == table_name


@pytest.mark.parametrize(("model_cls", "table_name"), OWNED_GRADE_MODELS)
def test_model_primary_key_columns(model_cls, table_name):
    pk_columns = {column.name for column in model_cls.__table__.primary_key.columns}
    assert pk_columns == GRADE_PK_COLUMNS


@pytest.mark.parametrize(("model_cls", "table_name"), OWNED_GRADE_MODELS)
def test_model_has_grade_columns(model_cls, table_name):
    column_names = {column.name for column in model_cls.__table__.columns}
    assert column_names == GRADE_COLUMNS


def test_create_owned_tables_materializes_all_grade_tables():
    engine = create_engine("sqlite:///:memory:")
    create_owned_tables(engine)

    inspector = inspect(engine)
    assert set(OWNED_GRADE_TABLES.values()).issubset(set(inspector.get_table_names()))
