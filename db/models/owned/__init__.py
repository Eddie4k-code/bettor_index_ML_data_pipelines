"""Owned snapshot and grade tables for bettorindex_data_pipelines."""

from typing import Any

from db.models.owned.cfb_team_bet_h2h_grades import CfbTeamBetH2hGrade
from db.models.owned.cfb_team_bet_h2h_pregame_snapshots import CfbTeamBetH2hPregameSnapshot
from db.models.owned.cfb_team_bet_spreads_grades import CfbTeamBetSpreadsGrade
from db.models.owned.cfb_team_bet_spreads_pregame_snapshots import CfbTeamBetSpreadsPregameSnapshot
from db.models.owned.cfb_team_bet_totals_grades import CfbTeamBetTotalsGrade
from db.models.owned.cfb_team_bet_totals_pregame_snapshots import CfbTeamBetTotalsPregameSnapshot
from db.models.owned.mlb_team_bet_h2h_grades import MlbTeamBetH2hGrade
from db.models.owned.mlb_team_bet_h2h_pregame_snapshots import MlbTeamBetH2hPregameSnapshot
from db.models.owned.mlb_team_bet_spreads_grades import MlbTeamBetSpreadsGrade
from db.models.owned.mlb_team_bet_spreads_pregame_snapshots import MlbTeamBetSpreadsPregameSnapshot
from db.models.owned.mlb_team_bet_totals_grades import MlbTeamBetTotalsGrade
from db.models.owned.mlb_team_bet_totals_pregame_snapshots import MlbTeamBetTotalsPregameSnapshot
from db.models.owned.nba_team_bet_h2h_grades import NbaTeamBetH2hGrade
from db.models.owned.nba_team_bet_h2h_pregame_snapshots import NbaTeamBetH2hPregameSnapshot
from db.models.owned.nba_team_bet_spreads_grades import NbaTeamBetSpreadsGrade
from db.models.owned.nba_team_bet_spreads_pregame_snapshots import NbaTeamBetSpreadsPregameSnapshot
from db.models.owned.nba_team_bet_totals_grades import NbaTeamBetTotalsGrade
from db.models.owned.nba_team_bet_totals_pregame_snapshots import NbaTeamBetTotalsPregameSnapshot
from db.models.owned.nfl_team_bet_h2h_grades import NflTeamBetH2hGrade
from db.models.owned.nfl_team_bet_h2h_pregame_snapshots import NflTeamBetH2hPregameSnapshot
from db.models.owned.nfl_team_bet_spreads_grades import NflTeamBetSpreadsGrade
from db.models.owned.nfl_team_bet_spreads_pregame_snapshots import NflTeamBetSpreadsPregameSnapshot
from db.models.owned.nfl_team_bet_totals_grades import NflTeamBetTotalsGrade
from db.models.owned.nfl_team_bet_totals_pregame_snapshots import NflTeamBetTotalsPregameSnapshot

OWNED_MODELS: tuple[type[Any], ...] = (
    NbaTeamBetH2hPregameSnapshot,
    NbaTeamBetSpreadsPregameSnapshot,
    NbaTeamBetTotalsPregameSnapshot,
    MlbTeamBetH2hPregameSnapshot,
    MlbTeamBetSpreadsPregameSnapshot,
    MlbTeamBetTotalsPregameSnapshot,
    NflTeamBetH2hPregameSnapshot,
    NflTeamBetSpreadsPregameSnapshot,
    NflTeamBetTotalsPregameSnapshot,
    CfbTeamBetH2hPregameSnapshot,
    CfbTeamBetSpreadsPregameSnapshot,
    CfbTeamBetTotalsPregameSnapshot,
    NbaTeamBetH2hGrade,
    NbaTeamBetSpreadsGrade,
    NbaTeamBetTotalsGrade,
    MlbTeamBetH2hGrade,
    MlbTeamBetSpreadsGrade,
    MlbTeamBetTotalsGrade,
    NflTeamBetH2hGrade,
    NflTeamBetSpreadsGrade,
    NflTeamBetTotalsGrade,
    CfbTeamBetH2hGrade,
    CfbTeamBetSpreadsGrade,
    CfbTeamBetTotalsGrade,
)
