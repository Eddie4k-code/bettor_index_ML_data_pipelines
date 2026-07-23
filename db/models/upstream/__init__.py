"""Read-only mirrors of shared PostgreSQL tables (revised_engine / hit_rate_worker)."""

from db.models.upstream.games import Game
from db.models.upstream.mlb_hit_rates import MLBHitRates
from db.models.upstream.mlb_team_bet_hit_rates import MlbTeamBetHitRates
from db.models.upstream.mlb_team_bet_spreads_hit_rates import MlbTeamBetSpreadsHitRates
from db.models.upstream.mlb_team_bet_totals_hit_rates import MlbTeamBetTotalsHitRates
from db.models.upstream.nba_team_bet_hit_rates import NbaTeamBetHitRates
from db.models.upstream.nba_team_bet_spreads_hit_rates import NbaTeamBetSpreadsHitRates
from db.models.upstream.nba_team_bet_totals_hit_rates import NbaTeamBetTotalsHitRates
from db.models.upstream.nfl_team_bet_hit_rates import NflTeamBetHitRates
from db.models.upstream.nfl_team_bet_spreads_hit_rates import NflTeamBetSpreadsHitRates
from db.models.upstream.nfl_team_bet_totals_hit_rates import NflTeamBetTotalsHitRates
from db.models.upstream.odds_api_featured_odds import OddsAPIFeaturedOdds
from db.models.upstream.odds_api_prop import OddsAPIProp

__all__ = [
    "Game",
    "MLBHitRates",
    "MlbTeamBetHitRates",
    "MlbTeamBetSpreadsHitRates",
    "MlbTeamBetTotalsHitRates",
    "NbaTeamBetHitRates",
    "NbaTeamBetSpreadsHitRates",
    "NbaTeamBetTotalsHitRates",
    "NflTeamBetHitRates",
    "NflTeamBetSpreadsHitRates",
    "NflTeamBetTotalsHitRates",
    "OddsAPIFeaturedOdds",
    "OddsAPIProp",
]
